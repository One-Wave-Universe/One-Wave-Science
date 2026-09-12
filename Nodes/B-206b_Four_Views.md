---
node_id: "B-206b"
canonical_name: "Four Views — Direction, Phase, Strength, Reference"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "Descriptive four-view readout vocabulary; does not alter the three-Mirror/three-Action primitive gate cycle"
metadata_standard: "I-06"
---

# Node B-206b: Four Views — Direction, Phase, Strength, Reference

## Canonical boundary

The primitive gate cycle is fixed elsewhere as:

```text
M1 -> A1 -> M2 -> A2 -> M3 -> A3 -> M1 ...
```

with exactly three Mirror gates and three Action gates.

The four Views below are **readout dimensions/modes** available to a Mirror-gate evaluation. They are not four Mirror gates and do not change the six-gate count.

## The Four Views

1. **Direction** — which way the resolved relation leans or moves relative to the active reference. At a ternary routing layer this may be represented as `-1 / 0 / +1`.
2. **Phase** — where the oscillatory relation is in its cycle, including handedness/orientation when the implementation tracks it.
3. **Strength** — how large or intense the relation is relative to its active reference. Threshold bands may represent this quantity without becoming gate states.
4. **Reference** — the local baseline `(0)` against which Direction, Phase, and Strength are interpreted.

A minimal descriptive packet is:

```text
ViewState {
    direction
    phase
    strength
    reference
}
```

This packet describes state. It does not command an action and does not add gate positions.

## Relationship to Action gates and Action modes

The primitive architecture has three Action gates: `A1`, `A2`, and `A3`.

B-206c provides an optional four-mode vocabulary for describing what an Action gate may do:

```text
Inward / Outward / Across / Over
```

Keep the counts separate:

```text
4 Views = readout vocabulary
4 Action modes = transformation vocabulary
3 Mirror gates = primitive read/compare positions
3 Action gates = primitive change/carry positions
6 total primitive gates = 6 process steps
```

There is no required one-to-one mapping between a View and an Action mode.

## Operational chain

```text
state
 -> Mirror gate reads Direction / Phase / Strength / Reference
 -> Mirror resolution
 -> paired Action gate A1/A2/A3
 -> optional action-mode description
 -> consequence/new state
 -> next Mirror gate
```

## Domain independence

The same View vocabulary can describe circuits, wave packets, cells, lattice relations, cognitive states, or other scale-specific systems. Domain labels are wrappers above the invariant engine.

## Anti-drift rule

If a representation turns Direction/Phase/Strength/Reference into four primitive Mirror gates, or turns Inward/Outward/Across/Over into four primitive Action gates, it has changed the architecture and must be rejected.

Canonical primitive remains:

```text
3 Mirror + 3 Action = 6 gates = 6 steps
```

## Yellow audit

- Four-view measurement vocabulary is canonical as a descriptor layer.
- Exact sensors and mathematical coordinates remain implementation-specific.
- Its relationship to dimensional 1D/2D/3D/4D representations must be derived separately.
