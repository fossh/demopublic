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

codex_home_dir = argv[1]
session_id_path = codex_home_dir + "/session_id"
environ["CODEX_HOME"] = codex_home_dir

if exists(session_id_path):
    session_id = open(session_id_path, "r", encoding="utf-8").read().strip()
    if session_id:
        print(session_id)
        raise SystemExit

session_files = glob(codex_home_dir + "/sessions/**/*.jsonl", recursive=True)
if session_files:
    session_id = basename(max(session_files, key=getmtime))
    session_id = session_id[: session_id.rfind(".")][-36:]
    open(session_id_path, "w", encoding="utf-8").write(session_id)
    print(session_id)
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

session_files = glob(codex_home_dir + "/sessions/**/*.jsonl", recursive=True)
if session_files:
    session_id = basename(max(session_files, key=getmtime))
    session_id = session_id[: session_id.rfind(".")][-36:]
    open(session_id_path, "w", encoding="utf-8").write(session_id)
    print(session_id)
