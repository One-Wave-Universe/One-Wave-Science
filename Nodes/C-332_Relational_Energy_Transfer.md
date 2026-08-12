---
node_id: "C-332"
canonical_name: "Relational Energy Transfer"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Applied Mechanics and Boundary Structure"
claim_gate_detail: "YELLOW (standard gravity-assist energy formula, restated relationally) / Gray-equivalent to established orbital mechanics"
metadata_standard: "I-06"
---

# Node C-332: Relational Energy Transfer

**Numbering note:** originally drafted as C-328; renumbered to C-332.
See `RELATIONAL_MECHANICS_NODE_BACKLOG.md`.

**Dependencies**
Upstream: C-331 Relative Encounter Frame Transformation
Downstream: D-421 Coherent Differential Accumulation; also the Differential Gravity Assist backlog item (RELATIONAL_MECHANICS_NODE_BACKLOG.md)

## Definition

```text
ΔK = V_J . (u_out - u_in)
```

The change in a body's kinetic energy (per unit mass), measured in the
Sun-centered frame, across a close encounter with a moving perturber
of velocity `V_J`, equals the perturber's velocity dotted with the
change in the body's Sun-frame velocity.

## Derivation

Starting from C-331's frame transform, `u = V_J + u'`, kinetic energy
per unit mass in the Sun frame is `K = (1/2)|u|^2`. The change across
the encounter:

```text
ΔK = (1/2)|u_out|^2 - (1/2)|u_in|^2
   = (1/2)(u_out - u_in) . (u_out + u_in)
```

Substitute `u_out = V_J + u'_out`, `u_in = V_J + u'_in`:

```text
u_out - u_in = u'_out - u'_in
u_out + u_in = 2V_J + u'_out + u'_in
```

so:

```text
ΔK = (1/2)(u'_out - u'_in).(2V_J + u'_out + u'_in)
   = V_J.(u'_out - u'_in) + (1/2)(|u'_out|^2 - |u'_in|^2)
```

By C-331, `|u'_out| = |u'_in|` (elastic in the perturber's frame), so
the second term vanishes exactly:

```text
ΔK = V_J . (u'_out - u'_in)
```

Since `u_out - u_in = u'_out - u'_in` (the constant `V_J` cancels in
the subtraction), this is equivalently:

```text
boxed: ΔK = V_J . (u_out - u_in)
```

which holds whether the velocity difference is evaluated in the Sun
frame or the Jupiter frame.

## Physical Reading

Kinetic energy is exchanged with the perturber's own translational
motion, not created. The body gains (or loses) energy in the
Sun-centered frame exactly to the extent its Sun-frame velocity change
has a component along the perturber's own velocity `V_J`. A perturber
at rest (`V_J = 0`) produces `ΔK = 0` in the Sun frame regardless of
how strongly it deflects the body — consistent with C-331's finding
that the encounter is elastic in the perturber's own (here, coincident
with the Sun's) frame.

## Gray Reference

This is the standard patched-conic gravity-assist energy-change
formula used in mission design (the basis of powered/unpowered
slingshot maneuvers); C-332 adds no new physics, only the relational
derivation chain (C-329 to C-331) that produces it from A-118's
primitives.

## Required Next Work

- The backlog's Differential Gravity Assist item: restate this result
  as "emergent relational path bending" rather than a separately
  posited force — the remaining conceptual step the backlog calls for.
- A numerical check of this formula against a real patched-conic
  gravity-assist case (e.g. a documented Voyager or Galileo flyby) as
  a Gray-comparison sanity check.

## Failure / Revision Conditions

This node fails if `ΔK` is computed without both `u_out` and `u_in`
being evaluated in the same frame, or if the formula is applied to a
non-elastic encounter (e.g. one involving atmospheric drag) without
adding the corresponding dissipative correction.
