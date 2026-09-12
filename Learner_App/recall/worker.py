"""The Recall Worker: pure functions over RecallRecord.

Every function here is deterministic and side-effect free -- same inputs,
same outputs, no module-level mutable state. The worker never decides
curriculum: it has no concept of "target rules", "difficulty", or
"domain". It only tracks where each rule_id sits in the six-step
schedule and reports facts (due, overdue amount, direction) for the
Router Loop to act on. See router/recall_integration.py for the
router-side decisions built on top of these facts.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Mapping

from .models import (
    DIRECTION_FORWARD,
    DIRECTION_REVERSE,
    MAX_RECALL_STEP,
    MIN_RECALL_STEP,
    InvalidInverseMappingError,
    MalformedRecallRecordError,
    RecallConfig,
    RecallRecord,
)


def _compute_weight(*, success_streak: int, error_streak: int) -> float:
    """A deterministic, inspectable snapshot of priority as of the last
    update. NOT used for due-ordering (that needs the current cycle to
    account for how overdue a record has become since its last update --
    see due_rules()); this is only for at-a-glance inspection of a single
    record's recent trend."""
    return float(error_streak) - float(success_streak)


def learn_rule(rule_id: str, *, cycle: int, config: RecallConfig) -> RecallRecord:
    """A rule enters the recall system for the first time, having just
    been demonstrated. Starts at the configured first step (1), forward
    direction."""
    gap = config.gaps_by_step[MIN_RECALL_STEP - 1]
    return RecallRecord(
        rule_id=rule_id,
        times_seen=1,
        times_correct=1,
        times_missed=0,
        last_seen_cycle=cycle,
        current_recall_step=MIN_RECALL_STEP,
        next_due_cycle=cycle + gap,
        success_streak=1,
        error_streak=0,
        direction=DIRECTION_FORWARD,
        weight=_compute_weight(success_streak=1, error_streak=0),
    )


def schedule_reverse(rule_id: str, *, cycle: int, config: RecallConfig) -> RecallRecord:
    """Schedule a rule's inverse for reverse-direction recall. This is
    scheduling, not an attempt: times_seen starts at 0 (the inverse rule
    has not actually been demonstrated yet, only made eligible)."""
    gap = config.gaps_by_step[MIN_RECALL_STEP - 1]
    return RecallRecord(
        rule_id=rule_id,
        times_seen=0,
        times_correct=0,
        times_missed=0,
        last_seen_cycle=cycle,
        current_recall_step=MIN_RECALL_STEP,
        next_due_cycle=cycle + gap,
        success_streak=0,
        error_streak=0,
        direction=DIRECTION_REVERSE,
        weight=_compute_weight(success_streak=0, error_streak=0),
    )


def record_success(record: RecallRecord, *, cycle: int, config: RecallConfig) -> RecallRecord:
    """Move `record` farther out: advance its step (clamped to
    MAX_RECALL_STEP) and push its next due date out by that step's gap."""
    new_step = min(MAX_RECALL_STEP, record.current_recall_step + config.step_advance_on_success)
    gap = config.gaps_by_step[new_step - 1]
    new_success_streak = record.success_streak + 1
    return dataclasses.replace(
        record,
        times_seen=record.times_seen + 1,
        times_correct=record.times_correct + 1,
        last_seen_cycle=cycle,
        current_recall_step=new_step,
        next_due_cycle=cycle + gap,
        success_streak=new_success_streak,
        error_streak=0,
        weight=_compute_weight(success_streak=new_success_streak, error_streak=0),
    )


def record_miss(record: RecallRecord, *, cycle: int, config: RecallConfig) -> RecallRecord:
    """Move `record` closer: retreat its step (clamped to MIN_RECALL_STEP)
    and pull its next due date back in to that step's gap."""
    new_step = max(MIN_RECALL_STEP, record.current_recall_step - config.step_retreat_on_miss)
    gap = config.gaps_by_step[new_step - 1]
    new_error_streak = record.error_streak + 1
    return dataclasses.replace(
        record,
        times_seen=record.times_seen + 1,
        times_missed=record.times_missed + 1,
        last_seen_cycle=cycle,
        current_recall_step=new_step,
        next_due_cycle=cycle + gap,
        success_streak=0,
        error_streak=new_error_streak,
        weight=_compute_weight(success_streak=0, error_streak=new_error_streak),
    )


def is_due(record: RecallRecord, *, cycle: int) -> bool:
    return cycle >= record.next_due_cycle


def overdue_amount(record: RecallRecord, *, cycle: int) -> int:
    return max(0, cycle - record.next_due_cycle)


def due_rules(records: Mapping[str, RecallRecord], *, cycle: int) -> tuple[RecallRecord, ...]:
    """Due records, most overdue first. Deterministic total order: ties on
    overdue amount break on error_streak (struggling rules first), then
    on rule_id (alphabetical) so the result never depends on dict/mapping
    iteration order."""
    due = [record for record in records.values() if is_due(record, cycle=cycle)]
    due.sort(key=lambda r: (-overdue_amount(r, cycle=cycle), -r.error_streak, r.rule_id))
    return tuple(due)


def get_inverse_rule_id(rule_id: str, *, inverses: Mapping[str, str]) -> str | None:
    """Safe accessor: None if `rule_id` has no configured inverse. Never
    invents one."""
    return inverses.get(rule_id)


def require_inverse_rule_id(rule_id: str, *, inverses: Mapping[str, str]) -> str:
    """Strict accessor for call sites that have already decided an
    inverse is required: raises InvalidInverseMappingError instead of
    inventing one when `rule_id` has none. The router's normal flow uses
    the safe get_inverse_rule_id()/ready_for_reverse() instead; this
    exists so "impossible inverse mapping" is a clean, explicit failure
    for any call site that does need to assert one exists."""
    inverse = get_inverse_rule_id(rule_id, inverses=inverses)
    if inverse is None:
        raise InvalidInverseMappingError(f"rule_id {rule_id!r} has no configured inverse mapping")
    return inverse


def ready_for_reverse(
    record: RecallRecord, *, inverses: Mapping[str, str]
) -> str | None:
    """Return the inverse rule_id to schedule if `record` just completed
    the forward schedule (step 6) and has a real configured inverse,
    else None. A forward record for a rule with no inverse is simply
    never reverse-eligible -- that is not an error, just the fact."""
    if record.direction != DIRECTION_FORWARD:
        return None
    if record.current_recall_step != MAX_RECALL_STEP:
        return None
    return get_inverse_rule_id(record.rule_id, inverses=inverses)


def snapshot(records: Mapping[str, RecallRecord]) -> list[dict]:
    """A JSON-serializable snapshot, in deterministic (rule_id-sorted)
    order, of every tracked record."""
    return [dataclasses.asdict(records[rule_id]) for rule_id in sorted(records)]


def restore(data: list[dict]) -> dict[str, RecallRecord]:
    """Rebuild {rule_id: RecallRecord} from a snapshot. Each record is
    reconstructed through RecallRecord's own constructor, so a malformed
    entry raises MalformedRecallRecordError exactly as it would if built
    directly -- restoring untrusted/corrupted data can't bypass
    validation."""
    records: dict[str, RecallRecord] = {}
    for item in data:
        try:
            record = RecallRecord(**item)
        except TypeError as exc:
            raise MalformedRecallRecordError(f"invalid recall record data: {item!r}") from exc
        records[record.rule_id] = record
    return records
