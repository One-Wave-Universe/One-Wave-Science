"""Fields: the active interpretive context.

A field is what makes "No interpretation outside an active field" concrete.
Every definition and every relation is scoped to exactly one field_id.
Fields may nest (science.physics.standard is a child of science.physics),
but nesting is purely organizational metadata -- a child field does NOT
automatically inherit its parent's definitions or relations. If a field's
`gate_rules` JSON explicitly lists inherited parent field ids, callers can
consult `allowed_parent_field_ids()`; nothing merges automatically.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field as dc_field
from datetime import datetime, timezone

from onewave.storage.sqlite import Storage


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class Field:
    field_id: str
    name: str
    parent_field_id: str | None = None
    description: str = ""
    gate_rules: dict = dc_field(default_factory=dict)

    def allowed_parent_field_ids(self) -> list[str]:
        """Parent field ids this field explicitly opts into inheriting from.

        Empty unless gate_rules carries an `"inherit"` list. No implicit
        inheritance ever happens -- see module docstring.
        """
        inherit = self.gate_rules.get("inherit", [])
        return list(inherit) if isinstance(inherit, list) else []


def add_field(
    db: Storage,
    field_id: str,
    name: str,
    parent_field_id: str | None = None,
    description: str = "",
    gate_rules: dict | None = None,
) -> Field:
    gate_rules = gate_rules or {}
    if parent_field_id is not None and get_field(db, parent_field_id) is None:
        raise ValueError(f"unknown parent_field_id: {parent_field_id!r}")
    db.execute(
        """
        INSERT INTO fields (field_id, name, parent_field_id, description, gate_rules)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(field_id) DO UPDATE SET
            name=excluded.name,
            parent_field_id=excluded.parent_field_id,
            description=excluded.description,
            gate_rules=excluded.gate_rules
        """,
        (field_id, name, parent_field_id, description, json.dumps(gate_rules)),
    )
    return Field(field_id, name, parent_field_id, description, gate_rules)


def _row_to_field(row) -> Field:
    return Field(
        field_id=row["field_id"],
        name=row["name"],
        parent_field_id=row["parent_field_id"],
        description=row["description"] or "",
        gate_rules=json.loads(row["gate_rules"]) if row["gate_rules"] else {},
    )


def get_field(db: Storage, field_id: str) -> Field | None:
    row = db.query_one("SELECT * FROM fields WHERE field_id = ?", (field_id,))
    return _row_to_field(row) if row else None


def list_fields(db: Storage) -> list[Field]:
    rows = db.query_all("SELECT * FROM fields ORDER BY field_id")
    return [_row_to_field(r) for r in rows]


def child_fields(db: Storage, parent_field_id: str) -> list[Field]:
    rows = db.query_all(
        "SELECT * FROM fields WHERE parent_field_id = ? ORDER BY field_id",
        (parent_field_id,),
    )
    return [_row_to_field(r) for r in rows]


def field_ancestry(db: Storage, field_id: str) -> list[Field]:
    """Return [field, parent, grandparent, ...] up to the root.

    This is organizational lineage only -- it does not imply that
    definitions/relations from ancestors apply to `field_id`.
    """
    chain: list[Field] = []
    current = get_field(db, field_id)
    seen: set[str] = set()
    while current is not None and current.field_id not in seen:
        chain.append(current)
        seen.add(current.field_id)
        current = get_field(db, current.parent_field_id) if current.parent_field_id else None
    return chain
