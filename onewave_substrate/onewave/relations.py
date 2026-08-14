"""Typed, field-scoped relations between concepts.

Relations carry the same epistemic-status discipline as definitions: a
relation observed in standard physics and a relation hypothesized in
One-Wave research are different rows in different fields, never merged.
Generic association (ASSOCIATED_WITH) is deliberately kept separate from
causal types (CAUSES) -- nothing here infers causal meaning from
correlation/association, and nothing auto-promotes an inferred relation's
epistemic status (see EpistemicStatus.INFERRED / section 25 of the brief).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum

from onewave.epistemic import EpistemicStatus
from onewave.storage.sqlite import Storage


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


class RelationType(str, Enum):
    IS_A = "is_a"
    PART_OF = "part_of"
    CAUSES = "causes"
    CORRELATES_WITH = "correlates_with"
    OPPOSES = "opposes"
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    TRANSITIONS_TO = "transitions_to"
    DEFINED_BY = "defined_by"
    ASSOCIATED_WITH = "associated_with"
    REQUIRES = "requires"
    EMERGES_FROM = "emerges_from"
    MAY_FOLLOW = "may_follow"
    MAY_LEAD_TO = "may_lead_to"


@dataclass(frozen=True)
class Relation:
    relation_id: str
    source_concept_id: str
    target_concept_id: str
    field_id: str
    relation_type: RelationType
    epistemic_status: EpistemicStatus
    weight: float | None
    source: str | None
    created_at: str


def _row_to_relation(row) -> Relation:
    return Relation(
        relation_id=row["relation_id"],
        source_concept_id=row["source_concept_id"],
        target_concept_id=row["target_concept_id"],
        field_id=row["field_id"],
        relation_type=RelationType(row["relation_type"]),
        epistemic_status=EpistemicStatus(row["epistemic_status"]),
        weight=row["weight"],
        source=row["source"],
        created_at=row["created_at"],
    )


def add_relation(
    db: Storage,
    source_concept_id: str,
    target_concept_id: str,
    field_id: str,
    relation_type: RelationType | str,
    epistemic_status: EpistemicStatus | str = EpistemicStatus.CANDIDATE,
    weight: float | None = None,
    source: str | None = None,
) -> Relation:
    if isinstance(relation_type, str):
        relation_type = RelationType(relation_type)
    if isinstance(epistemic_status, str):
        epistemic_status = EpistemicStatus(epistemic_status)

    relation_id = _new_id("rel")
    created_at = _now()
    db.execute(
        """
        INSERT INTO relations (
            relation_id, source_concept_id, target_concept_id, field_id,
            relation_type, epistemic_status, weight, source, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            relation_id, source_concept_id, target_concept_id, field_id,
            relation_type.value, epistemic_status.value, weight, source, created_at,
        ),
    )
    return Relation(
        relation_id=relation_id,
        source_concept_id=source_concept_id,
        target_concept_id=target_concept_id,
        field_id=field_id,
        relation_type=relation_type,
        epistemic_status=epistemic_status,
        weight=weight,
        source=source,
        created_at=created_at,
    )


def get_relations(
    db: Storage,
    concept_id: str,
    field_id: str | None = None,
    direction: str = "both",
) -> list[Relation]:
    """Relations touching `concept_id`, optionally scoped to one field.

    direction: "outgoing" (concept as source), "incoming" (concept as
    target), or "both" (default).
    """
    clauses = []
    params: list = []
    if direction in ("outgoing", "both"):
        clauses.append("source_concept_id = ?")
        params.append(concept_id)
    if direction in ("incoming", "both"):
        clauses.append("target_concept_id = ?")
        params.append(concept_id)
    where = " OR ".join(clauses)
    sql = f"SELECT * FROM relations WHERE ({where})"
    if field_id is not None:
        sql += " AND field_id = ?"
        params.append(field_id)
    sql += " ORDER BY field_id, relation_type"
    rows = db.query_all(sql, params)
    return [_row_to_relation(r) for r in rows]


def get_relations_between(
    db: Storage,
    source_concept_id: str,
    target_concept_id: str,
    field_id: str | None = None,
) -> list[Relation]:
    sql = (
        "SELECT * FROM relations WHERE source_concept_id = ? AND target_concept_id = ?"
    )
    params: list = [source_concept_id, target_concept_id]
    if field_id is not None:
        sql += " AND field_id = ?"
        params.append(field_id)
    rows = db.query_all(sql, params)
    return [_row_to_relation(r) for r in rows]
