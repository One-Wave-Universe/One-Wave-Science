"""Step 09 three-attempt correction-state verification."""

from pathlib import Path
import tempfile
import sys

FIELD_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIELD_ROOT))

from field.correction import (
    CorrectionDecision,
    CorrectionError,
    apply_test_evidence,
)
from field.state import FieldState
from field.test_runner import TestEvidence


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def initial_state() -> FieldState:
    return FieldState(
        goal="repair fixture",
        current_task="make one correction",
        attempt=1,
        max_attempts=3,
        last_action="run_test",
        last_result=None,
        next_action="evaluate_test",
        active_branch="field-coder/09-self-correction",
        active_step="09-self-correction",
    )


def evidence(passed: bool, exit_code: int | None) -> TestEvidence:
    return TestEvidence(
        command="python3 fixture_test.py",
        argv=("python3", "fixture_test.py"),
        stdout="fixture output\n",
        stderr="",
        exit_code=exit_code,
        timed_out=False,
        passed=passed,
    )


def main() -> int:
    failed = evidence(False, 1)

    first = apply_test_evidence(initial_state(), failed)
    require(first.decision is CorrectionDecision.RETRY, repr(first))
    require(first.state.attempt == 2, repr(first.state))
    require(first.state.next_action == "evidence_based_correction", first.state.next_action)
    require(first.state.last_result["exit_code"] == 1, repr(first.state.last_result))
    print("PASS: attempt 1 failure transitions to evidence-based attempt 2")

    second = apply_test_evidence(first.state, failed)
    require(second.decision is CorrectionDecision.REPLAN, repr(second))
    require(second.state.attempt == 3, repr(second.state))
    require(second.state.next_action == "materially_different_correction", second.state.next_action)
    print("PASS: attempt 2 failure transitions to materially different attempt 3")

    third = apply_test_evidence(second.state, failed)
    require(third.decision is CorrectionDecision.BLOCKED, repr(third))
    require(third.state.attempt == 3, repr(third.state))
    require(third.state.next_action == "blocked", third.state.next_action)
    print("PASS: attempt 3 failure enters BLOCKED without attempt 4")

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "blocked.json"
        third.state.save(path)
        restored = FieldState.load(path)
        require(restored == third.state, "blocked state did not survive reload")
        print("PASS: blocked state persisted and restored exactly")

    try:
        apply_test_evidence(third.state, failed)
    except CorrectionError as exc:
        require("fourth attempt" in str(exc), str(exc))
    else:
        raise AssertionError("blocked state allowed a hidden fourth transition")
    print("PASS: fourth retry path is mechanically rejected")

    passed = apply_test_evidence(initial_state(), evidence(True, 0))
    require(passed.decision is CorrectionDecision.PASS, repr(passed))
    require(passed.state.attempt == 1, repr(passed.state))
    require(passed.state.next_action == "review_ready", passed.state.next_action)
    print("PASS: passing evidence routes directly to review-ready")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
