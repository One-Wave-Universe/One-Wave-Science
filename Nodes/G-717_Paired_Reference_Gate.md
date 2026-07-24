---
node_id: "G-717"
canonical_name: "Paired Reference Gate"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Evaluation, Control, and Route Grammar"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node G-717: Paired Reference Gate

# G-717 Paired Reference Gate

Naming note: this node was previously titled "Mirror Gate," colliding
with C-301 Mirror Gate. Resolved in C-301's favor — C-301 has real
upstream (B-205 Mirror) and downstream (C-308 Spin-half) dependencies;
this node has never been cited by anything else in the corpus and its
own Dependencies section uses concept names rather than real node IDs.
Renamed rather than merged, since the content (bidirectional paired-
reference crossing with a commit condition) is real and distinct from
C-301's spin/topology framing — it just needed a name that doesn't
claim to be the primitive.

Appendix: G — Evaluation / Modulation / Validation  
Node Type: Function Node  
Role: Bidirectional crossing through shared middle  

---

## Dependencies

- Two References
- Shared Middle
- Paired Exchange
- Pair Response / Commit Condition

NOTE: these remain concept names, not real node IDs — this was already
flagged before the rename and is unchanged by it. Resolving this into
actual upstream/downstream node citations is separate, still-open work.

---

## Core

A Paired Reference Gate is a bidirectional wavegate operating between two reference positions through a shared middle.

---

## Definition

A Paired Reference Gate operates on paired references.

Every exchange:

- begins at one reference,
- crosses the shared middle `(0)`,
- reaches the paired reference,
- returns through the shared middle,
- oscillates about the shared middle.

The middle is the common reference point for both directions of travel.

---

## Base Grammar

```text
A(0)B
B(0)A
```

---

## Fundamental Pair

```text
1(0)-1
-1(0)1
```

---

## Working Progression

```text
1(0)-1   -1(0)1

↓
1(0)-2   -2(0)1

↓
2(0)-2   -2(0)2

↓
3(0)-3   -3(0)3

↓
4(0)-4   -4(0)4

↓
5(0)-5   -5(0)5
```

---

## Operational Rule

A Paired Reference Gate is valid only when both directions share the same middle.

```text
A → 0 → B
B → 0 → A
```

The crossing is not one-way.

The return is part of the gate.

No return means no completed Paired Reference Gate.

---

## Pair Response

Each side responds to the other through the shared middle.

```text
A(0)B + B(0)A
```

The paired response creates the complete gate cycle.

---

## Commit Condition

A Paired Reference Gate commits only when the paired exchange completes both directions.

```text
A(0)B
B(0)A
```

If only one side occurs, the gate remains incomplete.

---

## Function

The Paired Reference Gate allows the system to compare, reverse, and validate paired movement across a shared reference middle.

It supports:

- bidirectional evaluation,
- paired correction,
- modulation across reference sides,
- validation through return crossing,
- oscillation about shared middle.

---

## Appendix G Placement

Paired Reference Gate belongs in Appendix G because it is an evaluation/modulation/validation function.

It defines how paired references cross, return, and validate through a common middle.

---

## Proof State

YELLOW.

The base grammar is defined.

The paired exchange is defined.

The shared middle is defined.

The unresolved proof item is the separate Pair Response / Commit Condition rule.

Until that rule is fully separated and validated, Paired Reference Gate remains YELLOW.

---

## Operational Chain

```text
Two References
↓
Shared Middle
↓
Paired Exchange
↓
Paired Reference Gate
↓
Pair Response
↓
Commit Condition
↓
Validation
```

---

## Notes

Paired Reference Gate does not belong in every appendix.

Paired Reference Gate belongs in Appendix G as a validation gate.

The math and number progression must remain intact.
