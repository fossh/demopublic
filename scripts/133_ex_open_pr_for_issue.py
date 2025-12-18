"""
MUST HAVE REQUIREMENTS
- Script id: 133
- Standalone script (no local imports).
- Open a PR from `bundle/branch`; write url to `bundle/pr_url`.
- Must not read environment variables; use argv only.
- Argument: bundle dir.
"""

from json import load, dumps
from os.path import exists
from sys import argv
from urllib.request import Request, urlopen

bundle_dir = argv[1]
if not exists(bundle_dir + "/branch"):
    raise SystemExit

manifest = load(open(bundle_dir + "/manifest.json", "rb"))
event_payload = load(open(bundle_dir + "/event.json", "rb"))
branch_name = open(bundle_dir + "/branch", "r", encoding="utf-8").read().strip()

url = "https://api.github.com/repos/" + manifest["repo"] + "/pulls"
request = Request(
    url,
    data=dumps(
        {
            "title": "codex-v2: issue " + str(manifest["number"]),
            "head": branch_name,
            "base": event_payload["repository"]["default_branch"],
            "body": open(bundle_dir + "/codex_output.txt", "r", encoding="utf-8").read()[:60000],
        }
    ).encode(),
    method="POST",
)
request.add_header("Authorization", "Bearer " + manifest["github_token"])
try:
    r = load(urlopen(request))
    open(bundle_dir + "/pr_url", "w", encoding="utf-8").write(r.get("html_url", ""))
except Exception:
    open(bundle_dir + "/pr_url", "w", encoding="utf-8").write(
        "https://github.com/%s/pull/new/%s" % (manifest["repo"], branch_name)
    )
