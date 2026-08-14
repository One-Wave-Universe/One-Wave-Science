---
node_id: "D-415"
canonical_name: "Planetary Point-Path-Field Simulation"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Planetary-Scale Laboratory / Newtonian-Control Comparison / State-Driven Visualization"
claim_gate_detail: "YELLOW (scoped candidate-vs-control simulation; UPDATED_41 architecture only partially implemented, see Scope)"
metadata_standard: "I-06"
---

# Node D-415: Planetary Point-Path-Field Simulation

**Dependencies**
Upstream: A-102 Displacement, A-103 Differential, A-109 Inertial Memory, A-110 Oscillation, A-117 Dimensional Integrity, C-311 Electric-Magnetic Duality, C-317 Boundary-Tension Weave, C-318 Four-Interaction Mass-Effect Response, D-411 Mirrored Axis Pairs, D-412 Lattice Simulation and State-Driven Visualization Standard, UPDATED_41_PLANETARY_SCALE_DISPLACEMENT_MODEL.md
Lateral: D-413 Ground Lattice Orbital-Restoring Simulation (lower-scale analog architecture), UPDATED_38/39/40 (superseded narrower orbital framings)
Downstream: One_Wave_Bench experiment ledger

**Assets**
- `Nodes/D-415_Planetary_Point_Path_Field_Simulation/simulate_d415.py` — headless engine, single source of truth
- `Nodes/D-415_Planetary_Point_Path_Field_Simulation/results/` — CSV time series, `d415_summary.json` receipt, comparison plot
- `Nodes/D-415_Planetary_Point_Path_Field_Simulation/index.html` — static state-driven results viewer (reads the JSON/CSV receipt; renders nothing that was not computed by the engine)
- `Nodes/D-415_Planetary_Point_Path_Field_Simulation/README.md` — how to run, scope, and honesty boundary

## Purpose

UPDATED_41 proposes that a planet is a persistent planetary-scale displacement structure — a coupled 2D bound/compressed state, a recursive nine-part Point-Path-Field state, internal material/EM rotation, and instantaneous neighbor/reference interaction — rather than a point mass with a bolt-on magnetic correction. That document is a locked candidate architecture, not runnable code.

D-415 is the first runnable test of a scoped slice of that architecture. It asks a narrower, falsifiable question than the full UPDATED_41 grammar: **does a small, bounded, ablatable candidate correction to Newtonian gravity — built from prescribed internal rotation shear, an EM-alignment proxy, and a relaxing 2D compression state — produce a measurably different, non-arbitrary planetary trajectory from an identically-initialized Newtonian control, without retuning per-planet coefficients to force a match?**

It does this under D-412 discipline: declared state evolves under a reproducible update law; measurements are computed from the evolved arrays; the Newtonian control and post-Newtonian (1PN) control are run from **identical initial conditions and integrator tolerances** (spec layer 8), not reconstructed after the fact; every run can fail.

## What Is Actually Implemented (honest scope)

UPDATED_41 declares a nine-component recursive Point-Path-Field state (`PP, PPa, PF, PaP, PaPa, PaF, FP, FPa, FF`) per body, an internal fluid/dynamo solver, and a derived (not assigned) active range. D-415 does **not** implement all of that. It implements:

- a real Newtonian N-body integrator (Sun + Mercury, Venus, Earth, Mars, Jupiter) as the Path/orbital layer — this is the actual, non-candidate physics;
- an optional standard 1PN (post-Newtonian) correction term, the literal textbook Schwarzschild/EIH approximation, as the "later, post-Newtonian control" required by spec layer 8;
- a per-planet 2D compression scalar `C_i` (`L2D_i` analog) that relaxes toward a tidal-stress proxy — genuine persistent state, not a static parameter;
- prescribed (not solved) spin/core-differential rates from real spin periods plus an illustrative core-mantle offset, feeding a shear channel `eps_shear * DeltaOmega_core-mantle^2`;
- a declared periodic EM-alignment proxy (orbital-phase modulation) feeding an EM channel, active only for the three bodies UPDATED_41 S9-S12 identify as having a global intrinsic dynamo (Mercury, Earth, Jupiter); Venus and Mars are explicit no-dynamo controls with the channel structurally zero;
- the ternary local state machine (`A-103` differential, `-1/0/+1` on `delta_C = C_i(t) - C_i(0)` against a declared threshold, one radial axis pair, `2N=2` directed routes + `2N+1=3` centered states — `(0)` is never counted as a direction);
- the required fit-interval-versus-withheld-prediction-interval split, reporting RMS model separation in each window;
- the required "`d_ij + d_jk + d_ki = 0` is kinematic, not evidence" check, computed and labeled as a sanity check only.

What is **not** implemented, and is declared out of scope rather than faked: the full nine-part recursive P/Pa/F state; an internal fluid/dynamo solver (spin and core-offset are prescribed constants, not derived, and do not feed back from the orbital solver); a derived (non-cutoff) active range; FCC/HCP stacking and imposed-well ablations (D-409/D-413 lattice-scale concepts that do not apply to point-mass gravity); an absolute physical calibration of the correction coefficients. See `README.md` and the `limitations` array of every receipt for the complete list.

## Update Law (summary — full law in `simulate_d415.py`)

For each planet `i`, at every RK4 substep:

```text
a_newton_i      = sum over all other bodies j of  G m_j (r_j - r_i) / |r_j - r_i|^3
a_from_sun_i    = G m_sun (r_sun - r_i) / |r_sun - r_i|^3        (isolated for the candidate term)
K_eff_i(t)      = 1 + eps_shear * DeltaOmega_i^2                  [ablatable: use_core_differential]
                    + eps_em    * em_alignment_proxy_i(t)         [ablatable: use_em_shell, dynamo bodies only]
                    + w_coeff   * (C_i(t) - C_i(0))                [ablatable: use_boundary_weave]
a_candidate_i   = a_from_sun_i * (K_eff_i - 1)                     [zero when onewave_active=False: exact Newtonian control]
a_1pn_i         = standard Sun-dominated 1PN term                  [only when use_1pn=True]
a_i             = a_newton_i + a_candidate_i + a_1pn_i
dC_i/dt         = compress_relax * (tidal_target_i(t) - C_i)       [ablatable: use_memory]
```

`K_eff` is bounded by construction to a small perturbation (checked: `|K_eff - 1| < 1e-3` for every body and every timestep) — it is declared as a candidate correction to be tested, not a rewrite of gravity.

## Required Measurements (computed, not asserted)

- perihelion-precession estimate (arcsec/century) for the Newtonian control, the 1PN control, and the candidate model, plus a half-timestep convergence check;
- RMS model-separation between the candidate model and the Newtonian control, split into the fit interval and the withheld interval;
- numerical energy drift of the Newtonian control (integrator-integrity check);
- barycenter/center-of-momentum drift;
- applied work integrated from the candidate correction term, per body;
- `K_eff` bounds per body (perturbation-boundedness check);
- ternary local-state route counts per body;
- the kinematic-identity sanity check, explicitly labeled as not evidence.

## Required Ablations

`no_em_shell`, `no_boundary_weave`, `no_core_differential`, `no_memory`, `symmetric_mercury` (removes the UPDATED_41 S9 Sun-Mercury asymmetric term), `no_jupiter` (N-body-count analog of a spatial-refinement test), `zero_input` (must reduce exactly to the Newtonian control), and a half-timestep refinement run. `no_well`, FCC-vs-HCP, and periodic/random-lattice ablations are declared not applicable at this point-mass scale — see `README.md`.

## Failure / Revision Conditions

D-415 fails or must be revised if:

1. the `zero_input` ablation does not reduce exactly (to numerical precision) to the Newtonian control;
2. `K_eff` is not a bounded small perturbation for any body or case;
3. the kinematic-identity check is ever treated as evidence rather than a sanity check;
4. the candidate correction requires per-planet retuning of `eps_shear`, `eps_em`, or `w_coeff` beyond the single declared dynamo/no-dynamo structural switch to avoid contradictions (UPDATED_41 falsifier: "the same rule cannot operate across planets without body-by-body arbitrary coefficients");
5. the half-timestep run does not converge toward the same precession estimate as the base timestep;
6. the receipt's limitations are dropped or the candidate correction is reported as a validated physical result rather than a candidate architecture test.

## Claim Status

YELLOW. This is a scoped, honestly-bounded engineering test of one narrow slice of UPDATED_41. It is not a derivation of gravity, an internal planetary dynamo, a GR replacement, or the full recursive Point-Path-Field grammar, and it does not claim to match observed planetary ephemerides.
