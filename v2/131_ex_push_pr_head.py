"""
MUST HAVE REQUIREMENTS
- Script id: 131
- Standalone script (no local imports).
- If this is a PR from same repo, push commits back to PR head branch.
- Must not read environment variables; use argv only.
"""

from json import load
from os.path import exists
from subprocess import run
from sys import argv
from urllib.request import Request, urlopen

bundle_dir = argv[1]
work_dir = argv[2]
if not exists(bundle_dir + "/changed"):
    raise SystemExit

manifest = load(open(bundle_dir + "/manifest.json", "rb"))
event_payload = load(open(bundle_dir + "/event.json", "rb"))
pr_url = event_payload["issue"]["pull_request"]["url"]

request = Request(pr_url)
request.add_header("Authorization", "Bearer " + manifest["github_token"])
try:
    pr = load(urlopen(request))
except Exception:
    pr = {}

if pr.get("head", {}).get("repo", {}).get("full_name") == manifest["repo"]:
    run(["git", "push", "origin", "HEAD:refs/heads/%s" % pr["head"]["ref"]], cwd=work_dir, check=False)
