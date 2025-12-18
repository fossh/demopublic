"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Upload GitHub event/context bundle to S3 then sleep.
- Comment back with bundle location and how to replay it.
- Must not read environment variables; use argv only.
"""

from json import dump, dumps
from os import environ, makedirs
from urllib.request import Request, urlopen
from shutil import copyfile
from subprocess import run
from sys import argv
from time import sleep

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
# Configure aws env from argv
# ----------------------------------
if aws_access_key_id:
    environ["AWS_ACCESS_KEY_ID"] = aws_access_key_id
if aws_secret_access_key:
    environ["AWS_SECRET_ACCESS_KEY"] = aws_secret_access_key
if aws_region:
    environ["AWS_DEFAULT_REGION"] = aws_region

# ----------------------------------
# Write bundle files
# ----------------------------------
repo_name = repo.rsplit("/", 1)[1]
bundle = "/tmp/codexcli-bundle-%s" % run_id
makedirs(bundle, exist_ok=True)
copyfile(event_path, bundle + "/event.json")
if codex_auth_json_path:
    copyfile(codex_auth_json_path, bundle + "/codex_auth.json")
if github_context_json_path:
    copyfile(github_context_json_path, bundle + "/github_context.json")

codex_home = bundle + "/codex_home/" + kind + "/" + number
makedirs(codex_home, exist_ok=True)

dump(
    {"repo": repo, "run_url": run_url, "run_id": run_id, "kind": kind, "number": int(number)},
    open(bundle + "/meta.json", "w", encoding="utf-8"),
)
dump(
    [
        github_token,
        repo,
        bundle + "/event.json",
        run_url,
        codex_home,
        s3_bucket,
        aws_access_key_id,
        aws_secret_access_key,
        aws_region,
        bundle + "/codex_auth.json",
    ],
    open(bundle + "/argv.json", "w", encoding="utf-8"),
)

# ----------------------------------
# Upload to S3 and wait
# ----------------------------------
s3 = "s3://%s/%s/bundles/%s/" % (s3_bucket, repo_name, run_id)
run(["aws", "s3", "sync", bundle, s3], check=False)

# ----------------------------------
# Comment back with instructions
# ----------------------------------
body = (
    "Bundle uploaded:\n"
    + s3
    + "\n\nReplay:\n"
    + "1) aws s3 sync "
    + s3
    + " /tmp/codexcli-bundle-"
    + run_id
    + "\n"
    + "2) git clone https://github.com/"
    + repo
    + ".git /tmp/"
    + repo_name
    + "\n"
    + "3) python3 /tmp/"
    + repo_name
    + "/scripts/codexcli_bundle_run.py /tmp/codexcli-bundle-"
    + run_id
    + " /tmp/"
    + repo_name
    + " '@openai/codex@0.73.0'\n\nRun: "
    + run_url
)
u = "https://api.github.com/repos/" + repo + "/issues/" + number + "/comments"
req = Request(u, data=('{"body":' + dumps(body) + "}").encode(), method="POST")
req.add_header("Authorization", "Bearer " + github_token)
try:
    urlopen(req).read()
except Exception:
    pass

while 1:
    sleep(3600)
