# Ledger — slice s10 (36 files, all read in full)

## D-415 — One Wave Hybrid Physics Architecture   (`Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/HYBRID_PHYSICS.md`)
- Gate / lifecycle: subordinate to `AI_CANONICAL_START_HERE.md`, node metadata, UPDATED_38–41 (L3-5). One Wave channel "deliberately zero by default" (L39). Conservation gate = "numerical audit gate, not the final One Wave derivation" (L35).
- Upstream: AI_CANONICAL_START_HERE.md, UPDATED_38..UPDATED_41, MATH_INTEGRATION_MAP.md. Downstream / cites: Gray N-body control, 1PN, SPICE/Horizons, Einstein-Infeld-Hoffmann (L18-20).
- Core claim: "The simulator advances one barycentric state. It does not run three competing universes." (L9-10). One Wave mechanism "is not added to the relativistic acceleration" (L21-22). Each timestep emits "net-translation balance, and rotation balance of the channels" (L26).
- Equations: `a_control = a_Newton + a_1PN`; `OneWave_mechanism -> reconstruct geometry/stress response -> compare with a_1PN` (L13-14).
- Point / Path / Field role: none stated by name; Field substance/stress/flow/boundary/wake/EM/phase is the reconstruction channel (L23-24). Closure removes "rigid rotation components of a candidate internal acceleration" (L32-34).
- Magnetism / gravity / rotation link: EM listed as one Field ingredient of the explanatory channel (L23-24); not added as a gravity term. Rotation balance audited each step.
- Open / parked / not-set items: 7 requirements before nonzero channel (L42-49): Field state/evolution eq; Field->body acceleration map; energy functional matching momentum/torque closure; moving-wake transport law; phase-lock transfer (build/hold/break/hysteresis); differing prediction; refinement/ephemeris comparison. Scale transition needs declared length/time/energy/amplitude (L53-56).
- Conflicts: none.

## D-415 — Simulation Audit: Where New Mathematics Is Required   (`Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/MATH_GAPS.md`)
- Gate / lifecycle: "useful Yellow result" (L7). Oct 5 balance derivation closes energy/phase-charge accounting subproblem only (L97).
- Upstream: D-415 bench. Downstream / cites: `sweep_math_gaps.py`, `BALANCE_DERIVATION.md`, `balance_receipt.json`, `Lambda_ab`, `Psi`.
- Core claim: "does not yet produce persistent, rotating, phase-locked three-excitation motion" (L5-7). Hyperradius ~0.41; vorticity RMS ~0.074 of initial (L20-21); no completed harmonic lock return (L22).
- Equations: none (numeric receipts only: dt 0.02/0.04/0.08 -> 0.412/0.413/0.415).
- Point / Path / Field role: "smooth phase gradients are predominantly curl-free. Persistent distributed rotation needs either derived topological defects, a multi-component order parameter, or an explicit transport/circulation state coupled to `Psi`" (L42-45). "Point, Path, Field, EM, boundary, and nonlocal channels need one ledger. No rotation, amplification, or orbital response may appear without a matching Field exchange." (L69-71). Moving wake lacks material derivative (L63-65).
- Magnetism / gravity / rotation link: EM listed as a ledger channel (L69); otherwise none stated.
- Open / parked / not-set items: 8 gaps: persistent-mode potential; rotation generation/transfer; harmonic feedback operator (`Lambda_ab` does not alter Field update); derived nested nonlocal kernel; moving-wake eq; conserved transfer ledger; dimensionless scale law; measurement identity. Spatial rotation ledger, confinement, kernel derivation, three-excitation solution still open (L97).
- Conflicts: possible tension only — §2 "Rotation generation and transfer" (L40-45) seeks a mechanism generating rotation from the Field, versus canonical "a thing does not start [point spin] on its own"; and L69-71 single ledger exchanging rotation between Point/Path/Field could imply Path carrying L, versus G-769 (Path carries no L). Not explicit contradiction; flag for review.

## D-415 — Existing-Math Integration Map   (`Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/MATH_INTEGRATION_MAP.md`)
- Gate / lifecycle: D-415 nonlinear potential and global kernel are "isolated Yellow experiments … not the canonical planetary law" (L161-164). Promote nothing until D-412 receipt and dimensional declarations pass (L157).
- Upstream: authority order (L15-23): AI_CANONICAL_START_HERE.md, 00_MASTER_INDEX.md, ONE_WAVE_TERMINOLOGY_LEGEND.md, I-06 YAML metadata, UPDATED_*, audit/internal-proof files, node math, book Gray/2D/3D, sim receipts. UPDATED_38, 39, 40, 41 (L32-57).
- Downstream / cites (nodes defined/listed): A-101 Ground/Zero, A-102 Displacement, A-103 Differential, A-104 Gradient, A-105 Restoring Response, A-106 Pressure Response, A-107 Bounded Motion, A-109 Inertial Memory, A-112 Persistent Mode, A-112a Traveling Lattice Rupture, A-115 Unified Compression Field, A-116 3D Spherical Default, A-117 Dimensional Integrity; B-206a Shared Boundary, B-206b Four Views, B-216 Threshold Mathematics, B-220 Scale Layer, C-303 Kinetic Energy, C-307 Angular Momentum, C-310 Resistance Field, C-311 Electric/Magnetic Duality, C-313 Lorentz Invariance Conflict, C-317 Boundary-Tension Weave, C-318 Four-Interaction Mass-Effect Response; D-401 Flux, D-402 Resonant Mode, D-404 Nested Resonance, D-405 Harmonic Shell, D-408 2D six-neighbor lattice, D-409 3D twelvefold, D-410 4D recurrence shell, D-412 sim/receipt standard, D-413 Ground lattice orbital-restoring sim, E-503 pressure-gradient energy, E-518 relativistic energy-density, E-524 Kuramoto sync. Files: solar_system_control.py, hybrid_one_wave.py.
- Core claim: "D-415 must ingest that work; it may not restart the framework from a new candidate equation" (L8-9). UPDATED_41: "no universal cutoff, memory relay, mass-only well, or bolt-on magnetic gravity term" (L56-57).
- Equations (L107-126): `x = Delta_ref(psi, psi_0)`; `CHANGE_ij = LOCAL_SLOPE_i - REFERENCE_SLOPE_j`; `Delta_ij = grad(Phi_i) - grad(Phi_j)`; `S_i = |grad Phi_i|`; `DeltaS_i = S_i - S_ref`; `L2_i = {D_i, C_i, T_i, gamma_i, q_i, phase_i}`; `R_i = {PP, PPa, PF, PaP, PaPa, PaF, FP, FPa, FF}_i`; `DeltaOmega_ab = Omega_a - Omega_b`; `H_shear,i = SUM_ab gamma_ab |DeltaOmega_ab|^2`; `Omega_path,i = |r_i x v_i| / |r_i|^2`; `R_active,i = R[L2D_i, D_i, rho_i, P_i, Pa_i, F_i, EM_i, DeltaS_surroundings]`; `X_i(t+dt) = U[X_i(t), DeltaS_i(t), overlaps_i(t)]`.
- Point / Path / Field role: UPDATED_40 "nine recursive Point–Path–Field components; compressed 2D bound-lattice state; internal differential rotation and shear; matter/EM rotation; path and Field rotation" (L44-49). Path rate given by `Omega_path` (L121). Shear energy from differential rotation (L118-119). State must carry all nine PPF components, internal rotation, EM rotation (L146-148).
- Magnetism / gravity / rotation link: UPDATED_39 "EM shell as integrity/stiffness/response modifier; Mars and Venus no-global-dipole controls" (L40-41); UPDATED_41 forbids bolt-on magnetic gravity term (L56-57). Orbit, spin, tides as state readouts (L55).
- Open / parked / not-set items: functions `R`, `U`, `F` and coupling maps unresolved, need ansatz/dims/ablation/receipt (L129-131). Implementation sequence L146-157.
- Conflicts: none explicit. Watch item: UPDATED_39 "EM shell … orbital model" (L37-40) — EM as orbital response modifier must not become gravity (canonical g = -alpha K_L grad chi, K_L = I + kappa_R R, no magnetic term). The file itself forbids bolt-on magnetic gravity (L56-57).

## D-415 — One Wave Translation of Newtonian and Einsteinian Dynamics   (`Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/ONE_WAVE_NEWTON_EINSTEIN_TRANSLATION.md`)
- Gate / lifecycle: "interpretation aid, not a replacement derivation" (L3). Brick: Gray -> 2D Yellow -> 3D Yellow -> audit (L9). Promotion gate L221-228 (dims, derivation, energy/linear/angular-momentum receipts, Newton/GR limits, convergence, falsifiable prediction).
- Upstream: canonical nodes, UPDATED_38–41, MATH_INTEGRATION_MAP.md. Downstream / cites: Horizons/SPICE, Maxwell.
- Core claim: One Wave "does not alter established equations merely by renaming symbols" (L11-12); any extra term "must not double-count gravity already present in the Gray channels" (L13-14). Reconstruction "is not added to relativity as a second gravity term" (L145-146).
- Equations: `Laplacian(Phi) = 4 pi G rho`; `a_N = -gradient(Phi)` (L23-24); `a_i = G sum[j != i] m_j (r_j - r_i)/|r_j - r_i|^3` (L30); `G_mu_nu + Lambda g_mu_nu = (8 pi G / c^4) T_mu_nu` (L39); `E_A = integral W_A e[Psi] dA`; `q_A = integral x W_A e[Psi] dA / E_A` (L58-59); `rho_2D = P_2D[e[Psi]/c^2]` (L66); `T_mu_nu[Psi] = energy + momentum + pressure + shear + flux` (L99); `Geometry[T[Psi]] -> g_mu_nu` (L105); `a_control = a_Newton + a_1PN`; `OneWave[Psi] -> effective stress and geometry -> a_reconstructed` (L135-137).
- Point / Path / Field role: "Point: the measured excitation center and its internal rotation receipt. Path: the relational history q_A(t) and transported wake. Field: the surrounding Psi, potential/metric response, stress, and flux." (L75-77) "three measurements of one state" (L79-80). Rotation at every scale: "Point rotation: internal circulation/spin measurement / Path rotation: relational orbital or transported curvature history / Field rotation: curl/circulation of surrounding momentum or phase flow" (L124-126). Nested Point-PPF/Path-PPF/Field-PPF "do not automatically modify orbital acceleration" (L129-130).
- Magnetism / gravity / rotation link: §3 "coupling between core rotation, EM structure, Field circulation, and path motion needs a torque and energy-flux equation" (L177-181). §4 "Magnetic coupling cannot be represented by an unlabeled visual shell" (L185-187). Gravity is the Gray/GR control.
- Open / parked / not-set items: 9 missing items (L165-217): canonical action S[Psi,g,A,...], moving-wake transport, internal-to-external rotation transfer, EM coupling, persistent-mode eq, harmonic lock feedback, cross-scale projection, relativistic completeness, falsification.
- Conflicts: (1) L177-181 "Internal-to-external rotation transfer" between core rotation and "path motion" via torque implies L exchange into the Path, in tension with G-769 (Path rotation carries no L) and "a thing keeps the point spin it has". (2) L39 uses the Lambda (cosmological-constant) Einstein equation as Gray control; canonical says no expansion/scale factor — not an expansion claim, but note. (3) Gravity control here is `a_N = -grad Phi` (Gray), not the canonical One Wave `g = -alpha K_L grad chi`; labeled as control, so not a direct conflict.

## D-415 — Nonlocal Three-Excitation Field Bench (README)   (`Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/README.md`)
- Gate / lifecycle: "YELLOW experiment" (L68). planetary_visual.html "is a state-architecture projection, not validation" (L13).
- Upstream: canonical nodes (to derive from). Downstream / cites: nonlocal_field_bench.py, test_nonlocal_field_bench.py, sweep_math_gaps.py, render_galaxy_video.py, planetary_visual.html.
- Core claim: "advances one complex nonlinear Field on a periodic 2D triangular lattice, uses a strictly positive global kernel … without inserting point masses or pairwise force laws" (L4-6). Centers "are observables, not dynamical point particles" (L62-63).
- Equations: `Psi_next = Psi + (1 - gamma dt)(Psi - Psi_previous) + dt^2 [c^2 Laplacian_6(Psi) - alpha Psi - beta |Psi|^2 Psi - kappa(Psi - global_reference(Psi))]` (L48-53).
- Point / Path / Field role: receipt contains "separate Point, Path, and Field rotation measurements for each excitation" (L40-41); vorticity, Field-current velocity (L40).
- Magnetism / gravity / rotation link: visual scenes "Mercury/Sol EM-coupling, Venus rotational-mismatch, nested solar-wake, emergent spiral-arm" (L9-12) — visual only.
- Open / parked / not-set items: next gates L79-83 (derive potential/kernel; conserved PPF rotation transfer ledger; persistent translating excitations; capture/orbit/ejection; 3D/12-neighbor). Ledger open pending canonical Field Lagrangian (L85-87).
- Conflicts: none (galactic "transfers locking toward a next-arm mode" is visual).

## E-527 — Simulation Artifacts   (`Nodes/E-527_Simulation/README.md`)
- Gate / lifecycle: "canonical Bronze validation artifacts for node E-527" (L3-4).
- Upstream: E-527. Downstream / cites: simulate_e527.py, simulation_metadata.json.
- Core claim: cases: constant-supply plateau rejects "product-only cycle claim" (L17-18); "one finite reservoir creates one pulse, not a repeating oscillator" (L20-22); "corrected recharge/depletion/hysteresis model" (L24-25).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: scope limits recorded in metadata JSON (not enumerated).
- Conflicts: none.

## G-721 — Sequence Family Validation   (`Nodes/G-721_Sequence_Validation/README.md`)
- Gate / lifecycle: finite regression receipts.
- Upstream: G-721. Downstream / cites: sequence_family_validator.py.
- Core claim: Fibonacci, Sturmian, Tribonacci Arnoux-Rauzy, plastic/Padovan three-rail; "validate word construction only. They do not prove an android motor advantage." (L11)
- Equations: none. Point/Path/Field: none stated. Magnetism/gravity/rotation: none stated. Open: none. Conflicts: none.

## G-721a — Fibonacci Word Hop Validation   (`Nodes/G-721a_Validation/README.md`)
- Gate / lifecycle: reference validator.
- Upstream: G-721a, `-1(0)+1` choice architecture. Downstream / cites: fibonacci_word_validator.py and CSV/JSON/PNG outputs.
- Core claim: "not a physical-motion simulation and does not replace the live `-1(0)+1` choice architecture" (L19).
- Equations: none (golden-ratio convergence). Point/Path/Field: none stated. Magnetism/gravity/rotation: none stated. Open: none. Conflicts: none.

## G-723 — Spectral Validation   (`Nodes/G-723_Spectral_Validation/README.md`)
- Gate / lifecycle: reference receipts.
- Core claim: eigenvalue and Mahler-measure receipts for Fibonacci, plastic, Tribonacci, Lehmer; "algebraic examples, not physical or android safety thresholds" (L11).
- Equations: none. Point/Path/Field: none stated. Magnetism/gravity/rotation: none stated. Open: none. Conflicts: none.

## (no node) — One-Wave Animator   (`One_Wave_Animator/README.md`)
- Gate / lifecycle: Step 1 scene editor milestone.
- Upstream/Downstream: PySide6 app files.
- Core claim: Windows desktop cartoon scene editor; `.owascene` JSON format (L68-83).
- Equations: none. Point/Path/Field: none stated. Magnetism/gravity/rotation: none stated. Open: drawing tools later (L17). Conflicts: none.

## (no node) — Bench bridge entrypoint   (`One_Wave_Bench/AI_BRIDGE_START_HERE.md`)
- Core claim: root AI_BRIDGE_START_HERE.md is "the single authority for laptop/Jetson terminal route selection" (L3-5). Cites hive-pipe/BRIDGE_DIRECTIONS.md, MODULAR_HYSTERETIC_BRIDGE_MESH.md, GOBLIN_BRIDGE_ROLES.md.
- Equations / Point-Path-Field / magnetism-gravity-rotation / open: none stated. Conflicts: none.

## (no node) — CELL_V1 Petri Dish   (`One_Wave_Bench/App_Center/CELL_V1_Petri_Dish/README.md`)
- Gate / lifecycle: software model; "does not establish that the physical hardware implementation has been proven" (L28).
- Upstream: CELL_V1. Downstream: Miniverse -> M4 body-state packet -> Field/Void council loop (L36-42).
- Core claim: six side connections A+/B+/C+ and A-/B-/C-, Field/Void accumulation, ternary UP/STAY/DOWN, lean, hysteresis, memory, reinjection (L6-13). "The cell state is not clock-sequenced" (L16).
- Equations: none. Point/Path/Field: none stated (gyro-style signals as inputs, L36). Magnetism/gravity/rotation: none stated. Open: Miniverse integration target. Conflicts: none.

## (no node) — AI Council Protocol   (`One_Wave_Bench/App_Center/Composite_Agent_Lab/AI_COUNCIL_PROTOCOL.md`)
- Core claim: M4 chair/body state; Void admin (ALLOW/CORRECT/OVERRIDE/HOLD/ESCALATE); Field sole outward voice; Reference/Parser/Doctor goblins, Goblin Raccoon (L6-13). Council cycle L17-25. "software coordination design" (L49).
- Equations / PPF / magnetism-gravity-rotation / open: none stated. Conflicts: none.

## (no node) — Automated Referenced Quality Loop   (`One_Wave_Bench/App_Center/Composite_Agent_Lab/AUTOMATED_REFERENCED_QUALITY_LOOP.md`)
- Core claim: A+ = weighted score >= 0.95 plus hard gates (L16-21); "Only failed dimensions return to Field" (L24); hard stop after cycle limit (L30).
- Equations / PPF / magnetism-gravity-rotation: none stated. Conflicts: none.

## (no node) — One-Wave Local AI Architecture   (`One_Wave_Bench/App_Center/Composite_Agent_Lab/ONE_WAVE_LOCAL_AI.md`)
- Core claim: local LM is a replaceable component; runtime owns M4, hysteresis, Field/Void, goblins (L4-14); loop L20-32; env vars ONE_WAVE_LOCAL_AI_* (L39-42); "No model credentials belong in the repository" (L45).
- Equations / PPF / magnetism-gravity-rotation: none stated. Open: later stages L51-55. Conflicts: none.

## (no node) — Composite Agent Lab README   (`One_Wave_Bench/App_Center/Composite_Agent_Lab/README.md`)
- Core claim: Void = admin/reference/inhibition/commit; Field = sensing/proposal/action/speech (L24-25); M4 owns hysteretic gates, lean, pressure, "resistance", confidence, memory, reinjection (L38-47). "not evidence that the physical CELL_V1 mechanism has been demonstrated" (L51).
- Equations: none. PPF: none stated ("resistance" is a software state, not mass/organization). Magnetism/gravity/rotation: none stated. Conflicts: none.

## (no node) — Virtual Breadboard Canonical Architecture   (`One_Wave_Bench/BREADBOARD_CANONICAL_ARCHITECTURE.md`)
- Gate / lifecycle: capability states only MISSING/IMPLEMENTING/FAILING/PASSING (L432-436); no-rebuild protection (L560-571).
- Upstream: D-413 (preserved, L7). Downstream: layers 00_RULES..11_INTERFACE (L33-47).
- Core claim: breadboard is a reusable sim/measurement tool, builds external (L5). "No unexplained magic primitives … Do not hide Field/Void, ternary resolution, reinjection … inside a macro" (L86-87). "Reinjection is not an energy source." (L366)
- Equations: energy accounting `source energy = change in stored energy + load energy + modeled losses + declared numerical/model residual` (L357-364).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: Layer 07 MAGNETICS: coupled coils, mutual inductance, three windings W1/W2/W3, field-vector `Bx, By, Bz` (L295-326). "Do not assume a field is spherical or has a desired path" (L326). No gravity/rotation.
- Open / parked / not-set items: stage build order L573-624.
- Conflicts: none.

## (no node) — Virtual Breadboard Qualification Suite   (`One_Wave_Bench/BREADBOARD_QUALIFICATION_SUITE.md`)
- Core claim: 26 permanent regressions (L9-34); Field/Void validation primitive — "HOLD remains a real observable condition" from ordinary electronics (L61-65); hysteretic reinjection primitive (L71-73); flashlight qualification gate (L133-137).
- Equations: none. PPF: none stated. Magnetism: three-winding primitive, coupled coils (L87-89). Gravity/rotation: none stated. Conflicts: none.

## (no node) — Latest Balanced Build Status 2026-09-11   (`One_Wave_Bench/LATEST_BUILD_STATUS_2026-09-11.md`)
- Core claim: status table (L6-20); magnetic/non-contact switching "Development needed"; reinjection "No physical net-energy advantage" (L16-17). Claims boundary: "No runtime, efficiency, lift, stability, spherical-field, or reinjection benefit is accepted without a conventional control" (L43-44). Five lifecycle states are process stages (L41-42).
- Cites: CURRENT_BUILD_ORDER.md, cells/*, brain/BRAIN_CELL_P0.md, speaker/BALANCED_SPEAKER_P0.md, mobility/QC_RC_ROVER_DRONE_P0.md, flashlight/.
- Equations: none. PPF: none stated. Magnetism: Bx/By/Bz characterization of windings (L10). Gravity/rotation: gyro-fed balance loop (L20). Conflicts: none.

## D-412 / D-413 / A-117 — One-Wave Bench README   (`One_Wave_Bench/README.md`)
- Gate / lifecycle: "Stage 01 is a Yellow reduced model: the well is imposed and the shell is a collective coordinate" (L61-62).
- Upstream: D-413 engine (canonical), D-412 sim standard, A-117 native dimension (L4-6). Downstream: index.html, fixed_sim.html, schema/experiment_protocol.json, engine/run_experiment.py, build_manifest.py, runs/.
- Core claim: "same engine and one update law … Camera/projection never changes physics" (L21-22). "Nothing here claims gravity, charge, a proton, a Mirror Gate, or a Mass Effect." (L62-63)
- Equations: none.
- Point / Path / Field role: scenario `orbit_asymmetric` "Bounded shell orbiting an imposed curvature well with induced spin" (L26); `travel_across` displacement with wake (L28).
- Magnetism / gravity / rotation link: explicitly no gravity claim (L62-63); "induced spin" in orbit scenario (L26).
- Open: none. Conflicts: possible tension — L26 "orbiting an imposed curvature well with induced spin" suggests the path/well induces point spin, versus canonical "gravity does not start or affect point rotation" / "does not start one on its own". It is a Yellow reduced model, flagged not a hard conflict.

## (no node; cites G-756 indirectly via pack) — Brain Cell P0   (`One_Wave_Bench/brain/BRAIN_CELL_P0.md`)
- Gate / lifecycle: "software-first architecture; integrated runtime unvalidated" (L3). Lifecycle Idle -> Primed -> Executing -> Vectoring -> Resolving (L76).
- Core claim: View Up / Action Down share one bidirectional gate (L40-45); 3:1 nerve/brain and 6:1 oversight are "architecture ratios to test" (L30-36). Dream/M4 cannot commit; Administrator/Void can (L23-28).
- Equations: none (packet `target + axis + lean(-1/0/+1) + magnitude limit + slew limit + expiry + …`, L107-108).
- PPF / magnetism / gravity / rotation: none stated. Open: L143-154. Conflicts: none.

## G-756 / G-733 — Two sides vs noise   (`One_Wave_Bench/brain/CIRCUIT_NOISE.md`)
- Cites: G-756 ("two rails at every step … CMRR", L9), G-733 (hysteresis, L19).
- Core claim: common-mode rejected by stiff midpoint; differential kick outside dead-band can propose UP/DOWN; "noise does not run the motor" (L21).
- Equations / PPF / magnetism-gravity-rotation: none stated. Conflicts: none.

## (no node) — P0 circuit   (`One_Wave_Bench/brain/CIRCUIT_P0.md`)
- Core claim: rail splitter (TLE2426) is the virtual ground; three windings = three half-bridges; drive law UP/DOWN/HOLD (L19-23); never +V and -V on same winding (shoot-through, L25); back-to-back FETs for bidirectional gate (L31). Admin drives gates; M4 must not own pins (L45).
- Equations / PPF / gravity-rotation: none. Magnetism: windings only. Conflicts: none.

## G-756 — P0 build this   (`One_Wave_Bench/brain/P0_BUILD_THIS.md`)
- Core claim: one nerve + one brain cell; "G-756 is the dictionary on the wall. This file is the bench." (L37). Note: here virtual ground = "two equal resistors" (L10), which CIRCUIT_P0.md L5 says "is not a ground".
- Equations / PPF / magnetism-gravity-rotation: none stated. Conflicts with canonical rules: none (internal inconsistency vs CIRCUIT_P0.md L5 noted).

## G-721 / nested rotation — M4 verbal-command brain   (`One_Wave_Bench/brain/README.md`)
- Upstream: G-721 (rabbit-hop routes, L82), RABBIT_HOPPING_ADDRESS_TRANSLATOR_LOCK.md (L91).
- Core claim: BC-DC / TC-AC / QC-RC chain (L9-22); Field COMPRESS/HOLD/EXPRESS, Void DENY/DEFER/CONFIRM; Jetson GPU=Field, CPU=Void (L59-62).
- Equations: octave `-1 = 1/2, 0 = 1, +1 = 2` (L40-41); rail `(X-1)÷2`, `(X+1)÷2` (L96).
- Point / Path / Field role: "`nested_rotation.py` records Point, Path, and Field rotation at every declared carrier layer: Quantum magnetic, Electric, Quark vortex, and Proton knot. Each larger receipt may contain the smaller receipt, preserving rather than flattening its three rotation phases." (L70-73)
- Magnetism / gravity / rotation link: "Quantum magnetic" listed as innermost carrier layer of nested rotation (L71). No parent/child transport formula stated.
- Open: none stated. Conflicts: none (nesting preserves three rates; consistent with three-rate rule).

## G-753 / G-752 — Brain versus nerve   (`One_Wave_Bench/brain/TRIAD_BRAIN.md`)
- Core claim: "Brain = Dream / M4 / Administrator. See G-753." (L3); nerve = 3:1 three-winding ternary motor; "G-752 DC/AC/QC names, if used, are nerve timing — not brain lobes." (L7)
- Equations / PPF / magnetism-gravity-rotation: none stated. Conflicts: none.

## (no node) — Three-Winding Action / Nerve Cell P0   (`One_Wave_Bench/cells/ACTION_NERVE_CELL_P0.md`)
- Gate: "software contract exists; physical cell unvalidated" (L3).
- Core claim: bounded local action via three windings; one bilateral gate both directions (L46-49); 3:1 schedule (L64-69).
- Equations: none. PPF: none stated. Magnetism: "Measured `Bx/By/Bz` reconstruction instead of inferred field drawings" (L123); magnetic/non-contact switching is development target (L91). Rotation: mobility roll/pitch/yaw leans (L74-77), engineering only.
- Conflicts: none.

## (no node) — Balanced Base Cell P0   (`One_Wave_Bench/cells/BALANCED_CELL_P0.md`)
- Gate: "design specification; bench unvalidated" (L3).
- Equations: `differential = Vplus - Vminus`; `common_mode = (Vplus + Vminus)/2`; `reference_error = measured V0 - declared V0` (L30-34).
- Core claim: "The at-rest state is the latest stable held state, not an automatic return to an old zero" (L67-68).
- PPF / gravity / rotation: none stated. Magnetism: Hall sensing only when a magnetic state is under test (L50); nonvolatile magnetic memory open (L93-94). Conflicts: none.

## (no node) — Balanced Cell Family P0 Index   (`One_Wave_Bench/cells/README.md`)
- Core claim: four quantities per handoff: Direction, Phase, Strength, Reference (L20-23); HOLD "does not mean power off" (L70-72); no new primitive cell for P0 (L83-96).
- Equations / PPF / magnetism-gravity-rotation: none stated. Conflicts: none.

## (no node) — Sensor Cell P0   (`One_Wave_Bench/cells/SENSOR_CELL_P0.md`)
- Core claim: view packet schema (L19-31); "No single sensor is the reference for every scale" (L48); gyros supply angular-rate Views Up, do not drive motors (L51-54).
- Equations: none. PPF: none stated. Magnetism: 3-axis Hall/magnetometer `Bx, By, Bz` (L41). Rotation: gyro angular rate (engineering). Conflicts: none.

## A-111 — Open Data -> Wave Data Pipeline   (`One_Wave_Bench/data/OPEN_DATA_WAVE_PIPELINE.md`)
- Upstream: A-111 (wave representation must declare state identity, coupling rule, timing, propagation; L7-12).
- Core claim: schema `one-wave-wave-data-v2`; `f: null`, `frequency_known: false`; "Never replace null with zero" (L43-46). Metadata-derived waves are not physical waveforms (L38-39, L181-182). "corrected Mirror boundary permits coupling and phase shift with reflection, deflection, roll-off and scattering, without forced geometric penetration. A measured comparison requires the derived four-interaction response" (L188).
- Equations: none (timing contract: `inverse_sample_interval_Hz`, tolerance 1e-9).
- PPF / magnetism / gravity / rotation: none stated. Open: four-interaction response and detector-observable transform not derived (L188). Conflicts: none.

## (no node) — Science data acquisition and Mirror coupling work   (`One_Wave_Bench/data/SCIENCE_DATA_RUNBOOK.md`)
- Core claim: fetch/verify CERN/GWOSC metadata; failures stay failures; "Provider metadata … is not measured strain or collision events" (L17). Prediction route: "Reference the actual update and stable native 3D K/E/M/T profile. Derive boundary coupling and phase response without a penetration port." (L61-62). Mirror-gate coupling test and phase5 mass-claims audit "Neither is a first-principles 3D solution" (L72-77). PDG reference (L51).
- Equations: none. PPF / magnetism / gravity / rotation: none stated. Open: HEPData 403, Gaia DNS failure (L86-87). Conflicts: none.

## (no node) — Jetson archive relay branch-step   (`One_Wave_Bench/data/receipts/science-routes-20261005/BRANCH_STEP.md`)
- Core claim: branch-step receipt for archive metadata relays; HEPData blocked after 3 attempts (L18); CERN CSV acquisition resolved, 21 tests pass (L35-37).
- Cites: GENERAL_REFERENCE_RULES.md, AGENTS.md, AI_CANONICAL_START_HERE.md, AI_BRIDGE_START_HERE.md, ENGINE_EVIDENCE_PIPELINES.md, JETSON_SCIENCE_ARCHIVE_ROUTES.md.
- Equations / PPF / magnetism-gravity-rotation: none stated. Conflicts: none.

## (no node) — M4 Active World and Memory Router   (`One_Wave_Bench/engine/M4_ACTIVE_WORLD_AND_MEMORY_ROUTER.md`)
- Core claim: M4 = memory router, active-world constructor, "state/scale/phase router" (L21); memory path L31; "not a claim about biological consciousness or a verified physical mechanism" (L33).
- Equations / PPF / magnetism-gravity-rotation: none stated. Conflicts: none.

## (no node) — P0 Hexagon Layout   (`One_Wave_Bench/engine/electrical/HEXAGON_LAYOUT_DIAGRAM.md`)
- Core claim: pointy hexagon a+,b+,c+,a-,b-,c- around V_0 nucleus; three phases on opposite vertex pairs; half-bridge per vertex. "No single gate voltage keeps BOTH FETs off when node is at 2.5V … No overlap = no true neutral point" (L101-104). Options 1-4 (L110-126).
- Equations: gate thresholds (Vgs conditions, L89-99). PPF / magnetism / gravity / rotation: none stated (phase windings only). Open: neutral-zone fix unchosen. Conflicts: none.

## (no node) — Electrical (DC batch)   (`One_Wave_Bench/engine/electrical/README.md`)
- Core claim: MNA nodal solver, DCVoltageSource/Resistor/Wire/Ground only; "A passive resistive midpoint … is not fixed. Load it and it moves" (L45-50). Does not touch D-413 engine (L3-8). Cites `Virtual_Breadboard/00_RULES/`.
- Equations: energy = power * duration (L16). PPF / magnetism / gravity / rotation: none; magnetics out of scope (L56). Conflicts: none.

## Slice summary

(a) Nodes/chapters bearing on Point, Path, Field, rotation, magnetism, gravity, inertia, mass, resistance, lattice:
- D-415 (HYBRID_PHYSICS): rotation balance audited per step; One Wave channel zero by default; not added as gravity.
- D-415 (MATH_GAPS): no persistent rotation produced; phase gradients curl-free; requires single Point/Path/Field/EM ledger.
- D-415 (MATH_INTEGRATION_MAP): lists UPDATED_40 nine PPF components, bound-lattice state, matter/EM rotation; `Omega_path = |r x v|/|r|^2`; `H_shear` from differential rotation; UPDATED_41 bans bolt-on magnetic gravity; Mars/Venus no-global-dipole controls.
- D-415 (NEWTON_EINSTEIN): Point = internal spin, Path = orbital history, Field = curl — three measurements of one state; nested PPF not auto-modifying orbit; open torque law for internal-to-external rotation transfer; magnetic coupling must be explicit (Maxwell).
- D-415 (README): per-excitation separate Point/Path/Field rotation receipts; ledger open.
- A-101..A-117, B-206a/b, B-216, B-220, C-303, C-307 (angular momentum), C-310 (resistance field), C-311 (E/M duality), C-313, C-317, C-318 (mass effect), D-401..D-413, E-503, E-518, E-524: cited only by name in MATH_INTEGRATION_MAP.
- One_Wave_Bench README (D-412/D-413/A-117): orbit scenario with "induced spin", no gravity claim.
- brain/README: nested Point/Path/Field rotation receipts per carrier layer (Quantum magnetic, Electric, Quark vortex, Proton knot); larger contains smaller.
- Breadboard architecture/qualification, action/sensor cells: magnetics = coupled windings and measured Bx/By/Bz; no spherical-field assumption. Engineering, not physics nodes.
- A-111 / Science runbook: Mirror boundary coupling, four-interaction response, K/E/M/T profile — no rotation/magnetism statement.

(b) Conflicts / tensions found (none are hard contradictions; all flagged):
1. `Nodes/D-415_.../ONE_WAVE_NEWTON_EINSTEIN_TRANSLATION.md:177-181` — "Internal-to-external rotation transfer" couples core rotation to "path motion" via torque; implies L exchange into the Path, against G-769 (Path carries no L) and "keeps the point spin it has".
2. `Nodes/D-415_.../MATH_GAPS.md:40-45, 69-71` — "Rotation generation" from the Field and a single rotation ledger shared with Path; tension with "does not start [spin] on its own" and Path carries no L.
3. `One_Wave_Bench/README.md:26` — `orbit_asymmetric` "orbiting an imposed curvature well with induced spin": well/orbit inducing spin, against "gravity does not start or affect point rotation" (Yellow reduced model).
4. `Nodes/D-415_.../ONE_WAVE_NEWTON_EINSTEIN_TRANSLATION.md:39` — Gray control uses Einstein equation with Lambda term; canonical has no expansion/scale factor (Lambda not used for expansion here; note only).
5. Watch: `MATH_INTEGRATION_MAP.md:37-40` UPDATED_39 "EM shell orbital model" — EM as orbital response modifier must not become gravity; file itself forbids bolt-on magnetic gravity (L56-57).
- Internal (non-canonical) inconsistency: `brain/P0_BUILD_THIS.md:10` resistor-divider virtual ground vs `brain/CIRCUIT_P0.md:5` "A raw resistor divider is not a ground".

(c) Cross-references outside slice relevant to point rotation / magnetism:
- UPDATED_38, UPDATED_39 (EM shell, no-global-dipole), UPDATED_40 (recursive planetary Point-Path-Field rotation, bound lattice), UPDATED_41 (planetary displacement; no bolt-on magnetic gravity).
- C-307 Angular Momentum, C-310 Resistance Field, C-311 Electric/Magnetic Duality, C-318 Four-Interaction Mass-Effect, A-109 Inertial Memory, A-115 Unified Compression Field, D-413 Ground lattice orbital-restoring sim.
- `BALANCE_DERIVATION.md` / `balance_receipt.json` (D-415), `solar_system_control.py`, `hybrid_one_wave.py`, `nonlocal_field_bench.py`, `One_Wave_Bench/brain/nested_rotation.py`.
- G-756, G-733, G-752, G-753, G-721, A-111; `RABBIT_HOPPING_ADDRESS_TRANSLATOR_LOCK.md`.
