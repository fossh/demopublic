"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Run from a captured v2 bundle directory (no GitHub runner required).
- Restore/persist CODEX_HOME via S3, then run the existing `scripts/codexcli_main.py`.
- Must not read environment variables; use argv only.
"""

from json import load
from os import environ, makedirs
from subprocess import run
from sys import argv

# ----------------------------------
# Inputs
# ----------------------------------
bundle = argv[1]
repo_dir = argv[2]
codex_pkg = argv[3] if len(argv) > 3 else "@openai/codex@0.73.0"

m = load(open(bundle + "/manifest.json", "rb"))
kind = m["kind"]

# ----------------------------------
# Configure aws + codex home
# ----------------------------------
if m["aws_access_key_id"]:
    environ["AWS_ACCESS_KEY_ID"] = m["aws_access_key_id"]
if m["aws_secret_access_key"]:
    environ["AWS_SECRET_ACCESS_KEY"] = m["aws_secret_access_key"]
if m["aws_region"]:
    environ["AWS_DEFAULT_REGION"] = m["aws_region"]

codex_home = bundle + "/codex_home"
environ["CODEX_HOME"] = codex_home
makedirs(codex_home, exist_ok=True)
open(codex_home + "/auth.json", "wb").write(open(bundle + "/codex_auth.json", "rb").read())

if m["s3_bucket"] and run(["aws", "s3", "sync", m["s3_codex"], codex_home, "--exclude", "auth.json"]).returncode:
    raise SystemExit(2)

# ----------------------------------
# Ensure repo exists and select workdir (PR uses a worktree)
# ----------------------------------
if run(["git", "-C", repo_dir, "rev-parse", "--is-inside-work-tree"], stdout=-1).returncode:
    run(["git", "clone", "https://github.com/%s.git" % m["repo"], repo_dir], check=False)
work = repo_dir
if kind == "prs":
    n = str(m["number"])
    run(["python3", "scripts/gha_checkout_pr_worktree.py", n, "pr"], cwd=repo_dir, check=False)
    work = repo_dir + "/pr"

# ----------------------------------
# Setup tools (uv + codex)
# ----------------------------------
run(["python3", "scripts/gha_uv_sync.py"], cwd=repo_dir, check=False)
run(["python3", "scripts/gha_npm_install_codex.py", codex_pkg], cwd=repo_dir, check=False)

# ----------------------------------
# Run existing main script (disable its S3; v2 handles S3)
# ----------------------------------
args = [
    m["github_token"],
    m["repo"],
    bundle + "/event.json",
    m["run_url"],
    codex_home,
    "",
    m["aws_access_key_id"],
    m["aws_secret_access_key"],
    m["aws_region"],
    bundle + "/codex_auth.json",
]
run(["uv", "run", "--project", repo_dir, repo_dir + "/scripts/codexcli_main.py", *args], cwd=work, check=False)

# ----------------------------------
# Persist CODEX_HOME to S3
# ----------------------------------
if m["s3_bucket"]:
    run(["aws", "s3", "sync", codex_home, m["s3_codex"], "--exclude", "auth.json"], check=False)
