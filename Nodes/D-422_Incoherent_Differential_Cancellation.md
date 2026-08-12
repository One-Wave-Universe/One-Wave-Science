---
node_id: "D-422"
canonical_name: "Incoherent Differential Cancellation"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Geometry, Resonance, and Simulation"
claim_gate_detail: "YELLOW (standard random-walk bound, consistent with non-resonant perturbation theory) / not yet evaluated numerically"
metadata_standard: "I-06"
---

# Node D-422: Incoherent Differential Cancellation

**Dependencies**
Upstream: D-420 Resonant Phase Correlation, C-327 Relational Acceleration Equation
Downstream: the Resonant Locking Mode and Phase-Decoherent Repeated Interaction backlog items (RELATIONAL_MECHANICS_NODE_BACKLOG.md)

## Definition

D-421's accumulation sum

```text
Delta_v_total = sum_{n=1}^{N} Delta_v(phi_n)
```

behaves differently when `phi_n` drifts to become effectively
uniformly distributed (D-420's non-resonant case) rather than
recurring. If each `Delta_v(phi_n)` is treated as an independent draw
with fixed magnitude `|Delta_v_typical|` and phase uniformly
distributed, the expected net magnitude grows as a random walk rather
than linearly:

```text
E[|Delta_v_total|] ~ sqrt(N) * |Delta_v_typical|      (incoherent case)
```

with the mean vector sum trending toward zero (`E[Delta_v_total] -> 0`
as the phase distribution approaches uniform) even though individual
encounters are not weak.

## Why This Matters as the Companion to D-421

Without D-422, D-421's coherent-accumulation claim would have no
contrast case, and "resonance drives large cumulative change" would be
untestable — any accumulated change could be attributed to resonance
regardless of whether the phase condition actually held. D-422 gives
the null hypothesis: a body undergoing many strong but phase-random
encounters should show `sqrt(N)` growth, not linear growth, and not
systematic directional drift. A simulation claiming resonant
accumulation must show growth exceeding this `sqrt(N)` bound, not
merely show growth.

## Worked Consequence

The ratio of coherent to incoherent expected accumulation after `N`
encounters is:

```text
(N * |Delta_v_typical|) / (sqrt(N) * |Delta_v_typical|) = sqrt(N)
```

so the coherent/resonant case becomes increasingly distinguishable
from the incoherent case as more encounters are included — this gives
the backlog's Resonance Detector item a concrete, growing signal-to-null
ratio to test against rather than a fixed threshold.

## Required Next Work

- Confirm the `sqrt(N)` scaling numerically for a non-resonant test
  particle under repeated Jupiter encounters, as the explicit null
  case for D-421's linear-growth claim.

## Failure / Revision Conditions

This node fails if a case showing growth consistent with `sqrt(N)`
scaling is described as resonant, or if D-421's coherent case is
validated only by failing to also check the D-422 null case on the
same data.
