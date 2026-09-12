"""Full demonstration: emotion + science(standard/one_wave) + mythology in
one shared substrate, then the required demo queries from brief section 23.

Run with:  python -m examples.mixed_fields   (from onewave_substrate/)
"""

from __future__ import annotations

from onewave import ingest, runtime
from onewave.epistemic import EpistemicStatus
from onewave.query import query_concept, render_answer, render_path
from onewave.relations import get_relations_between
from onewave.storage.sqlite import Storage
from onewave.ternary import Ternary
from onewave.transition import TransitionParams

MYTHOLOGY_CONCEPTS = {
    "the_void": ("Void", (
        "Mythic: the pre-differentiated ground state before the first "
        "mirrored split -- the silence a wave departs from and returns to."
    )),
    "angel_13": ("13th Angel", (
        "Mythic: the thirteenth of the named boundary-guardians, said to "
        "preside over unresolved returns."
    )),
    "mega_city": ("Mega City", (
        "Mythic: a legendary maximally-coupled lattice settlement where "
        "every resident's wake overlaps every other's."
    )),
    "harmonic_anchor": ("harmonic anchor", (
        "Mythic: a fixed point in the myth cycle to which wandering paths "
        "are said to return."
    )),
    "big_zip": ("Big Zip", (
        "Mythic: the closing of all open paths into a single point, sung "
        "as the opposite of the Big Rip."
    )),
    "big_rip": ("Big Rip", (
        "Mythic: the unraveling of the lattice into disconnected, "
        "uncoupled points."
    )),
}


def seed_mythology(db: Storage) -> None:
    ingest.add_field(db, "mythology", "Mythology")
    ingest.add_field(db, "mythology.one_wave", "One-Wave Mythology", parent_field_id="mythology")

    for concept_id, (canonical_name, text) in MYTHOLOGY_CONCEPTS.items():
        ingest.ingest_entry(
            db, canonical_name, text, "mythology.one_wave", EpistemicStatus.MYTHOLOGY,
            concept_id=concept_id,
        )

    # mass and gravity also carry symbolic/mythological readings -- stored
    # under the SAME concept_id as their physics definitions, but scoped
    # to mythology.one_wave, so a query without an active field surfaces
    # all three interpretations grouped, never merged.
    ingest.ingest_entry(
        db, "mass",
        "Mythic: the symbolic weight the Void grants to a thing that "
        "resists return.",
        "mythology.one_wave", EpistemicStatus.MYTHOLOGY,
        relations=[("associated_with", "the_void", "mythology")],
    )
    ingest.ingest_entry(
        db, "gravity",
        "Mythic: the Void's memory of what was pulled apart during the "
        "Big Rip, pulling paths back toward the Big Zip.",
        "mythology.one_wave", EpistemicStatus.MYTHOLOGY,
        relations=[
            ("associated_with", "big_rip", "mythology"),
            ("associated_with", "big_zip", "mythology"),
        ],
    )

    ingest.add_relation(db, "big_zip", "big_rip", "mythology.one_wave",
                         "opposes", EpistemicStatus.MYTHOLOGY)
    ingest.add_relation(db, "angel_13", "harmonic_anchor", "mythology.one_wave",
                         "associated_with", EpistemicStatus.MYTHOLOGY)
    ingest.add_relation(db, "mega_city", "harmonic_anchor", "mythology.one_wave",
                         "emerges_from", EpistemicStatus.MYTHOLOGY)


def build_demo_db() -> Storage:
    import examples.emotions as emotions
    import examples.science as science

    db = Storage(":memory:")
    emotions.seed(db)
    science.seed(db)
    seed_mythology(db)
    return db


def _section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def run_demo() -> None:
    db = build_demo_db()
    params = TransitionParams()

    _section('Query 1: "What is anger?"')
    print(render_answer(query_concept(db, "anger")))

    _section('Query 2: "What is anger in the behavior field?"')
    print(render_answer(query_concept(db, "anger", active_field="behavior")))

    _section('Query 3: "What is gravity?" (standard physics vs One-Wave candidate)')
    print(render_answer(query_concept(db, "gravity")))

    _section('Query 4: "What does \'Void\' mean?"')
    print(render_answer(query_concept(db, "Void")))

    _section('Query 5: "How is fear related to anger?"')
    rels = get_relations_between(db, "fear", "anger")
    if not rels:
        print("(no direct relations found; checking anger -> fear)")
        rels = get_relations_between(db, "anger", "fear")
    for r in rels:
        print(f"  fear {r.relation_type.value} anger  [{r.epistemic_status.value}, field={r.field_id}]")

    _section('Query 6: "Show the path that caused this runtime record to enter RETURN."')
    rt = runtime.create_runtime(db, "gravity", "science.physics.one_wave")
    while runtime.get_field(db, rt.runtime_id, params) != Ternary.RETURN:
        rt, _ = runtime.apply_transition(db, rt.runtime_id, Ternary.ADVANCE, Ternary.ADVANCE, params)
    print(f"runtime_id={rt.runtime_id} entered RETURN after "
          f"{len(runtime.get_path(db, rt.runtime_id)) - 1} transitions")
    print(render_path(runtime.get_path(db, rt.runtime_id)))

    _section('Query 7: "Spawn a child field from this state and evolve it independently."')
    child = runtime.spawn_child(db, rt.runtime_id, mode="snapshot")
    print(f"spawned snapshot child {child.runtime_id} from parent {rt.runtime_id} "
          f"at state {child.local_state}")
    for _ in range(3):
        child, _ = runtime.apply_transition(db, child.runtime_id, Ternary.RETURN, Ternary.RETURN, params)
    parent_now = runtime.get_runtime(db, rt.runtime_id)
    print(f"child evolved independently to  {child.local_state}")
    print(f"parent, untouched, remains at   {parent_now.local_state}")


if __name__ == "__main__":
    run_demo()
