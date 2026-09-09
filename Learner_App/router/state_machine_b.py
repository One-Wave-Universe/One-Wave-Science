"""State Machine B: evaluation of a learner attempt into structured
evidence.

Three states, one allowed cycle:

    IDLE --begin_evaluation--> EVALUATING --emit_evidence--> EMITTED --acknowledge--> IDLE

evaluate_attempt() is the pure evaluation logic: it compares the rules the
attempt reports having demonstrated against the problem's target rules
(both are already-public string sets -- no domain knowledge, no re-solving
of the underlying problem, no access to anything Phase 1 didn't already
expose). It never invents or leaks a "correct answer"; `outcome` is
supplied by the attempt itself, from whatever graded it upstream of this
phase.
"""

from __future__ import annotations

from dataclasses import replace

from .models import (
    VALID_OUTCOMES,
    EvaluationEvidence,
    EvaluationLifecycle,
    EvaluatorState,
    LearnerAttempt,
    LearnerTaskState,
)


class IllegalEvaluationTransitionError(ValueError):
    def __init__(self, attempted: str, expected: EvaluationLifecycle, actual: EvaluationLifecycle):
        self.attempted = attempted
        self.expected = expected
        self.actual = actual
        super().__init__(
            f"{attempted}() requires lifecycle_state={expected!s}, got {actual!s}"
        )


class MalformedAttemptError(ValueError):
    """Raised when a LearnerAttempt is not well-formed -- an input
    boundary check, not a grading decision."""


class StaleAttemptError(ValueError):
    """Raised when an attempt's problem_id does not match the task
    state's active problem -- it cannot mutate the active cycle."""


def _require(state: EvaluatorState, expected: EvaluationLifecycle, attempted: str) -> None:
    if state.lifecycle_state != expected:
        raise IllegalEvaluationTransitionError(attempted, expected, state.lifecycle_state)


def begin_evaluation(state: EvaluatorState) -> EvaluatorState:
    """IDLE -> EVALUATING."""
    _require(state, EvaluationLifecycle.IDLE, "begin_evaluation")
    return replace(state, lifecycle_state=EvaluationLifecycle.EVALUATING)


def emit_evidence(state: EvaluatorState, evidence: EvaluationEvidence) -> EvaluatorState:
    """EVALUATING -> EMITTED."""
    _require(state, EvaluationLifecycle.EVALUATING, "emit_evidence")
    return replace(
        state,
        lifecycle_state=EvaluationLifecycle.EMITTED,
        last_evidence=evidence,
        evaluation_count=state.evaluation_count + 1,
    )


def acknowledge(state: EvaluatorState) -> EvaluatorState:
    """EMITTED -> IDLE."""
    _require(state, EvaluationLifecycle.EMITTED, "acknowledge")
    return replace(state, lifecycle_state=EvaluationLifecycle.IDLE)


def validate_attempt(attempt: LearnerAttempt, task_state: LearnerTaskState) -> None:
    """Raise MalformedAttemptError or StaleAttemptError, or return None if
    the attempt is acceptable to evaluate. Pure input-boundary validation:
    this never decides correctness."""
    if attempt.outcome not in VALID_OUTCOMES:
        raise MalformedAttemptError(
            f"attempt.outcome {attempt.outcome!r} is not one of {VALID_OUTCOMES}"
        )
    if not attempt.problem_id:
        raise MalformedAttemptError("attempt.problem_id must not be empty")
    if attempt.problem_id != task_state.current_problem_id:
        raise StaleAttemptError(
            f"attempt for problem_id {attempt.problem_id!r} does not match the active "
            f"problem_id {task_state.current_problem_id!r}"
        )


def evaluate_attempt(attempt: LearnerAttempt, task_state: LearnerTaskState) -> EvaluationEvidence:
    """Build EvaluationEvidence from an already-validated attempt. Caller
    must call validate_attempt() first (the router loop does)."""
    demonstrated = tuple(sorted(set(attempt.reported_rules_used)))
    target = set(task_state.current_rule_targets)
    missing = tuple(sorted(target - set(demonstrated)))

    error_kind = None
    if attempt.outcome != "correct" and missing:
        error_kind = f"missing_rule:{missing[0]}"

    confidence = "high" if not missing else "low"

    return EvaluationEvidence(
        problem_id=attempt.problem_id,
        outcome=attempt.outcome,
        error_kind=error_kind,
        demonstrated_rules=demonstrated,
        missing_rules=missing,
        confidence=confidence,
    )
