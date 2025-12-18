"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Run `scripts/codexcli_main.py` using a captured bundle directory.
- Allow overriding S3 bucket used by the bundle (to avoid touching production).
- Must not read environment variables; use argv only.
"""

from json import load
from os.path import exists
from subprocess import run
from sys import argv

# ----------------------------------
# Inputs
# ----------------------------------
bundle = argv[1]
repo_dir = argv[2]
codex_pkg = argv[3]
s3_bucket = argv[4] if len(argv) > 4 else ""

# ----------------------------------
# Ensure repo checkout exists (clone if needed)
# ----------------------------------
meta = load(open(bundle + "/meta.json", "rb"))
repo = meta["repo"]
if not exists(repo_dir + "/.git"):
    run(["git", "clone", "https://github.com/%s.git" % repo, repo_dir], check=False)

# ----------------------------------
# Fetch + select working directory
# ----------------------------------
run(["git", "-C", repo_dir, "fetch", "origin", "--prune"], check=False)
work = repo_dir
if meta["kind"] == "prs":
    run(
        ["python3", repo_dir + "/scripts/gha_checkout_pr_worktree.py", str(meta["number"]), repo_dir + "/pr"],
        cwd=repo_dir,
        check=False,
    )
    work = repo_dir + "/pr"

# ----------------------------------
# Install deps + codex
# ----------------------------------
run(["python3", repo_dir + "/scripts/gha_uv_sync.py"], cwd=repo_dir, check=False)
run(["python3", repo_dir + "/scripts/gha_npm_install_codex.py", codex_pkg], cwd=repo_dir, check=False)

# ----------------------------------
# Run codexcli main
# ----------------------------------
args = load(open(bundle + "/argv.json", "rb"))
if len(args) > 5 and s3_bucket:
    args[5] = s3_bucket
if meta["kind"] == "prs":
    run(["uv", "run", "--project", repo_dir, repo_dir + "/scripts/codexcli_main.py", *args], cwd=work, check=False)
else:
    run(["uv", "run", "--project", repo_dir, repo_dir + "/scripts/codexcli_main.py", *args], cwd=work, check=False)
