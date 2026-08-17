---
node_id: "B-223"
canonical_name: "Three Moves — Left, Stay, Right"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "Implementation-canonical signed ternary relation; domain names remain representations"
metadata_standard: "I-06"
---

# Node B-223: Three Moves — Left, Stay, Right

## Definition

The Three Moves are the ternary directional result of a differential around the active reference:

```text
-1 = LEFT
 0 = STAY / HOLD / NON-ACTION
+1 = RIGHT
```

The labels Left and Right are orientation labels, not absolute spatial directions. A domain may rename them Compress/Hold/Expand, CCW/Hold/CW, negative/neutral/positive, or another equivalent signed representation without changing the primitive.

## Differential Rule

For a measured relation `Delta` and zero window `epsilon`:

```text
Delta < -epsilon  -> -1
|Delta| <= epsilon -> 0
Delta > +epsilon  -> +1
```

The zero state is a real no-assertion/hold result, not a third actively driven polarity.

## DC / AC Separation

Current hardware architecture separates two levels of choice:

```text
DC engagement: EVERYTHING / NOTHING
AC differential: LEFT / STAY / RIGHT
```

DC decides whether the local operation participates. If engaged, the AC/differential relation resolves how it participates.

## Important Distinction

The Three Moves are not the Four Actions. The Four Actions are:

```text
Inward / Outward / Across / Over
```

The Three Moves give signed direction/hold. The Four Actions specify transformation through a boundary/relation.

## Hardware Interpretation

A balanced physical read can use two opposed signals around a shared reference:

```text
Delta = side_A - side_B
```

A mirrored pair `A` and `-A` ideally produces `Delta = 2A`; a balanced relation produces `Delta ~= 0`. Real hardware requires a measured zero window and does not assume perfect cancellation.

## Yellow Audit

- The signed ternary move grammar is implementation-canonical.
- Exact voltage, phase, flux, or mechanical thresholds must be measured in each physical implementation.
- Left/Right are orientation labels and must not be mistaken for universal spatial coordinates.
