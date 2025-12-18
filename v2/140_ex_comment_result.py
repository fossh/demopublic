"""
MUST HAVE REQUIREMENTS
- Script id: 140
- Standalone script (no local imports).
- Post execution results comment back to GitHub.
- Must not read environment variables; use argv only.
"""

from json import load, dumps
from urllib.request import Request, urlopen
from sys import argv

bundle_dir = argv[1]
codex_home_dir = bundle_dir + "/codex_home"
session_id = open(codex_home_dir + "/session_id", "r", encoding="utf-8").read().strip()

manifest = load(open(bundle_dir + "/manifest.json", "rb"))

pr = ""
try:
    pr = open(bundle_dir + "/pr_url", "r", encoding="utf-8").read().strip()
except Exception:
    pr = ""

codex_output = open(bundle_dir + "/codex_output.txt", "r", encoding="utf-8").read()
body = (
    "v2 session: "
    + session_id
    + "\n\n"
    + (("PR: " + pr + "\n\n") if pr else "")
    + codex_output
    + "\n\nRun: "
    + manifest["run_url"]
    + "\n"
)

url = "https://api.github.com/repos/" + manifest["repo"] + "/issues/" + str(manifest["number"]) + "/comments"
request = Request(url, data=('{"body":' + dumps(body) + "}").encode(), method="POST")
request.add_header("Authorization", "Bearer " + manifest["github_token"])
try:
    urlopen(request).read()
except Exception:
    pass
