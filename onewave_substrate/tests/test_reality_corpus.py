"""Tests for examples/reality_corpus.py, the Nodes/Root_Axioms markdown
parser used by examples/build_reality_database.py.

Uses synthetic markdown fixtures rather than reading the real repo's
Nodes/ directory, so these tests stay hermetic and pass even when this
package is extracted standalone (its own tests/ tree is self-contained;
the real corpus lives one level up in the parent repo checkout).
"""

from examples.reality_corpus import (
    ParsedNode,
    confidence_for_gate,
    extract_definition,
    extract_upstream_ids,
    field_for_node,
    parse_node_file,
)


def test_numbered_style_definition():
    body = """
# Node A-101: Ground / Zero

1. PURPOSE
Defines the reference condition.

2. DEFINITION
Ground / Zero is the reference state required for measurement.

3. STATE VARIABLES
psi = current field state.
"""
    text, tier = extract_definition(body)
    assert tier == "numbered"
    assert text == "Ground / Zero is the reference state required for measurement."


def test_markdown_heading_definition():
    body = """
# Node G-703: Modulation

Dependencies:
Upstream: G-702 Evaluation

## Definition

Modulation converts an evaluation signal into a bounded change of
activation.

Root Rule: Field Modulates.
"""
    text, tier = extract_definition(body)
    assert tier == "markdown_definition"
    assert text.startswith("Modulation converts an evaluation signal")


def test_plain_definition_label():
    body = """
# Node B-201: Equilibrium Balance

Definition:
Balance defines the scalar measure of equilibrium between driving and
opposing contributions.

Primitives:
E = external field contribution
"""
    text, tier = extract_definition(body)
    assert tier == "plain"
    assert "scalar measure of equilibrium" in text


def test_markdown_purpose_heading_fallback_when_no_definition_heading():
    body = """
# Node D-413: Ground Lattice Orbital-Restoring Simulation

**Dependencies**
Upstream: A-101 Ground Zero, A-102 Displacement

## Purpose

D-413 is the first runnable Ground-lattice background for later physical
simulations.
"""
    text, tier = extract_definition(body)
    assert tier == "markdown_purpose"
    assert text.startswith("D-413 is the first runnable")


def test_fallback_skips_structural_blocks_and_finds_prose():
    body = """
# Node X-999: Something

**Dependencies**
Upstream: A-101, A-102

Class:
Core grammar

Actual prose about what this node means goes here.
"""
    text, tier = extract_definition(body)
    assert tier == "fallback"
    assert "Actual prose" in text
    assert "Dependencies" not in text
    assert "Core grammar" not in text


def test_fallback_merges_colon_terminated_lead_in_with_next_block():
    body = """
# Node X-998: Fragment Case

This node formalizes one narrow claim:

The rupture relocates without creating a permanent tear.
"""
    text, tier = extract_definition(body)
    assert tier == "fallback"
    assert "formalizes one narrow claim" in text
    assert "rupture relocates" in text


def test_extract_upstream_ids_ignores_non_node_tokens():
    body = "Upstream: External Field (E), Internal Field (I), Resistance (R)\nDownstream: B-202"
    assert extract_upstream_ids(body) == ()


def test_extract_upstream_ids_finds_node_ids_and_dedupes():
    body = "UPSTREAM: A-101 Ground Zero, A-102 Displacement, A-102 again\nDOWNSTREAM: B-201"
    assert extract_upstream_ids(body) == ("A-101", "A-102")


def test_extract_upstream_ids_stops_before_lateral_and_downstream():
    body = (
        "Upstream: A-101 Ground Zero, A-102 Displacement\n"
        "Lateral: B-202 Pressure\n"
        "Downstream: C-301 Mirror Gate"
    )
    assert extract_upstream_ids(body) == ("A-101", "A-102")


def test_field_for_node_root_axiom():
    node = ParsedNode(
        node_id="A+101", canonical_name="One Field Ground", namespace="ROOT_AXIOM",
        gate="GREEN", lifecycle="ACTIVE", classification="Foundation Root",
        definition="text", upstream_ids=(), source_file="A+101.md",
    )
    assert field_for_node(node) == ("one_wave.root_axioms", "Root Axioms")


def test_field_for_node_series_mapping():
    for prefix, expected_field in [
        ("A-101", "one_wave.a_foundations"),
        ("B-201", "one_wave.b_balance"),
        ("C-301", "one_wave.c_mechanics"),
        ("D-401", "one_wave.d_resonance"),
        ("E-501", "one_wave.e_extended"),
        ("F-601", "one_wave.f_interaction"),
        ("G-701", "one_wave.g_evaluation"),
    ]:
        node = ParsedNode(
            node_id=prefix, canonical_name="X", namespace="NODE",
            gate="GREEN", lifecycle="ACTIVE", classification="",
            definition="text", upstream_ids=(), source_file="x.md",
        )
        assert field_for_node(node)[0] == expected_field


def test_confidence_for_gate_ordinal_scale():
    assert confidence_for_gate("GREEN") < confidence_for_gate("YELLOW")
    assert confidence_for_gate("YELLOW") < confidence_for_gate("BRONZE")
    assert confidence_for_gate("BRONZE") < confidence_for_gate("SILVER")
    assert confidence_for_gate("SILVER") < confidence_for_gate("GOLD")
    assert confidence_for_gate("UNKNOWN_COLOR") is None


def test_parse_node_file_reads_frontmatter_and_body(tmp_path):
    content = """---
node_id: "A-101"
canonical_name: "GROUND / ZERO"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Foundation Primitive"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node A-101: GROUND / ZERO

DEPENDENCIES:
UPSTREAM: A+101 One Field Ground.

1. PURPOSE
Defines the reference condition.

2. DEFINITION
Ground / Zero is the reference state required for measurement.

3. STATE VARIABLES
psi = current field state.
"""
    path = tmp_path / "A-101_Ground_Zero.md"
    path.write_text(content, encoding="utf-8")

    node = parse_node_file(path)
    assert node.node_id == "A-101"
    assert node.canonical_name == "GROUND / ZERO"
    assert node.gate == "YELLOW"
    assert node.definition == "Ground / Zero is the reference state required for measurement."
    assert node.upstream_ids == ("A+101",)


def test_parse_node_file_without_frontmatter_returns_none(tmp_path):
    path = tmp_path / "not_a_node.md"
    path.write_text("# Just a regular markdown file\n\nNo frontmatter here.", encoding="utf-8")
    assert parse_node_file(path) is None
