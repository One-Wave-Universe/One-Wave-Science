---
node_id: "C-328"
canonical_name: "Common-Mode Field Cancellation"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Applied Mechanics and Boundary Structure"
claim_gate_detail: "YELLOW (algebraic consequence of C-327) / not yet tested against a case with a genuinely large common-mode term"
metadata_standard: "I-06"
---

# Node C-328: Common-Mode Field Cancellation

**Numbering note:** originally drafted as C-324; renumbered to C-328.
See `RELATIONAL_MECHANICS_NODE_BACKLOG.md`.

**Dependencies**
Upstream: C-327 Relational Acceleration Equation
Downstream: C-329 Actual State = Reference + Differential; also the Common-Mode Rejection backlog item (RELATIONAL_MECHANICS_NODE_BACKLOG.md)

## Definition

Split each body's local acceleration into a shared background term and
a body-specific residual:

```text
S_i = S_common + s_i'
S_j = S_common + s_j'
```

Substituting into C-327:

```text
d̈_ij = S_i - S_j = (S_common + s_i') - (S_common + s_j') = s_i' - s_j'
```

`S_common` cancels exactly. The relative motion of `i` and `j` depends
only on the *difference* of their residual accelerations, never on
whatever background acceleration they share.

## Why This Is Not Trivial Bookkeeping

The physical content is that a background acceleration common to both
bodies — for example, the Sun-galactic-center acceleration shared by
both the Earth and the Moon — cannot show up in Earth-Moon relative
motion no matter how large it is, as long as it is genuinely common to
both. This is the same principle as a differential amplifier's
common-mode rejection (the backlog's Common-Mode Rejection item),
applied to acceleration rather
than voltage, and it is also the direct justification for A-119's
claim that a moving reference does not by itself break local
measurement: if the reference's motion is common-mode to the bodies
being compared, it cancels; only the residual (A-118's `CHANGE`) is
measurable locally.

## Worked Consequence

This gives a concrete criterion for the backlog's Motion-Generated
Background Differential item: a "background displacement/pressure term" from
continual motion through the proposed lattice can only affect local
relative dynamics through its *gradient* across the two bodies being
compared, i.e. through `s_i' - s_j'`, never through its bulk value. Any
claim that a uniform background motion directly alters local relative
motion contradicts this node and must be rejected or must show the
background is not actually uniform across the compared bodies.

## Required Next Work

- A numerical case with a large, explicitly nonzero `S_common` (e.g.
  the Sun's galactic-orbital acceleration) confirming Earth-Moon
  relative motion is unaffected to the precision the case can resolve.
- Connect explicitly to the Common-Mode Rejection backlog item once
  it is developed, so the same cancellation language is used for the
  electronics and orbital-mechanics applications rather than two
  independent statements.

## Failure / Revision Conditions

This node fails if a downstream calculation attributes a local
relative-motion effect to a background term without first showing that
background term is *not* common-mode between the two bodies being
compared.
