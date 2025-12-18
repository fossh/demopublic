"""
MUST HAVE REQUIREMENTS
- Script id: 001
- Standalone script (no local imports).
- Create a v2 bundle dir in /tmp and write `manifest.json`.
- Copy event/context/auth files into the bundle.
- Must not read environment variables; use argv only.
"""

from json import dump
from os import makedirs
from shutil import copyfile
from sys import argv

# ----------------------------------
# Inputs
# ----------------------------------
repo = argv[1]
event_path = argv[2]
run_url = argv[3]
run_id = argv[4]
s3_bucket = argv[5]
aws_access_key_id = argv[6]
aws_secret_access_key = argv[7]
aws_region = argv[8]
github_token = argv[9]
codex_auth_json_path = argv[10]
github_context_json_path = argv[11]
kind = argv[12]
number = argv[13]

# ----------------------------------
# Bundle layout
# ----------------------------------
repo_name = repo.rsplit("/", 1)[1]
bundle = "/tmp/codex-v2-bundle-" + run_id
makedirs(bundle, exist_ok=True)
copyfile(event_path, bundle + "/event.json")
copyfile(codex_auth_json_path, bundle + "/codex_auth.json")
copyfile(github_context_json_path, bundle + "/github_context.json")
makedirs(bundle + "/codex_home", exist_ok=True)

# ----------------------------------
# Manifest contract
# ----------------------------------
dump(
    {
        "repo": repo,
        "repo_name": repo_name,
        "run_id": run_id,
        "run_url": run_url,
        "kind": kind,
        "number": int(number),
        "s3_bundle": "s3://%s/%s/v2/bundles/%s/" % (s3_bucket, repo_name, run_id),
        "s3_codex": "s3://%s/%s/v2/%s/%s/codex_home/" % (s3_bucket, repo_name, kind, number),
        "s3_bucket": s3_bucket,
        "aws_access_key_id": aws_access_key_id,
        "aws_secret_access_key": aws_secret_access_key,
        "aws_region": aws_region,
        "github_token": github_token,
    },
    open(bundle + "/manifest.json", "w", encoding="utf-8"),
)

print(bundle)
