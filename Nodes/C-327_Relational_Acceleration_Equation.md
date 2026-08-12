---
node_id: "C-327"
canonical_name: "Relational Acceleration Equation"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Applied Mechanics and Boundary Structure"
claim_gate_detail: "YELLOW (standard relative-acceleration identity, re-derived in A-118/A-119 relational language) / not yet run as a numerical simulation"
metadata_standard: "I-06"
---

# Node C-327: Relational Acceleration Equation

**Numbering note:** this node was originally drafted as C-323 and was
renumbered to C-327 because C-323–C-326 were already committed to the
One-Wave Intrinsic Cell hardware nodes. See
`RELATIONAL_MECHANICS_NODE_BACKLOG.md`.

**Dependencies**
Upstream: A-118 Relational Differential Primitive, A-119 Moving Reference State, C-314 Three Frames of Reference
Downstream: C-328 Common-Mode Field Cancellation, C-329 Actual State = Reference + Differential; also the Differential Gravity Assist and Tidal/Gradient Difference backlog items (RELATIONAL_MECHANICS_NODE_BACKLOG.md)

## Definition

For two bodies `i` and `j` with position states `x_i(t)`, `x_j(t)` and
relative-position state `d_ij = x_i - x_j`:

```text
d̈_ij = S_i - S_j
```

where `S_i` and `S_j` are each body's own local field-sourced
acceleration (A-118's `LOCAL_SLOPE`, taken as the acceleration each
body actually experiences from the ambient field it sits in).

## Derivation

This is the standard identity for relative acceleration, restated in
A-118's relational vocabulary rather than introduced as a new physical
law:

```text
d_ij = x_i - x_j
ḋ_ij = ẋ_i - ẋ_j
d̈_ij = ẍ_i - ẍ_j = S_i - S_j
```

For a field sourced by a potential `Φ`, `S_i = -∇Φ(x_i)` and
`S_j = -∇Φ(x_j)`, so:

```text
d̈_ij = -[∇Φ(x_i) - ∇Φ(x_j)]
```

This is exactly a finite-baseline tidal/gradient-difference term (see
the backlog's Tidal/Gradient Difference item): the relative acceleration
between two bodies depends
on the *difference* of the field gradient at their two locations, not
on the absolute field value at either location alone. Where `Φ` is
Newtonian gravitational potential, this reduces to ordinary
differential/tidal gravity — this node does not claim a new force, it
claims that A-118's relational-differencing operator applied to
acceleration reproduces the standard tidal term, which is the required
consistency check before any relational reinterpretation is trusted.

## Why This Matters for the Relational Program

C-327 is the load-bearing check for the whole relational-mechanics
backlog: if `d̈_ij = S_i - S_j` did not reduce to the standard tidal
acceleration under a Newtonian `Φ`, the relational reformulation would
already be wrong at the two-body level, before any wake, resonance, or
scale-locality claim could be trusted. It does reduce correctly, so
the reformulation is at minimum consistent (Gray-equivalent) at this
level.

## What This Node Does Not Yet Claim

It does not yet claim a source for `S_i`, `S_j` beyond "each body's own
local field-sourced acceleration" — i.e. it does not yet derive `Φ` (or
its One-Wave equivalent, A-115's Unified Compression Field) from first
principles. It also has not been run as an actual numerical
integration; the identity above is algebraic, not a simulated result.

## Required Next Work

- Substitute a specific `S_i` (Newtonian `Φ`, or a One-Wave
  compression-field candidate from A-115) and integrate `d̈_ij`
  numerically for a known two-body case as a sanity check against
  Kepler orbits (Gray comparison).
- C-328's common-mode cancellation test, which depends directly on
  this node's `S_i - S_j` form.

## Failure / Revision Conditions

This node fails if `d̈_ij = S_i - S_j` is used with `S_i`, `S_j` sourced
inconsistently (e.g. one Newtonian, one One-Wave) without declaring
that mismatch explicitly, or if it is cited as deriving a new force
rather than restating the standard relative-acceleration identity in
relational language.
