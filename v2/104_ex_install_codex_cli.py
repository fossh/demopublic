"""
MUST HAVE REQUIREMENTS
- Script id: 104
- Standalone script (no local imports).
- Install Codex CLI via npm (global).
- Must not read environment variables; use argv only.
"""

from subprocess import run
from sys import argv

run(["npm", "i", "-g", argv[1]], check=False)
