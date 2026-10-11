# Self-organizing, self-reinforcing repository — bounded automation v1

**Meaning:** detect canonical drift, regenerate derived discovery indexes deterministically, run math and governance tests, and propose a reviewed repair. Self-reinforcing means evidence and references become more consistent with each accepted change; it does **not** mean an AI can validate its own physical claims or rewrite canon autonomously.

## Cycle
REFERENCE -> SCAN -> CLASSIFY -> GENERATE DERIVED SURFACES -> TEST -> RECEIPT -> REPAIR PR -> HUMAN REVIEW -> MERGE -> RE-SCAN.

The source of truth stays in the canonical files; generated indexes are projections, not competing authorities. Rabbit Hopping preserves identity and route provenance; Algorithm Zero recursion supplies a proposed organizational lens at each scale; the Circle of Fifths is a domain-specific mathematical model. Their mapping is not proof of universal physics.

## Existing authorities
- GENERAL_REFERENCE_RULES.md: one canonical source, task branches, receipts.
- Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md: node identity and metadata.
- scripts/sync_node_graph_indexes.py: deterministic master index and AI discovery synchronization.
- scripts/normalize_legacy_node_metadata.py: metadata check (no auto normalization).
- Math_Verification/verify.py and verify_integrations.py: arithmetic controls; physics remains unverified.
- MATH_BACKBONE/00_MATH_BACKBONE_LOCK.md: protected append-only math.

## Safety boundaries
- Automation **only** writes derived `00_MASTER_INDEX.md` and `AI_CANONICAL_START_HERE.md` through the existing synchronizer.
- Does not edit source nodes, lock files, metadata, science claims, CELL_V1, or breadboard.
- Opens/updates one repair branch and PR. Never auto-merges or self-approves.
- Workflow fails closed on any failed control. Changes to sources must pass existing checks.
- If token cannot create a PR, leave a failure receipt and manual recovery path; do not silently declare success.
- No autonomous agents or background LLM calls. No arbitrary generated edits.

## Operator commands
```sh
python3 scripts/normalize_legacy_node_metadata.py --check
python3 scripts/sync_node_graph_indexes.py --check
python3 Math_Verification/verify.py --all
python3 Math_Verification/verify_integrations.py
# To repair stale derived indexes on a task branch:
python3 scripts/sync_node_graph_indexes.py
git diff -- 00_MASTER_INDEX.md AI_CANONICAL_START_HERE.md
```

Future iterations: dependency graph with canonical node IDs, broken-link detection, source provenance, impact analysis, unit/energy/convergence gates, and reviewable AI suggestions. Never infer correctness from a passing format check.
