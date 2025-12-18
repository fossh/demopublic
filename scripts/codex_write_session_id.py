"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Update CODEX_HOME/session_id based on newest sessions/<id> directory.
- Must not read environment variables; use argv only.
"""

from os import listdir
from os.path import getmtime, isdir
from sys import argv

# ----------------------------------
# Find newest session directory
# ----------------------------------
h = argv[1]
d = h + "/sessions"
try:
    ds = listdir(d)
except FileNotFoundError:
    raise SystemExit
ds = [x for x in ds if isdir(d + "/" + x)]
if ds:
    open(h + "/session_id", "w", encoding="utf-8").write(max(ds, key=lambda x: getmtime(d + "/" + x)))

