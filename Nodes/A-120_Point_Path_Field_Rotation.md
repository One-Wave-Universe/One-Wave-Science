---
node_id: "A-120"
canonical_name: "Point-Path-Field Rotation"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Relational Primitive"
claim_gate_detail: "GREEN (three-part state definition) / not yet cross-validated against a specific persistent-mode instantiation"
metadata_standard: "I-06"
---

# Node A-120: Point-Path-Field Rotation

**Dependencies**
Upstream: A-109 Inertial Memory, A-112 Persistent Mode, A-113 Projection
Downstream: the Nested Point-Path-Field Recursion, Translation Through Field vs Internal Rotation, 3:1 Point-Path-Field Coordination, and Point-Path-Field State Record backlog items (RELATIONAL_MECHANICS_NODE_BACKLOG.md)

## Definition

Every persistent structure (A-112) is tracked with three co-existing
descriptors instead of being reduced to a single point-particle
position:

```text
POINT  = the current localized state (position/orientation now)
PATH   = the accumulated history of how POINT arrived at its current state
FIELD  = the rotational/projected structure (A-113 Projection) the
         persistent mode maintains around itself while POINT and PATH evolve
```

A conventional point-particle description keeps only POINT and
discards PATH and FIELD as bookkeeping. A-120 requires all three be
tracked together, because A-109 Inertial Memory already establishes
that prior state persists through recursive change (PATH is not
disposable) and A-113 Projection already establishes that a Persistent
Mode's structure extends outward into the field (FIELD is not
optional either).

## Relation to Existing Motion Nodes

This does not introduce new motion mechanics. C-302 Momentum, C-306
Torque, and C-307 Angular Momentum already exist as applied mechanics
nodes. A-120's contribution is a **bookkeeping requirement**: any
simulation or node that models a persistent structure's motion should
carry POINT, PATH, and FIELD as separate tracked quantities rather
than collapsing PATH and FIELD into POINT for convenience. The
backlog's Translation Through Field vs Internal Rotation item is the
direct downstream consequence — POINT translating is not the same claim as
FIELD rotating internally, and conflating them is the specific error
this node exists to prevent.

## Worked Consequence

For a body with center-of-state `q(t)` (POINT), trajectory history
`{q(t') : t' < t}` (PATH), and internal rotational/projected structure
`θ(t), ω(t)` (FIELD, matching D-413's reduced shell state `Q(t) =
(q, q̇, θ, ω)`):

```text
translation only:      q̇ != 0, ω == 0
internal rotation only: q̇ == 0, ω != 0
combined:               q̇ != 0, ω != 0  (the general case)
```

D-413's existing bounded-shell simulation already carries exactly this
three-part state; A-120 names the general requirement D-413
instantiates as a special case.

## Required Next Work

- A formal statement of what "the same recursive structure at the next
  scale" means for PATH and FIELD specifically (deferred to the
  Nested Point-Path-Field Recursion backlog item).
- At least one case distinguishing a POINT-only model's prediction
  from a full POINT-PATH-FIELD model's prediction on the same input.

## Failure / Revision Conditions

This node fails if a node claims to use "Point-Path-Field Rotation"
while only tracking POINT, or if PATH/FIELD are tracked but never used
to change a downstream calculation.
