# Code ledger c18

Files in slice: 7. All 7 read in full.

## solvers/hadron_knot_geometry.py
- Purpose / node IDs cited: Hadrons as bounded 3-vortex (baryon) or 2-vortex (meson) knots held by a "Boundary-Tension Weave". Cites C-317, C-318 (L8, L54, L326, L555). Self-declared Gate YELLOW (L30). Imported by many solvers/*coherence*/calibration scripts and by hadron_mass_predictor.py.
- Point rotation: not present. `VortexPhase` has `ell`, `em` quantum numbers and a static `phase_offset` (L82-86). There is no omega, L = I omega, attitude, or time evolution. The ell values are hard-set in the factory functions (L378-383, L411-416, L443-448, L476-479). Nothing starts or changes them. No gravity, no magnetic open/closed switch, no parent organization rate.
- Path rotation: not present.
- Field: "twist/vorticity" energy E_twist = eta_T Σ ∫|∇×v|² is approximated as ell(ell+1)/R² times volume (L282-305). No real curl is computed. There is no chi and no grad chi. Phase-locking energy uses Monte Carlo |ψ_a-ψ_b|² sampling with a fixed seed of 42 (L217-280). The pair "coherence" factor is 1/(1+ln ω_ratio), with ω = κ_T/m (L188-215, L240).
- Magnetism: not present. "Magnetic quantum number" is only a label (L83).
- Parent/child: not present.
- Hard-coded targets / refits: PDG quark masses (L43-50). Radii are seeded from the experimental targets 0.85, 0.87, 0.85 and 0.4 fm (L390, L392, L423, L425, L455, L457, L486, L488), and those same values are the calibration targets (L617-622). Because `compute_boundary_radius_from_parameters` returns base_scale·sqrt(κ/σ)·vortex_factor (L177), the "best" fit is simply κ_T=σ_T. The radius then equals target × 1.1, which is circular. Twist energy divides by len(vortices) after multiplying volume twice (L303), so it is dimensionally ad hoc.
- Pass criterion: gate "GREEN (calibration complete)" if the average radius error is under 10% (L740). The radius is the target scaled by a constant, so the pass is guaranteed by construction (κ=σ gives about a 10% error from vortex_factor 1.1). This is a spread or fit criterion, not rotation.
- Violations: L392/L425/L617-622/L740 use observed radii as inputs and then report the fit as calibration "GREEN" (a refit). L749 writes to the hard-coded path /home/claude/... outside the repo. Measured against the canonical P/P/F rules, the node is incomplete: no Point rate, no Path rate, and the field curl is a placeholder.

## solvers/hadron_mass_predictor.py
- Purpose / node IDs cited: Predicts hadron masses as constituent masses + weave energy + binding. Cites the C-317 equations (L661) and C-319 (R tensor, K_L, L310, L352-358, L390-393). Uses "Hypothesis A" per-flavor α exponents (L557-565).
- Point rotation: not present. The docstring mentions "Rotation and oscillation of the knot structure" (L307), but no spin, omega or L variable exists.
- Path rotation: not present.
- Field: inherits the E_twist placeholder from hadron_knot_geometry (L465). There is no chi and no grad chi.
- Magnetism: `compute_confined_pressure` sets the "magnetic pressure" to 0.12 × (constituent mass + 0.270 GeV)/volume (L329-345). Both the 12% fraction and the 270 MeV binding are hard-coded. `compute_lattice_reorganization_tensor` (L349-383) quotes τ_R ∂_t R = -R + λ_B W_B + λ_ω W_ω, but it actually returns the scalar r = min(mag_pressure/0.05, 1) (L374-381). R is NOT built from B (no W_B = B⊗B - |B|²I/3) and is not a tensor. K_L = I + κ_R R is only named in the docstring (L392) and never built as a tensor. Instead, kappa_R = 0.350 GeV is hard-coded (L428). It was back-solved from the 290 MeV nucleon gap (L403-405, L424-427) and then used as a scalar binding energy E_mag = -κ_R·r·P·(3/V) (L434-438). Gravity is not involved.
- Parent/child: not present.
- Hard-coded targets / refits: PDG hadron masses (L51-59) are used for error scoring. κ_R = 0.350 is back-solved from the experimental gap (L424-428). The binding bases -8 and -30 MeV are "empirical" (L500, L503). The κ_T_base values 0.297 and 0.50 are "calibrated" (L69, L568, L575). The α_dict comes from a grid search against the same targets (L557-565). The sensitivity sweep reuses the same targets (L676-704). Output is reported as "predicted_mass_MeV" (L534), which presents a fit as a prediction.
- Pass criterion: none formal. The script prints error % against PDG and the "improvement" of Hypothesis A over the baseline (L728-748). The figure of merit is mass spread or error, not rotation.
- Violations: L428 hard-codes kappa_R (canonical: kappa_R not set). L349-383 builds R from confinement pressure instead of from B, and as a scalar rather than a tensor. L392 claims K_L = I + κ_R R, but K_L is never used to map grad chi to g. Instead κ_R becomes a mass/binding coupling, a magnetism-into-binding/mass channel with no grad chi gate. L534 presents refit masses as predictions. L28 has a hard-coded external sys.path to /home/claude.

## solvers/harmonic_locking_unifier.py
- Purpose / node IDs cited: Narrative "harmonic locking at boundaries" unifier across electron g-2, three-body, triple-alpha and gravity (L1-24). Cites no node IDs. Only "PHASE_5_QUANTITATIVE_RESULTS.md" is referenced (L233).
- Point rotation: not present.
- Path rotation: not present. The three-body "collinear equilibrium" is only stored as numbers (L242-245).
- Field: only a text string, "E-field = ∇φ + ∇×A" (L294). No computation.
- Magnetism: not present.
- Gravity: "Metric emerges from lattice" at the Planck cutoff (L127-129, L252-255, L284-289, L368). These are strings and constants. No g = -α K_L grad chi.
- Parent/child: not present.
- Hard-coded targets / refits: electron_g2_prediction is set equal to electron_g2_experiment, the same literal 1.1596521818e-3, and labeled match "exact" (L236-238). Hoyle energy 7.654 MeV and width 0.092 (L248-249) are measured values stored as results. Scale hierarchy 1e17 vs "observed" 1e16 (L253-254); the report labels the observed value as "predicted" (L287). The couplings 0.5, 0.01, 0.6 and 1.0 are literal constants called "emerges" (L117-129).
- Pass criterion: none. The script prints and writes harmonic_locking_unification_results.json to the CWD (L393).
- Violations: L236-238 present an observed g-2 as an "exact" prediction match. L248, L280 and L287 present measured Hoyle values and the hierarchy as emergent. L128-129, L253-255 and L284-289 state "gravity emerges from lattice cutoff / metric", which is not the canonical g = -α K_L grad chi with R=0 giving the A-115 baseline. This competes with the canonical gravity law. Dead or legacy: no importers.

## solvers/higgs_criticality_solver.py
- Purpose / node IDs cited: Sweeps (β, γ) to find a lattice mode at the Higgs mass. Cites D-600 and D-602 (L174). Self-declared Gate YELLOW (L15).
- Point rotation: not present.
- Path rotation: not present. `DetectorPoint` phi is the detector azimuth (L47-72), not a rotation rate.
- Field: 1D dispersion λ² - C(k)λ + (1-γ) = 0 with C(k) = 1 + 2β(cos k - 1) (L171-203). No curl and no chi.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: TARGET_HIGGS_MASS = 0.125 "GeV" (L260). The value is a unit bug: 125 GeV is 125, and 0.125 GeV is 125 MeV. The searcher picks the (β, γ) closest to the target (L361-371) and the report calls it "HIGGS MASS PREDICTION" (L396). `scale_to_gev` multiplies by (0.511/511)/1000 = 1e-6 (L249-250), so the output is at most about 1e-6 GeV and can never reach the target. The "critical point" is therefore just the grid point at minimum error. Report L407-419 claims all fermion masses, couplings and the full SM spectrum are "unlocked", with no computation behind it. The synthetic detector event is invented (L455-462).
- Pass criterion: none formal. Best score = min |m - target| + 0.1·coherence error (L361-365). This is a target fit.
- Violations: L260 and L396 use an observed value (Higgs) as the target and report the fitted point as a prediction, and the target carries the unit bug. L407-419 make unsupported claims. L490 writes to the hard-coded /home/claude path. No importers in .py; its JSON output is consumed by lattice_visualizer.py (L492).

## solvers/high_energy_validator.py
- Purpose / node IDs cited: "Phase 4" mapping of the D-600/D-602 dispersion to particle masses (L5-12, L66, L83-107).
- Point rotation: not present.
- Path rotation: not present.
- Field: the longitudinal mode is labeled "E-like" (C = 2-γ-βk²) and the transverse mode "B-like" (C = 2-γ+βk²) (L83-107). These labels are the only "magnetism" content: there is no curl operator and no chi or grad chi.
- Magnetism: the "B-like transverse" label only (L96-107, L172-200). No B, R, K_L or κ_R.
- Parent/child: not present.
- Hard-coded targets / refits: SM mass table in electron units (L51-64). Several entries are numerically wrong: up 0.001 and down 0.002 electron masses, where the real values are about 4 and 9. The W, Z and Higgs entries are also inconsistent. Coupling α_OW = β/2π compared with 1/137 (L210-213). The "lattice cutoff" of 256 × 0.511e-3 GeV (L247) gives 0.131 GeV, but the comment says about 130 GeV (L245), which is a unit error. `characteristic_scale = mass × 0.511` is labeled GeV but is in MeV (L167, L197). Confidence values are hand-set (L154, L159, L184, L189, L222).
- Pass criterion: none. The only status is 'PHASE_4_PREDICTIONS_GENERATED' (L289). `save_report` is a stub (L305-308).
- Violations: L245-247, L167 and L197 contain unit errors, and the output is presented as "predictions". L51-64 is a reference table with wrong values. No rotation or magnetism canon content. Dead or legacy: no importers.

## solvers/joint_boundary_response.py
- Purpose / node IDs cited: Linear-response candidate on the native FCC12 shell with 4 roles (knot, electrical_shell, mirror, weave) (L1-5, L13). States explicitly "No particle target inputs or physical energy conversion... not a self-localized knot or a quark mass prediction" (L2-5). Cites no node IDs. Live: imported by run_joint_response.py, phase5a_unified_solver.py, phase5b_bounded_knot_forward.py, bulk_excitation.py and tests, and run in .github/workflows/native-3d-lab.yml.
- Point rotation: not present. There is no omega, L or attitude. The "boundary_inertia" function (L105-114) is the Schur-complement stiffness/mass matrix at the port, which is translational field inertia, not rotational. `carried_tensor` (L157-163) and `cycle_energy` (L165-177) handle a carried uniform translation velocity (gradients·velocity), not rotation.
- Path rotation: not present. `velocity` in cycle_energy is a translation of the pattern (L174), with no orbit.
- Field: FCC12 graph Laplacian (L52-64). The interaction block is diag(spatial) + cross·cycle Laplacian over the 4 roles (L66), and phase lock is c.phase_lock·cycle Laplacian (L70). Per-site 3D gradients come from least squares with a rank-3 check (L143-155). No curl, no wake, no chi or grad chi.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none. Coefficients are declared candidates (L18-24), and there are no particle targets.
- Pass criterion: no internal pass bit. Guards include the stability condition dt²λmax < 4 (L85-88), the anchoring check (L109-110), the solve residual 1e-10 (L129-131), and the derivative rank of 3 (L153-154). The scatter ledger reports pin - pout - loss (L139-141). Correctness is energy and flux bookkeeping, not rotation.
- Violations: none against the canon. Measured against the P/P/F completeness rule, it omits the Point and Path rates, which is acceptable because the file declares itself a response control only (L3-4).

## solvers/lattice_visualizer.py
- Purpose / node IDs cited: 1D lattice e+/e- peak/trough "pair production and annihilation" simulation with plots (L1-5). Cites no node IDs. Update rule ψ^{n+1} = ψ + (1-γ)(ψ - ψ_prev) + β(⟨ψ_j⟩ - ψ) (L34-49).
- Point rotation: not present.
- Path rotation: not present. The peaks are not moved; Gaussians are injected at fixed positions (L57-69).
- Field: 1D scalar ψ only. No curl and no chi.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: β and γ are loaded from higgs_criticality_results.json (L492-496), so they inherit the Higgs-target fit. The "Yukawa prediction" ω = (1-γ)β (L302) is an arbitrary formula. E_predicted = 2.0 is described as "2 × electron rest mass" (L379) without calibration. The initial state is unseeded random (L27), so runs are non-deterministic.
- Pass criterion: four tests (L281-450). Frequency within 10% of (1-γ)β (L310). Boundary width between 10 and 30 lattice cells (L357). E_released > 0 (L392); the energy error is computed but ignored. The phase difference must be within 0.5 rad of π (L442). All 4 passing prints "Framework VALIDATED - Ready for publication" (L473-474). This is a spread, width or energy-sign criterion, not rotation.
- Violations: L392 passes on the sign of the energy change while ignoring its own predicted value. L473-474 overclaims "VALIDATED - Ready for publication" from loose heuristic tests. L492-496 depend on the Higgs-target-fitted (β, γ). Dead or legacy: no importers.

## Slice summary
- Canonical point rotation: NONE of the 7 files implements point rotation (omega, L = Iω, attitude, open/closed dL/dt switch, or parent organization rate). None implements path rotation or a field curl/chi/grad chi. With respect to the P/P/F rule, every file is Point- and Path-incomplete.
- Magnetism/gravity violations:
  - hadron_mass_predictor.py: R is built from confinement pressure, not B (L349-383); R is a scalar, not a tensor; kappa_R = 0.350 is hard-coded and back-solved from the mass gap (L424-428); and κ_R·R feeds binding mass rather than K_L·grad chi (L434-438, L468-471).
  - harmonic_locking_unifier.py: gravity is asserted to "emerge from lattice cutoff/metric" (L128-129, L253-255, L284-289), not g = -α K_L grad chi.
- Refits presented as predictions:
  - hadron_knot_geometry.py: radii 0.85/0.87 fm are seeds and also targets, with gate GREEN (L392, L425, L617-622, L740).
  - hadron_mass_predictor.py: PDG masses, back-solved κ_R, empirical binding, and "predicted_mass" (L51-59, L428, L500-503, L534).
  - harmonic_locking_unifier.py: g-2 prediction is the same literal as the experiment, plus the Hoyle values (L236-238, L248-249).
  - higgs_criticality_solver.py: the 125 GeV target is entered as 0.125, the scale map caps output near 1e-6 GeV, and the report claims the full SM spectrum (L260, L249-250, L396, L407-419).
  - high_energy_validator.py: unit errors (L167, L197, L245-247).
  - lattice_visualizer.py: inherits the Higgs-fit β/γ and overclaims "VALIDATED" (L492-496, L473-474).
- Live vs dead:
  - Live: joint_boundary_response.py, the cleanest file, with no target inputs (CI workflow native-3d-lab.yml plus phase5a/5b and bulk_excitation importers).
  - Semi-live legacy calibration chain: hadron_knot_geometry.py and hadron_mass_predictor.py (imported by many calibration and diagnostic scripts in solvers/, which hard-code /home/claude paths).
  - Dead/legacy with no importers: harmonic_locking_unifier.py, higgs_criticality_solver.py, high_energy_validator.py, lattice_visualizer.py. lattice_visualizer only consumes the higgs_criticality JSON.
