"""Build Worker: compiles or starts the application -- a real subprocess
run against the project."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class BuildResult:
    success: bool
    exit_code: int
    stdout: str
    stderr: str


class BuildWorker:
    def __init__(self, project_root: str | Path, command: list, timeout_seconds: int = 300):
        self.project_root = Path(project_root)
        self.command = command
        self.timeout_seconds = timeout_seconds

    def run(self) -> BuildResult:
        try:
            completed = subprocess.run(
                self.command, cwd=self.project_root, capture_output=True, text=True,
                timeout=self.timeout_seconds,
            )
        except FileNotFoundError as exc:
            return BuildResult(success=False, exit_code=-1, stdout="", stderr=str(exc))
        except subprocess.TimeoutExpired as exc:
            return BuildResult(success=False, exit_code=-1, stdout=exc.stdout or "",
                                stderr=(exc.stderr or "") + f"\ntimed out after {self.timeout_seconds}s")

        return BuildResult(
            success=completed.returncode == 0,
            exit_code=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )
