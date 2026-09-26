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
