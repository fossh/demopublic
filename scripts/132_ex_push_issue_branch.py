"""
MUST HAVE REQUIREMENTS
- Script id: 132
- Standalone script (no local imports).
- Push a branch for issue changes; write branch name to `bundle/branch`.
- Must not read environment variables; use argv only.
- Arguments: bundle dir, work dir.
"""

from json import load
from os.path import exists
from subprocess import run
from sys import argv

bundle_dir = argv[1]
work_dir = argv[2]
if not exists(bundle_dir + "/changed"):
    raise SystemExit

manifest = load(open(bundle_dir + "/manifest.json", "rb"))
event_payload = load(open(bundle_dir + "/event.json", "rb"))
issue_number = str(manifest["number"])
branch_name = "codex-v2/issue-%s-%s" % (issue_number, event_payload["comment"]["id"])
run(["git", "push", "origin", "HEAD:refs/heads/%s" % branch_name], cwd=work_dir, check=False)
open(bundle_dir + "/branch", "w", encoding="utf-8").write(branch_name)
