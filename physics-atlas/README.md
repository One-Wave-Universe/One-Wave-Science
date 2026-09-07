# One-Wave Physics Atlas

`physics-atlas/` is the expansion zone for the cinematic physics program. It is intentionally separate from `sims/`, which remains the smaller baseline workbench and validation entrypoint.

Open `index.html` directly in a modern browser. No build step is required.

## Current scenes

1. Wave Packet — damped 2D scalar-wave toy.
2. Double-Slit Interference — two coherent sources on a damped lattice (illustrative), checked against an exact closed-form two-source path-length calculation compared to the textbook paraxial formula Δy = λL/d.
3. Coupled Oscillators — classical coupled oscillator control.
4. Rotating Field — three phase-shifted vectors and rotating resultant.
5. Spherical Flux — inverse-square geometry control.
6. Bound Orbit — Newtonian two-body Verlet control, with live Kepler elements (semi-major axis, eccentricity, period) derived from the vis-viva/angular-momentum relations.
7. Three-Body Figure Eight — Newtonian three-body stress test.
8. Star / Corona — reduced stellar transport/corona scaffold.
9. Galaxy Rotation — Kepler-like versus flat-curve comparison scaffold.
10. Redshift Ladder — normalized wavelength-shift comparison scaffold.
11. Accretion / Quasar — central-potential disk with clearly artistic macro overlays.

## Scientific separation

Every scene is tagged as one of:

- **CONTROL** — an established mathematical or classical-physics control model;
- **TOY / SCAFFOLD** — useful for testing structure or comparison but not a full physical solver;
- **ARTISTIC** — cinematic representation only.

The UI can show a One-Wave hypothesis overlay, but the exported diagnostics record:

`solver_affects_hypothesis = false`

That is a hard rule until a candidate law is written explicitly and can be falsified.

## Expansion rule

New physics should be added here as a separate scene/module with:

1. declared equations or algorithm;
2. baseline/control model;
3. parameters and units;
4. measurable outputs;
5. residuals or conservation diagnostics where applicable;
6. failure and instability exposure;
7. machine-readable export;
8. explicit statement of what is artistic, reduced, or unproven.

Do not let cinematic appearance count as evidence.
