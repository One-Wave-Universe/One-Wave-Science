"""Data contracts for the Phase 3 Recall Worker.

The Recall Worker is a worker under Router authority -- like Phase 1's
problem builder -- not a third state machine. It reports facts (which
rules are due, how overdue, current step, direction, recent history);
it never decides curriculum. See `Learner_App/router/recall_integration.py`
for where the Router Loop turns those facts into decisions.
"""

from __future__ import annotations

from dataclasses import dataclass

DIRECTION_FORWARD = "forward"
DIRECTION_REVERSE = "reverse"
VALID_DIRECTIONS = (DIRECTION_FORWARD, DIRECTION_REVERSE)

# The schedule is definitionally six steps -- these bounds are fixed, not
# configuration (RecallConfig configures the *gaps* and step *size*, not
# how many steps exist).
MIN_RECALL_STEP = 1
MAX_RECALL_STEP = 6


class RecallError(Exception):
    """Base class for recall-worker failures."""


class MalformedRecallRecordError(RecallError):
    """Raised when a RecallRecord's fields are not internally consistent --
    an input-boundary check, enforced at construction so a malformed
    record can never exist, whether built directly or restored from a
    snapshot."""


class UnknownRuleError(RecallError):
    """Raised when the router tries to schedule recall for a rule_id it
    does not recognize as part of the active curriculum/rule universe."""


class InvalidInverseMappingError(RecallError):
    """Raised when code asks for a required inverse mapping on a rule that
    does not have one. The safe accessor (get_inverse_rule_id) returns
    None instead of raising; this is for call sites that have already
    decided an inverse is required and would be a bug if there wasn't
    one -- it exists so 'invent a fake inverse' is never a silent option."""


@dataclass(frozen=True)
class RecallRecord:
    """One rule's position in the six-step recall schedule.

    Immutable: every update (record_success/record_miss in worker.py)
    returns a new RecallRecord rather than mutating this one, so a
    RouterLoop's recall state is always an explicit, replaceable mapping
    {rule_id: RecallRecord}, never something updated in place behind the
    router's back.
    """

    rule_id: str
    times_seen: int
    times_correct: int
    times_missed: int
    last_seen_cycle: int
    current_recall_step: int  # 1..6
    next_due_cycle: int
    success_streak: int
    error_streak: int
    direction: str  # "forward" | "reverse"
    weight: float  # last-computed priority snapshot; see worker.due_rules()
    # for the live, authoritative ordering used to pick what's due now.

    def __post_init__(self) -> None:
        errors: list[str] = []
        if not self.rule_id:
            errors.append("rule_id must not be empty")
        if not (MIN_RECALL_STEP <= self.current_recall_step <= MAX_RECALL_STEP):
            errors.append(
                f"current_recall_step {self.current_recall_step!r} must be within "
                f"[{MIN_RECALL_STEP}, {MAX_RECALL_STEP}]"
            )
        if self.direction not in VALID_DIRECTIONS:
            errors.append(f"direction {self.direction!r} must be one of {VALID_DIRECTIONS}")
        if self.times_seen < 0 or self.times_correct < 0 or self.times_missed < 0:
            errors.append("times_seen/times_correct/times_missed must be non-negative")
        if self.times_correct + self.times_missed > self.times_seen:
            errors.append("times_correct + times_missed cannot exceed times_seen")
        if self.success_streak < 0 or self.error_streak < 0:
            errors.append("success_streak/error_streak must be non-negative")
        if self.last_seen_cycle < 0 or self.next_due_cycle < 0:
            errors.append("last_seen_cycle/next_due_cycle must be non-negative")
        if errors:
            raise MalformedRecallRecordError("; ".join(errors))


@dataclass(frozen=True)
class RecallConfig:
    """Explicit, deterministic configuration -- no magic numbers scattered
    through the recall algorithm itself.

    `gaps_by_step[step - 1]` is how many cycles must pass before a rule at
    that step becomes due again. Must have exactly six (positive) entries,
    matching the fixed six-step schedule.
    """

    gaps_by_step: tuple[int, ...] = (1, 3, 7, 14, 30, 60)
    step_advance_on_success: int = 1
    step_retreat_on_miss: int = 1

    def __post_init__(self) -> None:
        if len(self.gaps_by_step) != MAX_RECALL_STEP:
            raise ValueError(
                f"gaps_by_step must have exactly {MAX_RECALL_STEP} entries, "
                f"got {len(self.gaps_by_step)}"
            )
        if any(gap <= 0 for gap in self.gaps_by_step):
            raise ValueError("gaps_by_step entries must all be positive")
        if self.step_advance_on_success <= 0 or self.step_retreat_on_miss <= 0:
            raise ValueError("step_advance_on_success/step_retreat_on_miss must be positive")
