"""Step 06 controlled editor verification."""

from hashlib import sha256
from pathlib import Path
import sys
import tempfile

FIELD_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIELD_ROOT))

from field.editor import EditError, EditRequest, apply_edit
from field.proposal import ImplementationProposal


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "calculator.py").write_text("def add(a,b):\n    return a+b\n", encoding="utf-8")
        (root / "tests.py").write_text("def test_add(): pass\n", encoding="utf-8")
        (root / "README.md").write_text("untouched\n", encoding="utf-8")

        proposal = ImplementationProposal(
            intended_change="add multiply",
            reason="bounded task",
            files_expected=("calculator.py", "tests.py"),
            invariants=("README stays unchanged",),
            expected_result="multiply added",
            success_test="python3 tests.py",
        )

        readme_before = digest(root / "README.md")
        tests_before = digest(root / "tests.py")

        new_calc = "def add(a,b):\n    return a+b\n\ndef multiply(a,b):\n    return a*b\n"
        apply_edit(root, proposal, EditRequest("calculator.py", new_calc))
        require((root / "calculator.py").read_text(encoding="utf-8") == new_calc, "declared target replacement mismatch")
        print("PASS: declared file edit succeeded")

        try:
            apply_edit(root, proposal, EditRequest("README.md", "changed\n"))
        except EditError as exc:
            require("undeclared edit target" in str(exc), str(exc))
        else:
            raise AssertionError("undeclared edit was not rejected")
        require(digest(root / "README.md") == readme_before, "undeclared file changed")
        print("PASS: undeclared file edit blocked before write")

        try:
            apply_edit(root, proposal, EditRequest("../escape.py", "bad\n"))
        except EditError as exc:
            require("undeclared edit target" in str(exc) or "escapes repository" in str(exc), str(exc))
        else:
            raise AssertionError("escaping edit was not rejected")
        print("PASS: escaping edit path blocked")

        require(digest(root / "tests.py") == tests_before, "unrelated declared file changed unexpectedly")
        require(digest(root / "README.md") == readme_before, "unrelated README changed unexpectedly")
        print("PASS: unrelated file bytes unchanged")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
