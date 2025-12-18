"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- If this is a PR from same repo, push commits back to PR head branch.
- Must not read environment variables; use argv only.
"""

from json import load
from os.path import exists
from subprocess import run
from sys import argv
from urllib.request import Request, urlopen

b = argv[1]
work = argv[2]
if not exists(b + "/changed"):
    raise SystemExit

m = load(open(b + "/manifest.json", "rb"))
e = load(open(b + "/event.json", "rb"))
u = e["issue"]["pull_request"]["url"]

req = Request(u)
req.add_header("Authorization", "Bearer " + m["github_token"])
try:
    pr = load(urlopen(req))
except Exception:
    pr = {}

if pr.get("head", {}).get("repo", {}).get("full_name") == m["repo"]:
    run(["git", "push", "origin", "HEAD:refs/heads/%s" % pr["head"]["ref"]], cwd=work, check=False)
