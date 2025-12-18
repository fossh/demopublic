"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Run Codex with `resume <session_id>` using bundle event comment text.
- Write output to `bundle/codex_output.txt`.
- Must not read environment variables; use argv only.
"""

from json import load
from os import environ
from subprocess import run
from sys import argv

b = argv[1]
work = argv[2]
h = b + "/codex_home"
environ["CODEX_HOME"] = h
sid = open(h + "/session_id", "r", encoding="utf-8").read().strip()

event = load(open(b + "/event.json", "rb"))
t = event["comment"]["body"]
i = t.find(" ")
prompt = (t[i + 1 :] if i > 0 else "") or "Help with this repository."

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
    sid,
    "-",
]
cp = run(cmd, input=prompt, text=True, capture_output=True, cwd=work)
open(b + "/codex_output.txt", "w", encoding="utf-8").write((cp.stdout or cp.stderr or "codex ran.")[:60000])
