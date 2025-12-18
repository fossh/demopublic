"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Push a branch for issue changes; write branch name to `bundle/branch`.
- Must not read environment variables; use argv only.
"""

from json import load
from os.path import exists
from subprocess import run
from sys import argv

b = argv[1]
work = argv[2]
if not exists(b + "/changed"):
    raise SystemExit

m = load(open(b + "/manifest.json", "rb"))
e = load(open(b + "/event.json", "rb"))
n = str(m["number"])
branch = "codex-v2/issue-%s-%s" % (n, e["comment"]["id"])
run(["git", "push", "origin", "HEAD:refs/heads/%s" % branch], cwd=work, check=False)
open(b + "/branch", "w", encoding="utf-8").write(branch)

