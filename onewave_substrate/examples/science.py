"""Demo dataset: `science.physics.standard` and `science.physics.one_wave`.

The same six concepts (mass, gravity, energy, field, wave, frequency) get
two independent definitions each -- one per field -- to demonstrate that
an accepted scientific definition and a One-Wave candidate model never
collapse into a single asserted answer (brief section 15). Six more
concepts are One-Wave-specific vocabulary (Mirror Gate, Point, Path,
Field Rotation, wake, scale locality), defined only in the one_wave field.
"""

from __future__ import annotations

from onewave import ingest
from onewave.epistemic import EpistemicStatus
from onewave.storage.sqlite import Storage

STANDARD_DEFINITIONS = {
    "mass": (
        "A measure of a body's resistance to acceleration under an applied "
        "force (inertial mass) and the source of gravitational attraction "
        "(gravitational mass); measured in kilograms."
    ),
    "gravity": (
        "The attractive interaction between masses, described classically "
        "by Newton's law of universal gravitation and relativistically as "
        "the curvature of spacetime (General Relativity)."
    ),
    "energy": (
        "The capacity of a system to do work; conserved in an isolated "
        "system under the first law of thermodynamics."
    ),
    "field": (
        "A physical quantity, scalar or vector, defined at every point in "
        "space and time (e.g. the electromagnetic field, the gravitational "
        "field)."
    ),
    "wave": (
        "A disturbance that transfers energy through a medium or field "
        "without net transport of matter, characterized by amplitude, "
        "wavelength, and frequency."
    ),
    "frequency": (
        "The number of complete cycles of a periodic phenomenon occurring "
        "per unit time, measured in hertz."
    ),
}

ONE_WAVE_DEFINITIONS = {
    "mass": (
        "Candidate: mass as a local Mirror Gate coupling strength -- "
        "resistance to displacement arising from a point's coupling to "
        "the ambient field gradient, not an intrinsic scalar property."
    ),
    "gravity": (
        "Candidate: gravity as an emergent restoring response of nested "
        "wave fields toward mutual phase balance -- a One-Wave 'wake' "
        "effect rather than a fundamental force."
    ),
    "energy": (
        "Candidate: energy as retained momentum (M_t) in the ternary "
        "transition record -- the memory term persisting across gate "
        "transitions."
    ),
    "field": (
        "Candidate: field as the local gradient F_t derived from "
        "Phi(M_t, Delta_t) -- the active interpretive/dynamical context "
        "of a runtime point."
    ),
    "wave": (
        "Candidate: wave as the observable trace of a runtime point's "
        "oscillation between ADVANCE and RETURN gate states along its path."
    ),
    "frequency": (
        "Candidate: frequency as the rate of ADVANCE/RETURN gate "
        "alternation along a runtime's path."
    ),
}

ONE_WAVE_SPECIFIC = {
    "mirror_gate": (
        "Mirror Gate",
        "Candidate: the gating mechanism Gamma(F, A, B) that admits or "
        "cancels a proposed transition based on the active field gradient.",
    ),
    "point": (
        "Point",
        "Candidate: a runtime record's current (F_t, Delta_t, M_t) state "
        "-- the addressable 'where' of the system at time t.",
    ),
    "path": (
        "Path",
        "Candidate: the ordered, append-only sequence of transition events "
        "(h_t) that produced a runtime's current point.",
    ),
    "field_rotation": (
        "Field Rotation",
        "Candidate: a coordinated change in the active field gradient "
        "shared across a group of relationally-linked runtime points.",
    ),
    "wake": (
        "wake",
        "Candidate: the persistent relational disturbance a moving point "
        "leaves in neighboring points' field gradients.",
    ),
    "scale_locality": (
        "scale locality",
        "Candidate: the principle that a runtime point's transition "
        "dynamics depend only on its local state and declared causal "
        "parents, never on unrelated distant state.",
    ),
}


def seed(db: Storage) -> None:
    ingest.add_field(db, "science", "Science")
    ingest.add_field(db, "science.physics", "Physics", parent_field_id="science")
    ingest.add_field(
        db, "science.physics.standard", "Standard Physics",
        parent_field_id="science.physics",
    )
    ingest.add_field(
        db, "science.physics.one_wave", "One-Wave Research",
        parent_field_id="science.physics",
    )

    for name, text in STANDARD_DEFINITIONS.items():
        ingest.ingest_entry(db, name, text, "science.physics.standard", EpistemicStatus.DEFINITION)

    for name, text in ONE_WAVE_DEFINITIONS.items():
        ingest.ingest_entry(db, name, text, "science.physics.one_wave", EpistemicStatus.CANDIDATE)

    for concept_id, (canonical_name, text) in ONE_WAVE_SPECIFIC.items():
        ingest.ingest_entry(
            db, canonical_name, text, "science.physics.one_wave", EpistemicStatus.CANDIDATE,
            concept_id=concept_id,
        )

    ingest.add_relation(db, "mass", "mirror_gate", "science.physics.one_wave",
                         "emerges_from", EpistemicStatus.CANDIDATE)
    ingest.add_relation(db, "gravity", "wake", "science.physics.one_wave",
                         "emerges_from", EpistemicStatus.CANDIDATE)
    ingest.add_relation(db, "wake", "point", "science.physics.one_wave",
                         "emerges_from", EpistemicStatus.CANDIDATE)
    ingest.add_relation(db, "point", "path", "science.physics.one_wave",
                         "emerges_from", EpistemicStatus.CANDIDATE)
    ingest.add_relation(db, "mirror_gate", "field", "science.physics.one_wave",
                         "requires", EpistemicStatus.CANDIDATE)


if __name__ == "__main__":
    from onewave.query import query_concept, render_answer

    db = Storage(":memory:")
    seed(db)
    print(render_answer(query_concept(db, "gravity")))
