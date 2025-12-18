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

bundle = argv[1]
work = argv[2]
msg = argv[3]

if run(["git", "status", "--porcelain"], cwd=work, stdout=-1, text=True).stdout:
    run(["git", "config", "user.name", "codexcli-bot"], cwd=work, check=False)
    run(["git", "config", "user.email", "codexcli-bot@users.noreply.github.com"], cwd=work, check=False)
    run(["git", "add", "-A"], cwd=work, check=False)
    run(["git", "commit", "-m", msg], cwd=work, check=False)
    open(bundle + "/changed", "w", encoding="utf-8").write("1")
