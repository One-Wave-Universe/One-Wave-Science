"""Append-only event log and explicit cross-lineage causality.

Within one runtime_id, `seq` (strictly increasing, assigned here) defines
local causal order -- that ordering is authoritative on its own and needs
no other record's cooperation. Across different runtime_ids, nothing may
be inferred from wall-clock time or seq alone: a transition may declare
`causal_parents` (other event_ids, from any lineage) that fed into it,
and those become rows in causal_edges. Local path order and cross-record
causal edges are deliberately two different mechanisms -- see
tests/test_recursive_frames.py / test_causal.py.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from onewave.ternary import Ternary
from onewave.storage.sqlite import Storage
from onewave.transition import State


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


@dataclass(frozen=True)
class PathEvent:
    event_id: str
    runtime_id: str
    seq: int
    kind: str  # "genesis" | "transition"
    a: Ternary
    b: Ternary
    gate_result: Ternary
    previous_field: Ternary
    resulting_field: Ternary
    previous_displacement: float
    resulting_displacement: float
    previous_memory: float
    resulting_memory: float
    created_at: str
    causal_parents: tuple[str, ...] = ()


def _row_to_event(row, causal_parents: tuple[str, ...] = ()) -> PathEvent:
    return PathEvent(
        event_id=row["event_id"],
        runtime_id=row["runtime_id"],
        seq=row["seq"],
        kind=row["kind"],
        a=Ternary(row["a"]),
        b=Ternary(row["b"]),
        gate_result=Ternary(row["gate_result"]),
        previous_field=Ternary(row["previous_field"]),
        resulting_field=Ternary(row["resulting_field"]),
        previous_displacement=row["previous_displacement"],
        resulting_displacement=row["resulting_displacement"],
        previous_memory=row["previous_memory"],
        resulting_memory=row["resulting_memory"],
        created_at=row["created_at"],
        causal_parents=causal_parents,
    )


def _next_seq(db: Storage, runtime_id: str) -> int:
    row = db.query_one(
        "SELECT COALESCE(MAX(seq), -1) AS max_seq FROM path_events WHERE runtime_id = ?",
        (runtime_id,),
    )
    return row["max_seq"] + 1


def append_event(
    db: Storage,
    runtime_id: str,
    a: Ternary,
    b: Ternary,
    gate_result: Ternary,
    previous_state: State,
    resulting_state: State,
    causal_parents: tuple[str, ...] = (),
    kind: str = "transition",
) -> PathEvent:
    event_id = _new_id("evt")
    seq = _next_seq(db, runtime_id)
    created_at = _now()
    db.execute(
        """
        INSERT INTO path_events (
            event_id, runtime_id, seq, kind, a, b, gate_result,
            previous_field, resulting_field,
            previous_displacement, resulting_displacement,
            previous_memory, resulting_memory, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            event_id, runtime_id, seq, kind, int(a), int(b), int(gate_result),
            int(previous_state.field_state), int(resulting_state.field_state),
            previous_state.displacement, resulting_state.displacement,
            previous_state.memory_state, resulting_state.memory_state,
            created_at,
        ),
    )
    for parent_event_id in causal_parents:
        add_causal_edge(db, event_id, parent_event_id)
    return PathEvent(
        event_id=event_id,
        runtime_id=runtime_id,
        seq=seq,
        kind=kind,
        a=a,
        b=b,
        gate_result=gate_result,
        previous_field=previous_state.field_state,
        resulting_field=resulting_state.field_state,
        previous_displacement=previous_state.displacement,
        resulting_displacement=resulting_state.displacement,
        previous_memory=previous_state.memory_state,
        resulting_memory=resulting_state.memory_state,
        created_at=created_at,
        causal_parents=tuple(causal_parents),
    )


def append_genesis_event(db: Storage, runtime_id: str, origin_state: State) -> PathEvent:
    """Record a runtime's creation as seq-0 event, previous_state fixed at
    the zero State(). Not a Gamma/Phi transition -- `kind="genesis"` marks
    it so replay() applies it as a direct state assignment rather than
    running it back through transition().
    """
    return append_event(
        db,
        runtime_id,
        a=Ternary.HOLD,
        b=Ternary.HOLD,
        gate_result=Ternary.HOLD,
        previous_state=State(),
        resulting_state=origin_state,
        kind="genesis",
    )


def get_causal_parents(db: Storage, event_id: str) -> tuple[str, ...]:
    rows = db.query_all(
        "SELECT causal_parent_event_id FROM causal_edges WHERE event_id = ?",
        (event_id,),
    )
    return tuple(r["causal_parent_event_id"] for r in rows)


def get_causal_children(db: Storage, event_id: str) -> tuple[str, ...]:
    rows = db.query_all(
        "SELECT event_id FROM causal_edges WHERE causal_parent_event_id = ?",
        (event_id,),
    )
    return tuple(r["event_id"] for r in rows)


def add_causal_edge(db: Storage, event_id: str, causal_parent_event_id: str) -> None:
    db.execute(
        "INSERT INTO causal_edges (edge_id, event_id, causal_parent_event_id) VALUES (?, ?, ?)",
        (_new_id("edge"), event_id, causal_parent_event_id),
    )


def get_event(db: Storage, event_id: str) -> PathEvent | None:
    row = db.query_one("SELECT * FROM path_events WHERE event_id = ?", (event_id,))
    if row is None:
        return None
    return _row_to_event(row, get_causal_parents(db, event_id))


def get_events(db: Storage, runtime_id: str) -> list[PathEvent]:
    """The ordered local path (h_t) for one runtime lineage."""
    rows = db.query_all(
        "SELECT * FROM path_events WHERE runtime_id = ? ORDER BY seq ASC",
        (runtime_id,),
    )
    return [_row_to_event(r, get_causal_parents(db, r["event_id"])) for r in rows]
