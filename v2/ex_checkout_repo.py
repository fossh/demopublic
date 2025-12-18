"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Ensure repo checkout exists at the given path (clone or fetch).
- Must not read environment variables; use argv only.
"""

from json import load
from subprocess import run
from sys import argv

m = load(open(argv[1] + "/manifest.json", "rb"))
repo_dir = argv[2]

if run(["git", "-C", repo_dir, "rev-parse", "--is-inside-work-tree"], stdout=-1).returncode:
    run(["git", "clone", "https://github.com/%s.git" % m["repo"], repo_dir], check=False)
run(["git", "-C", repo_dir, "fetch", "origin", "--prune"], check=False)

