# OWATCH logic kernel (next layer)

Not a cell. Not emergence. Not route-as-truth.

Gemini lock-in + DeepSeek no-inference: build this before more flower topology.

## Inputs
Sentence-level edges only for v1: SUPPORTS, CONTRADICTS.
Each edge: source span id, target span id, reference, intention, consequence.
Missing any of those three → HOLD. No derivation.

## Deterministic rules (v1)
- SUPPORTS(A,B) and SUPPORTS(B,C) → propose SUPPORTS(A,C) as DERIVED, never as canon.
- CONTRADICTS(A,B) and SUPPORTS(C,A) → propose CONTRADICTS(C,B) as DERIVED.
- CONTRADICTS(A,A) or cycle A⇔B⇔A of CONTRADICTS with no third referee → HOLD + terminate that route.
- Two derived CONTRADICTS that close a loop → HOLD. Do not write Nodes/. Do not strengthen route memory.

## Termination harness
Deliberate circular contradiction corpus. Pass if:
1. loop stops (no infinite propose),
2. HOLD fires,
3. route hysteresis for that path is decayed, not boosted,
4. later unrelated queries are not poisoned.

## Receipts
wrong_derivations, correct_derivations, holds, hysteresis_boost_on_bad_path (must be 0).

## Authority
route_memory_is_authority: false
derived ≠ source markdown
Flower/cell sims remain software twins for fan-out/contention tests only.


## Lineage and referee law

v1.1 freezes these implementation constraints:

- source and derived edges carry stable `edge_id` values;
- derived lineage stores exact `parent_ids`, not only `(source,target,type)`;
- derived edge IDs include rule ID + parent edge IDs + relation endpoints;
- only `source_class: canon`, `derived: false`, `CONTRADICTS` may act as referee;
- a matching canon referee deterministically invalidates a derived `SUPPORTS`;
- invalidation is idempotent and mark-before-recurse;
- stale derived descendants are recursively pruned by edge ID;
- referee HOLD/prune decays bad source routes and never boosts them;
- derived/ledger state remains disposable runtime state and never writes `Nodes/`.

## Repo-node authority chain

Every logic receipt carries this chain:

```text
GENERAL_REFERENCE_RULES.md
  -> AI_CANONICAL_START_HERE.md
  -> Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md
  -> LOGIC_KERNEL.md
  -> OWATCH_FULL_VISION.md
  -> corpus / receipt
```

The chain establishes authority and provenance. It does not make a derived edge canonical.

## Bronze second-corpus gate

Bronze requires an independent lifecycle corpus where:

1. a false SUPPORTS parent is derived;
2. a derived grandchild depends on it;
3. a non-derived canon CONTRADICTS referee invalidates the parent;
4. the parent and grandchild are pruned;
5. `wrong_derivations > 0`;
6. `stale_children_pruned > 0`;
7. `hysteresis_boost_on_bad_path = 0`;
8. an unrelated route is unchanged;
9. `Nodes/` remains untouched.

Receipt: `LOGIC_KERNEL_CORPUS2_RECEIPT.json`.
