# Gravity / Finite-Slope Proof Bench

This directory attacks the planetary finite-range and "sieve" logic from `UPDATED_38` through `UPDATED_41`.

The current bench is intentionally small. It does not try to simulate the whole Solar System before the boundary rule is logically sound.

## Current executable

`finite_slope_sieve_bench.py`

It runs two independent attacks:

1. **Finite-boundary attack**
   - tests an absolute parent-slope crossing;
   - tests a local differential/tidal crossing;
   - checks Earth/Sun against the lunar-orbit control;
   - checks whether a Hill-like boundary can be interpreted as a hard influence cutoff.

2. **Sieve / assimilation attack**
   - compares direct multi-source acceleration with a center-of-mass parent monopole;
   - measures relative acceleration error against the opening ratio `a/R`;
   - checks the expected quadratic far-field error when the center-of-mass dipole vanishes.

## Run

From the repository root:

```bash
python One_Wave_Bench/gravity/finite_slope_sieve_bench.py
```

Machine-readable receipt:

```bash
python One_Wave_Bench/gravity/finite_slope_sieve_bench.py --json
```

Tests:

```bash
cd One_Wave_Bench/gravity
python -m unittest -v test_finite_slope_sieve_bench.py
```

## Current result

The bench distinguishes three different ideas that had been getting mixed together:

| Idea | Current result |
|---|---|
| `local slope = absolute parent slope` defines finite boundary | **Rejected as general boundary** |
| `local slope = local differential/tidal reference` defines dominance boundary | **Works under inverse-square control** |
| dominance boundary means influence becomes zero | **Rejected** |
| distant explicit sources can be compressed into parent state | **Works under standard multipole control** |

For Earth relative to the Sun:

- absolute-background crossing: about `2.59e8 m`;
- lunar orbital radius: about `3.844e8 m`;
- differential/Hill-like boundary (`kappa=3`): about `1.497e9 m`.

So an absolute parent-slope comparison loses the Moon, while the local differential comparison produces a physically meaningful standard-control dominance scale.

But that dominance scale is **not** a force cutoff. The sieve interpretation that survives is:

`explicit local structure -> compressed parent representation -> reopen children when geometry/error requires it`

rather than:

`explicit local structure -> cutoff -> disappear`.

## Proof document

See:

`Internal_Proofs/08_Finite_Slope_Sieve_Boundary_and_Assimilation_Proof_Target.md`

That document contains the derivation, claim ledger, and the bridge requirement for a genuine One-Wave result.

## Build contract

### Purpose

Turn the finite-range hypothesis into a falsifiable numerical contract before building a full planetary simulator.

### Inputs

- source masses;
- source/target geometry;
- declared control law;
- boundary coefficient `kappa` for the control derivation;
- source-cluster geometry for compression tests.

### Outputs

- candidate boundary radii;
- balance residual;
- containment/control checks;
- opening ratio `a/R`;
- direct versus compressed acceleration residual;
- machine-readable claim status.

### Forbidden shortcuts

- no hand-selected AU cutoff presented as derived;
- no zeroing distant influence merely because local dominance ended;
- no planet-specific tuning to rescue a failed boundary;
- no visual-orbit success criterion;
- no promotion of Newtonian control math to proof of a One-Wave substrate.

### Acceptance rule

A candidate One-Wave boundary may replace the current standard-control derivation only when it is generated from a declared One-Wave field/update law and passes the same controls without per-body arbitrary coefficients.

## Next build

The next simulator should derive or import a candidate **Ground/lattice slope law** and run it through the exact same boundary/compression interface. That is the shortest path from the current architecture to a genuinely independent proof attempt.
