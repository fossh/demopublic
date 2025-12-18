"""
MUST HAVE REQUIREMENTS
- Script id: 090
- Standalone script (no local imports).
- Sleep for N seconds (used to keep capture workflow alive).
- Must not read environment variables; use argv only.
- Intended for GHA capture-only workflow.
"""

from time import sleep
from sys import argv

sleep(int(argv[1]))
