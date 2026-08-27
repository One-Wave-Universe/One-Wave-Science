---
node_id: "D-415"
canonical_name: "Nonlocal Three-Excitation One-Field Bench"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Numerical Simulation / Nonlocal Field Dynamics"
claim_gate_detail: "Runnable architecture validated for translation covariance and origin-free measurement; candidate potential and kernel remain underived"
metadata_standard: "I-06"
---

# D-415 — Nonlocal Three-Excitation One-Field Bench

**Planetary visual:**
`Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/planetary_visual.html` —
cinematic 16:9 Point–Path–Field projection with planetary scenes, nested wakes,
and a diffuse-to-spiral galactic arm-formation sequence, with direct 20-second
1080p WebM recording.

**Python video renderer:**
`Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/render_galaxy_video.py` —
browser-free deterministic spiral-arm animation rendered directly to H.264 MP4.

**Math-gap audit:**
`Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/sweep_math_gaps.py` and
`MATH_GAPS.md` — reproducible factor sweeps, ablations, refinement receipts,
and an explicit list of missing mathematical operators.

## Purpose

D-415 is the first runnable attack on a three-excitation problem using one
continuous Field rather than three point masses or three independently summed
potentials.  Extended structures are measured from the Field through windows;
the measured centers do not source pairwise forces.

## State and update

The current reduced state is one complex 2D Field `Psi`.  It advances through
a six-neighbor triangular-lattice wave operator, linear and nonlinear response,
and a strictly positive normalized global-reference kernel:

```text
Psi_next = Psi
         + (1 - gamma dt)(Psi - Psi_previous)
         + dt^2 [c^2 Laplacian_6(Psi)
                 - alpha Psi
                 - beta |Psi|^2 Psi
                 - kappa(Psi - K * Psi)]
```

`K * Psi` is a global reading of the same Field.  It is not the superposition
of independent body fields.  Every kernel entry is positive; there is no
hand-selected active radius or interaction cutoff.

## Measurements

Three Gaussian windows form a partition of unity and measure an energy-like
density.  Each measured center is

```text
q_k = integral(r W_k e) / integral(W_k e)
```

Field weights replace inserted point masses in the origin-free relational
coordinates.  The receipt records all three edge lengths, hyperradius,
hyperangle, relative shape cosine, measured phase, and Field weight.

Hyperradius alone is not treated as the full configuration.

## Dimensional discipline

- Native model: 2D triangular lattice.
- Coordination: six actual neighbors.
- Rendered dimension: none required by the batch bench.
- Omitted degrees: 3D volumetric motion and twelve-neighbor coordination.
- No `j +/- 5` or `j +/- 11` chain offset is used.

## Acceptance tests run

1. Constant fields have zero six-neighbor Laplacian.
2. The nonlocal kernel is strictly positive and normalized.
3. A common lattice translation commutes with the Field update.
4. Relational edge lengths and hyperradius ignore common translation.
5. A short numerical run remains finite.

The trace additionally records:

- odd-harmonic shared-node branches `H -> {2H+1, 2H+3}`;
- per-window phase and instantaneous frequency;
- three pairwise hysteretic phase-lock strengths;
- Field-current velocity and vorticity diagnostics;
- a candidate gradient-stress tensor diagnostic;
- separate internal Point, relational Path, and surrounding Field rotations;
- preliminary collision/merge, ejection, bounded-rotation, or unresolved class.

Passing these tests validates the implementation path only.  It does not
validate the candidate One-Wave law.

## Failure conditions and next work

The present law remains YELLOW because the potential and kernel are candidate
choices.  Promotion requires persistent translating excitations, a complete
Field energy/rotation ledger, reproducible capture or bounded three-excitation
motion, timestep/lattice refinement, and an independently specified test.

Next implementation targets:

1. derive the nonlinear potential and global kernel from canonical nodes;
2. derive a conserved Point–Path–Field transfer ledger;
3. strengthen capture, orbit, ejection, collision, Break, and Loop criteria;
4. implement native 3D twelve-neighbor geometry;
5. compare relational receipts with the Gray multipole control without
   inserting its point-mass mechanism into this solver.
