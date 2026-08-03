"""Test Worker: runs tests and reports exact failures -- a real
subprocess run, not an AI guessing at whether tests would pass."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TestResult:
    passed: bool
    exit_code: int
    stdout: str
    stderr: str
    summary: str


class TestWorker:
    __test__ = False  # not a pytest test class -- this runs *other* tests

    def __init__(self, project_root: str | Path, command: list | None = None, timeout_seconds: int = 120):
        self.project_root = Path(project_root)
        self.command = command or ["python3", "-m", "pytest", "-q"]
        self.timeout_seconds = timeout_seconds

    def run(self) -> TestResult:
        try:
            completed = subprocess.run(
                self.command, cwd=self.project_root, capture_output=True, text=True,
                timeout=self.timeout_seconds,
            )
        except FileNotFoundError as exc:
            return TestResult(passed=False, exit_code=-1, stdout="", stderr=str(exc),
                               summary=f"could not run test command: {exc}")
        except subprocess.TimeoutExpired as exc:
            return TestResult(passed=False, exit_code=-1, stdout=exc.stdout or "", stderr=exc.stderr or "",
                               summary=f"test command timed out after {self.timeout_seconds}s")

        summary = self._summarize(completed.stdout)
        return TestResult(
            passed=completed.returncode == 0,
            exit_code=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
            summary=summary,
        )

    def _summarize(self, stdout: str) -> str:
        lines = [line for line in stdout.splitlines() if line.strip()]
        return lines[-1] if lines else "(no output)"
