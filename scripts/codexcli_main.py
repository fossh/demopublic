"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Trigger only on issue_comment events with `/codexcli`.
- Respond back by posting a GitHub comment.
- For PR comments: run Codex CLI, optionally push commits back.
- For issue comments: run Codex CLI, optionally open a PR with changes.
- No environment variable reads; use argv only.
"""

from json import load
from subprocess import run
from sys import argv

import requests

# ----------------------------------
# Inputs (passed by workflow)
# ----------------------------------
token = argv[1]
repo = argv[2]
event_path = argv[3]
run_url = argv[4]
h = {"Authorization": "token " + token}
api = "https://api.github.com/repos/" + repo

# ----------------------------------
# Load the GitHub event payload
# ----------------------------------
event = load(open(event_path, "rb"))
issue = event["issue"]
issue_number = issue["number"]

# ----------------------------------
# Only react to `/codexcli ...`
# ----------------------------------
text = event["comment"]["body"]
if not text.startswith("/codexcli"):
    raise SystemExit

request_text = text[9:] or "Help with this repository."

# ----------------------------------
# Run Codex CLI for the user request
# ----------------------------------
last = "/tmp/codexcli_last_message.txt"
run(
    ["codex", "-a", "never", "exec", "-s", "workspace-write", "-C", ".", "--color", "never", "-o", last, "-"],
    input=request_text,
    text=True,
)
try:
    msg = open(last, "r", encoding="utf-8").read()
except FileNotFoundError:
    msg = "codexcli ran."

# ----------------------------------
# If Codex changed files, commit + push (PR) or open PR (issue)
# ----------------------------------
changed = run(["git", "status", "--porcelain"], stdout=-1, text=True).stdout
pr_link = ""
if changed:
    run(
        [
            "bash",
            "-lc",
            "git config user.name codexcli-bot; "
            "git config user.email codexcli-bot@users.noreply.github.com; "
            "git add -A; "
            "git commit -m 'codexcli: %s'" % issue_number,
        ]
    )
    if "pull_request" in issue:
        pr = requests.get(issue["pull_request"]["url"], headers=h).json()
        if pr["head"]["repo"]["full_name"] == repo:
            run(["git", "push", "origin", f"HEAD:refs/heads/{pr['head']['ref']}"])
    else:
        branch = "codexcli/issue-%s-%s" % (issue_number, event["comment"]["id"])
        run(["git", "push", "origin", f"HEAD:refs/heads/{branch}"])
        pr_link = "https://github.com/" + repo + "/pull/new/" + branch
        pr_link = (
            requests.post(
                api + "/pulls",
                headers=h,
                json={
                    "title": f"codexcli: issue {issue_number}",
                    "head": branch,
                    "base": event["repository"]["default_branch"],
                    "body": msg[:60000],
                },
            ).json().get("html_url")
            or pr_link
        )

requests.post(
    api + "/issues/%s/comments" % issue_number,
    headers=h,
    json={
        "body": (
            (("PR: " + pr_link + "\n\n") if pr_link else "")
            + msg[:60000]
            + "\n\nRun: "
            + run_url
            + "\n"
        )
    },
)
