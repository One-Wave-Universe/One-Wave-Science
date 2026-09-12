# One-Wave Physics Atlas

`physics-atlas/` is the expansion zone for the cinematic physics program. It is intentionally separate from `sims/`, which remains the smaller baseline workbench and validation entrypoint.

Open `index.html` directly in a modern browser. No build step is required.

## Current scenes

| # | Scene | Role | Connected Node |
|---|---|---|---|
| 1 | Wave Packet | damped 2D scalar-wave toy | not yet connected |
| 2 | Coupled Oscillators | classical coupled oscillator control | not yet connected |
| 3 | Rotating Field | three phase-shifted vectors and rotating resultant | not yet connected |
| 4 | Spherical Flux | inverse-square geometry control | not yet connected |
| 5 | Bound Orbit | Newtonian two-body Verlet control | `D-415` — `Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/solar_system_control.py` (the Gray control this scene's toy integrator stands in for) |
| 6 | Three-Body Figure Eight | Newtonian three-body stress test | `D-415` — `Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/` (the actual candidate three-excitation bench; this scene is a fixed classical figure-eight, not that bench) |
| 7 | Star / Corona | reduced stellar transport/corona scaffold | `G-715` — `Nodes/G-715_Stellar_Boundary_Reversal_Bench/` (the actual control-vs-hypothesis boundary-release test; this scene is cinematic only) |
| 8 | Galaxy Rotation | Kepler-like versus flat-curve comparison scaffold | no dedicated bench yet; nearest theoretical context is `C-323`/`A-115`, neither of which is a runnable rotation-curve comparison |
| 9 | Redshift Ladder | normalized wavelength-shift comparison scaffold | `E-528` — `Nodes/E-528_Static_Redshift_Transport.md` (the actual propagation law; this scene is a generic sine-stretch visual, not that law) |
| 10 | Accretion / Quasar | central-potential disk with clearly artistic macro overlays | not yet connected |

Every scene's side panel now shows its `Node:` line at runtime (see `index.html`'s `nodeLink` field), linking to the file above when one exists. This is a link, not a data feed: the canvas here runs its own small, self-contained toy code and does **not** import the Node's actual state, equations, or receipts. A scene tagged CONTROL or TOY/SCAFFOLD stays a visual stand-in for its Node until it is wired to read that Node's real output; do not read scene diagnostics here as if they were the Node's own results.

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
