"""Known-good Git workspace protection for Field Coder Step 10."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess


class GitSafetyError(RuntimeError):
    """Raised when a workspace safety operation cannot be completed safely."""


@dataclass(frozen=True)
class KnownGood:
    repo_root: str
    branch: str
    head: str


@dataclass(frozen=True)
class CandidateWorkspace:
    source_root: str
    worktree_root: str
    branch: str
    baseline_head: str


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise GitSafetyError(result.stderr.strip() or "git safety command failed")
    return result.stdout.strip()


def capture_known_good(repo_root: str | Path) -> KnownGood:
    """Capture a clean known-good checkout; dirty repos are rejected."""
    repo = Path(repo_root).resolve()
    if not repo.is_dir():
        raise GitSafetyError(f"repository root is not a directory: {repo}")
    if _git(repo, "rev-parse", "--is-inside-work-tree") != "true":
        raise GitSafetyError("path is not a Git working tree")
    status = _git(repo, "status", "--porcelain=v1", "--untracked-files=all")
    if status:
        raise GitSafetyError("known-good checkout must be clean")
    return KnownGood(
        repo_root=str(repo),
        branch=_git(repo, "branch", "--show-current"),
        head=_git(repo, "rev-parse", "HEAD"),
    )


def create_candidate_worktree(
    known_good: KnownGood,
    destination: str | Path,
    branch_name: str,
) -> CandidateWorkspace:
    """Create a separate candidate worktree at the exact known-good commit."""
    source = Path(known_good.repo_root).resolve()
    dest = Path(destination).resolve()
    if dest.exists():
        raise GitSafetyError(f"candidate destination already exists: {dest}")
    if not branch_name.strip():
        raise GitSafetyError("candidate branch name must not be empty")

    result = subprocess.run(
        ["git", "worktree", "add", "-b", branch_name, str(dest), known_good.head],
        cwd=source,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise GitSafetyError(result.stderr.strip() or "unable to create candidate worktree")

    head = _git(dest, "rev-parse", "HEAD")
    if head != known_good.head:
        raise GitSafetyError("candidate worktree did not start at known-good HEAD")

    return CandidateWorkspace(
        source_root=str(source),
        worktree_root=str(dest),
        branch=branch_name,
        baseline_head=known_good.head,
    )


def candidate_status(candidate: CandidateWorkspace) -> str:
    return _git(
        Path(candidate.worktree_root),
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
    )


def rollback_candidate(candidate: CandidateWorkspace) -> None:
    """Restore tracked and untracked candidate files to the baseline commit."""
    worktree = Path(candidate.worktree_root)
    _git(worktree, "reset", "--hard", candidate.baseline_head)
    _git(worktree, "clean", "-fd")
    if _git(worktree, "rev-parse", "HEAD") != candidate.baseline_head:
        raise GitSafetyError("candidate HEAD did not restore to baseline")
    if candidate_status(candidate):
        raise GitSafetyError("candidate worktree is not clean after rollback")
