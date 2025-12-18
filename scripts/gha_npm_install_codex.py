"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Install the requested Codex CLI npm package globally.
- Must not read environment variables; use argv only.
"""

from subprocess import run
from sys import argv

# ----------------------------------
# Install Codex CLI
# ----------------------------------
run(["npm", "i", "-g", argv[1]], check=False)

