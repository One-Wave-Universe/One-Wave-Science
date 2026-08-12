---
node_id: "D-421"
canonical_name: "Coherent Differential Accumulation"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Geometry, Resonance, and Simulation"
claim_gate_detail: "YELLOW (explicit summation form, consistent with standard secular-perturbation accumulation) / not yet evaluated numerically"
metadata_standard: "I-06"
---

# Node D-421: Coherent Differential Accumulation

**Dependencies**
Upstream: D-420 Resonant Phase Correlation, C-327 Relational Acceleration Equation, C-332 Relational Energy Transfer
Downstream: the Resonant Clearing Mode, Resonant Locking Mode, and Phase-Coherent Repeated Interaction backlog items (RELATIONAL_MECHANICS_NODE_BACKLOG.md)

## Definition

Across `N` successive encounters at phases `phi_1, phi_2, ..., phi_N`,
the net accumulated velocity change is the vector sum of each
encounter's individual differential kick (C-327/C-331's `u'_out -
u'_in` at that encounter):

```text
Delta_v_total = sum_{n=1}^{N} Delta_v(phi_n)
```

Under D-420's resonant condition (`phi_n` approximately constant or
slowly, monotonically advancing), successive `Delta_v(phi_n)` point in
similar directions, and the sum grows roughly linearly with `N`:

```text
|Delta_v_total| ~ N * |Delta_v_typical|      (coherent case)
```

## Why This Follows From D-420 Rather Than Being a New Assumption

`Delta_v(phi_n)` is a function of the encounter geometry alone (C-331's
scattering angle depends on approach phase and impact parameter). If
`phi_n` recurs (D-420), the same geometry recurs, so the same
`Delta_v` (up to slow drift) recurs — the vectors add rather than
average out. This is the same accumulation structure as driven
resonance in any linear or weakly nonlinear oscillator: a
phase-locked drive accumulates energy/momentum linearly in the number
of cycles, while a phase-random drive accumulates only as a random
walk (D-422).

## Worked Bound

If `Delta_v(phi_n)` varies smoothly with slowly drifting `phi_n` rather
than being exactly constant, the sum is bounded below by:

```text
|Delta_v_total| >= N * |Delta_v_typical| * cos(max phase drift per encounter)
```

which reduces to the linear-growth estimate above as the phase-drift
term goes to zero, and correctly predicts reduced (but still
super-random-walk) growth for a slowly precessing resonance.

## Required Next Work

- Numerically evaluate `Delta_v_total` for a real commensurability
  (e.g. a 2:1 Jupiter mean-motion resonance test particle) and compare
  the linear-growth estimate against the actual simulated accumulation.
- Explicit criterion connecting this node to the backlog's Resonant
  Clearing Mode item: how large must `Delta_v_total` become, relative
  to the local escape or libration-width scale, before clearing is
  expected.

## Failure / Revision Conditions

This node fails if accumulation is claimed as coherent (linear in `N`)
without first establishing D-420's phase-recurrence condition for the
specific case, or if the linear-growth estimate is used past the
regime where `Delta_v(phi_n)` can still be treated as approximately
constant across the accumulation window.
