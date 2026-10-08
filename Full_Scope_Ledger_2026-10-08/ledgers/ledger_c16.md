# Code ledger: slice c16 (14 files, all read in full)

Root: /home/user/One-Wave-Science/solvers/

## solvers/cascade_neural_router.py (426 lines)
- Purpose / node IDs cited: a "neural router" that maps an observation to "cascade parameters" (beta_0, r_decay, gamma, f_EM) and a confidence score. No node IDs cited. Runs a demo at import time (lines 315-426, no `__main__` guard). Referenced only by FRAMEWORK_COMPLETION_STATUS.md and SOLVER_INDEX.md.
- Point rotation: not present. No spin, omega, L or attitude.
- Path rotation: not present as dynamics. "satellite_velocity" and "M31 orbital velocity" (lines 329-333) are scalar speeds.
- Field: not present. `gamma` is a per-scale damping lookup (112-117) and is never used in the prediction.
- Magnetism: not present as B. "EM coherence" f_EM is a scalar lookup table (121-126) times (0.7+0.3*q) (179). It has no B, R, K_L or kappa_R.
- Parent/child: child signal = parent_velocity * beta_0 * exp(-d/r_decay) * f_EM (200-208), a raw scalar multiply with no transport. When there is no parent, the observation is multiplied by beta and used to "predict" itself (210-212), which is circular.
- Hard-coded targets / refits: beta_0, r_decay and gamma come from prior fits per scale (99-118). Galactic beta_0=0.2480 and r_decay 51.5/46.2 kpc are satellite fits (35-37). "Validator accuracy" weights are typed in (129-135), and atomic r_decay = Bohr radius (108). Confidence is 40% this hard-coded "accuracy" (252-257).
- Pass criterion: none computed. Lines 422-424 always print "successfully routes", "appropriate confidence" and "universality across scales", even though line 412 prints the beta_0 spread (0.248 vs 0.35, about 41%).
- Violations: cascade_neural_router.py:208 adds parent/child raw (no R_c^T transport). :212 is a circular self-prediction. :99-135 are hard-coded refit tables reported as "learned". :422-424 are unconditional success claims, and :424 claims universality against :412.

## solvers/coherence_diagnostic.py (175 lines)
- Purpose / node IDs cited: hadron "oscillation coherence" factor between quark pairs. No node IDs. Imports hadron_knot_geometry through a hard-coded path /home/claude/one-wave-science/solvers (line 10).
- Point rotation: not present. omega = kappa_T/m (35-36) is an "oscillation frequency", not a spin or L.
- Path rotation: not present.
- Field: not present. Coherence = 1/(1+ln(omega ratio)) (59) is an ad hoc factor.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: "actual_errors" -23.9/+27.7/+203.5 MeV (138-142) are prior model-minus-PDG residuals. The expected-sign rule maps "NO symmetric pair" to POSITIVE (155-156), which matches the known Lambda sign after the fact.
- Pass criterion: a sign-match check mark (163). Nothing is asserted.
- Violations: none against the rotation/magnetism rules. Methodological issue: coherence_diagnostic.py:153-158 is a sign rule chosen to agree with already-known residual signs.

## solvers/correction_formula_calibration.py (294 lines)
- Purpose / node IDs cited: fits a one-coefficient "correction" ΔE = A × range × rank × f(omega_ratio) to the proton, neutron and Lambda residuals. No node IDs. Uses the hard-coded /home/claude path (28).
- Point rotation: not present. omega = kappa_T/m (69-70) is not spin.
- Path rotation / Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: errors_obs (100-104), EXPT masses and PREDICTED_BASE (249-250). rank_factor values +1/-1/-2 (60-66) are chosen per hadron. lstsq fits A to the same three points (138-192), and "corrected masses" are then reported against the same data (255-262).
- Pass criterion: RMSE < 20 MeV prints "EXCELLENT" (275-276). That is an in-sample fit on 3 points.
- Violations: correction_formula_calibration.py:135-192 and 255-262 report a fit to observed masses as corrected predictions. :60-66 sets rank_factor ad hoc. No rotation-rule violations.

## solvers/coupled_resonator_validator.py (276 lines)
- Purpose / node IDs cited: simulates three coupled damped LC oscillators with coupling k(d)=g0*exp(-d/lambda_c). No node IDs. Referenced by VALIDATORS_INDEX.md and PHASE_5_COMPLETE_PROOF_STACK.md.
- Point rotation: not present.
- Path rotation: not present.
- Field: not present. Damping gamma = omega0/Q (36).
- Magnetism: not present (LC is only a label).
- Parent/child: not present.
- Hard-coded targets / refits: none observed. The "One-Wave prediction" k(d) is typed in as the input law (40-46), and "k_measured" is just amp3/amp1 (100-110). The test is tautological: it recovers what was put in.
- Pass criterion: corr(spacing, energy transfer) < -0.5 and smooth variation (198-201). Any monotone coupling passes, so this says nothing about One-Wave specifically.
- Violations: none against the canonical rules. Overclaim: coupled_resonator_validator.py:250 prints "One-Wave predictions VALIDATED". It also writes JSON into the working directory (269).

## solvers/coupling_constants_from_lattice.py (404 lines)
- Purpose / node IDs cited: claims alpha_em, m_e/m_p, alpha_s and G come from the D-409 twelvefold close-pack lattice. Cites D-409. Docstring maps "Division (pressure gradient) → Gravity" (21). Runs at import time.
- Point rotation: not present.
- Path rotation: not present (only print text at 383-384).
- Field: not present as a computed field. Gravity is "lattice curvature" / pressure gradient as text only (211-244).
- Magnetism: not present. EM is described as "Addition (constructive interference)" (18).
- Parent/child: not present.
- Hard-coded targets / refits:
  - alpha^-1 = 2*66+5 (127), numerology with a "+5" added.
  - Method 2 uses the observed 1836.15 (132).
  - The mass ratio uses a "1.3394 empirical harmonic correction" (165) and then returns the observed 1/1836.15 as "derived" (174-178), so the reported error is 0% by construction.
  - G_derived = 1/M_P² where M_P is built from 137.036 and 1836.15 (234-238), which is dimensionless and unanchored.
  - alpha_s uses the standard QCD beta-function constant (196-200).
- Pass criterion: none. Prints "ALL constants derived (no fitting)" and "FRAMEWORK STATUS: COMPLETE" unconditionally (366-402).
- Violations:
  - coupling_constants_from_lattice.py:174 reports an observed value as a derived one.
  - :132 and :165 use observed and empirical inputs.
  - :234-238 builds G from EM constants. No grad chi or K_L, so gravity is not tied to g = -alpha K_L grad chi. It is a numerology G, not a magnetism→gravity path.
  - :372-402 are false "no fitting" claims.

## solvers/determine_flavor_hierarchy.py (317 lines)
- Purpose / node IDs cited: grid-searches the radius-scaling exponent alpha per quark flavor (charm, bottom) against PDG hadron masses. Cites C-317 (279). Imports hadron_knot_geometry and hadron_mass_predictor (28-29) through the hard-coded /home/claude path.
- Point rotation: not present. VortexPhase uses ell=0, em=0 (62-114), with no spin or L.
- Path rotation / Field / Magnetism / Parent-child: not present. sigma_T, kappa_T and eta_T ("twist/vorticity") are passed through to HadronMassCalculator.
- Hard-coded targets / refits: PDG masses (32-48) are the fit targets. alpha_charm and alpha_bottom are picked by minimum error against those same masses (194-226). The script then claims "7 parameters predict ALL hadron masses" (308).
- Pass criterion: minimum average % error. No gate.
- Violations: determine_flavor_hierarchy.py:162-167 uses a bare `except:` fallback that returns sum(m_q)+1300 MeV, silently substituting a fake prediction into the fit. :194-226 and :308 present refit parameters as predictions.

## solvers/determine_oscillation_correction.py (201 lines)
- Purpose / node IDs cited: tries 4 one-coefficient forms in omega_ratio = m_max/m_min against the 3 residuals. No node IDs. Uses the hard-coded /home/claude path (18).
- Point rotation: not present. omega = kappa_T/m (54).
- Path rotation / Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: PREDICTED_MASSES and ERRORS_MEV are hard-coded (35-45). The coefficients are means of error/x on the same 3 points (111, 127, 144, 160).
- Pass criterion: lowest RMSE wins (183). In-sample.
- Violations: none against the rotation rules. Refit to residuals is presented as a "FORMULA" (187-195).

## solvers/dispersion_validator.py (309 lines)
- Purpose / node IDs cited: D-600 (1D scalar lattice dispersion), D-601 (named only), D-602 (vector E/B longitudinal vs transverse). Has a test (test_dispersion_validator.py) and is imported by dispersion_visualizer.py.
- Point rotation: not present.
- Path rotation: not present.
- Field:
  - Update rule psi_{n+1} = psi + (1-gamma)(psi - psi_{n-1}) + beta(avg - psi) (110-119).
  - D-600 characteristic λ² - Cλ + (1-γ) = 0 with C = 2-γ+β(cos k -1) (52-71).
  - D-602 longitudinal C = 2-γ-βk² ("E-like", divergence) (178-190) and transverse C = 2-γ+βk² ("B-like", curl) (192-204).
  - Curl appears only as the sign of a k² coefficient. No curl operator is computed.
- Magnetism: "B-like" is only the transverse dispersion branch. No B vector, R, K_L, kappa_R, and no gravity coupling.
- Parent/child: not present.
- Hard-coded targets / refits: none from observation.
- Pass criterion: D-600 is "PASS" if max|omega_meas - omega_th| < 0.1 (251). D-602 is hard-coded `'sign_flip_verified': True, 'status': 'PASS'` (256-260) with no computation. Note the simulation update (117-119) uses beta*(avg - psi) with avg = (psi+ + psi-)/2, which gives (β/2)(cos k - 1), while theory uses β(cos k - 1) (63). That is a factor-2 mismatch, so D-600 likely shows "REVIEW".
- Violations: dispersion_validator.py:256-260 hard-codes the D-602 PASS. :63 vs :115-119 is a theory/simulation coefficient mismatch. :303 writes to /tmp. No rotation-rule violations.

## solvers/dispersion_visualizer.py (168 lines)
- Purpose / node IDs cited: prints D-600 measured vs theory and D-602 E/B mode tables, plus a (γ,β) stability grid at k=π. Imports dispersion_validator.
- Point rotation / Path rotation: not present.
- Field: the same D-602 E-like/B-like branches as above (54-76).
- Magnetism: label only ("B-like transverse").
- Parent/child / Hard-coded targets: not present.
- Pass criterion: none. Lines 78-80 and 152-157 print "Sign flip verified" and "β < 1 (derived, not imposed)" unconditionally, while the stability grid (102-112) checks only k=π.
- Violations: dispersion_visualizer.py:78-80 and :152-157 are unconditional verification claims. No rotation-rule violations.

## solvers/driven_bulk.py (190 lines)
- Purpose / node IDs cited: declared external periodic drive on the existing FCC bulk constitutive engine. Covers energy and work bookkeeping, centroid tracking, and lowest-band packet projection. No node IDs. LIVE: used by .github/workflows/native-3d-lab.yml and test_driven_report.py, with DRIVEN_BULK_RECEIPT.md.
- Point rotation: not present. No spin, L or attitude is tracked, only the centroid (42-72).
- Path rotation: centroid displacement only (172-179). No orbit and no L.
- Field: the external potential is -sin(k·x)·f/k, applied as a split-step phase (20-28). There is no curl, chi or grad chi.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none. Scope says "no fitted inertia or physical mass" (190). Force is bounded to ±0.02 (15).
- Pass criterion: no pass bit. It reports energy-balance residual, norm error and a geometrically_resolved flag (179). Seam and concentration are declared reporting policies (43-46).
- Violations: none.

## solvers/electron_g2_solver.py (524 lines)
- Purpose / node IDs cited: electron anomalous magnetic moment a_e from "phase-boundary geometry". No node IDs. Referenced by VERIFIED_SOLUTIONS_BOOK.md, PHASE_5_VALIDATION_COMPLETE.md and the Standard_Physics audit register.
- Point rotation: electron spin is a constant `circulation = 0.5` (121) that is never used in any computation. There is no omega, no L = Iω, and nothing starts or changes it.
- Path rotation: not present. "Spin-orbit" g_SO is a single scalar (117, 138-152).
- Field: not present. P_electron and E_electron are constants (111-112), and the width is sqrt(0.1²+0.1²) (130-136).
- Magnetism: the magnetic moment is not computed from any B or circulation. a_e = (QED value) × g_SO/0.5 (306-311). No B, R, K_L or kappa_R.
- Parent/child: not present.
- Hard-coded targets / refits:
  - The "One-Wave" a_e is the QED value 1.159652181764e-3 typed in (306), scaled by g_SO/0.5, so the default reproduces QED exactly.
  - g_SO is bisection-fit to the experimental value (237-268).
  - The main block adds QED-like loops plus HVP 69e-10 and HLbL 10e-10 on top of that "tree" (434-435), double-counting even though line 354 says loops are avoided. The HVP/HLbL magnitudes are muon-scale, not electron.
  - "Fermilab 2021 (E989)" labels the electron value (71-73, 405), but E989 is the muon experiment.
- Pass criterion: none. The calibrated run matches "by construction" (503).
- Violations:
  - electron_g2_solver.py:306-311 reports a QED/observed input as a One-Wave prediction.
  - :237-268 fits g_SO to the target.
  - :434-435 double-counts loop corrections.
  - :121 makes spin (point rotation) a dead constant, so the magnetic moment has no L/Point carrier. The node is incomplete (no Point/Path/Field).

## solvers/exoplanet_resonance_statistics.py (349 lines)
- Purpose / node IDs cited: "Priority 3.2" statistical test that exoplanet period ratios cluster at harmonic ratios through "cascade inheritance / phase-locking to stellar wake". No node IDs. Runs at import time.
- Point rotation: not present. Docstring line 20 says resonant period ratios are "same as tidal locking", which conflates orbit-orbit mean-motion resonance (Path) with spin-orbit locking (Point, e.g. Mercury 3:2).
- Path rotation: orbital periods are generated as numbers only (64-106). No dynamics and no L.
- Field: "stellar wake frequency ω0" is text only (18-19).
- Magnetism / Parent-child: not present.
- Hard-coded targets / refits: the data is SYNTHETIC. 60% of systems are generated with harmonic ratios injected (65-84), and the test then "detects" them. p_harmonic_random=0.15 is assumed (270). The chi² compares observed adjacent-window pairs (148) against expected all-pairs counts (263-266), which is inconsistent. "Galactic 16.6%, atomic 0.1%, molecular 0.12%" are quoted from other files (333-335).
- Pass criterion: p < 0.01 prints "CASCADE INHERITANCE IS ACTIVE" and "Unification is experimentally validated" (308-316, 344-347).
- Violations: exoplanet_resonance_statistics.py:65-84 + :308-316 + :347 claim validation from planted synthetic data. :20 conflates Path resonance with Point (tidal/spin) lock. :263-266 vs :148 has a pair-count mismatch.

## solvers/find_missing_physics.py (249 lines)
- Purpose / node IDs cited: lists hadron residuals and suggests kinetic, running-mass and EM corrections. Cites C-317 (224). Prints only; no computation beyond arithmetic.
- Point rotation: not present. "η_T·∇×v" twist/vorticity term is named in text only (149, 224).
- Path rotation / Field / Parent-child: not present.
- Magnetism: EM self-energy α Z²/R × 1.44 (122-129), standard Coulomb. No B or K_L.
- Hard-coded targets / refits: PREDICTED masses are hard-coded (42-51). Neutron 990.6 here conflicts with 967.3 in determine_oscillation_correction.py:37 and correction_formula_calibration.py:250. B+/B0 are a "crude estimate" (49-50).
- Pass criterion: none.
- Violations: none against the rotation rules. Line 101 says baryon errors are "25-150 MeV HIGH" while proton is LOW (913.5 < 938.3), so the text does not match the data. Prediction tables are inconsistent across files.

## solvers/galaxy_external_validation.py (108 lines)
- Purpose / node IDs cited: source-locked external evaluation of the Milky Way circular speed (DR3+ 2023, 45 rows) against GalaxyRotationConstantInherited. Cites A115/C320 (57). LIVE: .github/workflows/galaxy-validation.yml and test_galaxy_validation.py. The SHA-256 contract blocks input drift (25-35).
- Point rotation: not present.
- Path rotation: circular speed v_c(R) is the observable. The prediction is v_total = local + "inherited constant" velocity from galaxy_rotation_constant_inherited_velocity.py (49-55). That "inherited velocity" is a scalar speed added to the local speed (66, required_additive_speed). This file does not show whether it is transported; that is decided in the imported module (outside the slice).
- Field: inverse constraint `alpha_g * (K_L grad chi)_R = v_c^2/R` (86-90). The canonical form, explicitly labelled as a necessary empirical requirement and not a prediction.
- Magnetism: K_L is listed as an unknown "from independent magnetic observations" (90). kappa_R is not set. It does not claim B produces gravity. Consistent with the canonical rules.
- Parent/child: the inherited velocity is a contract-fixed constant per variant (49-51), so there is no fit in this file. The boost control shows that a uniform boost cancels from dispersion (76-85), with scope stated.
- Hard-coded targets / refits: velocity_scale_factor and mw_inherited_velocity_kms come from the contract (data/mw_dr3plus_contract.json). model_fit_performed=False (81). Whether those contract values were originally fit is not visible here.
- Pass criterion: relative RMS ≤ contract threshold → "PASS" discrepancy screen (74). It explicitly does not confirm the model (2-5, 75). The pass bit is spread (RMS), not rotation.
- Violations: none in this file. Watch item: the additive "inherited" scalar velocity (66) may be a raw parent-rate add. Check galaxy_rotation_constant_inherited_velocity.py.

## Slice summary
- Point rotation, canonical: none of the 14 files implements point rotation (L = Iω with an open/closed magnetic switch, start rules or inertia axes). The only spin-like object is electron_g2_solver.py:121 `circulation = 0.5`, a dead constant.
- Point rotation, violated:
  - electron_g2_solver.py builds a magnetic moment with no Point/L carrier and takes QED and experiment as inputs (306-311, 237-268).
  - exoplanet_resonance_statistics.py:20 conflates Path (orbital MMR) with Point (tidal/spin lock).
  - cascade_neural_router.py:208 does a raw scalar parent→child multiply with no transport.
- Magnetism → gravity: no file in the slice lets B produce gravity. galaxy_external_validation.py:86-90 states g via K_L grad chi in the canonical form and leaves K_L/kappa_R unset. coupling_constants_from_lattice.py:234-238 builds G numerologically from alpha and m_p/m_e, outside the g = -alpha K_L grad chi structure.
- Field: dispersion_validator.py and dispersion_visualizer.py have D-602 E-like/B-like branches as ±βk² only. The D-602 PASS is hard-coded (dispersion_validator.py:256-260), and the D-600 theory and update coefficients differ by a factor of 2 (63 vs 115-119).
- Hard-coded targets / refits:
  - Hadron chain: coherence_diagnostic, correction_formula_calibration, determine_oscillation_correction, determine_flavor_hierarchy (bare-except fake prediction 162-167) and find_missing_physics. They use inconsistent neutron predictions (967.3 vs 990.6).
  - coupling_constants_from_lattice.py:174 returns the observed m_e/m_p as "derived".
  - electron_g2_solver.py fits g_SO and scales the QED value.
  - cascade_neural_router.py uses refit lookup tables.
  - exoplanet_resonance_statistics.py plants synthetic harmonics and then detects them.
- Live vs legacy:
  - LIVE (CI workflows plus tests): driven_bulk.py (native-3d-lab.yml) and galaxy_external_validation.py (galaxy-validation.yml). Both are clean, with declared scope.
  - Tested but not CI-gated here: dispersion_validator.py (test_dispersion_validator.py).
  - Legacy/demo with print-only overclaims: cascade_neural_router, coherence_diagnostic, correction_formula_calibration, coupled_resonator_validator, coupling_constants_from_lattice, determine_flavor_hierarchy, determine_oscillation_correction, dispersion_visualizer, electron_g2_solver, exoplanet_resonance_statistics, find_missing_physics. Several import from a hard-coded /home/claude/one-wave-science path.
- Cross-references outside the slice: galaxy_rotation_constant_inherited_velocity.py (inherited velocity add, needs a transport check); hadron_knot_geometry.py and hadron_mass_predictor.py (VortexPhase ell/em, eta_T vorticity); data/mw_dr3plus_contract.json (origin of velocity_scale_factor); satellite_galaxy_validator_clean_systems.py (source of beta_0=0.248 and r_decay).
