# Ledger — slice s11 (61 files, all read in full)

Node IDs actually cited anywhere in this slice: D-413, G-735, A-117, D-409, D-410, D-412, C-318, G-759. No file in this slice defines a canonical node; none cites C-306, C-307, C-311, C-319, C-320, G-749, G-750, G-769, A-115, E-528 or E-530.

---

## Bench doc — P0 Ternary Circuit Simulator   (`One_Wave_Bench/engine/electrical/README_CIRCUIT_SIMULATION.md`)
- Gate / lifecycle: "Phase 3 Unblocked" (L381); Phases 4-7 open checklists (L388-410). Tests claimed: 11 DC regressions + 2 P0 ternary (L60, L364).
- Upstream: none cited. Downstream / cites: solver_transient.py, p0_ternary_circuit.py, circuit_controller.py, transient_measurements.py, demo_circuit_controller.py, visualization_server.py, tests/test_dc_regressions.py, tests/test_p0_ternary.py, One_Wave_Bench/hardware/visualization/p0_breadboard_viewer.html (L414-433).
- Core claim: "Complete simulation, testing, and visualization suite for the P0 ternary three-phase motor drive circuit with virtual ground buffer." (L3). Virtual ground held at 2.5 V (L51, L383).
- Equations: P = V*I (L211); duty = on-time / total-time (L212); pass criteria vg_steady in (2.4, 2.6), vg_error in (0.0, 0.1) (L283-285). MNA / Backward Euler / Trapezoidal named, not written out.
- Point / Path / Field role: none stated. Phase 5 lists "Test rotating field generation" (L396) as an unchecked electrical item only.
- Magnetism / gravity / rotation link: only "120° gate sequencing" and "rotating field generation" as future electrical tasks (L395-396). No physics claim.
- Open / parked / not-set items: dead-band comparator, flyback, trapezoidal stability, 3-phase commutation, KiCad/BOM/SPICE, 3D UI (L388-410).
- Conflicts: none.

## Bench doc — P0 Hexagon Transient Stability Findings   (`One_Wave_Bench/engine/electrical/STABILITY_ANALYSIS_FINDINGS.md`)
- Gate / lifecycle: diagnostic findings; unresolved.
- Upstream: solver_transient.py. Downstream / cites: p0_hexagon_hbridge_stable.py, p0_hexagon_hbridge_stable_no_mem_damp.py, test_vary_r_sense.py, test_single_phase.py (L84-88).
- Core claim: "a systemic numerical stability issue in the MNA solver that persists across multiple circuit topologies" (L4); multi-phase diverges at ~35-50 µs, even passive (L11-14); suspected "MNA matrix conditioning/singularity" (L22).
- Equations: none (dt/τ criterion named, L22).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: recommends "Coupled flux instead of voltage: Use magnetic coupling between inductors instead of electrical node sharing" (L70) — circuit engineering, not a physics claim. Mentions "nerve ring coupling", "memory windings" (L29-30).
- Open / parked / not-set items: root cause A/B/C unresolved (L45-60); SPICE parity check (L78-81); topology variants (L91-93).
- Conflicts: none.

## Bench doc — BALANCED FLASHLIGHT P0   (`One_Wave_Bench/flashlight/BALANCED_FLASHLIGHT_P0.md`)
- Gate / lifecycle: P0 plan; VBB status 2026-09-08 "SIMULATION RESULT — not a physical bench result" (L145). Integrated run valid at 5 V, not the 9 V architecture (L195-199).
- Upstream: none cited. Downstream / cites: Virtual_Breadboard/test/flashlight-calibration/, run_flashlight_calibration.js, flashlight-prototype.test.js (L150-152); .github/workflows/breadboard-flashlight-tests.yml (L188).
- Core claim: "Reinjection is not an energy source. It is a control strategy for replacing measured losses only when needed." (L46). Maintenance rule: `state -> decay/loss -> lower threshold -> reinject -> upper threshold -> disconnect -> coast` (L36).
- Equations: none (thresholds 3.2 V / 4.6 V bands, L176-177).
- Point / Path / Field role: none stated in Point/Path/Field vocabulary. Magnetic path: progression to 3 wound axes and "measure Bx, By, and Bz and reconstruct the actual vector path" (L93-100).
- Magnetism / gravity / rotation link: "Do not assume the field is spherical from the coil layout." (L100). Selective reinjection maintaining a field-state band is a test, not a claim (L98).
- Open / parked / not-set items: 9 V -> logic-rail path; matched-brightness continuous-drive comparison (L199); projected battery meter; ferrite module.
- Conflicts: none.

## Bench lock — Balanced Flashlight State-Driven Reinjection Lock   (`One_Wave_Bench/flashlight/BALANCED_FLASHLIGHT_STATE_REINJECTION_LOCK.md`)
- Gate / lifecycle: architecture lock; 14-step pass order (L334-354); missing capabilities listed "Still to prove" (L318-326).
- Upstream: none cited by ID. Downstream / cites: BC-DC -> TC-AC -> QC-RC experiments (L9, L261-302); Virtual Breadboard.
- Core claim: "There is one continuously present virtual-ground / CENTER reference for the whole chain." (L42-43). "Reinjection is state-triggered, not time-triggered" (L68). "Time is not the trigger." (L97). Nerve gate "does not decide the state. It only opens/closes a local route" (L147-148).
- Equations: `B(t) = (Bx(t), By(t), Bz(t))` (L298).
- Point / Path / Field role: hardware analogy only — "BC-DC — point/state ... prove the reference-resolved point/state" (L263-271); "TC-AC — path/phase ... prove reversible path, phase, and zero crossing" (L273-279); "QC-RC — coordinated rotation ... Two phase-shifted AC axes can produce a rotating drive vector in a plane. A third ... can tilt/precess that drive vector through 3D" (L284-291). No Field (curl) layer is named as a separate third element; QC-RC is a rotating electrical drive vector, not field curl.
- Magnetism / gravity / rotation link: "preferred One-Wave hysteresis source is magnetic state / coercivity" (L106-107); square-loop remanence/coercive thresholds (L113); "Do not claim a spherical or volumetric magnetic field from a schematic." (L293); 3D field trajectory only after Bx/By/Bz capability exists (L351-352). No gravity statement.
- Open / parked / not-set items: bilateral nerve-gate regression; spatial B-field solver; magnetic-state-driven reinjection without binary IC; full X/Y -> AC -> rotating-field build (L319-324). Quinary/quaternary deliberately not forced (L31-38).
- Conflicts: none hard. Soft note: the point/path/rotation triad (L263-291) is a hardware analogy that omits a distinct Field-curl element; if read as the canonical Point/Path/Field triad it would be incomplete per the "missing one of the three" rule. The file does not claim it is that triad.

## Bench scope — Flashlight Scope, Ternary Three-Winding Stop   (`One_Wave_Bench/flashlight/FLASHLIGHT_SCOPE_TERNARY_STOP.md`)
- Gate / lifecycle: narrowing note; default stop = ternary three-winding nerve layer (L5-27).
- Upstream: BALANCED_FLASHLIGHT_STATE_REINJECTION_LOCK (implicit). Downstream / cites: none.
- Core claim: "The flashlight does not need to reach QC-RC / quadratic rotating-field behavior." (L7). "The three-winding element is not automatically QC-RC and is not automatically a brain cell." (L31). "The prototype stops at the last useful measured layer." (L74).
- Equations: none (`-1 / HOLD / +1`, L36).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: rotating magnetic-field experiments and Bx/By/Bz are optional follow-on (L45-51).
- Open / parked / not-set items: TC-AC, QC-RC, quaternary/quinary, 3D field claims all optional (L67-72).
- Conflicts: none.

## Media lock — Goblin Raccoon art lock   (`One_Wave_Bench/media/goblin_raccoon/GR_ART_LOCK.md`)
- Gate / lifecycle: hard animator constraint.
- Upstream / Downstream: Animator (implicit). No nodes.
- Core claim: "Goblin Raccoon (GR) artwork supplied by the creator is canonical input." (L7). Ground-contact anchor rule (L31); "The background is the world." (L35); no invented interpolation (L39).
- Equations: none.
- Point / Path / Field role: none stated. ("rotate the complete drawing", L14, is a 2D image transform.)
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: missing poses go through art-generation workflow (L27).
- Conflicts: none.

## Art — Micro film storyboard   (`One_Wave_Bench/micro/MICRO_FILM_STORYBOARD.md`)
- Gate / lifecycle: "art, not a derivation" (L1).
- Upstream / Downstream: none cited.
- Core claim: Shot 1 "black, one Point. Hex grows from it. Six pyramids. Sphere just a bound." (L3); Shot 2 "a seam that is the Mirror" (L4); Shot 3 "Four pressures at once ... Not a bouncing particle." (L5); Shot 4 "basin flip. Same hold, inverted orientation" (L6); Shot 5 "Do not title it Higgs." (L7). "No 125 GeV on screen. No a0." (L9).
- Equations: none.
- Point / Path / Field role: "one Point" as visual origin (L3); no rotation stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## Mobility plan — Balanced QC-RC Rover and Drone P0   (`One_Wave_Bench/mobility/QC_RC_ROVER_DRONE_P0.md`)
- Gate / lifecycle: "system plan; no vehicle build or flight evidence" (L3); 8-step validation ladder (L143-156).
- Upstream: PX4 / ArduPilot docs (L16-23). Downstream / cites: none internal.
- Core claim: native flight controller "owns sensor fusion, attitude/rate stabilization, motor allocation, arming, pilot takeover, and failsafes" (L8-9); One-Wave layer sends "only bounded high-level setpoint leans ... never sends raw motor outputs" (L9-11). 3 nerve cycles : 1 higher-brain function (L55-59). "HOLD does not set motor output to zero." (L104).
- Equations: none.
- Point / Path / Field role: none stated in canonical vocabulary. Engineering attitude/rate: gyros provide "fast roll, pitch, and yaw-rate views" (L78-79).
- Magnetism / gravity / rotation link: "Experimental magnetic switching, three-winding power stages, or reinjection do not enter the ESC/motor power path during P0" (L138-140). "Reinjection is an energy-recovery hypothesis, not an assumed power source" (L140-141).
- Open / parked / not-set items: controller selection, frames, latency budgets, envelope calibration, safety review (L172-191). No universal degree limits (L81-82).
- Conflicts: none.

## Run log — EXP-2026-09-11-BUILD-DOCS   (`One_Wave_Bench/runs/EXP-2026-09-11-BUILD-DOCS/README.md`)
- Gate / lifecycle: documentation-only branch step, Attempt 1/3; Void ALLOW with constraints (L34-47); "No electrical simulation, bench test, rover drive, or drone flight was run" (L61-62).
- Upstream: base HEAD e17c68d8...; AGENTS.md; flashlight locks; "nerve/brain nodes inspected" (L17, IDs not listed). Downstream / cites: balanced base/sensor/action/brain cells, speaker, QC-RC rover/drone, status matrix (L21-23).
- Core claim: "preserve V0 as a reference rather than load-current return; preserve HOLD as no new correction, not forced zero output" (L40-41).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: all physical claims untested (L68-71).
- Conflicts: none.

## Simulator note — See it   (`One_Wave_Bench/simulators/SEE_IT.md`)
- Gate / lifecycle: prototype visual; "G-735 Micro freeze still applies: this visual is a prototype until a conserved engine drives it." (L11).
- Upstream: G-735; field_void_recursive_sim.py. Downstream: see_hold.html.
- Core claim: hex + center = nest (six pyramids flattened); orange bead "toy hold walking the two wells (`sin^2 theta`)" (L6-9).
- Equations: `sin^2 theta` (L8) (toy "E4 angle", L11).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: engines "still have no camera" (L11).
- Conflicts: none.

## Simulator note — Where it is   (`One_Wave_Bench/simulators/WHERE_IT_IS.md`)
- Gate / lifecycle: explanatory note for see_actions.html.
- Upstream / Downstream: see_actions.html.
- Core claim: "The energy is the seven amplitudes on the hex." Inward/Outward/Across/Over/Hold actions (L5). "Kilograms would be that same change, contracted with W, when you translate the whole pattern. W is not in this file. So you can experience E. You cannot experience kg yet." (L7).
- Equations: none written (mass = change contracted with W, verbal).
- Point / Path / Field role: none stated. "Over walks the dipole toward the other well" (L5).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: W (mass contraction) absent (L7).
- Conflicts: none.

## Speaker plan — Balanced Speaker P0   (`One_Wave_Bench/speaker/BALANCED_SPEAKER_P0.md`)
- Gate / lifecycle: "hypothetical design; not simulated or bench tested" (L3).
- Upstream / Downstream: none.
- Core claim: "HOLD does not force the volume to zero; it means no new volume correction while the selected gain remains registered." (L21-22).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated (three-winding geometry benefit undetermined, L50-51).
- Open / parked / not-set items: driver, output stage, VBB models, bench test (L46-56).
- Conflicts: none.

## Simulator — One-Wave Simulator master shell   (`One_Wave_Simulator/README.md`)
- Gate / lifecycle: first active engine D-413 Ground Lattice Orbital-Restoring Lab; "Yellow reduced model" (L31); stages 2-6 "visible but locked" (L16).
- Upstream: D-413. Downstream / cites: native_3d/README.md (L35).
- Core claim: stage order Ground -> circulation -> confined Vortex Phase -> Three-Vortex Knot -> electrical shell / Mirror-Gate -> translation and four-interaction Mass-Effect (L9-14). "The imposed well and collective shell do not derive gravity, quarks, protons, charge, the Mirror Gate, or Mass Effect." (L31).
- Equations: none.
- Point / Path / Field role: runnable scope lists "off-axis drop and orbit presets" (Path-like) and "state-derived torque and axial spin" plus "orbital and spin readouts" (L24-26) — axial spin is a Point-like readout; orbital is Path-like; no Field-curl role stated.
- Magnetism / gravity / rotation link: an "imposed curvature well" (L22) with orbit presets and state-derived torque/axial spin (L24-25). The file does not say whether the well starts or alters axial spin.
- Open / parked / not-set items: all stages after Ground locked until state laws, controls and failure tests exist (L16).
- Conflicts: none confirmed. Possible tension to check in code (outside slice): if the imposed curvature well (a gravity stand-in) produces "state-derived torque and axial spin" (L22-25), that would conflict with "Gravity does not start or affect point rotation". The README is ambiguous, and it labels the well non-gravity (L31).

## Branch step — Native 3D adapter   (`One_Wave_Simulator/native_3d/BRANCH_STEP.md`)
- Gate / lifecycle: Attempts 1-3; status PARTIAL / UI NOT VERIFIED pending CI (L23-25, L32); merge requires CI + independent post-review (L32).
- Upstream: AGENTS, General Reference Rules, AI canonical start, A-117, D-409, D-412, C-318, G-759, bulk and joint-response solvers, chapter coverage registry, Reality Database spec (L11). Base main 254c627d.
- Core claim: "makes existing numerical models inspectable and controllable, rather than replacing equations with decorative movement" (L5). "Do not call imposed translation force-driven motion, a cavity tensor particle kg, or a complex-field closure established quantum physics." (L17). "The key assumption rejected is that visible displacement supplies a derived force or Mass Effect law." (L36).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: next cycle (periodic drive, ±force controls, source-work ledger, norm-centroid, pinning) requires separate authorization (L38).
- Conflicts: none.

## Branch step — Controlled periodic push   (`One_Wave_Simulator/native_3d/DRIVE_BRANCH_STEP.md`)
- Gate / lifecycle: bounded experiment; final numerical review: independent physics ALLOW, code review ALLOW; live browser remains final gate (L25-35).
- Upstream: main b897fa2c; PR204. Downstream / cites: solvers/driven_bulk.py, solvers/DRIVEN_BULK_RECEIPT.md (L9, L33). Protected: bulk_excitation.py, joint_boundary_response.py (L9).
- Core claim: "No new particle identification, fitted inertia, physical kg, source-calibration or stage promotion." (L7). "a force coefficient is an external protocol input; applied force and field response are measured from actual evolving state." (L23).
- Equations: numbers only — max norm drift 1.282e-13; q-zero Hessian converges to 0.3; exploratory 0.2853 vs 0.3; spectral 0.28318 (L17, L28-29).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: side32 half-force matched response unresolved; larger grids lack timestep sweeps (L30-32).
- Conflicts: none.

## Simulator — Native 3D field lab   (`One_Wave_Simulator/native_3d/README.md`)
- Gate / lifecycle: runnable lab; later physical stages locked (L25).
- Upstream: solvers/bulk_excitation.py, solvers/joint_boundary_response.py, solvers/driven_bulk.py; D-410; C-318; G-759; BULK_EXCITATION_DERIVATION.md, JOINT_RESPONSE_DERIVATION.md (L15-17, L23-25, L43-44). Downstream: DRIVEN_BULK_RECEIPT.md, DRIVEN_HALF_STRENGTH_RECEIPT.md (L86, L93).
- Core claim: bulk is "native 3D FCC12 periodic complex field ... This is a chosen constitutive hypothesis, not established quantum particle physics." (L15). Cavity tensor "is not instantaneous bulk inertia, a free particle, or a physical mass in kg." (L17). "A narrow acceleration fit alone cannot establish Mass Effect: the four-interaction work metric must be derived and recurrence maintained." (L27). "A small response is not infinite mass." (L71-72).
- Equations: `V(x)=−Σj fj sin(K xj)/K`, K=2π/L (L45-46); `ΔW=ΔVcell Σi ni(Vnew−Vold)` (L50); applied force `Σi ΔVcell ni fj cos(K xij)` (L51); ledger `Ebulk+Eexternal−Einitial−Wswitch−Wintervention` (L52); lower-band curvature "0.3 I" (L79); ~11.12 ppm finite-force correction (L96).
- Point / Path / Field role: none stated. Lattice translations ±(1,1,0) are "not force-driven displacement" (L16).
- Magnetism / gravity / rotation link: none stated. "its time trace does not establish D-410's 24-position recurrence" (L23).
- Open / parked / not-set items: four-interaction work metric, recurrence, calibrated units (L72-73); physical displacement/velocity and geometric weave not derived (L25).
- Conflicts: none.

## Publication — The One-Wave Times   (`One_Wave_Times/README.md`)
- Gate / lifecycle: presentation documents, "not canonical proof nodes" (L3).
- Upstream: "Every issue must cite its A-G sources" (L3).
- Core claim: issues separate measurement, interpretation, hypothesis, derivation owed, falsification test (L3); satire desk; "A joke is not a proof node" (L7).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## Animator A5 — Canonical Project Data Schema   (`Tools/Chats-Animator/A5_PROJECT_DATA_SCHEMA.md`)
- Gate / lifecycle: PASS (L3).
- Core claim: one saved project object with stores project/scenes/frames/characters/characterInstances/audioTracks/audioClips (L11-17); "Frame records are the authoritative animation state." (L25).
- Equations: none. Point / Path / Field role: none stated. Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: perspective, playback, interpolation, AI, undo, audio, export deferred (L38-49).
- Conflicts: none.

## Animator A6 — Undo / History Foundations   (`Tools/Chats-Animator/A6_UNDO_HISTORY_FOUNDATIONS.md`)
- Gate / lifecycle: PASS (L3); next B1 (L47).
- Core claim: "Human and AI edits use the same transaction format." (L9); before/after edits, reverse undo, bounded history, conflict refusal (L10-16).
- Equations: none. Point / Path / Field: none stated. Magnetism / gravity / rotation: none stated.
- Open / parked: none.
- Conflicts: none.

## Animator — Canonical Architecture   (`Tools/Chats-Animator/ANIMATOR_CANONICAL_ARCHITECTURE.md`)
- Gate / lifecycle: architecture; capability states only MISSING/IMPLEMENTING/FAILING/PASSING (L263-269); 9-point qualification gate (L384-395).
- Core claim: "The reel/timeline is the canonical animation state." (L58); layers 00-10 (L31-44); "No total rebuild to fix a local failure." (L53).
- Equations: none. Point / Path / Field: none stated ("rotation" L94 is 2D layer rotation). Magnetism / gravity / rotation: none stated.
- Open / parked: none specific.
- Conflicts: none.

## Animator B10 — Project Save / Load   (`Tools/Chats-Animator/B10_PROJECT_SAVE_LOAD.md`)
- Gate / lifecycle: RUNTIME PASS (L3); hard start "B9 sprite-sheet slicer runtime PASS" (L6).
- Core claim: `.owav` JSON project; malformed files rejected before mutation (L12-18).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none.
- Open / parked: audio, camera, tween, video export excluded (L30).
- Conflicts: none with canon. Internal status note: B9 file says B9 is only STATIC PASS and "Do not start B10 until B9 gets a browser smoke-test PASS" (B9 L3, L47); B10 asserts B9 runtime PASS (L6). Record-keeping inconsistency between two docs, not a physics conflict.

## Animator B11 — Audio Track Import + Reel Sync   (`Tools/Chats-Animator/B11_AUDIO_TRACK_SYNC.md`)
- Gate / lifecycle: RUNTIME PASS (L3). Core claim: one soundtrack synced from t=0; reel duration from holds and FPS (L5).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Open: next B12. Conflicts: none.

## Animator B12 — Per-Frame Camera Pan / Zoom   (`Tools/Chats-Animator/B12_CAMERA_MOTION.md`)
- Gate / lifecycle: RUNTIME PASS (L3). Core claim: camera X, Y, zoom stored per snapshot (L5).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

## Animator B13 — WebM Video Export   (`Tools/Chats-Animator/B13_VIDEO_EXPORT.md`)
- Gate / lifecycle: RUNTIME PASS (L3). Core claim: renders snapshots to 16:9 canvas, MediaRecorder WebM, VP9 + Opus verified (L5-7).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Open: no tween/MP4 (L10). Conflicts: none.

## Animator B1 — Background Loading   (`Tools/Chats-Animator/B1_BACKGROUND_LOADING.md`)
- Gate / lifecycle: PASS (L3). Core claim: background load/replace/remove, calibration revision increments (L6-13).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

## Animator B2 — Background Calibration   (`Tools/Chats-Animator/B2_BACKGROUND_CALIBRATION.md`)
- Gate / lifecycle: PASS (L3). Core claim: horizon, near/far ground references, guide overlay, hide after calibration (L6-14).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

## Animator B3 — Character / Prop Placement   (`Tools/Chats-Animator/B3_CHARACTER_PROP_PLACEMENT.md`)
- Gate / lifecycle: PASS (L3). Core claim: "feet/base depth drives automatic size" (L42); automatic scale interpolation far-to-near (L23).
- Equations: none. Point / Path / Field: none. Magnetism / gravity / rotation: none.
- Open / parked: "Dual Mirror Gate edit mode and Lazy Human mode remain required future features" (L39).
- Conflicts: none.

## Animator B4 — Frame Reel Foundation   (`Tools/Chats-Animator/B4_FRAME_REEL_FOUNDATION.md`)
- Gate / lifecycle: PASS (L3). Core claim: ordered frames, stable IDs, snapshots, hold 1x-12x default 2x (L15-22).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Open: Dual Mirror Gate / Lazy Human mode (L41). Conflicts: none.

## Animator B5 — Pose-to-Pose Reel Editing   (`Tools/Chats-Animator/B5_POSE_TO_POSE_EDITING.md`)
- Gate / lifecycle: PASS (L3). Core claim: insert, reorder, replace PNG, copy pose (L12-17).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

## Animator B6 — Onion Skin   (`Tools/Chats-Animator/B6_ONION_SKIN.md`)
- Gate / lifecycle: PASS (L3). Core claim: previous/next ghost overlays, non-interactive (L12-16).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

## Animator B7 — Repair + Playback   (`Tools/Chats-Animator/B7_REPAIR_AND_PLAYBACK.md`)
- Gate / lifecycle: "PASS (static/syntax verified)" (L3); browser smoke test still needed (L24).
- Core claim: reconstructed app.js and b4-frame-reel.js; FPS 1-60 default 24; holds expanded in playback (L9-19).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

## Animator B8 — Batch PNG Pose Import   (`Tools/Chats-Animator/B8_BATCH_POSE_IMPORT.md`)
- Gate / lifecycle: "PASS — static/syntax verified" (L3). Core claim: multiple PNGs become consecutive frames keeping placement/depth/scale (L12-18); "first direct Lazy Human production accelerator" (L24).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

## Animator B9 — Sprite-Sheet Slicer   (`Tools/Chats-Animator/B9_SPRITE_SHEET_SLICER.md`)
- Gate / lifecycle: "STATIC PASS — syntax verified" (L3); "Do not start B10 until B9 gets a browser smoke-test PASS." (L47).
- Core claim: rows/cols 1-16, blank cells skipped, nonblank cells become frames (L23-29).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none.
- Conflicts: none with canon; see B10 internal status note.

## Animator rule — Background-Calibrated Sizing Grid   (`Tools/Chats-Animator/BACKGROUND_SIZING_GRID_RULE.md`)
- Gate / lifecycle: LOCKED (L3). Core claim: "Background first." Grid visible only while placing/sizing; never in export (L5-11).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

## Animator C14 — Reusable Motion Sequence Library   (`Tools/Chats-Animator/C14_MOTION_SEQUENCE_LIBRARY.md`)
- Gate / lifecycle: hard stop = save/reopen/insert five sequences with 24 fps exposures intact (L120).
- Core claim: `.owmotion` JSON; "The project remains a true 24 fps timeline." (L40); drawing exposures stored separately from motion translation (L42).
- Equations: none. Point / Path / Field: none. Magnetism / gravity / rotation: none.
- Conflicts: none.

## Animator C15 — Full PNG Motion Atlas   (`Tools/Chats-Animator/C15_MOTION_ATLAS_SPEC.md`)
- Gate / lifecycle: spec. Core claim: `.owatlas` package; 8-way directions; walk/run 8-pose cycles; large body/gesture/face corpus; target 40-60 sequences / 300-500 PNGs (L12-253). "The active scene remains separate from the reusable atlas." (L256).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

## Animator C1 — Deterministic Path Motion Fitter   (`Tools/Chats-Animator/C1_PATH_MOTION_FITTER.md`)
- Gate / lifecycle: RUNTIME PASS (L3). Core claim: depth/size generated from one continuous path; smoothstep easing; 0.90 -> 0.50 monotonic (L6-20).
- Equations: none written (smoothstep named). Point / Path / Field: "path" here is a 2D animation path, not the canonical Path. Magnetism / gravity / rotation: none. Conflicts: none.

## Animator C22 — Fixed-Cel Playback Acceptance   (`Tools/Chats-Animator/C22_FIXED_CEL_PLAYBACK_ACCEPTANCE.md`)
- Gate / lifecycle: acceptance + regression `node c22-fixed-cel-demo.test.js` (L34).
- Core claim: 12 frames, 12 distinct cels, fixed x/groundY/manualScale, 24 FPS, 2-frame exposure (L17-25); render_moving_layer_demo.py "historical/noncanonical" (L40-41).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

## Animator C2 — Walk Cadence   (`Tools/Chats-Animator/C2_WALK_CADENCE.md`)
- Gate / lifecycle: RUNTIME PASS (L3). Core claim: 24 FPS at 6 beats/s = 4-frame holds; test holds 4,4,4,4,4,4,12 (L5-7).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none.
- Conflicts: none with canon. Superseded in part by CHATGPT_PROJECT_STATUS L15 ("Do not treat the earlier 24 fps / 6 pose-beat shortcut as the global animation rule").

## Animator C3 — One-Click Walk Builder   (`Tools/Chats-Animator/C3_ONE_CLICK_WALK_BUILDER.md`)
- Gate / lifecycle: RUNTIME PASS (L3). Core claim: coordinates C1 + C2 (L5).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

## Animator C4 — Pose Normalizer   (`Tools/Chats-Animator/C4_POSE_NORMALIZER.md`)
- Gate / lifecycle: RUNTIME PASS (L3). Core claim: trim, rescale to square canvas, bottom-anchor; 512×512, 15 px margin (L5-7). Order: Normalize -> Path -> Cadence -> Walk -> Audio/Camera -> Export (L10).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

## Animator C5 — Forest Path Production Test   (`Tools/Chats-Animator/C5_FOREST_PATH_PRODUCTION_TEST.md`)
- Gate / lifecycle: PASS — production output (L3). Core claim: 14 stills, 72 clock frames, no optical-flow tweens (L20-23).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Open: C6 dialogue scene (L31). Conflicts: none.

## Animator — ChatGPT Project Status   (`Tools/Chats-Animator/CHATGPT_PROJECT_STATUS.md`)
- Gate / lifecycle: C14 "BUILT — C14 runtime save/open/insert gate pending" (L7).
- Upstream: B13, C1-C5, C6-C12 protected (L10). Downstream: Tools/Voice-Forge/README.md (L107).
- Core claim: "true 24 fps production timeline" authoritative (L12-13); on 1s/2s/3s exposures (L18-21); "Perspective movement must not stair-step just because a drawing is held." (L23).
- Equations: none. Point / Path / Field / Magnetism / gravity / rotation: none.
- Open / parked: C14 runtime gate (L78-86); forest acting test (L88-101).
- Conflicts: none.

## Animator — README   (`Tools/Chats-Animator/README.md`)
- Gate / lifecycle: restored animator with runtime-tested features (L3).
- Core claim: "The reel is the source of truth." (L9); "This is not a single-image tween/moving-frame shortcut." (L11); AI director must edit same structures (L64).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

## Tool — One-Wave Voice Forge   (`Tools/Voice-Forge/README.md`)
- Gate / lifecycle: Phase 1 hard stop (L86-87).
- Core claim: standalone; no canned TTS source; no unauthorized cloning of real voices (L7-9); trait-based non-destructive blend (L27, L61-62).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

## Algorythm-Zer0 — Three-Gate Correction   (`docs/ALGORYTHM-ZERO-THREE-GATE-CORRECTION.md`)
- Gate / lifecycle: "canonical correction note for Algorythm-Zer0. It does not replace the full primitive" (L3).
- Upstream: Algorythm-Zer0 primitive (not by node ID). Downstream: body/hardware mappings.
- Core claim: "3 MIRROR GATES / 6 ADDRESS / STEP SIDES / 3 MOVES / 1 SHARED CENTER / REFERENCE" (L8-11). Gate 1 Binary = threshold/significance filter (L25-41); Gate 2 Ternary = fast nerve reflex, SPEND / HOLD / CONSERVE (L62-99); Gate 3 Quadratic = "VIEWS UP / ACTIONS DOWN" body-state integration (L101-131). "BODY ENERGY MAPPING != UNIVERSAL PHYSICAL LAW" (L252).
- Equations: `energy_change = input_or_recovery + reinjection - usage` (L174), with sign interpretation (L180-187).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: domain mappings do not redefine primitive "unless separately demonstrated and adopted" (L240).
- Conflicts: none.

## Repo split — Index   (`docs/repo_split/00_INDEX.md`)
- Gate / lifecycle: destination map (L30). Core claim: 12 target documents; split/size/migration rules (L5-30).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

## Repo split 01 — Canon and Core Model   (`docs/repo_split/01_CANON_AND_CORE_MODEL.md`)
- Gate / lifecycle: stub. Core claim: shortest authoritative description; "Core six-gate / mirrored architecture" (L8).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none.
- Conflicts: none with the canonical physics rules. Terminology tension: "six-gate" (L8) versus ALGORYTHM-ZERO-THREE-GATE-CORRECTION L245 "3 MIRROR GATES != 6 GATES" and L14 "Do not convert six steps into six gates."

## Repo split 02 — Physics and Cosmology   (`docs/repo_split/02_PHYSICS_AND_COSMOLOGY.md`)
- Gate / lifecycle: stub. Core claim: home for "Gravity and displacement ideas", "Redshift / tired-light proposals", black-hole/quasar recycling, mass effect, confinement, neutrino, superfluid medium (L7-13). Label established/hypothesis/derived/simulation/unresolved (L16).
- Equations: none. Point / Path / Field: none stated.
- Magnetism / gravity / rotation link: lists gravity as a topic only.
- Conflicts: none. Redshift-as-tired-light is consistent with the no-expansion / E-528 path-loss rule; E-528 not cited.

## Repo split 03 — Math, Geometry, and Encoding   (`docs/repo_split/03_MATH_GEOMETRY_AND_ENCODING.md`)
- Gate / lifecycle: stub. Core claim: ratios, symmetries, hex/pyramid/cube/sphere, DC/AC/RC mappings, Koide geometry (L7-12).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

## Repo split 04 — Hardware and Circuits   (`docs/repo_split/04_HARDWARE_AND_CIRCUITS.md`)
- Gate / lifecycle: stub. Core claim: balanced rails, virtual ground, three-winding ternary motor, magnetic memory / hold, reinjection loops (L7-13).
- Equations / Point-Path-Field: none. Magnetism: magnetic memory / hold listed as a topic (L11). Conflicts: none.

## Repo split 05 — Virtual Breadboard and Simulation   (`docs/repo_split/05_VIRTUAL_BREADBOARD_AND_SIMULATION.md`)
- Gate / lifecycle: stub. Core claim: MNA/sparse solver, adaptive stepping, Trapezoidal/Gear, ngspice parity (L7-15).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

## Repo split 06 — Biology, Brain, and Android Architecture   (`docs/repo_split/06_BIOLOGY_BRAIN_AND_ANDROID_ARCHITECTURE.md`)
- Gate / lifecycle: stub. Core claim: cells -> nerves -> M4 -> dream -> administrator -> executor; view-up / action-down; gyro/balance (L7-13).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

## Repo split 07 — Lattice, Memory, and Miniverse   (`docs/repo_split/07_LATTICE_MEMORY_AND_MINIVERSE.md`)
- Gate / lifecycle: stub. Core claim: superfluid-crystal-lattice storage; XYZ/hex/cube/sphere/pyramid geometry; DC/AC/RC access paths; recall vs hold; "Internal-world movement and field rotation" (L7-14).
- Equations: none.
- Point / Path / Field role: "field rotation" (L13) named as a topic, undefined.
- Magnetism / gravity / rotation link: none beyond L13.
- Conflicts: none hard. Terminology risk: "field rotation" (L13) blurs the canonical separation; Field curl is neither Point rotation nor Path rotation. When this stub is filled in, it should say which of the three rates it means.

## Repo split 08 — AI Agents, Jetson, and Terminal   (`docs/repo_split/08_AI_AGENTS_JETSON_AND_TERMINAL.md`)
- Gate / lifecycle: stub. Core claim: Jetson, terminal/SSH, agents, local models (L7-14).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

## Repo split 09 — Apps, Animator, and User Tools   (`docs/repo_split/09_APPS_ANIMATOR_AND_USER_TOOLS.md`)
- Gate / lifecycle: stub. Core claim: animator requirements, installers, motion libraries (L7-12).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

## Repo split 10 — Learning System and Math Rules   (`docs/repo_split/10_LEARNING_SYSTEM_AND_MATH_RULES.md`)
- Gate / lifecycle: stub. Core claim: rule-first teaching, times-table/division recursion, algebra rules (L7-13).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

## Repo split 11 — Tests, Experiments, and Validation   (`docs/repo_split/11_TESTS_EXPERIMENTS_AND_VALIDATION.md`)
- Gate / lifecycle: stub. Core claim: "Do not turn hypotheses into conclusions here." (L17).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

## Repo split 12 — Roadmap, Status, and Collaboration   (`docs/repo_split/12_ROADMAP_STATUS_AND_COLLABORATION.md`)
- Gate / lifecycle: stub. Core claim: project-wide status, PR tracking, handoff (L7-13).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

## GRAV-LAB pointer   (`grav-lab/README.md`)
- Gate / lifecycle: pointer. Core claim: "Octave cascade sims. Not the grant cell." Original tree in GRAV-LAB repo (L3-4).
- Equations / Point-Path-Field: none. Magnetism / gravity / rotation: name implies gravity, content states none. Conflicts: none.

## HEX-SPLIT pointer   (`hex-split/README.md`)
- Gate / lifecycle: pointer. Core claim: "Geometry / 12-tone clock. Cell hex for the bench is Builds `cell-v1/`." (L3).
- Equations / Point-Path-Field / Magnetism-gravity-rotation: none. Conflicts: none.

---

## Slice summary

### (a) Nodes / chapters in this slice bearing on Point, Path, Field, rotation, magnetism, gravity, inertia, mass, resistance, lattice organization or locking
No canonical node file sits in this slice. Nodes cited by slice files:
- D-413 (Ground Lattice Orbital-Restoring Lab; One_Wave_Simulator/README.md L5): the first active engine. Triangular/hex Ground with an imposed curvature well, orbit presets, "state-derived torque and axial spin" and spin/orbital readouts (L22-26). Explicitly does not derive gravity or Mass Effect (L31).
- G-735 (Micro freeze; SEE_IT.md L11): the visual stays a prototype until a conserved engine drives it.
- A-117, D-409, D-412 (native_3d/BRANCH_STEP.md L11): references for the native 3D adapter (bulk/cavity lattice engines). Content not restated.
- D-410 (native_3d/README.md L23): 24-position recurrence. The lab's time trace does not establish it.
- C-318 (Mass Mechanism Candidate Resolution) and G-759 (Mass Effect Four Actions) (native_3d/README.md L25; BRANCH_STEP L11): mass requires a derived four-interaction work metric plus recurrence. Cavity tensor is not inertia or kg (L17). The acceleration fit alone is insufficient (L27).

Non-node slice items bearing on these topics:
- BALANCED_FLASHLIGHT_STATE_REINJECTION_LOCK: BC-DC = "point/state", TC-AC = "path/phase", QC-RC = "coordinated rotation" (L263-291). This is a hardware analogy. Magnetic coercivity is the preferred hysteresis source (L106). No 3D field claim without measured Bx/By/Bz (L293, L351).
- FLASHLIGHT_SCOPE_TERNARY_STOP / BALANCED_FLASHLIGHT_P0: rotating fields are optional. The field shape must be measured, not assumed (P0 L100).
- WHERE_IT_IS: kg = the same change contracted with W under translation of the whole pattern; W is absent (L7).
- QC_RC_ROVER_DRONE_P0: engineering attitude/rate (gyro) control only. Magnetic stages are kept out of the flight power path (L138).
- repo_split/07: "Internal-world movement and field rotation" (L13). repo_split/02: gravity/displacement and redshift/tired-light topics (L7-8).

### (b) Conflicts found
No hard contradiction of the canonical rules (C-306/C-307/C-311/C-319/C-320/G-749/G-750/G-769) was found in this slice. Soft items:
1. One_Wave_Simulator/README.md L22-25: an imposed curvature well (gravity stand-in) appears with "state-derived torque and axial spin". If the well drives axial spin, it violates "Gravity does not start or affect point rotation". The README is ambiguous and says the well does not derive gravity (L31). D-413 code needs checking, outside this slice.
2. docs/repo_split/07_LATTICE_MEMORY_AND_MINIVERSE.md L13: "field rotation" is an undefined term that risks merging Field curl with Point/Path rotation.
3. BALANCED_FLASHLIGHT_STATE_REINJECTION_LOCK.md L263-291: the point/path/rotation hardware ladder has no separate Field-curl element. If it is ever read as the canonical triad, it is incomplete.
4. docs/repo_split/01_CANON_AND_CORE_MODEL.md L8: "Core six-gate" contradicts docs/ALGORYTHM-ZERO-THREE-GATE-CORRECTION.md L14 and L245 ("3 MIRROR GATES != 6 GATES"). This is a terminology conflict, not a physics one.
5. Non-physics record inconsistency: Tools/Chats-Animator/B10_PROJECT_SAVE_LOAD.md L6 says B9 has a runtime PASS, but B9_SPRITE_SHEET_SLICER.md L3 and L47 give it STATIC PASS only and gate B10 on a browser smoke test.

### (c) Cross-references outside this slice that matter for point rotation or magnetism
- Nodes/C-318_Mass_Mechanism_Candidate_Resolution.md, Nodes/G-759_Mass_Effect_Four_Actions.md (mass/inertia).
- D-413 lab code (One_Wave_Simulator index.html / engine): verify the source of torque/axial spin relative to the imposed well.
- A-117, D-409, D-410, D-412, G-735 node files.
- solvers/BULK_EXCITATION_DERIVATION.md, solvers/JOINT_RESPONSE_DERIVATION.md, solvers/driven_bulk.py, solvers/DRIVEN_BULK_RECEIPT.md, solvers/DRIVEN_HALF_STRENGTH_RECEIPT.md (inertia-like curvature 0.3 I; not mass).
- One_Wave_Bench/simulators/field_void_recursive_sim.py, see_hold.html, see_actions.html (W contraction for kg).
- Virtual_Breadboard square-loop magnetic memory core, coupled multi-winding toroid, MTJ/TMR sensor (cited in the flashlight lock, L313-316).
