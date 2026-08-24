---
node_id: "B-228"
canonical_name: "Mirrored Three-Gate Grammar"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "Extracted from UPDATED_37 and reconciled with current user corrections; hardware mapping remains experimental."
metadata_standard: "I-06"
---

# B-228 — Mirrored Three-Gate Grammar

## Core gate classes

The primitive uses three gate classes:

`Binary -> Ternary -> Quadratic`

with cardinalities

`2 -> 3 -> 4`.

The mirrored traversal uses the same classes in reverse:

`2 -> 3 -> 4 -> 4 -> 3 -> 2`.

## Current operational mapping

The outward half establishes and expands the shared state:

1. **Binary / Gate 1** — polarity choice paired with scale relation.
2. **Ternary / Gate 2** — direction and signed differential, including neutral/hold.
3. **First Quadratic** — vector actions acting on the shared polarity + direction + differential state.

The return half resolves and routes the consequence:

4. **Second Quadratic** — tensor-level resolving/readback relation across the shared vector state.
5. **Ternary return** — reduced directional/differential routing.
6. **Binary return** — final choice/participation closure into the next Begin/reference relation.

This node deliberately does not collapse gate class, dimensional view, lifecycle state, scale, and physical-current behavior into one label.

## Logical mirror

Let the gate-class sequence be

`g = (2,3,4,4,3,2)`.

Then

`g_i = g_(7-i)`

for `i = 1,...,6`, expressing the cardinality mirror around the central quadratic pair.

The central pair has equal cardinality but different jobs:

`Q_1 != Q_2` operationally even though `|Q_1| = |Q_2| = 4`.

`Q_1` applies vector actions; `Q_2` resolves the combined relation at tensor level and routes the return.

## Physical shorthand

The earlier experimental physical shorthand remains a useful mapping target:

`BC-DC -> TC-AC -> QC-RC`

with mirrored return through the same gate classes. This is a proposed hardware interpretation, not proof that a breadboard has achieved stable AC oscillation, rotating current, or magnetic memory.

## Separation rule

Keep these axes distinct:

- gate cardinality: `2 / 3 / 4`,
- process steps: `Begin / Build / Hold / Build / Break / Loop`,
- five computational states: B-226,
- dimensional views: D-414,
- compression/coordination ratios: D-415,
- physical electrical implementation: experimental bench layer.

## Relationships

- Depends on: B-223 Three Moves, B-224 Two Choices, B-226 Scalar-Differential-Vector-Tensor-Resolving, D-414 Four Dimensional Views, D-415 Five Compression Coordination Ratios.
- Refines: B-221 Six Recursive Steps without replacing it.
- Source provenance: `UPDATED_37_THREE_GATE_LANGUAGE_AND_SIX_STEP_MIRROR.md`.

## Test condition

A working simulation should log each transition with separate fields for gate class, state stage, dimensional view, scale ratio, and route direction. A failure occurs if any of these axes are silently substituted for another.