"""
MUST HAVE REQUIREMENTS
- Script id: 130
- Standalone script (no local imports).
- If there are git changes, commit them.
- If a commit happened, write `bundle/changed`.
- Must not read environment variables; use argv only.
"""

from subprocess import run
from sys import argv

bundle_dir = argv[1]
work_dir = argv[2]
commit_message = argv[3]

if run(["git", "status", "--porcelain"], cwd=work_dir, stdout=-1, text=True).stdout:
    run(["git", "config", "user.name", "codexcli-bot"], cwd=work_dir, check=False)
    run(["git", "config", "user.email", "codexcli-bot@users.noreply.github.com"], cwd=work_dir, check=False)
    run(["git", "add", "-A"], cwd=work_dir, check=False)
    run(["git", "commit", "-m", commit_message], cwd=work_dir, check=False)
    open(bundle_dir + "/changed", "w", encoding="utf-8").write("1")
