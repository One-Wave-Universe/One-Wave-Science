import pytest

from onewave import fields, concepts, runtime, replay
from onewave.ternary import Ternary
from onewave.transition import TransitionParams


def _seeded_root(db):
    fields.add_field(db, "science", "Science")
    concepts.add_concept(db, "gravity", "gravity")
    rt = runtime.create_runtime(db, "gravity", "science")
    params = TransitionParams()
    for _ in range(4):
        rt, _ = runtime.apply_transition(db, rt.runtime_id, Ternary.ADVANCE, Ternary.ADVANCE, params)
    return rt, params


def test_snapshot_child_origin_matches_parent_at_spawn_time(db):
    rt, params = _seeded_root(db)
    child = runtime.spawn_child(db, rt.runtime_id, mode="snapshot")
    assert child.spawn_mode == "snapshot"
    assert child.local_state == rt.local_state


def test_snapshot_child_does_not_move_when_parent_moves_later(db):
    rt, params = _seeded_root(db)
    child = runtime.spawn_child(db, rt.runtime_id, mode="snapshot")
    origin = runtime.get_point(db, child.runtime_id, params)

    for _ in range(10):
        rt, _ = runtime.apply_transition(db, rt.runtime_id, Ternary.RETURN, Ternary.RETURN, params)

    assert runtime.get_point(db, child.runtime_id, params) == origin


def test_snapshot_child_evolves_independently(db):
    rt, params = _seeded_root(db)
    child = runtime.spawn_child(db, rt.runtime_id, mode="snapshot")

    child, _ = runtime.apply_transition(db, child.runtime_id, Ternary.RETURN, Ternary.RETURN, params)
    child, _ = runtime.apply_transition(db, child.runtime_id, Ternary.RETURN, Ternary.RETURN, params)

    assert child.local_state != rt.local_state


def test_live_child_starts_at_zero_relative_offset(db):
    rt, params = _seeded_root(db)
    child = runtime.spawn_child(db, rt.runtime_id, mode="live")
    assert child.spawn_mode == "live"
    # Immediately after spawn, before the child makes its own move, its
    # effective displacement equals the parent's current displacement
    # (relative offset 0) -- only displacement composes per X_C(t) =
    # X_P(t) + Delta_{C|P}(t). memory_state stays local to the child (see
    # runtime.py docstring), so it need not match the parent's.
    child_point = runtime.get_point(db, child.runtime_id, params)
    parent_point = runtime.get_point(db, rt.runtime_id, params)
    assert child_point.displacement == parent_point.displacement
    assert child.memory_state == 0.0


def test_live_child_tracks_parent_motion(db):
    rt, params = _seeded_root(db)
    child = runtime.spawn_child(db, rt.runtime_id, mode="live")

    parent_before = runtime.get_point(db, rt.runtime_id, params)
    rt, _ = runtime.apply_transition(db, rt.runtime_id, Ternary.RETURN, Ternary.RETURN, params)
    parent_after = runtime.get_point(db, rt.runtime_id, params)

    assert parent_after.displacement != parent_before.displacement

    child_point = runtime.get_point(db, child.runtime_id, params)
    # X_C(t) = X_P(t) + Delta_{C|P}(t); child's own relative displacement
    # is still 0, so its effective displacement must equal the parent's.
    assert child_point.displacement == parent_after.displacement


def test_live_child_composes_own_relative_motion_with_parent(db):
    rt, params = _seeded_root(db)
    child = runtime.spawn_child(db, rt.runtime_id, mode="live")

    child, _ = runtime.apply_transition(db, child.runtime_id, Ternary.ADVANCE, Ternary.ADVANCE, params)
    parent_point = runtime.get_point(db, rt.runtime_id, params)
    child_point = runtime.get_point(db, child.runtime_id, params)

    assert child_point.displacement == pytest.approx(parent_point.displacement + child.displacement)


def test_snapshot_and_live_modes_are_not_blurred(db):
    rt, params = _seeded_root(db)
    snap = runtime.spawn_child(db, rt.runtime_id, mode="snapshot")
    live = runtime.spawn_child(db, rt.runtime_id, mode="live")

    for _ in range(3):
        rt, _ = runtime.apply_transition(db, rt.runtime_id, Ternary.RETURN, Ternary.RETURN, params)

    snap_point = runtime.get_point(db, snap.runtime_id, params)
    live_point = runtime.get_point(db, live.runtime_id, params)
    parent_point = runtime.get_point(db, rt.runtime_id, params)

    assert snap_point.displacement != parent_point.displacement
    assert live_point.displacement == parent_point.displacement


def test_invalid_spawn_mode_rejected(db):
    rt, _ = _seeded_root(db)
    with pytest.raises(ValueError):
        runtime.spawn_child(db, rt.runtime_id, mode="teleport")


def test_replay_reconstructs_both_snapshot_and_live_children(db):
    rt, params = _seeded_root(db)
    snap = runtime.spawn_child(db, rt.runtime_id, mode="snapshot")
    live = runtime.spawn_child(db, rt.runtime_id, mode="live")

    for _ in range(5):
        snap, _ = runtime.apply_transition(db, snap.runtime_id, Ternary.ADVANCE, Ternary.ADVANCE, params)
    for _ in range(5):
        live, _ = runtime.apply_transition(db, live.runtime_id, Ternary.RETURN, Ternary.RETURN, params)

    assert replay.verify_replay(db, snap.runtime_id, params)
    assert replay.verify_replay(db, live.runtime_id, params)
