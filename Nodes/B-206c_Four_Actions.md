---
node_id: "B-206c"
canonical_name: "Four Action Modes — Inward, Outward, Across, Over"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "Descriptive action-mode vocabulary used inside the three primitive Action gates; not four additional gates"
metadata_standard: "I-06"
---

# Node B-206c: Four Action Modes — Inward, Outward, Across, Over

## Canonical boundary

The primitive six-gate cycle contains exactly **three Action gates**:

```text
M1 -> A1 -> M2 -> A2 -> M3 -> A3 -> M1 ...
```

The words **Inward, Outward, Across, Over** are four **action modes** describing what an active Action gate may do. They are not four primitive Action gates and they do not change the gate count.

```text
3 Mirror gates + 3 Action gates = 6 gates = 6 steps
```

## Action-mode vocabulary

1. **Inward** — move/compress the active relation toward its local reference or center.
2. **Outward** — express/extend the active relation away from its local reference or center.
3. **Across** — establish/carry a relation across opposed sides through a shared reference/boundary.
4. **Over** — carry the resolved relation into a changed orientation, path, cell, or recursive scale when the implementation supports that transition.

A single Action gate may use one mode, combine modes, or use another derived domain-specific operation. The mode vocabulary does not create extra gate positions.

## Mirror/Action distinction

Mirror gates and Action gates are different primitive roles:

```text
Mirror gate = read / compare / reflect through reference
Action gate = change / carry the resolved relation
```

`Across` and `Over` describe possible Action behavior. They are not Mirror gates and are not themselves gate numbers.

## Relationship to the Four Views

The four View modes in B-206b are:

```text
Direction
Phase
Strength
Reference
```

Views describe what is read. Action modes describe how an Action gate may transform/carry the state after a Mirror/Action handoff.

```text
view packet
 -> Mirror-gate resolution
 -> one of A1/A2/A3
 -> optional Inward/Outward/Across/Over mode description
 -> consequence/new state
 -> next Mirror gate
```

There is no required one-to-one mapping between the four Views and the four Action modes.

## Recursive use

The same mode vocabulary may describe Action-gate consequences at multiple scales:

```text
local differential
 -> neighbor/path relation
 -> lattice field relation
 -> complete-system relation
```

The labels may remain stable while the physical mechanism changes by scale.

## Anti-drift rule

Reject any interpretation that says:

```text
Four Action modes = four primitive Action gates
```

or that adds these four modes to the three Action gates. The primitive count remains:

```text
A1 + A2 + A3 = three Action gates
M1 + M2 + M3 = three Mirror gates
three + three = six total gates
```

## Yellow audit

- The separation between four descriptive Action modes and three primitive Action gates is canonical.
- Exact mode selection and physical realization remain implementation-specific.
- Any hardware mapping must preserve the six-gate count and identify which of A1/A2/A3 performed the operation.
