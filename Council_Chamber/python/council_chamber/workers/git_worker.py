"""Git Worker: creates checkpoints and displays changes -- real git
subprocess calls against the project directory."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class GitResult:
    success: bool
    output: str


class GitWorker:
    def __init__(self, project_root: str | Path):
        self.project_root = Path(project_root)

    def _run(self, args: list) -> GitResult:
        completed = subprocess.run(
            ["git", *args], cwd=self.project_root, capture_output=True, text=True,
        )
        output = completed.stdout if completed.returncode == 0 else completed.stderr
        return GitResult(success=completed.returncode == 0, output=output)

    def status(self) -> GitResult:
        return self._run(["status", "--short"])

    def diff(self, staged: bool = False) -> GitResult:
        args = ["diff", "--staged"] if staged else ["diff"]
        return self._run(args)

    def checkpoint(self, message: str) -> GitResult:
        add_result = self._run(["add", "-A"])
        if not add_result.success:
            return add_result
        return self._run(["commit", "-m", message])

    def log(self, max_count: int = 10) -> GitResult:
        return self._run(["log", f"-{max_count}", "--oneline"])
