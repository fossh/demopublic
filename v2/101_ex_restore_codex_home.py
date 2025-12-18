"""
MUST HAVE REQUIREMENTS
- Script id: 101
- Standalone script (no local imports).
- Restore CODEX_HOME from S3 and write auth.json from bundle.
- Must not read environment variables; use argv only.
"""

from json import load
from os import environ, makedirs
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

h = b + "/codex_home"
environ["CODEX_HOME"] = h
makedirs(h, exist_ok=True)
open(h + "/auth.json", "wb").write(open(b + "/codex_auth.json", "rb").read())
if m["s3_bucket"]:
    run(["aws", "s3", "sync", m["s3_codex"], h, "--exclude", "auth.json"], check=False)
