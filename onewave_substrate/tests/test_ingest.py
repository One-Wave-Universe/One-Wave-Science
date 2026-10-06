from onewave import ingest
from onewave.concepts import get_concept
from onewave.epistemic import EpistemicStatus


def test_ingest_entry_creates_concept_definition_and_relations(db):
    ingest.add_field(db, "emotion", "Emotion")
    concept, definition, relations = ingest.ingest_entry(
        db, "anger", "An emotional state.", "emotion", EpistemicStatus.DEFINITION,
        relations=[("associated_with", "frustration"), ("opposes", "calm")],
    )
    assert concept.canonical_name == "anger"
    assert definition.field_id == "emotion"
    assert len(relations) == 2


def test_ingest_entry_reuses_existing_concept_across_fields(db):
    ingest.add_field(db, "science.physics.standard", "Standard Physics")
    ingest.add_field(db, "science.physics.one_wave", "One-Wave Research")

    concept_a, _, _ = ingest.ingest_entry(
        db, "mass", "Standard def.", "science.physics.standard", EpistemicStatus.DEFINITION,
    )
    concept_b, _, _ = ingest.ingest_entry(
        db, "mass", "One-Wave candidate def.", "science.physics.one_wave", EpistemicStatus.CANDIDATE,
    )
    assert concept_a.concept_id == concept_b.concept_id


def test_ingest_entry_rejects_unknown_field(db):
    import pytest
    with pytest.raises(ValueError):
        ingest.ingest_entry(db, "anger", "text", "no-such-field", EpistemicStatus.DEFINITION)


def test_relation_target_referenced_by_concept_id_does_not_clobber_canonical_name(db):
    # Regression test: a relation target passed by its concept_id (rather
    # than its canonical display name) must resolve to the existing
    # concept, not silently overwrite its canonical_name via a duplicate
    # slug-based create.
    ingest.add_field(db, "mythology.one_wave", "One-Wave Mythology")
    ingest.ingest_entry(
        db, "Big Rip", "Mythic unraveling.", "mythology.one_wave", EpistemicStatus.MYTHOLOGY,
        concept_id="big_rip",
    )
    ingest.ingest_entry(
        db, "Void", "Mythic ground state.", "mythology.one_wave", EpistemicStatus.MYTHOLOGY,
        concept_id="the_void",
        relations=[("associated_with", "big_rip", "mythology")],
    )

    big_rip = get_concept(db, "big_rip")
    assert big_rip.canonical_name == "Big Rip"
