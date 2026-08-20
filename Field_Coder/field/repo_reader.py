"""Read-only repository reconstruction for Field Coder Step 04."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess

from field.task_intake import TaskSpec


class RepoReadError(RuntimeError):
    """Raised when repository context cannot be read safely."""


@dataclass(frozen=True)
class RepoFile:
    path: str
    content: str


@dataclass(frozen=True)
class RepoContext:
    root: str
    branch: str
    head: str
    files: tuple[RepoFile, ...]


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RepoReadError(result.stderr.strip() or "git read failed")
    return result.stdout.strip()


def _safe_scoped_file(repo: Path, relative_path: str) -> Path:
    if not relative_path or Path(relative_path).is_absolute():
        raise RepoReadError(f"invalid scoped path: {relative_path!r}")

    candidate = (repo / relative_path).resolve()
    try:
        candidate.relative_to(repo)
    except ValueError as exc:
        raise RepoReadError(f"scoped path escapes repository: {relative_path}") from exc

    if not candidate.is_file():
        raise RepoReadError(f"scoped file does not exist: {relative_path}")
    return candidate


def read_repo_context(repo_path: str | Path, task: TaskSpec) -> RepoContext:
    """Read Git identity and task-scoped text files without modifying the repo."""
    task.validate()
    repo = Path(repo_path).resolve()
    if not repo.is_dir():
        raise RepoReadError(f"repository path is not a directory: {repo}")

    inside = _git(repo, "rev-parse", "--is-inside-work-tree")
    if inside != "true":
        raise RepoReadError("path is not a Git working tree")

    head = _git(repo, "rev-parse", "HEAD")
    branch = _git(repo, "branch", "--show-current")

    files: list[RepoFile] = []
    for relative_path in task.scope:
        source = _safe_scoped_file(repo, relative_path)
        try:
            content = source.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise RepoReadError(f"scoped file is not UTF-8 text: {relative_path}") from exc
        files.append(RepoFile(path=relative_path, content=content))

    return RepoContext(
        root=str(repo),
        branch=branch,
        head=head,
        files=tuple(files),
    )
