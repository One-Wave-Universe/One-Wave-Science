"""Runtime records: the active, path-dependent state of a concept in a field.

The knowledge graph (concepts/fields/definitions/relations) never mutates
because of runtime activity, and runtime state never rewrites the
knowledge graph -- they are deliberately separate stores connected only by
concept_id/field_id foreign keys.

Point / Path / Field terminology (see brief section 11), made literal:

    get_point(runtime_id) -> the current State (effective, see below)
    get_path(runtime_id)  -> the ordered local event history
    get_field(runtime_id) -> the current field_state (Ternary) of the point

Recursive reference frames (section 12): a runtime can spawn a child in
one of two modes, and the modes are never blurred.

* Snapshot child: `O_C = X_P(t_spawn)`. The child's initial (field_state,
  displacement, memory_state) is copied from the parent at spawn time and
  then evolves completely independently -- later parent motion never
  touches it again. spawn_mode == "snapshot".

* Live child: `X_C(t) = X_P(t) + Delta_{C|P}(t)`. The child stores only
  its own *relative* displacement/memory, starting at the zero state. Its
  effective point is computed at read time by recursively adding the
  parent's current effective displacement -- see get_point(). Only
  displacement composes this way (per the boxed formula); memory_state
  stays local to the child, and the effective field_state is recomputed
  from the composed displacement together with the child's own memory.
  spawn_mode == "live".
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from onewave.events import PathEvent, append_event, append_genesis_event, get_events
from onewave.storage.sqlite import Storage
from onewave.ternary import Ternary
from onewave.transition import State, TransitionParams, phi, transition


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


@dataclass(frozen=True)
class RuntimeRecord:
    runtime_id: str
    concept_id: str
    field_id: str
    field_state: Ternary
    displacement: float
    memory_state: float
    path: str
    parent_runtime_id: str | None
    spawn_mode: str  # "root" | "snapshot" | "live"
    created_at: str

    @property
    def local_state(self) -> State:
        return State(self.field_state, self.displacement, self.memory_state)


def _row_to_runtime(row) -> RuntimeRecord:
    return RuntimeRecord(
        runtime_id=row["runtime_id"],
        concept_id=row["concept_id"],
        field_id=row["field_id"],
        field_state=Ternary(row["field_state"]),
        displacement=row["displacement"],
        memory_state=row["memory_state"],
        path=row["path"],
        parent_runtime_id=row["parent_runtime_id"],
        spawn_mode=row["spawn_mode"],
        created_at=row["created_at"],
    )


def get_runtime(db: Storage, runtime_id: str) -> RuntimeRecord | None:
    row = db.query_one("SELECT * FROM runtime_records WHERE runtime_id = ?", (runtime_id,))
    return _row_to_runtime(row) if row else None


def create_runtime(
    db: Storage,
    concept_id: str,
    field_id: str,
    initial_state: State = State(),
) -> RuntimeRecord:
    runtime_id = _new_id("rt")
    created_at = _now()
    db.execute(
        """
        INSERT INTO runtime_records (
            runtime_id, concept_id, field_id, field_state, displacement,
            memory_state, path, parent_runtime_id, spawn_mode, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            runtime_id, concept_id, field_id, int(initial_state.field_state),
            initial_state.displacement, initial_state.memory_state,
            runtime_id, None, "root", created_at,
        ),
    )
    append_genesis_event(db, runtime_id, initial_state)
    return get_runtime(db, runtime_id)  # type: ignore[return-value]


def apply_transition(
    db: Storage,
    runtime_id: str,
    a: Ternary,
    b: Ternary,
    params: TransitionParams = TransitionParams(),
    causal_parents: tuple[str, ...] = (),
) -> tuple[RuntimeRecord, PathEvent]:
    """Advance one runtime lineage by one transition, append the event,
    and persist the new pointer. This is the only place runtime_records
    rows are ever UPDATEd -- the update always mirrors an appended event,
    so replay() can independently reconstruct the same pointer.
    """
    current = get_runtime(db, runtime_id)
    if current is None:
        raise ValueError(f"unknown runtime_id: {runtime_id!r}")

    previous_state = current.local_state
    new_state, gate_result = transition(previous_state, a, b, params)

    event = append_event(
        db, runtime_id, a, b, gate_result, previous_state, new_state, causal_parents
    )

    db.execute(
        """
        UPDATE runtime_records
        SET field_state = ?, displacement = ?, memory_state = ?
        WHERE runtime_id = ?
        """,
        (int(new_state.field_state), new_state.displacement, new_state.memory_state, runtime_id),
    )
    return get_runtime(db, runtime_id), event  # type: ignore[return-value]


def spawn_child(
    db: Storage,
    parent_runtime_id: str,
    mode: str = "snapshot",
    concept_id: str | None = None,
    field_id: str | None = None,
) -> RuntimeRecord:
    if mode not in ("snapshot", "live"):
        raise ValueError(f"mode must be 'snapshot' or 'live', got {mode!r}")

    parent = get_runtime(db, parent_runtime_id)
    if parent is None:
        raise ValueError(f"unknown parent_runtime_id: {parent_runtime_id!r}")

    child_id = _new_id("rt")
    created_at = _now()
    child_concept_id = concept_id or parent.concept_id
    child_field_id = field_id or parent.field_id

    if mode == "snapshot":
        origin = parent.local_state
    else:  # live: relative offset starts at zero
        origin = State()

    db.execute(
        """
        INSERT INTO runtime_records (
            runtime_id, concept_id, field_id, field_state, displacement,
            memory_state, path, parent_runtime_id, spawn_mode, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            child_id, child_concept_id, child_field_id, int(origin.field_state),
            origin.displacement, origin.memory_state,
            f"{parent.path}/{child_id}", parent_runtime_id, mode, created_at,
        ),
    )
    append_genesis_event(db, child_id, origin)
    return get_runtime(db, child_id)  # type: ignore[return-value]


def get_point(
    db: Storage,
    runtime_id: str,
    params: TransitionParams = TransitionParams(),
) -> State:
    """The effective current state, composing live-child ancestry.

    Root and snapshot-mode records return their own stored state as-is.
    Live-mode records add their parent's effective displacement (computed
    recursively) to their own local displacement, then recompute the
    effective field_state from that composed displacement together with
    their own local memory_state.
    """
    record = get_runtime(db, runtime_id)
    if record is None:
        raise ValueError(f"unknown runtime_id: {runtime_id!r}")

    if record.spawn_mode != "live" or record.parent_runtime_id is None:
        return record.local_state

    parent_point = get_point(db, record.parent_runtime_id, params)
    effective_displacement = record.displacement + parent_point.displacement
    effective_field = phi(record.memory_state, effective_displacement, params)
    return State(
        field_state=effective_field,
        displacement=effective_displacement,
        memory_state=record.memory_state,
    )


def get_field(
    db: Storage,
    runtime_id: str,
    params: TransitionParams = TransitionParams(),
) -> Ternary:
    return get_point(db, runtime_id, params).field_state


def get_path(db: Storage, runtime_id: str) -> list[PathEvent]:
    """The ordered local event history (h_t) for this runtime lineage only.

    Deliberately does not include ancestor events -- local path order is
    authoritative for one lineage; cross-lineage relationships are
    explicit causal edges, not a merged timeline (see events.py).
    """
    return get_events(db, runtime_id)
