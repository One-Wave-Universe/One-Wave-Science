---
node_id: "C-330"
canonical_name: "Moving Local Potential Perturbation"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Applied Mechanics and Boundary Structure"
claim_gate_detail: "YELLOW (standard patched-conic modeling assumption, restated relationally) / Gray-equivalent to established orbital mechanics, not yet a One-Wave-specific prediction"
metadata_standard: "I-06"
---

# Node C-330: Moving Local Potential Perturbation

**Numbering note:** originally drafted as C-326; renumbered to C-330.
See `RELATIONAL_MECHANICS_NODE_BACKLOG.md`.

**Dependencies**
Upstream: C-327 Relational Acceleration Equation, C-329 Actual State = Reference + Differential
Downstream: C-331 Relative Encounter Frame Transformation; also the Differential Gravity Assist backlog item (RELATIONAL_MECHANICS_NODE_BACKLOG.md)

## Definition

A moving mass such as Jupiter is represented as a localized deformation
travelling within the larger solar background field, rather than as an
independent field solved from scratch:

```text
Φ_total(x, t) = Φ_Sun(x) + φ_J(x - x_J(t))
```

`Φ_Sun` is the slowly-varying background potential (A-119's reference
term); `φ_J(x - x_J(t))` is the localized perturbation carried along
with Jupiter's own trajectory `x_J(t)`. This is C-329's
reference-plus-differential decomposition applied to a potential
field, with the differential term itself in motion.

## Gray Reference — This Is the Standard Patched-Conic Assumption

Representing a planet's gravity as a localized, moving perturbation on
a dominant central potential is the same modeling assumption
underlying the standard patched-conic approximation used throughout
mission-design orbital mechanics. This node makes no new physical
claim at this stage — it restates that standard assumption in A-118's
reference/differential vocabulary so C-331 and C-332 can be built from
it without silently re-deriving classical mechanics under a different
name.

## Why State It as a Node Anyway

The relational framing matters downstream: because `φ_J` moves with
`x_J(t)`, a body encountering it experiences a *time-varying* local
differential (A-118's `CHANGE`) even in a region where the background
`Φ_Sun` is nearly static. C-331's frame transformation and C-332's
energy-transfer result both depend on treating the encounter as
localized-perturbation-in-motion rather than as a fixed potential well
— the motion of `φ_J` itself is what allows a net energy exchange in
the Sun-centered frame (C-332), even though the encounter is
energy-conserving in Jupiter's own frame (C-331).

## Required Next Work

- State explicit validity bounds for the patched-conic split (sphere
  of influence, or equivalent) rather than leaving `φ_J`'s spatial
  extent implicit.
- Connect to A-115 (Unified Compression Field) if a One-Wave-specific
  form of `φ_J` is ever proposed in place of the standard gravitational
  potential; until then this node's `φ_J` is the Gray/Newtonian form.

## Failure / Revision Conditions

This node fails if it is presented as a novel One-Wave mechanism
rather than the standard patched-conic assumption restated relationally,
or if `φ_J` is treated as static once introduced, discarding the "moving"
part of its own name.
