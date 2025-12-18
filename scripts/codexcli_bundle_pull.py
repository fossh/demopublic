"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Download a previously captured bundle from S3 into a local directory.
- Must not read environment variables; use argv only.
"""

from os import environ, makedirs
from subprocess import run
from sys import argv

# ----------------------------------
# Inputs
# ----------------------------------
repo = argv[1]
run_id = argv[2]
out_dir = argv[3]
s3_bucket = argv[4]
aws_access_key_id = argv[5]
aws_secret_access_key = argv[6]
aws_region = argv[7]

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
# Pull bundle
# ----------------------------------
repo_name = repo.rsplit("/", 1)[1]
makedirs(out_dir, exist_ok=True)
run(["aws", "s3", "sync", "s3://%s/%s/bundles/%s/" % (s3_bucket, repo_name, run_id), out_dir], check=False)

