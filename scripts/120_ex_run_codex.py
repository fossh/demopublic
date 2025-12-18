"""
MUST HAVE REQUIREMENTS
- Script id: 120
- Standalone script (no local imports).
- Run Codex with `resume <session_id>` using bundle event comment text.
- Write output to `bundle/codex_output.txt`.
- Must not read environment variables; use argv only.
- Arguments: bundle dir, work dir.
"""

from json import load
from os import environ
from subprocess import run
from sys import argv

bundle_dir = argv[1]
work_dir = argv[2]
codex_home_dir = bundle_dir + "/codex_home"
environ["CODEX_HOME"] = codex_home_dir
session_id = open(codex_home_dir + "/session_id", "r", encoding="utf-8").read().strip()

event_payload = load(open(bundle_dir + "/event.json", "rb"))
comment_body = event_payload["comment"]["body"]
space_index = comment_body.find(" ")
prompt = (comment_body[space_index + 1 :] if space_index > 0 else "") or "Help with this repository."

cmd = [
    "codex",
    "exec",
    "-m",
    "gpt-5.2",
    "--config",
    "model_reasoning_effort=high",
    "--dangerously-bypass-approvals-and-sandbox",
    "--skip-git-repo-check",
    "resume",
    session_id,
    "-",
]
completed_process = run(cmd, input=prompt, text=True, capture_output=True, cwd=work_dir)
open(bundle_dir + "/codex_output.txt", "w", encoding="utf-8").write(
    (completed_process.stdout or completed_process.stderr or "codex ran.")[:60000]
)
