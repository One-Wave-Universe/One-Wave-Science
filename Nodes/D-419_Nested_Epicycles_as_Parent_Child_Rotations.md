---
node_id: "D-419"
canonical_name: "Nested Epicycles as Parent-Child Rotations"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Geometry / Recursive Rotation"
claim_gate_detail: "GREEN kinematic composition / YELLOW physical interpretation"
metadata_standard: "I-06"
---

# D-419 — Nested Epicycles as Parent-Child Rotations

## Purpose

Use "epicycle" correctly as **nested real rotation**: child motion carried by parent motion.

This node rejects ad-hoc correction circles added only to fit observations.

## Recursive rotation chain

```text
body point rotation
-> local orbital/path rotation
-> stellar-system motion
-> galactic rotation/orbit
-> cluster motion
-> larger parent-field motion
```

Each level has an independently identifiable center/reference, path, and field.

## Kinematic composition

For child position in parent coordinates:

[
mathbf r_G
=
mathbf r_P
+
R_Pmathbf r_C.
]

For multiple nested levels:

[
mathbf r_G
=
mathbf r_0
+
R_0mathbf r_1
+
R_0R_1mathbf r_2
+cdots
]

and orientation composition is

[
R_{m total}=R_0R_1cdots R_n.
]

This is ordinary nested-frame mathematics.

## One-Wave interpretation

The active hypothesis is that the same Point -> Path -> Field rotation grammar applies at each level.

A child trajectory is therefore read relative to:
1. its own local point rotation;
2. its local path rotation;
3. the rotation/translation of each parent frame.

## Anti-retrofit rule

An epicycle is licensed only when the corresponding parent/child rotational level is physically identified independently of the fit.

Disallowed:
- inventing an extra circle because a trajectory misses data;
- assigning arbitrary frequency/phase solely to force agreement.

Allowed:
- composing measured planetary spin, orbit, stellar motion, galactic motion, cluster motion, or other real parent rotations.

## Link to gravity relay

D-419 supplies the rotation bookkeeping for D-418.

The relay state carries not only scalar position but the inherited orientation/rotation of each parent level.

## Failure condition

If nested rotations add no predictive value beyond standard coordinate transforms, classify D-419 as a useful representation only.

A novel claim requires a derived coupling between nested rotation and the physical lattice/field state.

## Nobel-readiness link

See `NOBEL_READINESS/MASTER_CHALLENGE_MAP.md`.
