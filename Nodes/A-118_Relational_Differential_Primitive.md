---
node_id: "A-118"
canonical_name: "Relational Differential Primitive"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Relational Primitive"
claim_gate_detail: "GREEN (operator definition and disambiguation from A-103) / YELLOW work (explicit update rule and boundary conditions) not yet built"
metadata_standard: "I-06"
---

# Node A-118: Relational Differential Primitive

**Distinct, do not merge** with A-103 Differential. See
`DUPLICATE_NAME_DISAMBIGUATION.md`.

**Dependencies**
Upstream: A-103 Differential, A-104 Gradient
Downstream: A-119 Moving Reference State, C-327 Relational Acceleration Equation; also the Differential Displacement State backlog item (RELATIONAL_MECHANICS_NODE_BACKLOG.md)

## Definition

```text
CHANGE = LOCAL_SLOPE - REFERENCE_SLOPE
```

A-103 defines the differential operator between two **states**:
`Δ(A,B) = A − B`. A-104 applies that same operator across **space**
(gradient). A-118 applies the identical differencing operator one
order up — between two **rates of change** (slopes), not two states:

```text
LOCAL_SLOPE     = the field's own rate of change sampled at the point of interest
REFERENCE_SLOPE = the rate of change of whatever containing relation that point is tracked against
CHANGE          = LOCAL_SLOPE - REFERENCE_SLOPE
```

This is the same relational move A-103 already makes (define a
quantity by subtraction against a reference rather than reading an
absolute value), applied to the derivative rather than the value
itself. It does not replace A-103; it is the specific operational form
A-119 (moving reference), the backlog's differential-displacement-state
item, and C-327 (relational acceleration) build on.

## Why This Is Not Just A-103 Again

A-103's Displacement specialization (A-102) is explicitly measured
against Ground/Zero — a fixed reference. A-118 exists because A-119
proposes the reference itself is allowed to move. Once the reference
moves, a bare state-level differential (A-103) silently mixes two
effects: the object's own change, and the reference's change. A-118
keeps them separated by operating on slopes so the reference's own
motion can be tracked and subtracted explicitly (see A-119, C-328
Common-Mode Field Cancellation) rather than accidentally absorbed into
the object's reported change.

## Worked Form

For a scalar or vector field quantity `ψ` sampled at position `x` and
a reference sampled at reference position `x_R`:

```text
LOCAL_SLOPE(x, t)     = dψ/dt |_x
REFERENCE_SLOPE(x_R,t)= dψ_R/dt |_{x_R}
CHANGE(x, t)          = dψ/dt |_x - dψ_R/dt |_{x_R}
```

If `x_R` is fixed (A-101 Ground/Zero, non-moving), `REFERENCE_SLOPE`
collapses to zero for a static reference field and A-118 reduces to an
ordinary time-derivative of A-103's differential — consistent, not
contradictory, with the existing A-series.

## Required Next Work

- An explicit update rule for how CHANGE feeds back into the next
  state (this node defines the operator, not yet the full recursive
  step).
- Boundary conditions: what happens when LOCAL_SLOPE and
  REFERENCE_SLOPE are sampled at different scales (see A-125
  Scale-Locality).
- At least one worked numerical example distinguishing A-118's output
  from a naive A-103 differential on the same data.

## Failure / Revision Conditions

This node fails if it is cited as replacing or superseding A-103, or
if CHANGE is computed without explicitly stating what supplied
REFERENCE_SLOPE.
