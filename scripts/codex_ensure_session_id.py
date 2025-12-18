"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- If CODEX_HOME has no session id yet, generate one by running Codex once.
- Print the session id (UUID).
- Must not read environment variables; use argv only.
"""

from glob import glob
from os.path import basename, exists, getmtime
from subprocess import DEVNULL, run
from sys import argv

h = argv[1]
p = h + "/session_id"

# ----------------------------------
# Find existing session id
# ----------------------------------
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

# ----------------------------------
# Generate a session (one cheap Codex call)
# ----------------------------------
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

