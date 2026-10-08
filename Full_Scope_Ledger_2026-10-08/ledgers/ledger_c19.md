# Code ledger, slice c19

All 10 files read in full. All are in /home/user/One-Wave-Science/solvers/. None of them models point rotation, magnetism through R/K_L, or gravity from grad chi. Line numbers refer to each file.

## /home/user/One-Wave-Science/solvers/mathematical_harmonic_proof.py
- Purpose / node IDs cited: claims to prove that "harmonic locking is inevitable" on a 1D lattice with boundaries (Dirichlet Laplacian + Gaussian well, lines 60-117). No node IDs.
- Point rotation: not present.
- Path rotation: not present.
- Field: scalar 1D wave operator H = Laplacian + V (lines 103-117). No curl, wake, chi or grad chi.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none from observation. Output "status": "Proven" is hard-coded (line 497).
- Pass criterion: `is_harmonic = error < 10%` (line 172). But every "RESULT ... ✓" line is printed unconditionally (lines 380, 406, 426, 450). **The run is broken.** The discrete Laplacian (lines 73-77) and V (line 97, always negative) give a negative-definite H. So `eigenvalues > 0` (lines 133, 191) removes every mode. I checked this by rebuilding the same matrices with numpy: max eigenvalue -9.68, 0 positive. `harmonic_analysis`, `numerical_vs_analytic` and `spatial_modes` therefore all come out empty, yet the script reports "Proven". The analytic claim ω_n = n·ω_1 is also wrong for a discrete lattice, which gives a sin(nπ/2N) dispersion (the docstring at line 182 even says so). Only `boundary_sharpness_effect` produces numbers, and it just fits ||V|| against σ (lines 268-294). That is a property of the Gaussian, not a coupling result. It also changes `self.boundary_sharpness` permanently (line 273).
- Violations:
  - lines 481, 509: claims "Gravity: Lattice cutoff -> metric curvature" / "Metric from lattice cutoff boundary". This conflicts with the canonical g = -alpha K_L grad chi, which is not metric curvature and not a boundary-cutoff effect. Narrative only.
  - lines 133/191 vs 380/406/426/450/497: reports a proof when the computed result is empty. The pass is not evidence.
  - Used by generate_publication_figures.py:332 (loads `mathematical_harmonic_proof_results.json`), so the empty or false result can reach published figures.

## /home/user/One-Wave-Science/solvers/maxwell_validator.py
- Purpose / node IDs cited: "Phase 3" check that E-like and B-like modes from D-602 satisfy Maxwell's equations (lines 1-7). Cites D-602.
- Point rotation: not present.
- Path rotation: not present.
- Field: the docstring promises a vector update with ∇(∇·ψ) - ∇×(∇×ψ) (line 50). The code is the scalar damped neighbour-average rule applied to two independent 1D complex arrays (lines 73-90). No curl is computed anywhere.
- Magnetism: "B" is not built from any curl, R or K_L. It is initialised as B = i·E (lines 69-70) and updated by the same scalar rule as E (lines 88-90), so B ≡ i·E for all time. No kappa_R, no tensor. Gravity is not addressed.
- Parent/child: not present.
- Hard-coded targets / refits: gamma and beta are retuned in main ("Reduced damping", "Increased coupling", lines 327-329) until checks pass.
- Pass criterion: (a) |E|/|B| ratio constant (line 112). This is trivially true because B = iE. (b) rms|E·B*| > 0.001 (line 141). (c) |ω/k - 1| < 0.5 (line 179). (d) momentum fluctuation < 10 (line 214). (e) energy max < 3× initial (line 253). None of these tests a Maxwell equation (no div or curl). "PASS" prints "Ready for publication" (line 355).
- Violations: none of the canonical point/magnetism rules is implemented. The magnetism content is fabricated: B is a phase-rotated copy of E (lines 69-70, 88-90). It is not a magnetic field and has no link to R = B⊗B - |B|²I/3. The "Maxwell validated" claim is unsupported. Not referenced by any other code (dead).

## /home/user/One-Wave-Science/solvers/measure_weave_components.py
- Purpose / node IDs cited: decomposes the C-317 "boundary-tension weave" E_weave = σ_T·A + κ_T·ΔΨ² + η_T·∇×v for proton, neutron and Λ (lines 3-21). Cites C-317.
- Point rotation: not present. The vortices carry only `phase_offset` (line 76). No ω, L or axis.
- Path rotation: not present.
- Field: the "η_T·∇×v" twist term is not a computed curl. It is vorticity := n_vortex / (2πR) (lines 117-121), multiplied by R³.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: measured hadron masses (lines 36-40). Quark masses (lines 30-34). base_radius 0.85 (line 68). alpha_light / alpha_strange -0.05 / -0.150 (line 50). kappa_T_base 1.5 with a √m_scale rule labelled "KEY" (lines 95-103). σ_T and η_T (line 91). `PREDICTED_STATIC` (lines 43-47) is defined but never used. The docstring units are GeV (lines 12-14), but the code adds the terms to MeV masses with no conversion (line 130).
- Pass criterion: none. Diagnostic only, reports error vs experiment.
- Violations: no canonical rotation or magnetism violation. Exploratory fit. Hard-coded external path `/home/claude/one-wave-science/solvers` (line 25). Dead (not imported).

## /home/user/One-Wave-Science/solvers/molecular_geometry_harmonic_resonance.py
- Purpose / node IDs cited: "Priority 3.1". Claims bond angles come from Circle-of-Fifths harmonic phase locking to a molecular wake (lines 3-24). No node IDs. Says it relies on satellite_galaxy_validator_clean_systems.py and atomic_spectra_cascade_resonance.py (lines 5-7).
- Point rotation: not present.
- Path rotation: not present.
- Field: "molecular wake" is used only in prose. No field is computed.
- Magnetism: not present.
- Parent/child: "Cascade inheritance (parent wake -> child motion)" (line 325) is printed only. Nothing is transported or added.
- Hard-coded targets / refits: observed angles (lines 36-79). The tetrahedral angle is the standard VSEPR geometry arccos(-1/3) (line 147), relabelled "emerges from harmonic resonance". 120° and 180° are returned as constants (lines 163, 186). Lone-pair factors 0.975 (line 180) and 0.95 (line 203) are hand-picked so that 109.47·f lands near 107° and 104.5°. `harmonic_angles` / `harmonic_ratios` (lines 108-126) are computed but never used in any prediction. The branch choice keys on the molecule name ("Water", "Ammonia", lines 240-245). Prints hard-coded cross-scale results "16.6%" and "0.1%" (lines 317-318).
- Pass criterion: mean % error tiers (lines 288-310).
- Violations: no canonical rotation or magnetism violation. Observed and standard-geometry values are reported as harmonic predictions. Runs at import time (module-level script). Cited in docstrings of exoplanet_resonance_statistics.py, galaxy_rotation_c319_corrected.py and coupling_constants_from_lattice.py as "harmonic grammar proven", but none of them imports it.

## /home/user/One-Wave-Science/solvers/multi_variable_correction_fit.py
- Purpose / node IDs cited: fits correction formulas to the hadron mass error (lines 3-15). No node IDs.
- Point rotation: not present. "ω" = kappa_T / m_quark (line 40) is a labelled ratio, not a spin rate.
- Path rotation: not present.
- Field: not present.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: EXPT masses and a hard-coded PREDICTED table (lines 106-107). Four least-squares fits with 3-4 free parameters to 3 data points (lines 157-216). These are exactly or near-exactly determined, so RMSE ≈ 0 by construction, and the "corrected mass" is then reported against experiment (lines 255-262). Formula 2's sign indicator is chosen after seeing the error signs (line 175).
- Pass criterion: none. Ranks fits by RMSE.
- Violations: no canonical rotation or magnetism violation. Pure refit of measured masses presented as a "physical interpretation" (lines 270-285). Hard-coded external sys.path (line 18). Dead.

## /home/user/One-Wave-Science/solvers/muon_g2_harmonic_validator.py
- Purpose / node IDs cited: "Level 1.2" harmonic-locking prediction of muon a_μ from electron a_e (lines 3-13). No node IDs.
- Point rotation: not present. g-2 is a spin magnetic moment, but no spin, L or precession is modelled.
- Path rotation: not present.
- Field: not present.
- Magnetism: not present. No B, R or K_L.
- Parent/child: not present.
- Hard-coded targets / refits: measured a_e and a_μ (lines 41-44). Prediction 1 is a_e·(1 + 0.001·ln(m_μ/m_e)) (lines 106-108). The 0.001 coefficient is unexplained and puts the result within about 0.01% of measured a_μ. Prediction 2 is a_e·1.0001 (line 149). `mass_correction`, `harmonic_correction`, `coupling_ratio` and `levels_up` are computed and discarded (lines 88, 92, 130-136). The σ denominator 0.43e-10 is hard-coded (line 158).
- Pass criterion: |error| < 1% / < 0.1% (lines 261-271). Ratio a_μ/a_e within 0.001 of 1 (line 273). That fails (ratio ≈ 1.0054), but the saved JSON conclusion still says "validating harmonic locking principle" (line 308).
- Violations: no canonical rotation or magnetism violation. Tuned constant reported as a prediction. The saved conclusion contradicts the computed pattern test. Dead.

## /home/user/One-Wave-Science/solvers/muon_g2_solver.py
- Purpose / node IDs cited: "Phase 5" universal g_SO test for the muon (lines 3-35). No node IDs.
- Point rotation: not present. Mentions "spin-orbit coupling" g_SO = 0.5 (lines 127-128) as a scalar only.
- Path rotation: not present.
- Field: not present. (P, E) "phase positions" (lines 120-125) are unused in any output except a print.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: **`muon_g2_from_universal_coupling` returns `self.constants.a_mu_exp_central`, the measured value (line 202)**, with the comment "use experimental value as calibration" (line 201). Everything computed above it (phase_factor, vp, hvp, hlbl, tree_muon; lines 181-198) is discarded. So deviation_OW = 0 and sigma_OW = 0 (lines 223, 227), and the script prints "One-Wave prediction closer to experiment" (lines 381-382). a_e_OW is also the measured a_e ("Empirically fitted", line 250). The docstring's numbers are inconsistent (3.5σ vs 5.4σ, 0.35 ppb vs 0.5 ppm, lines 7-19).
- Pass criterion: |sigma_OW| < |sigma_SM|. Guaranteed by returning the measurement.
- Violations: no canonical rotation or magnetism violation. Measured value input = reported prediction (line 202). Dead.

## /home/user/One-Wave-Science/solvers/neural_oscillations_validator.py
- Purpose / node IDs cited: "Level 1.5+". Claims EEG bands are an octave ladder from boundary harmonic locking (lines 3-17). No node IDs.
- Point rotation: not present.
- Path rotation: not present.
- Field: prose only ("Maxwell fields at neural boundaries", lines 157-161). "Coupling" = permittivity contrast × conductivity / width (line 141). This is a dimensional product that is never used afterwards.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: base 2 Hz and octave scale 2 chosen (lines 61-64). Clinical band ranges (lines 43-49). Literature-like peak list (lines 267-275), matched to the nearest ladder rung (lines 290-301). PAC ratios, including "1.5 (tritone)", are hard-coded descriptions (lines 178-203).
- Pass criterion: none formal. Labels "excellent/good/fair" by % error (line 301). The summary asserts the conclusion regardless (lines 321-332).
- Violations: no canonical rotation or magnetism violation. Narrative claims without a model. Dead.

## /home/user/One-Wave-Science/solvers/neutrino_mass_solver.py
- Purpose / node IDs cited: "Phase 5". Neutrino masses from "pressure coupling" (lines 3-32). No node IDs.
- Point rotation: not present.
- Path rotation: not present.
- Field: "pressure field gradient (gravity mediation)" coupling is a hard-coded list [0.1, 0.15, 0.5] (lines 130-133). No gradient is computed.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: measured Δm², mixing angles and the Σm bound (lines 56-78). Only m1 is "derived": (g_W/4π)·0.1·(1/137000)·1e3 (lines 199-214), with an "Empirical ... Rough estimate" suppression. **m2 and m3 are computed from the measured splittings (lines 226-227).** The "Verification via mass splittings" (lines 359-361) then just returns those inputs. Oscillation probabilities and PMNS use the measured angles directly (lines 253-295). The printout "Oscillation probabilities match KamLAND/T2K/Daya Bay data" (line 442) is circular.
- Pass criterion: none formal. Asserts the ✓ lines unconditionally (lines 432-435).
- Violations: no canonical rotation or magnetism violation. Lines 130-133 attribute neutrino mass to "coupling to pressure field (gravity mediation)". That is a mass-from-gravity-coupling claim with no grad chi / K_L structure. Narrative only, not canonical g. Also measured inputs are reported as outputs. Imported by standard_model_mysteries_unified.py:445 (live in that aggregator).

## /home/user/One-Wave-Science/solvers/observational_data_loader.py
- Purpose / node IDs cited: data-source abstraction for galaxy validators (lines 3-21). No node IDs.
- Point rotation: not present.
- Path rotation: supplies galaxy rotation-curve tables v(r) (lines 90-103, 114-125, 268-303). These are orbital (path) speeds. The loader carries no L and makes no claim about it, which is consistent with the canon (path carries no L).
- Field: not present.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: `MastGalaxyRotation` is a hard-coded table (lines 259-306) labelled "Real observational data" with source "MAST (NASA HEASARC + ...)". No archive is ever queried. Because source != "SYNTHETIC", `is_real` = True (line 384). The values differ from the SYNTHETIC table and from the cited papers' tabulations, and their provenance is unverified (the Chemin et al. 2009 citation also gives "AJ 142, 31"; the real paper is ApJ 705, 1395). The cache key uses Python `hash()` of a string (line 184). That hash is salted per process, so the cache never hits across runs and leaves one new /tmp file per run.
- Pass criterion: n/a (loader).
- Violations: no canonical rotation or magnetism violation. Provenance mislabel: hand-entered numbers flagged is_real=True (lines 262-266, 286-290, 384). This is live. It is imported by galaxy_rotation_validator.py:21, galaxy_rotation_c319_corrected.py:28, galaxy_rotation_cascade_wake_validator.py:19 and pressure_model_calibrator.py:27, and watched by .github/workflows/galaxy-validation.yml:7,16. So every downstream galaxy "real data" result rests on unsourced tables.

## Slice summary
- **Canonical point rotation:** none of the 10 files implements it. None has ω, L = Iω, an inertia axis, an open/closed magnetic switch (dL/dt = 0 vs -γL), parent→child transport (ω_c + R_cᵀω_p), R = B⊗B - |B|²I/3, K_L, kappa_R, or g = -α K_L grad χ. None has a Point/Path/Field split, so by the canon every "node" here is incomplete. That is a gap, not an active contradiction.
- **Conflicts with the canon (narrative):**
  - mathematical_harmonic_proof.py:481,509: gravity as "lattice cutoff -> metric curvature".
  - neutrino_mass_solver.py:130-133: mass via "pressure field (gravity mediation)" coupling.
  - maxwell_validator.py:69-70,88-90: "B" is i·E, not a magnetic field, while the file claims Maxwell validation.
- **Integrity faults:**
  - mathematical_harmonic_proof: every eigenvalue is negative, so all results are empty, yet "Proven" is printed. Its JSON feeds generate_publication_figures.py.
  - muon_g2_solver:202 returns the measured a_μ as the prediction.
  - muon_g2_harmonic_validator: tuned 0.001 coefficient. Its saved conclusion contradicts the failed ratio test.
  - neutrino_mass_solver:226-227 derives m2 and m3 from the measured splittings.
  - multi_variable_correction_fit: 3-4 parameter fits to 3 points.
  - molecular_geometry: hand-picked lone-pair factors 0.975 and 0.95.
  - observational_data_loader: hand-entered tables flagged is_real=True.
- **Live vs dead:**
  - Live:
    - observational_data_loader.py: imported by 4 galaxy solvers and a CI workflow.
    - neutrino_mass_solver.py: imported by standard_model_mysteries_unified.py.
    - mathematical_harmonic_proof.py: its output JSON is consumed by generate_publication_figures.py.
  - Dead or standalone: maxwell_validator, measure_weave_components and multi_variable_correction_fit (both with a broken /home/claude sys.path), molecular_geometry_harmonic_resonance (cited in docstrings only), muon_g2_harmonic_validator, muon_g2_solver, neural_oscillations_validator.
- **Node IDs in slice:** C-317 (weave energy; measure_weave_components.py:8) and D-602 (E/B modes; maxwell_validator.py:5). Neither bears on point rotation or magnetism as implemented.
- **Cross-refs outside slice:** hadron_knot_geometry.py (vortex phase offsets), satellite_galaxy_validator_clean_systems.py and atomic_spectra_cascade_resonance.py ("cascade inheritance" parent→child claims, worth auditing for transport), galaxy_rotation_*.py and pressure_model_calibrator.py (consumers of the loader), standard_model_mysteries_unified.py, generate_publication_figures.py.
