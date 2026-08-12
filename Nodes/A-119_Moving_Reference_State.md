---
node_id: "A-119"
canonical_name: "Moving Reference State"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Relational Primitive"
claim_gate_detail: "GREEN (definition and consequence for A-118) / no quantitative model of what moves the reference yet"
metadata_standard: "I-06"
---

# Node A-119: Moving Reference State

**Dependencies**
Upstream: A-118 Relational Differential Primitive
Downstream: A-125 Scale-Locality, C-327 Relational Acceleration Equation; also the Motion-Generated Background Differential and Dynamic Barycentric Reference backlog items (RELATIONAL_MECHANICS_NODE_BACKLOG.md)

## Definition

The reference used in A-118's `REFERENCE_SLOPE` term is not required
to be at rest. A-101 Ground/Zero establishes that *some* reference
state is required for measurement; this node adds that the reference
state itself may carry its own nonzero slope.

```text
REFERENCE_SLOPE(t) != 0 in general
```

Consequence: a local measurement (e.g. "Earth-bound" or "laboratory")
is not automatically stationary relative to whatever larger field or
body it is embedded in. Any laboratory frame is itself already a
moving reference relative to its own containing scale (Earth relative
to Sun, Sun relative to galactic structure), and A-118's CHANGE term
must account for that reference motion explicitly rather than assume
it away.

## Why This Matters Operationally

Without this node, A-118's `REFERENCE_SLOPE` defaults silently to
zero, which is only correct for a genuinely static reference (A-101's
Ground/Zero case). A-119 makes explicit that the reference term is a
real, generally nonzero input that must be supplied, not omitted by
default. This is what C-327 (Relational Acceleration Equation) and the
backlog's Dynamic Barycentric Reference item build on: the reference
itself has a source term.

## Scope

This node states that the reference can move and that this must be
represented explicitly. It does not yet derive *what* determines a
given reference's motion in general — that is left to the
scale-specific applications (A-125 Scale-Locality for the general
rule; C-327 for the two-body relational-acceleration case).

## Required Next Work

- A general rule for selecting which containing relation supplies the
  reference at a given scale (tracked as the Reference Selection Rule
  in RELATIONAL_MECHANICS_NODE_BACKLOG.md).
- At least one case where treating the reference as moving produces a
  different, checkable prediction than treating it as fixed.

## Failure / Revision Conditions

This node fails if a downstream calculation sets `REFERENCE_SLOPE = 0`
without stating that choice explicitly, or if "moving reference" is
used to explain away a discrepancy after the fact rather than being
specified before a calculation is run.
