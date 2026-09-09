"""State Machine A: the live learner/task interaction state.

Five states, one allowed cycle, five transition functions -- each function
names the exact edge it performs and validates the state it starts from.
An out-of-order call raises IllegalTaskTransitionError instead of being
silently coerced.

    IDLE --assign_problem--> PRIMED --present_to_learner--> EXECUTING
      ^                                                         |
      |                                                  receive_attempt
      |                                                         v
      +--resolve_cycle-- RESOLVING <--apply_route_decision-- VECTORING
"""

from __future__ import annotations

from dataclasses import replace

from .models import LearnerTaskState, TaskLifecycle


class IllegalTaskTransitionError(ValueError):
    """Raised when a transition is attempted from a state that does not
    permit it. The state is never coerced into a valid one silently."""

    def __init__(self, attempted: str, expected: TaskLifecycle, actual: TaskLifecycle):
        self.attempted = attempted
        self.expected = expected
        self.actual = actual
        super().__init__(
            f"{attempted}() requires lifecycle_state={expected!s}, got {actual!s}"
        )


def _require(state: LearnerTaskState, expected: TaskLifecycle, attempted: str) -> None:
    if state.lifecycle_state != expected:
        raise IllegalTaskTransitionError(attempted, expected, state.lifecycle_state)


def assign_problem(
    state: LearnerTaskState, problem_id: str, rule_targets: tuple[str, ...]
) -> LearnerTaskState:
    """IDLE -> PRIMED. Only called after a GeneratedProblem has already
    passed Phase 1 verification -- a rejected/unverified packet must never
    reach this transition."""
    _require(state, TaskLifecycle.IDLE, "assign_problem")
    return replace(
        state,
        lifecycle_state=TaskLifecycle.PRIMED,
        current_problem_id=problem_id,
        current_rule_targets=tuple(rule_targets),
        attempt_count=0,
        waiting_for_input=False,
    )


def present_to_learner(state: LearnerTaskState) -> LearnerTaskState:
    """PRIMED -> EXECUTING."""
    _require(state, TaskLifecycle.PRIMED, "present_to_learner")
    return replace(state, lifecycle_state=TaskLifecycle.EXECUTING, waiting_for_input=True)


def receive_attempt(state: LearnerTaskState) -> LearnerTaskState:
    """EXECUTING -> VECTORING."""
    _require(state, TaskLifecycle.EXECUTING, "receive_attempt")
    return replace(
        state,
        lifecycle_state=TaskLifecycle.VECTORING,
        attempt_count=state.attempt_count + 1,
        waiting_for_input=False,
    )


def apply_route_decision(state: LearnerTaskState) -> LearnerTaskState:
    """VECTORING -> RESOLVING."""
    _require(state, TaskLifecycle.VECTORING, "apply_route_decision")
    return replace(state, lifecycle_state=TaskLifecycle.RESOLVING)


def resolve_cycle(state: LearnerTaskState) -> LearnerTaskState:
    """RESOLVING -> IDLE. Always the clean boundary state: no active
    problem, no rule targets carried over."""
    _require(state, TaskLifecycle.RESOLVING, "resolve_cycle")
    return replace(
        state,
        lifecycle_state=TaskLifecycle.IDLE,
        current_problem_id=None,
        current_rule_targets=(),
        attempt_count=0,
        waiting_for_input=False,
    )
