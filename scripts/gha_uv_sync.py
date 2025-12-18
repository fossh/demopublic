"""
MUST HAVE REQUIREMENTS
- Standalone script (no local imports).
- Ensure uv is installed and run `uv sync --frozen`.
- Must not read environment variables; use argv only.
"""

from subprocess import run
from sys import executable

# ----------------------------------
# Install uv (and keep pip current)
# ----------------------------------
run([executable, "-m", "pip", "install", "-U", "pip", "uv"], check=False)

# ----------------------------------
# Sync deps
# ----------------------------------
run(["uv", "sync", "--frozen"], check=False)

