"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Trigger only on issue_comment events with `/codexcli`.
- Respond back by posting a GitHub comment.
- For PR comments: run Codex CLI review and post the output.
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

# ----------------------------------
# Load the GitHub event payload
# ----------------------------------
event = load(open(event_path, "rb"))
comment = event["comment"]

# ----------------------------------
# Only react to `/codexcli ...`
# ----------------------------------
text = comment["body"]
if not text.startswith("/codexcli"):
    raise SystemExit

request_text = text[9:]
issue_number = event["issue"]["number"]

prompt = (
    request_text if request_text else "Review this PR and call out the most important issues."
)

cp = run(["codex", "review", "-"], input=prompt, text=True, capture_output=True)
review = cp.stdout or cp.stderr

requests.post(
    f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments",
    headers={"Authorization": f"Bearer {token}"},
    json={"body": (review[:60000] + "\n\n" if review else "codexcli ran.\n\n") + f"Run: {run_url}\n"},
)
