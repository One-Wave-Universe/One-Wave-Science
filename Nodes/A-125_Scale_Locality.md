---
node_id: "A-125"
canonical_name: "Scale-Locality"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Relational Primitive"
claim_gate_detail: "GREEN (rule statement and B-220 cross-reference) / no simulation has tested whether locally inherited state actually reproduces a global-lookup result"
metadata_standard: "I-06"
---

# Node A-125: Scale-Locality

**Dependencies**
Upstream: A-118 Relational Differential Primitive, A-119 Moving Reference State, B-220 Scale Layer
Downstream: the Finite Wake Assimilation, Multi-Body Edge Network, One-Wave Relational Solver Rule, Reference Selection Rule, and Relational Nonlocality Theorem Target backlog items (RELATIONAL_MECHANICS_NODE_BACKLOG.md)

## Definition

A node representing structure at a distant location is not permitted
to read that location's global/absolute state directly. It must
instead be represented through the **locally inherited state and
boundary conditions of the scale layer that actually contains it**:

```text
distant structure's local representation
    = f( containing scale's local boundary state,
         containing scale's local reference slope (A-119) )
```

not

```text
distant structure's local representation = direct_lookup(global_state)
```

This is the relational analogue of B-220 Scale Layer's requirement
that meaning be preserved across Micro→Small→Medium→Large→Macro: B-220
requires the *interpretation* to survive the scale change; A-125
requires the *data access pattern* used to compute that interpretation
to stay local at every scale, never reaching directly into a distant
scale's raw state.

## Why This Is a Distinct Claim From "Just Use Local Variables"

The nontrivial part is not "compute locally" — it is that the locally
available boundary state must, in principle, already carry everything
the distant structure's influence would otherwise require, because
that boundary state was itself built by the same local-differencing
process one scale down. A-119's moving reference is the mechanism that
makes this plausible: if every scale's reference already carries its
containing scale's slope, then a scale-locally computed quantity is
not blind to the larger structure — it inherited that structure's
state through the reference term, not through a lookup.

## Worked Form

For nested scales `s=1 (Moon), s=2 (Earth), s=3 (Sun)` (see the
backlog's Nested Wake Capture item):

```text
REFERENCE_SLOPE at scale s = LOCAL_SLOPE inherited from scale s+1's
                              own A-118 computation at scale s+1
```

i.e. Earth's reference slope (as seen by the Moon) is Earth's own
local slope relative to the Sun, not a separately fetched "Earth's
absolute state." This chains A-118 through B-220's scale layers rather
than treating each scale as an isolated lookup table.

## What This Node Does Not Yet Claim

It does not yet claim that this local-inheritance scheme reproduces
the same numerical result as a direct global calculation (e.g. a
standard N-body integrator with full pairwise gravitational terms).
That equivalence is an open, testable question — tracked as the
backlog's Relational Nonlocality Theorem Target and Wake vs Potential
Numerical Equivalence Test items — not an assumed conclusion.

## Required Next Work

- The Reference Selection Rule (backlog): the general procedure for
  choosing which containing relation supplies a given scale's reference.
- A minimal two-scale numerical test comparing scale-local inheritance
  against direct global lookup on identical initial conditions.

## Failure / Revision Conditions

This node fails if "scale-locality" is invoked to justify skipping a
distant interaction entirely rather than representing it through an
inherited boundary state, or if the local/global equivalence is
asserted without the comparison test above having been run.
