"""
MUST HAVE REQUIREMENTS
- Script id: 103
- Standalone script (no local imports).
- Create/refresh a `pr/` worktree at PR head.
- Must not read environment variables; use argv only.
"""

from json import load
from subprocess import run
from sys import argv

manifest = load(open(argv[1] + "/manifest.json", "rb"))
repo_dir = argv[2]
pr_number = str(manifest["number"])

run(["git", "-C", repo_dir, "fetch", "origin", "refs/pull/%s/head:codex_v2_pr" % pr_number], check=False)
run(["git", "-C", repo_dir, "worktree", "add", repo_dir + "/pr", "codex_v2_pr"], check=False)
