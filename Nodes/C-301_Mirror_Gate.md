---
node_id: "C-301"
canonical_name: "Mirror Gate"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Applied Mechanics and Boundary Structure"
claim_gate_detail: "Implementation crossover is canonical; scale-specific physical origin remains open"
metadata_standard: "I-06"
---

# Node C-301: Mirror Gate

## Definition

The Mirror Gate is the shared-reference crossover event/boundary between two opposed sides of one relational oscillator.

In the canonical state-machine notation:

```text
F1/V6 - V5/F2 - F3/V4 - V3/F4 - F5/V2 - V1/F6 - ...
```

- `/` means **one simultaneous mirrored pair state**. It is not a serial gate separator.
- `-` means the **Mirror Gate crossover**: the opposed oscillations return toward their shared reference `(0)`, meet/cross, phase-shift, and emerge in the next alternating orientation.

The engine begins from the shared middle/reference `-(0)+`, not from an isolated serial `F1` instruction.

## Six Logical Pair Positions

The invariant logical sequence is:

```text
F1/V6
 -
V5/F2
 -
F3/V4
 -
V3/F4
 -
F5/V2
 -
V1/F6
 -
F1/V6 ...
```

Dynamic orientation alternates:

```text
F/V -> V/F -> F/V -> V/F -> F/V -> V/F
```

The twelve labels are the two sides of six coupled pair positions, not twelve independent serial instructions.

## Current VTC Physical Interpretation

The current hardware design uses **three physical Mirror Gates**, each traversed in two orientations/phases, to express the six logical pair positions.

```text
3 physical Mirror Gates x 2 orientations = 6 logical pair positions
```

This is an engineering interpretation to be validated by the VTC bench program; it is not claimed as a universal physical count at every scale.

## Local Crossover Sequence

```text
mirrored peak/trough relation
 -> return toward local reference
 -> meet at (0)
 -> cross
 -> phase shift / handedness update
 -> next mirrored pair orientation
```

The new consequence can become the reference/input for the next relation.

## Across and Over

From `B-206c`:

```text
Across = establish/carry the relation through the shared reference/boundary.
Over   = complete the crossover/phase shift and emerge in the next orientation.
```

## Physical-Hardware Boundary

A VTC implementation may use linked opposed switching elements, magnetic coupling, differential sensing, or another physical mechanism. The Mirror Gate node defines the relational crossover; it does not assume one specific material implementation.

## Yellow Audit

- Slash/dash notation and crossover semantics are implementation-canonical.
- The three-physical-gate VTC realization requires bench validation.
- Claims that the same physical mechanism explains quantum, atomic, biological, collider, or cosmological behavior remain separate hypotheses and are not established by the compute architecture alone.
