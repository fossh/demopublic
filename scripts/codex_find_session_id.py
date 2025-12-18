"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Print the best session id for CODEX_HOME.
- Must not read environment variables; use argv only.
"""

from os import listdir
from os.path import exists, getmtime, isdir
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
# Fallback: newest sessions/<id> directory
# ----------------------------------
d = argv[1] + "/sessions"
try:
    ds = listdir(d)
except FileNotFoundError:
    raise SystemExit
ds = [x for x in ds if isdir(d + "/" + x)]
if ds:
    print(max(ds, key=lambda x: getmtime(d + "/" + x)))

