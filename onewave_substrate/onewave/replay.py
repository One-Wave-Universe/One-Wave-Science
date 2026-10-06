"""Deterministic replay: state must be reproducible from events alone.

replay(db, runtime_id) walks a runtime's own append-only event log from
the beginning and reconstructs its local (field_state, displacement,
memory_state) purely from the recorded (a, b) transition inputs -- it
never reads the runtime_records pointer row. verify_replay() then checks
that reconstruction against the persisted pointer, which is the contract
tests/test_replay.py exercises across 100 transitions.
"""

from __future__ import annotations

from dataclasses import dataclass

from onewave.events import PathEvent, get_events
from onewave.storage.sqlite import Storage
from onewave.transition import State, TransitionParams, transition


class ReplayError(Exception):
    """Raised when a persisted event's recorded outcome does not match
    what a fresh transition() call over the same (state, a, b, params)
    produces -- i.e. the log has been tampered with or params drifted."""


@dataclass(frozen=True)
class ReplayResult:
    runtime_id: str
    final_state: State
    events_replayed: int


def replay(
    db: Storage,
    runtime_id: str,
    params: TransitionParams = TransitionParams(),
    strict: bool = True,
) -> ReplayResult:
    """Rebuild a runtime's local state from its event log alone.

    strict=True (default) re-verifies every non-genesis event by rerunning
    transition() and comparing the recorded resulting state to the
    freshly computed one; a mismatch raises ReplayError immediately,
    pinpointing the first divergent event.
    """
    events: list[PathEvent] = get_events(db, runtime_id)
    if not events:
        raise ValueError(f"no events found for runtime_id: {runtime_id!r}")

    state = State()
    for event in events:
        if event.kind == "genesis":
            state = State(event.resulting_field, event.resulting_displacement, event.resulting_memory)
            continue

        new_state, gate_result = transition(state, event.a, event.b, params)

        if strict:
            recorded = State(event.resulting_field, event.resulting_displacement, event.resulting_memory)
            if new_state != recorded or gate_result != event.gate_result:
                raise ReplayError(
                    f"replay diverged at event {event.event_id} (seq={event.seq}): "
                    f"recomputed {new_state!r} (gate={gate_result!r}) != "
                    f"recorded {recorded!r} (gate={event.gate_result!r})"
                )
        state = new_state

    return ReplayResult(runtime_id=runtime_id, final_state=state, events_replayed=len(events))


def verify_replay(
    db: Storage,
    runtime_id: str,
    params: TransitionParams = TransitionParams(),
) -> bool:
    """True iff replaying the event log exactly reproduces the persisted
    runtime_records pointer for this lineage."""
    from onewave.runtime import get_runtime  # local import: avoid a cycle

    current = get_runtime(db, runtime_id)
    if current is None:
        raise ValueError(f"unknown runtime_id: {runtime_id!r}")

    result = replay(db, runtime_id, params)
    return result.final_state == current.local_state
