"""
MUST HAVE REQUIREMENTS
- Script id: 099
- Standalone script (no local imports).
- Run the v2 capture scripts in order (bundle -> upload -> comment -> optional sleep).
- Must not read environment variables; use argv only.
"""

from subprocess import run
from sys import argv

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
item_number = argv[13]
sleep_seconds = argv[14] if len(argv) > 14 else ""

p = argv[0]
d = (p[: p.rfind("/") + 1] if "/" in p else "")
b = "/tmp/codex-v2-bundle-" + run_id

cmds = (
    [
        "python3",
        d + "001_cap_make_bundle.py",
        repo,
        event_path,
        run_url,
        run_id,
        s3_bucket,
        aws_access_key_id,
        aws_secret_access_key,
        aws_region,
        github_token,
        codex_auth_json_path,
        github_context_json_path,
        kind,
        item_number,
    ],
    ["python3", d + "002_cap_upload_bundle_s3.py", b],
    ["python3", d + "003_cap_comment_bundle.py", b],
)
for cmd in cmds:
    run(cmd, check=False)
if sleep_seconds:
    run(["python3", d + "090_cap_sleep.py", sleep_seconds], check=False)

