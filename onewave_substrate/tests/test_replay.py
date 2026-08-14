import random

import pytest

from onewave import fields, concepts, runtime
from onewave.replay import ReplayError, replay, verify_replay
from onewave.ternary import Ternary
from onewave.transition import TransitionParams


def _seed(db):
    fields.add_field(db, "science", "Science")
    concepts.add_concept(db, "gravity", "gravity")
    return runtime.create_runtime(db, "gravity", "science")


def test_replay_reproduces_state_after_100_events(db):
    rt = _seed(db)
    params = TransitionParams()
    rng = random.Random(1234)
    choices = list(Ternary)

    for _ in range(100):
        a, b = rng.choice(choices), rng.choice(choices)
        rt, _ = runtime.apply_transition(db, rt.runtime_id, a, b, params)

    assert verify_replay(db, rt.runtime_id, params)

    result = replay(db, rt.runtime_id, params)
    assert result.events_replayed == 101  # 1 genesis + 100 transitions
    assert result.final_state == rt.local_state


def test_replay_survives_loss_of_derived_state(db):
    rt = _seed(db)
    params = TransitionParams()
    rng = random.Random(99)
    choices = list(Ternary)

    for _ in range(100):
        a, b = rng.choice(choices), rng.choice(choices)
        rt, _ = runtime.apply_transition(db, rt.runtime_id, a, b, params)

    before = rt.local_state

    # Simulate loss/corruption of the derived pointer row (runtime_records
    # is a cache -- path_events, referenced by foreign key, is the
    # append-only source of truth and cannot itself be deleted out from
    # under its events). Overwrite the cache with garbage and confirm
    # replay() ignores it entirely, reconstructing purely from the event
    # log and landing back on the pre-corruption state.
    db.execute(
        "UPDATE runtime_records SET field_state = 1, displacement = -999, memory_state = -999 "
        "WHERE runtime_id = ?",
        (rt.runtime_id,),
    )
    assert runtime.get_runtime(db, rt.runtime_id).local_state != before

    result = replay(db, rt.runtime_id, params)
    assert result.final_state == before


def test_replay_detects_tampered_event():
    from onewave.storage.sqlite import Storage

    db = Storage(":memory:")
    rt = _seed(db)
    params = TransitionParams()
    rt, _ = runtime.apply_transition(db, rt.runtime_id, Ternary.ADVANCE, Ternary.ADVANCE, params)
    rt, _ = runtime.apply_transition(db, rt.runtime_id, Ternary.ADVANCE, Ternary.ADVANCE, params)

    # Corrupt the recorded resulting_displacement of the first transition event.
    db.execute(
        "UPDATE path_events SET resulting_displacement = 999 "
        "WHERE runtime_id = ? AND kind = 'transition' AND seq = 1",
        (rt.runtime_id,),
    )

    with pytest.raises(ReplayError):
        replay(db, rt.runtime_id, params)
