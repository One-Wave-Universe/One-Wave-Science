# Code ledger, slice c20 (10 files, all read in full)

## solvers/oscillating_boundary_dynamics.py
- Purpose / node IDs cited: Hadron mass correction: boundary radius R(t)=R0+dR sin(wt) subtracts an "oscillation energy" from HadronMassCalculator output (L1-20, 111-133). No node IDs cited.
- Point rotation: not present. "Phase" here is vortex phase offset (L57-70), not body spin/attitude.
- Path rotation: not present.
- Field: not present (no curl, wake, chi, grad chi). Boundary is called "excitation of displacement field psi" in prose only (L18-19, 245-246).
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: measured hadron masses (L35-39) used as error reference; PDG current quark masses (L29-33). Arbitrary scalings: dR = 0.05*(max_diff/pi) (L80), w = 2pi kappa_T/(m_avg*100) "rough scaling" (L88), E_osc*1000 "dimensionless -> MeV" (L107), shell thickness 1% (L100). kappa_T_base=0.373 etc. passed in (L45-46, 156-162). Sign of E_osc chosen to subtract (L120-123) to reduce overprediction.
- Pass criterion: avg dynamic error <1% and all <1.5% vs measured masses (L222-225). Not point rotation.
- Violations: none against point-rotation/magnetism rules (topic absent). Data-integrity issue: free unit scalings (L88, L107) tuned toward measured masses; sys.path hard-coded to /home/claude/... (L23).

## solvers/oscillating_phase_mechanism.py
- Purpose / node IDs cited: Narrative analysis that quark-mass-dependent phase oscillation changes phase-locking energy (L1-20). No node IDs.
- Point rotation: not present.
- Path rotation: not present.
- Field: not present.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: PDG quark masses (L28-32), measured hadron masses (L34-38), prior "PREDICTED" values (L40-44); correction coefficients -0.3 and 0.1 invented (L101); omega = 0.373/m (L72); amplitude formula ad hoc (L76). Prints error-pattern explanation (L200-203) that is narrative, not computed.
- Pass criterion: none (print-only analysis).
- Violations: none against canonical rotation rules. Hard-coded sys.path (L23).

## solvers/phase5a_source_term_bridge.py
- Purpose / node IDs cited: Maps four-interaction state Z=(Z_K,Z_E,Z_M,Z_T) to A-115 source J_source and solves radial chi (L1-19). Cites D-409, A-115, C-318, C-322, A-109, C-309 (L8-15, 63-64). Imported by phase5a_unified_solver.py, phase5c, phase5d (live dependency).
- Point rotation: not present. Z_K described as "knot vortex circulation" (L75-76) but scalar/vector Z_K is simply scaled (L87-92); no omega, L or attitude.
- Path rotation: not present.
- Field: J = s_K Z_K + s_E Z_E + s_M Z_M + s_T Z_T + c_cross(pairwise products) (L71-242). Radial Poisson-like solve with stiffness K_chi+S_u (L298-314); gradient (L317-319); g = -alpha_g grad chi with alpha_g=1.0 "to be calibrated" (L322-323); displacement reconstruction (L326-328). No curl, no wake term in this file.
- Magnetism: not present. Z_M is "Mirror-Gate orientation" (L122-146), not B; no R, no K_L. Gravity is plain -alpha grad chi (A-115 baseline), so grad chi = 0 -> g = 0 holds here.
- Parent/child: not present.
- Hard-coded targets / refits: coefficients s_K=1.0, s_E=0.8, s_M=1.2, s_T=0.6, c_cross=0.12, rho_u, mu_u, K_chi=2.0, S_u=2.0 hard-coded and labeled "from D-409 joint-response solver" without import (L56-66). No observed targets.
- Pass criterion: test only asserts source finite, nonzero, right shape (L365-367); name claims "energy conservation" (L340-349) but nothing checks energy.
- Violations: none against rotation/magnetism rules. Bug: `gradient_Z_E.norm()` (L116) is not an ndarray method; raises AttributeError whenever an E gradient is passed. Lattice sites mapped to radius by linspace (L281), not geometry. Test name overclaims (L340).

## solvers/phase5c_three_view_verification.py
- Purpose / node IDs cited: Ablation of bridge coefficients to show mass-effect, gravity (local+wake) and mirror-gate channels share one source; then 125 GeV calibration (L1-18). Cites D-409, Phase 5A/5B.
- Point rotation: not present.
- Path rotation: not present.
- Field: uses UnifiedCompressionSolver outputs acceleration_local / acceleration_wake (L97-101, 166-169); no own field math.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: Path B uses 125 GeV as calibration anchor: scale_factor = 125/E_MG (L310-312), then higgs_mass reported as 125 (L324). Lepton "spectrum" uses placeholder multipliers 0.5e-3, 0.1, 1.8 (L325-328). Synthetic profile hand-built (L81-86).
- Pass criterion: "CONFIRMED" if every ablated coefficient drops all channels by >10% (L243-269).
- Violations: none against rotation rules. Logic bug: ablation always uses self.Z_profile (L143-159), not the synthetic test profile, so TEST 2 ablations compare against a synthetic baseline using native-profile ablations. The bridge ablation at L131-148 is discarded; unified solver re-solve (L154-160) is what is reported. 125 GeV is an input, not a prediction (L310-324).

## solvers/phase5d_planetary_falsification.py
- Purpose / node IDs cited: "Planetary falsification" of unified gravity, with magnetic reorganization and point rotation (L1-34). Cites C-319, C-320, C-325, G-749, G-769, D-409, A-115 (L23-30).
- Point rotation: compute_point_rotation (L406-454). I = (2/5) M R^2 (L430). Rotation is STARTED by gravity: torque = alpha_torque * max|acceleration_local| * R * M (L434-435), where acceleration_local is -grad chi gravity; then omega = torque / I (L438-439), which is dimensionally wrong (tau/I is angular acceleration, not omega) and is not L-dot = tau integration. No initial spin carried in, no open/closed magnetic switch, no gamma, no organization target rate, no inertia-axis stability. Comment says "L-dot = tau" (L20, 150-152, 411) but code does not integrate L.
- Path rotation: omega_orbital = v / a (L444-445) used only as a ratio comparator (L452); labeled "rad/year (rough)" but units are km/s / km = 1/s. Carries no L. G-769 cited but not implemented.
- Field: g from UnifiedCompressionSolver (L173-189): acceleration_local + acceleration_wake. No curl.
- Magnetism: compute_magnetic_reorganization (L367-404). B_effective is built FROM compression chi: B = |chi|/(1+|chi|) (L387). R is NOT built from W_B = B(x)B - |B|^2 I/3 (docstring L374 says so, code does not); R = sign(dB/dr) (L392-393), a scalar +/-1 per radius. K_L is a scalar "path_accessibility_scaling" = 1 + kappa_R * mean|R| (L396), which is always 1+kappa_R. kappa_R = 0.1 hard-coded (L146); lambda_B, lambda_omega set but unused (L147-148). K_L is never applied to g (no g = -alpha K_L grad chi anywhere). Jupiter/Saturn magnetic moments "predicted" from sum(chi^2) times 1e27 / 1e26 (L326-329, 354-357): magnetism derived from compression field.
- Parent/child: not present.
- Hard-coded targets / refits: Mercury precession = 40.0 + 3.0*(normalized gradient) (L220) so result lands in 40-43 by construction; observed 43.11 (L222); pass if within 1 arcsec (L227). Moon: 1.0 + 2*max_gradient (L298) vs 2.725 (L299). Venus agreement is `acceleration_at_venus > 1e-6` vs hard-coded retrograde_observed=True (L263-270); Venus distance in km (1e8) compared against solver edges in lattice units (L256) so the branch almost always yields 0 -> False. Magnetic moments scaled by observed order of magnitude (L329, L357). energy_scale_factor 136.44 from 5C 125 GeV anchor (L126, L502).
- Pass criterion: per-test 'agreement' bits against observed values (L227, L270, L304); none are point-rotation-based.
- Violations:
  - phase5d:L434-439 gravity/compression gradient starts and sets point rotation (rule: gravity does not start or affect point rotation; a thing does not start spin on its own).
  - phase5d:L439 omega = tau/I; not L = I omega bookkeeping; violates C-306/C-307 L bookkeeping.
  - phase5d:L406-454 no open/closed magnetic switch (dL/dt=0 vs -gamma L); no organization target rate.
  - phase5d:L387 B derived from chi (magnetism from compression, inverse direction; B not an independent input).
  - phase5d:L392-393 R = sign(dB/dr), not W_B-driven symmetric traceless tensor; L396 K_L scalar not tensor.
  - phase5d:L146 kappa_R = 0.1 hard-coded (rule: kappa_R not set).
  - phase5d:L367-404 K_L computed but never multiplies grad chi; C-320 coupling claimed (L19, L403) but not implemented.
  - phase5d:L326-329, L354-357 magnetic moments generated from compression energy and scaled to observed magnitude.
  - phase5d:L220, L298 hard-coded offsets toward observed Mercury/Moon values reported as predictions.
  - phase5d:L263-270 Venus "prediction" is a threshold test with unit mismatch (L256), reported against hard-coded True.
  - G-769 path rotation cited (L28) but not separated or implemented; field curl absent -> node incomplete (Point/Path/Field).

## solvers/phase5e_inertial_coupling_dynamics.py
- Purpose / node IDs cited: Moon recession, Mercury 3:2 and perihelion, Venus retrograde via "K_L gating of inertial lag" (L1-37). Cites C-319, C-320, G-749, A-115, D-409 (L28-33).
- Point rotation: Mercury spin is not computed; T_rotation = (2/3) T_orbit is written in (L230-234) from the observed 3:2 ratio. "resonance_stability" = K_L_sun efficiency (L239). Venus spin direction = 'retrograde' if (1 - K_L_venus) > 0.5 with K_L_venus = 0.0 hard-coded (L286, L303-307): spin direction set by gravity-wake "drag torque" (L288-299). No L, no I, no omega integration, no open/closed switch, no organization target rate.
- Path rotation: orbital period from 2 pi r / v (L227-228); barycenter centripetal vs gravitational (L67-77). Carries no L. Not separated from point rotation as a distinct rate object.
- Field: no chi solve; "gravity wake" is narrative (L288-299). No curl.
- Magnetism: K_L built from compression chi: R_eff = |chi|/(1+|chi|) (L155-159), K_L = 1 + kappa_R R_eff scalar (L162), efficiency = 1/K_L (L167). No B, no W_B. chi_earth = (Z_K+Z_M)/2 (L178-182); chi_sun = 1.5 hard-coded (L195). kappa_R = 0.1 hard-coded (L141); lambda_B unused (L142). Moon acceleration = a_bary*(1-eff)*(M_E/M_moon)*eff converted with s^2/1000 (L109-122) (dimensionally m/s^2 * s^2 = m, labeled mm/year).
- Parent/child: not present (no R_c^T omega_p transport; Moon/Earth/Sun rates not composed).
- Hard-coded targets / refits: Mercury 3:2 ratio is input (L231) and reported as resonance result (L241-248). Perihelion precession_predicted = 43.00 hard-coded "From Phase 5D" (L260-261), PASS if <1% from 43.11 (L269) - guaranteed pass. Venus retrograde guaranteed by K_L_venus=0.0 (L286, L304-307, L314). Moon observed 2.725 (L358), pass within 0.5 (L363). Z profile literal 0.8409 (L475-480).
- Pass criterion: Mercury/Venus PASS bits are hard-wired; Moon is a numeric comparison. None is point-rotation physics.
- Violations:
  - phase5e:L231-234 Mercury 3:2 spin is an input reported as an output (canonical requires 3:2 from lattice organization target rate).
  - phase5e:L260-269 perihelion 43.00 hard-coded, guaranteed PASS.
  - phase5e:L286, L303-307 Venus spin direction forced by gravity-wake drag with K_L=0 (gravity changing point rotation; magnetism used as a resistance gate rather than the open/closed dL/dt switch).
  - phase5e:L222-224 claims 3:2 is "magnetic + gravitational coupling"; canonical: magnetic channel off must still leave the face; gravity does not affect point rotation.
  - phase5e:L155-167 K_L/R derived from chi, not from B via W_B; scalar not tensor; L141 kappa_R=0.1 hard-coded.
  - phase5e:L106-122 Moon "acceleration" from barycenter lag times K_L efficiency; unit error (L122).
  - No parent/child transport anywhere for Sun-Earth-Moon.

## solvers/phase_locking_mechanism.py
- Purpose / node IDs cited: Diagnostic print of HadronMassCalculator components and error correlation (L1-18). No node IDs.
- Point rotation: not present.
- Path rotation: not present.
- Field: not present (twist term eta_T curl v mentioned in print only, L108).
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: kappa_T_base=0.297 "Calibrated value" (L63); measured hadron masses (L33-37); prior predicted values (L39-43); binding energy described as "empirical" (L94). Narrative error values printed as literals (L146-148).
- Pass criterion: none (analysis/print).
- Violations: none against rotation rules. Hard-coded sys.path (L21).

## solvers/precision_tests.py
- Purpose / node IDs cited: "5 experimental predictions" (pair angle, positronium, muon g-2, hadron dipoles, muon pair suppression) (L1-16). No node IDs.
- Point rotation: not present (spin mentioned only in docstrings, L113-116).
- Path rotation: not present.
- Field: not present.
- Magnetism: magnetic moments are literals, no B/R/K_L (L238-251).
- Parent/child: not present.
- Hard-coded targets / refits: every "prediction" is a literal near the measured value: pair 3D angle 175.0 (L89); ortho/para Ps lifetimes 145e-9 / 0.123e-9 (L135-136); muon (g-2)/2 = 0.00116592 (L189) vs measured 0.00116592089; dipoles 2.79, -1.91, -0.61 (L245-251); 1 GeV ratio 0.012 (L312). Labeled "QED prediction + higher-order knot effects" and "Predict within 0.1%" with no computation. Positronium lifetimes labeled _ns but stored in seconds (L50-51).
- Pass criterion: count of errors <5% (L446) -> "framework validity" (L453). Pass is literal-vs-measured.
- Violations: no rotation-rule violations (topic absent). Severe evidence violation: all reported predictions are hard-coded observed values (L89, L135-136, L189, L245-251, L312). Writes to /home/claude/... path (L459).

## solvers/pressure_model_calibrator.py
- Purpose / node IDs cited: Fits GalacticPressureProfile (P0, a_s, r_core) to MAST galaxy rotation curves; grid + Nelder-Mead; cross-validation MW<->M31 (L1-21). No node IDs.
- Point rotation: not present. "Galaxy rotation" here is circular-velocity (path) curve fitting.
- Path rotation: orbital velocity curve v(r) from pressure profile (L72-73, L166-167); carries no L. Implementation lives in galaxy_rotation_validator.py (outside slice).
- Field: pressure profile only; no chi, grad chi, curl, wake in this file.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: parameters are explicitly fit to observed velocities (L57-79, 117-135); results are fits, labelled as calibration (honest). Bounds hard-coded (L66-70). Fallback fabricates radii by linspace if missing (L51-53).
- Pass criterion: none (reports chi^2); cross-validation reports test-galaxy chi^2 (L193-202).
- Violations: none against rotation rules. Note: fitted rotation curve is a refit, must not be cited as a prediction; radii fallback (L51-53) can silently fabricate geometry.

## solvers/proton_compression_simulator.py
- Purpose / node IDs cited: Energy-balance proton compression to locate Mirror-Gate threshold and calibrate lambda from 125 GeV (L1-18). Cites C-318, C-322 (L6, L151, L213).
- Point rotation: not present.
- Path rotation: not present (compression "path" is xi coordinate, L32, L237-240).
- Field: not present (no chi field; radius R(xi) quadratic, L80-87).
- Magnetism: not present ("Mirror" is orientation-flip energy, not B).
- Parent/child: not present.
- Hard-coded targets / refits: E_scale = 50 GeV "chosen to make the model reach ~125 GeV" (L76-78, L176-177); E_M functional form "chosen to match empirical 125 GeV" (L159-160); threshold defined as where E_total crosses 125 (L219-222); lambda = 125/E_MG (L253-263), so E_MG ~ 125 by construction. PDG quark masses (L332-335) as comparison; uncalibrated masses literal (L328-331). Coefficients 0.03, 2.0(1+5xi), 0.3(1+3xi^2), 0.2(1+2xi^2), 0.1 cross (L102, L120, L138, L141, L184) hard-coded.
- Pass criterion: none explicit; reports lambda and mass errors.
- Violations: none against rotation rules. Circular 125 GeV calibration (L78, L174-177, L221) - anchor is input, not prediction.

## Slice summary
- Canonical point rotation: NO file in this slice implements point rotation canonically. None carries an initial spin, integrates L = I omega under dL/dt = tau, has an open/closed magnetic switch (dL/dt = 0 vs -gamma L), a parent organization target rate, greatest/least inertia axis stability, or omega_c + R_c^T omega_p transport.
- Violators on rotation/magnetism:
  - phase5d_planetary_falsification.py: gravity (max |g| from grad chi) sets the torque and omega = tau/I (L434-439); B derived from chi (L387); R = sign(dB/dr) not W_B (L392-393); K_L scalar and never applied to g (L396); kappa_R=0.1 (L146); magnetic moments from sum(chi^2) scaled to observed (L329, L357); Mercury/Moon outputs built with offsets toward observed (L220, L298); Venus unit mismatch (L256-263).
  - phase5e_inertial_coupling_dynamics.py: Mercury 3:2 is an input reported as result (L231-248); perihelion 43.00 hard-coded PASS (L261-269); Venus retrograde forced by gravity-wake drag with K_L=0 (L286-314); K_L from chi, scalar, kappa_R=0.1 (L141, L155-167); no parent/child transport.
- Other evidence violations (non-rotation): precision_tests.py all five "predictions" are literals at measured values (L89, L135-136, L189, L245-251, L312); proton_compression_simulator.py and phase5c_three_view_verification.py use 125 GeV as input then report it (L78/L174-177/L221; L310-324); oscillating_boundary_dynamics.py free unit scalings tuned to masses (L88, L107).
- Bugs: phase5a_source_term_bridge.py L116 `.norm()` on ndarray; phase5c L143-159 ablation uses native profile in synthetic test; phase5e L122 unit error; precision_tests L50-51 ns label on seconds.
- Live vs dead: phase5a_source_term_bridge.py is a live dependency (imported by phase5a_unified_solver.py, phase5b_bounded_knot_forward.py, phase5c, phase5d). phase5c/5d are Phase 5 pipeline scripts (5d references 5C's 136.44 scale). phase5e is standalone (no imports of 5A-5D; hard-coded Z). Hadron scripts (oscillating_boundary_dynamics, oscillating_phase_mechanism, phase_locking_mechanism) and precision_tests.py use hard-coded /home/claude/ sys.path/output paths: legacy exploratory. pressure_model_calibrator.py is a galaxy rotation-curve fitter (depends on galaxy_rotation_validator.py, observational_data_loader.py). proton_compression_simulator.py depends on proton_mirror_gate_calibration.py; audit_phase5_mass_claims.py and vortex_phase_oscillations.py reference files in this slice.
- Cross-refs outside slice that matter: phase5a_unified_solver.py (produces acceleration_local/acceleration_wake used by 5c/5d), phase5b_bounded_knot_forward.py (D-409 Z profile), galaxy_rotation_validator.py, audit_phase5_mass_claims.py.
