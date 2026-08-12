---
node_id: "C-331"
canonical_name: "Relative Encounter Frame Transformation"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Applied Mechanics and Boundary Structure"
claim_gate_detail: "YELLOW (standard Galilean frame transform, restated relationally) / Gray-equivalent to established orbital mechanics"
metadata_standard: "I-06"
---

# Node C-331: Relative Encounter Frame Transformation

**Numbering note:** originally drafted as C-327; renumbered to C-331
because C-327 was reassigned to Relational Acceleration Equation. See
`RELATIONAL_MECHANICS_NODE_BACKLOG.md`.

**Dependencies**
Upstream: C-314 Three Frames of Reference, C-330 Moving Local Potential Perturbation
Downstream: C-332 Relational Energy Transfer; also the Differential Gravity Assist backlog item (RELATIONAL_MECHANICS_NODE_BACKLOG.md)

## Definition

A body's encounter state during a close pass by a moving perturber
(C-330's `x_J(t)`, velocity `V_J`) is transformed between two frames:

```text
u  = velocity in the Sun-centered (background) frame
u' = velocity in the Jupiter-centered (perturber) frame
u' = u - V_J          (Galilean transform, constant V_J over the encounter)
```

## Why the Perturber Frame Is the Useful One

In the Jupiter-centered frame, the encounter with a purely
gravitational, time-independent local potential (C-330's `φ_J`,
approximately static over the short encounter duration) conserves
kinetic energy by symmetry — an elastic scattering event. The
incoming and outgoing speeds relative to Jupiter are equal; only the
direction changes:

```text
|u'_in| = |u'_out|,   u'_out = R(χ) u'_in
```

where `R(χ)` is a rotation by the scattering angle `χ` determined by
the approach geometry and `φ_J`'s strength. This holds in Jupiter's
frame precisely because C-330 treats `φ_J` as (locally, over the
encounter) static — the same frame in which the perturbation itself is
at rest.

## Transforming Back

The Sun-frame velocities before and after are recovered by adding
`V_J` back (this is C-329's reference-plus-differential identity
applied to velocity):

```text
u_in  = V_J + u'_in
u_out = V_J + u'_out
```

Kinetic energy is **not** conserved in this frame, because `V_J` is a
different constant added to a rotated vs. unrotated relative velocity.
This apparent asymmetry — conserved in one frame, not conserved in the
other — is exactly the structure C-332 turns into a usable energy-
transfer formula.

## Gray Reference

This is the standard patched-conic frame transform used in mission
gravity-assist design; no new physics is claimed here, only the
restatement needed to connect C-330's moving-perturbation picture to
C-332's energy result.

## Required Next Work

- State the sphere-of-influence / encounter-duration bound under which
  treating `V_J` as constant and `φ_J` as static-in-its-own-frame is
  valid (inherits the same open item from C-330).

## Failure / Revision Conditions

This node fails if kinetic energy is claimed to be conserved in the
Sun-centered frame during the encounter, or if the elastic-scattering
result `|u'_in| = |u'_out|` is applied in the Sun-centered frame rather
than the Jupiter-centered frame where it actually holds.
