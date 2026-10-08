# Code ledger: slice c22

All paths are relative to `/home/user/One-Wave-Science/solvers/`. All 10 files were read in full.

## satellite_galaxy_validator_em_coherence_fixed.py
- Purpose / node IDs cited: It subclasses `SatelliteVelocityPredictor` and multiplies the host-wake coupling by an "EM field coherence" factor f_EM. No node IDs are cited directly; it inherits the A-115 / Book 5 Ch1 framing from the base file. An evidence warning at L3-6 says the validation language is unsupported (`INVALID_COMPARISON`, L192, L266-269).
- Point rotation: not present. No spin, omega, L or attitude anywhere.
- Path rotation: A scalar `v_host * beta_r` "inherited orbital velocity" is added to v_local (L163-164). It carries no L. It is not a real orbit or turning model.
- Field: There is no curl, chi or grad chi. The "wake" is the scalar `beta_0*exp(-r/r_decay)` (L140).
- Magnetism: `EMFieldCoherence` (L49-103) is a hand-set scalar per host: baseline 1.0/0.7, scale 50/30 kpc, location factor 1.0/0.65 (L69-81). It is clipped to [0.3, 1.2] (L103). There is no B, no R, no W_B and no K_L tensor. This "B+E coherence" scalar directly scales the gravitational-wake coupling (L146-149). So magnetism modulates the gravity-like term, and grad chi is never involved.
- Parent/child: The host rate is added raw as a scalar velocity (`v_local + v_inherited`, L164). There is no rotation transport.
- Hard-coded targets / refits: These were fit to observed dispersions of "clean" satellites and then reused: velocity_scale_factor 38.69, beta_0 0.2480, r_decay 51.5/46.2 kpc (L118-121, L25-29). The coherence constants (L69-81) are chosen to explain the M31/MW asymmetry.
- Pass criterion: There is no pass bit, only mean percent error per host and the M31-MW spread (L249-256). It is explicitly labelled `INVALID_COMPARISON`.
- Violations:
  - L146-149 and L100: magnetism (an EM coherence scalar) changes the gravity/wake coupling. Canonically, magnetism does not become gravity: g = -alpha K_L grad chi, and K_L must be a tensor built from R.
  - L164: the parent rate is added raw. Canonically it is transported first, then added.
  - L118-121: refit observed parameters are reused as "fixed predictions".
  - The node has no Point and no Field component, so it is incomplete.

## satellite_galaxy_velocity_validator.py
- Purpose / node IDs cited: The "Extended Compression Effect" satellite-velocity predictor (A-115 / Book 5 Ch1, L10, L140). It also holds the satellite datasets (L53-130). Line numbers below are the file's own.
- Point rotation: not present.
- Path rotation: `v_wake = v_host*0.3` inside r_ring (L202) is added to v_local (L203). Host "orbital velocities" are 110/170 km/s (L153-154). It carries no L.
- Field: The compression ring is a step function (`in_ring = r < r_ring`, L198). There is no chi, grad chi or curl.
- Magnetism: not present.
- Parent/child: The host scalar velocity is added raw to the satellite velocity (L203). There is no transport.
- Hard-coded targets / refits:
  - The host velocities are "fitted" (L152-154).
  - velocity_scale_factor is 39.23, "from MW/M31 fitting" (L162).
  - The ring radii are chosen so that LMC/SMC and M110 fall inside (L158-159).
  - The local term `log10(M)/10*scale` (L194-195) is not physical.
- Pass criterion: mean in-ring error below 30% prints "STRONG VALIDATION" (L363-364). Out-of-ring satellites are excluded from validation (L346-347).
- Violations:
  - L203: the parent rate is added raw.
  - L162 and L153-159: fitted parameters are presented as predictions.
  - L363-371 and L400-404: the file claims "PROVE" / "Dark matter = compression ring" on a criterion that excludes failures.
  - Point and Field are missing.
  - The output compares orbital velocity to internal dispersion. The sibling file now flags this as an invalid observable mapping.

## standard_model_mysteries_unified.py
- Purpose / node IDs cited: An orchestrator for 14 "Standard Model mysteries" with keystones (W2 gravity, flavor, lattice asymmetry) and cascades. It cites A-115 / Book 5 Ch1 (L204).
- Point rotation: not present.
- Path rotation: not present.
- Field: The pressure field is P = 1/(r+0.1) (L192), with Ricci from Laplacian(P) (L195). Gravity is a = -grad P (docstring L169). The "extended compression signature" is the mean |grad P| (L206-207). The asymmetry keystone takes `np.angle(field)` std as "CP violation" (L364-370). There is no chi, K_L or curl.
- Magnetism: not present. g-2 is the textbook QED series (L636, L668-675), not a field model.
- Parent/child: not present.
- Hard-coded targets / refits. Inputs and constants are echoed back as predictions:
  - Superfluid expansion / dark energy 0.68 (L211, L419, L428) is compared to 0.68.
  - Extended compression 0.27 is compared to 0.27 with `error_percent: 0.0` (L856-862).
  - Higgs mass is `125.0 + (pressure_max-1)` (L568) against 125.1. The fallback returns 125.1 (L585).
  - Proton radius uses base_radius 0.84 against 0.8414 (L714). The fallback returns 0.8414 (L734).
  - Confinement is 200*exp(-dα) against 200 (L605-611).
  - Muon g-2 includes measured HVP 0.6933e-3 (L672). The fallback hard-codes the prediction (L694).
  - Neutrino fallbacks hard-code errors of 8% and 0.5% (L488-493).
  - `gravity_acceleration_magnitude: 9.81` is hard-coded (L217, L233).
  - Every keystone failure path substitutes "synthetic results" and still marks the cascades "success" (L227-237, L303-313, L385-395, L484-486, L582-591, L731-738).
  - A hard-coded output path to /home/claude/... (L40, L1024).
- Pass criterion: `status == "success"` counts as "solved" (L931, L960). "Converged" means error below 10% against the echoed constants (L940, L961).
- Violations:
  - L211, L855 and the "superfluid_expansion" cascade conflict with "No expansion, no scale factor" (the dark-energy-as-expansion framing).
  - L192 and L206: gravity is taken from a pressure gradient with no K_L / chi structure.
  - L217: g = 9.81 is hard-coded.
  - L568, L714 and L856-862: observed values are reported as predictions (including 125 GeV).
  - The synthetic fallbacks fabricate success.
  - Point, Path and Field are all missing.

## superconductor_phase_transition_validator.py
- Purpose / node IDs cited: "Level 1.3+" boundary-coupling reinterpretation of superconductivity. No node IDs are cited.
- Point rotation: not present.
- Path rotation: not present.
- Field: not present. There are no spatial fields, only closed-form functions of T/T_c.
- Magnetism: `critical_field_prediction` gives H_c = (1-T/T_c)^2 (L136-158). `london_penetration_depth` gives λ_L = λ_0/√(1-T/T_c) with λ_0 = 0.1 (L160-181). These are the textbook empirical laws, copied in. There is no B tensor, R or K_L.
- Parent/child: not present.
- Hard-coded targets / refits:
  - The exponent alpha = 0.5 is chosen to equal the BCS √ scaling (L130). L445 then prints "matches √(1-T/T_c) scaling exactly ✓". This is circular.
  - `harmonic_exponent` 1.5 (L84) is unused.
  - The T_c values are measured inputs (L49-80). The "ceramic > elemental" result is just an average of those inputs (L216-224).
  - main writes `superconductor_validation_results.json` to the CWD (L484).
- Pass criterion: none. It only prints "✓" claims.
- Violations:
  - L130 and L445: the target scaling is used as the input exponent and reported as a match.
  - L136-181: magnetic behaviour is copied from empirical law. No point-opening or L channel is modelled.
  - Point, Path and Field are all missing.

## symmetric_pair_binding_asymmetry.py
- Purpose / node IDs cited: Proton vs neutron error sign-flip "anchor" hypothesis. No node IDs are cited.
- Point rotation: not present. Quark "oscillation" is a mass label only.
- Path rotation: not present.
- Field: not present.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits:
  - kappa_T_base 297 and phase_diff_energy 6.58 "empirical" (L80-84).
  - binding_correction +25 / +12.5 "empirical offset" (L102, L104).
  - Observed errors -23.9/+27.7/+203.5 and base predictions are hard-coded (L133-143). The "predicted sign" is compared against these.
  - The predicted magnitude "~25 MeV" is the hard-coded offset (L238).
  - Hard-coded /home/claude path (L30).
- Pass criterion: a sign match ✓ per hadron (L249). The signs are rules written after seeing the observed signs.
- Violations: L102 and L133-143 are observed residuals encoded as a mechanism, with the same data then used as confirmation (a refit). There are no point/path/field components.

## test_algorithm_zero_3d_volumetric.py
- Purpose / node IDs cited: A unittest suite for `algorithm_zero_3d_volumetric_lattice` (`VolumetricD409Lattice`, `GalaxyRotationValidator`), citing D-409 (L3).
- Point rotation: not present. "Rotation velocity" is a galaxy rotation curve (L152-173), which is path rotation.
- Path rotation: `measure_rotation_velocity` returns radii and velocities (L154-157). The test asserts every v is between 50 and 350 km/s (L169-173), and that the curve changes under evolution (L243-265). It carries no L.
- Field: psi and rho lattices of shape (32,48,16) (L33-34). Wake injection is center-localized (L47-60). The update has a damping gamma (L97-108). There is no curl, chi or grad chi in the tests.
- Magnetism: not present.
- Parent/child: The "cascade inheritance" class name (L299) only tests field energy being above 0 (L315, L337). There is no rate transport.
- Hard-coded targets / refits:
  - The physical window 50-350 km/s is the assertion target (L172-173).
  - The "universal" gamma 0.05 and beta 0.15 are hard-coded (L273-277).
  - The 8x "volumetric_coupling_enhancement" is a tunable galaxy-scale factor (L287-296), which contradicts "without scale-specific tuning" (L272).
  - The reference curve is checked for an inner rise and a flat outer part (L197-202).
- Pass criterion: shape and finiteness, energy decreases with damping, and velocities fall in the plausible range. A passing suite prints "VALIDATED" (L384).
- Violations:
  - L169-173: the pass bit is a path-rotation velocity range, not point rotation or spread.
  - L287-296: a scale-specific enhancement factor exists despite the universality claim.
  - Point is missing and there is no Field curl.

## test_algorithm_zero_complete.py
- Purpose / node IDs cited: A test of `algorithm_zero_physics_engine` (OneWaveFieldUpdater, AlgorithmZeroCycle, CascadeSimulator) and `algorithm_zero_emergence`.
- Point rotation: not present.
- Path rotation: not present.
- Field: The updater steps a complex psi with damping 0.05 and coupling 0.15 (L47-58). "Pressure gradient effects" and "gravity_emergence_strength" come from a Gaussian (L274-282). Vortex quantization is printed but not asserted (L285-288). There is no chi, K_L or curl check.
- Magnetism: not present.
- Parent/child: The phase-locking test sets child = 0.5*parent (L262). Locking is therefore trivially true, so this is not a rate-transport test.
- Hard-coded targets / refits: none numeric. The energy-conservation tolerance is 20% (L63).
- Pass criterion: The file passes when all of these hold:
  - energy within 20% and the field changed (L73)
  - the phase cycle pattern holds (L127; `cycles_restart` is computed but not required)
  - result dict keys are present (L165, L191)
  - the encyclopedia is non-empty (L227, L245)
  - trivial locking plus pressure keys are present (L290)
- Violations:
  - L262-269: the locking test is tautological.
  - L274-282: "gravity emergence" is taken from a pressure gradient with no K_L / grad-chi contract.
  - No point rotation is present anywhere.

## test_bulk_excitation.py
- Purpose / node IDs cited: A rigorous unittest for `bulk_excitation.BulkExcitation`: a 4-component complex field on a periodic shell lattice. No node IDs are cited.
- Point rotation: not present. The global phase rotation `f*exp(.7j)` (L58) is a phase symmetry, not spin.
- Path rotation: not present.
- Field: The tests cover the following. No curl, chi or grad chi is tested.
  - an energy-gradient finite-difference check (L18-25)
  - a stationary state with mu < 0 (L27-33)
  - norm and energy conservation with second-order time refinement (L35-43)
  - time reversal (L45-47)
  - translation symmetry (L49-52)
  - a non-mutating detector (L54-59)
  - a linear control that disperses (L71-77)
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none. There are only numerical-integrity thresholds.
- Pass criterion: numerical correctness (gradient, conservation, reversibility, symmetry). There is no physics-target matching.
- Violations: none against the rules. It is out of scope for rotation and magnetism. As a node it has Field only.

## test_coherence_formulas.py
- Purpose / node IDs cited: Compares six coherence-decay formulas of the quark "omega ratio". No node IDs are cited.
- Point rotation: not present. omega = kappa_T/m (L64-65) is a mass-derived oscillation rate, not a spin carrying L.
- Path rotation: not present.
- Field: not present.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: Measured hadron masses are listed (L88-92) but unused. kappa_T_base is 0.297 (L64, L100). The formula search (V1-V6) is a fit exploration. V5 is identical to V2 and V6 to V3.
- Pass criterion: none. It prints coherences and concludes that a separate binding correction is needed (L166-171). Its `test_formula_variant` name (L78) would be collected by pytest, which would error on missing fixtures.
- Violations: none on the rotation and magnetism rules. Its conclusion motivates the empirical offset added in symmetric_pair_binding_asymmetry.py.

## test_coherence_inversion.py
- Purpose / node IDs cited: The "coherence inversion" hypothesis κ_eff = κ/avg_coherence for no-anchor hadrons. No node IDs are cited.
- Point rotation: not present.
- Path rotation: not present.
- Field: not present beyond the `WeaveDensity` / `WeavingEnergyCalculator` imports (L97-106).
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits:
  - kappa_T_base 0.40 (L46, L225).
  - binding_energy_base -8 / -30 MeV (L165-167).
  - The anchor rule sign ±1 (L136-141).
  - The inversion factor is designed to raise Lambda binding toward the measured mass (L12-20). The masses are inputs (L34-39) and the result is reported as error versus them.
  - Hard-coded /home/claude path (L24).
- Pass criterion: none. It prints the average percent error.
- Violations: L80-88 and L136-146 use ad-hoc rules tuned to observed residuals. There are no point/path/field components.

## Slice summary
- **Canonical point rotation:** None of the 10 files implements it. No file has an L = I·omega state, an open/closed magnetic switch (dL/dt = 0 vs -gamma L), principal-axis stability, or parent/child rotation transport (omega_c + R_c^T omega_p).
- **Rule violations:**
  - Magnetism feeding gravity: `satellite_galaxy_validator_em_coherence_fixed.py` L146-149 scales the gravitational-wake coupling by an EM-coherence scalar. There is no B, R or K_L tensor, and grad chi is never used.
  - Raw parent-rate addition: both satellite files add host velocity to the satellite velocity as scalars (em_coherence L164; velocity_validator L203).
  - Expansion framing: `standard_model_mysteries_unified.py` L211 and L855 use "superfluid expansion" (dark energy 0.68), which conflicts with "no expansion".
  - Gravity built from pressure gradients: `standard_model_mysteries_unified.py` L192/L206 and `test_algorithm_zero_complete.py` L274-282 build gravity from grad P with no K_L / chi contract. `standard_model_mysteries_unified.py` L217 also hard-codes g = 9.81.
- **Hard-coded targets / refits:**
  - In standard_model_mysteries_unified.py: Higgs 125.0, proton radius 0.84, dark-energy 0.68 and ECE 0.27 with 0% error, synthetic fallbacks marked "success".
  - Satellite fits (39.23 / 38.69, beta_0, r_decay, ring radii).
  - Superconductor exponent 0.5 chosen to equal BCS and then reported as a match.
  - Hadron binding offsets (+25 MeV, ±1 anchor rule, κ inversion) built from observed residuals.
- **Pass bits:** None is point rotation. They are percent error against echoed constants, a 50-350 km/s path-rotation window (`test_algorithm_zero_3d_volumetric.py`), dict-key presence and tautological locking (`test_algorithm_zero_complete.py`), and numerical integrity (`test_bulk_excitation.py`, which is sound).
- **Live vs dead/legacy:**
  - Live-ish test harnesses: `test_bulk_excitation.py` (rigorous, Field only), `test_algorithm_zero_3d_volumetric.py` and `test_algorithm_zero_complete.py` (each depends on its engine module).
  - Legacy/exploratory scripts: `standard_model_mysteries_unified.py`, `symmetric_pair_binding_asymmetry.py`, `test_coherence_formulas.py` and `test_coherence_inversion.py`. All four hard-code `/home/claude/...` sys.path.
  - Superseded/flagged: the satellite validators. The em_coherence file carries a 2026-10-06 `INVALID_COMPARISON` evidence warning pointing to GALAXY_EXTERNAL_VALIDATION.md.
  - Narrative-only, no solver dynamics: `superconductor_phase_transition_validator.py`.
- **Cross-references outside the slice:** algorithm_zero_3d_volumetric_lattice.py, algorithm_zero_physics_engine.py, algorithm_zero_emergence.py, w2_gravity_emergence.py, determine_flavor_hierarchy.py, neutrino_mass_solver.py, hadron_knot_geometry.py, hadron_mass_predictor.py, bulk_excitation.py, GALAXY_EXTERNAL_VALIDATION.md, A-115 / Book 5 Ch1, D-409.
