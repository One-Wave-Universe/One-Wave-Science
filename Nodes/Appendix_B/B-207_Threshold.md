---
node_id: "B-207"
canonical_name: "Threshold State"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node B-207: Threshold State

Dependencies:
Upstream: B-206 Paired Loop, B-206b Four Views, B-201 Equilibrium Balance
Downstream: B-208 Threshold Windows, B-209 Break Condition, B-210 Return,
B-216 Threshold Mathematics, G-702 Evaluation, G-703 Modulation

## Correction

The earlier scalar threshold `T in [0,100]` mixed together three different
properties:

1. how active the system is,
2. which direction it is leaning,
3. whether the relationship or loop remains intact.

Those are not the same variable. A low-energy state can be healthy rest, while a
high-energy state can remain coherent or become dangerous. Compression and
expression can occur at either high or low activation.

Threshold is therefore represented by a state vector rather than one score.

## Definition

For exchange step `n`, define

```text
Theta_n = (q_n, a_n, p_n)
```

where:

- `q_n in [0,1]` = coupling or loop integrity,
- `a_n in [0,1]` = total activation / available energy fraction,
- `p_n in [-1,1]` = polarity, with `-1` compressive and `+1` expressive.

The roles are independent:

```text
q answers: Is the loop still connected?
a answers: How activated is it?
p answers: Which way is it leaning?
```

A threshold region is a region in this three-variable state space.

## Relationship Rule

Threshold remains a property of the relationship or bounded operating loop, not
an intrinsic worth assigned to either participant.

For an individual-scale instance, `q` means internal coherence or retained
access between functions. For a paired system, `q` means connection integrity.
The mathematical role is the same; the scale-specific substrate must still be
stated under I-04.

## Projection Domain

All updates must remain inside

```text
Omega = [0,1] x [0,1] x [-1,1]
```

using the projection operator `Pi_Omega`. This guarantees that a numerical
update cannot create impossible values such as negative integrity or activation
greater than the normalized maximum.

## Operational Chain

```text
Paired Loop
-> Four Views
-> Threshold State (q,a,p)
-> Evaluation
-> Modulation
-> Return / Hold / Redirect / Break
```

## Yellow Result

The threshold concept is now mathematically separated into three variables with
explicit domains and testable meanings. The numerical locations of specific
operating bands remain calibration targets, but the architecture no longer
confuses low activation with broken access or compression with low energy.

## Yellow Audit

- Physical units are normalized; a hardware or biological instance must define
  what measured quantity maps to `a`, `p`, and `q`.
- The candidate numerical bands in B-208 are provisional and scale-dependent.
- The update law and stability conditions are in B-216.
- Experimental calibration is required before Bronze promotion.
