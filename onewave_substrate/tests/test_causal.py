"""Causal graph: two independent runtime lineages feeding a third.

Local path order within one runtime_id stays authoritative on its own;
cross-lineage causality is only ever the explicit causal_edges recorded
via `causal_parents`, never inferred from timestamps or global sequence.
"""

from onewave import fields, concepts, runtime
from onewave.events import get_causal_children, get_causal_parents, get_events
from onewave.ternary import Ternary
from onewave.transition import TransitionParams


def test_two_independent_lineages_feed_a_third(db):
    fields.add_field(db, "science", "Science")
    concepts.add_concept(db, "a", "concept a")
    concepts.add_concept(db, "b", "concept b")
    concepts.add_concept(db, "c", "concept c")
    params = TransitionParams()

    rt_a = runtime.create_runtime(db, "a", "science")
    rt_b = runtime.create_runtime(db, "b", "science")
    rt_c = runtime.create_runtime(db, "c", "science")

    rt_a, event_a = runtime.apply_transition(db, rt_a.runtime_id, Ternary.ADVANCE, Ternary.ADVANCE, params)
    rt_b, event_b = runtime.apply_transition(db, rt_b.runtime_id, Ternary.ADVANCE, Ternary.ADVANCE, params)

    # c's transition is explicitly caused by both a's and b's prior events.
    rt_c, event_c = runtime.apply_transition(
        db, rt_c.runtime_id, Ternary.ADVANCE, Ternary.ADVANCE, params,
        causal_parents=(event_a.event_id, event_b.event_id),
    )

    # Local path order stays separate per lineage: each of a/b/c has its
    # own independent seq numbering starting from its own genesis.
    path_a = get_events(db, rt_a.runtime_id)
    path_b = get_events(db, rt_b.runtime_id)
    path_c = get_events(db, rt_c.runtime_id)
    assert [e.seq for e in path_a] == [0, 1]
    assert [e.seq for e in path_b] == [0, 1]
    assert [e.seq for e in path_c] == [0, 1]

    # Cross-lineage causality is recoverable via explicit causal edges.
    parents_of_c = set(get_causal_parents(db, event_c.event_id))
    assert parents_of_c == {event_a.event_id, event_b.event_id}

    assert event_c.event_id in get_causal_children(db, event_a.event_id)
    assert event_c.event_id in get_causal_children(db, event_b.event_id)

    # And the PathEvent object returned inline carries the same info.
    assert set(event_c.causal_parents) == {event_a.event_id, event_b.event_id}


def test_no_causal_edges_without_explicit_declaration(db):
    fields.add_field(db, "science", "Science")
    concepts.add_concept(db, "a", "concept a")
    concepts.add_concept(db, "b", "concept b")
    params = TransitionParams()

    rt_a = runtime.create_runtime(db, "a", "science")
    rt_b = runtime.create_runtime(db, "b", "science")

    rt_a, event_a = runtime.apply_transition(db, rt_a.runtime_id, Ternary.ADVANCE, Ternary.ADVANCE, params)
    rt_b, event_b = runtime.apply_transition(db, rt_b.runtime_id, Ternary.ADVANCE, Ternary.ADVANCE, params)

    # No global ordering/causality is claimed just because b happened
    # after a in wall-clock time -- no edge exists unless declared.
    assert get_causal_parents(db, event_b.event_id) == ()
    assert get_causal_children(db, event_a.event_id) == ()
