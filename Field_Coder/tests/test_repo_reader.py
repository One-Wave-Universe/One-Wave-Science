"""Step 04 read-only repository reconstruction verification.

Run from repository root:
    python3 Field_Coder/tests/test_repo_reader.py
"""

from hashlib import sha256
from pathlib import Path
import subprocess
import sys
import tempfile

FIELD_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIELD_ROOT))

from field.repo_reader import read_repo_context
from field.task_intake import TaskSpec


def run(repo: Path, *args: str) -> str:
    result = subprocess.run(
        list(args),
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return result.stdout.strip()


def worktree_hashes(repo: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in sorted(repo.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        rel = path.relative_to(repo).as_posix()
        hashes[rel] = sha256(path.read_bytes()).hexdigest()
    return hashes


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "fixture"
        repo.mkdir()
        run(repo, "git", "init")
        run(repo, "git", "config", "user.email", "field@example.invalid")
        run(repo, "git", "config", "user.name", "Field Fixture")
        run(repo, "git", "checkout", "-b", "fixture-read")

        (repo / "tests").mkdir()
        (repo / "calculator.py").write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")
        (repo / "tests" / "test_calculator.py").write_text(
            "from calculator import add\n\ndef test_add():\n    assert add(2, 3) == 5\n",
            encoding="utf-8",
        )
        (repo / "README.md").write_text("fixture only\n", encoding="utf-8")
        run(repo, "git", "add", "calculator.py", "tests/test_calculator.py", "README.md")
        run(repo, "git", "commit", "-m", "fixture baseline")

        before_head = run(repo, "git", "rev-parse", "HEAD")
        before_branch = run(repo, "git", "branch", "--show-current")
        before_status = run(repo, "git", "status", "--porcelain")
        before_hashes = worktree_hashes(repo)

        task = TaskSpec(
            summary="inspect calculator files",
            scope=("calculator.py", "tests/test_calculator.py"),
            success_criteria=("context contains both scoped files",),
        )
        context = read_repo_context(repo, task)

        require(context.head == before_head, "context HEAD mismatch")
        require(context.branch == "fixture-read", context.branch)
        require(
            tuple(item.path for item in context.files)
            == ("calculator.py", "tests/test_calculator.py"),
            repr(context.files),
        )
        require("def add" in context.files[0].content, context.files[0].content)
        require("README.md" not in tuple(item.path for item in context.files), "reader escaped task scope")
        print("PASS: task-scoped repository context reconstructed")

        after_head = run(repo, "git", "rev-parse", "HEAD")
        after_branch = run(repo, "git", "branch", "--show-current")
        after_status = run(repo, "git", "status", "--porcelain")
        after_hashes = worktree_hashes(repo)

        require(after_head == before_head, "HEAD changed during read")
        require(after_branch == before_branch, "branch changed during read")
        require(after_status == before_status == "", "working tree changed during read")
        require(after_hashes == before_hashes, "working-tree file bytes changed during read")
        print("PASS: repository remained byte-for-byte clean in working tree")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
