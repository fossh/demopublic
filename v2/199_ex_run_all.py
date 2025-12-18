"""
MUST HAVE REQUIREMENTS
- Script id: 199
- Standalone script (no local imports).
- Run the v2 execution scripts in order.
- Must not read environment variables; use argv only.
"""

from subprocess import run
from sys import argv

bundle_dir = argv[1]
repo_dir = argv[2]

# ----------------------------------
# Detect PR vs issue without JSON parsing
# (matches `json.dump` output from v2/001_cap_make_bundle.py)
# ----------------------------------
is_pr = b'"kind": "prs"' in open(bundle_dir + "/manifest.json", "rb").read()

script_dir = repo_dir + "/v2/"
work_dir = repo_dir + ("/pr" if is_pr else "")

if is_pr:
    cmds = (
        ["python3", script_dir + "101_ex_restore_codex_home.py", bundle_dir],
        ["python3", script_dir + "102_ex_checkout_repo.py", bundle_dir, repo_dir],
        ["python3", script_dir + "103_ex_checkout_pr_worktree.py", bundle_dir, repo_dir],
        ["python3", script_dir + "104_ex_install_codex_cli.py", "@openai/codex@0.73.0"],
        ["python3", script_dir + "110_ex_assert_single_session.py", bundle_dir + "/codex_home"],
        ["python3", script_dir + "111_ex_ensure_session_id.py", bundle_dir + "/codex_home"],
        ["python3", script_dir + "120_ex_run_codex.py", bundle_dir, work_dir],
        ["python3", script_dir + "130_ex_commit_if_changed.py", bundle_dir, work_dir, "codex-v2"],
        ["python3", script_dir + "131_ex_push_pr_head.py", bundle_dir, work_dir],
        ["python3", script_dir + "140_ex_comment_result.py", bundle_dir],
        ["python3", script_dir + "150_ex_persist_codex_home.py", bundle_dir],
    )
else:
    cmds = (
        ["python3", script_dir + "101_ex_restore_codex_home.py", bundle_dir],
        ["python3", script_dir + "102_ex_checkout_repo.py", bundle_dir, repo_dir],
        ["python3", script_dir + "104_ex_install_codex_cli.py", "@openai/codex@0.73.0"],
        ["python3", script_dir + "110_ex_assert_single_session.py", bundle_dir + "/codex_home"],
        ["python3", script_dir + "111_ex_ensure_session_id.py", bundle_dir + "/codex_home"],
        ["python3", script_dir + "120_ex_run_codex.py", bundle_dir, work_dir],
        ["python3", script_dir + "130_ex_commit_if_changed.py", bundle_dir, work_dir, "codex-v2"],
        ["python3", script_dir + "132_ex_push_issue_branch.py", bundle_dir, work_dir],
        ["python3", script_dir + "133_ex_open_pr_for_issue.py", bundle_dir],
        ["python3", script_dir + "140_ex_comment_result.py", bundle_dir],
        ["python3", script_dir + "150_ex_persist_codex_home.py", bundle_dir],
    )

for cmd in cmds:
    run(cmd, check=False)
