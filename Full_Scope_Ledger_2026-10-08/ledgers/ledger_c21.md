# Code ledger, slice c21 (14 files, all read in full)

All paths under /home/user/One-Wave-Science/solvers/.

## proton_mirror_gate_calibration.py
- Purpose / node IDs cited: Fix a global energy scale lambda from 125 GeV "Mirror-Gate" energy and apply it to quark masses. Cites C-318, C-322, C-317, C-311, Book1_Ch02.
- Point rotation: not present. `omega_up = 0.2` GeV (L103) is a scalar energy-like "circulation frequency" used only in E = 0.5*omega^2*V (L106-107). It has no axis, no L = I omega, and no update law.
- Path rotation: not present.
- Field: not present. There is no curl, wake or chi.
- Magnetism: not present. There is no B, R, K_L or kappa_R.
- Parent/child: not present.
- Hard-coded targets / refits: The 125 GeV target is an input (L246, L327). `mirror_gate_work` = E_hold + 250*xi (L206), where the comment says k = 250 GeV was chosen "to produce ~125 GeV gate at xi ~ 0.5" (L204), so lambda is tuned by construction. The uncalibrated masses are typed in (L347-351) and compared against PDG values that are also typed in (L353-357). The proton PDG mass 938.3 is listed (L54). The cross term is a flat 10% (L173).
- Pass criterion: none. It prints lambda and the % error against PDG.
- Violations: Physics claim, not a rotation rule: a "prediction" is calibrated to an observed value chosen to hit that value (L204-206, L246). No rotation-rule violation, because no rotation is modelled.

## quark_mass_solver.py
- Purpose / node IDs cited: "Four-interaction" quark mass derivation for u/d/s/c/b/t. Cites C-318, C-322, C-317, C-311, C-316, Book1_Ch02.
- Point rotation: not present. "omega_circulation = omega_up*sqrt(mass_scale)" (L167-171) is a scalar energy density. There is no axis, no L, nothing that starts or stops it, and no gravity or magnetic coupling.
- Path rotation: not present.
- Field: not present.
- Magnetism: not present. The "spin-orbit" term is E_SO = g_SO*0.1*E_circ (L202), a scalar with no B.
- Parent/child: not present.
- Hard-coded targets / refits: This is circular. `mass_scale` for each flavor is the PDG mass ratio itself: 4.67/2.16, 95/2.16, 1270/2.16, 4180/2.16 and 172700/2.16 (L106-121). That ratio feeds omega (L171), kappa_T (L333), the radius (L132) and `confined_scale_factor = 0.0015*sqrt(mass_scale)` (L512). The output is then compared with the same PDG masses (L547-554, L592). lambda = 0.976 is hard-coded (L556, L660). The m_d/m_u "expected" ratio of 2.16 (L622) is hard-coded from the same PDG ratio (4.67/2.16 = 2.162).
- Pass criterion: none formal. Text output only.
- Violations: (Non-rotation) observed masses are used as inputs and then reported as predictions (L106-121 -> L592). It also has a runtime bug: L774-777 reference undefined `light_error` / `heavy_error` (NameError in `__main__`).

## quark_mass_spectrum_optimized.py
- Purpose / node IDs cited: Applies per-flavor radius exponents alpha "found by grid search" (L53-62). No node IDs.
- Point rotation, Path rotation, Field, Magnetism, Parent/child: not present.
- Hard-coded targets / refits: The per-flavor alpha values were fitted to PDG (L55-62) and are reported as an improvement against the same PDG values (L44-51, L100). The improvement figures are printed as fixed strings, not computed (L197-200). It imports quark_mass_solver, so it inherits the PDG-ratio inputs. The sys.path entry is hard-coded to `/home/claude/...` (L27).
- Pass criterion: none.
- Violations: (Non-rotation) refit reported as a prediction (L55-62, L197-200).

## quark_oscillation_analysis.py
- Purpose / node IDs cited: Exploratory correlation of hadron mass errors with quark "oscillation frequency" omega = kappa_T/m (L50-69). No node IDs.
- Point rotation: not present. omega is a scalar frequency, not a spin.
- Path rotation, Field, Magnetism, Parent/child: not present.
- Hard-coded targets / refits: Experimental hadron masses (L31-35), predicted masses (L37-41) and errors (L43-47) are all literals. Quark masses are PDG values (L24-28).
- Pass criterion: none. It prints a narrative only.
- Violations: none against the rotation rules. The analysis is post-hoc on hard-coded numbers.

## refine_weave_parameters.py
- Purpose / node IDs cited: Grid-sweeps sigma_T and kappa_T to fit proton, neutron and Lambda masses (L106-154). Cites C-317 in text (L207).
- Point rotation, Path rotation, Field, Magnetism, Parent/child: not present.
- Hard-coded targets / refits: Observed hadron masses are the fit target (L28-32, via HadronMassCalculator error_percent). alpha_strange = -0.150 and alpha_light = -0.05 are fixed refit values (L38, L126-127).
- Pass criterion: "SUB-PERCENT ACCURACY ACHIEVED" if the average nucleon error is below 1% (L177). This is a fit-residual criterion, not physics.
- Violations: (Non-rotation) a fit residual is presented as accuracy (L177-182).

## refined_correction_formula.py
- Purpose / node IDs cited: Least-squares fit of a correction term to 3 hadron errors, with 5 variants. No node IDs.
- Point rotation, Path rotation, Field, Magnetism, Parent/child: not present. omega = kappa_T/m is a scalar (L68-72).
- Hard-coded targets / refits: The observed errors are literals (L100-104), and so are EXPT and PREDICTED_BASE (L243-244). Variant E fits 2 free coefficients to 3 points (L182-187).
- Pass criterion: "SUB-1% accuracy" if the average corrected error is below 1% (L265).
- Violations: (Non-rotation) the fit uses the target data. There is also a sign bug: `error_obs` = pred - expt (L100-104), but the corrected mass is `base + correction` (L253). That doubles the error instead of removing it; it should be base - correction.

## reverse_engineer_mechanism.py
- Purpose / node IDs cited: Narrative diagnosis of baryon vs meson errors. Prints text only. No node IDs except C-317 in text (L202).
- Point rotation, Path rotation, Field, Magnetism, Parent/child: not present.
- Hard-coded targets / refits: Hadron masses and "predicted" values are literals (L37-47). The meson "errors" (L91-95) are hard-coded and never used, but the file still claims "<1 MeV" (L97).
- Pass criterion: none.
- Violations: none against the rotation rules. The meson-success claim has no computation behind it (L91-97).

## run_bulk_excitation.py
- Purpose / node IDs cited: Reproduction driver for bulk_excitation.BulkExcitation, a 3D FCC12 nonlinear complex field. It is labelled "TESTED HYPOTHETICAL CONSTITUTIVE MODEL; not canonical" (L42).
- Point rotation: not present. The field phase slope at the detector is measured (L31-33), but that is a field phase, not a body spin with L.
- Path rotation: not present.
- Field: The field is a complex 3-component order parameter on FCC12 (in bulk_excitation.py). There is no explicit curl or chi.
- Magnetism: not present. Note that `R` in bulk_excitation.py is `cycle_laplacian()` (bulk_excitation.py:34), a 3x3 phase-lock coupling. It is NOT the magnetic R and is not built from B.
- Parent/child: not present.
- Hard-coded targets / refits: none. There are no physical targets. The "limits" are declared (L48), and source hashes are recorded (L41).
- Pass criterion: none here. Tests live in test_bulk_excitation.py, run in CI by .github/workflows/native-3d-lab.yml.
- Violations: none.

## run_driven_bulk.py
- Purpose / node IDs cited: Applies a uniform force to a linear packet in BulkExcitation (via DrivenBulk), tracks centroid and energy balance, and checks the long-wavelength curvature against the analytic value 0.3 (L36-44).
- Point rotation: not present.
- Path rotation: not present. Centroid translation only (L23).
- Field: `curvature()` builds the dispersion from FCC offsets plus `phase_lock*m.R` (L39). As above, R is the cycle Laplacian, not magnetism.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none. The file states "No threshold is tuned to force 0.3" (L63) and "no measured/fitted physical mass" (L56). Source hashes are guarded (L54-55).
- Pass criterion: the energy-balance residual and curvature error are recorded. Pass/fail itself is in test_driven_report.py (CI).
- Violations: none. This is a live, CI-wired file (native-3d-lab.yml path filter).

## run_joint_response.py
- Purpose / node IDs cited: Reproduction driver for joint_boundary_response.JointResponse, a dimensionless reflecting FCC12 cavity scattering setup. It runs unitarity, ledger, Schur-inertia and energy-drift checks (L18-39).
- Point rotation: not present. There is a "carried_tensor" per mode (L12) and a boundary inertia tensor (L23-24), but no spin state, no L and no omega update.
- Path rotation, Field (curl or chi), Magnetism, Parent/child: not present.
- Hard-coded targets / refits: none. The file says "candidate inputs; no self-localized particle or GeV prediction" (L35).
- Pass criterion: the numeric checks dict (L38). Test assertions are in test_joint_boundary_response.py (CI).
- Violations: none.

## satellite_galaxy_validator_clean_systems.py
- Purpose / node IDs cited: Fits 4 parameters to 3 satellites (LMC, M32, M110) and declares "EXTENDED COMPRESSION EFFECT MODEL VALIDATED" (L193-197). Cites A-115 / Book 5 Ch1 (L17, L113), plus C-319 as a next step (L199).
- Point rotation: not present.
- Path rotation: Host "orbital velocity" times beta(r) is added linearly to v_local (L65-66). It is a scalar speed, with no L and no transport.
- Field: The wake is a scalar `v_wake = v_host*beta0*exp(-r/r_decay)` (L51, L65). There is no curl and no chi.
- Magnetism: not present. Magnetism is only promised as the next step (L199-201).
- Parent/child: The host-to-satellite "inheritance" is a raw scalar addition of speeds (L66), not omega_c + R_c^T omega_p.
- Hard-coded targets / refits: 4 free parameters (velocity_scale, beta0, r_decay_mw, r_decay_m31) are fitted by Nelder-Mead to 3 observed velocity dispersions (L86-122) and then reported as validation (L193-197). The model is over-determined by construction. The 0.0% M32 error in the docstring (L7) is a fit artefact. Sigma_obs = 2 km/s is assumed (L100).
- Pass criterion: none computed. The "VALIDATED" and "CONFIRMED" lines print unconditionally (L193-197).
- Violations: (1) The fit is reported as confirmation (L119-122 -> L193-197). (2) The scalar parent-to-child speed addition is untransported (L66). (3) The model compares a host orbital speed with the satellite's internal velocity dispersion, which mixes path rotation with internal kinematics (L70-71).

## satellite_galaxy_validator_corrected_gravity.py
- Purpose / node IDs cited: v_total = host rotation-curve speed + beta(r)*host orbital speed (L106-119). No node IDs.
- Point rotation: not present.
- Path rotation: The host rotation curve is a hand-shaped piecewise profile scaled to 244 km/s (L46-80). It is path speed only, with no L.
- Field: not present. There is no chi, so there is no grad chi. "Gravity" is a hand-shaped speed profile, not g = -alpha K_L grad chi.
- Magnetism: not present.
- Parent/child: Raw scalar addition, v_host_gravity + v_cascade (L119), with no transport.
- Hard-coded targets / refits: The 244 km/s scale is set so the profile gives about 220 km/s at the solar radius (L62-64, L79). 4 parameters are fitted to all satellites (L146-179). `velocity_scale_factor` is fitted but unused in this override (it is never read in L96-143).
- Pass criterion: mean error below 25% prints "STRONG VALIDATION" (L246-247).
- Violations: (1) Gravity is a curve fitted to observed rotation, not derived from grad chi (L46-80). (2) The scalar parent-child speed sum is untransported (L119). (3) The host circular speed (about 200 km/s) is compared with the satellite's internal `velocity_dispersion_kms` (L139-141), which is a category error. (4) Runtime bug: `self.mw_cascade_radius` and `self.m31_cascade_radius` (L123, L125) do not exist in the parent class, which only has `mw_ring_radius` (satellite_galaxy_velocity_validator.py:158-159). The module raises AttributeError at import during the optimisation at L178.

## satellite_galaxy_validator_distance_coupling.py
- Purpose / node IDs cited: beta(r) = beta0*exp(-r/r_decay) coupling. The docstring says satellites "inherit path curvature (rotation) but not direct gravity" (L5).
- Point rotation: not present.
- Path rotation: The "path curvature inheritance" is again a scalar v_host*beta added to v_local (L56-57), with no L.
- Field, Magnetism: not present.
- Parent/child: raw scalar addition (L57).
- Hard-coded targets / refits: 4 parameters are fitted to observed dispersions (L67-102). The file then claims "Path curvature inheritance confirmed" if the mean error is below 30% (L173-175).
- Pass criterion: mean error below 30% (L173).
- Violations: (1) The fit is reported as confirmation (L173-175). (2) The parent-to-child addition is untransported (L57). (3) Runtime bug: it reads `result['in_cascade']` (L46, L80), but the parent returns `in_ring` (satellite_galaxy_velocity_validator.py:215). This raises a KeyError at module-level optimisation (L98), so the file is dead.

## satellite_galaxy_validator_em_coherence.py
- Purpose / node IDs cited: Multiplies beta(r) by an "EM coherence" factor f_EM per host (L15, L174-175). No node IDs. It is superseded by `satellite_galaxy_validator_em_coherence_fixed.py`, which test_galaxy_validation.py imports instead.
- Point rotation: not present.
- Path rotation: Scalar v_host*beta*f_EM added to v_local (L191-192).
- Field: not present.
- Magnetism: B is a hard-coded per-host scalar (`b_field_strength_microG` 1.5 / 1.2, L65, L72) and is never used in any formula. f_EM is built from host-labelled constants: organization index 0.88 / 0.55, coherence scale 35 / 25 kpc, multipliers 0.65 and 0.15, and clamps (L65-75, L99-128). There is no B tensor, no W_B, no R, no K_L and no kappa_R. Magnetism here directly scales the speed added to a satellite. That makes magnetism act as a gravity / orbital-velocity contribution with no grad chi, which contradicts "magnetism does not become gravity; grad chi = 0 -> g = 0".
- Parent/child: raw scalar addition (L192).
- Hard-coded targets / refits: The f_EM constants are chosen per host to close the M31-vs-MW error gap that the docstring quotes (L5-7, L22-31). The 4 parameters are then fitted (L212-247). Previous errors of 64.8%, 11.7% and 53.1% are hard-coded into the printouts (L284, L302, L327).
- Pass criterion: host error spread below 20% prints "SUCCESS: EM coherence explains asymmetry" (L329-331). A mean error below 20% prints "publication-ready" (L340-342).
- Violations: (1) Magnetism-to-gravity: an EM factor directly scales the orbital velocity contribution with no grad chi (L174-175, L191-192). (2) Ad hoc host-specific "magnetic" constants with an unused B value (L65-75). (3) The untransported scalar parent-child sum (L192). (4) The same `in_cascade` KeyError bug (L181, L227), so the file is dead.

## Slice summary
- **Canonical point rotation:** No file in this slice implements Point rotation (G-749, L = I omega) canonically. None has a spin vector, inertia axes, an open/closed magnetic switch (dL/dt = 0 vs -gamma L), or a parent organization target rate. The "omega" in the quark files (quark_mass_solver L167-171, quark_oscillation_analysis L50-69, refined_correction_formula L68-72) is a scalar energy or frequency proxy, not rotation.
- **Rotation-related violations:**
  - All four satellite_galaxy_validator_* files treat host-to-satellite "inheritance" as a raw scalar speed addition, with no omega_c + R_c^T omega_p transport. They also mix path speed with internal velocity dispersion.
  - satellite_galaxy_validator_em_coherence.py lets an EM/B "coherence" factor directly add orbital velocity without grad chi. Magnetism acts as gravity, which violates the K_L rule.
  - satellite_galaxy_validator_corrected_gravity.py replaces g = -alpha K_L grad chi with a rotation curve fitted to observation.
- **Refits reported as predictions:**
  - quark_mass_solver.py uses PDG mass ratios as inputs and then compares the output with PDG (L106-121, L592).
  - The 125 GeV calibration is constructed to hit the target (proton_mirror_gate_calibration L204-206; quark_mass_solver L512, L660).
  - quark_mass_spectrum_optimized.py and refine_weave_parameters.py use grid-search fits.
  - refined_correction_formula.py also has a sign bug (L253).
  - In the satellite files, 4 parameters are fitted to 3 or more points and reported as "VALIDATED" or "CONFIRMED".
- **Runtime-dead files:**
  - quark_mass_solver.py `__main__` (NameError, L774).
  - satellite_galaxy_validator_corrected_gravity.py (AttributeError, L123).
  - satellite_galaxy_validator_distance_coupling.py and satellite_galaxy_validator_em_coherence.py (KeyError on `in_cascade`).
  - quark_mass_spectrum_optimized.py, quark_oscillation_analysis.py, refine_weave_parameters.py, refined_correction_formula.py and reverse_engineer_mechanism.py all hard-code sys.path to /home/claude/... (they still run from the solvers dir).
- **Live solvers:**
  - run_driven_bulk.py is CI-wired via .github/workflows/native-3d-lab.yml. run_bulk_excitation.py and run_joint_response.py are drivers for modules tested in the same CI.
  - These three are honest, target-free constitutive controls with no rotation or magnetism content.
  - Their `R` matrix is a 3-phase cycle Laplacian (bulk_excitation.py:34), not magnetic R. It must not be confused with K_L = I + kappa_R R.
- **Legacy or exploratory:** all quark/hadron files and all four satellite validators. The maintained satellite path is satellite_galaxy_validator_em_coherence_fixed.py, which is outside this slice.
- **Cross-references outside this slice:**
  - satellite_galaxy_velocity_validator.py: parent class, with the ring radius and hard-coded host orbital speeds of 110 and 170 km/s (L153-154).
  - satellite_galaxy_validator_em_coherence_fixed.py
  - hadron_knot_geometry.py and hadron_mass_predictor.py
  - bulk_excitation.py, driven_bulk.py and joint_boundary_response.py
  - MASTER_SOLVER_INDEX.md
