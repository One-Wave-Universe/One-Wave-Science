#!/usr/bin/env python3
"""Structured terminal parser/executor for the Jetson Hive Pipe gateway.

The parser accepts argv arrays, runs as the current unprivileged Jetson user,
and returns structured stdout/stderr/exit status for the calling AI. Normal
shell wrappers such as ``bash -lc`` are supported because several AI clients use
them for routine terminal work.
"""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import time
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
HOME = Path.home().resolve()
MAX_ARGS = 128
MAX_ARG_LEN = 4096
MAX_TIMEOUT = 300
MAX_OUTPUT = 512 * 1024

# Direct high-risk system programs remain unavailable through normal AI terminal
# access. The primary boundaries are still non-root execution, systemd
# NoNewPrivileges/ProtectSystem, authenticated client tokens, and bounded writable
# directories; this list is not treated as the main security boundary.
BLOCKED_PROGRAMS = {
    "sudo", "su", "doas", "pkexec",
    "mount", "umount", "fdisk", "cfdisk", "sfdisk", "parted", "gdisk",
    "mkfs", "mkfs.ext4", "mkfs.xfs", "mkfs.btrfs", "mkswap", "swapon",
    "wipefs", "cryptsetup", "losetup", "blockdev", "hdparm",
    "shutdown", "reboot", "poweroff", "halt",
}

SENSITIVE_PARTS = (
    "/.ssh/",
    "/.gnupg/",
    "/.aws/",
    "/.config/hive-pipe/tokens/",
    "/.config/gh/",
)


def _clip(text: str) -> tuple[str, bool]:
    raw = text.encode("utf-8", errors="replace")
    if len(raw) <= MAX_OUTPUT:
        return text, False
    return raw[:MAX_OUTPUT].decode("utf-8", errors="replace") + "\n[output clipped]\n", True


def _inside_home(path: Path) -> bool:
    try:
        path.relative_to(HOME)
        return True
    except ValueError:
        return False


def _validate_cwd(cwd: str | None) -> Path:
    target = REPO_ROOT if not cwd else Path(cwd).expanduser().resolve()
    if not target.is_dir():
        raise ValueError(f"cwd is not a directory: {target}")
    if not _inside_home(target):
        raise ValueError("cwd must stay inside the Jetson user's home directory")
    return target


def _validate_argv(argv: Any) -> list[str]:
    if not isinstance(argv, list) or not argv:
        raise ValueError("argv must be a non-empty string array")
    if len(argv) > MAX_ARGS:
        raise ValueError(f"argv exceeds {MAX_ARGS} entries")
    if not all(isinstance(arg, str) and arg for arg in argv):
        raise ValueError("every argv entry must be a non-empty string")
    if any(len(arg) > MAX_ARG_LEN for arg in argv):
        raise ValueError(f"argv entry exceeds {MAX_ARG_LEN} characters")

    program = Path(argv[0]).name
    if program in BLOCKED_PROGRAMS or program.startswith("mkfs."):
        raise ValueError(f"program is disabled through AI terminal access: {program}")

    joined = "\n".join(argv)
    for marker in SENSITIVE_PARTS:
        if marker in joined:
            raise ValueError("access to credential/private-key paths is disabled")
    return argv


def pwd(cwd: str | None = None) -> dict[str, Any]:
    target = _validate_cwd(cwd)
    return {"ok": True, "cwd": str(target)}


def which(name: str) -> dict[str, Any]:
    if not isinstance(name, str) or not name or "/" in name or len(name) > 128:
        raise ValueError("name must be a simple executable name")
    if name in BLOCKED_PROGRAMS:
        return {"ok": False, "name": name, "path": None, "disabled": True}
    found = shutil.which(name)
    return {"ok": found is not None, "name": name, "path": found}


def run(argv: Any, cwd: str | None = None, timeout: int | float = 60) -> dict[str, Any]:
    command = _validate_argv(argv)
    target = _validate_cwd(cwd)
    try:
        timeout_value = max(1, min(int(timeout), MAX_TIMEOUT))
    except (TypeError, ValueError):
        raise ValueError("timeout must be an integer number of seconds")

    started = time.monotonic()
    env = os.environ.copy()
    env.setdefault("LANG", "C.UTF-8")

    try:
        completed = subprocess.run(
            command,
            cwd=target,
            text=True,
            capture_output=True,
            timeout=timeout_value,
            check=False,
            env=env,
            shell=False,
        )
        stdout, stdout_clipped = _clip(completed.stdout)
        stderr, stderr_clipped = _clip(completed.stderr)
        return {
            "ok": completed.returncode == 0,
            "argv": command,
            "cwd": str(target),
            "exit_code": completed.returncode,
            "stdout": stdout,
            "stderr": stderr,
            "output_clipped": stdout_clipped or stderr_clipped,
            "duration_ms": int((time.monotonic() - started) * 1000),
        }
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout or ""
        err = exc.stderr or ""
        if isinstance(out, bytes):
            out = out.decode("utf-8", errors="replace")
        if isinstance(err, bytes):
            err = err.decode("utf-8", errors="replace")
        stdout, stdout_clipped = _clip(out)
        stderr, stderr_clipped = _clip(err)
        return {
            "ok": False,
            "argv": command,
            "cwd": str(target),
            "exit_code": 124,
            "stdout": stdout,
            "stderr": stderr,
            "output_clipped": stdout_clipped or stderr_clipped,
            "timed_out": True,
            "duration_ms": int((time.monotonic() - started) * 1000),
        }
