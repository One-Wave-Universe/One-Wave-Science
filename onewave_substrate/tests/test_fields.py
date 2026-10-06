import pytest

from onewave import fields


def test_add_and_get_field(db):
    f = fields.add_field(db, "science.physics.standard", "Standard Physics")
    fetched = fields.get_field(db, "science.physics.standard")
    assert fetched == f
    assert fetched.name == "Standard Physics"


def test_nested_fields_and_ancestry(db):
    fields.add_field(db, "science", "Science")
    fields.add_field(db, "science.physics", "Physics", parent_field_id="science")
    fields.add_field(db, "science.physics.standard", "Standard Physics", parent_field_id="science.physics")

    ancestry = fields.field_ancestry(db, "science.physics.standard")
    assert [f.field_id for f in ancestry] == [
        "science.physics.standard",
        "science.physics",
        "science",
    ]


def test_child_fields_lookup(db):
    fields.add_field(db, "science.physics", "Physics")
    fields.add_field(db, "science.physics.standard", "Standard Physics", parent_field_id="science.physics")
    fields.add_field(db, "science.physics.one_wave", "One-Wave Physics", parent_field_id="science.physics")

    children = {f.field_id for f in fields.child_fields(db, "science.physics")}
    assert children == {"science.physics.standard", "science.physics.one_wave"}


def test_unknown_parent_field_rejected(db):
    with pytest.raises(ValueError):
        fields.add_field(db, "orphan", "Orphan", parent_field_id="does.not.exist")


def test_child_field_does_not_inherit_parent_gate_rules_by_default(db):
    fields.add_field(db, "science.physics", "Physics", gate_rules={"inherit": ["science"]})
    child = fields.add_field(
        db, "science.physics.standard", "Standard Physics", parent_field_id="science.physics"
    )
    # No implicit inheritance: the child's own gate_rules are empty unless
    # explicitly given, regardless of what the parent declares.
    assert child.allowed_parent_field_ids() == []


def test_field_can_explicitly_opt_into_parent_inheritance(db):
    child = fields.add_field(
        db,
        "science.physics.standard",
        "Standard Physics",
        gate_rules={"inherit": ["science.physics"]},
    )
    assert child.allowed_parent_field_ids() == ["science.physics"]
