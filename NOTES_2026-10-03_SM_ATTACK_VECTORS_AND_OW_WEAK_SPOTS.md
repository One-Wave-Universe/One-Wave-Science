# Notes — SM attack vectors and One-Wave joints to solidify

**Date:** 2026-10-03  
**Status:** working note. Not a node. Not a Brick promotion.  
**Does not override:** C-318, C-322, Updated 24/26/46, G-745, G-757 through G-768, `ONE_WAVE_SCIENCE_ATTACK_MAP.md`, `Nodes/G-728_Mathematics_Attack_Laundry_List.md`.  
**Rule:** the Standard Model still wins the spreadsheet until one fixed `E4` and `W` produce a dimensionless gate ratio and one second observable with no retune. This page is the queue.

Sources for the charge sheet: `Nodes/G-761_SM_Assumption_Smash.md`, `Nodes/C-322_Mirror_Gate_Higgs_Scale_Resonance.md`, `Nodes/C-318_Mass_Mechanism_Candidate_Resolution.md`, `Nodes/G-760_Micro_First_Attack_Mirror_Term.md`.

---

## 1. Attack vectors on the Standard Model

Hit the joint the SM does not derive. Do not hit a measured number.

### AV-1 — Primary. Yukawa write-in

SM fermion masses are inserted:

```text
m_f = y_f * v
```

`v` is one vacuum number. Each `y_f` is a free coupling. The scalar is unprotected, so the hierarchy (why `v` is electroweak, not Planck) is also inserted. The measured self-coupling then sits near vacuum metastability. That is a fit of a spectrum, not a derivation of one.

One-Wave counter, already written, not yet numeric:

- Mass Effect is carried four-interaction hold, `M_ij = d^2 E4 / dv_i dv_j` at rest. C-318. Not `V''(v)`.
- 125 GeV is Mirror-Gate work `E_MG = E4(q_G) - E4(q_0)`, not "the Higgs mass." C-322. And `m_eff != E_MG / c^2`.
- The only non-circular first number is

```text
R_G = E_MG / (m_eff * v_lat^2)
```

from one coefficient set. Then either predict 125 from an independent micro anchor, or calibrate on 125 and predict one other mass or the width. Not both. G-761.

### AV-2 — Do not attack the 125 GeV peak

The collider number stays. C-322 is Green as interpretation and empirical anchor, Yellow as a derivation. Denying the peak loses the argument before the mechanism is tested.

### AV-3 — Do not attack with zone-edge `a0`

G-745 and Updated 46 quarantine this. Under `c_eff = c`,

```text
a0_edge ≈ 5e-18 m
```

about a thousand times smaller than a nucleon. Forcing `a0 ~ 1 fm` smuggles in `c_eff / c ~ 2e-3`. Hoyle 7.654 MeV must not ingest that length and call itself blind.

### AV-4 — Do not attack "four forces are fake" before the cross term lives

G-761 and G-762: gauge groups may be Gray shadows of knot / shell / Mirror / weave. They are not a trophy. Zeroing `E_x` reimports the SM split. Cross stays on or the smash is fake.

### AV-5 — Secondary, empirical. Spectrum versus independent Yukawas

If masses are unrelated `y_f`, a shared scale-phase across a measured spectrum should not beat matched nulls. That test is G-767, and it has not been run. A failure against the nulls kills the lattice reading. It is not evidence "hidden by the conventional names."

Handshake, do not collapse:

- G-766 generates dispersion / octave structure from the lattice without fitting peaks.
- G-767 measures scale phase in real spectra without assuming the lattice.
- Compare only after both sides are frozen.

### AV-6 — Parked. Real SM gaps, wrong first strike

| Gap | Why it waits |
|---|---|
| Gravity absent from SM | G-728 H1 Newtonian control is not built. No `delta_a_OW` until Gray orbits recover. |
| Neutrino mass | Book 1 Ch8 exists. No fixed update predicts the splittings. |
| Cosmology / redshift | E-533 timing law is an unverified recovery target. Fit is not mechanism. |
| Three generations | `2 x 3 = 6` is bookkeeping prior to `SU(n)`. It is not a derived generation count. G-761 §7. |
| Color | QCD labels in G-736 are an overlay. Topological color on the seven-cell is not derived. |

---

## 2. One-Wave weak spots that must be solidified

These are the joints that currently make AV-1 a charge sheet instead of a hit. Ordered by what blocks the hit.

### W1 — Blocker. Two Mirror wells do not survive the weave

`Nodes/G-760_Micro_First_Attack_Mirror_Term.md`. Yellow.

| Form | Result |
|---|---|
| `E_M = alpha * sin^2 theta` | Singular at vanishing dipole. G-757 receipt. |
| `E_M = alpha * S^2` | Smooth. One valley. Both seeds relax to `S = 0`, `E = 0`. NEB is flat. |
| `E_M = alpha * S^2 + mu * (C^2 + S^2 - m^2)^2` | Should pin `C = ±m`. On the seven-cell the weave (`beta_K`, `beta_T`) flattens the ring. Relaxed state `C = 0`, `S = 0`. Barrier ~ 0. |

G-762 names this failure mode exactly: weave wins, Mirror dipole dies, no second basin.

**Do not misread** `Nodes/G-757_HESSIAN_RECEIPT.md` (2026-09-06). That receipt says a *seeded finite dipole* under `sin^2 theta` is locally positive-semidefinite after quotienting global phase (`n_negative = 0`). It also says the connecting path and saddle were not computed, and that `C = S = 0` under `sin^2 theta` is a coordinate singularity (`O(1e9)` eigenvalues), not a physical saddle. Local PSD of a seed is not basin survival under descent. G-760 is the later result. Descent kills the wells.

**Work, do not skip:**

1. Scan `mu` against `beta_T` and `beta_K`. Keep only the region where two relaxed minima hold `|C| > 0` and opposite sign.
2. Hessian at both minima, physical slice only (global phase quotiented).
3. Only then NEB and a saddle with one negative mode.
4. Only then `W` and Mass Effect.
5. Proton-knot observables last.

If no coefficient set keeps two wells, G-757 has no gate on this graph and C-322 has no path to integrate. Say that. Do not retune the words.

### W2 — Work metric `W` is not derived, so GeV cannot come out

C-318 Green as mechanism identity. Yellow as profiles, coefficients, and spectrum. G-728 F1–F5 unchecked.

The update has a global scale freedom: `W -> lambda W` multiplies both `M_ij` and `E_MG` and does not move the trajectory. That is a no-go for kilograms or GeV from the current parameterization. It is not a failure of persistence.

Until `W` is derived from the discrete update (positive-semidefinite, off-diagonal blocks kept), the only legal target is `R_G`. Absolute scale is F5, and it must not be borrowed from G-745.

### W3 — One rule has not yet made both light and mass

C-318 open item: a gapless traveling mode with `M ≈ 0`, and a bounded recurrent hold with nonzero carried-pattern response, from the same update. G-761 §6. Still open. Do not give the photon a second passport to paper over the gap.

Damping is not mass. `C_ij v_j` is drag. Folding it into `M` trips the C-313 preferred-frame conflict. G-728 E1, E4, E5 still open: exact damped roots, Lorentz honesty, error bounds on any emergent invariant.

### W4 — Octave / 2× scale is not established

- G-766: six-neighbor dispersion and octave tests are specified and **have not been run**. No physical spacing. No proton, quark, mass, or new EM law from that packet.
- G-768 **disproved** the claim that one static `J_c = -J` assignment gives isotropic `a' = 2a`. The M-type mode is a stripe, `psi_nm = A (-1)^(n+m)`, not a doubled triangular lattice. Rotational averaging can restore isotropy of a rank-2 tensor. It does not give factor 2.
- Next smallest step, already written: build coarse-grain maps `R_1, R_2, R_3` and compute `R_3 R_2 R_1` without inserting 2. Result may be `2I`, `sI` with `s != 2`, or not isotropic. The calculation wins.
- Rabbit-hop `2N` and musical ratios are not evidence for spatial doubling. G-768 §7.

### W5 — Spectral attack is unfired

G-767 is a contract, not a result. Statistic and `x0` rule are not frozen. Required order: PDG tables, then CERN event spectra, then GWOSC, and only then other bands. Nulls include shuffle, phase shift, acceptance, smooth-density, and synthetic octave / non-octave controls. Superfluid-crystal language stays a hypothesis until dispersion, anisotropy, or transport distinguishes it.

### W6 — EM / proton bridge is a packet, not a solution

G-765: equations and failure gates exist. No physical coupling, no proton-like localized mode, no multi-observable fit. Search is forbidden until the linear EM-coupled lattice passes G-766 controls. G-736 `uud` / `R,G,B` tags are Gray labels on a kinematic visualization.

### W7 — PPF and gravity are downstream of the micro hold

G-728 C1–C10 (Point / Path / Field transforms, no double-counting of spin) are unchecked. Updated 51 starts C2 only.

G-728 H1–H13: no validated Newtonian N-body yet, so no honest One-Wave orbital correction. Galactic I1–I7 wait on that. Do not solidify cosmology by skipping the two-body regression.

### W8 — Logic layer is in better shape. Do not re-litigate it as the SM attack

G-728 A1–A6 and B1–B3 are checked: six routes, mirror operator, commitment, Ground/Hold split, noise hysteresis, center geometry, six-gate extractor. Open inside that layer: B4 Build-before-Break, B5 delayed noisy threshold, B6 return versus reset. Those matter for hardware. They do not replace W1.

---

## 3. Solidify order

Do these in order. Parallel work is allowed only where it cannot pretend to be the smash.

1. **W1 coefficient scan** on the seven-cell. Publish the region or the empty region.
2. Hessian at the surviving minima only.
3. Barrier path. One negative mode or an honest zero.
4. Fixed dimensionless `W`, crosses on. Compute `R_G` or record that the barrier is zero.
5. One second observable. Width or another mass. No retune. That is the SM hit.
6. Beside that, not instead of it: run G-766 steps 1–6 (analytic dispersion and controls). Freeze the G-767 statistic. Compute G-768 `R_cycle`.
7. Do not open proton labels, galactic trails, or a new `a0` before 1–5 exist.

## 4. Already solid enough to stand on

- Measurements stay. Ontology of the Higgs syrup is what is challenged. G-761.
- Speed-ceiling shortcut to mass is erased and barred from re-entry. C-318.
- `hbar omega = 125 GeV` is retired as the mechanism. C-322.
- 125 GeV is not a lattice constant. Updated 46.
- Static signed-axis isotropic 2× is disproved. G-768.
- Finite six-route logic and the mirror operator exist as tested code. G-728 A, G-729.

## 5. Failure conditions for this note

This note itself fails if a later edit:

- cites the 2026-09-06 Hessian receipt as proof of two basins;
- calls 125 GeV both the calibration and the prediction;
- feeds G-745 `a0` into a nuclear test;
- promotes G-766 or G-767 before the runs and nulls exist;
- or treats `R_cycle = 2I` as already shown.
