"""Build the One-Wave "reality" database: the repository's own canonical
Nodes/ + Root_Axioms/ corpus, ingested through the One-Wave lens.

Unlike examples/build_database.py (a small, hand-authored demo dataset
mixing several fields to prove field separation works), this builder
ingests the *actual* body of concept definitions this repository already
maintains -- ~150 Root Axiom / Node files, each a real claim about
"reality" as modeled by the One-Wave framework -- and writes them into a
single field tree rooted at `one_wave`, sub-divided by the corpus's own
A-G series:

    one_wave
    ├── one_wave.root_axioms     (the 3 Root Axioms: A+101, A+102, A+103)
    ├── one_wave.a_foundations   (A-series: ground, displacement, ...)
    ├── one_wave.b_balance       (B-series: balance, threshold, choice, ...)
    ├── one_wave.c_mechanics     (C-series: Mirror Gate, momentum, mass, ...)
    ├── one_wave.d_resonance     (D-series: resonance, lattice, ...)
    ├── one_wave.e_extended      (E-series: cross-domain applications)
    ├── one_wave.f_interaction   (F-series: influence, transfer, ...)
    └── one_wave.g_evaluation    (G-series: evaluation, gates, decision, ...)

Every concept is stored with epistemic_status = CANDIDATE: this is the
One-Wave framework's own working model of reality, not an externally
validated claim, and the substrate's core rule ("no interpretation
outside an active field") applies here too -- these claims live in the
`one_wave.*` fields and are never presented as `science.physics.standard`
fact. Each node's own internal review state (its `gate` color: GREEN /
YELLOW / BRONZE / SILVER / GOLD) is preserved as a numeric `confidence`
and recorded verbatim in `source`, rather than folded into
EpistemicStatus, which stays reserved for the field-vs-field distinction.

DEPENDENCIES/UPSTREAM references between nodes (e.g. "A-102 Displacement
UPSTREAM: A-101 Ground/Zero") become EMERGES_FROM relations: `A-102
EMERGES_FROM A-101`. A referenced node id that isn't itself part of the
corpus (an external cross-reference, e.g. into Books/) gets a bare stub
concept so the relation still has somewhere to point.

Usage:
    python3 -m examples.build_reality_database [output_path] [--repo-root PATH]
    # defaults to onewave_reality.db, auto-detecting the repo root as the
    # parent of onewave_substrate/ (Nodes/ and Root_Axioms/ live there)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from examples.reality_corpus import ParsedNode, confidence_for_gate, field_for_node, load_corpus
from onewave import fields as fields_mod
from onewave.concepts import add_concept, add_definition, get_concept
from onewave.epistemic import EpistemicStatus
from onewave.relations import RelationType, add_relation
from onewave.storage.sqlite import Storage

FIELD_TREE = [
    ("one_wave", "One-Wave", None,
     "The One-Wave framework's own model of reality, as maintained in this "
     "repository's Nodes/ and Root_Axioms/ corpus. Root organizational field "
     "-- concepts are always ingested into one of its named children below, "
     "never into this bare root, so a query always names a specific series."),
    ("one_wave.root_axioms", "Root Axioms", "one_wave", "The 3 foundational Root Axioms."),
    ("one_wave.a_foundations", "A-Series: Foundations", "one_wave",
     "Ground, displacement, differential, gradient, restoring response, and other core measurement primitives."),
    ("one_wave.b_balance", "B-Series: Balance, Threshold & Choice", "one_wave",
     "Balance, mirror, threshold, loop, and choice-cycle structures."),
    ("one_wave.c_mechanics", "C-Series: Mechanics & Physics Candidates", "one_wave",
     "Mirror Gate, momentum, energy, mass-mechanism candidates, and other One-Wave physics models."),
    ("one_wave.d_resonance", "D-Series: Resonance & Lattice", "one_wave",
     "Resonant modes, spherical/lattice structure, and nested resonance."),
    ("one_wave.e_extended", "E-Series: Extended & Cross-Domain Physics", "one_wave",
     "Cross-domain applications: music, biology, cosmology, and other extended physics candidates."),
    ("one_wave.f_interaction", "F-Series: Interaction & Transfer", "one_wave",
     "Influence, transfer, resonance, interference, and related interaction primitives."),
    ("one_wave.g_evaluation", "G-Series: Evaluation, Gates & Decision", "one_wave",
     "Evaluation, modulation, correction, validation, and decision/gate grammar."),
    ("one_wave.other", "Other", "one_wave", "Nodes that don't fit the standard A-G series."),
]


def _detect_repo_root() -> Path:
    # examples/build_reality_database.py -> examples -> onewave_substrate -> repo root
    return Path(__file__).resolve().parents[2]


def seed_fields(db: Storage) -> None:
    for field_id, name, parent_id, description in FIELD_TREE:
        fields_mod.add_field(db, field_id, name, parent_field_id=parent_id, description=description)


def ingest_corpus(db: Storage, nodes: list[ParsedNode]) -> None:
    # Pass 1: every node becomes a concept (keyed by its own node_id --
    # this also resolves the exact B-201/G-709 "Balance" name collision
    # the corpus itself calls out, since concept identity is node_id, not
    # display name) plus one field-scoped definition.
    for node in nodes:
        field_id, _ = field_for_node(node)
        add_concept(db, node.node_id, node.canonical_name.title())
        add_definition(
            db,
            concept_id=node.node_id,
            field_id=field_id,
            text=node.definition,
            epistemic_status=EpistemicStatus.CANDIDATE,
            source=(
                f"{node.namespace} {node.node_id}; gate={node.gate}; "
                f"lifecycle={node.lifecycle}; classification={node.classification}; "
                f"file={Path(node.source_file).name}"
            ),
            confidence=confidence_for_gate(node.gate),
        )

    # Pass 2: UPSTREAM references become EMERGES_FROM relations. Targets
    # outside the corpus (or nodes we failed to parse) get a bare stub
    # concept so the foreign key on relations.target_concept_id holds.
    for node in nodes:
        field_id, _ = field_for_node(node)
        for upstream_id in node.upstream_ids:
            if upstream_id == node.node_id:
                continue
            if get_concept(db, upstream_id) is None:
                add_concept(db, upstream_id, upstream_id)
            add_relation(
                db,
                source_concept_id=node.node_id,
                target_concept_id=upstream_id,
                field_id=field_id,
                relation_type=RelationType.EMERGES_FROM,
                epistemic_status=EpistemicStatus.CANDIDATE,
                source=f"parsed from {node.node_id} DEPENDENCIES/UPSTREAM",
            )


def build(db_path: str, repo_root: Path) -> Storage:
    nodes_dir = repo_root / "Nodes"
    root_axioms_dir = repo_root / "Root_Axioms"
    if not nodes_dir.is_dir() or not root_axioms_dir.is_dir():
        raise SystemExit(
            f"Could not find Nodes/ and Root_Axioms/ under {repo_root}. "
            f"This builder reads the One-Wave-Science repository's own corpus, "
            f"so it must run from inside a checkout of the full repo (or pass "
            f"--repo-root explicitly)."
        )

    path = Path(db_path)
    if path.exists():
        path.unlink()

    db = Storage(str(path))
    seed_fields(db)
    nodes = load_corpus(nodes_dir, root_axioms_dir)
    ingest_corpus(db, nodes)
    return db


def summarize(db: Storage) -> str:
    lines = ["Row counts:"]
    for table in ("concepts", "fields", "definitions", "relations"):
        n = db.query_one(f"SELECT COUNT(*) AS n FROM {table}")["n"]
        lines.append(f"  {table:<12} {n}")
    lines.append("")
    lines.append("Concepts per field:")
    for row in db.query_all(
        "SELECT field_id, COUNT(*) AS n FROM definitions GROUP BY field_id ORDER BY field_id"
    ):
        lines.append(f"  {row['field_id']:<24} {row['n']}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", nargs="?", default="onewave_reality.db")
    parser.add_argument("--repo-root", default=None, help="Path to the One-Wave-Science repo checkout")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve() if args.repo_root else _detect_repo_root()
    db = build(args.output, repo_root)
    print(f"Built {args.output} from {repo_root}")
    print(summarize(db))
    db.close()


if __name__ == "__main__":
    main()
