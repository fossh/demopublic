"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- List issue/PR comments and print each one as: id<TAB>login<TAB>body
- No environment variable reads; use argv only.
"""

from sys import argv

import requests

# ----------------------------------
# Inputs
# ----------------------------------
token = argv[1]
repo = argv[2]
issue_number = argv[3]

# ----------------------------------
# List and print comments
# ----------------------------------
for c in requests.get(
    f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments",
    headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    timeout=60,
).json():
    print(c["id"], c["user"]["login"], c["body"].replace("\n", "\\n"), sep="\t")

