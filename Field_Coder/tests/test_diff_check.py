"""Step 07 actual-diff self-check verification."""

from pathlib import Path
import subprocess
import sys
import tempfile

FIELD_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIELD_ROOT))

from field.diff_check import inspect_diff
from field.editor import EditRequest, apply_edit
from field.proposal import ImplementationProposal


def run(repo: Path, *args: str) -> str:
    result = subprocess.run(list(args), cwd=repo, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return result.stdout.strip()


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
        (repo / "calculator.py").write_text("def add(a,b):\n    return a+b\n", encoding="utf-8")
        (repo / "README.md").write_text("baseline\n", encoding="utf-8")
        run(repo, "git", "add", "calculator.py", "README.md")
        run(repo, "git", "commit", "-m", "baseline")

        proposal = ImplementationProposal(
            intended_change="add multiply",
            reason="bounded task",
            files_expected=("calculator.py",),
            invariants=("README remains unchanged",),
            expected_result="multiply added",
            success_test="python3 -m pytest",
        )

        apply_edit(
            repo,
            proposal,
            EditRequest(
                "calculator.py",
                "def add(a,b):\n    return a+b\n\ndef multiply(a,b):\n    return a*b\n",
            ),
        )
        matching = inspect_diff(repo, proposal)
        require(matching.matches_proposal, repr(matching))
        require(matching.changed_files == ("calculator.py",), repr(matching.changed_files))
        require("calculator.py" in matching.unified_diff, matching.unified_diff)
        print("PASS: matching actual diff accepted with evidence")

        (repo / "README.md").write_text("unexpected change\n", encoding="utf-8")
        mismatch = inspect_diff(repo, proposal)
        require(not mismatch.matches_proposal, "unexpected change incorrectly matched proposal")
        require(mismatch.unexpected_files == ("README.md",), repr(mismatch.unexpected_files))
        require("README.md" in mismatch.changed_files, repr(mismatch.changed_files))
        require("README.md" in mismatch.unified_diff, mismatch.unified_diff)
        print("PASS: unexpected extra change failed self-check with diff preserved")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
