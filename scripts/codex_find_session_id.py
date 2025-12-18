"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Print the best session id for CODEX_HOME.
- Must not read environment variables; use argv only.
"""

from os.path import basename, exists, getmtime
from glob import glob
from sys import argv

# ----------------------------------
# Prefer explicit session id file
# ----------------------------------
p = argv[1] + "/session_id"
if exists(p):
    s = open(p, "r", encoding="utf-8").read().strip()
    if s:
        print(s)
        raise SystemExit

# ----------------------------------
# Fallback: newest sessions/**/*.jsonl file => last 36 chars
# ----------------------------------
fs = glob(argv[1] + "/sessions/**/*.jsonl", recursive=True)
if fs:
    s = basename(max(fs, key=getmtime))
    print(s[: s.rfind(".")][-36:])
