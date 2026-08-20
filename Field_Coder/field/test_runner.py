"""Bounded success-test execution for Field Coder Step 08."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shlex
import subprocess

from field.proposal import ImplementationProposal


class TestRunnerError(ValueError):
    """Raised when a declared success-test command is invalid."""


@dataclass(frozen=True)
class TestEvidence:
    command: str
    argv: tuple[str, ...]
    stdout: str
    stderr: str
    exit_code: int | None
    timed_out: bool
    passed: bool


def run_success_test(
    repo_root: str | Path,
    proposal: ImplementationProposal,
    *,
    timeout_seconds: float = 30.0,
) -> TestEvidence:
    """Execute one declared test without a shell and return evidence for every outcome."""
    root = Path(repo_root).resolve()
    if not root.is_dir():
        raise TestRunnerError(f"repository root is not a directory: {root}")
    if timeout_seconds <= 0:
        raise TestRunnerError("timeout_seconds must be greater than zero")

    command = proposal.success_test.strip()
    if not command:
        raise TestRunnerError("success test must not be empty")

    try:
        argv = tuple(shlex.split(command))
    except ValueError as exc:
        raise TestRunnerError(f"invalid success test command: {exc}") from exc
    if not argv:
        raise TestRunnerError("success test must contain a command")

    try:
        result = subprocess.run(
            argv,
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout_seconds,
            shell=False,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode() if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        return TestEvidence(
            command=command,
            argv=argv,
            stdout=stdout,
            stderr=stderr,
            exit_code=None,
            timed_out=True,
            passed=False,
        )
    except OSError as exc:
        return TestEvidence(
            command=command,
            argv=argv,
            stdout="",
            stderr=str(exc),
            exit_code=None,
            timed_out=False,
            passed=False,
        )

    return TestEvidence(
        command=command,
        argv=argv,
        stdout=result.stdout,
        stderr=result.stderr,
        exit_code=result.returncode,
        timed_out=False,
        passed=(result.returncode == 0),
    )
