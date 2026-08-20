"""Controlled declared-path text editor for Field Coder Step 06."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from field.proposal import ImplementationProposal


class EditError(ValueError):
    """Raised when an edit violates the accepted proposal boundary."""


@dataclass(frozen=True)
class EditRequest:
    path: str
    new_content: str


def _safe_target(root: Path, relative_path: str) -> Path:
    if not relative_path or Path(relative_path).is_absolute():
        raise EditError(f"invalid edit path: {relative_path!r}")
    target = (root / relative_path).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise EditError(f"edit path escapes repository: {relative_path}") from exc
    if not target.is_file():
        raise EditError(f"edit target must be an existing file: {relative_path}")
    return target


def apply_edit(
    repo_root: str | Path,
    proposal: ImplementationProposal,
    request: EditRequest,
) -> Path:
    """Replace one declared UTF-8 text file and reject every undeclared path."""
    root = Path(repo_root).resolve()
    if not root.is_dir():
        raise EditError(f"repository root is not a directory: {root}")
    if request.path not in proposal.files_expected:
        raise EditError(f"undeclared edit target: {request.path}")
    if not isinstance(request.new_content, str):
        raise EditError("new_content must be text")

    target = _safe_target(root, request.path)
    target.write_text(request.new_content, encoding="utf-8")
    return target
