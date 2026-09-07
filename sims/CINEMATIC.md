# Cinematic physics workbench

File: `sims/cinematic.html` — open locally in a modern browser; no build step.

This is a **micro-to-macro simulation and visualization workbench**. It deliberately separates numerical controls, exploratory toy models, and artistic overlays so cinematic presentation cannot promote a One-Wave claim.

## Current scale ladder

1. **Responsive Ground** — exploratory damped 2D scalar-wave grid with explicit evolving state and pulse perturbations.
2. **Spherical Flux** — analytic geometry control showing that conserved radial flux has density proportional to `1/r^2` because spherical area grows as `4*pi*r^2`.
3. **Bound Orbit** — equal-mass Newtonian two-body control using velocity Verlet, initialized at the normalized circular speed `v = sqrt(1/2)` and reporting energy, angular momentum, and total momentum.
4. **Three-Body Stress Test** — Newtonian equal-mass figure-eight control with calculated relational edges and the same conservation diagnostics.
5. **Galaxy Field** — reduced test-particle disk in a declared central potential. Self-gravity is not solved.
6. **Accretion -> Quasar** — Newtonian disk motion plus explicitly artistic jet/glow/lensing-style overlays. This is not a GR black-hole solver.

## Controls

- play / pause;
- reset;
- perturb current scene;
- time-scale control;
- trail persistence;
- relational-edge overlay;
- hypothesis-overlay switch;
- cinematic UI fade;
- CSV diagnostic export.

## Integrity lock

The hypothesis overlay is visual only in this build. Exported diagnostics explicitly record:

`solver_affects_hypothesis = false`

The candidate finite-wake / assimilation boundary is **not allowed to change trajectories** until an explicit update law and falsifiable boundary criterion are derived. No cutoff radius is inserted by hand.

The numerical control track therefore remains independent of One-Wave interpretation. A visually compelling result is not a success criterion.

## Validation target

Before promoting any speculative scene:

1. keep a standard control track;
2. declare the candidate One-Wave update separately;
3. emit machine-readable residuals;
4. sweep timestep and model parameters;
5. expose unstable and failed regions;
6. run ablations;
7. compare against accepted reference data or a higher-quality control solver;
8. only then consider whether the candidate law adds predictive content.

The current workbench is an expandable front end for that program, not evidence that the full One-Wave physical model is established.
