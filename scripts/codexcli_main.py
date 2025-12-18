"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Trigger only on issue_comment events with `/codexcli`.
- Respond back by posting a GitHub comment.
- For PR comments: run Codex CLI, optionally push commits back.
- For issue comments: run Codex CLI, optionally open a PR with changes.
- No environment variable reads; use argv only.
- Resume prior Codex session when a session id is provided.
- Work without GitHub runner (argv-only inputs).
"""

from glob import glob
from json import load
from os import environ, makedirs
from os.path import basename, exists, getmtime
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
codex_home = argv[5]
s3_bucket = argv[6]
aws_access_key_id = argv[7]
aws_secret_access_key = argv[8]
aws_region = argv[9]
codex_auth_json_path = argv[10]
h = {"Authorization": "token " + token}
api = "https://api.github.com/repos/" + repo

# ----------------------------------
# Configure env for aws/codex from argv
# ----------------------------------
environ["CODEX_HOME"] = codex_home
if aws_access_key_id:
    environ["AWS_ACCESS_KEY_ID"] = aws_access_key_id
if aws_secret_access_key:
    environ["AWS_SECRET_ACCESS_KEY"] = aws_secret_access_key
if aws_region:
    environ["AWS_DEFAULT_REGION"] = aws_region

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
# Restore CODEX_HOME from S3 (optional)
# ----------------------------------
makedirs(codex_home, exist_ok=True)
open(codex_home + "/auth.json", "wb").write(open(codex_auth_json_path, "rb").read())
repo_name = repo.rsplit("/", 1)[1]
kind = "prs" if "pull_request" in issue else "issues"
prefix = f"s3://{s3_bucket}/{repo_name}/{kind}/{issue_number}/"
if s3_bucket:
    if run(["aws", "s3", "sync", prefix, codex_home, "--exclude", "auth.json"]).returncode:
        raise SystemExit(2)

# ----------------------------------
# Fail fast if more than one session id exists
# ----------------------------------
fs = glob(codex_home + "/sessions/**/*.jsonl", recursive=True)
if fs and len({basename(f)[-41:-5] for f in fs}) > 1:
    raise SystemExit(3)

# ----------------------------------
# Ensure a session id exists (bootstrap if needed)
# ----------------------------------
sid_path = codex_home + "/session_id"
session_id = ""
if exists(sid_path):
    session_id = open(sid_path, "r", encoding="utf-8").read().strip()
if not session_id and fs:
    s = basename(max(fs, key=getmtime))
    session_id = s[: s.rfind(".")][-36:]
if not session_id:
    run(
        [
            "codex",
            "exec",
            "-m",
            "gpt-5.2",
            "--config",
            "model_reasoning_effort=high",
            "--dangerously-bypass-approvals-and-sandbox",
            "--skip-git-repo-check",
            "-",
        ],
        input="say hi",
        text=True,
    )
    fs = glob(codex_home + "/sessions/**/*.jsonl", recursive=True)
    if fs:
        s = basename(max(fs, key=getmtime))
        session_id = s[: s.rfind(".")][-36:]
open(sid_path, "w", encoding="utf-8").write(session_id)

# ----------------------------------
# Run Codex CLI for the user request
# ----------------------------------
cmd = [
    "codex",
    "exec",
    "-m",
    "gpt-5.2",
    "--config",
    "model_reasoning_effort=high",
    "--dangerously-bypass-approvals-and-sandbox",
    "--skip-git-repo-check",
]
cmd += ["resume", session_id]
cmd += ["-"]
cp = run(cmd, input=request_text, text=True, capture_output=True)
msg = cp.stdout or cp.stderr or "codexcli ran."

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
            "session: " + session_id + "\n\n"
            + (("PR: " + pr_link + "\n\n") if pr_link else "")
            + msg[:60000]
            + "\n\nRun: "
            + run_url
            + "\n"
        )
    },
)

# ----------------------------------
# Save CODEX_HOME to S3 (optional)
# ----------------------------------
if s3_bucket:
    run(["aws", "s3", "sync", codex_home, prefix, "--exclude", "auth.json"])
