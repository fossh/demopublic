"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Update CODEX_HOME/session_id based on newest sessions/<id> directory.
- Must not read environment variables; use argv only.
"""

from glob import glob
from os.path import basename, getmtime
from sys import argv

# ----------------------------------
# Find newest session file and persist id
# ----------------------------------
h = argv[1]
fs = glob(h + "/sessions/**/*.jsonl", recursive=True)
if fs:
    s = basename(max(fs, key=getmtime))
    open(h + "/session_id", "w", encoding="utf-8").write(s[: s.rfind(".")][-36:])
