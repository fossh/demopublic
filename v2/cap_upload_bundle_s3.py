"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Upload a v2 bundle directory to S3 using `aws s3 sync`.
- Must not read environment variables; use argv only.
"""

from json import load
from os import environ
from subprocess import run
from sys import argv

m = load(open(argv[1] + "/manifest.json", "rb"))
if m["aws_access_key_id"]:
    environ["AWS_ACCESS_KEY_ID"] = m["aws_access_key_id"]
if m["aws_secret_access_key"]:
    environ["AWS_SECRET_ACCESS_KEY"] = m["aws_secret_access_key"]
if m["aws_region"]:
    environ["AWS_DEFAULT_REGION"] = m["aws_region"]

run(["aws", "s3", "sync", argv[1], m["s3_bundle"]], check=False)

