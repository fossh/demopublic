"""
MUST HAVE REQUIREMENTS
- Script id: 002
- Standalone script (no local imports).
- Upload a v2 bundle directory to S3 using `aws s3 sync`.
- Must not read environment variables; use argv only.
"""

from json import load
from os import environ
from subprocess import run
from sys import argv

manifest = load(open(argv[1] + "/manifest.json", "rb"))
if manifest["aws_access_key_id"]:
    environ["AWS_ACCESS_KEY_ID"] = manifest["aws_access_key_id"]
if manifest["aws_secret_access_key"]:
    environ["AWS_SECRET_ACCESS_KEY"] = manifest["aws_secret_access_key"]
if manifest["aws_region"]:
    environ["AWS_DEFAULT_REGION"] = manifest["aws_region"]

run(["aws", "s3", "sync", argv[1], manifest["s3_bundle"]], check=False)
