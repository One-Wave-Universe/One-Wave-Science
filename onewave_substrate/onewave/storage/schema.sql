-- One-Wave knowledge substrate -- Phase 1 SQLite schema.
--
-- Design notes:
--   * Nothing here is stored as an opaque JSON blob unless the data is
--     genuinely unstructured free text (e.g. `fields.gate_rules`, which is
--     an open-ended, field-specific rule configuration with no fixed
--     shape yet).
--   * `definitions` is append-only: a logical definition (`definition_id`)
--     may have many immutable revisions (`revision_id` primary key),
--     linked by `supersedes`. Nothing is ever UPDATEd or DELETEd there.
--   * `path_events` is append-only per `runtime_id`, ordered by `seq`.
--     `runtime_records` holds a mutable *pointer* to the current
--     (field_state, displacement, memory_state) -- that pointer is always
--     re-derivable from initial state + ordered events via replay().
--   * Causality across runtime lineages is explicit (`causal_edges`),
--     never inferred from timestamps.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS concepts (
    concept_id      TEXT PRIMARY KEY,
    canonical_name  TEXT NOT NULL,
    created_at      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS aliases (
    alias       TEXT NOT NULL,
    concept_id  TEXT NOT NULL REFERENCES concepts(concept_id),
    PRIMARY KEY (alias, concept_id)
);

CREATE TABLE IF NOT EXISTS fields (
    field_id         TEXT PRIMARY KEY,
    name             TEXT NOT NULL,
    parent_field_id  TEXT REFERENCES fields(field_id),
    description      TEXT,
    gate_rules       TEXT
);

-- Append-only definition revisions. `definition_id` is the stable lineage
-- key shared by every revision of "the same" definition; `revision_id` is
-- the primary key of one immutable row.
CREATE TABLE IF NOT EXISTS definitions (
    revision_id       TEXT PRIMARY KEY,
    definition_id     TEXT NOT NULL,
    concept_id        TEXT NOT NULL REFERENCES concepts(concept_id),
    field_id          TEXT NOT NULL REFERENCES fields(field_id),
    text              TEXT NOT NULL,
    epistemic_status  TEXT NOT NULL,
    source            TEXT,
    confidence        REAL,
    created_at        TEXT NOT NULL,
    revision          INTEGER NOT NULL,
    supersedes        TEXT REFERENCES definitions(revision_id)
);

CREATE INDEX IF NOT EXISTS idx_definitions_lineage
    ON definitions(definition_id, revision);
CREATE INDEX IF NOT EXISTS idx_definitions_concept_field
    ON definitions(concept_id, field_id);

CREATE TABLE IF NOT EXISTS relations (
    relation_id        TEXT PRIMARY KEY,
    source_concept_id  TEXT NOT NULL REFERENCES concepts(concept_id),
    target_concept_id  TEXT NOT NULL REFERENCES concepts(concept_id),
    field_id           TEXT NOT NULL REFERENCES fields(field_id),
    relation_type      TEXT NOT NULL,
    epistemic_status   TEXT NOT NULL,
    weight             REAL,
    source             TEXT,
    created_at         TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_relations_source
    ON relations(source_concept_id, field_id);
CREATE INDEX IF NOT EXISTS idx_relations_target
    ON relations(target_concept_id, field_id);

-- Current pointer state of one runtime lineage. Always re-derivable from
-- replay(runtime_id) over path_events -- this table is a cache, not the
-- source of truth.
CREATE TABLE IF NOT EXISTS runtime_records (
    runtime_id         TEXT PRIMARY KEY,
    concept_id         TEXT NOT NULL REFERENCES concepts(concept_id),
    field_id           TEXT NOT NULL REFERENCES fields(field_id),
    field_state        INTEGER NOT NULL,
    displacement        REAL NOT NULL,
    memory_state        REAL NOT NULL,
    path                TEXT NOT NULL,
    parent_runtime_id   TEXT REFERENCES runtime_records(runtime_id),
    spawn_mode          TEXT NOT NULL DEFAULT 'root',
    created_at          TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS path_events (
    event_id                TEXT PRIMARY KEY,
    runtime_id              TEXT NOT NULL REFERENCES runtime_records(runtime_id),
    seq                     INTEGER NOT NULL,
    kind                    TEXT NOT NULL DEFAULT 'transition',
    a                       INTEGER NOT NULL,
    b                       INTEGER NOT NULL,
    gate_result             INTEGER NOT NULL,
    previous_field          INTEGER NOT NULL,
    resulting_field         INTEGER NOT NULL,
    previous_displacement   REAL NOT NULL,
    resulting_displacement  REAL NOT NULL,
    previous_memory         REAL NOT NULL,
    resulting_memory        REAL NOT NULL,
    created_at              TEXT NOT NULL,
    UNIQUE (runtime_id, seq)
);

CREATE INDEX IF NOT EXISTS idx_path_events_runtime
    ON path_events(runtime_id, seq);

-- Explicit causal DAG across (possibly different) runtime lineages.
-- Local append order within one runtime_id is authoritative on its own;
-- this table is the only source of cross-lineage causal claims.
CREATE TABLE IF NOT EXISTS causal_edges (
    edge_id                  TEXT PRIMARY KEY,
    event_id                 TEXT NOT NULL REFERENCES path_events(event_id),
    causal_parent_event_id   TEXT NOT NULL REFERENCES path_events(event_id)
);

CREATE INDEX IF NOT EXISTS idx_causal_edges_event
    ON causal_edges(event_id);
CREATE INDEX IF NOT EXISTS idx_causal_edges_parent
    ON causal_edges(causal_parent_event_id);
