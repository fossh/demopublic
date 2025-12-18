"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Install pip packages passed on argv (uses current Python).
- Must not read environment variables; use argv only.
"""

from subprocess import run
from sys import argv, executable

# ----------------------------------
# Install packages
# ----------------------------------
run([executable, "-m", "pip", "install", "-U", "pip", *argv[1:]], check=False)

