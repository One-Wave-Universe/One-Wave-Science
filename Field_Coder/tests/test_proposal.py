"""Step 05 grounded proposal verification."""

from pathlib import Path
import sys

FIELD_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIELD_ROOT))

from field.proposal import ProposalDraft, ProposalError, build_proposal
from field.repo_reader import RepoContext, RepoFile
from field.task_intake import TaskSpec


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def expect_error(task: TaskSpec, context: RepoContext, draft: ProposalDraft, fragment: str) -> None:
    try:
        build_proposal(task, context, draft)
    except ProposalError as exc:
        require(fragment in str(exc), str(exc))
    else:
        raise AssertionError("expected ProposalError")


def fixture():
    task = TaskSpec(
        summary="add multiplication while preserving addition",
        scope=("calculator.py", "tests/test_calculator.py"),
        success_criteria=("multiplication passes", "addition still passes"),
    )
    context = RepoContext(
        root="/fixture",
        branch="fixture-read",
        head="abc123",
        files=(
            RepoFile("calculator.py", "def add(a,b): return a+b\n"),
            RepoFile("tests/test_calculator.py", "def test_add(): pass\n"),
        ),
    )
    return task, context


def valid_draft() -> ProposalDraft:
    return ProposalDraft(
        changes=("add a multiply(a, b) function",),
        reason="the current bounded task requires multiplication support",
        files_expected=("calculator.py", "tests/test_calculator.py"),
        invariants=("existing addition behavior remains unchanged",),
        expected_result="multiplication works and addition still passes",
        success_test="python3 -m pytest tests/test_calculator.py",
    )


def main() -> int:
    task, context = fixture()
    proposal = build_proposal(task, context, valid_draft())
    require(proposal.intended_change == "add a multiply(a, b) function", proposal.intended_change)
    require(proposal.files_expected == task.scope, repr(proposal.files_expected))
    print("PASS: valid grounded single-change proposal accepted")

    d = valid_draft()
    expect_error(task, context, ProposalDraft(d.changes, d.reason, (), d.invariants, d.expected_result, d.success_test), "files expected must not be empty")
    print("PASS: missing target files rejected")

    expect_error(task, context, ProposalDraft(d.changes, d.reason, d.files_expected, (), d.expected_result, d.success_test), "invariants must not be empty")
    print("PASS: missing invariants rejected")

    expect_error(task, context, ProposalDraft(d.changes, d.reason, d.files_expected, d.invariants, d.expected_result, ""), "success test must not be empty")
    print("PASS: missing success test rejected")

    expect_error(task, context, ProposalDraft(("add multiply", "refactor parser"), d.reason, d.files_expected, d.invariants, d.expected_result, d.success_test), "exactly one intended change")
    print("PASS: multi-change proposal rejected")

    expect_error(task, context, ProposalDraft(d.changes, d.reason, ("README.md",), d.invariants, d.expected_result, d.success_test), "outside task scope")
    print("PASS: out-of-scope target rejected")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
