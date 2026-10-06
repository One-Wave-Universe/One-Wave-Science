# G-760 smooth Mirror basin result — 2026-10-04

Status: model-specific numerical progress; scientific gate remains YELLOW.
Reference commit: 5a6dba0e340edbe12b11b9fad682817ce7c68963.
Canonical donor nodes: G-757, G-760, G-762. This receipt does not alter their metadata.
Implementation: mirror_basin_scan.py. Raw receipt: mirror_basin_scan_receipt.json.

## Analytic boundary

For the phase-locked Gamma=0 branch, set ac=1 and
ar[k]=1+(C cos(2 pi k/6)+S sin(2 pi k/6))/3.
With eps=0, R=1 and x=0 exactly. Ring roughness and weave dipole penalties each
equal their coefficient times (C²+S²)/3. Define k=(bK+bT)/3.

Replace the legacy angular Mirror, explicitly and only in this experiment, by
M=aM S²+mu(C²+S²-m²)². Then the restricted energy is
E=k(C²+S²)+aM S²+mu(C²+S²-m²)².

For positive aM, mu and m:
- 2 mu m² <= k: C=S=0 is the minimum on this slice (critical equality has a soft C direction).
- 2 mu m² > k: C=±sqrt(m²-k/(2mu)), S=0 are the two minima on this slice.
- Positive amplitudes require the selected dipole radius to remain compatible with ar>0.

This is an exact restricted-energy identity, NOT a sufficient condition for every
full-model direction or coefficient. Cross coupling can destabilize directions
outside the slice. The numerical full-slice Hessian is therefore checked separately.

## Execution and outcome

Jetson direct terminal process 1179913, exit 0:
`OPENBLAS_NUM_THREADS=1 python3 -m unittest -v test_mirror_basin_scan`: 6/6 pass.
`OPENBLAS_NUM_THREADS=1 python3 mirror_basin_scan.py --output mirror_basin_scan_receipt.json`:
90 cases, 180 endpoint optimizations, 45 accepted stable pairs.

Grid: bK={0.1,0.4,1.0}; bT={0.05,0.2,0.8}; chi={0,0.05};
m=1; mu/mu_critical={0.5,0.9,1.1,2,5}. Other coefficients retain G-757 defaults.
Positive-amplitude bounds; pc=0 removes global phase. All six relative phases
are included in each 13x13 Hessian. Two difference steps: 1e-4 and 5e-5.
Acceptance requires optimizer success, gradient infinity norm <1e-5,
interior amplitudes, both minimum eigenvalues >1e-5 and opposite C signs.

| mu / critical | Cases | Accepted opposite-sign pairs |
|---|---:|---:|
| 0.5 | 18 | 0 |
| 0.9 | 18 | 0 |
| 1.1 | 18 | 14 |
| 2 | 18 | 18 |
| 5 | 18 | 13 |

Nine above-threshold cases were NOT accepted because one optimizer endpoint
reported ABNORMAL_TERMINATION_IN_LNSRCH, despite small residuals and positive
computed Hessians. These are unresolved optimizer statuses, not evidence that
the wells disappeared. No statuses were silently converted to success.

At bK=0.4, bT=0.2, chi=0.05, mu=0.2, m=1:
C≈±0.70710678, S≈0, E≈0.15.
Smallest physical-slice Hessian eigenvalue ≈0.126588 at both endpoints and both
step sizes. This establishes locally stable basins for this explicit experimental
energy, including cross-on stability. The cross coefficient is nonzero but its
energy contribution vanishes at these symmetric endpoints; E and Gamma also
vanish up to numerical regularization. Thus this does NOT satisfy the full
four-nonzero-interaction G-762 hold requirement.

## Protected baseline and limits

Legacy e4_seven_cell.py and all existing nodes were left unchanged.
Existing test_e4_seven_cell has 2 passes and 1 inherited failure:
test_symmetric_zero_dipole_and_circulation computes theta=1.8157749899 at a
nominally zero dipole, where the angular coordinate is undefined and floating
point cancellation selects an angle. Do not claim a green full baseline.
The opt-in smooth energy sums K/E/T/x directly, avoiding legacy angular M subtraction.

No NEB path or minimum global barrier established. No derived W, carry inertia,
R_G, physical mass, nonzero winding hold or second observable established.
The positive Hessians are finite-difference numerical evidence, not rigorous
global certificates. No patent/hardware validation is implied.

## Next permitted finish-line gate

Use the accepted endpoints for a separate barrier/path step, including alternative
S and phase escape routes and boundary controls. Then derive W independently,
compute dimensionless R_G and a second observable without retuning. Keep these
gates separate from this necessary basin-survival result.

Contribution: Codex, model-assisted derivation and software implementation; executed
on the user's Jetson through direct terminal. No successful external Field/Void
provider dialogue or OpenClaw execution is claimed.
