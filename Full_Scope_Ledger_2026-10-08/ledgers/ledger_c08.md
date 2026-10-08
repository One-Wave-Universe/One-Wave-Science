# Code ledger: slice c08

The canonical rules come from LEDGER_INSTRUCTIONS.md. I read all 23 files in full. To check behaviour, I ran 5 Engine smokes read-only (`python3 -B -I`, run from /tmp, so nothing was written to the repo): magnetic_axis, rotations3, omega_s_field, hex_hold, chi_stepper. I did NOT run `Integrity_Tools/apply_integrity_update.py`, because it writes into the repo. Imports from outside the slice are noted but were not ledgered: `Engine/source_chi_wakes.py` (chi = parent wake(TOP) + local leftovers, with grad_chi computed by finite difference) and `DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/dispersion_phase1.py`.

---

## One-Wave-Science/DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/maxwell_validation_phase6a.py
- Purpose / node IDs cited: "Phase 6A" Maxwell check on a 2D hex lattice, using a modified 2-term characteristic equation (lines 1-17). It cites no node IDs.
- Point rotation: not present.
- Path rotation: not present.
- Field: E-like = grad(div psi) and B-like = -curl curl psi, stated in text only (lines 93-95, 232-238). No lattice operator is evaluated. The only "field" in the code is the scalar dispersion functions at lines 33-72.
- Magnetism: B is a transverse dispersion branch. There is no R, no K_L, no kappa_R, no chi and no gravity.
- Parent/child: not present.
- Hard-coded targets / refits: gamma = beta = 0.5 is fixed at lines 99, 184 and 273. Test 4 fits omega^2 = a + b k^2 (line 299) and reports "PASSED (PARTIALLY)", with no external target.
- Pass criterion: printed text only. Test 1 builds A_E = k and A_B = k_perp (lines 125-130), then "verifies" the alignment it just built. Test 3 prints "PASSED (EXACTLY)" from a vector identity, and no computation is done (lines 245, 363). Test 2 only compares frequency ratios against a 0.8-1.2 window (line 207). No pass bit exists, and nothing tests point rotation.
- Violations: none against the rotation/magnetism canon. Non-canonical problems: Tests 1 and 3 pass by construction (lines 125-147, 245). The transverse constant (1+gamma-beta k^2) was hand-altered; see modified_update_rule.py.

## One-Wave-Science/DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/modified_maxwell_validation.py
- Purpose / node IDs cited: tests whether the "modified" transverse dispersion propagates (lines 1-17). It cites no node IDs.
- Point rotation: not present.
- Path rotation: not present.
- Field: transverse versus longitudinal dispersion only (lines 27-66).
- Magnetism: B is the transverse branch. There is no R, K_L or chi.
- Parent/child: not present.
- Hard-coded targets / refits: line 35 changes the constant to `1 + gamma - beta * k_sq  # MODIFIED from (1 - gamma)` purely to obtain oscillation (lines 175-200 call this "BREAKTHROUGH"). Line 218 says the result is "Aligned with canonical requirement (Δ < 0 for oscillation)", so the form was chosen to hit the wanted outcome.
- Pass criterion: Re(omega) > 0.001 is printed as "PROPAGATING" (lines 93-102). There is no pass bit.
- Violations: none against the rotation canon. Process problem: the equation was refit to produce the desired behaviour (line 35).

## One-Wave-Science/DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/modified_update_rule.py
- Purpose / node IDs cited: proposes a damped wave update rule (lines 1-20). It cites no node IDs.
- Point rotation: not present.
- Path rotation: not present.
- Field: the operator grad(div) - curl curl appears in text only.
- Magnetism: not present beyond the "transverse (B-like)" label.
- Parent/child: not present.
- Hard-coded targets / refits: the docstring's own derivation gives the constant (1 - gamma) (lines 40-42). The code instead uses `constant = 1 + gamma - beta * k_sq  # Changed sign to allow oscillation` (line 68), so the stated derivation and the code disagree. Lines 61-66 admit the form was chosen to get complex roots.
- Pass criterion: |Re omega| > 0.001 is printed as "PROPAGATING" (line 110). There is no pass bit.
- Violations: none against the rotation canon. Self-contradiction: lines 40-42 versus line 68.

## One-Wave-Science/DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/parameter_optimization.py
- Purpose / node IDs cited: a (gamma, beta) scan to make transverse waves "light-like" (lines 1-13). It cites no node IDs. It imports `vector_field_framework` (line 17), and that import runs the module's top-level plotting and printing.
- Point rotation: not present.
- Path rotation: not present.
- Field: uses `vector_dispersion_transverse/longitudinal` from vector_field_framework.
- Magnetism: not present beyond the B-like label.
- Parent/child: not present.
- Hard-coded targets / refits: the target is an omega/k std/mean as small as possible, plus |lambda| <= 1, combined with a 0.6/0.4 weighting (lines 49-67). The best grid point is reported as "viable parameters" (line 245), so this is a refit to a wanted property. The hard-coded save path `/tmp/claude-0/-home-claude/3b9cfc7f.../parameter_optimization.png` (line 231) is a stale path from another session and will fail on this machine.
- Pass criterion: overall score > 0.7 means "viable" (line 244).
- Violations: none against the rotation canon. A stale absolute output path is at line 231.

## One-Wave-Science/DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/phase6b_unified_verification.py
- Purpose / node IDs cited: "Phase 6B" unified mode. Cites C-311 ("E and B are PROJECTIONS of a single field P_c", lines 175-177, 267-270), PHASE_6B_BREAKTHROUGH.md and unified_mode_extraction.py (line 11).
- Point rotation: not present.
- Path rotation: not present.
- Field: Helmholtz split, with grad(div psi) as E and curl(curl psi) as B (lines 190-200). This is text only.
- Magnetism: B is a projection of psi. There is no R, K_L or chi.
- Parent/child: not present.
- Hard-coded targets / refits: `dispersion_unified` simply returns `dispersion_E_like` (lines 102-109). It then prints "Ratio = 1.0 ✓ (compatible)" (line 115), so omega_E = omega_B is imposed by aliasing one function to the other. Line 149 formats a float with `{:>3}`, which works but is cosmetic.
- Pass criterion: printed claims only. "Faraday ... Automatically satisfied by Helmholtz decomposition" (line 265) is asserted without computation.
- Violations: none against the rotation canon. Pass by construction: lines 102-115 and 263-266.

## One-Wave-Science/DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/test_symmetric_laplacian.py
- Purpose / node IDs cited: replaces grad(div) - curl curl with a symmetric Laplacian so that E and B share one equation (lines 1-9). It cites no node IDs.
- Point rotation: not present.
- Path rotation: not present.
- Field: the Laplacian is applied as -k^2 (line 21).
- Magnetism: not present beyond the label.
- Parent/child: not present.
- Hard-coded targets / refits: none. gamma = beta = 0.5 (line 62).
- Pass criterion: prints "omega_E = omega_B AUTOMATICALLY" (line 125). This is a tautology, since one equation is used for both.
- Violations: none against the rotation canon. Note: `cmath` is used at line 42 but imported only at line 55. This works at call time.

## One-Wave-Science/DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/unified_mode_extraction.py
- Purpose / node IDs cited: the "Track A" unified mode. Cites C-311 (line 343: "E and B are radial and rotational projections of a single pressure field P_c").
- Point rotation: not present.
- Path rotation: not present.
- Field: text claims grad(div psi) = -k^2 (k·A) k_hat and that curl(curl psi) acts on the perpendicular part "with a minus sign" (lines 50-53, 159-160).
- Magnetism: B-like is the curl projection. There is no R, K_L or chi.
- Parent/child: not present.
- Hard-coded targets / refits: `dispersion_unified` = `dispersion_E_like` (lines 202-204), so matching is imposed, the same pattern as the phase6b file. Lines 153-170 contain the inline acknowledgment "Wait—that's what we already have!" and then assert the averaged coupling "might be" -beta k^2.
- Pass criterion: printed checkmarks only (lines 337-341).
- Violations: none against the rotation canon. Pass by construction at lines 202-204 and 337-341. The sign claim is an algebra error; see vector_field_framework.py.

## One-Wave-Science/DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/vector_field_framework.py
- Purpose / node IDs cited: vector-field update psi^{n+1} = psi^n + (1-gamma)(psi^n - psi^{n-1}) + beta[grad(div psi) - curl curl psi] (lines 23-37). It cites no node IDs.
- Point rotation: not present.
- Path rotation: not present.
- Field: `laplacian_3d`, `divergence_3d`, `curl_3d` and `gradient_3d` are all stubs that contain only `pass` (lines 39-71), so no lattice field is computed. `decompose_amplitude` splits A into parallel and perpendicular parts (lines 95-112).
- Magnetism: the B-like branch is the transverse dispersion (lines 163-178). There is no R, K_L or chi, and no gravity.
- Parent/child: not present.
- Hard-coded targets / refits: none. gamma = beta = 0.5 (lines 190-191). The stale save path at line 263 is `/tmp/claude-0/-home-claude/3b9cfc7f.../vector_dispersion.png`. Line 295 imports `dispersion_phase1`, which is outside the slice.
- Pass criterion: prints "VERDICT: Vector field naturally produces E/B-like separation!" (line 311). There is no pass bit.
- Violations: none against the rotation canon. MATH ERROR: line 134 states curl(curl psi) = -k^2 (A - (k·A)k_hat). For a plane wave, curl(curl psi) = (ik)×(ik×A) = +k^2 A_perp. The file's own identity at line 32 (curl curl psi = -lap psi + grad div psi) makes grad(div psi) - curl curl psi = lap psi. That operator gives the SAME -beta k^2 for both the longitudinal and transverse parts. So the "sign flip" at lines 137-142, the separate transverse equation at lines 163-178 (C = 2 - gamma + beta k^2), and the whole Phase 6A/6B "E/B separation" chain built on it (all 7 Phase-1 files in this slice) rest on a sign error. The symmetric-Laplacian file accidentally lands on the correct single equation.

## One-Wave-Science/DERIVATION_PHASE_2_CERN_BRIDGE/cern_particle_mapper.py
- Purpose / node IDs cited: maps SM particles to One-Wave modes. Cites A-114 (dispersion), C-309 (damping) and C-311 (vector field) at line 7, and CERN_TO_WAVE_REFERENCE.md.
- Point rotation: the `OneWaveMode.angular_momentum_components` field (line 95) is just (cos angle, sin angle) of a user-supplied orientation (lines 310-313). It is not L, there is no I and no omega, and it never changes. Spin J is copied from the PDG table (lines 57-70).
- Path rotation: not present.
- Field: none. `dispersion_omega_exact` is a stub that returns the small-k form (lines 186-194). Decay rate = gamma·omega/2π is "Rough scaling (OPEN)" (line 192).
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: PDG masses including H = 125.1, Z = 91.188 and W = 80.379 (lines 30-43) are used as inputs. "Eigenfrequency" is just mass × 1e9 (line 264), and k = m/√(β/2) (lines 219-220), so every mode quantity is the measured mass rescaled. The cross-section uses `coupling_factor = 1e6  # Empirical; tuned to match data` (line 488) and the experimental sigma = 61.4 fb as input (line 537). The "prediction" is compared against that measured value with a 50% tolerance (line 566), so measured data goes in and is reported as a match. `decay_width_to_timescale` returns seconds, not "steps" (lines 279-280; the field is named `damping_timescale_steps`).
- Pass criterion: `matches_experiment` is relative error < tolerance (lines 125-127), and the demo uses 50%. Nothing tests point rotation.
- Violations: (1) The measured masses and sigma are inputs that come back as "One-Wave" outputs, and a tuned coupling factor of 1e6 is involved (lines 30-43, 219, 264, 488, 537, 566). (2) "Angular momentum components" are an orientation angle with no I omega (lines 95, 310-313), so L bookkeeping is mislabeled, contrary to the C-307 ownership of L.

## One-Wave-Science/Engine/chi_stepper.py
- Purpose / node IDs cited: motion under g = -α grad chi from nested wakes. Kill test: dropping the parent wake must change the path (lines 2-7). It cites no node IDs.
- Point rotation: not present.
- Path rotation: the trajectory is integrated with g = -α grad chi (lines 20-25). There is no angular rate and no L. Translational velocity is damped by (1 - 0.02) every step (lines 23-24).
- Field: chi comes from `source_chi_wakes` (the parent wake plus locals) via `grad_chi` (line 21). A painted-Gaussian control is at lines 42-56.
- Magnetism: none. g = -α grad chi with an implicit K_L = I, which is the A-115 baseline, and grad chi = 0 gives g = 0. α = 2.4 is hard-coded (line 20).
- Parent/child: the parent wake is just summed into chi (line 61). No rates are transported.
- Hard-coded targets / refits: none (no observed values).
- Pass criterion: path L2 differences > 0.05 / 0.05 / 0.02 (line 71). It is a path-sensitivity test. Verified run: pass = true.
- Violations: none.

## One-Wave-Science/Engine/chromatic_circle.py
- Purpose / node IDs cited: symmetries of the 12-rail Z12 (rotation R, diameter I, reflection S, unit multiplication). It cites no node IDs.
- Point rotation: not present. R(n) = n+1 mod 12 is a label rotation (line 10).
- Path rotation: not present.
- Field: not present.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: group identities (line 58).
- Violations: none.

## One-Wave-Science/Engine/field_from_rail.py
- Purpose / node IDs cited: "fifths field rate" on a rail labeled -5..6 (lines 2, 13-31). It cites no node IDs.
- Point rotation: not present.
- Path rotation: not present.
- Field: `omega_field = 2π·5/12/TOP` (line 16). This "field rate" is numerology from the hop packet, not curl, wake or chi.
- Magnetism: not present.
- Parent/child: TOP = 2N from the packet (line 10).
- Hard-coded targets / refits: none observed.
- Pass criterion: labels exclude 7 and 11 (line 29). This is a labeling check only.
- Violations: none strictly. Note: a "field rotation" rate defined without curl does not satisfy the Field leg of Point/Path/Field.

## One-Wave-Science/Engine/hex_hold.py
- Purpose / node IDs cited: three blobs on an axial hex under g = -α grad chi wakes, where "hold" means staying inside the rim (lines 2-4). It cites no node IDs.
- Point rotation: not present.
- Path rotation: blob trajectories only (lines 36-41). There is no angular rate and no L.
- Field: grad chi from wakes (line 37). `hex_sites` (lines 17-25) is defined but never used, so the "hex" is not used in the dynamics.
- Magnetism: none (K_L = I implicit).
- Parent/child: the parent wake is summed into chi.
- Hard-coded targets / refits: none. Initial vy = ±0.15 (line 31), α = 1.8 (line 28).
- Pass criterion: all 3 blobs inside 1.5R for 70% of the last third (lines 42-54). Verified run: held = 3 and pass = true, which contradicts the docstring's "Last official receipt was 0/5" (line 4). The hold comes from velocity damping of 0.08 per step (lines 38-39), which drains kinetic energy so the blobs stall. It does not come from bound organization.
- Violations: none against the rotation canon. "Hold" is produced by artificial damping, so it is not evidence of lattice organization.

## One-Wave-Science/Engine/magnetic_axis.py
- Purpose / node IDs cited: a "parent-axis magnetic reorienter + child moments", applying torque to child spin toward the parent axis (lines 2-8). It mentions the CERN Z_K envelope peak and PLANET_SPIN_B.json (Gray constraints). It cites no node IDs.
- Point rotation: represented ONLY as a unit attitude vector s (lines 51-53). There is no omega, no I and no |L|, because s is renormalized every step (lines 38-39). The starting values are hard-coded per kid (lines 51-53). The changes are torque = κ (s × p_parent) (lines 24-29) and `step_spin`: s += τ dt, multiply by (1 - 0.18), renormalize (lines 32-39). The 0.18 damping is cancelled by the renormalization, so it is cosmetic. Gravity and grad chi do not touch s (correct). There is NO open/closed magnetic switch, so neither dL/dt = 0 nor dL/dt = -γL is represented, because |L| is not represented at all. There is no parent organization RATE target, only an axis.
- Dynamics finding (verified by running the file): ds/dt = κ s × p is precession about p, not alignment. Explicit Euler plus renormalization keeps s·p constant and then shrinks it on each normalization, so s drifts AWAY from the parent axis. LOCK_CANDIDATE starts at s·p = 0.97 and ends at 0.954 (tail mean 0.958). VENUS_CLASS stays at -0.998. The "lock" pass happens only because the starting alignment 0.97 is already above the 0.85 bar. The file's claim "torque on child spin toward parent axis" (line 5) is false for this code.
- Path rotation: not present.
- Field: not present. The comment says the chi pit lives in source_chi_wakes.
- Magnetism: B is not built. There is no W_B, no R, no K_L and no kappa_R. "Magnetism" is a hard-coded parent unit axis (0,0,1) (line 49) times amp = zk_peak × TOP/12 (line 48) times kappa = 1.1, which is a calibration (lines 46, 78). It does not produce gravity (correct by absence).
- Parent/child: the parent axis is used directly in the child torque. No R_c^T transport is done and no rates are combined.
- Hard-coded targets / refits: kappa = 1.1 is a "calibration" (line 78). The CERN Z_K peak stamps the amplitude (lines 20-21, 48). The Uranus-class and Venus-class starts are observed-planet constraints (lines 52-53), and their outcomes are reported as pass flags (lines 75-76).
- Pass criterion: LOCK_CANDIDATE tail-mean alignment > 0.85 (lines 66, 77). It is an attitude-alignment test, not a point-rotation rate test.
- Violations: (1) Point rotation lacks L = I omega. Only attitude is evolved, which leaves the Point leg incomplete per G-749/C-307. (2) There is no open/closed magnetic gradient switch (dL/dt = 0 vs -γL). (3) "Torque toward parent axis" actually precesses and drifts away (lines 24-39), so the lock pass is set by the initial condition (line 51), not derived. (4) kappa is hard-coded as a calibration (lines 46, 78), and the magnetic strength is stamped from CERN Z_K (line 48). (5) No transport-then-add for parent/child (no R_c^T omega_p).

## One-Wave-Science/Engine/omega_s_field.py
- Purpose / node IDs cited: "omega_s from the moving triad". omega = dθ/dt of blob-0 about the triad centroid, compared with 3τ/2 (lines 2-6). It references D-413 in the honest strings (lines 59, 61).
- Point rotation: not present. Despite the name omega_s, the measured quantity is a PATH angular rate (blob-0 position angle about the centroid, lines 19-22 and 41-43). It is not a spin.
- Path rotation: yes. omega = wrapped Δθ/dt (lines 42-43). It carries no L.
- Field: grad chi from wakes (line 36).
- Magnetism: none.
- Parent/child: τ = 1/parent_sigma (line 28), and the theory value 1.5τ comes from the parent scale (line 29).
- Hard-coded targets / refits: the theory value 3τ/2 is a prescribed target, not an observed one.
- Pass criterion: rel_err < 0.35 (line 58). Verified run: rel_err = 0.99995 and pass = false (it still fails, as the docstring warns).
- Violations: a naming and role conflation. "omega_s" (spin rate) is measured as path rotation about the centroid (lines 19-22, 42-43). Under G-749/G-769 the path rate carries no L and must not stand in for the point spin.

## One-Wave-Science/Engine/prove_one_wave.py
- Purpose / node IDs cited: algebraic receipts (hop identities, rail fifths, chi linearity, paint-not-source). It cites no node IDs (D-413 appears in the not_proven list, line 77).
- Point rotation: not present.
- Path rotation: not present.
- Field: chi linearity is ASSERTED, not computed (lines 47-52: `"pass": True`).
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: `all_pass` over the parts (line 70). Two parts hard-code pass = True: chi_linearity (line 50) and paint_not_source (line 61).
- Violations: none against the rotation canon. Hard-coded pass bits at lines 50 and 61.

## One-Wave-Science/Engine/rotations3.py
- Purpose / node IDs cited: "Potential, slope, and three rotations: point, path, field" (lines 2-9). It cites no node IDs.
- Point rotation: s is a unit attitude vector that starts at a hard-coded [0.2, 0.1, 0.97] (line 30). It is changed by torque κ(s × axis) plus an Euler step, damping (1 - 0.15) and renormalization (lines 48-55), so it has the same precession/drift behaviour as magnetic_axis. The reported "point_rotation" is `hypot(tx, ty, tz)`, the torque magnitude (line 58), which is neither a spin rate nor L. There is no I and no L. Gravity (grad chi) does not touch s (correct). There is no open/closed switch and no organization target.
- Path rotation: w_path = wrapped Δθ/dt of position about the ORIGIN, labelled "about parent" (lines 45-47). It carries no L (correct).
- Field: "field rotation" is an imposed constant field_rate = 0.07 (line 31). phi_f accumulates (line 36) but is never used. The axis stays fixed at [0, 0, 1] (line 37), so the field rate has no effect. There is no curl. chi and grad chi come from wakes (lines 38-39).
- Magnetism: the torque axis is a fixed unit vector and kappa = 1.1 is hard-coded (line 25). No B, R or K_L.
- Parent/child: not transported. The axis is global.
- Hard-coded targets / refits: none observed. Start s and kappa are arbitrary.
- Pass criterion: slope tail > 0 and finite potential (line 78). Nothing about point, path or field rotation is tested. Verified run: pass = true, with point_rotation_tail = 0.283 (a torque magnitude).
- Violations: (1) The "point rotation" output is a torque magnitude, not omega and not L = I omega (line 58). (2) The Field leg is an imposed constant that is never applied (lines 31, 36-37), not curl. (3) The pass bit ignores all three rotations (line 78). (4) There is no magnetic open/closed switch.

## One-Wave-Science/Engine/two_rotations.py
- Purpose / node IDs cited: two mirrored walks, +5 and -5, on a 12-count (lines 2, 8-17). It cites no node IDs.
- Point rotation: not present. The "rotations" are label walks.
- Path rotation: not present.
- Field: not present.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: both walks meet at 6 after 6 steps and close at 0 after 12 (line 37).
- Violations: none.

## One-Wave-Science/GRAV_LAB/modules/knot.js
- Purpose / node IDs cited: a braided closed curve modulated by vortex spin phase (lines 2-11). It cites no node IDs.
- Point rotation: reads `v.spin` as a phase only (line 8).
- Path rotation: the curve parameter angle is used for drawing only.
- Field: not present.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: none (it is visual).
- Violations: none.

## One-Wave-Science/GRAV_LAB/modules/knot_view.js
- Purpose / node IDs cited: canvas drawing of vortex arcs and the knot (lines 2-21). It cites no node IDs.
- Point rotation: `v.spin` sets the arc start angle (line 5). Display only.
- Path rotation: not present.
- Field: not present.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: none.
- Violations: none.

## One-Wave-Science/GRAV_LAB/modules/view.js
- Purpose / node IDs cited: projects lattice sites and colours them by chi (lines 2-36). It cites no node IDs.
- Point rotation: not present. `field.spin` is a camera yaw that advances by 0.008 per frame (lines 4, 36). This is view rotation, not physics.
- Path rotation: not present.
- Field: site chi is used only for alpha (lines 32-33).
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: none.
- Violations: none. Note: the camera rotation is named `field.spin`, which could be confused with point spin.

## One-Wave-Science/GRAV_LAB/modules/vortices.js
- Purpose / node IDs cited: three vortices at 120 degrees (lines 2-9). It cites no node IDs.
- Point rotation: spin starts at the position angle a (line 6). It is driven by `v.spin += 0.02` every step, unconditionally (line 11), with no torque, no I and no L. The spin is pushed at a constant rate from nowhere.
- Path rotation: positions are fixed and do not orbit.
- Field: not present.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: none (visual).
- Violations: (visual module only) the spin is self-driven at a constant increment (line 11). If this were read as physics, it would contradict "a thing keeps the point spin it has; it does not start one on its own".

## One-Wave-Science/Integrity_Tools/apply_integrity_update.py
- Purpose / node IDs cited: the "Updated 32" repository integrity migration. It writes YAML front matter on every node, the alias registry, the governance moves, rebuilt Internal_Proofs, the Book 1 chapter map, the AI packs, the wiki patches, the master index, the validator and the CHANGELOG (lines 251-487). Physics-relevant aliases: C-06→C-306 Torque, C-07→C-307 Angular Momentum, C-08→C-308 Spin-half (lines 56-58); I-08→E-528 Static Redshift Transport, I-09→A-115 Unified Compression Field, I-10/C-3113→C-311 Electric-Magnetic Duality, C-3114→C-310 Resistance Field, J-101→C-309 Propagation Limit, J-106→C-314 Three Frames of Reference (lines 89-104). C-3118 is the "UNBUILT_PHASE_LOCKING_PROPOSAL" (line 113).
- Point rotation: not present (no physics).
- Path rotation: not present.
- Field: not present.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none (physics). The date "July 23, 2026" is hard-coded at line 458.
- Pass criterion: the generated validator's `report['pass'] = not errors` (embedded at line 478).
- Violations: none against the canon. Hazards: (1) ROOT = the file's parent directory, i.e. `Integrity_Tools/` (line 6), while every path assumes the repo root (Nodes/, Books/, ...). Run from its current location, it would read and write the wrong tree or crash. (2) It is a destructive one-shot writer (moves, unlinks, rewrites all nodes), so it must not be re-run.

---

## Slice summary

**Point rotation implemented canonically:** none. No file in this slice represents L = I omega, an inertia tensor, the greatest/least-inertia stability rule, an open/closed magnetic switch (dL/dt = 0 vs -γL), a parent organization rate target, or transported parent/child rates (omega_c + R_c^T omega_p).

**Files that touch point rotation, and how they deviate:**
- `Engine/magnetic_axis.py`: attitude-only unit spin vector. "Toward-axis torque" κ s×p actually precesses, and with renormalization drifts away (verified: 0.97 → 0.954). Lock pass = initial condition above 0.85. kappa = 1.1 calibration, CERN Z_K amplitude stamp, observed Uranus/Venus starts. No L, no magnetic switch, no transport.
- `Engine/rotations3.py`: same spin update. "point_rotation" output = torque magnitude (line 58). Field rotation is an imposed constant that is never applied (lines 31, 36-37). The pass bit ignores all three rotations (line 78).
- `Engine/omega_s_field.py`: "omega_s" is measured as a path rate about the centroid, which conflates Point and Path. Still fails (rel_err ≈ 1.0).
- `GRAV_LAB/modules/vortices.js`: spin self-incremented at a constant rate (line 11), visual only.
- `DERIVATION_PHASE_2_CERN_BRIDGE/cern_particle_mapper.py`: "angular momentum components" = an orientation angle. Spin J is copied from PDG.

**Gravity / Field:** `chi_stepper.py`, `hex_hold.py`, `omega_s_field.py` and `rotations3.py` use g = -α grad chi from wakes with an implicit K_L = I (the A-115 baseline). Gravity never touches spin in any of them (consistent). No file builds B, W_B, R, K_L or kappa_R, and none lets magnetism produce gravity. hex_hold's "hold" comes from 0.08-per-step velocity damping. `field_from_rail.py`'s "field rate" is numerology, not curl.

**Magnetism in the derivation files:** B is only the transverse dispersion branch. The Phase 6A/6B chain (7 files) rests on a sign error. vector_field_framework.py:134 has curl(curl psi) = -k^2 A_perp, but the correct value is +k^2 A_perp, so grad(div psi) - curl curl psi = lap psi and both branches share one equation. The "B-like" constant (1+γ-βk²) was hand-changed "to allow oscillation" (modified_update_rule.py:68, modified_maxwell_validation.py:35). The "unified" mode imposes ω_B = ω_E by aliasing functions (phase6b:102-115, unified_mode_extraction:202-204). Maxwell tests 1 and 3 pass by construction.

**Hard-coded targets / refits:** cern_particle_mapper.py (PDG masses including H = 125.1 used as inputs, coupling_factor = 1e6 "tuned to match data", the measured 61.4 fb compared at 50% tolerance); parameter_optimization.py (γ, β refit to a light-like criterion); magnetic_axis.py (kappa calibration, CERN Z_K stamp, observed planet starts); prove_one_wave.py (pass = True hard-coded at lines 50 and 61).

**Live vs dead/legacy:**
- Live, runnable smokes: the Engine files (chi_stepper, hex_hold, magnetic_axis, omega_s_field, rotations3, prove_one_wave, chromatic_circle, field_from_rail, two_rotations), all "YELLOW" smoke jobs, and the GRAV_LAB visual modules.
- Legacy/exploratory: the 8 DERIVATION_PHASE_1 scripts. These are print-only, two of them hard-code a stale /tmp path from another session, and vector_field_framework has stub operators.
- Prototype: cern_particle_mapper (stubs and placeholders, marked OPEN).
- One-shot migration that has already run: apply_integrity_update.py (its ROOT now points at the wrong directory).

**Cross-references outside the slice that matter:** Engine/source_chi_wakes.py (chi/grad chi source for all the Engine smokes); PLANET_SPIN_B.json (observed planet spin/B constraints); D-413 (shear law / omega_s well); C-311 (E/B projections of P_c); A-114 / C-309 (dispersion, damping); CERN_TO_WAVE_REFERENCE.md; characteristic_equation_solver.py; dispersion_phase1.py; C-306, C-307 and C-308 via the aliases in apply_integrity_update.py.
