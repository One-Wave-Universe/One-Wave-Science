"""Step 10 known-good Git workspace protection verification."""

from hashlib import sha256
from pathlib import Path
import subprocess
import sys
import tempfile

FIELD_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIELD_ROOT))

from field.git_safety import (
    capture_known_good,
    candidate_status,
    create_candidate_worktree,
    rollback_candidate,
)


def run(repo: Path, *args: str) -> str:
    result = subprocess.run(list(args), cwd=repo, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return result.stdout.strip()


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        source = base / "source"
        candidate_path = base / "candidate"
        source.mkdir()
        run(source, "git", "init")
        run(source, "git", "config", "user.email", "field@example.invalid")
        run(source, "git", "config", "user.name", "Field Fixture")
        run(source, "git", "checkout", "-b", "known-good")
        (source / "calculator.py").write_text("def add(a,b):\n    return a+b\n", encoding="utf-8")
        run(source, "git", "add", "calculator.py")
        run(source, "git", "commit", "-m", "known good")

        original_hash = digest(source / "calculator.py")
        original_branch = run(source, "git", "branch", "--show-current")
        known = capture_known_good(source)

        candidate = create_candidate_worktree(known, candidate_path, "field-candidate")
        require(candidate.baseline_head == known.head, repr(candidate))
        require(run(candidate_path, "git", "rev-parse", "HEAD") == known.head, "candidate baseline mismatch")
        print("PASS: isolated candidate worktree created at known-good HEAD")

        (candidate_path / "calculator.py").write_text("broken !!!\n", encoding="utf-8")
        (candidate_path / "junk.tmp").write_text("untracked bad file\n", encoding="utf-8")
        require(candidate_status(candidate), "bad candidate unexpectedly clean")
        rollback_candidate(candidate)
        require(candidate_status(candidate) == "", "candidate not clean after rollback")
        require(digest(candidate_path / "calculator.py") == original_hash, "tracked file not restored")
        require(not (candidate_path / "junk.tmp").exists(), "untracked file survived rollback")
        print("PASS: deliberate bad candidate completely restored")

        require(run(source, "git", "rev-parse", "HEAD") == known.head, "source HEAD changed")
        require(run(source, "git", "branch", "--show-current") == original_branch, "source branch changed")
        require(run(source, "git", "status", "--porcelain") == "", "source checkout became dirty")
        require(digest(source / "calculator.py") == original_hash, "source bytes changed")
        print("PASS: known-good source checkout remained unchanged")

        successful = "def add(a,b):\n    return a+b\n\ndef multiply(a,b):\n    return a*b\n"
        (candidate_path / "calculator.py").write_text(successful, encoding="utf-8")
        require("calculator.py" in candidate_status(candidate), candidate_status(candidate))
        require("multiply" in (candidate_path / "calculator.py").read_text(encoding="utf-8"), "candidate edit missing")
        require(run(source, "git", "status", "--porcelain") == "", "source dirtied by inspectable candidate")
        require(digest(source / "calculator.py") == original_hash, "source bytes changed by candidate")
        print("PASS: successful candidate remains inspectable while source stays clean")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
