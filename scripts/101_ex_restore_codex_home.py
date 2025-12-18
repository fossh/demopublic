"""
MUST HAVE REQUIREMENTS
- Script id: 101
- Standalone script (no local imports).
- Restore CODEX_HOME from S3 and write auth.json from bundle.
- Must not read environment variables; use argv only.
- Reads S3 + AWS creds from `manifest.json`.
"""

from json import load
from os import environ, makedirs
from subprocess import run
from sys import argv

bundle_dir = argv[1]
manifest = load(open(bundle_dir + "/manifest.json", "rb"))

if manifest["aws_access_key_id"]:
    environ["AWS_ACCESS_KEY_ID"] = manifest["aws_access_key_id"]
if manifest["aws_secret_access_key"]:
    environ["AWS_SECRET_ACCESS_KEY"] = manifest["aws_secret_access_key"]
if manifest["aws_region"]:
    environ["AWS_DEFAULT_REGION"] = manifest["aws_region"]

codex_home_dir = bundle_dir + "/codex_home"
environ["CODEX_HOME"] = codex_home_dir
makedirs(codex_home_dir, exist_ok=True)
open(codex_home_dir + "/auth.json", "wb").write(open(bundle_dir + "/codex_auth.json", "rb").read())
if manifest["s3_bucket"]:
    run(["aws", "s3", "sync", manifest["s3_codex"], codex_home_dir, "--exclude", "auth.json"], check=False)
