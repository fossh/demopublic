"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Persist bundle CODEX_HOME back to S3 (exclude auth.json).
- Must not read environment variables; use argv only.
"""

from json import load
from os import environ
from subprocess import run
from sys import argv

b = argv[1]
m = load(open(b + "/manifest.json", "rb"))

if m["aws_access_key_id"]:
    environ["AWS_ACCESS_KEY_ID"] = m["aws_access_key_id"]
if m["aws_secret_access_key"]:
    environ["AWS_SECRET_ACCESS_KEY"] = m["aws_secret_access_key"]
if m["aws_region"]:
    environ["AWS_DEFAULT_REGION"] = m["aws_region"]

if m["s3_bucket"]:
    run(["aws", "s3", "sync", b + "/codex_home", m["s3_codex"], "--exclude", "auth.json"], check=False)

