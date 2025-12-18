"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Create a `git worktree` for PR head at a given path.
- Must not read environment variables; use argv only.
"""

from subprocess import run
from sys import argv

# ----------------------------------
# Fetch PR head and create worktree
# ----------------------------------
run(["git", "fetch", "origin", "refs/pull/%s/head:codexcli_pr" % argv[1]], check=False)
run(["git", "worktree", "add", argv[2], "codexcli_pr"], check=False)

