# Ledger b06 — Builds/cell-v1 (HEX_DIFFERENTIAL_BUILD … VALIDATION_PLAN)

Repo for this slice: `/home/user/Builds/cell-v1/`. 42 files, all read in full. Hardware build docs, not One-Wave-Science nodes. Only one file in the slice (`SCIENCE_AGAINST_CELL.md`) cites One-Wave node IDs. Everything else cites build files (CELL.md, CELL0.md, etc.) or external references R1–R14.

Vocabulary warning that applies to the whole slice: in these docs "FIELD"/"VOID" means the two opposed windings/toroids (one FIELD-side, one VOID-side), and "path" means a retained magnetic route in the hysteretic lattice. Neither word means the canonical Field (curl) or Path (ride/orbit). No file in the slice mentions point rotation, spin, angular momentum L, I·omega, moment of inertia, dL/dt, gamma, gravity, chi, K_L, kappa_R, parent/child frames, Moon/Mercury, expansion or redshift.

---

## HEX_DIFFERENTIAL_BUILD — wiring-level hex differential prototype   (`cell-v1/HEX_DIFFERENTIAL_BUILD.md`)
- Gate / lifecycle: build/bench plan (H0–H8); "HEX_V1 passes its first stage when…" (179-188). Nothing measured.
- Upstream: none named. Downstream / cites: CELL semantics "one-loop/one-FLIP" (190); precedents: synchro/stator, back-to-back MOSFET, rail splitter (194-196).
- Core claim: "six wound magnetic sectors; three opposed differential branches; three bidirectional center switches; one shared active midpoint reference" (8-11). "The six outer terminals are the six hex faces" (53).
- Equations: none.
- Point / Path / Field role: none stated in canonical sense. Hardware: six tapered sectors at 60° (57), opposed axes A+↔A−, B+↔B−, C+↔C− (69-72), center air gap so "cross-axis coupling measurable" (74); 6x6 coupling matrix (171); base-to-base face coupling to neighbours (151-157).
- Magnetism / gravity / rotation link: magnetic coupling between opposed sectors and neighbour faces only. Test 2 measures induced response "with gates open, then closed" (165). These are electrical MOSFET gates, not magnetic open/closed states. Gravity and rotation: none stated.
- Open / parked / not-set items: MOSFET choice depends on gate drive (113); the midpoint source/sink stage (99); mapping to CELL semantics only after pass (190).
- Conflicts: none against canonical. Internal: uses a resistor R_A0 to CENTER_BUS (33) and a 10k/10k divider for CENTER (97). PARTS.md:7 says "No designed resistors in the CELL … CENTER". Line 97 limits the divider to signal-only tests, which partly addresses this.

## HEX_LATTICE — hysteretic body-state / muscle-memory layer   (`cell-v1/HEX_LATTICE.md`)
- Gate / lifecycle: architecture proposal; 2026-09-27 stack lock (166); "Exact material and fabrication are open" (65).
- Upstream: none. Downstream / cites: V_BUS, CENTER, nucleus, reinjection.
- Core claim: "dedicated hysteretic layer laid beneath the cells … not V_BUS and … not CENTER" (3-7); carries "Br / path bias / body-state history" (26); "bias a path through the body" (57).
- Equations: none.
- Point / Path / Field role: in this file "path" is a retained magnetic route ("repeatedly used movement paths; preferred / practiced motor routes", 71-72). It is not the canonical ride. Point and Field: none stated.
- Magnetism / gravity / rotation link: remanence Br holds the path bias (120). Phase-I target behaviours include "wheel motion; propeller / rotor motion" (149-150). These are motor habits, not point rotation. Gravity: none stated.
- Open / parked / not-set items: material; nested layers (finger→hand→limb→body, 155-162) deferred; the list of measurements (120-127).
- Conflicts: none.

## HEX_SEATS — hex seats clockwise   (`cell-v1/HEX_SEATS.md`)
- Gate / lifecycle: geometry note.
- Upstream / Downstream: none.
- Core claim: "Side 0 A+ … Side 5 C-" (22-27); mirrors are opposite sides, three hops apart (49-53); "one differential per letter. Six seats, three D's" (55); "Core of axis A lives at A+ (side 0). A- (side 3) is the other end of that core" (57).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated. Line 57 implies one core per axis.
- Open / parked / not-set items: the first sketch is self-flagged as "messy" (19).
- Conflicts: none against canonical. Internal: the first sketch (8-17) labels B+ twice and uses E/F. Line 19 supersedes it.

## HYSTERESIS — CELL_V1 retained-state loop   (`cell-v1/HYSTERESIS.md`)
- Gate / lifecycle: experimental claim. "Material hysteresis is established physics. Useful CELL_V1 system hysteresis is an experimental claim" (92).
- Upstream / Downstream: V_BUS, CENTER/(0), nucleus, etched lattice; Permalloy nanostripe precedent (54).
- Core claim: "two scales of the same history-dependent process": local nucleus and "etched hysteretic lattice paths" (5-8); "The process path is the memory" (52).
- Equations: `H = N I / l_e`; `B = B(H, history)`; `Phi = B A_e`; `lambda = N Phi`; `v = d(lambda)/dt` (17-21).
- Point / Path / Field role: "path" here is an etched magnetic route that biases a later traversal (52). Point and Field: none stated.
- Magnetism / gravity / rotation link: remanence and coercivity are what make a state retained or flippable (24). Gravity and rotation: none stated.
- Open / parked / not-set items: the mapping from the seven electrical bands to magnetic loop depth is "not locked until measured" (83); film material, thickness, width, coercivity (54).
- Conflicts: none against canonical. Internal: it says the current motor nucleus is one square figure-8 and warns "Do not restore the obsolete 'three independent cores'" (103-105). HYSTERESIS_LOOP.md:16-22 has three figure-8s, one per axis.

## HYSTERESIS_LOOP — loop × ferrite per axis   (`cell-v1/HYSTERESIS_LOOP.md`)
- Gate / lifecycle: note; "We use that. We did not discover it" (14).
- Upstream / Downstream: none named.
- Core claim: "Square ferrite figure-8 … Br stays near Bm … one state, three pieces of iron" (3); "Three figure-8s (A B C). They are not three separate memories" (22).
- Equations: none. Inline: squareness Br/Bm ≥ ~0.9 (12).
- Point / Path / Field role: none stated. "The three loops are how that state can have a heading" (22).
- Magnetism / gravity / rotation link: the same current writes Br and then collapses onto V_BUS (20). Saturation is "protected habit" (28).
- Open / parked / not-set items: fade is required (28).
- Conflicts: none against canonical. Internal: one figure-8 per axis (16-22) against one nucleus per cell (MAGNETICS:140; HYSTERESIS:103-105).

## LACTATE_BUS — V_BUS and lactate analogy   (`cell-v1/LACTATE_BUS.md`)
- Gate / lifecycle: "Analogy for the proposal. Not biochemistry in the cell" (3).
- Upstream / Downstream: V_BUS, CENTER.
- Core claim: the bus has three lactate-like jobs: shuttle/reinjection, buffer, signal/send-up (13-17). "Strain is level still dropping while ask is already on" (31).
- Equations: none.
- Point / Path / Field role: none stated. Line 39 says "the field receives up and PASSes", which is FIELD in the build-semantic sense.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none stated.
- Conflicts: none.

## LATTICE_MATERIAL — under-lattice material   (`cell-v1/LATTICE_MATERIAL.md`)
- Gate / lifecycle: proposal.
- Upstream: plated-wire memory precedent (6). Downstream: figure-8 read.
- Core claim: "Copper carries current. It does not keep Br. The under lattice that remembers is a magnetic layer on that current path" (3-4).
- Equations: none.
- Point / Path / Field role: none stated. Stack: current (Cu/BeCu, "V_BUS metal") / memory (Permalloy or square ferrite) / read ("figure-8 on CENTER sees that field as a shift of home") (13-15).
- Magnetism / gravity / rotation link: graded write depth comes from Hc layers (NiFe, NiCo) (28-30).
- Open / parked / not-set items: material choice.
- Conflicts: none against canonical. Internal: it puts the memory film directly on the V_BUS copper and the read figure-8 "on CENTER" (13-15, 20). LOCK_FLOWER_STACK:29 says "Do not merge the sheet into V_BUS". SQUARE_FERRITE:19 says the nucleus "is not CENTER".

## LATTICE_STRAIN_AND_MEMORY — muscle memory, distributed intelligence, strain   (`cell-v1/LATTICE_STRAIN_AND_MEMORY.md`)
- Gate / lifecycle: architecture statement.
- Upstream: the "primary cross-mirror axis" (9). Downstream: the figure-8 read head.
- Core claim: "$$\text{Toroid (FIELD)} \iff \text{Lattice (VOID)}$$" (11). Toroid = per-cell, discrete flips. Lattice = body-level continuous potential (13-19). One metal carries memory, distributed intelligence and strain (25-36).
- Equations: the FIELD⇔VOID mapping (11); saturation where "dΦ/dB flattens" (51).
- Point / Path / Field role: it calls the per-cell toroid "FIELD" and the shared lattice "VOID". This is a terminology collision with canonical Field (curl), not a physics claim. It says nothing about point rotation or path ride.
- Magnetism / gravity / rotation link: remanent domain orientation is the memory (40). "Local decisions at cell 1 perturb the magnetic boundary condition at cell 7" (46). Gravity: none stated.
- Open / parked / not-set items: none stated.
- Conflicts: none against canonical, apart from the word "FIELD" being used for a local toroid (11-19).

## LOCK_FLOWER_STACK — flower sandwich + domain-wall muscle memory   (`cell-v1/LOCK_FLOWER_STACK.md`)
- Gate / lifecycle: "YELLOW geometry lock. Gray physics catalog" (4). Recorded 2026-09-28. "No T6 rebase from this file" (5).
- Upstream: CELL.md, CELL_ASSEMBLED.md, CELL_V1_2026-09-28_CORRECTION.md (7). Downstream: VALIDATION_PLAN.md, TRANSFLUXOR.md.
- Core claim: locked vertical stack (12-26): FIELD ring ↔ nucleus ↔ VOID ring; local gate hysteresis; loss-threshold reinjection; shared domain-wall sheet; V_BUS. Flower: "middle A+ kisses neighbor A-" (38-40). "Twelve shared sides" (43). "FIELD flip writes VOID sheet. VOID sheet biases next FIELD flip" (57).
- Equations: none.
- Point / Path / Field role: the path groove is a domain-wall route along shared edges (63). Point and Field: none stated. "A+ on a point" is banned (8, 115), but that means a hex corner, not point rotation.
- Magnetism / gravity / rotation link: walls pinned by geometry. "Too-soft film + no pin = global blob"; "Too-hard film = first habit freezes" (66-68). Not locked: "Torque" (105). Gravity: none stated.
- Open / parked / not-set items: k between rounds and nucleus; Helmholtz gap field; 3+3 winding map; permalloy thickness; Hc/Br/τ; torque; E_rec; M4 tip; "AZ0 cosmology / T6 rebase"; "Any claim that this has been measured" (100-111).
- Conflicts: none against canonical. Internal: line 17 gives M4 as "two-pyramid tip↔tip (base↔base between cells)". PARTS.md:20 and THE_CELL.md:16 give the M4 nucleus as "base-to-base".

## LOG — hardware log template   (`cell-v1/LOG.md`)
- Gate / lifecycle: "Empty log = hardware score 0%" (3). The template is unfilled.
- Upstream / Downstream: validation tests A–J (44-53); T1–T5; ring R2/R3.
- Core claim: per-session blanks for T1–T5, remanence, E_in/E_rec, and fade τ (5-40).
- Equations: none.
- Point / Path / Field role: none stated. Has a "Field/void per pair" blank (26).
- Magnetism / gravity / rotation link: "rails-off remanence matches last D sign" (13); loop type square/unknown/EMI(illegal) (14).
- Open / parked / not-set items: everything. No measured entries.
- Conflicts: none.

## MAGNETICS — CELL_V1 rebuilt magnetic layout   (`cell-v1/MAGNETICS.md`)
- Gate / lifecycle: "must agree with CELL.md" (3). "Not established" items are flagged (20).
- Upstream: R1–R8 in PROVEN_PARTS_REFERENCES.md; Rajchman & Lo 1956 (216). Downstream: VIEW_ACTION_STACK (BC–DC/TC–AC/QC–RC).
- Core claim: "one-piece square two-aperture figure-8 magnetic nucleus" (7); "two plain round toroids" as the outer/body interface (44); six tapered sectors, A+…C−, tip-to-tip inside and base-to-base between cells (59-67); "etched/patterned hysteretic path layer" (89).
- Equations: `H = N I / l_e`; `B = B(H, history)`; `Phi = B A_e`; `lambda = N Phi`; `v = d(lambda)/dt` (25-29). `B_view = Bx x_hat + By y_hat`; `|B_view|^2 = Bx^2 + By^2`; `theta = atan2(By, Bx)` (35-37). `H_net ~ (N_F I_F + N_V I_V) / l_e` and `H_net ~ (N_F I_F - N_V I_V) / l_e` (165, 170).
- Point / Path / Field role:
  - Point: none stated.
  - Path: etched hysteretic paths are the muscle-memory candidate (89-101).
  - Field: QC–RC "rotating/vector magnetic relation" (11); the rotating field comes from phase-related windings (R3) (17); measure "rotation/ellipticity/handedness" (125). This rotating field is a winding vector sum. The file attaches no L to it.
- Magnetism / gravity / rotation link: transfluxor apertures "create several closed magnetic flux paths with shared legs" (220). This is the only "closed" magnetic language, and it means flux loops, not the canonical open/closed point gradient. Gravity: none stated.
- Open / parked / not-set items: Bx/By winding placement (40); toroid winding map (51); which F/V mode means WRITE, READ, Field or Void "until measured" (175); lobe configuration (185); CELL mapping of transfluxor (243).
- Conflicts: none against canonical. Internal: it bans MTJ and IC as the decision mechanism (151). PARTS_PROPOSAL:19 and SPINTRONICS:16 mention MTJ/TMR as an endgame or read path.

## MEMORY — two figure-8s   (`cell-v1/MEMORY.md`)
- Gate / lifecycle: short note.
- Upstream / Downstream: cited by USABLE_MEMORY_BENCH:5 and PRIOR_ART:79.
- Core claim: "Round figure-8 toroid = differential / ternary side" (5). "Square figure-8 = lattice and bus side. Shared edges. Group diary" (8-9). "Cap = last kick. Not a diary" (13).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: "The core's own loop is the band" (11).
- Open / parked / not-set items: none.
- Conflicts: none against canonical. Internal: the square/round role assignment (5-9) contradicts NUCLEUS_TOROID_TYPES:34-35, MAGNETICS:140-141, SQUARE_FERRITE:3-10 and LOCK_FLOWER_STACK:14-16. Those say round = sensor nucleus, square = motor nucleus, and the lattice is a domain-wall sheet.

## METAPLASTICITY_ANALOGUE — analogue only   (`cell-v1/METAPLASTICITY_ANALOGUE.md`)
- Gate / lifecycle: "YELLOW mapping. Biology is Gray catalog" (3).
- Upstream: NOT_SOFTWARE.md, `algorithms/lean_weight.py` (5); Abraham–Bear, BCM, Benna-Fusi (20-35). Downstream: REINJECT_BUS build order (68).
- Core claim: a table mapping Gray mechanisms to analogue CELL slots, plus forbidden digital stand-ins (46-56). "Visible lean = present efficacy (Field)" (41).
- Equations: none (θ_M named).
- Point / Path / Field role: "Field" = visible lean (41), in the build-semantic sense. Path: "Reinjection revisits the path" (54). Point: none stated.
- Magnetism / gravity / rotation link: write vs erase bias is "same H, different prior B" (50). Fade by "Thermal / demag / opposite excursion" (56).
- Open / parked / not-set items: seven analogue tests (60-66).
- Conflicts: none.

## MONDAY_HARDWARE_VALIDATION_BRIEF — engineering handoff   (`cell-v1/MONDAY_HARDWARE_VALIDATION_BRIEF.md`)
- Gate / lifecycle: handoff; "No measured claim is made …" (200).
- Upstream / Downstream: V0–V8 sequence (127-152).
- Core claim: "square figure-8 nucleus sits in the coupling region of the two outer/body magnetic structures … one 3-D field problem" (41). "The novelty claim is therefore the integration" (112).
- Equations: none.
- Point / Path / Field role: none stated in canonical sense. Path = etched-path muscle memory (V7, 149). The field is treated as a 3-D coupled magnetic field to be measured (41-54).
- Magnetism / gravity / rotation link: Helmholtz gives a uniform central field, and "anti-Helmholtz excitation … creates a central zero / gradient" (44-45). The test is common vs opposed outer excitation against prior nucleus state (50-54). Gravity and rotation: none stated.
- Open / parked / not-set items: core material, CENTER impedance, clamp design, saturation model (185-192); later nuclei out of scope (196).
- Conflicts: none.

## NOT_SOFTWARE — weight system is not software   (`cell-v1/NOT_SOFTWARE.md`)
- Gate / lifecycle: principle.
- Upstream / Downstream: `algorithms/lean_weight.py` (39); Zer0 (39).
- Core claim: "The three differentials are the algorithm. In analog" (3). "Memory is that lean remaining in the path" (11).
- Equations: `DA = A+ − A−`, `DB = B+ − B−`, `DC = C+ − C−` (16-18).
- Point / Path / Field role: none stated. "Commit is local DC. The turn is AC" (21). "Lattice DC brings the consequence back through the shared hysteresis layer" (21).
- Magnetism / gravity / rotation link: "magnetic domain alignment" is the weight (9), and "magnetic state decays" (31). Gravity: none stated.
- Open / parked / not-set items: a symbol/language processor is a "separate question" (35).
- Conflicts: none.

## NO_CLOCK — event-driven, no clock   (`cell-v1/NO_CLOCK.md`)
- Gate / lifecycle: bands "locked" (22-34); bench items open (72-82).
- Upstream / Downstream: none named.
- Core claim: "No global clock … Rhythm is a consequence of thresholds" (5). Ports are bidirectional: "A+ out and A− back are one channel with opposite polarity" (13). Seven normalized bands with 5-point hysteresis gaps (26-34).
- Equations: none (band table 26-32).
- Point / Path / Field role: none stated. "Choice is flow direction": a lean to A+ makes current flow A+ → A− (58-60).
- Magnetism / gravity / rotation link: "Cross a band → fire (drive, write the core…)" (38). Gravity and rotation: none stated.
- Open / parked / not-set items: threshold drift, refractory, gate drive, HOLD return, power-up (74-80).
- Conflicts: none against canonical. Internal: it calls the seven bands "locked" (24). SEVEN.md:36-40 says the band table "stole the number". HYSTERESIS:83 says the band-to-loop mapping is "not locked until measured".

## NUCLEUS_TOROID_TYPES — nucleus and toroid types   (`cell-v1/NUCLEUS_TOROID_TYPES.md`)
- Gate / lifecycle: "Current Build-repo geometry authority for cell-role magnetic cores" (3).
- Upstream / Downstream: none named.
- Core claim: four geometry functions (7-10). Role map table (32-38): sensor = round figure-8, motor = square figure-8, M4 = double-triangle, five-mind = double pentagon, six-mind = double hexagon. All roles share two plain round toroids.
- Equations: none.
- Point / Path / Field role: the cluster-routing pyramids meet "tip-to-tip inside a cell and base-to-base between neighboring cells" (10, 72-80), and that routing "carries physical state/consequence" (82). Point and Field: none stated.
- Magnetism / gravity / rotation link: "All current core hardware is 2D / planar. The magnetic fields … are inherently 3D" (50).
- Open / parked / not-set items: no field strength, hysteresis, torque or retention claimed without measurement (61).
- Conflicts: none.

## OPTION_A_TOROID_THRESHOLD — coercivity as threshold   (`cell-v1/OPTION_A_TOROID_THRESHOLD.md`)
- Gate / lifecycle: design option (Phase-I A2).
- Upstream / Downstream: two-of-three SUM/PERMIT.
- Core claim: "The magnetic core's coercivity (H_c) is the band edge" (3). Removes the LM339, ladder resistors and 74HC (10-13). "The core is inherently self-detecting" (31).
- Equations: `MMF = N × I`; `I = V_d / R_sense`; `H_c · l_path = N · I_threshold` (23-25); `V_threshold = H_c · l_path / (N · G_sense)` (38).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: a domain flip gives a dΦ/dt pulse (21). An optional bias winding shifts effective Hc (45).
- Open / parked / not-set items: walking-third resolution (44).
- Conflicts: none against canonical. Internal: it keeps R_sense (24). It contradicts PERMIT_DRIVE/TWO_OF_THREE comparator designs, and states that it supersedes them.

## OTHER_PLASTICITIES — explored, not imported   (`cell-v1/OTHER_PLASTICITIES.md`)
- Gate / lifecycle: "Gray catalog. CELL slots are hypotheses" (3).
- Upstream: NOT_SOFTWARE, ENERGY_LEARN, HYSTERESIS, WEIGHT_LEAN, NO_CLOCK, READINESS, BUS_STATE, METAPLASTICITY_ANALOGUE, USABLE_MEMORY_BENCH, REINJECT_BUS, BREADBOARD (7-12, 48).
- Core claim: CELL slots for tag-and-capture, intrinsic, scaling, heterosynaptic, inhibitory, neuromodulator, dendritic, E/I (16-66). Order P0…P6 → flower (70).
- Equations: none.
- Point / Path / Field role: none stated. Path memory is defined as "only the core Br changed" (30).
- Magnetism / gravity / rotation link: inhibition analogue is "an opposed winding that subtracts flux" (48).
- Open / parked / not-set items: second species; lactate (54, 71).
- Conflicts: none against canonical. Internal: "P6 on shared square figure-8" (20) treats the square figure-8 as a shared body core (as in MEMORY.md), against the square = motor nucleus geometry lock.

## PARTS — current prototype parts map   (`cell-v1/PARTS.md`)
- Gate / lifecycle: "prototype / validation BOM" (3).
- Upstream / Downstream: R7/R9 power topology.
- Core claim: constraints (7-21): no designed resistors in control/threshold/CENTER/reinjection; no LM339, no op-amp, no clock; motor nucleus = square figure-8; "M4 nucleus = two triangular/pyramidal toroidal loops base-to-base" (20). Three half-bridges, six MOSFETs (96-116). "Three mirror gates = one complete loop = one FLIP" (148).
- Equations: none.
- Point / Path / Field role: "Their magnetic vector sum is the proven physical precedent for a rotating field" (118). Memory has three scales (156-159). Point: none stated.
- Magnetism / gravity / rotation link: rotating field from the A/B/C phases (118), with no L attached. Gravity: none stated.
- Open / parked / not-set items: MOSFET part, toroid material, turns, recovery path (27-33); the ≤1 V gate translation (152).
- Conflicts: none against canonical. Internal: the M4 base-to-base description conflicts with LOCK_FLOWER_STACK:17 (tip↔tip). Its resistor and comparator ban (7-11, 64-66) conflicts with PERMIT_DRIVE:37-40, TWO_OF_THREE:34-40 and HEX_DIFFERENTIAL_BUILD:33, 97.

## PARTS_PROPOSAL — parts and cousins   (`cell-v1/PARTS_PROPOSAL.md`)
- Gate / lifecycle: proposal; NSF-shaped risk statement (55).
- Upstream: Magnetics Inc catalog; ARCHITECTURE.md (41). Neighbours: DYNAP-SE2, Blumind, EB-MTJ (45-47).
- Core claim: "memory element is a square-loop tape core on CENTER" (17). Bidirectional port via transmission gate or an analog mux (PSMUX1247) (27-28).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: Orthonol/Permalloy 80/Supermalloy squareness sets write depth (11-13).
- Open / parked / not-set items: foundry/MPW later (37).
- Conflicts: none against canonical. Internal: "square-loop tape core on CENTER" (17) contradicts SQUARE_FERRITE:19 ("not CENTER") and STACK:9 ("CENTER … Not a core"). The MTJ "IC endgame" (19) and analog-mux IC (28) contradict MAGNETICS:151 and PARTS:77 (no IC switch).

## PERMIT_DRIVE — PERMIT to metal   (`cell-v1/PERMIT_DRIVE.md`)
- Gate / lifecycle: proposal.
- Upstream / Downstream: TWO_OF_THREE SUM; half-bridge actions.
- Core claim: trip rises at |SUM| > 1.5 and releases at < 1.2 (9-10). The action table PASS/PULL/PUSH/FLIP gives high- and low-side states (26-31).
- Equations: thresholds 1.5 / 1.2 units of Iss (9-10).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: parts (37-43).
- Conflicts: none against canonical. Internal: it specifies an LM339, TS5A/4066 analog switches, and resistors for the trip and SUM (37-40). PARTS.md:7-11 and 64-66, STACK.md:17 and MEMORY.md:11 ban these.

## PHYSICAL_NET — physical analog network   (`cell-v1/PHYSICAL_NET.md`)
- Gate / lifecycle: "proposal law, not a filled log" (61).
- Upstream / Downstream: none named.
- Core claim: "Reinjection is a current that has to land somewhere" (3). "Bus is a reservoir … No address" (28). "Reinjection is only real when a second axis then draws that charge" (55).
- Equations: `E_in = ∫ V I dt during drive`; `E_rec = ½ C (V_after² − V_before²)`; `E_loss = E_in − E_rec − E_useful` (64-66).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: "Magnetic H is still the core, not these caps" (22).
- Open / parked / not-set items: C_steer/C_BUS start values (19-20).
- Conflicts: none.

## PRIOR_ART_AND_TEST_TARGETS — comparison map   (`cell-v1/PRIOR_ART_AND_TEST_TARGETS.md`)
- Gate / lifecycle: "comparison map, not canon" (3).
- Upstream: transfluxors; magnetic majority; Abraham-Bear; Benna-Fusi; Frey-Morris; OTHER_PLASTICITIES.md; MEMORY.md (79). Downstream: Tests A–J.
- Core claim: nine mechanism classes, each with "Falsify" criteria (9-110). Zer0 is described as "(0)t → event → consequence → resolve → (0)t+1" (55).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: "magnetic majority, current-summing thresholds" (27); six-sector multiphase stator (47).
- Open / parked / not-set items: the research list (116).
- Conflicts: none against canonical. Internal: "square-figure-8 body diary" (79) and "two seats on one square figure-8" (91) follow MEMORY.md's role, against the geometry lock.

## PROVEN_PARTS_REFERENCES — evidence / reference map R1–R14   (`cell-v1/PROVEN_PARTS_REFERENCES.md`)
- Gate / lifecycle: "references established mechanisms, not proof" (3); hard rule (70).
- Upstream: R1 resolver (ADI), R2 synchro, R3 rotating field (ADALM1000), R4 TDK ferrite, R5/R6 Sci Rep permalloy nanowires, R7 Infineon, R8 Infineon braking, R9 TI half-bridges, R10 onsemi, R11 Rajchman–Lo, R12 US3376427A, R13 US3328785A, R14 historical.
- Core claim: an evidence table pairing each CELL block with a precedent and the CELL-specific claim still to prove (55-66, 113-118).
- Equations: none.
- Point / Path / Field role: none stated. R3 says "phase-related stator fields vector-sum into a continuously rotating magnetic field" (21). R12 says "at least two closed magnetic paths with portions in common" (100).
- Magnetism / gravity / rotation link: rotating field by vector sum only. No L, and no gravity.
- Open / parked / not-set items: the nucleus material (27).
- Conflicts: none.

## READINESS — readiness, not a soul   (`cell-v1/READINESS.md`)
- Gate / lifecycle: grant language.
- Upstream / Downstream: none.
- Core claim: "Bus low. Tail current down. Return sluggish. Thresholds harder to cross" (5). "Readiness — build it, measure it. Experience — leave it alone" (38-39).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: subjective experience is "open" (34).
- Conflicts: none.

## README — cell-v1 index   (`cell-v1/README.md`)
- Gate / lifecycle: index. "CELL.md is the lock" (3).
- Downstream / cites: MONDAY_HARDWARE_VALIDATION_BRIEF.md, PARTS.md, REFERENCE.md, VIEW_ACTION_STACK.md (7-14).
- Core claim: BC–DC → TC–AC → QC–RC stack; four views up (Direction/Phase/Strength/Reference); four actions down (Inward/Outward/Across/Over) (14).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none against canonical. Internal: SCIENCE_AGAINST_CELL:3 names `CELL_CURRENT.md` and `LOCK.md` as "the cell", while this file names CELL.md.

## REFERENCE — electrical/state references, 2026-09-27 lock   (`cell-v1/REFERENCE.md`)
- Gate / lifecycle: "supersedes older fixed-CENTER wording" (3).
- Upstream: CELL.md (40).
- Core claim: "CENTER is the current combined full-body-state balance relation" (7). V_BUS is the energy reservoir and "not long-term muscle memory" (23). Three hysteresis scales: gate-local, nucleus, shared under-cell (30-32). Hard rule: `live body-state CENTER != V_BUS != role-specific nucleus` (45).
- Equations: none (the inequality rule at 45-46).
- Point / Path / Field role: none stated. The shared layer is "body/path/muscle memory" (32).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: how CENTER is distributed to all three axes is "OPEN / BENCH" (14).
- Conflicts: none against canonical. Internal: it supersedes the fixed CENTER in HEX_DIFFERENTIAL_BUILD:97 (2.5 V) and TOP_RAIL:27 (divider from V_TOP).

## REINJECT_BUS — reinjection bus   (`cell-v1/REINJECT_BUS.md`)
- Gate / lifecycle: architecture plus hypothesis list (124-131). Locks dated 2026-09-27 (167) and 2026-10-02 (177).
- Upstream: DC_AC_RC.md (18), CELL0.md (162). Downstream: METAPLASTICITY build order.
- Core claim: "Lattice DC is the brain reinjection loop" (179). "Recoverable inductive energy is steered toward V_BUS" (53). "If you recover 40%, say 40%. Never 100%" (76).
- Equations: `E = ½ C V²` (64); `E_in = ∫ V(t)·I(t) dt`; `E_L = ½ L I²`; `E_rec = ½ C (V_final² − V_initial²)`; `E_loss = E_in − E_rec − E_useful` (71-74).
- Point / Path / Field role: the path is the shared hysteresis trace that the return "revisits" (49, 88). Build step 6 is "Sequence A→B→C. Field rotates. Recovery during rotation" (154), a winding-driven rotating field with no L attached. Point: none stated.
- Magnetism / gravity / rotation link: "Winding — field stores the event" (45). Saturation needs fade (143). Gravity: none stated.
- Open / parked / not-set items: hypotheses (126-131); lower-loss route settling is not a measured claim (175).
- Conflicts: none against canonical. "CELL_V1 does not assume energy creation" (77) is consistent with conservation.

## SCIENCE_AGAINST_CELL — science vs cell, 2026-10-04   (`cell-v1/SCIENCE_AGAINST_CELL.md`)
- Gate / lifecycle: cross-check. "Green means internally defined. Yellow means the math is constrained. Neither is a bench result" (5). "No node here is Bronze or above" (23).
- Upstream: `One-Wave-Science/00_MASTER_INDEX.md` (5); CELL_CURRENT.md, LOCK.md (3).
- Downstream / cites (node IDs): A-101, A-103, A-104, A-109, B-205, B-206b, D-408, D-411, C-319, C-320, C-311.
- Core claim:
  - "A-101 Ground / Zero. A reference is required … The cell's CENTER is that reference" (9).
  - "A-103 Differential" is tip to tip, plus against minus (10).
  - "A-104 Gradient … C, the magnetic gradient, is this job and no other" (11).
  - "A-109 Inertial memory. Prior state persists through the next update" (12).
  - "B-205 Mirror" (13).
  - "B-206b Four views" are readouts (14).
  - "D-408 Sixfold lattice" is the flower (15).
  - "D-411 Mirrored axis pairs. N pairs give 2N directed routes" (16).
  - "C-319 / C-320. Magnetism reorganizes which lattice paths are open. It does not become the scalar field, and it does not specify a square nucleus" (17).
  - "C-311 says electric and magnetic are two projections of one pressure" (24).
- Equations: none.
- Point / Path / Field role: the only file that touches canonical nodes.
  - Path: D-411 routes; C-319/C-320 "which lattice paths are open".
  - Field: A-104 gradient.
  - Point: none stated. A-109 "inertial memory" is about state persistence. It says nothing about moment of inertia or L.
- Magnetism / gravity / rotation link: magnetism "does not become the scalar field" (17), which is consistent with the canonical rule "Magnetism does not become gravity". Magnetic open is restated as opening lattice paths (17). Gravity and point rotation: none stated.
- Open / parked / not-set items: the science "cannot certify the hardware" (28).
- Conflicts:
  - SCIENCE_AGAINST_CELL.md:17 paraphrases C-319/C-320 as "Magnetism reorganizes which lattice paths are open". The canonical rule says magnetism opens the **point** (open magnetic gradient: dL/dt = 0; closed: dL/dt = −γL). The file moves "open" from the point to lattice paths and leaves out the dL/dt split. This divergence should be checked against C-319/C-320 directly.
  - SCIENCE_AGAINST_CELL.md:11 assigns the A-104 gradient to "the magnetic gradient" (sensor C) "and no other". This is a cell assignment, and the file itself says so at line 21. It is a soft issue only.

## SEVEN — seven is the two systems combined   (`cell-v1/SEVEN.md`)
- Gate / lifecycle: reinterpretation.
- Upstream: CELL.md (36).
- Core claim: "The two systems are FIELD and VOID … Seven is what those two systems are when they are combined" (5-7). Interface count is 3 + 3 + 1 (CENTER). Flower count is 6 + 1 (13-28).
- Equations: none (count table 44-51).
- Point / Path / Field role: FIELD/VOID are the two plain round body toroids (5), in the build sense. Point and Path: none stated.
- Magnetism / gravity / rotation link: "Helmholtz is weather over it, not the seventh seat" (53).
- Open / parked / not-set items: none.
- Conflicts: none against canonical. Internal: it demotes the seven-band scale (36-40), which NO_CLOCK:24 and TWO_OF_THREE:5 call "locked".

## SOURCES — full cell packet sources   (`cell-v1/SOURCES.md`)
- Gate / lifecycle: pointer list. "They are not Science-grant claims" (3).
- Downstream / cites: One-Wave-Science `CELL_V1_BUILD_PACKET.md`, `CELL_V1_BRAIN_CELL_PARTS.md`, `CELL_V1_REAL_HARDWARE_PAMPHLET.md`, `CELL_V1_BOARD_1_BASELINE_TEST_HARNESS.md`, `CELL_V1_ANTI_DRIFT.md` (7-11); CELL0.md, LOG.md (13).
- Core claim, Equations, Point/Path/Field, Magnetism link: none.
- Open / parked / not-set items: none.
- Conflicts: none against canonical. Note: SCIENCE_AGAINST_CELL:5 says these pamphlets "are being removed from" Science, so these URLs may go stale.

## SPINTRONICS — spintronics = actions down   (`cell-v1/SPINTRONICS.md`)
- Gate / lifecycle: mapping, now and later.
- Upstream / Downstream: PERMIT, two-of-three.
- Core claim: "Charge current in the under lattice already is the write. Spintronics is how that current torques the magnetic layer" (5). Action map: PUSH grows Br, PULL backs toward a minor loop, FLIP beats Hc, PASS has no write and regens to V_BUS (11-14).
- Equations: `H = NI/ℓ` (20).
- Point / Path / Field role: none stated in canonical sense. Spin torque on magnetization (STT/SOT) is a material write mechanism, not point rotation.
- Magnetism / gravity / rotation link: "Lattice current → spin current → torque on Br" (22). Gravity: none stated.
- Open / parked / not-set items: heavy-metal understrip (Ta/W/Pt) later (22).
- Conflicts: none against canonical. Internal: "later TMR reads Br" (16) sits close to the MAGNETICS:151 MTJ ban, but it is a read path only and line 24 forbids an MTJ crossbar.

## SQUARE_FERRITE — square figure-8 motor-control nucleus   (`cell-v1/SQUARE_FERRITE.md`)
- Gate / lifecycle: role lock.
- Core claim: "square figure-8 toroidal structure is the motor-control-cell nucleus" (3). "It is not the universal CELL_V1 nucleus" (5). "it is not CENTER; it is not V_BUS" (19-20).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: "planar / 2D. Its magnetic field is 3D" (26).
- Open / parked / not-set items: none.
- Conflicts: none against canonical. Internal: it contradicts MEMORY.md, STACK.md and PARTS_PROPOSAL.md (see slice summary).

## STACK — one hex top to bottom   (`cell-v1/STACK.md`)
- Gate / lifecycle: note.
- Core claim: V_TOP / three diffs / "round figure-8 toroid ← differential side" / CENTER / "square figure-8 ← lattice + bus side" / V_BUS / PACK (6-12). "Same collapse current writes the square on the way back to the bus" (15). "No comparators anywhere" (17).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: collapse current writes the square core (15).
- Open / parked / not-set items: plating (19).
- Conflicts: none against canonical. Internal: the round/square role assignment (8-15) contradicts NUCLEUS_TOROID_TYPES:34-35 and LOCK_FLOWER_STACK:14-16.

## STATE_AND_ACTION — state and action   (`cell-v1/STATE_AND_ACTION.md`)
- Gate / lifecycle: note.
- Core claim: "Memory is domain history in that axis figure-8" (7). "Two-of-three + PERMIT is commutation" (13). "Iron holds Br / Bus carries collapse / Phases sense and throw" (22-24).
- Equations: none.
- Point / Path / Field role: none stated. Line 9 says the cell "has one heading". That is a magnetic state direction, not an attitude or spin.
- Magnetism / gravity / rotation link: commutation as coherence rule (26).
- Open / parked / not-set items: none.
- Conflicts: none against canonical. Internal: it has one figure-8 per axis (7), as in HYSTERESIS_LOOP, against the one-nucleus-per-cell lock.

## THE_CELL — the cell   (`cell-v1/THE_CELL.md`)
- Gate / lifecycle: "detail under CELL.md; if wording conflicts, CELL.md wins" (70).
- Core claim: "one coupled physical state machine with a universal outer/body differential pair and a role-specific nucleus" (3). M4 nucleus = "two triangular toroidal loops base-to-base" (16).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: "planar / 2D. The magnetic fields are 3D" (22).
- Open / parked / not-set items: none.
- Conflicts: none against canonical. Internal: M4 base-to-base (16) against LOCK_FLOWER_STACK:17.

## TOP_RAIL — top rail   (`cell-v1/TOP_RAIL.md`)
- Gate / lifecycle: "Both faces have power. That is locked" (3). V_TOP generation is a proposal (15).
- Core claim: "Three names. Three nodes": V_TOP, V_BUS, CENTER (5-9). CENTER is a "divider from V_TOP, then allowed to move a little" (27).
- Equations: none.
- Point / Path / Field role, Magnetism link: none stated.
- Open / parked / not-set items: V_TOP voltage, 9/5/3.3 V (34).
- Conflicts: none against canonical. Internal: CENTER as a divider (27) is against the PARTS.md:7 resistor ban and the REFERENCE.md:7 live-balance definition.

## TRANSFLUXOR — mechanism (Gray prior art)   (`cell-v1/TRANSFLUXOR.md`)
- Gate / lifecycle: "comparison class … does not prove CELL_V1" (5). Bench tests 1–5 earn the name (57-65).
- Upstream: Rajchman & Lo 1956 (3).
- Core claim: two apertures give three legs (11-15). Block/reset vs set/unblock; NDRO (21-29). "Path length is the decoder" (37).
- Equations: `I = Hc·l / n` (37).
- Point / Path / Field role: "path" here is magnetic flux path length (long vs short), not the canonical ride. Point and Field: none stated.
- Magnetism / gravity / rotation link: blocked vs unblocked is a closed-flux gating state. In the "Blocked" state flux cannot change in an already-saturated leg (21-23). In the "Unblocked" state flux can "slosh" (27). This is the nearest build analogue to a magnetic "closed/open" gate, but the file ties it to no point or L. Gravity: none stated.
- Open / parked / not-set items: whether the square figure-8 is a transfluxor at all (51, 65).
- Conflicts: none against canonical. The mismatch list (48-53) is self-reported.

## TWO_OF_THREE — current-sum block   (`cell-v1/TWO_OF_THREE.md`)
- Gate / lifecycle: "Identity of the flower. Analog. No MCU" (3).
- Core claim: one unit = Iss, threshold 1.5 units (7). A sum table gives HOLD or permit (9-16). "Walking third is not inside the sum. Separate inhibit" (18).
- Equations: `SUM voltage = k × (N_plus − N_minus)` (34).
- Point / Path / Field role, Magnetism link: none stated.
- Open / parked / not-set items: parts family (24-40).
- Conflicts: none against canonical. Internal: "locked seven-band" (5) against SEVEN.md. It also specifies comparators ("jellybean op-amp or LM339-class") and a "resistor to CENTER" (34, 40), which PARTS.md:7-11 and STACK:17 ban.

## USABLE_MEMORY_BENCH — memory / meta / cascade bench recipes   (`cell-v1/USABLE_MEMORY_BENCH.md`)
- Gate / lifecycle: "YELLOW bench recipes" (3).
- Upstream: BREADBOARD.md, WEIGHT_LEAN.md, NO_CLOCK.md, REINJECT_BUS.md, METAPLASTICITY_ANALOGUE.md, MEMORY.md (5).
- Core claim: P0 two-lean through P7 bounded moving reference (11-61). The receipt line requires "no processor in the write path" (70).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: P6 uses "Flux + remanence + shared core only" (57).
- Open / parked / not-set items: flower-scale tag, inhibitory species, lactate, intrinsic (75).
- Conflicts: none against canonical. Internal: it repeats MEMORY.md's "square figure-8 = body diary" (5) while also using the square figure-8 as the motor-control nucleus (9).

## VALIDATION_PLAN — Phase-I validation plan   (`cell-v1/VALIDATION_PLAN.md`)
- Gate / lifecycle: executable plan for MASTER_CURRENT_STATE.md (3).
- Upstream: USABLE_MEMORY_BENCH, OTHER_PLASTICITIES, METAPLASTICITY_ANALOGUE, NOT_SOFTWARE (5-7).
- Core claim: core Tests A–E, then memory extensions F–J (19-33). "A successful test validates only the premise that test was designed to measure" (11).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: Test B requires no "monotonic drift into saturation" (59). Test E covers six-sector coupling (85-93).
- Open / parked / not-set items: flower, M4, five-mind, six-mind and "full Algorythm-Zer0 runtime" are not validated (148). Current, pulse width and turns are not locked (154).
- Conflicts: none.

---

## Slice summary

### (a) Nodes and chapters in this slice that bear on Point, Path, Field, rotation, magnetism, gravity, inertia, mass, resistance, lattice organization or locking

**One-Wave node IDs cited in the whole slice.** All of them are in SCIENCE_AGAINST_CELL.md, and the file says none is "Bronze or above":
- A-101 Ground/Zero: CENTER is the reference (9).
- A-103 Differential: tip-to-tip, plus against minus (10).
- A-104 Gradient: assigned to the cell's magnetic-gradient lean C (11).
- A-109 Inertial memory: prior state persists through the update (12). This is about memory, not moment of inertia.
- B-205 Mirror: the opposite face reverses sign (13).
- B-206b Four views: readouts, not gates (14).
- D-408 Sixfold lattice: the flower, one center and six neighbours (15).
- D-411 Mirrored axis pairs: three pairs give six directed routes (16).
- C-319 / C-320: "Magnetism reorganizes which lattice paths are open"; does not become the scalar field; does not specify a square nucleus (17).
- C-311: E and B are two projections of one pressure (24).
- 00_MASTER_INDEX.md: gate source (5).

**How the build hardware implements Point / Path / Field.** It does not implement them in the canonical sense.
- **Point:** no file implements or mentions point rotation, spin, L = Iω, attitude or inertia axes. The nearest hardware objects are CENTER/(0) as the "lean home" reference (REFERENCE:7) and the role-specific nucleus. "A+ on a point" is banned, but that means a hex corner (LOCK_FLOWER_STACK:8, 115).
- **Path:** implemented as retained magnetic routes. These are the etched/patterned Permalloy domain-wall lattice under the cells (HEX_LATTICE, HYSTERESIS:50-59, MAGNETICS:87-101, LOCK_FLOWER_STACK:43-63, LATTICE_MATERIAL), routing pyramids tip-to-tip and base-to-base (NUCLEUS_TOROID_TYPES:72-80), and transfluxor flux-path length (TRANSFLUXOR:37). This is route memory and flux path. It is not the canonical orbital ride, and no file says it carries or lacks L.
- **Field:** used two ways.
  1. FIELD/VOID as the two opposed windings or round toroids, and as the "Toroid (FIELD) ⇔ Lattice (VOID)" mapping (LATTICE_STRAIN_AND_MEMORY:11; SEVEN:5; MAGNETICS:154-175; LOCK_FLOWER_STACK:19, 57).
  2. A physical rotating magnetic field from the A/B/C winding vector sum, the QC–RC layer (MAGNETICS:11, 125; PARTS:118; PROVEN_PARTS R3:21; REINJECT_BUS:154 "Field rotates").
  - No curl, wake or compression-gradient language appears, except the anti-Helmholtz "central zero / gradient" (MONDAY:45) and A-104 (SCIENCE:11).

**Magnetic open / closed in the build hardware.**
- There is no dL/dt = 0 or −γL anywhere.
- "Closed" appears only as closed magnetic flux loops in multi-aperture cores (MAGNETICS:220; PROVEN_PARTS R12:100).
- The nearest gate analogue is transfluxor blocked (no flux change possible) vs unblocked (flux sloshes) (TRANSFLUXOR:21-29).
- MOSFET gates are "open, then closed" (HEX_DIFFERENTIAL_BUILD:165), but these are electrical.
- The only canonical-node statement is SCIENCE_AGAINST_CELL:17 (C-319/C-320 opens lattice paths).

**Gravity:** none stated in any of the 42 files.

**Mass / resistance-as-mass/organization:** none stated. Resistance appears only as electrical resistance (DC resistance, RDS(on), R_sense).

**Lattice organization / locking:**
- One shared domain-wall sheet under the seven-cell flower makes up the distributed intelligence (LOCK_FLOWER_STACK:43-47; LATTICE_STRAIN_AND_MEMORY:44-47).
- "Two cells couple when their crossings line up" (NO_CLOCK:70). This is the closest analogue to rate locking. It is about threshold crossing rate, not point rotation rate.
- Bound-lattice 1:1 / 3:2 locking: none stated.

### (b) Conflicts found

**Against the canonical rules:**
1. SCIENCE_AGAINST_CELL.md:17 paraphrases C-319/C-320 as "Magnetism reorganizes which lattice paths are open". The canonical rule is that magnetism opens the **point** (open: dL/dt = 0; closed: dL/dt = −γL). The file moves "open" onto paths and leaves out the L bookkeeping. Verify against the C-319/C-320 source.
2. Terminology collision, not physics: LATTICE_STRAIN_AND_MEMORY.md:11-19, SEVEN.md:5 and MAGNETICS.md:154-175 use "FIELD" for a per-cell toroid or winding. Canonical Field is curl, which is neither point nor path. Readers could conflate the two.
3. Soft: SCIENCE_AGAINST_CELL.md:11 says A-104 gradient is the magnetic-gradient lean "and no other". This is a cell assignment, and the file admits as much at line 21.
4. No file contradicts these canonical rules: no gravity or expansion claims, no L exception, no magnetism-to-gravity claim. SCIENCE:17 explicitly says magnetism "does not become the scalar field".

**Internal Builds contradictions** (recorded because they affect which magnetic element does what):
- **Square vs round figure-8 role.**
  - MEMORY.md:5-9, STACK.md:8-15, OTHER_PLASTICITIES.md:20, PRIOR_ART_AND_TEST_TARGETS.md:79, 91 and USABLE_MEMORY_BENCH.md:5 say: square = lattice/bus/body diary, round = differential side.
  - NUCLEUS_TOROID_TYPES.md:34-35, MAGNETICS.md:140-141, SQUARE_FERRITE.md:3-10 and LOCK_FLOWER_STACK.md:14-16 say: square = motor nucleus, round = sensor nucleus, and the lattice is a separate domain-wall sheet.
- **One core per axis vs one nucleus per cell.** HYSTERESIS_LOOP.md:16-22, STATE_AND_ACTION.md:7 and HEX_SEATS.md:57 have one core per axis. HYSTERESIS.md:103-105 and MAGNETICS.md:140 have one nucleus per cell.
- **M4 orientation.** LOCK_FLOWER_STACK.md:17 says tip↔tip. PARTS.md:20 and THE_CELL.md:16 say base-to-base.
- **Comparators, resistors and ICs.** PERMIT_DRIVE.md:37-40 and TWO_OF_THREE.md:34-40 (LM339, analog-switch ICs, resistors), HEX_DIFFERENTIAL_BUILD.md:33, 97 (R_A0, 10k divider) and TOP_RAIL.md:27 (CENTER divider) all use parts that PARTS.md:7-11, 64-66, STACK.md:17 and MEMORY.md:11 ban. OPTION_A_TOROID_THRESHOLD.md removes the comparators.
- **Memory core on CENTER.** PARTS_PROPOSAL.md:17 says "square-loop tape core on CENTER". SQUARE_FERRITE.md:19 and STACK.md:9 say no core on CENTER. LATTICE_MATERIAL.md:15, 20 puts a "figure-8 on CENTER" read and sits the memory film on V_BUS copper (13), against LOCK_FLOWER_STACK.md:29.
- **MTJ and IC parts.** PARTS_PROPOSAL.md:19, 28 and SPINTRONICS.md:16 mention MTJ/TMR and mux ICs. MAGNETICS.md:151 and PARTS.md:77 exclude them.
- **Seven-band scale.** NO_CLOCK.md:24 and TWO_OF_THREE.md:5 call it "locked". SEVEN.md:36-40 demotes it. HYSTERESIS.md:83 says the mapping is not locked.
- **Fixed CENTER.** HEX_DIFFERENTIAL_BUILD.md:97 (2.5 V) and TOP_RAIL.md:27 use a fixed CENTER. REFERENCE.md:3-14 defines a live body-state CENTER and supersedes them.
- **Which file is the lock.** README.md:3 names CELL.md. SCIENCE_AGAINST_CELL.md:3 names CELL_CURRENT.md and LOCK.md.

### (c) Cross-references outside this slice that matter for point rotation or magnetism
- One-Wave-Science nodes: C-319, C-320, C-311, A-104, A-109, D-408, D-411, A-101, A-103, B-205, B-206b, and `00_MASTER_INDEX.md` (all from SCIENCE_AGAINST_CELL.md).
- Build files outside the slice:
  - CELL.md, CELL_ASSEMBLED.md, CELL_V1_2026-09-28_CORRECTION.md, CELL_CURRENT.md, LOCK.md, CELL0.md
  - VIEW_ACTION_STACK.md (QC–RC rotating field), DC_AC_RC.md
  - BREADBOARD.md, WEIGHT_LEAN.md, ENERGY_LEARN.md, BUS_STATE.md, ARCHITECTURE.md, MASTER_CURRENT_STATE.md
  - `algorithms/lean_weight.py`
- One-Wave-Science hardware pamphlets (SOURCES.md:7-11): CELL_V1_BUILD_PACKET.md, CELL_V1_BRAIN_CELL_PARTS.md, CELL_V1_REAL_HARDWARE_PAMPHLET.md, CELL_V1_BOARD_1_BASELINE_TEST_HARNESS.md, CELL_V1_ANTI_DRIFT.md.
- External magnetic precedents: R1–R14 (resolver, synchro, rotating field, ferrite B-H, permalloy domain-wall pinning, transfluxor patents).
- "AZ0 cosmology / T6 rebase" and "Algorythm-Zer0 runtime" are explicitly parked (LOCK_FLOWER_STACK:110; VALIDATION_PLAN:148).
