from onewave import concepts, fields
from onewave.epistemic import EpistemicStatus
from onewave.query import query_concept
from onewave.relations import RelationType, add_relation, get_relations, get_relations_between


def _seed_mass(db):
    fields.add_field(db, "science.physics.standard", "Standard Physics")
    fields.add_field(db, "science.physics.one_wave", "One-Wave Research")
    fields.add_field(db, "mythology.one_wave", "One-Wave Mythology")

    concepts.add_concept(db, "mass", "mass")
    concepts.add_concept(db, "mirror_gate", "Mirror Gate")
    concepts.add_concept(db, "the_void", "Void")

    concepts.add_definition(
        db, "mass", "science.physics.standard",
        "A measure of an object's resistance to acceleration under an applied force.",
        EpistemicStatus.DEFINITION,
    )
    concepts.add_definition(
        db, "mass", "science.physics.one_wave",
        "Candidate: mass as a local Mirror Gate coupling effect.",
        EpistemicStatus.CANDIDATE,
    )
    concepts.add_definition(
        db, "mass", "mythology.one_wave",
        "Symbolic weight the Void grants to a thing that resists return.",
        EpistemicStatus.MYTHOLOGY,
    )

    add_relation(
        db, "mass", "mirror_gate", "science.physics.one_wave",
        RelationType.EMERGES_FROM, EpistemicStatus.CANDIDATE,
    )
    add_relation(
        db, "mass", "the_void", "mythology.one_wave",
        RelationType.ASSOCIATED_WITH, EpistemicStatus.MYTHOLOGY,
    )


def test_relations_scoped_to_declared_field(db):
    _seed_mass(db)
    standard_relations = get_relations(db, "mass", field_id="science.physics.standard")
    assert standard_relations == []

    one_wave_relations = get_relations(db, "mass", field_id="science.physics.one_wave")
    assert len(one_wave_relations) == 1
    assert one_wave_relations[0].relation_type == RelationType.EMERGES_FROM


def test_no_leakage_of_unsupported_claims_between_fields(db):
    _seed_mass(db)

    standard = query_concept(db, "mass", active_field="science.physics.standard")
    assert len(standard.answers) == 1
    defs = standard.answers[0].definitions
    assert len(defs) == 1
    assert defs[0].epistemic_status == EpistemicStatus.DEFINITION
    assert "Mirror Gate" not in defs[0].text
    assert standard.answers[0].relations == ()  # no One-Wave/mythology relations here

    one_wave = query_concept(db, "mass", active_field="science.physics.one_wave")
    assert one_wave.answers[0].definitions[0].epistemic_status == EpistemicStatus.CANDIDATE

    myth = query_concept(db, "mass", active_field="mythology.one_wave")
    assert myth.answers[0].definitions[0].epistemic_status == EpistemicStatus.MYTHOLOGY


def test_query_without_active_field_groups_but_never_merges(db):
    _seed_mass(db)
    result = query_concept(db, "mass")
    field_ids = {a.field_id for a in result.answers}
    assert field_ids == {"science.physics.standard", "science.physics.one_wave", "mythology.one_wave"}

    statuses_by_field = {a.field_id: {d.epistemic_status for d in a.definitions} for a in result.answers}
    assert statuses_by_field["science.physics.standard"] == {EpistemicStatus.DEFINITION}
    assert statuses_by_field["science.physics.one_wave"] == {EpistemicStatus.CANDIDATE}
    assert statuses_by_field["mythology.one_wave"] == {EpistemicStatus.MYTHOLOGY}


def test_get_relations_between_two_concepts(db):
    _seed_mass(db)
    rels = get_relations_between(db, "mass", "mirror_gate")
    assert len(rels) == 1
    assert rels[0].field_id == "science.physics.one_wave"
