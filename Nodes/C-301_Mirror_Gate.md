---
node_id: "C-301"
canonical_name: "Mirror Gate"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Applied Mechanics and Boundary Structure"
claim_gate_detail: "Canonical role: three Mirror gates occupy three of the six primitive gate positions; the other three positions are Action gates"
metadata_standard: "I-06"
---

# Node C-301: Mirror Gate

## Definition

A Mirror Gate is the read/compare/reflect gate of the shared-reference oscillator. It evaluates the opposed relation through the shared `(0)` reference and hands the resolved relation to the following Action gate.

The full primitive is not six Mirror crossovers. It is one six-gate cycle:

```text
Mirror 1 -> Action 1 -> Mirror 2 -> Action 2 -> Mirror 3 -> Action 3 -> loop
```

Therefore:

```text
3 Mirror gates + 3 Action gates = 6 gates = 6 steps
```

## Mapping to the six process steps

```text
Gate 1  BEGIN = Mirror 1
Gate 2  BUILD = Action 1
Gate 3  HOLD  = Mirror 2
Gate 4  BUILD = Action 2
Gate 5  BREAK = Mirror 3
Gate 6  LOOP  = Action 3
```

The step names and gate positions are the same six positions. They are not parallel six-count systems.

## Field/Void paired view

The existing paired notation is retained as a view of those same positions:

```text
BEGIN / Mirror 1 = F1/V6
BUILD / Action 1 = V5/F2
HOLD  / Mirror 2 = F3/V4
BUILD / Action 2 = V3/F4
BREAK / Mirror 3 = F5/V2
LOOP  / Action 3 = V1/F6
```

`/` means one simultaneous opposed Field/Void relation. The two sides are not separate serial gates.

A Mirror gate may involve return toward the shared reference, comparison/crossover, and phase/orientation update as part of its read/reflect operation. That does **not** insert an extra Mirror gate between each of the six positions.

## Local Mirror -> Action handoff

```text
opposed relation arrives
 -> Mirror gate reads relation against shared reference
 -> mirror/reference resolution is produced
 -> paired Action gate changes/carries the relation
 -> resulting state becomes input to the next Mirror gate
```

This is the repeating primitive at all three Mirror/Action pairs.

## Physical-hardware boundary

A VTC implementation may use linked opposed switching elements, magnetic coupling, differential sensing, or another physical mechanism. There are three primitive Mirror-gate roles in the six-gate cycle and three primitive Action-gate roles.

Hardware may realize one gate role with multiple devices, phases, windings, or paths. Those implementation details do not multiply the logical gate count.

## Relationship to views/actions vocabulary

Higher routing layers may use vocabularies such as Direction/Phase/Strength/Reference or Inward/Outward/Across/Over. Those are descriptive views or action modes available **inside** a gate role. They are not four extra primitive Action gates and do not alter the six-gate count.

## Anti-drift rule

Reject any interpretation that says:

- six steps plus six separate gates;
- six Mirror gates between six step positions;
- three Mirror gates used twice create six Mirror-gate positions;
- route addresses or view/action labels add primitive gates.

The canonical count is fixed:

```text
M1 -> A1 -> M2 -> A2 -> M3 -> A3 -> M1 ...
```
