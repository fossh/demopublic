"""
MUST HAVE REQUIREMENTS
- Script id: 110
- Standalone script (no local imports).
- Exit non-zero if CODEX_HOME contains more than one session id.
- Must not read environment variables; use argv only.
"""

from glob import glob
from os.path import basename
from sys import argv

session_files = glob(argv[1] + "/sessions/**/*.jsonl", recursive=True)
if session_files and len({basename(f)[-41:-5] for f in session_files}) > 1:
    raise SystemExit(1)
