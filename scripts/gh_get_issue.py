"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Fetch a GitHub issue/PR as JSON and print it.
- No environment variable reads; use argv only.
"""

from json import dumps
from sys import argv

import requests

# ----------------------------------
# Inputs
# ----------------------------------
token = argv[1]
repo = argv[2]
issue_number = argv[3]

# ----------------------------------
# Fetch + print
# ----------------------------------
print(
    dumps(
        requests.get(
            f"https://api.github.com/repos/{repo}/issues/{issue_number}",
            headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
            timeout=60,
        ).json()
    )
)

