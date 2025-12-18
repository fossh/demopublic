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

m = load(open(argv[1] + "/manifest.json", "rb"))

body = (
    "v2 bundle:\n"
    + m["s3_bundle"]
    + "\n\nReplay:\n"
    + "aws s3 sync "
    + m["s3_bundle"]
    + " /tmp/codex-v2-bundle-"
    + m["run_id"]
    + "\n"
    + "git clone https://github.com/"
    + m["repo"]
    + ".git /tmp/"
    + m["repo_name"]
    + "\n"
    + "python3 /tmp/"
    + m["repo_name"]
    + "/v2/101_ex_restore_codex_home.py /tmp/codex-v2-bundle-"
    + m["run_id"]
    + "\n"
    + "python3 /tmp/"
    + m["repo_name"]
    + "/v2/102_ex_checkout_repo.py /tmp/codex-v2-bundle-"
    + m["run_id"]
    + " /tmp/"
    + m["repo_name"]
    + "\n"
    + "python3 /tmp/"
    + m["repo_name"]
    + "/v2/104_ex_install_codex_cli.py @openai/codex@0.73.0\n"
    + "python3 /tmp/"
    + m["repo_name"]
    + "/v2/111_ex_ensure_session_id.py /tmp/codex-v2-bundle-"
    + m["run_id"]
    + "/codex_home\n"
    + "python3 /tmp/"
    + m["repo_name"]
    + "/v2/120_ex_run_codex.py /tmp/codex-v2-bundle-"
    + m["run_id"]
    + " /tmp/"
    + m["repo_name"]
    + "\n"
    + "python3 /tmp/"
    + m["repo_name"]
    + "/v2/140_ex_comment_result.py /tmp/codex-v2-bundle-"
    + m["run_id"]
    + "\n\nMore: /tmp/"
    + m["repo_name"]
    + "/v2/"
    + "\n\nRun: "
    + m["run_url"]
)

u = "https://api.github.com/repos/" + m["repo"] + "/issues/" + str(m["number"]) + "/comments"
req = Request(u, data=('{"body":' + dumps(body) + "}").encode(), method="POST")
req.add_header("Authorization", "Bearer " + m["github_token"])
try:
    urlopen(req).read()
except Exception:
    pass
