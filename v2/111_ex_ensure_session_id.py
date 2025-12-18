"""
MUST HAVE REQUIREMENTS
- Script id: 111
- Standalone script (no local imports).
- Ensure CODEX_HOME has a session id (bootstrap by running Codex once).
- Print session id.
- Must not read environment variables; use argv only.
"""

from glob import glob
from os import environ
from os.path import basename, exists, getmtime
from subprocess import DEVNULL, run
from sys import argv

h = argv[1]
p = h + "/session_id"
environ["CODEX_HOME"] = h

if exists(p):
    s = open(p, "r", encoding="utf-8").read().strip()
    if s:
        print(s)
        raise SystemExit

fs = glob(h + "/sessions/**/*.jsonl", recursive=True)
if fs:
    s = basename(max(fs, key=getmtime))
    s = s[: s.rfind(".")][-36:]
    open(p, "w", encoding="utf-8").write(s)
    print(s)
    raise SystemExit

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
    stdout=DEVNULL,
    stderr=DEVNULL,
)

fs = glob(h + "/sessions/**/*.jsonl", recursive=True)
if fs:
    s = basename(max(fs, key=getmtime))
    s = s[: s.rfind(".")][-36:]
    open(p, "w", encoding="utf-8").write(s)
    print(s)
