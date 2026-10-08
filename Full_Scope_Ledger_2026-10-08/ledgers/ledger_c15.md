# Code ledger: slice c15 (11 files, all read in full)

## /home/user/One-Wave-Science/solvers/algorithm_zero_galaxy_validation_comprehensive.py
- Purpose / node IDs cited: Phase 2 "validation" of a 3D "D-409" volumetric lattice (imported from `algorithm_zero_3d_volumetric_lattice`, outside slice) against 5 hard-typed galaxy rotation curves (NGC 628, NGC 3198, NGC 2403, M31, M101; L64-137) plus a random toy "cluster" (L301-335). Node cited: D-409 only (L4, L21).
- Point rotation: not present. No spin, omega, L, attitude or inertia anywhere.
- Path rotation: galaxy "rotation curve" v(r) comes from `lattice.measure_rotation_velocity()` (L150-152, external). Cluster galaxies get a random scalar `v_orbital = 100 + 50*randn` (L323); no direction and no L. It is a ride with no point-rotation partner.
- Field: `inject_galactic_wake(amplitude=0.5)` plus `run_equilibration(50)` (L398-399), external. No curl, no chi, no grad chi.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: the observed curves are typed in by hand (L70-136) with approximate round numbers. Halo NFW parameters m200, c200 and rho0 (L74-136) are copied into the output (L289-293) but never used. The virial mass uses Newtonian `G = 4.3e-3` (L365-369), which is standard gravity and not the canonical g = -alpha K_L grad chi. One lattice with the same parameters is built for every galaxy (L397-399), so the per-galaxy chi-squared tests a single fixed curve against different data. dof = n-3 is assumed (L186).
- Pass criterion: chi-squared p-value > 0.05 means "GOOD" (L278). The conclusion string "validated against multiple real galaxy datasets" is hard-coded (L472) whatever the result. Results are written to the stale path `/home/claude/one-wave-science/...` (L475). The p-value is spread, not point rotation.
- Violations:
  - L365-369: Newtonian G virial mass is used as a gravity law instead of g = -alpha K_L grad chi.
  - L472: the success conclusion is hard-coded regardless of the fit.
  - Galaxy "rotation" is path rotation only. The point rate is missing, so each node is incomplete (G-749/G-769 trio).
  - L323: cluster velocities are random inputs, then reported as dynamics.

## /home/user/One-Wave-Science/solvers/algorithm_zero_phase3_parameter_tuner.py
- Purpose / node IDs cited: grid search that tunes the Phase 3 pressure-tensor knobs to reach target curve shapes (an inner gradient of 30+ km/s/kpc, an outer plateau within ±25, a range of 100-250; L4-7, L41-59). No nodes are cited.
- Point rotation: not present.
- Path rotation: only "rotation velocity" output from the lattice (L106, L116).
- Field: delegated to PressureTensorLattice.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: the whole file is a refit to observed rotation-curve shape targets (L41-59, L258-260).
- Pass criterion: lowest penalty score (L58, L220).
- Violations / defects:
  - The API does not match `algorithm_zero_phase3_pressure_tensor.py`, so the file cannot run.
    - L67-70 passes `n_r`, `n_theta`, `n_z`, `r_disk`, `z_height` and `rho_0`. The dataclass fields are `radius_points`, `theta_points` and `height_points`, so this raises a TypeError.
    - L100-103 passes arguments to `enable_nonlinear_saturation(saturation_amplitude=...)` and `enable_asymmetric_mass_coupling(gradient_response_strength=...)`, but both methods take no arguments.
    - L110/L113 calls `run_equilibration(n_steps=)` and `run_evolution(n_steps=)`, but the keyword is `steps`.
    - L107/L116-121 treats the returned dict as an ndarray.
    - L126/L139 reads `lattice.radii`, which does not exist.
  - Each trial's exception is swallowed (L216-217), so the tuner reports "No results yet" or empty output instead of failing. The file is dead.
  - Its purpose (fitting curve shape to observation) is a refit, not a prediction.

## /home/user/One-Wave-Science/solvers/algorithm_zero_phase3_pressure_tensor.py
- Purpose / node IDs cited: replaces the Phase 2 scalar psi with a 6-component "pressure tensor" on an (r, theta, z) grid. It adds saturation and grad rho coupling, and keeps "universal" gamma = 0.05 and beta = 0.15 (L50-51). No nodes are cited.
- Point rotation: not present. No omega, L or inertia. The docstring says p_thetatheta "-> angular momentum" (L284), but nothing computes L.
- Path rotation: `measure_rotation_velocity` (L280-328) builds `v = 50 + 50*mean|p_thth| + 80*phase_gradient + 30*shear` and clips it to [20, 400] (L313-320). The 50 km/s floor, the scale factors and the clip are hand-set, and the result carries no L.
- Field: neighbour "Laplacian" with periodic `np.roll` on all axes, including radial and vertical wrap (L162-184). The update is p_new = p + (1-gamma)(p - p_prev) + beta*8*lap + 0.1*coupling (L264-269). Coupling is either 0.1*rho (L229) or grad rho times hand factors 0.5, 0.1 and 0.3 (L216-226). The wake is seeded as cos(theta) in p_thth for r < 3 (L135-142). No curl, no chi, no grad chi.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: `volumetric_coupling_enhancement = 8.0` (L54). The velocity map constants (L313-320) are tuned to give km/s in the galaxy range. Disk scale lengths 6 kpc and 1 kpc (L95-96). `self.rho[i_r]` is zeroed at r = 0 (L108).
- Pass criterion: none quantitative. `main` prints hard-coded check marks (L498-501). "is_stable" means max|p| < 1e3 (L338).
- Violations:
  - Rotation velocity is manufactured from a hand-set floor plus clip (L313-320), not from point or path dynamics.
  - L498-501: unconditional "✓" success claims.
  - Rotation is path-only with no point rate (incomplete trio).
  - Periodic radial and vertical boundaries (L172-181) are unphysical but not a canonical-rule breach.

## /home/user/One-Wave-Science/solvers/algorithm_zero_physics_engine.py
- Purpose / node IDs cited: One-Wave update ψ ← ψ + (1-γ)(ψ - ψ_prev) + β(⟨ψ_j⟩ - ψ) (L11, L155-168). It also has a six-phase "Algorithm Zero" cycle (L37-44, L203-269) and a multiscale cascade with a "gravity wake" parent→child (L170-176, L275-351). No node IDs are cited.
- Point rotation: not present. No omega, L or attitude.
- Path rotation: not present. `parent_velocity` appears only in `compute_wake_field` (L288-330), which is never called.
- Field: scalar complex ψ with a 26-neighbour average (L144-153). The "wake" is |parent field| masked behind the velocity direction (L306-330, unused). No curl, no chi, no grad chi.
- Magnetism: not present.
- Parent/child: the parent field is zoomed to the child grid, normalised to max 1, and **added raw** as `psi_new + wake_strength * interpolated*strength` (L171-176, L190-197), with strength 0.3 hard-coded (L439). Nothing is transported. The comment calls it "gravity wake nesting" (L170). `compute_phase_lock_frequency` returns the parent frequency in both branches (L347-351), which is a tautological "perfect phase-lock".
- Hard-coded targets / refits: PhysicalScale frequency ratios are typed in by hand (L48-54).
- Pass criterion: `validate_algorithm_zero` hard-codes all five checks to True (L561-567). Only `harmonic_identity` is re-tested, and it passes if any FFT peak exists (L571-573).
- Violations / defects:
  - L442-443: `field_prev = field.copy()` is set before `step`, so the momentum term (1-γ)(ψ - ψ_prev) is always 0. The core update rule is not executed as written.
  - L428-432: the phase manager is passed a float (field.real[0,0,0]) as `current_phase`, and its result is discarded. The six-step cycle never runs, yet "six_step_cycle" reports PASS (L562).
  - L171-176: the parent→child rate/field is added raw with no transport. This violates "transport first, then add" in spirit (here it is a scalar field, not omega).
  - L170/L275: "gravity wake" is driven by |ψ| with no grad chi. It is not g = -alpha K_L grad chi.
  - L561-567: the validation is hard-coded True.

## /home/user/One-Wave-Science/solvers/analyze_lambda_problem.py
- Purpose / node IDs cited: diagnostic breakdown of why the hadron "weave" model underpredicts the Lambda mass. It uses `hadron_knot_geometry` (outside slice). No nodes are cited.
- Point rotation: not present. ω here is κ_T/m (L104), a per-quark oscillation frequency, not spin. Mass enters as 1/ω, an inertia-like resistance.
- Path rotation: not present.
- Field: not present. Weave energy terms come from the external `WeavingEnergyCalculator` (L66-71).
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits:
  - PDG masses 1115.7 (L89), 938.3 and 939.6 (L172-173) are targets.
  - Binding energies -8.0 (L77, L83), -5.5 (L169) and -10.5 (L170) are hard-coded per hadron.
  - L135-142 back-solves the κ_T needed to hit the observed Lambda mass, which is an explicit refit.
  - Docstring numbers (L14-20) and the printed status "~2-10% error ✓ / ~43%" (L190-191) are static strings, not computed.
- Pass criterion: none; the file is diagnostic only.
- Violations:
  - L169-170: per-hadron binding constants are typed in by hand.
  - L135-142: inverse-fit to the measured mass.
  - L190-191: hard-coded status claims.
  - L29: stale sys.path `/home/claude/...`.

## /home/user/One-Wave-Science/solvers/asymmetric_oscillation_effects.py
- Purpose / node IDs cited: pairwise quark mass-asymmetry table for p, n and Λ. No nodes are cited.
- Point rotation: not present. ω = κ_T/m per quark (L67-68), with κ_T = 297 MeV hard-coded (L50).
- Path rotation, Field, Magnetism, Parent/child: not present.
- Hard-coded targets / refits:
  - Error values {p: -23.9, n: +27.7, Λ: +203.5} MeV are typed in (L140-144), not computed.
  - The narrative percentages -2.5% (L168) and +18.2% (L183) are static. They also contradict the 43% "underpredicted" figure in analyze_lambda_problem.py (L191 there).
  - Local quark masses up 2.16, down 4.67, strange 95.0 (L36-40) shadow the imported module's table.
- Pass criterion: none.
- Violations: L140-144 uses hard-coded "errors" as data for a correlation claim. L31 has a stale path.

## /home/user/One-Wave-Science/solvers/atomic_spectra_cascade_resonance.py
- Purpose / node IDs cited: "Universal framework proof" that hydrogen levels come from "cascade resonance / phase-locking to nuclear wake" (L1-23). No nodes are cited.
- Point rotation: not present. No electron spin or L, and `omega_0_au = 1.0` is unused (L78).
- Path rotation: not present. "Orbit" appears only in prose.
- Field / Magnetism / Parent/child: not present. The "nuclear wake" is not modelled.
- Hard-coded targets / refits: `resonance_scale = E_ionization_eV = 13.6` (L37, L82) and E_n = -13.6 Z²/n² (L105). This is the observed Rydberg formula entered as input, then the observed Rydberg wavelengths are "predicted" (L119-148). It is circular.
- Pass criterion: mean wavelength error < 0.5% means "PERFECT ... UNIVERSAL FRAMEWORK CONFIRMED" (L215-218). Any error comes only from rounding hc (L112-114).
- Violations:
  - L37/L82/L105: the observed 13.6 eV/n² is the input, and the match is reported as a framework confirmation (L216-218, L255-258).
  - The whole file runs at import time with no main guard (L161-260).

## /home/user/One-Wave-Science/solvers/atomic_spectroscopy_validator.py
- Purpose / node IDs cited: "Level 0 harmonic locking". It claims Helmholtz decomposition at the atomic boundary explains spectra (L1-13). No nodes are cited.
- Point rotation: not present. Fine structure is attributed to "∇×A" in prose (L219, L230, L260), but no spin or L is computed.
- Path rotation: not present.
- Field: no field is computed. Helmholtz (∇φ + ∇×A) appears in strings only (L240-262).
- Magnetism: not present beyond prose. No B and no R.
- Parent/child: not present.
- Hard-coded targets / refits:
  - Measured R_∞ and R_H are inputs (L49-50), and the standard Rydberg formula is the "prediction" (L81-97).
  - "Helmholtz correction" is `base * 1e-5 * harmonic_scaling` with `boundary_geometry_factor = 0.00001` typed in (L120-125). The comment claims it "emerges from field decomposition".
  - Fine-structure "prediction" is α²(Z/n)³·109700 (L223), an approximate textbook formula. The computed value is never compared or printed (only the measured value is printed, L357).
  - Several "measured" wavenumbers are wrong: Paschen-β 7800 should be about 7799.3, Brackett 2469 about 2467.8, and Lyman-α 82258.919 is fine. These are minor.
- Pass criterion: none computed. The "VERIFICATION ✓ No free parameters" block is static text (L411-416), even though L120 is a free parameter.
- Violations:
  - L120: a free parameter is inserted while "no free parameters" is claimed (L397, L414).
  - L49-50/L81-97: the measured Rydberg constant is used as input and reported as validation.
  - L408-409 claims "Level 3+: Gravity from lattice cutoff", which is not the canonical g = -alpha K_L grad chi (prose only).
  - L433 writes JSON to the CWD (outside this audit; not run).

## /home/user/One-Wave-Science/solvers/boundary_condition_analysis.py
- Purpose / node IDs cited: traces hadron boundary radius R(m_scale) and κ_T(m_scale) for p, n and Λ (L1-29). No nodes are cited. Note that "R" here is a boundary radius, not the canonical magnetic tensor R.
- Point rotation, Path rotation, Field, Magnetism, Parent/child: not present.
- Hard-coded targets / refits:
  - base_radius 0.85 fm (L61), α = -0.05 (L62), and κ_T_base = 0.297 GeV "calibrated via binary search" (L66, L17) are fitted constants.
  - The surface energy prints σ_T·A labelled "MeV" while σ_T is in GeV/fm² (L179-182), a unit mislabel by 1000×.
- Pass criterion: none; diagnostic only.
- Violations:
  - L66: a calibrated κ_T is inherited from a fit to hadron masses.
  - L182: unit error in the printout.
  - L32: stale path.
  - The `HadronMassCalculator` import (L36) is unused.

## /home/user/One-Wave-Science/solvers/bulk_excitation.py
- Purpose / node IDs cited: self-described "hypothetical nonlinear closure, separate from the canonical memory update" (L1). It is a 4-component field on a periodic FCC12 lattice with a split-step NLS evolution (L92-103), a fixed-norm stationary solve (L77-90) and diagnostics. No nodes are cited.
- Point rotation: not present. No omega, L or attitude. The "phase_lock" term is a 4-cycle graph Laplacian coupling between components (L34, L49; `cycle_laplacian` in joint_boundary_response.py L27-31), not rotation.
- Path rotation: not present.
- Field: scalar 4-component amplitudes. Discrete Laplacian over 12 FCC offsets (L48), focusing -ρ and saturation +ρ² nonlinearity (L55, L96). No curl, chi or grad chi.
- Magnetism: not present. `self.R` (L34) is a cycle Laplacian matrix and unrelated to the canonical magnetic R (name collision only).
- Parent/child: not present.
- Hard-coded targets / refits: none against observation. Coefficients are model inputs (L13-18). It is honest about being hypothetical (L1, L78).
- Pass criterion: none internal. It reports conservation errors for norm and energy (L130-137) and the stationary residual (L89). Checks are numerical, with no physics claim.
- Violations: none against the canonical rules. The file is clean numerical code with input validation (L22-28, L79, L93, L124-127). It is live, used by run_bulk_excitation.py, test_bulk_excitation.py and others.

## /home/user/One-Wave-Science/solvers/calibrate_coherence_parameters.py
- Purpose / node IDs cited: grid sweep of κ_T_base, σ_T and binding_correction_strength to minimise mean |error %| on p, n and Λ masses (L1-8, L59-86). No nodes are cited.
- Point rotation, Path rotation, Field, Magnetism, Parent/child: not present.
- Hard-coded targets / refits: PDG masses 938.3, 939.6 and 1115.7 (L17-21) are the fit targets. Three free parameters are fit to three data points (L60-62), so it is fully determined by observation. Any resulting "prediction" of these masses is a refit. The objective uses absolute error (hadron_mass_predictor.py L521-522), so signs do not cancel.
- Pass criterion: minimum average error.
- Violations: L60-86 fits 3 parameters to 3 measured masses. Any downstream report of these masses as predictions would be a refit. L11 has a stale path.

## Slice summary

**Point rotation canonically implemented:** none. No file in c15 represents spin, omega, L = Iω, attitude, inertia axes, an open/closed magnetic switch (dL/dt = 0 vs -γL), parent-organization target rates, or the R_p R_c / ω_c + R_cᵀω_p transport.

**Files that violate or are incomplete:**
- **Galaxy files** (`algorithm_zero_galaxy_validation_comprehensive.py`, `algorithm_zero_phase3_pressure_tensor.py`, `algorithm_zero_phase3_parameter_tuner.py`):
  - "Rotation" is path-only (the v(r) ride), manufactured from hand-scaled maps with a floor and clip (pressure_tensor L313-320). No point rate exists, so each node is incomplete.
  - The comprehensive validator uses Newtonian G for virial mass (L365-369) instead of g = -α K_L ∇χ.
  - Success conclusions are hard-coded in both the comprehensive validator (L472) and pressure_tensor (L498-501).
  - The tuner refits to observed curve shapes and is API-broken.
- **algorithm_zero_physics_engine.py**:
  - The parent→child "gravity wake" is added raw with no transport (L171-176).
  - "Gravity" is driven by |ψ|, not ∇χ.
  - The momentum term is zeroed by a bug (L442-443).
  - The six-step cycle is never applied (L428-432).
  - All validations are hard-coded True (L561-567).
- **Atomic files**: the observed Rydberg formula or constant is input, then reported as a prediction:
  - atomic_spectra_cascade_resonance.py L37/L82/L105.
  - atomic_spectroscopy_validator.py L49-50, plus a free 1e-5 factor at L120 alongside a "no free parameters" claim.
- **Hadron files** (`analyze_lambda_problem.py`, `asymmetric_oscillation_effects.py`, `boundary_condition_analysis.py`, `calibrate_coherence_parameters.py`): measured masses are fit targets. They use typed-in binding constants and error tables (analyze L169-170; asymmetric L140-144) and fit 3 parameters to 3 masses (calibrate L60-86). Their status claims contradict each other (43% vs 18.2% for Λ).
- **Clean:** `bulk_excitation.py` (labelled hypothetical; no canonical-rule breach).

**Live vs dead/legacy:**
- **Live:** `bulk_excitation.py`, imported by run_/test_/plot_bulk_excitation, test_driven_bulk and others.
- **Dead:**
  - `algorithm_zero_phase3_parameter_tuner.py` (broken API).
  - `algorithm_zero_galaxy_validation_comprehensive.py` (writes to the nonexistent `/home/claude/...` path).
  - The hadron diagnostics (stale `/home/claude/...` sys.path; run only if the solvers dir is the CWD).
- **Legacy demos:** `algorithm_zero_physics_engine.py` and `algorithm_zero_phase3_pressure_tensor.py` are referenced by test_algorithm_zero_complete.py, standard_model_mysteries_unified.py, a111_closure_validator.py and the native_3d test_lab. They are demo-grade, not canonical solvers.

**Cross-references outside the slice:**
- algorithm_zero_3d_volumetric_lattice.py (D-409 lattice; owns the galaxy rotation-velocity extraction).
- hadron_knot_geometry.py and hadron_mass_predictor.py (weave energy and the κ_T phase-locking).
- joint_boundary_response.py (cycle_laplacian, OFFSETS).
