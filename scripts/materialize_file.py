"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Writes stdin bytes to the given path.
- No environment variable reads; use argv + stdin only.
"""

from sys import argv, stdin

# ----------------------------------
# Write stdin to the target path
# ----------------------------------
open(argv[1], "wb").write(stdin.buffer.read())

