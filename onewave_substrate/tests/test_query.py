import pytest

from onewave import ingest
from onewave.epistemic import EpistemicStatus
from onewave.query import query_concept, render_answer


def _seed_gravity(db):
    ingest.add_field(db, "science.physics.standard", "Standard Physics")
    ingest.add_field(db, "science.physics.one_wave", "One-Wave Research")
    ingest.ingest_entry(
        db, "gravity",
        "The attractive force/curvature effect between masses.",
        "science.physics.standard", EpistemicStatus.DEFINITION,
    )
    ingest.ingest_entry(
        db, "gravity",
        "Candidate: gravity as an emergent Mirror Gate wake effect.",
        "science.physics.one_wave", EpistemicStatus.CANDIDATE,
    )


def test_query_with_active_field_returns_only_that_field(db):
    _seed_gravity(db)
    result = query_concept(db, "gravity", active_field="science.physics.standard")
    assert len(result.answers) == 1
    assert result.answers[0].field_id == "science.physics.standard"
    assert result.answers[0].definitions[0].epistemic_status == EpistemicStatus.DEFINITION


def test_query_without_active_field_returns_grouped_fields(db):
    _seed_gravity(db)
    result = query_concept(db, "gravity")
    field_ids = {a.field_id for a in result.answers}
    assert field_ids == {"science.physics.standard", "science.physics.one_wave"}


def test_query_unknown_concept_raises(db):
    with pytest.raises(ValueError):
        query_concept(db, "does-not-exist")


def test_query_resolves_by_alias(db):
    ingest.add_field(db, "emotion", "Emotion")
    ingest.ingest_entry(
        db, "anger", "An emotional state of frustration.", "emotion",
        EpistemicStatus.DEFINITION, aliases=("angry", "rage"),
    )
    result = query_concept(db, "rage")
    assert result.concept.canonical_name == "anger"


def test_epistemic_filter_excludes_other_statuses(db):
    _seed_gravity(db)
    result = query_concept(db, "gravity", epistemic_filter=EpistemicStatus.CANDIDATE)
    field_ids = {a.field_id for a in result.answers if a.definitions}
    assert field_ids == {"science.physics.one_wave"}


def test_include_history_exposes_prior_revisions(db):
    ingest.add_field(db, "emotion", "Emotion")
    concept, first, _ = ingest.ingest_entry(
        db, "anger", "v1 definition.", "emotion", EpistemicStatus.CANDIDATE,
    )
    ingest.add_definition(
        db, "anger", "emotion", "v2 definition, refined.",
        EpistemicStatus.DEFINITION, supersedes=first.revision_id,
    )
    result = query_concept(db, "anger", include_history=True)
    revisions = next(iter(result.history.values()))
    assert [r.text for r in revisions] == ["v1 definition.", "v2 definition, refined."]


def test_render_answer_never_merges_field_text():
    _fields_note = "render_answer must show each field as its own block"
    from onewave.storage.sqlite import Storage
    db = Storage(":memory:")
    _seed_gravity(db)
    result = query_concept(db, "gravity")
    text = render_answer(result)
    assert "Standard Physics" in text
    assert "One-Wave Research" in text
    # Both status labels present and distinguishable, not collapsed.
    assert "definition" in text
    assert "candidate" in text


def test_render_answer_handles_no_data_for_field():
    from onewave.storage.sqlite import Storage
    db = Storage(":memory:")
    ingest.add_field(db, "electronics", "Electronics")
    ingest.add_field(db, "emotion", "Emotion")
    ingest.ingest_entry(db, "anger", "text", "emotion", EpistemicStatus.DEFINITION)
    result = query_concept(db, "anger", active_field="electronics")
    text = render_answer(result)
    assert "No stored interpretations" in text
