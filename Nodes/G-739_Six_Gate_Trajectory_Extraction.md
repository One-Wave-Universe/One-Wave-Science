---
node_id: "G-739"
canonical_name: "Six-Gate Mirror-Action Trajectory Extraction"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Legacy G-Series / Canonicalized Node"
claim_gate_detail: "Measures behavior at the canonical six gate positions; it does not define a second six-gate system"
metadata_standard: "I-06"
---

# Node G-739: Six-Gate Mirror-Action Trajectory Extraction

## Canonical structure

This node does **not** create six measured oscillator gates beside the six-step program. The six process steps are the six gates:

```text
Gate 1  BEGIN = Mirror 1
Gate 2  BUILD = Action 1
Gate 3  HOLD  = Mirror 2
Gate 4  BUILD = Action 2
Gate 5  BREAK = Mirror 3
Gate 6  LOOP  = Action 3
```

or, by role:

```text
M1 -> A1 -> M2 -> A2 -> M3 -> A3 -> M1 ...
```

Exactly three positions are Mirror gates and exactly three are Action gates.

## Purpose

Trajectory extraction measures whether the physical/computational state at each canonical gate position actually behaves like its declared step. It must not paint a desired six-step sequence onto an animation, fabricate missing evidence, or invent a second set of gates.

The behavior labels remain:

```text
BEGIN -> BUILD -> HOLD -> BUILD -> BREAK -> LOOP
```

but they are measurements of the same six Mirror/Action gate positions defined by B-221a and C-301.

## Per-sample receipt

For sample `i`, the extractor may receive:

- `x_i`: displacement from the declared center/reference;
- `v_i`: velocity or state-change rate;
- `E_i`: stored-state or energy ledger;
- `c_i in [0,1]`: coherence;
- `h_i >= 0`: instability/heat receipt;
- `gate_i`: which of the six canonical gate positions is active;
- `role_i`: Mirror or Action.

The finite difference

```text
dot(E)_i = (E_i - E_(i-1)) / (t_i - t_(i-1))
```

can separate building, holding, and release behavior. Every tolerance is declared by the caller and retains the units of its variable.

## Evidence rules by canonical position

- **Gate 1 / BEGIN / Mirror 1:** shared-reference entry or beginning relation is read and established.
- **Gate 2 / BUILD / Action 1:** state is actively built/carried away from the first mirror resolution.
- **Gate 3 / HOLD / Mirror 2:** the built relation is read against reference and must demonstrate coherent retention rather than merely zero speed.
- **Gate 4 / BUILD / Action 2:** a second active build/carry operation follows the Hold mirror result.
- **Gate 5 / BREAK / Mirror 3:** the third mirror read detects/releases the condition that ends the built relation; a Break must be evidenced, not assumed.
- **Gate 6 / LOOP / Action 3:** the return/loop action carries the consequence into the next Gate 1 / BEGIN relation.

`Unclassified` remains valid when evidence is insufficient or contradictory. Unclassified is an audit result, not a seventh gate.

## Mirror/action discipline

A Mirror gate is a read/compare/reflect/reference role. An Action gate changes or carries the relation forward. A trajectory implementation fails if it sends a primitive action into a Mirror position or treats an Action position as another independent Mirror crossover without an explicit derived mechanism.

Higher-order view/action vocabularies may annotate the receipt, but they cannot change the primitive count:

```text
3 Mirror gates + 3 Action gates = 6 gates = 6 steps
```

## Validation boundary

Deterministic tests should cover all six canonical positions, ambiguous evidence, role alternation, and the requirement that Gate 6 feeds the next Gate 1 rather than creating Gate 7.

This node is an extractor/auditor. It does not prove a universal physical mechanism.

**Brick recommendation:** Yellow.
