"""
MUST HAVE REQUIREMENTS
- Script id: 150
- Standalone script (no local imports).
- Persist bundle CODEX_HOME back to S3 (exclude auth.json).
- Must not read environment variables; use argv only.
- Reads S3 + AWS creds from `manifest.json`.
"""

from json import load
from os import environ
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

if manifest["s3_bucket"]:
    run(["aws", "s3", "sync", bundle_dir + "/codex_home", manifest["s3_codex"], "--exclude", "auth.json"], check=False)
