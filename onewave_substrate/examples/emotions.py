"""Demo dataset: the `emotion` field (and one `behavior`-field definition
of `anger`, used by the "What is anger in the behavior field?" demo query
in mixed_fields.py).

Concepts: anger, fear, calm, joy, grief, frustration.
"""

from __future__ import annotations

from onewave import ingest
from onewave.epistemic import EpistemicStatus
from onewave.storage.sqlite import Storage


def seed(db: Storage) -> None:
    ingest.add_field(db, "emotion", "Emotion")
    ingest.add_field(db, "behavior", "Behavior")

    ingest.ingest_entry(
        db, "anger",
        "An emotional state associated with frustration, perceived injustice, "
        "blocked goals, or threat.",
        "emotion", EpistemicStatus.DEFINITION,
        aliases=("angry", "rage"),
        relations=[
            ("associated_with", "frustration"),
            ("may_follow", "fear"),
            ("may_lead_to", "frustration"),
            ("opposes", "calm"),
        ],
    )
    ingest.ingest_entry(
        db, "anger",
        "A pattern of increased vocal volume, tense posture, clenched fists, "
        "and approach-oriented (rather than avoidance) action tendencies.",
        "behavior", EpistemicStatus.OBSERVED,
    )

    ingest.ingest_entry(
        db, "fear",
        "An emotional state triggered by the perception of threat or danger, "
        "typically producing avoidance or freeze responses.",
        "emotion", EpistemicStatus.DEFINITION,
        relations=[
            ("may_lead_to", "anger"),
            ("opposes", "calm"),
        ],
    )

    ingest.ingest_entry(
        db, "calm",
        "A low-arousal emotional state characterized by the absence of "
        "threat perception and reduced physiological activation.",
        "emotion", EpistemicStatus.DEFINITION,
    )

    ingest.ingest_entry(
        db, "joy",
        "A positive emotional state associated with the attainment of a "
        "goal or a rewarding, safe experience.",
        "emotion", EpistemicStatus.DEFINITION,
        relations=[("opposes", "grief")],
    )

    ingest.ingest_entry(
        db, "grief",
        "An emotional state responding to loss, associated with sadness, "
        "yearning, and withdrawal.",
        "emotion", EpistemicStatus.DEFINITION,
        relations=[("may_lead_to", "anger")],
    )

    ingest.ingest_entry(
        db, "frustration",
        "An emotional state arising when progress toward a goal is blocked.",
        "emotion", EpistemicStatus.DEFINITION,
        relations=[("may_lead_to", "anger")],
    )


if __name__ == "__main__":
    from onewave.query import query_concept, render_answer

    db = Storage(":memory:")
    seed(db)
    print(render_answer(query_concept(db, "anger")))
