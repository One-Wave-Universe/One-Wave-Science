# Nonlocal Three-Excitation Field Bench

`physics-atlas/index.html`'s "Bound Orbit" and "Three-Body Figure Eight"
scenes link back to this directory as their connected Node. That atlas is a
separate, self-contained cinematic scaffold (its own small toy integrator) --
it does not read this bench's actual state, equations, or receipts. This
README, `solar_system_control.py`, and the receipts these tests produce
remain the authoritative source for orbital/three-body claims.

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

## Real per-body spin/EM/parent-wake data (Updated 38-41 wiring)

`solar_system_control.py` now also carries, per body: real observed sidereal
spin (Point-rotation) periods, a `spin_orbit_ratio` diagnostic, and the
`HAS_GLOBAL_INTRINSIC_DIPOLE` control flags Updated 39/40 already require
(False for Venus, Mars, and the Moon; True for Mercury, Earth, and the giant
planets). These confirm, as data rather than assertion, that Mercury's 3:2
spin-orbit resonance and the Moon's synchronous lock are the real standard
gravitational/tidal control facts -- not evidence for a magnetic-lock
hypothesis for any of these bodies, including Uranus/Neptune (whose own
rotation is not solar-tide-locked at all; only some of their moons are
tidally locked to *them*, again by gravity).

`acceleration_receipt`/`step` gained a fourth named channel,
`external_parent_wake`: a one-way linear tidal-tensor form for an unmodeled
parent-scale mass distribution (Attack Map section K/M's Great Attractor ->
cluster -> galaxy -> star nesting). It is kept separate from
`one_wave_candidate` because an external parent field is legitimately
allowed to add net momentum to the modeled system (its source isn't
simulated), unlike an internal exchange among modeled bodies. It defaults to
the zero tensor: only the mathematical form is fixed here, not a calibrated
Milky-Way-tide value.

## Next gates

1. Derive the nonlinear potential and nonlocal kernel from canonical nodes.
2. Derive a conserved Point, Path, and Field rotation transfer ledger.
3. Demonstrate persistent translating excitations without a prescribed path.
4. Run capture, orbit, ejection, collision, Break, and Loop classifications.
5. Promote to 3D/12-neighbor geometry and compare against the Gray control.

The rotation observables and phase-lock state are implemented. A complete
conserved transfer ledger remains open because it depends on deriving the
canonical Field Lagrangian and nonlocal transfer law.
