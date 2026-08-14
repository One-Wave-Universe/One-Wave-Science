# D-415 Planetary Point-Path-Field Simulation

Open `index.html` in a modern browser for the state-driven results viewer, or
re-run the engine yourself:

```
cd Nodes/D-415_Planetary_Point_Path_Field_Simulation
python3 simulate_d415.py --out results
```

`--duration YEARS` overrides the default 30-year run (all other parameters
live in `Params` at the top of `simulate_d415.py`). A full default run takes
several minutes on a single core; there is no live browser physics engine
here (see "Why a static viewer" below).

## What this tests

UPDATED_41 (`UPDATED_41_PLANETARY_SCALE_DISPLACEMENT_MODEL.md`) proposes that
a planet is a persistent planetary-scale displacement structure rather than a
point mass with a bolt-on magnetic correction. That document is a locked
candidate architecture, not code. D-415 implements one scoped, falsifiable
slice of it and runs it under D-412 discipline: declared state evolves under
a reproducible update law, and the **Newtonian control**, the **1PN
(post-Newtonian) control**, and the **candidate One-Wave model** are run from
identical initial conditions and integrator tolerances (spec layer 8) — never
reconstructed after the fact from different code paths.

The full node write-up, the exact update law, the required measurements, and
the failure conditions are in `../D-415_Planetary_Point_Path_Field_Simulation.md`.
Read that first.

## Quick summary of scope

Real, non-candidate physics: an N-body Newtonian integrator for the Sun and
five planets (Mercury, Venus, Earth, Mars, Jupiter), plus the textbook 1PN
correction term.

Candidate, under test: a small bounded multiplicative correction `K_eff` to
the Sun-body gravity term, built from prescribed internal-rotation shear, a
declared EM-alignment proxy (dynamo bodies only — Venus and Mars are explicit
no-dynamo controls), and a relaxing 2D compression state `C_i`. `K_eff` is
checked to stay within `|K_eff - 1| < 1e-3` of pure Newtonian gravity in
every run — it is a perturbation to be tested, not a replacement for gravity.

## Explicit non-applicability

Some D-412-required test categories are lattice-scale concepts that do not
apply to point-mass N-body gravity, and are declared out of scope rather than
forced into a meaningless test:

- **no-well ablation** — D-413's imposed curvature well is a Ground-lattice
  concept; there is no imposed well here, gravity itself is the real N-body
  Newtonian field.
- **FCC vs HCP local stacking** — a D-409 3D close-packed lattice concept.
- **cell area** — no lattice cells exist at point-mass scale.
- **periodic/random/simple-control lattices** — the analog control at this
  scale is the Newtonian-only run itself, which the engine already reports.

## Numerical-precision caveat on the precession measurement

The perihelion-precession diagnostic uses the instantaneous osculating
eccentricity-vector angle (the Laplace-Runge-Lenz direction), computed
exactly from the integrated position and velocity at every sample -- no
periapsis-passage detection or interpolation involved. It is still a
numerical diagnostic, not an ephemeris-grade propagation, and near-circular
orbits (Venus, Earth) have a small, poorly-directed eccentricity vector, so
their precession estimate is noisy by physical construction, not by a bug.
Every run includes a half-timestep (`dt_refine_half`) case specifically so
the receipt can report whether the estimate is converging — check
`measurements.dt_convergence_relative_change` in `results/d415_summary.json`
before treating any precession number as more than a rough comparison
between the three models. As a sanity check, the 1PN control's Mercury
excess over the Newtonian control is compared against the known measured GR
value (~42.98 arcsec/century, Clemence 1947) — this validates the 1PN
implementation itself, not the candidate correction.

## Why a static viewer

`index.html` renders the precomputed `results/d415_summary.json` and CSV
time series — it does not re-run physics in the browser. D-413's live
JavaScript lattice engine and this engine are different code paths; keeping
one canonical Python engine as the single source of truth (matching the
`One_Wave_Bench` pattern used for D-413) avoids a second, unaudited
implementation of the same update law.

## Honesty boundary

D-415 does not derive an internal planetary dynamo, an absolute active
range, kilograms, a GR replacement, or the full nine-part recursive
Point-Path-Field state UPDATED_41 declares. It does not claim to match
observed planetary ephemerides — its held-out test compares the candidate
model against this engine's own Newtonian control, not against independent
ranging data. See the `limitations` array in every generated
`d415_summary.json` for the complete, current list.
