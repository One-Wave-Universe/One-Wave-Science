"""Ingestion pipeline.

Low-level primitives (add_concept, add_definition, add_relation, add_field)
are thin re-exports of the domain-module functions -- ingestion doesn't
get its own copy of that logic. `ingest_entry` is the higher-level
convenience wrapper described in brief section 18: one call that resolves
or creates a concept, appends a field-scoped definition, and attaches any
relations, auto-creating stub target concepts as needed so relations can
be declared before their targets have full definitions of their own.
"""

from __future__ import annotations

import re

from onewave.concepts import (
    Concept,
    DefinitionRecord,
    add_concept,
    add_definition,
    find_concept,
    get_concept,
)
from onewave.epistemic import EpistemicStatus
from onewave.fields import Field, add_field, get_field
from onewave.relations import Relation, RelationType, add_relation
from onewave.storage.sqlite import Storage

__all__ = [
    "add_concept",
    "add_definition",
    "add_relation",
    "add_field",
    "ingest_entry",
]


def _slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", name.strip().lower()).strip("_")
    return slug or "concept"


def _resolve_or_create_concept(db: Storage, name: str, concept_id: str | None) -> Concept:
    if concept_id is not None:
        existing = get_concept(db, concept_id)
        if existing is not None:
            return existing
        return add_concept(db, concept_id, name)

    # `name` may be a canonical name/alias (the common case) or, for
    # relation targets in particular, an existing concept_id -- try an
    # exact id match first. Falling straight to find_concept()/creation
    # would, for an id-shaped string that collides with another
    # concept's slug, silently over-write that concept's canonical_name
    # via add_concept's upsert instead of resolving to it.
    existing = get_concept(db, name)
    if existing is not None:
        return existing
    existing = find_concept(db, name)
    if existing is not None:
        return existing
    return add_concept(db, _slugify(name), name)


def ingest_entry(
    db: Storage,
    name: str,
    definition: str,
    field: str,
    epistemic_status: EpistemicStatus | str,
    relations: list[tuple[str, str] | tuple[str, str, str]] | None = None,
    concept_id: str | None = None,
    aliases: tuple[str, ...] | list[str] = (),
    source: str | None = None,
    confidence: float | None = None,
) -> tuple[Concept, DefinitionRecord, list[Relation]]:
    """Ingest one concept's field-scoped definition plus its relations.

    `relations` entries are (relation_type, target_name_or_id) or
    (relation_type, target_name_or_id, epistemic_status); target concepts
    that don't exist yet are created as bare stubs (no definition), never
    silently promoted to a validated epistemic status themselves.
    """
    if get_field(db, field) is None:
        raise ValueError(
            f"unknown field_id: {field!r} -- call add_field() before ingest_entry()"
        )

    concept = _resolve_or_create_concept(db, name, concept_id)
    if aliases:
        add_concept(db, concept.concept_id, concept.canonical_name, aliases=aliases)
        concept = get_concept(db, concept.concept_id)  # type: ignore[assignment]

    definition_record = add_definition(
        db,
        concept_id=concept.concept_id,
        field_id=field,
        text=definition,
        epistemic_status=epistemic_status,
        source=source,
        confidence=confidence,
    )

    created_relations: list[Relation] = []
    for entry in relations or ():
        relation_type, target_name = entry[0], entry[1]
        relation_status: EpistemicStatus | str = entry[2] if len(entry) > 2 else EpistemicStatus.CANDIDATE
        target_concept = _resolve_or_create_concept(db, target_name, None)
        created_relations.append(
            add_relation(
                db,
                source_concept_id=concept.concept_id,
                target_concept_id=target_concept.concept_id,
                field_id=field,
                relation_type=RelationType(relation_type),
                epistemic_status=relation_status,
                source=source,
            )
        )

    return concept, definition_record, created_relations
