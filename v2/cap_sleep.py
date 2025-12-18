"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Sleep for N seconds (used to keep capture workflow alive).
- Must not read environment variables; use argv only.
"""

from time import sleep
from sys import argv

sleep(int(argv[1]))

