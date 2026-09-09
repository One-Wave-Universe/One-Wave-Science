"""Data contracts for the Phase 2 router loop.

Two state machines, connected by one router loop:

    STATE MACHINE A (LearnerTaskState) <-> ROUTER LOOP <-> STATE MACHINE B (EvaluatorState)
                                               |
                                            WORKERS (Phase 1 problem builder)

The router loop is the orchestrator, not a third state machine. It owns
routing/sequencing decisions (RouteDecision); State Machine A owns the live
task/interaction state; State Machine B owns evaluation of a learner
attempt into structured evidence (EvaluationEvidence). Neither state
machine, nor any worker, may choose curriculum rules on its own -- that
authority belongs to the router loop alone.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any


def _as_tuple(value: Any) -> tuple[str, ...]:
    return tuple(value) if value else ()


def _freeze_mapping(value: Mapping[str, Any] | None) -> MappingProxyType:
    items = dict(value) if value else {}
    return MappingProxyType(dict(items))


class TaskLifecycle(str, Enum):
    """State Machine A's five states, in their one allowed cycle order:
    IDLE -> PRIMED -> EXECUTING -> VECTORING -> RESOLVING -> IDLE."""

    IDLE = "IDLE"
    PRIMED = "PRIMED"
    EXECUTING = "EXECUTING"
    VECTORING = "VECTORING"
    RESOLVING = "RESOLVING"


@dataclass(frozen=True)
class LearnerTaskState:
    """State Machine A: the live learner/task interaction state.

    Owned fields only -- this never carries routing decisions (those are
    the router's RouteDecision) or evaluation results (those are the
    evaluator's EvaluationEvidence).
    """

    lifecycle_state: TaskLifecycle
    current_problem_id: str | None
    current_rule_targets: tuple[str, ...]
    attempt_count: int
    waiting_for_input: bool
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "current_rule_targets", _as_tuple(self.current_rule_targets))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))


class EvaluationLifecycle(str, Enum):
    """State Machine B's three states, in their one allowed cycle order:
    IDLE -> EVALUATING -> EMITTED -> IDLE."""

    IDLE = "IDLE"
    EVALUATING = "EVALUATING"
    EMITTED = "EMITTED"


@dataclass(frozen=True)
class EvaluatorState:
    """State Machine B: bookkeeping around the evaluation-in-progress."""

    lifecycle_state: EvaluationLifecycle
    last_evidence: "EvaluationEvidence | None"
    evaluation_count: int


@dataclass(frozen=True)
class LearnerAttempt:
    """The event that starts an evaluation: what a learner did, already
    classified into an outcome by whatever graded it (out of scope for
    this phase -- a human, a test harness, or a future answer-checking
    component per CLAUDE.md's "later explicitly authorized component").

    `reported_rules_used` lets State Machine B compute which of the
    problem's target rules were NOT demonstrated -- a domain-agnostic set
    comparison, not a re-derivation of the hidden answer.
    """

    problem_id: str
    outcome: str  # "correct" | "incorrect" | "incomplete"
    reported_rules_used: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "reported_rules_used", _as_tuple(self.reported_rules_used))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))


VALID_OUTCOMES = ("correct", "incorrect", "incomplete")


@dataclass(frozen=True)
class EvaluationEvidence:
    """State Machine B's output: structured evidence, not a routing
    decision. The router reads this; it does not have to obey it."""

    problem_id: str
    outcome: str
    error_kind: str | None
    demonstrated_rules: tuple[str, ...]
    missing_rules: tuple[str, ...]
    confidence: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "demonstrated_rules", _as_tuple(self.demonstrated_rules))
        object.__setattr__(self, "missing_rules", _as_tuple(self.missing_rules))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))


class RouteAction(str, Enum):
    """What the router decided the next problem should look like. Not a
    third state machine -- this is the router loop's own decision output,
    consumed by the caller to build the next RulePacket."""

    ADVANCE = "ADVANCE"
    REPEAT = "REPEAT"
    REDUCE_DIFFICULTY = "REDUCE_DIFFICULTY"
    EXPLAIN = "EXPLAIN"


@dataclass(frozen=True)
class RouteDecision:
    """The router's decision: which rules, difficulty, and domain the
    next RulePacket should carry, and why. `reason_code` is a short
    machine-readable token, not a paragraph -- see policy.py for the
    fixed vocabulary."""

    action: RouteAction
    target_rules: tuple[str, ...]
    allowed_support_rules: tuple[str, ...]
    forbidden_rules: tuple[str, ...]
    difficulty: int
    domain: str
    seed: int
    reason_code: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "target_rules", _as_tuple(self.target_rules))
        object.__setattr__(self, "allowed_support_rules", _as_tuple(self.allowed_support_rules))
        object.__setattr__(self, "forbidden_rules", _as_tuple(self.forbidden_rules))


def initial_task_state() -> LearnerTaskState:
    return LearnerTaskState(
        lifecycle_state=TaskLifecycle.IDLE,
        current_problem_id=None,
        current_rule_targets=(),
        attempt_count=0,
        waiting_for_input=False,
    )


def initial_evaluator_state() -> EvaluatorState:
    return EvaluatorState(
        lifecycle_state=EvaluationLifecycle.IDLE,
        last_evidence=None,
        evaluation_count=0,
    )
