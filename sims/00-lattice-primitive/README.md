# Stage 00 — Lattice Primitive

This is the true bottom of the One-Wave science simulation stack.

## Primitive

The primitive is **not a cell and not a particle**.

It is one local lattice degree of freedom with:

- reference / equilibrium
- signed displacement
- amplitude
- phase
- orientation / direction
- local frequency
- coupling to neighbors
- retained local history
- energy / excitation measure
- scale index

A cell is a later organized structure made from many coupled lattice sites.

## First hierarchy

1. **Lattice site**
   - one local oscillatory state

2. **Coupled lattice**
   - nearest-neighbor interaction
   - wave propagation
   - standing modes
   - defects
   - vortical circulation
   - octave scaling

3. **Stable localized structures**
   - candidate knots / loops / vortices
   - tested for persistence and conservation

4. **Proton-knot hypothesis layer**
   - represent a proton-like object as a candidate stable knot/loop only as a One-Wave hypothesis
   - compare its simulated observables against proton measurements
   - do not assume the knot is real until benchmarks pass

5. **Quark-vortex hypothesis layer**
   - represent quark-like substructure as candidate nested or coupled vortical modes
   - compare against collider observables
   - retain CERN reconstruction labels only as reference metadata

6. **ATP / biochemical energy layer**
   - ATP is not a primitive lattice object
   - model ATP as a higher-scale energy-transfer cycle built from lower-scale field interactions
   - use measured chemistry/biophysics data and energy scales as validation targets

## Scientific boundary

The simulator may test:
- whether stable knot-like modes emerge
- whether nested vortices reproduce measured collider patterns
- whether larger-scale energy-transfer cycles can be represented from lower-level dynamics

It must not hard-code those outcomes.

## Canonical path

LATTICE SITE
→ COUPLED LATTICE
→ WAVE / PATH / FIELD
→ STABLE LOOP / KNOT / VORTEX
→ PROTON-LIKE / QUARK-LIKE HYPOTHESIS TESTS
→ CHEMICAL / ATP ENERGY-TRANSFER TESTS
→ larger physics and biology

## Octave scaling

For scale index n:

scale(n) = 2^n

Frequency, amplitude, and geometry scaling are separate controls.

Raw or measured reference data are never overwritten by scaled views.

## First executable G-766 control

Run the bounded dispersion and octave fixtures with:

```bash
cd sims/00-lattice-primitive
python3 -m unittest -v test_dispersion_octave_fixture.py
python3 dispersion_octave_fixture.py
```

The fixture derives the six-neighbor triangular-lattice symbol, compares the
continuous-time analytic frequency with the finite-timestep leapfrog
frequency, and checks exact-octave and non-octave detector controls. Its JSON
receipt keeps `a_num` numerical, refuses a physical lattice-spacing claim,
and does not treat sampling rate as measured signal frequency.

## Reusable numerical kernel and guard

`lattice-kernel.js` exposes `LatticeKernel.advance(sites, parameters, dt, forces)`
and `LatticeKernel.measure(sites, parameters, circulationRing)` in the browser,
or the same API through CommonJS in Node. Site state is `{x, v, phase, n}`;
`n` is a reciprocal neighbor-index array. Parameters are `frequencyHz`,
`coupling`, `damping` (ζ), and `nonlinearity` (λ), all finite and nonnegative,
with strictly positive frequency. Coordinates, displacement, coupling and energy
remain numerical quantities; frequency labels do not establish a physical lattice scale.

The original kick-then-drift symplectic Euler equation is unchanged. Each requested
interval uses adaptive internal substeps satisfying `h sqrt(K) <= 0.25` and
`h gamma <= 0.25`, where `K = omega² + 2 maxDegree J + 3 lambda max|x|²`
and `gamma = 2 zeta omega`. The stiffness bound is checked again against each
candidate state; a failed candidate halves the trial step. This is a local
numerical guard, not a global nonlinear stability theorem or an accuracy claim.

A requested interval is atomic: `advance` never mutates the supplied state.
Nonfinite input/state/energy or more than 4096 trials rejects the entire interval.
The UI pauses with the error, retains the last valid state, and does not advance
the rejected replay sample. Reduce parameters or reset, then resume explicitly.
No clamping or silently replaced state is used. Parameter changes restart the
energy reference, because the previous energy is no longer a conservation baseline.

GWOSC samples are held constant through internal substeps. Original samples and
4096 Hz source cadence are unchanged; numerical subdivision does not create new
measurements. Solver receipts expose the requested interval, subdivisions and
trial budget. Zero-state phase coherence remains 1 by the existing phase
convention, not evidence of an oscillating coherent wave.

Run the focused checks without dependencies:

```sh
node --test sims/00-lattice-primitive/test_lattice_kernel.js
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s sims/00-lattice-primitive -p 'test*.py' -v
```

Tests cover an analytic oscillator, bounded undamped numerical energy, damping,
timestep refinement, extreme UI frequency, nonlinear drive, atomic refusal,
37-site/90-edge topology, actual GW input samples and UI event integration.
These checks do not complete the G-764 falsification list, spatial convergence,
nonlinear confinement, physical calibration or browser visual-quality review.
