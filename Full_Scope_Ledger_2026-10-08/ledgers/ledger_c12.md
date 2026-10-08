# Code ledger: slice c12 (29 files)

Root: /home/user/One-Wave-Science. All files read in full. No repo edits.

## One_Wave_Bench/logic_core/damping_matrix_dispersion.py
- Purpose / node IDs cited: G-746 / E1 scalar damped Klein-Gordon dispersion (scalar gate GREEN, matrix wrapper YELLOW, E5 YELLOW) (1-17). A-114 lattice z-roots (59-65). Two-channel F/V coupled matrix polynomial (68-86).
- Point rotation: not present. `omega` here is wave temporal frequency, not body spin.
- Path rotation: not present.
- Field: scalar wave dispersion omega(k) = -i gamma/2 +/- sqrt(c^2k^2+omega0^2-gamma^2/4) (20-25); spatial attenuation (36-49); group velocity (52-56). No curl, chi or grad chi.
- Magnetism: not present. `gamma` is wave damping (24), not the closed-magnetic L resistance.
- Parent/child: not present.
- Hard-coded targets / refits: none. Receipt explicitly sets derived_a0=False, closes_E5=False (117-118).
- Pass criterion: algebraic identities (undamped KG recovery, decoupled matrix contains scalar pair).
- Violations: none.

## One_Wave_Bench/logic_core/ground_hold_classifier.py
- Purpose / node IDs cited: logical Ground / center / movement / coherent Hold classifier for the six-route logic (1-7). No node IDs.
- Point rotation: not present. Phase state is an oscillator (x, v/omega), not attitude.
- Path rotation: not present.
- Field: docstring says logical Ground is not a claim of zero Field energy (3-5). No field quantities.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: thresholds only (19-26), no observed values.
- Pass criterion: coherent_hold = choice present AND HOLD AND phase-locked AND energy retained AND topology retained (92-98).
- Violations: none.

## One_Wave_Bench/logic_core/group_velocity_zeros.py
- Purpose / node IDs cited: G-747 two group-velocity zeros; A-114 lattice dispersion (1, 19-26).
- Point rotation: not present.
- Path rotation: not present.
- Field: continuum vg*vp = c_eff^2 (9-16); A-114 lattice vg zero at zone edge k=pi (19-26).
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none; derived_a0=False, closes_E5=False (38-39).
- Pass criterion: vg(pi)=0, small-k vg=0.5, vg*vp=c^2.
- Violations: none.

## One_Wave_Bench/logic_core/hex_lattice_graph.py
- Purpose / node IDs cited: D1 triangular/sixfold graph for "3 > 1(0)1 < 6" on D-408 lattice vectors (1-11). States it is not 3D/4D and not a Mass Effect derivation (10-11).
- Point rotation: not present.
- Path rotation: not present (directed_routes 145-146 are graph neighbors, not turning).
- Field: not present (graph Laplacian 93-108 only).
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: coordination 6, seven-cell, Laplacian kernel constant.
- Violations: none.

## One_Wave_Bench/logic_core/mirror_operator.py
- Purpose / node IDs cited: Mirror operator for center-origin six-route architecture; Mirror = oscillatory phase evolution, never swaps binary relation (1-6).
- Point rotation: not present. `rotate_phase` (39-52) is a phase-space rotation of an oscillator (x, v/omega), amplitude-preserving; it is not body attitude or L. Docstring says damping/drive deferred (44).
- Path rotation: not present.
- Field: not present.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: amplitude preserved, half cycle reverses move, discrete mirror is involution.
- Violations: none.

## One_Wave_Bench/logic_core/path_rotation.py
- Purpose / node IDs cited: G-769 C3 Path rotation, "Kinematics of the ride. Not the point." (1).
- Point rotation: not present by design.
- Path rotation: discrete turning angle between successive center-to-center edges (30-35); path_receipt sums turning, corners, mean edge, curvature (38-54). Carries no L: `"L": None` (51), `"magnetic_gradient_applied": False` (52), `"gravity_coefficient_on_point": 0.0` (53). Regular hexagon helper (57-61) closes at 2 pi.
- Field: not present.
- Magnetism: not present (flag False, 52).
- Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: hex closed path turning = 2 pi, straight path = 0, L is None.
- Violations: none. Canonical for the Path channel (ride carries no L).

## One_Wave_Bench/logic_core/point_rotation.py
- Purpose / node IDs cited: G-749 C2 Point rotation receipts (1). Brick algebra GREEN, inertia origin YELLOW (77-78).
- Point rotation: attitude R (3x3) + omega_body + diagonal inertia (45-49). L_body = I omega (51-56); L_ground = R L_body (58-59). STARTED: only by explicit constructor input (e.g. receipt_planar_spin 69-70); nothing in the module starts a spin. CHANGED: `point_L_dot` (82-89): magnetic_open=True -> dL/dt = 0 (87-88); closed -> dL/dt = -resistance * L (89). Gravity argument is accepted and explicitly deleted (84): gravity does not start or change L. `magnetic_open` is a boolean input, not computed from a B gradient. Euler step in step_L (92-94). Inertia-axis stability: least and greatest stable, middle "fights" (97-99), canonical. No parent "organization" target rate: the closed branch decays L toward 0, not toward a shared lattice rate (no bound-lattice Moon 1:1 / Mercury 3:2 mechanism here).
- Path rotation: receipt asserts path_circulation_stolen=False (75).
- Field: field_curl_stolen=False (76); no field computation.
- Magnetism: only the open/closed switch (87-89); no B, R, K_L or kappa_R built.
- Parent/child: `compose` (62-66) builds R = R_parent R_child (63), correctly, but sets omega = child_in_parent.omega_body only (65). The comment (64) claims "transport child omega into parent body", yet R_c^T omega_p is never computed or added; the parent rate is DROPPED. Canonical is omega_body = omega_c + R_c^T omega_p. The correct function exists in logic_core/body_rate_transport.py `compose_omega_body` (outside slice, lines 34-36) but `compose` does not call it.
- Hard-coded targets / refits: none.
- Pass criterion: det R = 1, L_body = I omega, open gradient keeps L regardless of gravity, closed decays at -resistance L, middle axis fights, and (test) composed omega equals the child omega alone.
- Violations:
  - point_rotation.py:62-66 - parent/child compose drops parent rate (omega = omega_c, not omega_c + R_c^T omega_p); comment at :64 misdescribes the code. Conflicts with G-750 transport rule.
  - (gap, not a contradiction) point_rotation.py:82-89 - no shared-organization target rate for bound bodies; closed branch only damps to 0.

## One_Wave_Bench/logic_core/ppf_schema.py
- Purpose / node IDs cited: C1 recursive Point-Path-Field schema X_s = {P_s, gamma_s, F_s; children} (1-13). Frames ground (A-101), local, path. States it does not derive C2-C4 (5-7).
- Point rotation: PointState has position (m) and a scalar orientation (rad) only (68-82). No omega, no L, no inertia. Not started or changed anywhere.
- Path rotation: PathState start/end/length/circulation, circulation in m/s marked "proxy until C3" (85-102); segment_path sets circulation 0 (164-173). No turning.
- Field: FieldState amplitude + phase, "not a Path substitute" (105-114); zero_field (176-180). No curl.
- Magnetism: unit "T" allowed (34); nothing built.
- Parent/child: children must be scale-1 (127-134). `nest` (183-195) makes the parent Path a bounding-box segment of the child positions (186-188); no rate transport, no frame composition.
- Hard-coded targets / refits: none.
- Pass criterion: unit/frame validation, depth/leaf counts.
- Violations:
  - (incompleteness, declared) ppf_schema.py:68-82 - Point node has no point-rotation rate / L; per the "missing one of three leaves a node incomplete" rule the schema node is incomplete. The module self-declares this as bookkeeping only (5-7), so it is a gap rather than a contradiction.
  - ppf_schema.py:186-188 - parent Path is synthesized from the spatial spread of children, not a ride of the parent; minor conflation of child placement with parent Path.

## One_Wave_Bench/logic_core/six_route_logic.py
- Purpose / node IDs cited: finite reference for "Updated 43" two-choice x three-move logic; disclaims commitment amplitudes, magnetic hardware, consciousness (1-6).
- Point rotation: not present.
- Path rotation: not present.
- Field: not present.
- Magnetism: explicitly not implemented (4).
- Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: exactly 6 addresses 0..5 (77-86); Ground (0,0) and Conflict (1,1) rejected (56-66).
- Violations: none.

## One_Wave_Bench/logic_core/test_body_rate_transport.py
- Purpose / node IDs cited: tests G-750 body_rate_transport.py (module outside slice).
- Point rotation: tests compose_omega_body = omega_c + R_c^T omega_p: planar rates add 1+2=3 (8-10); tilted child pulls parent z into body -y (12-17); body and ground charts agree on |omega| (19-27).
- Path rotation: not present.
- Field: not present.
- Magnetism: not present.
- Parent/child: canonical transport-then-add verified (8-27).
- Hard-coded targets / refits: none.
- Pass criterion: transported sum and chart agreement.
- Violations: none. Note: contradicts the behaviour locked in by test_point_rotation.py:20 (see below).

## One_Wave_Bench/logic_core/test_commitment_map.py
- Purpose / node IDs cited: tests commitment_map.py (outside slice) five-level commitment memory with hysteresis and phase lock.
- Point rotation / Path / Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: none (parameter thresholds only).
- Pass criterion: one pulse cannot fully commit (24-27); repeated aligned drive reaches level +/-3 (29-37); opposite phase blocks drive (39-42); hysteresis (51-71).
- Violations: none.

## One_Wave_Bench/logic_core/test_damping_matrix_dispersion.py
- Purpose / node IDs cited: tests G-746/E1 module above.
- Point / Path / Magnetism / Parent-child: not present.
- Field: dispersion checks (26-51), A-114 unit circle at gamma=0 (54-57), coupling splits roots (64-67).
- Hard-coded targets / refits: none.
- Pass criterion: gate labels and algebraic identities; receipt refuses E5/a0 (46-50).
- Violations: none.

## One_Wave_Bench/logic_core/test_ground_hold_classifier.py
- Purpose: tests ground_hold_classifier.py.
- Point / Path / Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: Ground has no route (13-17), YES/NO holds distinct (19-27), center crossing is not hold (29-36), retention/phase/topology gates (46-66).
- Violations: none.

## One_Wave_Bench/logic_core/test_mirror_operator.py
- Purpose: tests mirror_operator.py.
- Point / Path / Field / Magnetism / Parent-child: not present (phase rotation of oscillator only, 29-46).
- Hard-coded targets / refits: none.
- Pass criterion: choice preserved, involution, amplitude preserved, 2 pi return.
- Violations: none.

## One_Wave_Bench/logic_core/test_path_rotation.py
- Purpose: tests G-769 path_rotation.py.
- Path rotation: hex closes 2 pi with 6 corners (8-11); straight ride 0 (16-20); right angle pi/2 (22-25).
- Point rotation: asserts L is None for a path (12, 25); magnetic gradient not applied (13); gravity coefficient on point 0 (14).
- Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: turning totals and L=None.
- Violations: none.

## One_Wave_Bench/logic_core/test_point_rotation.py
- Purpose: tests G-749 point_rotation.py.
- Point rotation: det R = 1, L_body = (0,0,2) (8-12); ground L rotates with frame (22-26); open gradient keeps L for any gravity (29-35); closed gradient dL = -4 L and ignores gravity, step reduces |L| (37-45); middle inertia axis fights (47-51).
- Path rotation: path_circulation_stolen False (12).
- Field / Magnetism: open/closed boolean only.
- Parent/child: test_compose_multiplies_frames (14-20) uses parent omega (0,0,1) and child omega (0,0,4) with planar R and asserts composed omega_z == 4.0 (20). Canonical transport (omega_c + R_c^T omega_p) gives 5.0. The test locks in the dropped-parent-rate behaviour.
- Hard-coded targets / refits: none.
- Pass criterion: as listed; the compose pass bit is "child rate alone".
- Violations:
  - test_point_rotation.py:20 - asserts omega_body[2] == 4.0, enshrining the parent-rate drop from point_rotation.py:65; conflicts with G-750 rule and with test_body_rate_transport.py:8-10 (which asserts 1+2=3 for the same planar case).

## One_Wave_Bench/media/goblin_raccoon/film_reel.py
- Purpose: audio-first film-reel timeline for Goblin Raccoon Studio animation (1-14). Not physics.
- Point rotation: not present (rotation_deg at 78 is a sprite display angle).
- Path rotation / Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: none (default perspective grid values 38-41 are UI calibration).
- Pass criterion: n/a (no tests in file).
- Violations: none.

## One_Wave_Bench/media/goblin_raccoon/film_reel_renderer.py
- Purpose: renders film-reel project to MP4 via PIL + ffmpeg (1-7, 141-218).
- Point rotation: not present (sprite rotate at 108-109 is image rotation).
- Path / Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: n/a.
- Violations: none.

## One_Wave_Bench/media/goblin_raccoon/studio_api.py
- Purpose: deterministic action API for human UI and AI directors on a FilmProject (1-6).
- Point / Path / Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: n/a.
- Violations: none.

## One_Wave_Bench/media/goblin_raccoon/test_studio_api.py
- Purpose: pytest for studio_api.
- Point / Path / Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: frame math (e.g. 3250 ms at 24 fps -> frame 78, 37), action receipts.
- Violations: none.

## One_Wave_Bench/simulators/chapter_registry.py
- Purpose: coverage registry for chapter-driven simulators (1, 32-56). Cites Book1 Ch01-Ch17, Book2 Ch01, Book5 Ch1-Ch5; C-318 work metric (46).
- Point rotation: listed as motion label only: Ch01 "Point/Path/Field rotation" DIAGNOSTIC via micro/vortex_diagnostics.py (33); Ch02 "proton-knot rotation" (34); Book5 "stellar rotation", "galactic rotation" (51-52). All PLANNED except Ch01/Ch03 diagnostic, Ch14 visual partial, Ch16/Ch17 engine partial.
- Path rotation: Ch12 "orbital Path" (44).
- Field: Ch13 "Field rotation", "precession", gray control "Maxwell plus LLG" (45).
- Magnetism: Ch13 nested EM-PPF, UNBUILT/PLANNED (45). No B/R/K_L.
- Parent/child: not present.
- Hard-coded targets / refits: none (gray controls named only).
- Pass criterion: validate_registry - no duplicates, non-PLANNED entries must name an engine (59-67).
- Violations: none. Note Ch12 gravity and Ch13 magnetism engines are UNBUILT (44-45), so the registry records no live gravity/magnetism solver.

## One_Wave_Simulator/native_3d/test_lab.py
- Purpose: unittest for native_3d server.py Lab (field engine, displacement, cavity model, drive/force protocol, source SHA receipts, HTTP guards). Cites solvers/bulk_excitation.py (85).
- Point rotation: not present.
- Path rotation: not present (imposed translation via np.roll, 27-36).
- Field: complex field stepping with norm/energy conservation (15-25); cavity "response tensor" with max_diagonal_error and zero-mode tensor ~0 (51-64); not curl/chi.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: norm relative error < 1e-12, energy conserved to 12 places, transactional rejection, energy-balance residual 0 under drive, source drift blocks mutation.
- Violations: none.

## Tools/Chats-Animator/c1-path-motion.js
- Purpose: animator UI to lay existing pose frames along a bezier screen path with feet-depth perspective (12-27, 84-110). Not physics; "path" is a sprite path.
- Point / Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: n/a.
- Violations: none.

## Tools/Chats-Animator/c2-walk-cadence.js
- Purpose: converts FPS / beats into pose hold frames (152-178). Not physics.
- All physics fields: not present.
- Violations: none.

## Tools/Chats-Animator/c20-five-scale-architecture.js
- Purpose: Animator command routing through Cells (parse), Nerves (events), DirectorPort, Dream (motion-library reuse, asset requests), Administrator (validation/audit), M4 (route/execute) (11-371). Uses One-Wave scale names as software roles; not physics.
- All physics fields: not present.
- Hard-coded targets / refits: none.
- Pass criterion: selfTest four checks (374-388).
- Violations: none against the physics rules.

## Tools/Chats-Animator/c21-copy-paste-assistant-plugin.js
- Purpose: registers a live AI "creative partner" plugin over local HTTP /api/assistant; UI to paste and save an OpenAI API key (22-35, 105-134, 176-189).
- All physics fields: not present.
- Violations: none against the physics rules. Side note (not a physics rule): requires/stores a developer API key (storesApiKeys: true, 185-186), which differs from the repo CLAUDE.md preference for a non-API-key Claude route; that guidance is Claude-specific, so this is informational only.

## Tools/Chats-Animator/c8-dialogue-frame-sync.js
- Purpose: snaps speech clips to reel frame start times computed from holds/FPS (207-255).
- All physics fields: not present.
- Violations: none.

## Tools/Chats-Animator/c9-voice-recorder.js
- Purpose: MediaRecorder voice take into a Voice Lab layer (263-342).
- All physics fields: not present.
- Violations: none.

## Workshop/chessboard/pointer_controller.js
- Purpose: FIELD and VOID pointer-stick UI over a chessboard; ternary -1/0/+1 display, 3 nerve flips per supervisor exchange, 6 flips per full pipeline (1-8, 41-90).
- Point rotation: not present (stick `rotate(lean deg)` is CSS, 38).
- Path / Field / Magnetism / Parent-child: not present ("FIELD"/"VOID" are UI side labels).
- Hard-coded targets / refits: ratio constants 3 and 6 (6-7) are UI design constants, not observed values.
- Pass criterion: n/a.
- Violations: none.

## Slice summary

Files read: 29 of 29.

Canonical point-rotation implementations:
- One_Wave_Bench/logic_core/point_rotation.py (G-749): L = I omega in body and ground charts; open magnetic gradient dL/dt = 0, closed dL/dt = -resistance L; gravity argument discarded (84) so gravity never starts or changes L; spin only exists if supplied; least/greatest inertia axes stable, middle fights. This part is canonical.
- One_Wave_Bench/logic_core/path_rotation.py (G-769): ride turning with L=None and zero gravity-on-point coefficient. Canonical.
- test_body_rate_transport.py exercises the canonical G-750 transport in body_rate_transport.py (outside slice).

Violations / conflicts:
1. point_rotation.py:62-66 - `compose` sets omega_body = omega_child only; R_c^T omega_p is never added, and the comment at :64 says it transports. Conflicts with omega_body = omega_c + R_c^T omega_p (G-750). The correct function `compose_omega_body` in body_rate_transport.py:34-36 is not used.
2. test_point_rotation.py:20 - asserts composed omega_z == 4.0 (parent 1 dropped), locking in violation 1; inconsistent with test_body_rate_transport.py:8-10 (1+2=3).
3. Gap: point_rotation.py:82-89 - no shared-organization (bound lattice) target rate; closed branch only decays to 0, so Moon 1:1 / Mercury 3:2 locking cannot arise here. `magnetic_open` is a boolean input, not computed from a magnetic gradient.
4. Gap (self-declared): ppf_schema.py:68-82 - Point node has orientation only, no rate/L, so a PPF node is incomplete under the three-rate rule; ppf_schema.py:186-188 parent Path built from children's bounding box.

No file in the slice builds B, R, W_B, K_L or kappa_R, and none computes gravity, chi or grad chi; no magnetism-to-gravity path exists here. No hard-coded observed targets (Mercury 3:2, Moon 1:1, 125 GeV, masses) are used as inputs in slice files.

Live vs dead/legacy:
- Live physics receipts/tests: logic_core point_rotation, path_rotation, ppf_schema, damping_matrix_dispersion, group_velocity_zeros, hex_lattice_graph (all with tests); native_3d test_lab (tests server.py field engine).
- Live logic (non-physics): six_route_logic, mirror_operator, ground_hold_classifier, commitment tests.
- Registry only: simulators/chapter_registry.py (Ch12 gravity and Ch13 EM engines UNBUILT).
- Not physics (animation/media/UI tooling): goblin_raccoon/*, Tools/Chats-Animator/*, Workshop/chessboard/pointer_controller.js.

Cross-references outside the slice that matter: logic_core/body_rate_transport.py (correct G-750 transport, unused by point_rotation.compose); logic_core/commitment_map.py; One_Wave_Simulator/native_3d/server.py and solvers/bulk_excitation.py; micro/vortex_diagnostics.py (Ch01 Point/Path/Field diagnostic); logic_core/zone_edge_a0.py (uses E125_MEV as a gray control, marked not derived, outside slice).
