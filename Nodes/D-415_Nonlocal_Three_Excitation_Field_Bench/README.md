# Nonlocal Three-Excitation Field Bench

This directory contains the first runnable One-Wave three-excitation bench.
It advances one complex nonlinear Field on a periodic 2D triangular lattice,
uses a strictly positive global kernel, and extracts three extended excitation
measurements without inserting point masses or pairwise force laws.

`planetary_visual.html` is the cinematic 16:9 visual companion. It provides
Sol–Earth–Moon, Mercury/Sol EM-coupling, Venus rotational-mismatch, nested
solar-wake, and emergent spiral-arm scenes. The galactic scene starts with a
diffuse rotating stellar population, builds harmonic trails, thins their outer
length, and transfers locking toward a next-arm mode. The canvas records a 20-second 1080p WebM directly for
video production. It is a state-architecture projection, not validation.

## Run

```bash
python nonlocal_field_bench.py --steps 300 --output run_output
python -m unittest -v test_nonlocal_field_bench.py
python sweep_math_gaps.py
python -m http.server 8000
```

Open `http://localhost:8000/planetary_visual.html` for the video interface.

For a browser-free Python MP4 render:

```bash
python render_galaxy_video.py --output galaxy_arm_formation.mp4
```

The Python renderer streams RGB frames directly into `ffmpeg` and produces a
20-second 1080p H.264 video by default.

The run produces `three_excitation_trace.csv` and `summary.json` containing
Field-derived centers, weights, phases, relational edges, hyperradius,
hyperangle, and shape cosine.

The receipt also includes harmonic phase/frequency, hysteretic pair-lock state,
Field-current velocity, vorticity, a candidate gradient-stress diagnostic, and
separate Point, Path, and Field rotation measurements for each excitation.

## Model

The discrete update is

```text
Psi_next = Psi
         + (1 - gamma dt)(Psi - Psi_previous)
         + dt^2 [c^2 Laplacian_6(Psi)
                 - alpha Psi
                 - beta |Psi|^2 Psi
                 - kappa(Psi - global_reference(Psi))]
```

`Laplacian_6` uses the six actual neighbors of a triangular lattice.  Six is
a coordination count, not the one-dimensional offset `j +/- 5`.  The global
reference is a normalized convolution over the one Field.  Its kernel is
strictly positive, so no arbitrary interaction cutoff exists.

Three measurement windows form a partition of unity.  They measure extended
Field regions and update their centers from an energy-like density.  The
centers are observables, not dynamical point particles.  Jacobi-like
relational coordinates use measured Field weights rather than inserted mass.

## Honest limits

- YELLOW experiment: the nonlinear potential and global kernel are candidate
  equations, not derived or experimentally validated laws.
- The current implementation is 2D/6-neighbor.  A later 3D implementation
  must use twelve actual volumetric neighbors rather than a 1D offset.
- The three seeded excitations are not yet proven persistent modes.
- This bench tests numerical architecture: one Field, global connection,
  extended measurement, translation covariance, and origin-free outputs.
- It does not claim a solution to the celestial three-body problem.

## Next gates

1. Derive the nonlinear potential and nonlocal kernel from canonical nodes.
2. Derive a conserved Point, Path, and Field rotation transfer ledger.
3. Demonstrate persistent translating excitations without a prescribed path.
4. Run capture, orbit, ejection, collision, Break, and Loop classifications.
5. Promote to 3D/12-neighbor geometry and compare against the Gray control.

The rotation observables and phase-lock state are implemented. A complete
conserved transfer ledger remains open because it depends on deriving the
canonical Field Lagrangian and nonlocal transfer law.
