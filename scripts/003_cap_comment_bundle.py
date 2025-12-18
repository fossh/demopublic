"""
MUST HAVE REQUIREMENTS
- Script id: 003
- Standalone script (no local imports).
- Comment on the issue/PR with v2 bundle S3 location and replay steps.
- Must not read environment variables; use argv only.
"""

from json import load, dumps
from urllib.request import Request, urlopen
from sys import argv

manifest = load(open(argv[1] + "/manifest.json", "rb"))

body = (
    "v2 bundle:\n"
    + manifest["s3_bundle"]
    + "\n\nReplay:\n"
    + "aws s3 sync "
    + manifest["s3_bundle"]
    + " /tmp/codex-v2-bundle-"
    + manifest["run_id"]
    + "\n"
    + "git clone https://github.com/"
    + manifest["repo"]
    + ".git /tmp/"
    + manifest["repo_name"]
    + "\n"
    + "python3 /tmp/"
    + manifest["repo_name"]
    + "/scripts/199_ex_run_all.py /tmp/codex-v2-bundle-"
    + manifest["run_id"]
    + " /tmp/"
    + manifest["repo_name"]
    + "\n\nOr run step-by-step:\n"
    + "python3 /tmp/"
    + manifest["repo_name"]
    + "/scripts/101_ex_restore_codex_home.py /tmp/codex-v2-bundle-"
    + manifest["run_id"]
    + "\n"
    + "python3 /tmp/"
    + manifest["repo_name"]
    + "/scripts/102_ex_checkout_repo.py /tmp/codex-v2-bundle-"
    + manifest["run_id"]
    + " /tmp/"
    + manifest["repo_name"]
    + "\n"
    + "python3 /tmp/"
    + manifest["repo_name"]
    + "/scripts/104_ex_install_codex_cli.py @openai/codex@0.73.0\n"
    + "python3 /tmp/"
    + manifest["repo_name"]
    + "/scripts/111_ex_ensure_session_id.py /tmp/codex-v2-bundle-"
    + manifest["run_id"]
    + "/codex_home\n"
    + "python3 /tmp/"
    + manifest["repo_name"]
    + "/scripts/120_ex_run_codex.py /tmp/codex-v2-bundle-"
    + manifest["run_id"]
    + " /tmp/"
    + manifest["repo_name"]
    + "\n"
    + "python3 /tmp/"
    + manifest["repo_name"]
    + "/scripts/140_ex_comment_result.py /tmp/codex-v2-bundle-"
    + manifest["run_id"]
    + "\n\nMore: /tmp/"
    + manifest["repo_name"]
    + "/scripts/"
    + "\n\nRun: "
    + manifest["run_url"]
)

url = "https://api.github.com/repos/" + manifest["repo"] + "/issues/" + str(manifest["number"]) + "/comments"
request = Request(url, data=('{"body":' + dumps(body) + "}").encode(), method="POST")
request.add_header("Authorization", "Bearer " + manifest["github_token"])
try:
    urlopen(request).read()
except Exception:
    pass
