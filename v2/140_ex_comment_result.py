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

b = argv[1]
h = b + "/codex_home"
sid = open(h + "/session_id", "r", encoding="utf-8").read().strip()

m = load(open(b + "/manifest.json", "rb"))

pr = ""
try:
    pr = open(b + "/pr_url", "r", encoding="utf-8").read().strip()
except Exception:
    pr = ""

msg = open(b + "/codex_output.txt", "r", encoding="utf-8").read()
body = "v2 session: " + sid + "\n\n" + (("PR: " + pr + "\n\n") if pr else "") + msg + "\n\nRun: " + m["run_url"] + "\n"

u = "https://api.github.com/repos/" + m["repo"] + "/issues/" + str(m["number"]) + "/comments"
req = Request(u, data=('{"body":' + dumps(body) + "}").encode(), method="POST")
req.add_header("Authorization", "Bearer " + m["github_token"])
try:
    urlopen(req).read()
except Exception:
    pass
