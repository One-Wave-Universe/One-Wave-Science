"""Patch Worker: safely applies an approved change.

Never writes anything on its own -- the caller (the orchestrator, acting
on the user's explicit approval) decides when apply() runs. preview_diff
lets the user see exactly what would change before approving it.
"""

from __future__ import annotations

import difflib
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProposedChange:
    file_path: str  # relative to project_root
    new_content: str
    description: str = ""


@dataclass
class PatchResult:
    success: bool
    message: str


class PathEscapesProjectRootError(ValueError):
    pass


class PatchWorker:
    def __init__(self, project_root: str | Path):
        self.project_root = Path(project_root).resolve()

    def _resolve_target(self, file_path: str) -> Path:
        target = (self.project_root / file_path).resolve()
        if self.project_root not in target.parents and target != self.project_root:
            raise PathEscapesProjectRootError(f"{file_path!r} resolves outside the project root")
        return target

    def preview_diff(self, change: ProposedChange) -> str:
        target = self._resolve_target(change.file_path)
        old_lines = target.read_text().splitlines(keepends=True) if target.exists() else []
        new_lines = change.new_content.splitlines(keepends=True)
        diff = difflib.unified_diff(
            old_lines, new_lines,
            fromfile=f"a/{change.file_path}", tofile=f"b/{change.file_path}",
        )
        return "".join(diff)

    def apply(self, change: ProposedChange) -> PatchResult:
        try:
            target = self._resolve_target(change.file_path)
        except PathEscapesProjectRootError as exc:
            return PatchResult(success=False, message=str(exc))

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(change.new_content)
        return PatchResult(success=True, message=f"applied change to {change.file_path}")
