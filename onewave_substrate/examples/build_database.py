"""Build a persistent, on-disk SQLite database from the field entries.

This is the actual "database builder": it takes the field entries defined
in emotions.py / science.py / mixed_fields.py (concepts, field-scoped
definitions, typed relations) and writes them into a real .db file you
can open and inspect afterward with `sqlite3`, instead of the ephemeral
":memory:" database the query demo (examples/mixed_fields.run_demo) uses.

Rebuilds from scratch every run -- the field entries in source are the
authoritative data, and the .db file is a deterministic build output of
them, not something to hand-edit or run twice and accumulate duplicate
rows into.

Usage:
    python3 -m examples.build_database [output_path]
    # defaults to onewave.db in the current directory
"""

from __future__ import annotations

import sys
from pathlib import Path

import examples.emotions as emotions
import examples.mixed_fields as mixed_fields
import examples.science as science
from onewave.storage.sqlite import Storage

TABLES = (
    "concepts",
    "aliases",
    "fields",
    "definitions",
    "relations",
    "runtime_records",
    "path_events",
    "causal_edges",
)


def build(db_path: str) -> Storage:
    """Write a fresh SQLite database at db_path, seeded from every field
    entry in the demo dataset (emotion, behavior, standard physics,
    One-Wave research, One-Wave mythology)."""
    path = Path(db_path)
    if path.exists():
        path.unlink()

    db = Storage(str(path))
    emotions.seed(db)
    science.seed(db)
    mixed_fields.seed_mythology(db)
    return db


def summarize(db: Storage) -> str:
    lines = ["Row counts:"]
    for table in TABLES:
        n = db.query_one(f"SELECT COUNT(*) AS n FROM {table}")["n"]
        lines.append(f"  {table:<16} {n}")
    return "\n".join(lines)


def main() -> None:
    out_path = sys.argv[1] if len(sys.argv) > 1 else "onewave.db"
    db = build(out_path)
    print(f"Built {out_path}")
    print(summarize(db))
    db.close()


if __name__ == "__main__":
    main()
