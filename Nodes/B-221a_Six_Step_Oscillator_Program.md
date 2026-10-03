---
node_id: "B-221a"
canonical_name: "Six-Step / Three-Mirrored-Flip Oscillator"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "Canonical architecture lock: six process positions form three reflected bidirectional flips: 1↔6, 2↔5, 3↔4"
metadata_standard: "I-06"
---

# Node B-221a: Six-Step / Three-Mirrored-Flip Oscillator

## Canonical lock

The old `Mirror 1 / Action 1 / Mirror 2 / Action 2 / Mirror 3 / Action 3` numbering is **retired**. It incorrectly imposed three separately numbered Action gates onto the six-step cycle.

There is one six-position heartbeat:

```text
1 BEGIN
  ↓
2 BUILD
  ↓
3 HOLD
  ↓
4 BUILD
  ↓
5 BREAK / RELEASE
  ↓
6 LOOP
  ↓
1 BEGIN
```

Its mirror structure is:

```text
1 BEGIN  ⇄  6 LOOP             — FLIP 1: VOID / REFERENCE
2 BUILD  ⇄  5 BREAK / RELEASE  — FLIP 2: POWER / CHARGE-RELEASE
3 HOLD   ⇄  4 BUILD            — FLIP 3: TRIGGER / LOADED-ARMED
```

Therefore:

```text
6 steps = 3 mirrored bidirectional flips
```

The six positions are the six faces of those three reflected pairs.

## Canonical chart

```text
1. BEGIN  ─┐
           ├─ FLIP 1 — VOID / REFERENCE
6. LOOP   ─┘

2. BUILD  ─┐
           ├─ FLIP 2 — POWER / CHARGE-RELEASE
5. BREAK  ─┘

3. HOLD   ─┐
           ├─ FLIP 3 — TRIGGER / LOADED-ARMED
4. BUILD  ─┘
```

This reflection is positional:

```text
1 ⇄ 6
2 ⇄ 5
3 ⇄ 4
```

Do not replace it with consecutive pairings `1→2, 3→4, 5→6`.

## Meaning of the three flips

### Flip 1 — Void / reference

```text
BEGIN ⇄ LOOP
```

BEGIN establishes or exposes the current reference/void. LOOP returns, reconciles, recovers, and re-establishes the reference for recurrence.

### Flip 2 — Power

```text
BUILD ⇄ BREAK / RELEASE
```

BUILD develops/loads the power condition. BREAK/RELEASE is its mirrored expression/release.

### Flip 3 — Trigger

```text
HOLD ⇄ BUILD
```

HOLD is the loaded/retained condition. The second BUILD is the mirrored trigger-armed condition immediately preceding release.

## Field / Void paired notation

Legacy F/V labels may remain as descriptive receipts only if they preserve the current reflected structure.

The authority is the positional mirror:

```text
BEGIN ⇄ LOOP
BUILD ⇄ BREAK
HOLD  ⇄ BUILD
```

Do not use legacy F/V labels to reconstruct three numbered Action gates.

## Recursion

The three flips are recursively composable through Begin/Loop boundaries.

```text
FLIP 1: BEGIN ⇄ LOOP
          │
          └── FLIP 2: BUILD ⇄ BREAK
                         │
                         └── FLIP 3: HOLD ⇄ BUILD
```

A supported flip/transition may expose a local BEGIN/LOOP relation and may instantiate the same grammar at another physically supported scale.

This is architectural recursion. It does not assert physically infinite recursion. Actual depth must be established by the implementation or measurement.

See:

- `Builds/CELL_V1_RECURSIVE_OPERATING_CYCLE.md`
- `Builds/CELL_V1_SIX_STEPS_THREE_MIRRORED_FLIPS.md`

The nested ASCII chart in the recursive operating-cycle file is part of the architecture record and must be preserved.

## Relationship to Views and Actions

Views and Actions are directional/read-write descriptions projected through the mirrored relations. They are **not separately numbered primitive gates**.

The four-Views-up / four-Actions-down vocabulary may describe information/action orientation through a flip, but it must not create:

- Action 1,
- Action 2,
- Action 3,

as independent primitive gate identities.

There are three mirrored flips, not three Mirror gates plus three separately numbered Action gates.

## Relationship to Three Moves and Six Routes

The six-step heartbeat is not the route-address space.

`UPDATED_43_TWO_CHOICE_THREE_MOVE_SIX_ROUTE_LOGIC.md` separately defines:

```text
2 binary choices × 3 ternary moves = 6 route addresses
```

and:

```text
DOWN / HOLD / UP = -1 / 0 / +1
```

Matching counts do not merge mechanisms.

## Relationship to Five-State Self Lifecycle

The five-state lifecycle remains a separate behavioral description:

```text
IDLE → PRIMED → EXECUTING → VECTORING → RESOLVING
```

It does not replace the six-step / three-flip grammar.

## Scale boundary

Scale labels are not aliases for the six positions or three flips. If the same three-flip grammar recurs at another scale, that recurrence must be explicitly mapped.

## Superseded interpretation

The following formulation is retired and must not be reconstructed as current authority:

```text
BEGIN = Mirror 1
BUILD = Action 1
HOLD  = Mirror 2
BUILD = Action 2
BREAK = Mirror 3
LOOP  = Action 3
```

Likewise retired:

```text
3 Mirror gates + 3 Action gates = 6 gates
```

The six steps remain six process positions, but their structural relation is three mirrored bidirectional flips.

## Anti-drift audit

A description fails this node if it:

- restores Action 1 / Action 2 / Action 3 as primitive gate identities;
- restores three consecutive Mirror→Action pairs as the fundamental pairing;
- treats BEGIN↔LOOP, BUILD↔BREAK, HOLD↔BUILD as optional instead of canonical;
- turns four Views/four Actions into additional primitive flips;
- turns six route addresses into six oscillator gates;
- treats the three flips as three unrelated sequential switches;
- deletes the recursive Begin/Loop relation.

Canonical primitive:

```text
SIX PROCESS POSITIONS
        =
THREE MIRRORED BIDIRECTIONAL FLIPS

1 BEGIN ⇄ 6 LOOP
2 BUILD ⇄ 5 BREAK / RELEASE
3 HOLD  ⇄ 4 BUILD
```
