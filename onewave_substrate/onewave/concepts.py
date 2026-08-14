"""Concepts and their field-scoped definitions.

A Concept is a bare, field-independent identity ("emotion.anger" means
"anger" and nothing else). All interpretation -- text, epistemic status,
confidence -- lives in DefinitionRecord rows scoped to a field. This is
what lets "mass" have a standard-physics definition, a One-Wave candidate
definition, and a mythological definition that never collapse together.

Definitions are append-only: `add_definition` never overwrites a row. A
correction supersedes the previous revision via `supersedes`, and the full
history stays queryable (`get_definition_history`).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from onewave.epistemic import EpistemicStatus
from onewave.storage.sqlite import Storage


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


@dataclass(frozen=True)
class Concept:
    concept_id: str
    canonical_name: str
    aliases: tuple[str, ...] = ()
    created_at: str = ""


@dataclass(frozen=True)
class DefinitionRecord:
    revision_id: str
    definition_id: str
    concept_id: str
    field_id: str
    text: str
    epistemic_status: EpistemicStatus
    source: str | None
    confidence: float | None
    created_at: str
    revision: int
    supersedes: str | None


# ---------------------------------------------------------------- concepts

def add_concept(
    db: Storage,
    concept_id: str,
    canonical_name: str,
    aliases: tuple[str, ...] | list[str] = (),
) -> Concept:
    created_at = _now()
    db.execute(
        """
        INSERT INTO concepts (concept_id, canonical_name, created_at)
        VALUES (?, ?, ?)
        ON CONFLICT(concept_id) DO UPDATE SET canonical_name=excluded.canonical_name
        """,
        (concept_id, canonical_name, created_at),
    )
    for alias in aliases:
        db.execute(
            "INSERT OR IGNORE INTO aliases (alias, concept_id) VALUES (?, ?)",
            (alias, concept_id),
        )
    return get_concept(db, concept_id)  # type: ignore[return-value]


def get_concept(db: Storage, concept_id: str) -> Concept | None:
    row = db.query_one("SELECT * FROM concepts WHERE concept_id = ?", (concept_id,))
    if row is None:
        return None
    alias_rows = db.query_all("SELECT alias FROM aliases WHERE concept_id = ?", (concept_id,))
    return Concept(
        concept_id=row["concept_id"],
        canonical_name=row["canonical_name"],
        aliases=tuple(r["alias"] for r in alias_rows),
        created_at=row["created_at"],
    )


def find_concept(db: Storage, name_or_alias: str) -> Concept | None:
    """Resolve a canonical name or alias (case-insensitive) to a Concept."""
    row = db.query_one(
        "SELECT concept_id FROM concepts WHERE lower(canonical_name) = lower(?)",
        (name_or_alias,),
    )
    if row is None:
        row = db.query_one(
            "SELECT concept_id FROM aliases WHERE lower(alias) = lower(?)",
            (name_or_alias,),
        )
    if row is None:
        return None
    return get_concept(db, row["concept_id"])


def list_concepts(db: Storage) -> list[Concept]:
    rows = db.query_all("SELECT concept_id FROM concepts ORDER BY concept_id")
    return [get_concept(db, r["concept_id"]) for r in rows]  # type: ignore[misc]


# -------------------------------------------------------------- definitions

def _row_to_definition(row) -> DefinitionRecord:
    return DefinitionRecord(
        revision_id=row["revision_id"],
        definition_id=row["definition_id"],
        concept_id=row["concept_id"],
        field_id=row["field_id"],
        text=row["text"],
        epistemic_status=EpistemicStatus(row["epistemic_status"]),
        source=row["source"],
        confidence=row["confidence"],
        created_at=row["created_at"],
        revision=row["revision"],
        supersedes=row["supersedes"],
    )


def add_definition(
    db: Storage,
    concept_id: str,
    field_id: str,
    text: str,
    epistemic_status: EpistemicStatus | str,
    source: str | None = None,
    confidence: float | None = None,
    supersedes: str | None = None,
) -> DefinitionRecord:
    """Append a new, immutable definition revision.

    If `supersedes` names a prior revision_id, the new row continues that
    revision's `definition_id` lineage at `revision + 1`. Otherwise a fresh
    definition_id lineage is started at revision 1.
    """
    if isinstance(epistemic_status, str):
        epistemic_status = EpistemicStatus(epistemic_status)

    if supersedes is not None:
        prior = get_definition(db, supersedes)
        if prior is None:
            raise ValueError(f"unknown supersedes revision_id: {supersedes!r}")
        definition_id = prior.definition_id
        revision = prior.revision + 1
    else:
        definition_id = _new_id("def")
        revision = 1

    revision_id = _new_id("rev")
    created_at = _now()
    db.execute(
        """
        INSERT INTO definitions (
            revision_id, definition_id, concept_id, field_id, text,
            epistemic_status, source, confidence, created_at, revision, supersedes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            revision_id, definition_id, concept_id, field_id, text,
            epistemic_status.value, source, confidence, created_at, revision, supersedes,
        ),
    )
    return DefinitionRecord(
        revision_id=revision_id,
        definition_id=definition_id,
        concept_id=concept_id,
        field_id=field_id,
        text=text,
        epistemic_status=epistemic_status,
        source=source,
        confidence=confidence,
        created_at=created_at,
        revision=revision,
        supersedes=supersedes,
    )


def get_definition(db: Storage, revision_id: str) -> DefinitionRecord | None:
    row = db.query_one("SELECT * FROM definitions WHERE revision_id = ?", (revision_id,))
    return _row_to_definition(row) if row else None


def get_definition_history(db: Storage, definition_id: str) -> list[DefinitionRecord]:
    rows = db.query_all(
        "SELECT * FROM definitions WHERE definition_id = ? ORDER BY revision ASC",
        (definition_id,),
    )
    return [_row_to_definition(r) for r in rows]


def get_current_definitions(
    db: Storage,
    concept_id: str,
    field_id: str | None = None,
) -> list[DefinitionRecord]:
    """Latest revision of every definition lineage for a concept.

    Scoped to `field_id` when given; otherwise returns the current
    definition from every field that has one, one row per field (never
    merged -- callers group by field_id themselves, see query.py).
    """
    if field_id is not None:
        rows = db.query_all(
            """
            SELECT d.* FROM definitions d
            INNER JOIN (
                SELECT definition_id, MAX(revision) AS max_rev
                FROM definitions
                WHERE concept_id = ? AND field_id = ?
                GROUP BY definition_id
            ) latest
            ON d.definition_id = latest.definition_id AND d.revision = latest.max_rev
            ORDER BY d.field_id, d.definition_id
            """,
            (concept_id, field_id),
        )
    else:
        rows = db.query_all(
            """
            SELECT d.* FROM definitions d
            INNER JOIN (
                SELECT definition_id, MAX(revision) AS max_rev
                FROM definitions
                WHERE concept_id = ?
                GROUP BY definition_id
            ) latest
            ON d.definition_id = latest.definition_id AND d.revision = latest.max_rev
            ORDER BY d.field_id, d.definition_id
            """,
            (concept_id,),
        )
    return [_row_to_definition(r) for r in rows]
