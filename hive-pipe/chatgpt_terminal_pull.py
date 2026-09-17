#!/usr/bin/env python3
"""Jetson-side pull worker for the ChatGPT terminal bridge.

The worker polls the dedicated GitHub branch for one request JSON, executes the
argv through the existing Hive Pipe terminal_parser, then commits the structured
result back to the same branch. It does not expose or require the Jetson MCP
bearer token because execution happens locally on the Jetson.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))
import terminal_parser  # noqa: E402

REMOTE = os.environ.get("CHATGPT_TERMINAL_REMOTE", "origin")
BRANCH = os.environ.get("CHATGPT_TERMINAL_BRANCH", "chatgpt-terminal")
REQUEST_PATH = ".chatgpt-terminal/request.json"
RESULT_PATH = ".chatgpt-terminal/result.json"
STATE_DIR = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local/state")) / "one-wave-chatgpt-terminal"
STATE_FILE = STATE_DIR / "last_request.json"
POLL_SECONDS = max(5, int(os.environ.get("CHATGPT_TERMINAL_POLL_SECONDS", "15")))
MAX_REQUEST_BYTES = 8192


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args],
        text=True,
        capture_output=True,
        check=check,
    )


def read_remote_file(path: str) -> tuple[str | None, str | None]:
    run_git("fetch", "--quiet", REMOTE, BRANCH)
    ref = f"{REMOTE}/{BRANCH}"
    commit = run_git("rev-parse", ref).stdout.strip()
    shown = run_git("show", f"{ref}:{path}", check=False)
    if shown.returncode != 0:
        return commit, None
    if len(shown.stdout.encode("utf-8")) > MAX_REQUEST_BYTES:
        raise ValueError(f"{path} exceeds {MAX_REQUEST_BYTES} bytes")
    return commit, shown.stdout


def load_state() -> dict[str, Any]:
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_state(request_id: str, request_commit: str) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(
        json.dumps({"id": request_id, "request_commit": request_commit}, indent=2) + "\n",
        encoding="utf-8",
    )
    tmp.replace(STATE_FILE)


def validate_request(raw: str) -> dict[str, Any]:
    request = json.loads(raw)
    request_id = request.get("id")
    argv = request.get("argv")
    cwd = request.get("cwd", str(REPO_ROOT))
    timeout = request.get("timeout", 120)

    if not isinstance(request_id, str) or not request_id.strip() or len(request_id) > 128:
        raise ValueError("id must be a non-empty string <= 128 characters")
    if not isinstance(argv, list) or not argv or not all(isinstance(x, str) and x for x in argv):
        raise ValueError("argv must be a non-empty JSON array of non-empty strings")
    if not isinstance(cwd, str) or not cwd.startswith("/") or len(cwd) > 1024:
        raise ValueError("cwd must be an absolute path <= 1024 characters")
    if not isinstance(timeout, int) or timeout < 1 or timeout > terminal_parser.MAX_TIMEOUT:
        raise ValueError(f"timeout must be an integer from 1 to {terminal_parser.MAX_TIMEOUT}")

    return {"id": request_id.strip(), "argv": argv, "cwd": cwd, "timeout": timeout}


def execute_request(request: dict[str, Any], request_commit: str) -> dict[str, Any]:
    completed_at = datetime.now(timezone.utc).isoformat()
    try:
        parsed = terminal_parser.run(
            request["argv"],
            cwd=request["cwd"],
            timeout=request["timeout"],
        )
        return {
            "id": request["id"],
            "request_commit": request_commit,
            "completed_at": completed_at,
            **parsed,
        }
    except Exception as exc:
        return {
            "id": request["id"],
            "request_commit": request_commit,
            "completed_at": completed_at,
            "ok": False,
            "exit_code": None,
            "stdout": "",
            "stderr": "",
            "error": f"{type(exc).__name__}: {exc}",
        }


def publish_result(result: dict[str, Any]) -> None:
    """Commit only result.json to the dedicated remote branch.

    Uses a temporary worktree so the user's active project checkout/branch is not
    touched by command-transport traffic.
    """
    run_git("fetch", "--quiet", REMOTE, BRANCH)
    with tempfile.TemporaryDirectory(prefix="one-wave-chatgpt-terminal-") as td:
        worktree = Path(td) / "bridge"
        subprocess.run(
            ["git", "-C", str(REPO_ROOT), "worktree", "add", "--detach", str(worktree), f"{REMOTE}/{BRANCH}"],
            text=True,
            capture_output=True,
            check=True,
        )
        try:
            result_path = worktree / RESULT_PATH
            result_path.parent.mkdir(parents=True, exist_ok=True)
            result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(worktree), "add", RESULT_PATH], check=True)
            changed = subprocess.run(
                ["git", "-C", str(worktree), "diff", "--cached", "--quiet"],
                check=False,
            ).returncode != 0
            if not changed:
                return
            subprocess.run(["git", "-C", str(worktree), "config", "user.name", "one-wave-jetson-bridge"], check=True)
            subprocess.run(["git", "-C", str(worktree), "config", "user.email", "jetson-bridge@users.noreply.github.com"], check=True)
            subprocess.run(
                ["git", "-C", str(worktree), "commit", "-m", f"terminal: result {result.get('id', 'unknown')} [skip ci]"],
                text=True,
                capture_output=True,
                check=True,
            )
            push = subprocess.run(
                ["git", "-C", str(worktree), "push", REMOTE, f"HEAD:{BRANCH}"],
                text=True,
                capture_output=True,
                check=False,
            )
            if push.returncode != 0:
                # One bounded retry after refreshing the command branch.
                subprocess.run(["git", "-C", str(worktree), "fetch", REMOTE, BRANCH], check=True)
                subprocess.run(["git", "-C", str(worktree), "rebase", f"{REMOTE}/{BRANCH}"], check=True)
                subprocess.run(["git", "-C", str(worktree), "push", REMOTE, f"HEAD:{BRANCH}"], check=True)
        finally:
            subprocess.run(
                ["git", "-C", str(REPO_ROOT), "worktree", "remove", "--force", str(worktree)],
                text=True,
                capture_output=True,
                check=False,
            )


def poll_once() -> bool:
    commit, raw = read_remote_file(REQUEST_PATH)
    if not commit or raw is None:
        return False

    request = validate_request(raw)
    state = load_state()
    if state.get("id") == request["id"] and state.get("request_commit") == commit:
        return False

    result = execute_request(request, commit)
    publish_result(result)
    save_state(request["id"], commit)
    print(json.dumps(result, sort_keys=True))
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="poll once and exit")
    parser.add_argument("--watch", action="store_true", help="poll continuously")
    args = parser.parse_args()
    watch = args.watch or not args.once

    if not (REPO_ROOT / ".git").exists():
        raise SystemExit(f"not a git checkout: {REPO_ROOT}")

    if not watch:
        poll_once()
        return 0

    print(f"CHATGPT_TERMINAL_PULL watching {REMOTE}/{BRANCH} every {POLL_SECONDS}s")
    while True:
        try:
            poll_once()
        except Exception as exc:
            print(f"CHATGPT_TERMINAL_PULL_ERROR {type(exc).__name__}: {exc}", file=sys.stderr)
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    raise SystemExit(main())
