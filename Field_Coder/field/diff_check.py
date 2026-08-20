"""Actual changed-file and unified-diff evidence for Field Coder Step 07."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess

from field.proposal import ImplementationProposal


class DiffCheckError(RuntimeError):
    """Raised when Git diff evidence cannot be collected."""


@dataclass(frozen=True)
class DiffEvidence:
    changed_files: tuple[str, ...]
    unexpected_files: tuple[str, ...]
    missing_expected_files: tuple[str, ...]
    unified_diff: str
    matches_proposal: bool


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise DiffCheckError(result.stderr.strip() or "git diff read failed")
    return result.stdout


def inspect_diff(repo_root: str | Path, proposal: ImplementationProposal) -> DiffEvidence:
    """Return actual Git evidence even when it does not match the proposal."""
    repo = Path(repo_root).resolve()
    if not repo.is_dir():
        raise DiffCheckError(f"repository root is not a directory: {repo}")

    status = _git(repo, "status", "--porcelain=v1", "--untracked-files=all")
    changed: list[str] = []
    for line in status.splitlines():
        if len(line) < 4:
            continue
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        changed.append(path)

    changed_files = tuple(sorted(set(changed)))
    expected = set(proposal.files_expected)
    actual = set(changed_files)
    unexpected = tuple(sorted(actual - expected))
    missing = tuple(sorted(expected - actual))
    unified_diff = _git(repo, "diff", "--no-ext-diff", "--")

    return DiffEvidence(
        changed_files=changed_files,
        unexpected_files=unexpected,
        missing_expected_files=missing,
        unified_diff=unified_diff,
        matches_proposal=(not unexpected and not missing),
    )
