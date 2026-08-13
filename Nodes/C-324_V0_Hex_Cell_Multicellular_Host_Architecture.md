---
node_id: "C-324"
canonical_name: "One-Wave V0 Hex Cell — Multicellular Host Architecture"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "PROPOSED_BUILD"
classification: "Engineering / Applied Hardware Node"
claim_gate_detail: "YELLOW (architecture and proof checklist defined) / no organelle has yet passed the V0 proof list"
metadata_standard: "I-06"
---

# Node C-324: One-Wave V0 Hex Cell — Multicellular Host Architecture

BOUNDARY STATEMENT (read first): this is a proposed hardware
architecture for a six-organelle-plus-coordinator host cell. It makes
no claim that the design is built, tested, or biologically accurate.
It proposes an engineering target to build and test, per I-05 Proposed
Build.

**Dependencies**
Upstream: A-101 Ground/Zero, B-201 Equilibrium Balance, B-205 Mirror, C-301 Mirror Gate, C-311 Electric/Magnetic Duality, C-323 Primitive Continuous Mirrored Chain
Lateral: C-312 Hierarchical Sensor-Control Architecture (Android Body), C-315 Wave Reader V1
Downstream: C-325 One-Wave V0-A Intrinsic Cell Engineering Architecture, C-326 One-Wave V0 Intrinsic Cell First-Organelle Build Wiring, Books/Engineer_The_Future/Vol1/Ch06

## Purpose

C-324 is the multicellular scaling target for the single-organelle
intrinsic cell defined in C-325 and built in C-326: a coordinator plus
six logic/memory organelles plus one mitochondria power organelle,
arranged in a hex ring, with dual-rail balanced-ternary state and
five-level modulation.

## Core

```text
dual active reference rails (VA / VB)
shared relational center (CB)
ternary: -1 / 0 / +1
five modulation levels:
  Ceiling (+2)
  High    (+1)
  Middle  (0)
  Low     (-1)
  Floor   (-2)
```

Choice determines direction. Modulation determines how strongly the
state is maintained.

## Motion

```text
DC  -> Point Rotation
AC  -> Path/Oscillation Rotation
RFC (Rotating Field Current) -> Field Rotation
```

**Correction:** this section previously read "RC (Rotational Current)."
RFC is the intended term (Rotating Field Current), confirmed as
intentional, not a typo for RC.

**Recursion note (not merged):** "recursion" here means the
Point -> Path -> Field structure can occur again inside, or at, the
next scale — not a relabeling of this section. That is the same claim
the backlog's Nested Point-Path-Field Recursion item makes in the
abstract A-series vocabulary (see RELATIONAL_MECHANICS_NODE_BACKLOG.md).
Candidate I-04 disposition: **Scale-Specific Instance** — this
DC/AC/RFC triad would be the physical/circuit-scale instantiation of
that general recursive structure, not a duplicate of it. This is a
candidate reading only; the two are not merged here, and remain
separately addressable until the backlog item is developed enough to
check the mapping term-by-term.

## Reinjection

Sense phase, amplitude, and magnetic state. Inject only enough energy
to replace losses and preserve the existing rotational state. This is
the same intrinsic phase-synchronous reinjection rule formalized in
C-325 (`INJECT = LOSS_REQUEST AND PHASE_MATCH`).

## Multicellular Host

```text
1 Coordinator
6 Logic/Memory organelles
1 Mitochondria power organelle
```

**Coordinator**
- dual-reference rails
- timing
- oversight
- phase coordination

**Logic organelles**
- ternary polarity
- modulation
- phase
- local memory
- path preference

**Mitochondria**
- maintain magnetic memory state
- phase-synchronous reinjection
- replenish losses
- preserve stored orientation
- never rewrite memory during maintenance

## Hex Cell Layout

```text
        N1 ---- N2
      /            \
    N6      C       N3
      \            /
        N5 ---- N4
```

States: clockwise, hold, counterclockwise.

## V0 Proof Checklist

1. Stable dual-reference center
2. Reliable ternary state
3. Five modulation levels
4. Rotational circulation
5. Magnetic memory retention
6. Phase-synchronous reinjection
7. Neighbor-to-neighbor state transfer

None of these seven items has a recorded pass result yet. C-325
records a behavioral (non-hardware) simulation of items 1-3 and 6;
C-326 is the first buildable single-organelle wiring toward a physical
pass. Items 4, 5, and 7 require the multi-organelle ring this node
describes and are open.

## Failure / Revision Conditions

C-324 fails if:

- a hex-ring build is attempted before a single organelle (C-326)
  passes its own test plan (C-325 docs/04_TEST_PLAN.md);
- the coordinator is treated as a conventional CPU rather than another
  One-Wave cell specialized for shared reference and phase
  coordination;
- any of the seven V0 Proof items above is marked passed without a
  recorded, reproducible measurement.
