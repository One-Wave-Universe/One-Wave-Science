#!/usr/bin/env python3
"""Structured terminal parser/executor for the One-Wave host gateway.

The parser accepts argv arrays, runs as the current unprivileged host user,
and returns structured stdout/stderr/exit status for the calling AI. Normal
shell wrappers such as ``bash -lc`` are supported because several AI clients use
them for routine terminal work.
"""

from __future__ import annotations

import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile
import time
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
HOME = Path.home().resolve()
MAX_ARGS = 128
MAX_ARG_LEN = 4096
MAX_TIMEOUT = 300
MAX_OUTPUT = 512 * 1024
MAX_SOURCE = 12 * 1024
MAX_TOOL_ARGS = 64
CPP_STANDARDS = {"c++17", "c++20", "c++23"}
PARSER_CONTRACT = "one-wave-terminal-parser-v2"

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
SENSITIVE_SOURCE_TERMS = (
    ".ssh",
    ".gnupg",
    ".aws",
    "hive-pipe/tokens",
    ".config/gh",
)


def _configured_roots() -> tuple[Path, ...]:
    """Resolve the explicit work roots exported by the systemd installer."""
    roots = [HOME]
    for raw in os.environ.get("HIVE_PIPE_ALLOWED_ROOTS", "").split(os.pathsep):
        raw = raw.strip()
        if not raw:
            continue
        path = Path(raw).expanduser().resolve()
        if path.is_dir():
            roots.append(path)
    return tuple(dict.fromkeys(roots))


ALLOWED_ROOTS = _configured_roots()


def reference() -> dict[str, Any]:
    """Return a machine-readable operating reference for AI and human clients."""
    return {
        "contract": PARSER_CONTRACT,
        "purpose": "bounded non-root software work with explicit receipts",
        "workflow": [
            "inspect the current directory and repository state",
            "send argv as a string array with an authorized working directory",
            "read stdout, stderr, exit_code, guidance, and intervention",
            "make one bounded correction or request the named higher-level action",
            "verify the resulting state before continuing",
        ],
        "authorized_roots": [str(root) for root in ALLOWED_ROOTS],
        "limits": {
            "max_arguments": MAX_ARGS,
            "max_argument_characters": MAX_ARG_LEN,
            "max_timeout_seconds": MAX_TIMEOUT,
            "max_output_bytes": MAX_OUTPUT,
            "max_source_bytes": MAX_SOURCE,
        },
        "boundaries": {
            "user": "current unprivileged service user",
            "privilege_escalation": "blocked",
            "raw_disk_mount_power_controls": "blocked",
            "credential_private_key_paths": "blocked",
            "shell": "argv execution; shell wrappers are parsed under the same service sandbox",
        },
        "intervention_levels": {
            "none": "continue with evidence from the receipt",
            "ai_correction": "the caller can make a bounded command/path/timeout correction",
            "path_authorization": "an operator must create or explicitly authorize a work path",
            "tool_installation": "an operator or package manager must provide a missing executable",
            "authentication": "an operator must repair credentials or remote authorization",
            "privileged_operator": "a human must perform an approved root/system action outside this parser",
        },
    }


def explain_failure(*, exit_code: int | None = None, stderr: str = "", error: str = "",
                    timed_out: bool = False) -> dict[str, Any]:
    """Classify a failure and name the next boundary-respecting intervention."""
    text = f"{error}\n{stderr}".lower()
    if timed_out or exit_code == 124:
        return {
            "code": "TIMEOUT_REPLAN_REQUIRED",
            "level": "ai_correction",
            "higher_level_required": False,
            "explanation": "The bounded command exceeded its time budget.",
            "next_action": "Split the work, narrow its scope, or retry once with a justified timeout up to the documented maximum.",
        }
    if "cwd is not a directory" in text or "no such file or directory" in text:
        return {
            "code": "PATH_CREATION_OR_CORRECTION_REQUIRED",
            "level": "path_authorization",
            "higher_level_required": True,
            "explanation": "The requested executable or working path does not exist in the current runtime view.",
            "next_action": "Locate the intended path. If it is new, have the operator create and explicitly authorize only that work directory.",
        }
    if "cwd must stay inside" in text or "authorized" in text and "root" in text:
        return {
            "code": "PATH_AUTHORIZATION_REQUIRED",
            "level": "path_authorization",
            "higher_level_required": True,
            "explanation": "The requested path is outside the parser's authorized work roots.",
            "next_action": "Choose an existing authorized root or reinstall the service with the specific dedicated work directory authorized.",
        }
    if "program is disabled" in text or "operation not permitted" in text or "permission denied" in text or "read-only file system" in text:
        return {
            "code": "PRIVILEGED_OPERATOR_REQUIRED",
            "level": "privileged_operator",
            "higher_level_required": True,
            "explanation": "The requested operation crosses the non-root or protected-filesystem boundary.",
            "next_action": "Report the exact blocked action and let a human approve and run the smallest required system-level command; do not bypass the parser.",
        }
    if "command not found" in text or "not found on path" in text or "executable file not found" in text:
        return {
            "code": "TOOL_INSTALLATION_OR_PATH_REQUIRED",
            "level": "tool_installation",
            "higher_level_required": True,
            "explanation": "A required executable is missing or not visible on the service PATH.",
            "next_action": "Verify the executable name and PATH, then have the operator install the package if it is genuinely absent.",
        }
    if any(marker in text for marker in ("authentication failed", "could not read username", "publickey", "repository not found")):
        return {
            "code": "AUTHENTICATION_REPAIR_REQUIRED",
            "level": "authentication",
            "higher_level_required": True,
            "explanation": "The remote rejected or could not obtain the configured identity.",
            "next_action": "Repair the existing account/remote authentication outside command payloads; never place tokens or private keys in the request.",
        }
    return {
        "code": "COMMAND_REVIEW_REQUIRED",
        "level": "ai_correction",
        "higher_level_required": False,
        "explanation": "The command failed inside the allowed boundary without matching a known infrastructure condition.",
        "next_action": "Inspect stderr and exit_code, make one evidence-based correction, and escalate after repeated failure.",
    }


def explain_exception(error: BaseException) -> dict[str, Any]:
    return explain_failure(error=f"{type(error).__name__}: {error}")


def _with_guidance(result: dict[str, Any]) -> dict[str, Any]:
    result["parser_contract"] = PARSER_CONTRACT
    result["reference"] = {
        "tool": "terminal_reference",
        "contract": PARSER_CONTRACT,
        "instruction": "Call terminal_reference for workflow, limits, authorized roots, and intervention levels.",
    }
    if result.get("ok"):
        result["guidance"] = {
            "code": "VERIFIED_COMMAND_COMPLETE",
            "level": "none",
            "higher_level_required": False,
            "explanation": "The command completed inside the bounded parser.",
            "next_action": "Use the receipt as evidence and verify state before the next mutation.",
        }
    else:
        result["guidance"] = explain_failure(
            exit_code=result.get("exit_code"),
            stderr=result.get("stderr", ""),
            error=result.get("error", ""),
            timed_out=bool(result.get("timed_out")),
        )
    return result


def _clip(text: str) -> tuple[str, bool]:
    raw = text.encode("utf-8", errors="replace")
    if len(raw) <= MAX_OUTPUT:
        return text, False
    return raw[:MAX_OUTPUT].decode("utf-8", errors="replace") + "\n[output clipped]\n", True


def _inside_allowed_root(path: Path) -> bool:
    for root in ALLOWED_ROOTS:
        try:
            path.relative_to(root)
            return True
        except ValueError:
            continue
    return False


def _validate_cwd(cwd: str | None) -> Path:
    target = REPO_ROOT if not cwd else Path(cwd).expanduser().resolve()
    if not target.is_dir():
        raise ValueError(f"cwd is not a directory: {target}")
    if not _inside_allowed_root(target):
        allowed = ", ".join(str(root) for root in ALLOWED_ROOTS)
        raise ValueError(f"cwd must stay inside an authorized One-Wave work root: {allowed}")
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
    if program in {"bash", "sh", "dash", "zsh"}:
        command_index = next((i for i, arg in enumerate(argv[1:], start=1) if "c" in arg.lstrip("-") and arg.startswith("-")), None)
        if command_index is not None and command_index + 1 < len(argv):
            try:
                shell_tokens = shlex.split(argv[command_index + 1], posix=True)
            except ValueError as exc:
                raise ValueError(f"invalid shell payload: {exc}") from exc
            for token in shell_tokens:
                candidate = Path(token.strip(";&|(){}")).name
                if candidate in BLOCKED_PROGRAMS or candidate.startswith("mkfs."):
                    raise ValueError(f"program is disabled through AI terminal access: {candidate}")
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
        return _with_guidance({
            "ok": completed.returncode == 0,
            "argv": command,
            "cwd": str(target),
            "exit_code": completed.returncode,
            "stdout": stdout,
            "stderr": stderr,
            "output_clipped": stdout_clipped or stderr_clipped,
            "duration_ms": int((time.monotonic() - started) * 1000),
        })
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout or ""
        err = exc.stderr or ""
        if isinstance(out, bytes):
            out = out.decode("utf-8", errors="replace")
        if isinstance(err, bytes):
            err = err.decode("utf-8", errors="replace")
        stdout, stdout_clipped = _clip(out)
        stderr, stderr_clipped = _clip(err)
        return _with_guidance({
            "ok": False,
            "argv": command,
            "cwd": str(target),
            "exit_code": 124,
            "stdout": stdout,
            "stderr": stderr,
            "output_clipped": stdout_clipped or stderr_clipped,
            "timed_out": True,
            "duration_ms": int((time.monotonic() - started) * 1000),
        })

def _validate_source(code: Any) -> str:
    if not isinstance(code, str) or not code.strip():
        raise ValueError("code must be a non-empty string")
    if len(code.encode("utf-8")) > MAX_SOURCE:
        raise ValueError(f"code exceeds {MAX_SOURCE} UTF-8 bytes")
    lowered = code.lower()
    if any(term.lower() in lowered for term in SENSITIVE_SOURCE_TERMS):
        raise ValueError("source references credential/private-key paths")
    return code


def _validate_tool_args(args: Any) -> list[str]:
    if args is None:
        return []
    if not isinstance(args, list) or len(args) > MAX_TOOL_ARGS:
        raise ValueError(f"args must be a string array with at most {MAX_TOOL_ARGS} entries")
    if not all(isinstance(arg, str) and len(arg) <= MAX_ARG_LEN for arg in args):
        raise ValueError(f"every args entry must be a string no longer than {MAX_ARG_LEN} characters")
    joined = "\n".join(args)
    for marker in SENSITIVE_PARTS:
        if marker in joined:
            raise ValueError("access to credential/private-key paths is disabled")
    return args


def python_run(code: Any, *, args: Any = None, cwd: str | None = None,
               timeout: int | float = 60) -> dict[str, Any]:
    """Run supplied Python source as a temporary script inside an authorized root."""
    source = _validate_source(code)
    program_args = _validate_tool_args(args)
    target = _validate_cwd(cwd)
    with tempfile.TemporaryDirectory(prefix=".hive-pipe-python-", dir=target) as tmp:
        script = Path(tmp) / "main.py"
        script.write_text(source, encoding="utf-8")
        result = run(["python3", str(script), *program_args], cwd=str(target), timeout=timeout)
    result.update({
        "language": "python",
        "runner": shutil.which("python3") or "python3",
        "temporary_source": True,
    })
    return result


def cpp_compile_run(code: Any, *, args: Any = None, cwd: str | None = None,
                    timeout: int | float = 60, standard: str = "c++20") -> dict[str, Any]:
    """Compile supplied C++ source with g++, execute it, then remove temporary artifacts."""
    source = _validate_source(code)
    program_args = _validate_tool_args(args)
    target = _validate_cwd(cwd)
    if standard not in CPP_STANDARDS:
        raise ValueError(f"standard must be one of: {', '.join(sorted(CPP_STANDARDS))}")
    compiler = shutil.which("g++")
    if not compiler:
        raise ValueError("g++ is not installed or not on PATH")
    with tempfile.TemporaryDirectory(prefix=".hive-pipe-cpp-", dir=target) as tmp:
        source_path = Path(tmp) / "main.cpp"
        binary_path = Path(tmp) / "program"
        source_path.write_text(source, encoding="utf-8")
        compile_result = run([
            compiler, f"-std={standard}", "-O2", "-Wall", "-Wextra", "-pedantic",
            str(source_path), "-o", str(binary_path),
        ], cwd=str(target), timeout=timeout)
        if not compile_result.get("ok"):
            return {
                "ok": False,
                "language": "c++",
                "phase": "compile",
                "compiler": compiler,
                "standard": standard,
                "stdout": compile_result.get("stdout", ""),
                "stderr": compile_result.get("stderr", ""),
                "exit_code": compile_result.get("exit_code"),
                "compile": compile_result,
                "temporary_source": True,
            }
        run_result = run([str(binary_path), *program_args], cwd=str(target), timeout=timeout)
    run_result.update({
        "language": "c++",
        "phase": "run",
        "compiler": compiler,
        "standard": standard,
        "compile": compile_result,
        "temporary_source": True,
    })
    return run_result
