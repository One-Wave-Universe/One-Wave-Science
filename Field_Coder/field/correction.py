"""Bounded failure-evidence transitions for Field Coder Step 09."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum

from field.state import FieldState
from field.test_runner import TestEvidence


class CorrectionError(RuntimeError):
    """Raised when a correction transition would violate the three-attempt law."""


class CorrectionDecision(str, Enum):
    PASS = "PASS"
    RETRY = "RETRY"
    REPLAN = "REPLAN"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class CorrectionOutcome:
    decision: CorrectionDecision
    state: FieldState


def evidence_record(evidence: TestEvidence) -> dict[str, object]:
    """Convert execution evidence into JSON-safe persistent state evidence."""
    return {
        "command": evidence.command,
        "argv": list(evidence.argv),
        "stdout": evidence.stdout,
        "stderr": evidence.stderr,
        "exit_code": evidence.exit_code,
        "timed_out": evidence.timed_out,
        "passed": evidence.passed,
    }


def apply_test_evidence(state: FieldState, evidence: TestEvidence) -> CorrectionOutcome:
    """Apply one test result to Field state without permitting a fourth attempt."""
    state.validate()

    if state.next_action == "blocked":
        raise CorrectionError("blocked state cannot transition to a fourth attempt")

    record = evidence_record(evidence)

    if evidence.passed:
        next_state = replace(
            state,
            last_action="test_passed",
            last_result=record,
            next_action="review_ready",
        )
        return CorrectionOutcome(CorrectionDecision.PASS, next_state)

    if state.attempt < 1:
        raise CorrectionError("failure transition requires an active attempt")

    if state.attempt == 1:
        next_state = replace(
            state,
            attempt=2,
            last_action="test_failed_attempt_1",
            last_result=record,
            next_action="evidence_based_correction",
        )
        return CorrectionOutcome(CorrectionDecision.RETRY, next_state)

    if state.attempt == 2:
        next_state = replace(
            state,
            attempt=3,
            last_action="test_failed_attempt_2",
            last_result=record,
            next_action="materially_different_correction",
        )
        return CorrectionOutcome(CorrectionDecision.REPLAN, next_state)

    if state.attempt == state.max_attempts == 3:
        next_state = replace(
            state,
            last_action="test_failed_attempt_3",
            last_result=record,
            next_action="blocked",
        )
        return CorrectionOutcome(CorrectionDecision.BLOCKED, next_state)

    raise CorrectionError(
        f"unsupported attempt state: {state.attempt}/{state.max_attempts}"
    )
