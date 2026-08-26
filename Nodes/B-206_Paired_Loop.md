---
node_id: "B-206"
canonical_name: "Paired Exchange / Paired Loop"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "GREEN (reciprocal paired-exchange definition) / YELLOW (threshold and physical realization)"
metadata_standard: "I-06"
---

# Node B-206: Paired Exchange / Paired Loop

Dependencies:
Upstream: B-201 Equilibrium Balance, B-202 Pressure, B-203 Expression, B-204 Compression, B-222 Oscillation Center
Downstream: B-206a Shared Boundary, B-206b Four Views, B-207 Threshold, B-215 Hyperloop, B-221a Six-Step Oscillator Program

## Core

A Paired Exchange is one reciprocal interaction carried by two complementary sides through a shared reference.

The two sides are not a sender and a receiver taking turns. Both sides participate at the same time.

## Definition

Each participant simultaneously:

- expresses;
- compresses;
- sends state;
- receives state.

Oscillation changes the relative phase, direction, or dominance of those complementary activities. It does not turn participation on for one side and off for the other.

The paired relation is the primitive object:

```text
A <-> B
```

with a shared reference `(0)`.

A one-way description may be used as an approximation only when the missing reciprocal path is explicitly justified by a boundary, constraint, coarse-graining step, or information loss.

## Balanced Three-Position Exchange

The local signed positions remain:

```text
-1   0   +1
```

A mirrored exchange can be written as:

```text
A: +1 -> 0 -> -1
B: -1 -> 0 -> +1
```

The two traces are one coupled exchange, not six independent instructions. Both sides pass through the same center/reference.

## Repeated Switching

The same paired relation can trade places repeatedly:

```text
(+1,-1) -> (0,0) -> (-1,+1)
(-1,+1) -> (0,0) -> (+1,-1)
```

The important invariant is reciprocal exchange through shared reference, not a fixed assignment of one side as Express and the other as Compress.

## Relationship to Expression and Compression

B-203 Expression and B-204 Compression remain distinct descriptive functions, but this node corrects the earlier implication that one participant expresses while the other only compresses.

Within a complete paired exchange, both functions are present on both sides. Their relative phase or strength may differ.

## Relationship to the Six-Pair Oscillator

B-221a uses six coupled logical pair positions. Each slash pair is simultaneous. B-206 supplies the reciprocity rule inherited by those pair positions.

The six-pair oscillator therefore must not be implemented as twelve unrelated serial one-way commands.

## Scale / Representation Boundary

The reciprocal structure may be instantiated at different scales, but scale examples are representations, not proof of universal physical scale invariance.

Candidate representations include:

```text
cell <-> cell
cluster <-> cluster
Field <-> Void processing regions
system <-> system
```

The invariant claim of this node is only the reciprocal paired-exchange structure.

## Operational Chain

```text
shared reference
-> paired reciprocal exchange
-> differential / phase relation
-> threshold or routing condition
-> continued exchange, crossover, or break
```

## Yellow Audit

- What physical mechanism realizes simultaneous send/receive and express/compress in the bench primitive?
- What determines the threshold for continued exchange versus break/crossover?
- Does the physical implementation preserve reciprocity under load and delay?
- What state variables are required to describe phase, direction, strength, and reference without collapsing them into one scalar?
- Under what conditions is a one-way approximation valid?
