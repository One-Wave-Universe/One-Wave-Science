# Code ledger — slice c10 (24 files)

## Nexus_Integration/Truth_Computer/truth-computer-core.js
- Purpose / node IDs cited: browser-side Truth Computer trace builder. Classifies records into canonical/observed/one-wave/candidate/unknown by regex over status text (14-31), maps OG-00..OG-21 spine stages to questions (61-87) and keyword evidence (89-115), adds a scale-invariance section (117-133), builds a trace (135-174). Node IDs: OG-00..OG-21 only.
- Point rotation: not present.
- Path rotation: not present.
- Field: not present. "field" appears only as an evidence keyword (91, 104).
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none. Classification is by regex, so "active" in any field ranks a record as canonical (29), which is a weak truth gate but not a physics refit.
- Pass criterion: none. The output is a ranked trace; `missingEvidence` = no records (171).
- Violations: none against the physics rules. Side note: status regex ordering means "unresolved" -> candidate (26), and any "active" text -> canonical (29). This is a classification weakness, not a rule violation.

## Nodes/D-413_Ground_Lattice_Orbital_Restoring_Simulation/simulate_d413.py
- Purpose / node IDs cited: D-413 reduced triangular Ground lattice plus an imposed Gaussian "curvature well" plus a rigid elliptical "displacement shell" packet with (x,y,vx,vy,theta,omega) (13). Status YELLOW (54).
- Point rotation: scalar `omega`, `theta` in Q (13), with scalar `packet_inertia=1.6` (11). The initial omega is set per case: 0 / 0.08 / 0 / 0 / 0 (52). What changes it: `shell_force` integrates the gravity-well gradient (`sx=-p.gravity*gx`) over 24 shell points and builds torque `tau += rx*sy - ry*sx` (33). It returns `p.spin_coupling*tau/N - .045*q.omega` (34), and the step applies `q.omega += tau/p.packet_inertia*dt` (40). So **the gravity gradient spins the point up from omega=0**, with a hard-coded 0.045 drag that always damps spin. There is no open/closed magnetic switch, no parent organization target rate, and the shell geometry is the only coupling (`asymmetry`, 31).
- Path rotation: the packet orbits the well. `orbital_L = dx*vy - dy*vx` is logged (42) but carries no separate state. The well also drives translation (34, 40).
- Field: there is no curl or chi field. The lattice has edge strain and compression `comp` (36). The packet's pressure and compression push the lattice (36), but the lattice does not act back on the packet: the packet is driven only by the imposed well (33-34).
- Magnetism: not present. There is no B, R, K_L or kappa_R. The well is an imposed scalar gradient (26-29) and gravity = `-p.gravity*grad` (33), not `-alpha K_L grad chi`.
- Parent/child: not present.
- Hard-coded targets / refits: none observational. Its limitations list says the well is imposed, not derived (54).
- Pass criterion: four checks (54). Zero-input drift; **"asymmetric_shell_generates_more_spin_than_symmetric_ablation"**, which requires the gravity well to produce point spin; the well bends the path; the lattice strains. Pass is partly the point spin being created by gravity.
- Violations:
  - simulate_d413.py:33-34,40: gravity (the well gradient) applies torque and starts/changes point rotation. This contradicts "Gravity does not start or affect point rotation" and "a thing keeps the point spin it has; it does not start one on its own."
  - simulate_d413.py:54: a pass criterion rewards gravity-generated spin.
  - simulate_d413.py:34: unconditional spin drag `-.045*omega`. This is a dL/dt = -gamma L decay with no magnetic open/closed switch.
  - simulate_d413.py:11,13: inertia is scalar, so the greatest/least-inertia axis stability cannot be represented.
  - Field curl is absent. Point, Path and Field are not three separate rates (incomplete).

## Nodes/D-415_Hexagonal_Lattice_Interaction_Dynamics/simulate_d415.py
- Purpose / node IDs cited: D-415 runner. Cites C-323, A-115, E-532, E-531, D-408, D-412, C-318 (2-12, 129, 166). It evolves 2-D site displacement u with bulk/shear/grad-chi/oriented-residual/curvature bond responses (143-168).
- Point rotation: not present. `C` is a fixed "oriented residual" vector per bound site (162-163, 203-204). It is zeroed when a site is unbound (233, 242) and has no rate, inertia or L.
- Path rotation: not present.
- Field: `chi_n = -sum e·(u_j-u_i)` (103-117); Laplacian of chi (120-125); `alpha*(chi_j-chi_i)*e` gradient response (160). Outer-annulus `wake_chi_rms` is a wake measure (252-256). There is no curl.
- Magnetism: not present. "gravity view = local compression gradient" is stated in the docstring (6) and payload (385) but never computed as g. There is no K_L or R.
- Parent/child: not present.
- Hard-coded targets / refits: `free_sector_delta_H_ok=True` is hard-coded (292), and `dual_harmonic_check` returns True as a placeholder (218). This is a receipt field asserting a check that is never run.
- Pass criterion: zero-input no drift/no bound, free packet stays unbound, single core produces bound, energy drift <0.25 (371-379). There is no rotation in the pass bit.
- Violations:
  - simulate_d415.py:292 (and 218): E-531 free-sector check reported True without being computed.
  - Point and Path rotations are absent, so the node is incomplete per the Point/Path/Field rule.
  - The comment at 8 relabels dark matter as wake compression (an interpretation, not computed). There is no direct rule conflict.

## Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/balance_audit.py
- Purpose / node IDs cited: energy and charge audit of the D-415 nonlocal candidate (1). It checks that the force is the negative energy gradient, the kernel is even, the nonlocal quadratic is PSD, the damped ledger refines, and charge follows Q_next=(1-gamma dt)Q (11-92).
- Point rotation: not present.
- Path rotation: not present.
- Field: complex field u. The energy terms are kinetic, gradient, linear, nonlinear, nonlocal (17-24). The U(1) charge Im<u,v> (31-32) is a phase-rotation conserved quantity of the field, not body L.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: eight numerical identity checks (76-82). Status PASS/FAIL (84). The stated scope is "no persistent-mode or physical-law validation" (85).
- Violations: none.

## Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/hybrid_one_wave.py
- Purpose / node IDs cited: a "hybrid" ledger (1). The orbit is advanced by `solar_system_control.step(..., relativity=True)`, i.e. Newtonian plus 1PN (92). A One Wave candidate acceleration is only audited, never added (73, 90).
- Point rotation: not present. There is no body spin.
- Path rotation: orbits integrated by Newton+1PN (outside file). `close_internal_channel` removes net translation and rigid rotation from the One Wave candidate using the system inertia tensor (30-49), so it preserves total orbital L. The net torque is reported (72).
- Field: not present.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: MASSES are measured planetary masses, imported from solar_system_control.py:47-55 (outside slice). Gravity is Newtonian `G*M/r^2` from those masses (solar_system_control.py:127, 140).
- Pass criterion: none in the file. The tests check channel closure and that the explanation is not added to the orbit.
- Violations:
  - hybrid_one_wave.py:54,74,92: the live dynamics are Newtonian/1PN mass gravity, not g = -alpha K_L grad chi. The file declares itself a control/explanation audit (73, 90), so this is a scoped use of Gray physics rather than a claimed One Wave law. It is still the orbit solver used here, and it contains no chi.
  - Point and Field rotation are absent (incomplete).

## Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/nonlocal_field_bench.py
- Purpose / node IDs cited: YELLOW one-field nonlinear nonlocal wave on a periodic triangular lattice with three extended excitations (1-7). It measures windows, phase locks, relational Jacobi coordinates, and Point/Path/Field rotation receipts.
- Point rotation: `rotation_receipts` defines `point_rotation[k] = sum(core*vorticity)/sum(core)`, the core-window (w^2) density-weighted **field vorticity** (279-287). It is diagnostic only. There is no inertia, no L, no state that persists, and no start condition: it is whatever circulation the field has. Nothing explicitly changes it. The math-gap list admits "vorticity is not reliably retained" (sweep_math_gaps.py:85).
- Path rotation: `path_rotation = wrap(angle_now - angle_prev)/dt` of each excitation about the weighted centroid (292-302). It carries no L. The classification "bounded_rotation_candidate" is when the accumulated path rotation >2pi (397-405).
- Field: superfluid velocity `Im(conj(psi) grad psi)/|psi|^2` (210-214), vorticity (215-217), `field_rotation` = annulus-weighted vorticity (286-289), and a stress proxy (221-223). There is no chi or grad chi, and no wake transport.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none observational. The seed phases (0, 2pi/3, 4pi/3) and drift carriers are chosen (94-106).
- Pass criterion: no pass bit. The outcome classification is based on edge lengths and **path** rotation (395-407).
- Violations:
  - nonlocal_field_bench.py:285-287: Point rotation is computed as weighted field curl (vorticity). The canon says field curl is neither point nor path rotation, and point rotation carries L = I omega. Here "point" is a sub-window of the same curl as "field" (286-289), differing only by window weight, so Point and Field are not separate rates.
  - There is no L = I omega bookkeeping (C-306/C-307 not honoured; sweep_math_gaps.py:89 admits "Point, Path, Field ... exchange are not closed").

## Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/planetary_displacement_state.py
- Purpose / node IDs cited: executable state schema for "Updated 38-41" (1-6). Point/Path/Field/Bound2D/RecursivePPF dataclasses plus receipts.
- Point rotation: `RotationState` holds six 3-vectors: core, fluid, mantle, body, em, field (27-33), in `PointState` (37-42). All are **inputs**. There is no inertia, no L, no evolution, and no start/change rule.
- Path rotation: `PathState.rotation = r x v / |r|^2` (53-56). It carries no L. It is a relational angular rate.
- Field: `FieldState` with slope, curvature, active_range, rotation vector, em_shell, reference_slope (59-67). `local_reference_slope` DeltaS = S_local - S_ref (114-122). `distinguishable_active_range` (125-133). There is no chi tensor and no curl computation.
- Magnetism: `em_shell_modifier` K_eff = K0 [1 + eta C] (162-164) is a **scalar** stiffness modifier with C supplied externally. It is not R from B (no W_B = B⊗B - |B|²I/3) and not tensor K_L. There is no gravity computed here, so "B produces gravity when grad chi=0" is not testable. The test asserts C=0 leaves K0 (test file 49-50).
- Parent/child: `rotation_differentials` subtracts core-mantle, body-em, body-field and body-path vectors raw (136-144). There is no frame transport (no R_c^T omega_p). `shear_measure` H = sum gamma_ab |DeltaOmega_ab|^2 (147-159) is computed on untransported differences.
- Hard-coded targets / refits: none in module.
- Pass criterion: none in module.
- Violations:
  - planetary_displacement_state.py:140-143,156: nested rotations (core/mantle/body/path) are differenced in one shared frame without transport. This contradicts "omega_body = omega_c + R_c^T omega_p; transport first, then add."
  - planetary_displacement_state.py:162-164: the EM modifier is scalar K0(1+eta C), not K_L = I + kappa_R R with R built from B. eta is a free input, effectively an unset kappa_R, so this is not a hard-coded violation, but the shape (scalar, not tensor) conflicts.
  - planetary_displacement_state.py:27-33: point rotations have no L = I omega (C-306/C-307) and no inertia axes.

## Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/render_galaxy_video.py
- Purpose / node IDs cited: MP4 visualization of the D-415 "harmonic trail-lock" spiral-arm hypothesis (1-6). It is labelled "VISUALIZATION IS NOT VALIDATION" (192).
- Point rotation: not present.
- Path rotation: star `angular_rate = 0.055/(0.28+r/460)+noise` is a **hard-coded rotation curve** (40-42). The angle advances by the rate minus a lock pull (210). `pattern_spin = 0.026 t` is hard-coded (105, 201). It carries no L.
- Field: none computed. The "parent-curvature traces" are drawn ellipses (110-116).
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: the rotation curve and arm count (m = 2/3 switching every 16 s, 104) are scripted, not derived.
- Pass criterion: none (renderer).
- Violations: none against the rules. It is a declared visualization. The scripted path rate and pattern speed are noted in case anyone cites the video as evidence.

## Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/sweep_math_gaps.py
- Purpose / node IDs cited: parameter, ablation and dt/size refinement sweep of nonlocal_field_bench (1-56). It writes findings with an explicit math-gap list (83-92).
- Point rotation: indirectly, via `vorticity_retention` (28-29). Gap 85: "Rotational source/transfer: vorticity is not reliably retained."
- Path rotation: via the `classification` from the bench (32).
- Field: sweeps nonlocal_response, nonlinear_response, kernel_length, damping (40-45).
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: none. It reports spreads only.
- Violations: none. It openly records that the Point/Path/Field transfer ledger is not closed (89) and that there is no moving-wake transport (88).

## Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/test_hybrid_one_wave.py
- Purpose / node IDs cited: unit tests for hybrid_one_wave.
- Point rotation: not present.
- Path rotation: test 16-26 checks that the closed candidate has zero net translation and torque (system orbital L is not invented).
- Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: uses measured MASSES via solar_system_control (6, 22).
- Pass criterion: the default is Newton+1PN with zero One Wave (10-14); closure (16-26); the explanation is not added to the orbit (35-41); non-finite input is rejected; finite step.
- Violations: none in the test itself. It locks in Newtonian+1PN as the orbit dynamics (see the hybrid_one_wave entry).

## Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/test_nonlocal_field_bench.py
- Purpose / node IDs cited: unit tests for the Laplacian, kernel, translation covariance, relational invariance, minimum image, finiteness, harmonic branches, lock hysteresis, and descriptor finiteness (19-96).
- Point rotation: not tested. `rotation_receipts` has no test.
- Path rotation: not tested directly.
- Field: descriptors are only checked to be finite (85-96).
- Magnetism / Parent-child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: numerical properties only.
- Violations: none. Gap: there is no test that Point, Path and Field rotations are distinct, or that point spin is conserved.

## Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/test_planetary_displacement_state.py
- Purpose / node IDs cited: tests for the planetary state schema with a made-up "Earth" state (12-23).
- Point rotation: input vectors core 1.1, fluid 0.9, mantle 1.0, body 1.0, em 0.8, field 0.7, all on z (14-16). They are arbitrary, not Earth data.
- Path rotation: r=(1,0,0), v=(0,1,0) gives path rotation (0,0,1) (38-39).
- Field: slope and active-range tests (27-36).
- Magnetism: `em_shell_modifier(4,0,99)==4` asserts the EM modifier vanishes with coupling C=0 ("no global dipole control", 49-50).
- Parent/child: core-mantle differential 0.1 and matter-em 0.2 are asserted by raw subtraction (46-47).
- Hard-coded targets / refits: none observational. The name "Earth" is a label only.
- Pass criterion: arithmetic identities.
- Violations: test_planetary_displacement_state.py:46-47 locks in untransported rotation differencing (same issue as planetary_displacement_state.py:140-143).

## One_Wave_Animator/app/canvas_view.py
- Purpose / node IDs cited: PySide6 scene canvas for a 2-D cutout animator (background, character layers, z-order, save/load). There are no node IDs.
- Point rotation / Path rotation / Field / Magnetism / Parent-child: not present. Items have no rotation.
- Hard-coded targets / refits: none.
- Pass criterion: n/a.
- Violations: none (not physics).

## One_Wave_Animator/app/graphics_items.py
- Purpose / node IDs cited: QGraphicsItem subclasses: image layer, locked background, draggable aspect-locked resizable character (19-147).
- Point rotation / Path rotation / Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: n/a.
- Violations: none.

## One_Wave_Animator/tests/test_gui_smoke.py
- Purpose / node IDs cited: headless GUI smoke test: import, drag, resize, reorder, delete, save, reload (30-94).
- Point rotation / Path rotation / Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: expects an 800x450 sample background (37).
- Pass criterion: the round-trip scene equality holds.
- Violations: none.

## One_Wave_Bench/brain/command_memory.py
- Purpose / node IDs cited: verbal command memory (follow / hurry up / slow down / stop). It maps commands to a BC-DC / TC-AC / QC-RC route, does Hopfield-style recall with a Boltzmann confidence, keeps hash-chained learning receipts, and runs an M4 dual-state router (Expressive = Field/Dream proposes, Compressive = Void/Administrator commits) (1-17, 239-345).
- Point rotation: "rotational_phase" = phase_quadrant * pi/2 (76-78) is a routing label, not physical rotation.
- Path rotation / Field / Magnetism / Parent-child: not present physically. "Field" and "Void" are state-machine names (191-213).
- Hard-coded targets / refits: none.
- Pass criterion: n/a. Stop always commits with Administrator permission (292-296).
- Violations: none (not physics).

## One_Wave_Bench/brain/nested_rotation.py
- Purpose / node IDs cited: "Declared Point-Path-Field nesting and threshold/season cycles" schema (1-6). Carriers run quantum magnetic -> electric -> quark vortex -> proton knot (33-37).
- Point rotation: `point_phase` is a phase angle in [0,tau) per carrier (77, 85-87). There is no rate, no L, no inertia, and no evolution.
- Path rotation: `path_phase` (78). A phase only.
- Field: `field_phase` (79). A phase only.
- Magnetism: the "Quantum magnetic" carrier is a label (35). There is no B.
- Parent/child: `contained` children must be from a smaller carrier layer (82, 90-93). There is no rate composition or frame transport, and phases are not composed at all.
- Hard-coded targets / refits: threshold bands 100-90 ... 15-0 with gaps (49-57). These are declared, not physical.
- Pass criterion: schema validation only.
- Violations: none. It requires all three Point/Path/Field slots (consistent with the "three separate" rule) but as phases without L, which is incomplete rather than contradictory. The docstring disclaims physical derivation (3-5).

## One_Wave_Bench/brain/rabbit_hop_scale_rail.py
- Purpose / node IDs cited: 1-12 outward N*2 / 12-24 division address rail (1-7, 57-115).
- Point rotation / Path rotation / Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: n/a.
- Violations: none.

## One_Wave_Bench/brain/receipt_store.py
- Purpose / node IDs cited: append-only, flock-guarded JSONL store for command learning receipts (12-50).
- Point rotation / Path rotation / Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: n/a.
- Violations: none.

## One_Wave_Bench/brain/test_command_memory.py
- Purpose / node IDs cited: tests for the command routes, locked direction words, Void/Field ternaries, recall, receipt chain, and the M4 router (17-167).
- Point rotation: tests that the four phase quadrants are covered (98-100). This is a routing label only.
- Path rotation / Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: behavioural assertions on the router.
- Violations: none.

## One_Wave_Bench/brain/test_nested_rotation.py
- Purpose / node IDs cited: tests for threshold bands, seasons, carrier nesting, and that every receipt has Point/Path/Field phases (13-68).
- Point rotation: asserts that the three phase slots exist (39-43). There is no L.
- Path rotation / Field: phases only.
- Magnetism: label only.
- Parent/child: nesting order only (45-68). There is no transport.
- Hard-coded targets / refits: none.
- Pass criterion: schema assertions.
- Violations: none.

## One_Wave_Bench/dynamics/asymmetric_oscillator.py
- Purpose / node IDs cited: 1-D double-well oscillator `x'' + c x' + a x^3 - b x - h = u(t)`. It is a gate-mechanics candidate, explicitly "not the foundational One-Wave field equation" (1-11).
- Point rotation: not present. `omega_ref` is a damping reference frequency, not spin (31, 42).
- Path rotation / Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: none in the module. It gives exact equilibria, fold bias, and an energy ledger residual (182-187).
- Violations: none.

## One_Wave_Bench/engine/build_manifest.py
- Purpose / node IDs cited: scans One_Wave_Bench/runs receipts into manifest.json for the bench UI. Engine "D-413" (47).
- Point rotation: it carries a `spin` series from receipts (24), i.e. the D-413 gravity-torque spin above. It does not compute it.
- Path rotation / Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: it copies each receipt's `all_checks_pass` (40, 51).
- Violations: none directly. It propagates D-413 receipts whose pass includes gravity-generated spin (see simulate_d413.py:54).

## One_Wave_Bench/engine/electrical/__init__.py
- Purpose / node IDs cited: package init for a DC resistive Kirchhoff/Ohm solver (1-23). It explicitly excludes magnetics (8).
- Point rotation / Path rotation / Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: n/a.
- Violations: none.

## Slice summary
- **Canonical point rotation:** no file in this slice implements it (L = I omega, kept unless magnetically closed, dL/dt = 0 / -gamma L switch, gravity-independent, transported parent/child rates). No file has an open/closed magnetic switch, a parent organization target rate, R built from B, tensor K_L, or g = -alpha K_L grad chi.
- **Violating / non-canonical:**
  - D-413 simulate_d413.py is a live bench engine, fed into One_Wave_Bench/engine/build_manifest.py. The gravity-well gradient torques the shell and spins the point up from omega=0 (33-34, 40). Spin decays with an unswitched drag of 0.045 (34). Inertia is scalar. Its pass check rewards gravity-made spin (54).
  - nonlocal_field_bench.py (D-415) is live YELLOW. "Point rotation" is core-weighted field vorticity (285-287), the same curl as "field rotation" with a different window. There is no L.
  - planetary_displacement_state.py (D-415) is a schema. Nested rotations are differenced without R^T transport (140-143). The EM modifier is scalar K0(1+eta C), not tensor K_L from B (162-164). The test locks in the raw differencing (test 46-47).
  - simulate_d415.py: hard-coded `free_sector_delta_H_ok=True` / placeholder check (218, 292). It has no Point or Path rotation.
  - hybrid_one_wave.py: the orbit dynamics are Newton+1PN with measured masses (via solar_system_control.py, outside slice). It is a declared control, but there is no chi gravity.
- **Live solvers vs dead/legacy:**
  - Live physics benches: simulate_d413.py, simulate_d415.py, nonlocal_field_bench.py (plus balance_audit and sweep_math_gaps as audits of it), hybrid_one_wave.py.
  - Schemas without dynamics: planetary_displacement_state.py, nested_rotation.py.
  - Visualization only: render_galaxy_video.py, which uses a scripted rotation curve.
  - Non-physics: truth-computer-core.js, the Animator files, command_memory/receipt_store/rabbit_hop_scale_rail and their tests, asymmetric_oscillator.py (gate candidate), build_manifest.py, and electrical/__init__.py.
