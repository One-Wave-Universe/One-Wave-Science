# Code ledger — slice c17 (10 files, all read in full)

## solvers/galaxy_rotation_c319_corrected.py (378 lines)
- Purpose / node IDs cited: Galaxy rotation curve fit for MW / M31 as "local gravity + cascade-inherited wake modulated by C-319 magnetic coherence" (L3-19). Cites C-319 (L3, 18, 120, 171), D-409 (L376). References satellite_galaxy_validator_em_coherence_fixed.py etc. (L6-9). Module-level script (no `main()` guard; L281-378 run on import).
- Point rotation: not present. No spin, omega, L, I or attitude anywhere. The "rotation" is only circular orbital speed v_c = sqrt(r g) (L240).
- Path rotation: orbital speed of the disk, v = sqrt(r * g_total) (L240). Carries no L (no L in the code at all). This is the only rotation modeled.
- Field: "compression wave in psi field" named in docstring (L114) but not computed. Inherited wake is a scalar exponential g_inherited = A * beta0 * f_EM * exp(-r/r_decay) (L161-165). No curl, no chi, no grad chi.
- Magnetism: no B vector, no R, no K_L, no kappa_R. "C-319 magnetic coherence" is a hand-written piecewise scalar f_EM(r) (L169-199, values 0.75/0.70/0.60/0.40 and galaxy factors 0.85/0.95 at L195,197) that MULTIPLIES a gravity term (L165, L233). The magnetic factor directly scales gravitational acceleration. B is not used, so the grad chi = 0 case is not testable; there is no chi.
- Parent/child: parent (Local Group) wake added raw to child gravity: g_total = g_local + g_inherited (L236). No frame transport.
- Hard-coded targets / refits: disk/bulge masses and scale lengths "from literature" (L75-84); beta0 = 0.2480, r_decay 51.5/46.2, f_em_baseline 0.362/0.927 copied from a satellite fit (L132-140); cluster_amplitude swept 10..100 against the same observed curves and best chi2 picked (L300-327), then reported as "PUBLICATION-READY... explained" (L365-368). Fit-then-claim.
- Pass criterion: mean chi2 of rotation-curve speed residuals < 200 -> "PUBLICATION" (L312-313, L365). Not point rotation, not spread; it is a path-speed curve fit.
- Violations:
  - galaxy_rotation_c319_corrected.py:165,233 — magnetic coherence factor f_EM multiplies gravitational acceleration (magnetism changes gravity strength; canon: magnetism enters only via K_L = I + kappa_R R on grad chi, and does not become gravity).
  - :169-199 — "magnetic" factor is a hand-tuned scalar of radius, not built from B; no R, no K_L tensor.
  - :236 — parent wake added raw to child (no transport).
  - :300-330,365-368 — amplitude refit to the observed curves, then reported as explanation.
  - Point rotation (G-749) absent; node incomplete (Point/Path/Field: only Path speed present).

## solvers/galaxy_rotation_c319_magnetic_coupling.py (294 lines)
- Purpose / node IDs cited: "Phase 2.2 Priority 2" — tests whether C-319 magnetic lattice reorganization bridges a "46x gap" (L3-13). Cites C-319, D-409 (L42-43, L288). Imports CascadeWakeRotationValidator from galaxy_rotation_cascade_wake_validator.py (L22-26).
- Point rotation: not present. `rotation_axis_alignment`, `disk_inclination` (L58-63) are set but never used anywhere. No omega / L / attitude.
- Path rotation: v = sqrt(r * g_total_enhanced) (L167). No L.
- Field: inherited wake taken from base validator (L146-159). No curl / chi / grad chi.
- Magnetism: `magnetic_field_strength` = 1.2 / 1.15 (L60, 64) unused. Enhancement beta(r) = 0.2480 * exp(-r/r_decay) * (1 + f_EM(r)) (L87-119) with the same hand-piecewise f_EM as c319_corrected. Applied as g_inherited_enhanced = beta * g_inherited_base (L160). Docstring says "The magnetic field does not create new gravity" (L12) but the code multiplies the gravity term by a magnetic factor. Note: beta < 0.25*(1+0.8) < 0.5 everywhere, so this actually REDUCES g_inherited (docstring L74 says "Enhancement is MODEST: 1.5-3.0x" — the code contradicts it). No R from B, no K_L, no kappa_R.
- Parent/child: g_local + beta*g_inherited, raw addition (L161).
- Hard-coded targets / refits: beta0=0.2480, r_decay 50/46 from satellite fit (L87-88); best_amplitude = 5.0 "converged from Priority 1" (L227) hard-coded (Priority 1 sweep only goes 0.5..2.5, so 5.0 is not its output).
- Pass criterion: both chi2 < 500 -> "SUCCESS: C-319 magnetic coupling bridges the gap" (L276-278). The elif branches at L279/L282 (<200, <100) are unreachable because <500 is tested first. Path-speed fit only.
- Violations:
  - galaxy_rotation_c319_magnetic_coupling.py:160 — magnetic factor multiplies gravitational acceleration (magnetism changes gravity), contradicting its own L12.
  - :87-119 — "magnetic" coupling not built from B (B strength L60/64 unused); no R / K_L tensor.
  - :161 — raw parent+child addition.
  - :227 — amplitude hard-coded, not derived.
  - :276-284 — unreachable pass tiers; pass is a chi2 fit.
  - Point rotation absent.

## solvers/galaxy_rotation_cascade_wake_validator.py (341 lines)
- Purpose / node IDs cited: Phase 2.2 base validator "Dark Matter as Extended Compression Effect (Wake Nesting)", v_c^2/r = |g_local + g_inherited| (L3-7). Cites A-115 / Book 5 Ch1 (L101, 126). Imported by c319_magnetic_coupling, constant_inherited_velocity, inherited_rotation_field (live dependency of those three).
- Point rotation: not present.
- Path rotation: v = sqrt(r * g_total) (L228). No L.
- Field: "compression ring" g_wake piecewise function of radius (L133-146): 0.1A, A(r-1)/(r+5), 10A/(r+20). Docstring attributes it to superfluid pressure gradient grad P (L102-104) and "galaxy's displacement" — but in code it is named and passed as `g_inherited` from parent "Local_Group" (L212-221), so the docstring (own-motion ring) and the code (inherited parent wake) disagree. No curl, no chi.
- Magnetism: none (C-319 only listed as future work L335).
- Parent/child: cluster wake added raw (L222).
- Hard-coded targets / refits: local_scaling 1.2 / 0.9 per galaxy (L205); wake_amplitude swept 0.5..2.5 against observed curves, best chosen (L298-325). Hand-shaped g_local / g_wake profiles.
- Pass criterion: none enforced; prints interpretation "If chi2 ~ 10-50 ... Compression ring model works" (L330-337). Fit statistic only.
- Violations:
  - galaxy_rotation_cascade_wake_validator.py:213-222 — parent wake added raw as gravity on the child (no transport).
  - :133-146 — wake is a hand-drawn profile, not a field solution; docstring/code mismatch on whose wake it is.
  - :298-325 — amplitude refit on the data being "explained".
  - Point rotation absent.

## solvers/galaxy_rotation_constant_inherited_velocity.py (300 lines)
- Purpose / node IDs cited: Phase 2.3 "FINAL CORRECTED PHYSICS": inherited part is the galaxy's ORBITAL VELOCITY in the cluster frame, constant at all radii; v_total = v_local + v_inherited (L3-24). Mentions C-319, D-409 (L290). Imported by solvers/galaxy_external_validation.py (L14 there) — this is the live galaxy model of the set.
- Point rotation: not present. Claims "The disk rotates AS A WHOLE at the orbital velocity" (L46) — but a constant tangential speed at every r is not a rigid (single omega) rotation; no omega or L is defined.
- Path rotation: the galaxy's orbital speed about the Local Group, 110 / 170 km/s (L61-64), is copied unchanged onto every star's circular speed (L125) and added to v_local (L128). This takes the parent PATH (ride, which carries no L) and turns it into the child's internal rotation — a Path rate is being used as if it set a Point/disk rotation. Mechanism "phase-locking" (L45) not modeled.
- Field: none (no wake, no chi).
- Magnetism: none.
- Parent/child: parent speed added raw as a scalar to the child speed (L128). Not R_c^T omega_p; the parent quantity is a translational speed, not even a rate, and is added without any frame transport.
- Hard-coded targets / refits: v_orbital 110 / 170 km/s "observational basis" (L54-64); velocity_scale_factor optimized by minimize_scalar on bounds (10,100) against the same curves (L203-212), then "Dark matter = inherited orbital velocity ... One-Wave framework VALIDATED" (L281-284).
- Pass criterion: combined chi2 < 100 -> "EXCELLENT ... VALIDATED" (L281). Speed-curve fit; not point rotation.
- Violations:
  - galaxy_rotation_constant_inherited_velocity.py:125-128 — parent Path (orbital ride) imposed on the child as internal rotation; ride is treated as carrying rotation/L (canon: Path carries no L; a thing keeps its point spin and does not acquire one from the ride).
  - :128 — raw scalar addition of parent and child motion, no transport.
  - :62-64, :203-212, :281-284 — hard-coded orbital speeds + fitted scale factor reported as validation.
  - Point rotation absent; Field absent.

## solvers/galaxy_rotation_inherited_rotation_field.py (325 lines)
- Purpose / node IDs cited: Phase 2.3 "galaxy phase-locking to parent cluster's ROTATING WAKE PATTERN" (L6-15). Cites "Algorithm Zero" coupling 0.3 (L44, 70) and C-319 magnetic stabilization (L73-75).
- Point rotation: a parent rate exists: Omega_cluster = v_cluster / R_cluster = 600/1500 = 0.4 (L62-67), named "rotation rate of cluster wake". It is computed from a bulk translational flow speed (L62 "Bulk flow velocity", L54 "recession ~600 km/s") divided by a size — i.e., a translation speed converted into a rotation rate. Nothing starts or changes it; no L, no I. Unit claim "Myr^-1 or equivalently km/s/kpc" (L87) — (km/s)/kpc is ~1.02 Gyr^-1 per unit, so 0.4 km/s/kpc is ~0.41 Gyr^-1, not 0.4 Myr^-1; printed period "15 Myr" (L68, L238) is off by ~1000x.
- Path rotation: child velocity v_inherited = Omega * r * 0.3 * 1.0 (L92-95), i.e. a rigid-body profile v ∝ r. Docstring L164 says v_inherited "stays constant" — contradicts v ∝ r in the code (the later constant_inherited_velocity.py L6-7 itself flags this as wrong). No L.
- Field: "rotating compression wake" named (L41), not computed. No curl/chi.
- Magnetism: magnetic_stabilization = 1.0 multiplier on the inherited velocity (L75, L95). Not from B; no R/K_L/kappa_R. Magnetism gates a rotation transfer from parent to child.
- Parent/child: v_total = v_local + Omega_p * r * 0.3 (L173). Parent rate scaled by 0.3 and added raw; no R_c^T transport; "child inherits 30% of parent motion" (L70) is a parent-organization share, not the canonical keep-your-own-spin + transport.
- Hard-coded targets / refits: Local Group v=600, R=1500 kpc, M=2e12 (L62-64); coupling 0.3 (L71); velocity_scale_factor = 100 "Empirical calibration" (L170).
- Pass criterion: combined chi2 < 100 -> "EXCELLENT" (L307). Speed-curve fit.
- Violations:
  - galaxy_rotation_inherited_rotation_field.py:62-67 — rotation rate manufactured from a bulk translational (path) speed.
  - :92-95, :173 — parent rate fraction added raw to child; no transport, child spin not kept/own.
  - :75, :95 — "magnetic" scalar multiplies inherited motion, not built from B.
  - :68, :87, :238 — unit/period error (Myr vs Gyr).
  - :164 vs :92-95 — docstring/code contradiction.
  - Point rotation proper (L = I omega) absent.

## solvers/galaxy_rotation_validator.py (391 lines)
- Purpose / node IDs cited: "Phase 5 Test 1" — (P,E) pressure field predicts rotation curves; "dark matter is displacement pressure" (L3-8, L385). No node IDs.
- Point rotation: not present.
- Path rotation: circular orbit speed v = sqrt(r |a|) with a from dP/dr (L157-172). No L.
- Field: scalar pressure P(r) = 0.3 P0 exp(-r/r_core) + 0.7 P0 exp(-r/a_s) (L116-131); acceleration a = -grad P (L146-155; pressure_gradient already returns -dP/dr at L144, then negated again at L155 — sign doubled, absolute value taken at L165 hides it). No curl, no chi; gravity from grad P without density (docstring L92 says a = -grad P / rho, code drops rho). Uses "expansion/transition" (L91) only as a radial-pressure word, not cosmology.
- Magnetism: none.
- Parent/child: none.
- Hard-coded targets / refits: 125-point grid search over (P0, a_s, r_core) fitted to each galaxy's observed curve (L204-251). Strawman "Standard Model" = constant 220 km/s (L257-268). Loads data at import (L78-79).
- Pass criterion: One-Wave chi2 < flat-220 chi2 for both galaxies -> "SUCCESS ... Dark matter is displacement pressure" (L380-385). Fitted 3-parameter exponential vs a 0-parameter constant; not a physics test. Note an exponential-pressure gradient falls off exponentially, so it cannot produce a flat curve.
- Violations:
  - galaxy_rotation_validator.py:204-251, :380-385 — per-galaxy fit to the data, reported as solving dark matter.
  - :257-268 — straw comparison.
  - :144/:155 — double negation of the gradient (masked by abs at L165); :92 vs :150 rho dropped.
  - Point rotation absent; gravity not in canonical g = -alpha K_L grad chi form (no chi).

## solvers/generate_publication_figures.py (577 lines)
- Purpose / node IDs cited: Generates 6 "publication" PNGs (lattice update rule, lepton mass formula, hadron calibration sweep, 3D field snapshot, precision summary, muon g-2) (L2-14). No node IDs. Writes to /home/claude/one-wave-science/publication/figures (L37) — stale path, not this repo.
- Point rotation: not present. Figure 4 labels Gaussian blobs "Electron vortex" / "Positron vortex" (L331-332) but no circulation or spin is computed — the field is a pair of scalar Gaussians (L278).
- Path rotation: not present.
- Field: update rule psi^{n+1} = psi^n + (1-gamma)(psi^n - psi^{n-1}) + beta(<psi_nbrs> - psi^n) (L123), shown with 6 face neighbors (L87-120) — not the 12-neighbor D-409 lattice used elsewhere. No curl.
- Magnetism: none.
- Parent/child: none.
- Hard-coded targets / refits: every plotted "prediction" is a literal: lepton predictions 0.510/111.7/1912.5 vs 0.511/105.7/1777 (L168-169); calibration heat map is a synthetic paraboloid centered on the chosen optimum (0.012, 0.010) and labeled "based on actual calibration results" / "Min error 0.4%" (L209-228); "Positronium 123 vs 125", "Pair angle 175 vs 155" (L364-365); muon g-2 framework value 0.00116592000 / 1165920 vs experiment 1165921 (L362, L387, L449) with a "Lattice Correction -158" bar (L467) chosen to land on experiment; historical g-2 series includes a "2026 framework prediction" point (L431-438). Text claims "matches ... to 0.001%" and "3 sigma tension is RESOLVED" (L490-496). Also internally inconsistent: SM bar 0.00116591810 (L387) vs 1165918e-11 text (L493) vs component sum 11659183+683+92+195 (L466, not equal to 1165918).
- Pass criterion: none; pure plotting of hard-coded numbers.
- Violations:
  - generate_publication_figures.py:168, :209-228, :361-367, :387, :431-438, :449, :466-467, :487-496 — hard-coded "predictions" set to (or tuned onto) observed values and presented as framework results; synthetic error surface presented as calibration output.
  - :87-123 — 6-neighbor cubic update shown as the lattice rule (conflicts with D-409 12-neighbor elsewhere).
  - No Point/Path/Field rotation content; dead/legacy (stale output path).

## solvers/gravity_emergence_validator.py (562 lines)
- Purpose / node IDs cited: "W2 gravity derivation": discrete Laplacian -> Ricci -> Einstein equations; Schwarzschild; galaxy rotation without dark matter (L3-14). Cites A-115 / Book 5 Ch1 (L7), D-409 (L27-32).
- Point rotation: not present.
- Path rotation: circular speed v = sqrt(|g_total| r) (L414). No L.
- Field: scalar pressure P; D-409 12 FCC offsets defined (L57-71) but never used — laplacian_3d uses 6 cubic neighbors (L94-105; comment L103-104 admits it). "Ricci" tensor = 8pi * second derivatives of P (L223-249) with only the xy off-diagonal filled; R_00 = 8pi * Laplacian (L238), so trace double-counts the Laplacian. Metric fixed Minkowski (L281). No curl, no chi, no grad chi; gravity is not g = -alpha K_L grad chi.
- Magnetism: none.
- Parent/child: none.
- Hard-coded targets / refits: Schwarzschild P(r) = 1 - r_s/r is inserted by hand (L159-164, L491) then "recovered". kappa = 8pi asserted (L145, L237, L291). g_wake = 2 r_s / r^3 = 4M/r^3 (L407-408) — falls faster than g_local = M/r^2, so it cannot flatten curves, yet the summary prints "Galaxy rotation curves match observation" (L551).
- Pass criterion: `satisfied_einstein_equations` = deviation < 0.1 (L309) and Schwarzschild checks (L356-357: |R| < 1e-6 at r=100 — actual |R| = 4e-6 for M=1, so this flag is False). Regardless of these computed bits, L536-561 unconditionally prints "FULL IMPLEMENTATION COMPLETE", "G_mu_nu ∝ T_mu_nu relationship holds", "READY FOR PUBLICATION". Pass is printed, not computed.
- Violations:
  - gravity_emergence_validator.py:536-561 — success claims hard-printed independent of computed pass bits (L309, L356-357).
  - :159-164, :491 — target (Schwarzschild) inserted as input and reported as recovered.
  - :57-71 vs :94-105 — D-409 12-neighbor claimed, 6-neighbor used.
  - :407-414, :551 — g_wake ∝ 1/r^3 claimed to explain flat curves.
  - Gravity not in canonical K_L grad chi form; no grad chi = 0 -> g = 0 test.
  - Point rotation absent.

## solvers/hadron_collision_simulator.py (288 lines)
- Purpose / node IDs cited: Photon-hadron "collisions" to measure binding energies via knot breaking (L2-13). No node IDs. Imports hadron_knot_geometry (L19-23). Writes JSON to stale path /home/claude/one-wave-science/solvers/ (L279).
- Point rotation: not present (no spin/omega/L of the knots).
- Path rotation: not present.
- Field: not present (weave energy from imported calculator, L60).
- Magnetism: none.
- Parent/child: none.
- Hard-coded targets / refits: EXPERIMENTAL_BINDING_ENERGIES proton 7.289, neutron 8.665, Lambda 1115.68, pi+ 139.57 (L137-142); docstring lists pi+/pi0 "binding 135 MeV" (L11-12). These mix nuclear binding numbers (7.289/8.665 are not proton/neutron binding energies of single nucleons) with full rest masses. weave sigma_T=0.012, kappa_T=0.010 "calibrated" (L155-161). "Collision" outcome is a threshold rule with 0.9 / 0.1 efficiencies (L75-82); the binding_energy reported in main is just total_weave_energy*1000 (L220), not a collision measurement; measure_binding_energy() (L99-133) is never called.
- Pass criterion: |measured - experimental| < 20% -> "MATCH" (L226). Mass/energy fit, not rotation.
- Violations:
  - hadron_collision_simulator.py:137-142, :220-226 — experimental values used as targets with mixed/incorrect definitions; "measurement" is the input weave energy.
  - :75-82 — arbitrary 0.9/0.1 constants presented as collision physics.
  - :279 — writes to stale absolute path.
  - No Point/Path/Field rotation content (node-incomplete per canon if read as a particle model).

## solvers/hadron_flavor_dependent_scaling.py (260 lines)
- Purpose / node IDs cited: Scan alpha_strange so the Lambda mass fits while nucleons stay < 10% (L3-13). No node IDs. Imports hadron_knot_geometry, hadron_mass_predictor (L20-21); sys.path to stale /home/claude/... (L17).
- Point rotation: not present.
- Path rotation: not present.
- Field: not present.
- Magnetism: none.
- Parent/child: none.
- Hard-coded targets / refits: PDG masses proton 938.3, neutron 939.6, Lambda 1115.7 (L24-28) and quark masses (L31-35) are the fit targets; alpha_strange scanned over 13 values and chosen by min Lambda error (L121-188); sigma_T, kappa_T_base, eta_T "from nucleon fit" (L129-131); radius = 0.85 * m_scale^alpha (L97-106). Overrides parent compute_boundary_radius (parent at hadron_mass_predictor.py:123, called at :336/:419/:451, so the override is live). "original_lambda_error = 29.9" hard-coded (L205).
- Pass criterion: p, n < 10% and Lambda < 15% -> "KEYSTONE UNLOCK SUCCESSFUL" (L227-232). Mass fit to the same masses used as targets.
- Violations:
  - hadron_flavor_dependent_scaling.py:24-28, :121-188, :227-232 — measured hadron masses used as fit targets, success reported as explanation (fit-then-claim).
  - :17 — stale sys.path.
  - No rotation content.

## Slice summary
- Canonical point rotation (L = I omega, kept spin, open/closed magnetic switch dL/dt = 0 vs -gamma L, axis stability by inertia): implemented in NONE of the 10 files. No file defines I, L, attitude, or a torque.
- Rotation-related violations:
  - Path speed used as rotation: galaxy_rotation_constant_inherited_velocity.py:125-128 (parent orbital ride imposed as child disk rotation); galaxy_rotation_inherited_rotation_field.py:62-67 (rotation rate made from bulk flow speed / size), :92-95,:173 (0.3 x parent rate added raw).
  - No parent/child transport anywhere; all parent contributions added raw: c319_corrected.py:236, c319_magnetic_coupling.py:161, cascade_wake_validator.py:222, constant_inherited_velocity.py:128, inherited_rotation_field.py:173.
- Magnetism violations: c319_corrected.py:165,233 and c319_magnetic_coupling.py:160 multiply gravitational acceleration by a hand-set "magnetic coherence" scalar (magnetism altering gravity; not via K_L = I + kappa_R R; R not built from B; B strength set but unused at magnetic_coupling.py:60,64). inherited_rotation_field.py:75,95 magnetic scalar gates inherited motion. No file builds W_B = B⊗B - |B|^2 I/3, no K_L tensor, no kappa_R, no chi / grad chi, no grad chi = 0 -> g = 0 check.
- Gravity form: none uses g = -alpha K_L grad chi. galaxy_rotation_validator.py uses -grad P (with doubled sign, L144/155); gravity_emergence_validator.py maps P second derivatives to "Ricci" with Schwarzschild inserted by hand.
- Hard-coded targets / fit-then-claim: every file. Most serious: generate_publication_figures.py (literal "predictions" equal to experiment, synthetic calibration surface, g-2 "-158 lattice correction"), gravity_emergence_validator.py:536-561 (success printed unconditionally), hadron_collision_simulator.py:220 ("measured" = input energy), hadron_flavor_dependent_scaling.py (PDG masses fitted then "keystone unlock").
- Other defects: unit/period error inherited_rotation_field.py:68,87,238 (Myr vs Gyr, ~1000x); unreachable pass tiers c319_magnetic_coupling.py:279-284; docstring/code contradictions c319_magnetic_coupling.py:12,74 vs 119/160 and inherited_rotation_field.py:164 vs 92-95; D-409 12 neighbors declared but 6 used (gravity_emergence_validator.py:57-71 vs 94-105; figures L87-123).
- Live vs dead: galaxy_rotation_cascade_wake_validator.py is a live import dependency (used by c319_magnetic_coupling, constant_inherited_velocity, inherited_rotation_field). galaxy_rotation_constant_inherited_velocity.py is imported by solvers/galaxy_external_validation.py (live). hadron_flavor_dependent_scaling.py depends on live hadron_mass_predictor / hadron_knot_geometry. Standalone/legacy scripts with no importers found: galaxy_rotation_c319_corrected.py (also executes on import), galaxy_rotation_c319_magnetic_coupling.py, galaxy_rotation_inherited_rotation_field.py (superseded by constant_inherited_velocity per its L5-7), galaxy_rotation_validator.py, gravity_emergence_validator.py, hadron_collision_simulator.py and generate_publication_figures.py (both write to stale /home/claude/one-wave-science paths, L279 / L37). None is a canonical point-rotation solver.
