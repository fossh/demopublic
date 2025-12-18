"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Create a GitHub issue; prints the created issue number.
- No environment variable reads; use argv only.
"""

from sys import argv

import requests

# ----------------------------------
# Inputs
# ----------------------------------
token = argv[1]
repo = argv[2]
title = argv[3]
body = argv[4] if len(argv) > 4 else ""

# ----------------------------------
# Create issue
# ----------------------------------
r = requests.post(
    f"https://api.github.com/repos/{repo}/issues",
    headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    json={"title": title, "body": body},
    timeout=60,
)
r.raise_for_status()
print(r.json()["number"])

