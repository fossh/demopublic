"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Set GitHub repo secrets from a local .env-like file.
- Must not read environment variables; use argv only.
"""

from subprocess import run
from sys import argv

# ----------------------------------
# Parse KEY=VALUE lines and set secrets
# ----------------------------------
repo = argv[1]
for line in open(argv[2], "r", encoding="utf-8"):
    line = line.strip()
    if not line or line[0] == "#":
        continue
    if line.startswith("export "):
        line = line[7:]
    if "=" not in line:
        continue
    k, v = line.split("=", 1)
    if k == "GITHUB_TOKEN":
        continue
    if v and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1]
    run(["gh", "secret", "set", k, "--repo", repo, "-b", v])

