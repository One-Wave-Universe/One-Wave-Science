# G-715 Bench: Boundary-Release Two-Layer Toy Model

This directory is the first runnable bench for Node
`G-715_Stellar_Boundary_Reversal.md`, addressing its section 13
("Test / Simulation direction") and Yellow Audit item 5 ("Need
simulation showing stable condition where T_cor > T_s from boundary
energy deposition").

## What this bench is

A two-compartment, deterministic ODE toy in **arbitrary model units**,
not measured solar parameters. It compares two modes:

- `control` — the two layers are linked only by ordinary conduction.
  Conduction can only move heat from hot to cold, so this mode is the
  naive "core hot -> surface cooler -> outer atmosphere cooler"
  expectation from G-715 section 2. It cannot produce `T_cor > T_s`
  at steady state.
- `hypothesis` — a fraction of the interior input bypasses the dense
  surface layer as a release channel (standing in for magnetic
  tension / wave transport) and is deposited directly into the thin
  outer layer, per G-715's `Hold -> Fold -> Release -> Heat -> Flow`
  chain.

## Run

```bash
python3 boundary_release_bench.py
python3 -m unittest -v test_boundary_release_bench.py
```

Sample output:

```text
[control   ] T_s=   33.98  T_cor=   33.15  T_cor>T_s=False  steady=True  energy_balance_residual=-1.5e-09
[hypothesis] T_s=   27.83  T_cor=  140.75  T_cor>T_s=True   steady=True  energy_balance_residual=-7.2e-09
```

## What this establishes

- The boundary-release mechanism described in G-715 is
  **thermodynamically self-consistent**: a steady state exists where
  the thin outer layer is hotter than the dense boundary layer, energy
  is conserved (`energy_in - energy_out - energy_stored ~ 0`), and the
  reversal strengthens monotonically with the release fraction rather
  than appearing only at one arbitrary parameter setting.
- The control case, using the same two-compartment structure but only
  ordinary conduction, cannot produce the reversal regardless of how
  strongly the layers are coupled (`test_control_never_reverses_across_conduction_strengths`).
  This rules out "the two-compartment structure itself trivially
  produces a reversal" as the explanation.
- Setting `release_fraction = 0.0` collapses hypothesis mode back to a
  non-reversing case, confirming the release channel — not some other
  hidden asymmetry between the two loss terms — is what does the work.

## What this does NOT establish (honest limits)

- This is not a solar model. Units are dimensionless; no attempt is
  made to match real photosphere (~5800 K) or corona (~1-3 MK)
  temperatures, real solar flux, or real radiative-loss physics.
- `k_rad_s`, `k_rad_cor`, `k_wind`, and `release_fraction` are chosen
  to have the qualitative shape G-715 argues for (dense layer =
  strong radiative coupling, thin layer = weak radiative coupling);
  they are not derived from magnetic reconnection, Alfven-wave, or
  turbulence microphysics, and are not fit to any observation.
- It does not distinguish reconnection heating from MHD/Alfven-wave
  heating from turbulent heating — all three are lumped into one
  scalar `release_fraction`.
- It says nothing about magnetic switchbacks (G-715 section 8).
- It does not prove the Sun uses this mechanism. It shows the
  mechanism is not thermodynamically self-contradictory and that a
  toy version of it behaves the way G-715 claims it should, under a
  control that could have falsified it and did not.

## Status

Node `G-715` remains **YELLOW**. This bench answers one Yellow Audit
item (a toy stability demonstration) and leaves the rest — deriving
the conversion rule from real MHD/reconnection physics, separating
the three heating-candidate contributions, connecting to switchbacks,
and any quantitative comparison to real solar data — open, as listed
in G-715 section 14.
