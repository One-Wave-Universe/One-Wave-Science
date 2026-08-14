# One-Wave Generative Relational Knowledge Substrate — Phase 1

A working Python reference implementation of a generative, state-aware
knowledge substrate that stores concepts as relational, field-aware
records instead of flat dictionary entries.

The one rule everything else here exists to enforce:

> **No interpretation outside an active field.**

The same concept ("mass", "gravity", "anger", "Void") can carry multiple,
mutually non-contradictory interpretations across different fields
(`science.physics.standard`, `science.physics.one_wave`,
`mythology.one_wave`, `emotion`, `behavior`, ...). The engine never merges
them into one asserted answer.

This is Phase 1: **correctness and transparency over performance.** No
C++ kernel, no LLM. SQLite, pure functions, and deterministic replay.

## Quick start

```bash
cd onewave_substrate
python3 -m pip install -e ".[dev]"   # or just: pip install pytest
python3 -m pytest                    # 54 tests
python3 -m examples.mixed_fields     # full demo dataset + required demo queries, in-memory
python3 -m examples.build_database   # writes a real, persistent onewave.db to disk
```

`examples.mixed_fields` runs everything against an ephemeral `:memory:`
SQLite database -- it exists only for the life of that process, which is
fine for a query demo. `examples.build_database` is the actual database
*builder*: it takes the same field entries (emotion, behavior, standard
physics, One-Wave research, One-Wave mythology -- 24 concepts, 8 fields,
33 definitions, 20 relations) and writes them into a real `.db` file on
disk that you can inspect afterward with the `sqlite3` CLI or any SQLite
browser:

```bash
python3 -m examples.build_database onewave.db
sqlite3 onewave.db ".tables"
sqlite3 onewave.db "SELECT field_id, epistemic_status, text FROM definitions WHERE concept_id='mass';"
```

It rebuilds from scratch on every run (deletes any existing file at the
given path first), so re-running it never accumulates duplicate rows --
the field entries in `examples/*.py` are the source of truth, and the
`.db` file is a deterministic build output of them, not something to
hand-edit.

## Layout

```
onewave/
  ternary.py     Ternary enum (RETURN/HOLD/ADVANCE) + sgn3()
  epistemic.py   EpistemicStatus vocabulary
  fields.py      Field model (nested, non-inheriting by default)
  concepts.py    Concept identity + append-only DefinitionRecord revisions
  relations.py   Typed, field-scoped Relation + RelationType
  transition.py  Pure Gamma (gate) / Phi (field update) / T (transition)
  events.py      Append-only PathEvent log + explicit causal_edges DAG
  runtime.py     RuntimeRecord: point/path/field, snapshot & live children
  replay.py      Rebuild state from events alone; detect divergence
  query.py       query_concept() + deterministic template rendering
  ingest.py      add_concept/add_definition/add_relation/add_field + ingest_entry()
  storage/       SQLite connection (sqlite.py) + schema (schema.sql)
tests/           54 tests across gate truth table, phi, transition, replay,
                 fields, relations, recursive frames, causality, query, ingest
examples/        emotions.py, science.py, mixed_fields.py (full demo + Section 23 queries)
                 build_database.py (builds a persistent onewave.db on disk)
```

Knowledge graph (concepts/fields/definitions/relations) and runtime state
(runtime_records/path_events/causal_edges) are separate SQLite tables. A
definition never mutates because of runtime activity; a transition never
rewrites the knowledge graph.

## Design decisions made where the brief was ambiguous

The brief's boxed formulas were occasionally underspecified (dual-ternary
gate precedence, the sign in Φ, what "live child" composition means in
full). Rather than guess silently, each choice is documented at the point
it's made and is covered by a test:

1. **Gamma's dual-ternary precedence** (`transition.py`): ground input
   (`A==0 or B==0 → HOLD`) beats mirror cancellation (`A == -F → HOLD`,
   regardless of B) beats consensus (`A == B → g = A`, else `HOLD`). Full
   27-combination truth table is hand-derived independently of the
   implementation in `tests/test_gamma.py`.
2. **Phi uses a restoring sign**: `F' = sgn3(M' - κ·Δ')`. Memory pushes
   the field forward; accumulated displacement pulls it back — consistent
   with "restoring response" elsewhere in the One-Wave material. This is
   what makes a runtime driven by constant ADVANCE inputs eventually flip
   into RETURN (see the demo's Query 6) instead of diverging forever.
3. **Live children compose displacement only**: `X_C(t) = X_P(t) +
   Δ_{C|P}(t)`, computed recursively at read time
   (`runtime.get_point`). `memory_state` stays local to the child; the
   effective `field_state` is recomputed from the composed displacement
   and the child's own memory. Snapshot children never recompute anything
   after spawn — they're fully independent.
4. **Definitions are append-only revisions**, not append-only rows with
   no lineage: `definition_id` is a stable lineage key, `revision_id` is
   the immutable per-revision primary key, `supersedes` chains them.
5. **`EpistemicStatus.INFERRED`** was added beyond the brief's required
   list to give inferred relations somewhere to live that isn't
   `CANDIDATE`, `DEFINITION`, `OBSERVED`, or `DERIVED` — nothing is ever
   auto-promoted into those without an explicit step (brief §25).
6. **Genesis events**: every runtime lineage gets a `kind="genesis"`
   event at seq 0 recording its origin state. This makes `replay()`
   fully self-contained (start from `State()`, replay every event) even
   for snapshot/live children whose origin isn't the zero state.

## Core rule, enforced in code (not just docs)

- `query_concept(db, concept, active_field=...)` — with a field given,
  only that field's claims come back.
- `query_concept(db, concept)` — without a field, results are grouped by
  field and returned as separate `FieldAnswer` blocks; `render_answer()`
  prints them as separate labeled sections. Nothing is flattened.
- `tests/test_relations.py::test_no_leakage_of_unsupported_claims_between_fields`
  and `test_query_without_active_field_groups_but_never_merges` assert
  this directly against the `mass` example from brief §15.

## Definition of Done — Phase 1 (brief §29), verified

- [x] SQLite schema works (`onewave/storage/schema.sql`, FK-enforced).
- [x] Concepts can be added (`add_concept`, `ingest_entry`).
- [x] Multiple definitions per concept, separated by field
      (`tests/test_relations.py`, `examples/science.py`).
- [x] Epistemic status enforced end-to-end (`EpistemicStatus`, never
      silently collapsed — see design decision docs above).
- [x] Relations are typed (`RelationType`, 14 types).
- [x] Ternary runtime transitions work (`transition.py`, `Ternary`).
- [x] History is append-only (`path_events`, `definitions` revisions).
- [x] Replay is deterministic (`tests/test_replay.py`, 100-event replay +
      cache-corruption survival + tamper detection).
- [x] Γ passes the full 27-combination truth table
      (`tests/test_gamma.py`), including explicit mirror-cancellation and
      ground-input invariant tests.
- [x] Φ uses both memory and displacement (`tests/test_phi.py`).
- [x] Snapshot child references work (`tests/test_recursive_frames.py`).
- [x] Live child references work (same file).
- [x] Cross-record causal edges work (`tests/test_causal.py`: two
      independent lineages feeding a third, local order stays separate
      from the explicit causal DAG).
- [x] Queries respect active field (`tests/test_query.py`).
- [x] Standard science and One-Wave claims never silently merge
      (`examples/science.py` + `test_relations.py`).
- [x] Mythology stays explicitly mythology (`examples/mixed_fields.py`,
      `EpistemicStatus.MYTHOLOGY`).
- [x] The emotion/science/one-wave/mythology demonstration dataset works
      end-to-end: `python3 -m examples.mixed_fields` runs all seven
      required demo queries from brief §23 (anger; anger in the behavior
      field; gravity across standard/one-wave/mythology; Void; fear↔anger
      relation; the path into RETURN; spawning and independently
      evolving a snapshot child).

Run `python3 -m pytest -v` to see all 54 tests individually; run
`python3 -m examples.mixed_fields` to see the demo queries' actual output.

## What's deliberately NOT here yet

- No C++ kernel (brief §1, §28 — only after this reference implementation
  is validated, which it now is).
- No LLM (brief §24) — `query.render_answer` is plain deterministic
  templating; an LLM, if ever added, sits above this module and
  verbalizes its structured output.
- No automatic field inference (brief §17) — `active_field` is always
  either explicit or omitted (grouped-by-field results); `infer_field()`
  is future work.
- No automatic claim promotion (brief §25) — inferred relations stay
  `CANDIDATE`/`INFERRED` until an explicit validation step exists.
