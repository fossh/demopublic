"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Capture everything needed to run v2 execution into a single bundle dir.
- Upload the bundle to S3 and comment back with replay instructions.
- Must not read environment variables; use argv only.
"""

from json import dump, dumps
from os import environ, makedirs
from shutil import copyfile, rmtree
from subprocess import run
from sys import argv
from time import sleep
from urllib.request import Request, urlopen

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
sleep_seconds = int(argv[14]) if len(argv) > 14 else 0

# ----------------------------------
# Configure aws env from argv
# ----------------------------------
if aws_access_key_id:
    environ["AWS_ACCESS_KEY_ID"] = aws_access_key_id
if aws_secret_access_key:
    environ["AWS_SECRET_ACCESS_KEY"] = aws_secret_access_key
if aws_region:
    environ["AWS_DEFAULT_REGION"] = aws_region

# ----------------------------------
# Bundle layout (one dir is the contract)
# ----------------------------------
repo_name = repo.rsplit("/", 1)[1]
bundle = "/tmp/codex-v2-bundle-%s" % run_id
rmtree(bundle, ignore_errors=True)
makedirs(bundle, exist_ok=True)
copyfile(event_path, bundle + "/event.json")
copyfile(codex_auth_json_path, bundle + "/codex_auth.json")
copyfile(github_context_json_path, bundle + "/github_context.json")

s3_bundle = "s3://%s/%s/v2/bundles/%s/" % (s3_bucket, repo_name, run_id)
s3_codex = "s3://%s/%s/v2/%s/%s/codex_home/" % (s3_bucket, repo_name, kind, number)

dump(
    {
        "repo": repo,
        "repo_name": repo_name,
        "run_id": run_id,
        "run_url": run_url,
        "kind": kind,
        "number": int(number),
        "s3_bundle": s3_bundle,
        "s3_codex": s3_codex,
        "s3_bucket": s3_bucket,
        "aws_access_key_id": aws_access_key_id,
        "aws_secret_access_key": aws_secret_access_key,
        "aws_region": aws_region,
        "github_token": github_token,
    },
    open(bundle + "/manifest.json", "w", encoding="utf-8"),
)

# ----------------------------------
# Upload bundle
# ----------------------------------
run(["aws", "s3", "sync", bundle, s3_bundle], check=False)

# ----------------------------------
# Comment back with location + replay
# ----------------------------------
body = (
    "v2 bundle:\n"
    + s3_bundle
    + "\n\nReplay:\n"
    + "aws s3 sync "
    + s3_bundle
    + " /tmp/codex-v2-bundle-"
    + run_id
    + "\n"
    + "git clone https://github.com/"
    + repo
    + ".git /tmp/"
    + repo_name
    + "\n"
    + "python3 /tmp/"
    + repo_name
    + "/v2/execute.py /tmp/codex-v2-bundle-"
    + run_id
    + " /tmp/"
    + repo_name
    + "\n\nRun: "
    + run_url
)
u = "https://api.github.com/repos/" + repo + "/issues/" + number + "/comments"
req = Request(u, data=('{"body":' + dumps(body) + "}").encode(), method="POST")
req.add_header("Authorization", "Bearer " + github_token)
try:
    urlopen(req).read()
except Exception:
    pass

if sleep_seconds:
    sleep(sleep_seconds)

