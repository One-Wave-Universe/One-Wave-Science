"""SQLite storage backend.

Deliberately thin: this module owns the connection, schema bootstrap, and
low-level execute/query helpers. Domain semantics (what a Concept or a
Relation *is*) live in the sibling domain modules (concepts.py, fields.py,
relations.py, runtime.py, events.py) -- they take a Storage instance and
issue SQL against it. Keeping the knowledge graph and the query helpers in
one place, but the meaning of the rows in another, is what lets each
domain module stay readable on its own.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Iterable, Sequence

_SCHEMA_PATH = Path(__file__).with_name("schema.sql")


class Storage:
    """A single SQLite-backed connection to the substrate database.

    Use `Storage(":memory:")` for tests/examples that don't need
    persistence across process runs, or a file path for a durable store.
    """

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.init_schema()

    def init_schema(self) -> None:
        schema_sql = _SCHEMA_PATH.read_text()
        self.conn.executescript(schema_sql)
        self.conn.commit()

    def execute(self, sql: str, params: Sequence[Any] = ()) -> sqlite3.Cursor:
        cur = self.conn.execute(sql, params)
        self.conn.commit()
        return cur

    def executemany(self, sql: str, seq_of_params: Iterable[Sequence[Any]]) -> None:
        self.conn.executemany(sql, seq_of_params)
        self.conn.commit()

    def query_one(self, sql: str, params: Sequence[Any] = ()) -> sqlite3.Row | None:
        cur = self.conn.execute(sql, params)
        return cur.fetchone()

    def query_all(self, sql: str, params: Sequence[Any] = ()) -> list[sqlite3.Row]:
        cur = self.conn.execute(sql, params)
        return cur.fetchall()

    def close(self) -> None:
        self.conn.close()

    def __enter__(self) -> "Storage":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
