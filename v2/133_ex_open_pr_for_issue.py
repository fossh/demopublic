"""
MUST HAVE REQUIREMENTS
- Script id: 133
- Standalone script (no local imports).
- Open a PR from `bundle/branch`; write url to `bundle/pr_url`.
- Must not read environment variables; use argv only.
"""

from json import load, dumps
from os.path import exists
from sys import argv
from urllib.request import Request, urlopen

b = argv[1]
if not exists(b + "/branch"):
    raise SystemExit

m = load(open(b + "/manifest.json", "rb"))
e = load(open(b + "/event.json", "rb"))
branch = open(b + "/branch", "r", encoding="utf-8").read().strip()

u = "https://api.github.com/repos/" + m["repo"] + "/pulls"
req = Request(
    u,
    data=dumps(
        {
            "title": "codex-v2: issue " + str(m["number"]),
            "head": branch,
            "base": e["repository"]["default_branch"],
            "body": open(b + "/codex_output.txt", "r", encoding="utf-8").read()[:60000],
        }
    ).encode(),
    method="POST",
)
req.add_header("Authorization", "Bearer " + m["github_token"])
try:
    r = load(urlopen(req))
    open(b + "/pr_url", "w", encoding="utf-8").write(r.get("html_url", ""))
except Exception:
    open(b + "/pr_url", "w", encoding="utf-8").write("https://github.com/%s/pull/new/%s" % (m["repo"], branch))
