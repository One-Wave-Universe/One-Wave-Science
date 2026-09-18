# Physics Atlas scene map

The atlas is organized by scale, not by claim priority.

| Scale | Scene | Current role | Next quantitative upgrade |
|---|---|---|---|
| micro | Wave Packet | scalar-field toy | boundary sweeps, dispersion residuals, wave-packet benchmarks |
| micro | Coupled Oscillators | classical control | normal-mode spectrum, damping/drive sweeps |
| micro/control | Rotating Field | vector geometry control | RL/RLC winding model, phase error, torque proxy |
| bridge | Spherical Flux | analytic control | shell-flux residual plot and alternate dimensions |
| orbital | Bound Orbit | Newtonian control | Kepler elements, timestep convergence, perturbation sweeps |
| orbital | Three-Body Figure Eight | Newtonian stress test | finite-reach candidate family beside control, never inside it |
| stellar | Star / Corona | reduced scaffold | hydrostatic structure, energy transport, MHD/corona model |
| galactic | Galaxy Rotation | comparison scaffold | ingest observed rotation curves and fit competing laws |
| cosmic | Redshift Ladder | comparison scaffold | ingest standard-candle/BAO/SN data and compare model residuals |
| macro | Accretion / Quasar | artistic + simple dynamics | GR geodesic/MHD-backed renderer or clearly separated imported solution |

## One-Wave candidate-law gate

A One-Wave candidate may only affect a solver after these fields exist:

- state variables;
- update equation;
- parameters with units;
- initial/boundary conditions;
- conserved or expected quantities;
- prediction that differs from the control;
- falsification condition;
- comparison dataset or accepted benchmark.

Until then it stays overlay-only.
