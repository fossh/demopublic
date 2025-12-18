"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Post a GitHub issue/PR comment; body is read from stdin.
- No environment variable reads; use argv + stdin only.
"""

from sys import argv, stdin

import requests

# ----------------------------------
# Inputs
# ----------------------------------
token = argv[1]
repo = argv[2]
issue_number = argv[3]
body = stdin.read()

# ----------------------------------
# Post comment
# ----------------------------------
requests.post(
    f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments",
    headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    json={"body": body},
    timeout=60,
).raise_for_status()

