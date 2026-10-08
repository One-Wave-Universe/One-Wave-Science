# Ledger b04 — Builds/Virtual_Breadboard (19 files)

Repo for this slice: `/home/user/Builds/Virtual_Breadboard` (Builds repo, not One-Wave-Science). All 19 files read in full (2996 lines total). No files edited.

Scope note for every entry below: these are hardware / simulator build documents. They do not define Point / Path / Field as separate rotational rates and do not use the canonical magnetic open/closed (dL/dt = 0 vs dL/dt = -gamma L) language. Where a file uses words like "spin", "rotating B", "Field", "hold", "reinject", "closed" or "L", the meaning is recorded literally, so naming collisions with canon are visible. The only node ID cited anywhere in the slice is **G-744** (README.md:570,573). A grep for `[A-Z]-[0-9]+` over all 19 files found nothing else; the only other hits were TO-92 package names.

---

## AI_COLLABORATION — Virtual Breadboard AI Collaboration Contract   (`AI_COLLABORATION.md`)
- Gate / lifecycle: process contract. Applies to "any AI or human joining Virtual Breadboard work" (:3). Merge-agreement gate (:149-174).
- Upstream: `00_RULES/architecture.md`, `03_ELECTRICAL_CORE/MAP.md`, `SPICE_PARITY.md`, `SOLVER_CONVERGENCE.md`, `11_INTERFACE/MAP.md`, `js/circuit.js`, `js/app.js`, `js/ai.js`, `AI_CONSTRUCTION_LOG.md`, `.github/workflows/breadboard-flashlight-tests.yml` (:42-51). Downstream: `proposals/` (:182), every contributing branch.
- Core claim: "The simulator must remain reality-first ... must either pass measurement or report failure honestly" (:7). "The UI owns no physics. AI owns no physics. A virtual-device program owns no physics" (:224).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: lists "magnetic ... experiments" as a lab capability (:15). Nothing else stated.
- Open / parked / not-set items: desktop acceptance, ARM64/Jetson packaging, virtual-device schema and runtime, device-program interpreter, multi-device scheduler (:57-67, :274-285).
- Conflicts: none.

## AI_CONSTRUCTION_LOG — Miniverse / Mega City AI Construction Log   (`AI_CONSTRUCTION_LOG.md`)
- Gate / lifecycle: signed ledger. Entries: GPT-5.6 Sol (DO NOT MERGE YET, :59-76), Claude Sonnet 5 (AGREE TO MERGE, :99-116), Codex (docs only, :119-128), Grok (AGREE TO MERGE, :130-147).
- Upstream: AI_COLLABORATION.md. Downstream / cites: PR #78, #79, #51; `07_MAGNETICS/SOLVERS.md` (:139); `Virtual_3D_Electronics/js/circuit.js`, `js/magnetics.js`, `js/parts.js` (:143); `cell-v1/LOG.md` (:142).
- Core claim (Grok entry, :139): "Linear step `L = AL N²` agrees between the breadboard toroid stamp and the 3D transient analytic, within 2%. Figure-8 thresholds do not agree: breadboard card 2/4 AT, static path about 2.67/4.97 AT, mesh window 3 / 4.75 / 8."
- Equations: `L = AL N²` (:139). Here L is inductance, not angular momentum.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: separates toroid, round figure-8, square figure-8 and the historical transfluxor (:138). "No measured B-H" (:142). "Full 3D place/rotate are not done" (:142).
- Open / parked / not-set items: figure-8 threshold split, "Do not average them" (:141). Not done: B–J validation, reinjection, six-sector, tag-and-capture, diode PERMIT, BOM reconcile. `cell-v1/LOG.md` is blank (:142). The hc = 2 card is locked by tests (:144).
- Conflicts: none against canon. Symbol hazard: `L` = inductance (:139) vs canonical L = I omega.

## BENCH_REALITY_CONTRACT — Bench Reality Contract   (`BENCH_REALITY_CONTRACT.md`)
- Gate / lifecycle: "AUTHORITATIVE QUALIFICATION BOUNDARY FOR PHYSICAL-BENCH CLAIMS" (:5). PASS ladder: SOLVER → MODEL → BENCH-REALITY → PHYSICAL (:187-192).
- Upstream: none cited. Downstream: README.md:81 points here.
- Core claim: "A solver PASS means only that the equations for the supplied model solved ... It does not automatically mean a breadboard build is physically valid" (:7). The CELL_V1 bench is ±12 V with a real 0 V midpoint and "is not a TLE2426 / rail-splitter topology" (:33-39).
- Equations: `I_0 ~= 0`, `V(0_bus) ~= V(0_source)` (:50-51); `|I_source| <= 20 mA` (:101); `VGS = Vgate - Vsource` (:117).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: §7 Magnetic truth (:149-163): "Toroids, ferrite rings, inductors, or drawn loops are not evidence of magnetic hold." A magnetic-memory claim needs a drive-off receipt that survives controls for L/R decay, RC storage, reverse recovery, sensor offset, instrument zero, thermal drift and core remanence. "Until then, magnetic parts are measurement experiments, not passed cell functions." §6: "CELL_V1: G+ / G0 / G- experiments; MOTOR: disconnected" (:140-142).
- Open / parked / not-set items: magnetic hold is unproven. Motor power stage comes later on a separate ESC/driver (:145).
- Conflicts: none against canon. Internal conflicts with other slice files are listed in the summary.

## BRAIN_3D_SCALE — 3D electrical brain, scalable build   (`BRAIN_3D_SCALE.md`)
- Gate / lifecycle: build ladder, Levels 0-3 with a pass table (:88-95).
- Upstream: `ONE_WAVE_CELL.md`, `brain_2state.py`, `nerve_cell.py` (:16). Downstream: BRAIN_CUBE_STACK.
- Core claim: "One cell. Then a slice. Then a stack. Then two stacks. Same law every time" (:3). "hex = slice. cube = stack. sphere = rotation of the walk (A→B→C and the other way)" (:12).
- Equations: none.
- Point / Path / Field role: none stated in canonical terms. "Walk around the ring is rotating B in the plane (the hex slice)" (:41). This is a sequenced field-command rotation, not a point rate and not a ride. "Field" / "Void" here are the two controller hemispheres, explorer and checker (:63-68), not the physical field.
- Magnetism / gravity / rotation link: "rotating B" walk (:41). The sphere is "rotation of the walk" (:12). "Field never grabs engage. Void never invents torque" (:68).
- Open / parked / not-set items: physical scale stops at "two cells on one G" (:74).
- Conflicts: none. Naming collision: "Field" = controller state.

## BRAIN_CUBE_STACK — Cube stacking method   (`BRAIN_CUBE_STACK.md`)
- Gate / lifecycle: method plus falsify list (:45-50).
- Upstream: BRAIN_3D_SCALE (Level 1 slices). Downstream: BUILD_25 step 23, BUILD_26_50 step 39.
- Core claim: "A cube is not six new faces of electronics. It is hex slices stacked on one spine" (:3). "DC clothes copied upward, AC stays in the slice, RC is still the window inside each cell" (:15).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: "Leftover B stays in the cell / slice that earned it. Reinjection is local. The spine carries imbalance, not memory" (:24). "A lean on slice 1 must not require slice 0 to invert. If it does, you built a puppet, not a stack" (:23). That is a local-ownership rule loosely similar to parent/child locality, but no equation is given.
- Open / parked / not-set items: Rubik scale (:33).
- Conflicts: none.

## BUILDS/MAP — Builds, separate from the breadboard   (`BUILDS/MAP.md`)
- Gate / lifecycle: canon separation rule (:5).
- Upstream: `00_RULES/architecture.md`, `interface_rules.md` (:34). Downstream / cites: `experiments/brain_cell_001.json`, `experiments/prototype_001.json`, `STAGE1_PHYSICAL_BUILD.md`, Cal A-H presets in `js/app.js`, `test/qualification.test.js`, `test/primitives.test.js`, `test/regression-builds/*.js`, `05_MEASUREMENT`, future `BUILDS/flashlight/`.
- Core claim: "A build uses the breadboard. A build does not become part of the breadboard" (:5).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated. The flashlight build is described as "balanced/reinjection vs. a conventional reference circuit" (:43).
- Open / parked / not-set items: relocation of presets to `BUILDS/`. The flashlight build does not exist yet (:42-44).
- Conflicts: none.

## BUILD_25 — Next 25 steps   (`BUILD_25.md`)
- Gate / lifecycle: bench steps 1-25 at a 50 mA knob, ending in a written receipt (:29).
- Upstream: `brain_2state.py`, `nerve_cell.py` (:15). Downstream: BUILD_26_50, LOCK.md.
- Core claim: rails, then I_0, then station A, then B, then speaker, then sensors (NTC, SS49E Hall, piezo), then station C, then a two-cell "Height-2 cube" (:23).
- Equations: none.
- Point / Path / Field role: none stated. "Walk A then B then C +1, others STAY" (:21).
- Magnetism / gravity / rotation link: Hall at the star logged quiet / during click / after STAY (:18).
- Open / parked / not-set items: motor work only after the receipt exists (:29).
- Conflicts: none against canon. Internal: 50 mA knob (:3) vs BENCH_REALITY_CONTRACT:101 (≤20 mA) and ONE_WAVE_CELL:91 (20 mA first).

## BUILD_26_50 — Steps 26–50   (`BUILD_26_50.md`)
- Gate / lifecycle: allowed only after BUILD_25 step 25 receipt (:3).
- Upstream: BUILD_25, `brain_2state`, ONE_WAVE_CELL. Downstream: `10_RECEIPTS/` CELL_V1_YYYYMMDD (:48), F1 PCB (:49-50).
- Core claim: coils replace the 1 k loads. "Walk A→B→C. Watch Hall rotate. All STAY. Note leftover Hall (reinject or not)" (:28). "Balance is a pair" (:30).
- Equations: none. Step 37 integrates rail current per click.
- Point / Path / Field role: none stated. Hall rotation follows the field walk (:28).
- Magnetism / gravity / rotation link: leftover Hall and reinjection (:28). Flight setpoint only, "Do not replace the FC inner loop" (:45-46).
- Open / parked / not-set items: SiC, 2212 and live props are excluded until F1 PCB plus current limit (:50).
- Conflicts: none against canon. Internal: step 35 "Wire Thought → jumpers or Nano GPIO (P-MOS LOW = +1, N-MOS HIGH = −1)" conflicts with ONE_WAVE_CELL:66 and BENCH_REALITY_CONTRACT §5 (no direct BLUE-referenced GPIO on ±12 gates).

## CELL_V1_FULL_BUILD — CELL_V1 Full Physical Build   (`CELL_V1_FULL_BUILD.md`)
- Gate / lifecycle: "F0 LOW-VOLTAGE PROTOTYPE / MEASUREMENT BUILD" (:5). Power-up sequence P0-P10 (:282-389). Pass numbers (:401-416).
- Upstream: LOCKED_CELL_TOPOLOGY. Downstream / cites (:463-478): `01_PARTS/CELL_V1_PARTS_BOM.md`, `02_CONNECTIONS/CELL_V1_NETLIST.md`, `03_ELECTRICAL_CORE/THREE_RAIL_VIRTUAL_GROUND.md`, `TLE2426_VIRTUAL_GROUND.md`, `MOSFET_BODY_DIODE.md`, `REVERSE_RECOVERY.md`, `04_TIME_AND_DYNAMICS/DC_AC_RC_CYCLE.md`, `07_MAGNETICS/ROTATIONAL_HOLD_TEST.md`, `09_TESTS/CELL_V1_WORKING_PATH.md`, `CELL_V1_SAFE_BRINGUP.md`, `10_RECEIPTS/CELL_V1_RECEIPT_SCHEMA.json`, regression builds 20 and 21.
- Core claim: "3 logical Mirror gates ... 12 devices DOES NOT mean 12 logical gates" (:29-45). Not established: "a spatial Bx/By/Bz magnetic field model; persistent magnetic memory after drive removal; the proposed One-Wave matter, lattice, displacement-pressure, gluonic-tension, or gravity mechanisms" (:17-21).
- Equations: `3 stations × 2 legs × 2 MOSFETs = 12` (:42); `tau ~= RRC × C = 1,000 × 10 uF = 10 ms` (:233); `I_G = V(10-ohm)/10 ohm` (:333).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: P10 "magnetic sense only ... Do not close reinjection feedback yet" (:374-376). First question: "Does measured field/flux follow current and polarity reproducibly?" (:381). §11 ferrite-ring hold experiment with four receipts, and "magnetic hold candidate" only if a drive-off retained signal reverses with prior polarity and beats the controls (:422-441). "capacitor voltage persisting ... = RC storage NOT magnetic memory NOT matter hold" (:240-244). Gravity is explicitly not established (:21).
- Open / parked / not-set items: magnetic reinjection, three-winding actuation, motor, memristive elements and XYZ field claims all wait for F0 receipts (:447-459). Magnetic memory is "FAIL/UNPROVEN" (:415).
- Conflicts: none against canon. Internal: 5 V supply plus TLE2426 NET_G (:52-61) vs BENCH_REALITY_CONTRACT:39-41 ("not a TLE2426 / rail-splitter topology" for the present CELL_V1 bench).

## DETAILED_BUILD — 2-state brain + 3-winding body   (`DETAILED_BUILD.md`)
- Gate / lifecycle: long bench sheet, sections A-G with passes and a receipt (:236-248).
- Upstream / cites: FULL_BODY_ARCHITECTURE, `09_TESTS/CELL_V1_DO_IT.md`, `HEX-SPLIT/brain_2state.py`, `HEX-SPLIT/nerve_cell.py` (:7).
- Core claim: "brain_2state.py Field lists lean/live, Void sets engage; nerve_cell.py three windings + mid, process = memory; copper ±12, three half-bridges, star = G = I_0" (:14-16).
- Equations: none.
- Point / Path / Field role: none stated in canonical terms. "Walk: A+1 (0.5 s), STAY, B+1, STAY, C+1, STAY. Watch I_0 step. That is rotating command. Field walk" (:175).
- Magnetism / gravity / rotation link: Hall at the star. "If it keeps a bias vs the pre-walk quiet, leftover B is talking (hold/reinject). If it dies immediately, memory is only current" (:186). "Calling Hall memory when it tracks only current" is illegal (:230). Actuator: "shaft or coil field follows live gate" (:220).
- Open / parked / not-set items: motor size, memristor.
- Conflicts: none against canon. Internal: Nano GPIO direct gate drive (:161-166, :186-208) conflicts with ONE_WAVE_CELL:66 and BENCH_REALITY_CONTRACT §5. The 50 mA knob (:4) conflicts with the ≤20 mA limit. The ±12 three-half-bridge motor "body" conflicts with BENCH_REALITY_CONTRACT §6 ("MOTOR: disconnected").

## FULL_BODY_ARCHITECTURE — Full body, nerve to brain, master build   (`FULL_BODY_ARCHITECTURE.md`)
- Gate / lifecycle: master map. "Until those exist the posters are maps" (:397-398).
- Upstream: HEX-SPLIT (README, SHAPES, SIX, GROUND, BODY, LATTICE, THEORY, CIRCLE, SYNC, BRAIN_CELL, `nerve_cell.py`, `clock_sync.py`) (:343-351). Downstream / cites: LOCKED_CELL_TOPOLOGY, `04_TIME_AND_DYNAMICS/THE_SYSTEM.md`, `DC_AC_RC_CYCLE.md`, `THREE_RAIL_VIRTUAL_GROUND.md`, `TLE2426_VIRTUAL_GROUND.md`, `MOSFET_BODY_DIODE.md`, `REVERSE_RECOVERY.md`, `07_MAGNETICS/ROTATING_FIELD.md`, `SPINTRONICS_LOOP.md`, `ROTATIONAL_HOLD_TEST.md`, `09_TESTS/` CELL_V1_DO_IT, FULL, MOTOR_IS_TERNARY, BENCH, WORKING_PATH, SAFE_BRINGUP, FULL_SYSTEM_BUILD, CELL_V1_POSTER, POSTER_CELL_MOTOR, POSTER_QUADRATIC_TOP, `experiments/brain_cell_001.json`, STAGE1_PHYSICAL_BUILD (:353-380).
- Core claim: "views UP (memristor / Hall B / MEM); spin UP (location, I_0, phase); spin DOWN (winding torque)" (:263-265). "rotating B walk A→B→C; hold+reinject leftover B is next baseline" (:279-280). "Feeling informs. Does not fire the FET. Override = engage 0. Not Gate-7" (:283-284).
- Equations: none. State table: "+1 high ON, STAY both OFF, −1 low ON, both ON illegal" (:300).
- Point / Path / Field role: none stated in canonical terms. "spin UP / spin DOWN" are signal-direction labels. "spin DOWN" = winding torque, a field-driven actuation. No point L or path ride is defined.
- Magnetism / gravity / rotation link: rotating B walk, leftover B hold/reinject, Hall = proprioception (:391).
- Open / parked / not-set items: motor, memristor (:324-325).
- Conflicts: canon terminology risk. "spin DOWN (winding torque)" (:265) labels field-produced torque as "spin", while canon keeps point spin (G-749) separate from field curl. Not a law conflict, since torque changing L belongs to C-306/C-307. Internal: the motor-is-cell framing conflicts with BENCH_REALITY_CONTRACT §6.

## HEX_CELL_BOARD — Virtual hex-cell PCB (CELL_V1)   (`HEX_CELL_BOARD.md`)
- Gate / lifecycle: "MODELED ≠ bench PASS ... Hardware truth is still only `cell-v1/LOG.md`" (:12-14). Tests: `test/hexcell-*.test.js` (:74-76).
- Upstream: PERFBOARD.md, `cad/pcb_hex.svg`, `cell-v1/HEX_SEATS.md`, `cell-v1/CELL.md`, `cell-v1/PHYSICAL_NET.md` (:5-7). Downstream: `js/hexexamples.js`, `js/ai.js`, `simulate.js`.
- Core claim: "3 mirrors = A/B/C (opposed pairs side 0↔3, 1↔4, 2↔5). 6 seats ≠ 6 mirrors" (:26). "CENTER island (lean reference / virtual ground) ... ≠ V_BUS, not a winding return" (:21).
- Equations: "transfluxor legs b2/b3 with L1 = b2+b3 conserved by small-aperture drive; winding voltages from Faraday's law" (:40-41).
- Point / Path / Field role: none stated. A "hysteresis lattice route" is named as a placeable part (:9-10), with no rotational meaning given.
- Magnetism / gravity / rotation link: square-loop memory cores, toroid, transfluxor, round figure-8 (sensor, hypothesized mean turn 0.028 m), square figure-8 (motor, 0.040 m) (:32-38).
- Open / parked / not-set items: "Core materials, Hc, φsat, switching τ are idealized". "How mirror commits drive the nucleus is not locked". "Multi-cell flower (base-to-base lattice between cells) is the next board step" (:80-82).
- Conflicts: none.

## INSTALL_UBUNTU — Ubuntu install   (`INSTALL_UBUNTU.md`)
- Gate / lifecycle: install instructions for release vbb-linux-1.0.2.
- Upstream: GitHub release. Downstream: `experiments/brain_cell_001.json` (:27).
- Core claim: install the `.deb`, which launches through `virtual-breadboard-simulator-safe` (:19-21).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## LOCK — the cell   (`LOCK.md`)
- Gate / lifecycle: software stamps passed. "Copper still owes BUILD_25 steps 1–11" (:16-18).
- Upstream: HEX-SPLIT `brain_2state.py`, `nerve_cell.py`, `10_RECEIPTS/cell_v1_stamp1_rails.py`, `cell_v1_stamp2_bridge.py`. Canonical read: ONE_WAVE_CELL, DETAILED_BUILD, BUILD_25, FULL_BODY_ARCHITECTURE, LOCKED_CELL_TOPOLOGY (:22-26).
- Core claim: "Kitty Hawk / hive / slip-ship = GRAV play. Not this folder's job" (:3). "Ideal G. Ideal switches. That is the virtual lock for the *law*, not for body diodes or layout" (:14).
- Equations: stamp results: I_0 0 / ±1.2 mA; STAY 0, +1 = +12 mA, −1 = −12 mA (:11-12).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: gravity is excluded from this folder (:3).
- Open / parked / not-set items: copper receipts.
- Conflicts: none.

## LOCKED_CELL_TOPOLOGY — DC, AC, Virtual Ground, Three Mirrored Gates   (`LOCKED_CELL_TOPOLOGY_DC_AC_MIRRORED_GATES.md`)
- Gate / lifecycle: "LOCKED CONCEPTUAL TOPOLOGY — design specification and simulation hypothesis. Not established gravity physics" (:5).
- Upstream: none. Downstream: CELL_V1 files under `01_PARTS` … `10_RECEIPTS` (:51), `09_TESTS/CELL_V1_SAFE_BRINGUP.md` (:92).
- Core claim: "Opposed DC rails `→ + | 0 | − ←`. Virtual ground is the middle rail. AC oscillates through the center both ways. Three mirrored stations plus RC decide hold / lean / quit. Magnetic layer retains only after it is measured. Receipt returns on the mid BACK to the controller. Never a forward output past the center" (:96).
- Equations: cycle sequences `0 → +1 → 0 → -1 → 0` and `0 → -1 → 0 → +1 → 0` (:30-31).
- Point / Path / Field role: none stated. "DC → AC → RC → rotational hold": "magnetic loop retains last route only after sense receipts, mid returns home" (:41-43). "route" here is a circuit route, not a path ride.
- Magnetism / gravity / rotation link: rotational hold is gated on sense receipts (:43). Gravity is explicitly not established (:5). "`0` = reclosed at virtual ground; hold (oscillator still live)" (:34). Here "closed" is electrical, not the canonical magnetic closed state.
- Open / parked / not-set items: §7-11 are only referenced (:51).
- Conflicts: none.

## MAGNETIC_SOLVER — Individual magnetic-component solver   (`MAGNETIC_SOLVER.md`)
- Gate / lifecycle: "These checks qualify numerical/model behavior only" (:13).
- Upstream: `js/circuit.js` (implied). Downstream: none cited. Cites TI DRV8833 datasheet §10.3.2 (:17).
- Core claim: cards are "ideal square-loop lumped models. Their coercivity, flux and switching-time constants are simulation parameters, not measured specifications" (:5). At a coercive boundary the solver uses "the convex mixture of adjacent switching branches ... not a measured domain-wall model" (:9).
- Equations: "V = R I + N delta(phi)/dt. Large-aperture transfluxor windings link phiLeg*(b2+b3); small-aperture windings link phiLeg*b3. Ampere-turns are the sum of N I on each aperture" (:7).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: retention and polarity reversal are covered as engine tests (:13). "Not implemented here: spatial field/null maps, material-specific domain structure, measured B-H calibration" (:15).
- Open / parked / not-set items: bench qualification of ALD1106/ALD110800 and the user's cores (:15). DRV8833 class model is incomplete (:17).
- Conflicts: none.

## ONE_WAVE_CELL — ONE-WAVE CELL, combined   (`ONE_WAVE_CELL.md`)
- Gate / lifecycle: merge of the split sheets, with a receipt (:109-122) and an illegal list (:126-128).
- Upstream / cites: FULL_BODY_ARCHITECTURE, DETAILED_BUILD, HEX-SPLIT `brain_2state.py`, `nerve_cell.py`, BODY, SIX, GROUND, BRAIN_CELL, SYNC, `clock_sync.py`; VBB LOCKED_CELL_TOPOLOGY, THE_SYSTEM, ROTATING_FIELD, SPINTRONICS_LOOP, TLE2426_VIRTUAL_GROUND, MOSFET_BODY_DIODE, REVERSE_RECOVERY, CELL_V1_*, POSTER_*, STAGE1_PHYSICAL_BUILD, `experiments/brain_cell_001.json`; regression `23_dualrail_gpio_gate_guard.js` (:75, :134-135).
- Core claim: "Brain is two states. Body is three windings. Mid is G. Process is memory. Motor is the ternary layer. Spintronics goes down and up" (:3). "Do not connect a BLUE-referenced Nano GPIO directly to either gate on the ±12 V build" (:66).
- Equations: none. Gate-bias targets: P-MOS ON gate≈+6 V, VGS≈−6 V; 2N7000 ON gate≈−6 V, VGS≈+6 V (:70-71).
- Point / Path / Field role: none stated in canonical terms. "spin UP location, I_0, phase; spin DOWN torque, winding current" (:17-18). "rotating B walk A→B→C" (:28). "hold all STAY, leftover B; reinject leftover B is next baseline" (:29-30).
- Magnetism / gravity / rotation link: rotating B, leftover-B hold and reinjection, Hall at the star (:51, :101).
- Open / parked / not-set items: Nano needs a level-shifted or isolated driver (:75, :103). Motor only after the resistor receipts (:105).
- Conflicts: canon terminology risk, the same "spin DOWN = torque" point as FULL_BODY. "reinject" means leftover-B baseline and is unrelated to E-530 reinjection (name collision only). Internal: "Motor is the ternary layer" (:3) vs BENCH_REALITY_CONTRACT §6.

## PERFBOARD — Virtual Perfboard   (`PERFBOARD.md`)
- Gate / lifecycle: "Simulation results are model evidence, not bench qualification" (:61). Tests: `test/perfboard-*.test.js`.
- Upstream: `js/board.js`. Downstream: HEX_CELL_BOARD.
- Core claim: "Every pad is isolated ... Two leads on adjacent pads are not connected until you add a solder run or wire" (:12, :19-20).
- Equations: none. Expected values: LED ≈ 9.3 mA; 10k/10k @ 9 V gives 4.5 V; RC 1k/100 uF gives 3.16 V at tau (:44, :54).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## README — Virtual Breadboard Simulator   (`README.md`)
- Gate / lifecycle: product README. "MODELED is not PASS" (:49). Points to BENCH_REALITY_CONTRACT (:81).
- Upstream: `../validation/SCIENCE_CONNECTIONS.md` (:2, "links do not imply validation"). Downstream / cites: STAGE1_PHYSICAL_BUILD.md, `test/circuit.test.js` (T-DIV … T-NO-MACRO), `test/practice-interface.test.js`, `js/*.js`, `simulate.js`. **Node cited: G-744**, "Ternary cell (G-744): Stage 1 Real Millivolt Ternary ... the actual G-744 circuit" (:570-573).
- Core claim: an MNA solver with real-part models. "This is deliberately a simplified analog model ... no core saturation, no skin effect" (:269-275).
- Equations: Virtual Ground `V(out) = (V(A)+V(B))/2` (:133-134); toroid L = `A_L * turns²` (:165); sense voltage `N · dΦ/dt` (:196, :539); RC τ = 15 ms (Cal E, :512) and τ = R·C = 1 s (memory cell, :521); window `V0 ± 20mV` (:575).
- Point / Path / Field role: none stated. MTJ Angle Sensor gives sin/cos "of a rotating field" but is "not a claim to simulate real magnetic/inductive field physics" (:147-157).
- Magnetism / gravity / rotation link: Memory Core (:187-214): normalized remanent `B ∈ [-1,+1]`. Below Hc, "B is frozen exactly where it was". Past ±Hc it flips toward ±1. "Power the driving FETs off entirely and B does not move: this is DC memory that survives the gate closing". Group memory and toward/away neighbor coupling arise "from real multi-winding superposition and winding-polarity (dot-convention) physics" (Cal H, :552-560). This is idealized: "no temperature dependence, no half-select disturb" (:211-213, :276-281). No gravity.
- Open / parked / not-set items: no B-H curve, saturation or leakage flux (:172-173). Toroid is linear only.
- Conflicts: none against canon. Symbol hazard: `A_L * turns²` inductance "L" vs canonical L. Internal tension: README:200-202 calls the memory core "DC memory that survives the gate closing" as a model statement, while BENCH_REALITY_CONTRACT §7 says magnetic parts are unproven measurement experiments until a drive-off receipt. README:81-83 does defer to that contract.

---

## Slice summary

### (a) Node IDs / chapters and how they bear on Point / Path / Field, rotation, magnetism, gravity, inertia, mass, resistance, lattice

- **G-744** (README.md:570-573): the Stage 1 Real Millivolt Ternary cell, built from a window comparator, a V0 reference and a P/N MOSFET pair writing MEM. It is a ternary decision circuit (Left / Hold / Right). The slice gives it no rotation, magnetism, gravity or inertia role.
- No other node or chapter IDs are cited in the slice. The files below bear on the requested topics only in hardware terms:
  - **Point**: no file defines point rotation, L = I omega, attitude or inertia. Nothing implements the canonical point rate.
  - **Path**: no file defines a ride or orbit. "route" (LOCKED_CELL:43), "WORKING_PATH" and "static path" (AI_CONSTRUCTION_LOG:139, magnetic path length) are circuit or flux-path terms only.
  - **Field**: the hardware's field-like element is the sequenced **rotating B walk A→B→C** of three windings on a star (FULL_BODY:279, ONE_WAVE_CELL:28, DETAILED_BUILD:175, BRAIN_3D_SCALE:12,41, BUILD_26_50:28), read by a Hall sensor at the star. "Field" / "Void" are controller hemispheres (explorer / checker), not the physical field.
  - **Magnetic open/closed**: the canonical dL/dt = 0 vs −gamma L split is not used anywhere. The nearest hardware analogues, stated only as analogues:
    - square-loop memory-core hold, where B is frozen below Hc and survives drive-off in the model (README:191-202; MAGNETIC_SOLVER:7-13);
    - ordinary L/R inductive decay, which must be excluded as a control (BENCH_REALITY:155; CELL_V1_FULL_BUILD:441);
    - "leftover B" hold and reinjection after all-STAY (ONE_WAVE_CELL:29-30, DETAILED_BUILD:186, BRAIN_CUBE_STACK:24).
    - Hardware status: magnetic hold is **unproven** (CELL_V1_FULL_BUILD:415, BENCH_REALITY §7). Reinjection feedback is deliberately not closed (CELL_V1_FULL_BUILD:376).
  - **Gravity**: explicitly out of scope in LOCK.md:3, LOCKED_CELL:5 and CELL_V1_FULL_BUILD:21.
  - **Lattice**: "hysteresis lattice route" part and "multi-cell flower (base-to-base lattice)" as the next board (HEX_CELL_BOARD:9,82). Toward/away neighbor core coupling via shared ampere-turns (README Cal H). Hex slice, cube and Rubik stacking on a shared G spine (BRAIN_3D_SCALE, BRAIN_CUBE_STACK). None of these claim bound-lattice rate locking, mass or resistance = mass/organization.
  - **Resistance**: electrical only (ohms, RDS(on)). No inertia or mass meaning.

### (b) Conflicts

Against the canonical rules: **no direct law conflicts**. Terminology and symbol hazards:
1. "spin UP / spin DOWN (winding torque)" (FULL_BODY_ARCHITECTURE:264-265; ONE_WAVE_CELL:17-18). This labels field-driven winding torque and signal flow as "spin", which blurs canon's separation of point spin (G-749) from field curl.
2. `L` = inductance (`L = AL N²`, AI_CONSTRUCTION_LOG:139; `A_L * turns²`, README:165) vs canonical L = I omega.
3. "reinject leftover B" (ONE_WAVE_CELL:30, FULL_BODY:280, BRAIN_CUBE_STACK:24) is unrelated to E-530 reinjection (name collision).
4. "Field" = controller hemisphere (BRAIN_3D_SCALE:63, DETAILED_BUILD:14, ONE_WAVE_CELL:12) vs canonical Field (curl).

Internal conflicts between slice files:
5. Rail topology: CELL_V1_FULL_BUILD:52-61 (5 V + TLE2426 NET_G) vs BENCH_REALITY_CONTRACT:33-41 (±12 V real midpoint, "not a TLE2426 / rail-splitter topology").
6. Gate drive: DETAILED_BUILD:161-166 and BUILD_26_50:35 (direct Nano GPIO on P/N gates) vs ONE_WAVE_CELL:66 and BENCH_REALITY_CONTRACT:120-128 (forbidden on the ±12 build).
7. Current limit: BUILD_25:3 and DETAILED_BUILD:4 (50 mA) vs BENCH_REALITY_CONTRACT:101 (≤20 mA F0 acceptance) and ONE_WAVE_CELL:91 (20 mA first).
8. Motor in the cell: ONE_WAVE_CELL:3, FULL_BODY:286-301 and DETAILED_BUILD §10 (three half-bridges / motor as the cell body) vs BENCH_REALITY_CONTRACT:134-145 ("CELL_V1 and a BLDC inverter are separate machines ... MOTOR: disconnected").
9. Magnetic memory wording: README:200-202 ("DC memory that survives the gate closing", model) vs BENCH_REALITY_CONTRACT:151-163 and CELL_V1_FULL_BUILD:415 (unproven). README:81-83 defers to the contract, so this is a model-vs-bench scope difference rather than a contradiction.
10. Figure-8 coercive thresholds disagree across solvers: 2/4 AT, ~2.67/4.97 AT, and 3 / 4.75 / 8 (AI_CONSTRUCTION_LOG:139,141). This is recorded and must not be averaged.

### (c) Cross-references outside the slice that matter for point rotation or magnetism
- `07_MAGNETICS/ROTATING_FIELD.md`, `07_MAGNETICS/SPINTRONICS_LOOP.md`, `07_MAGNETICS/ROTATIONAL_HOLD_TEST.md`, `07_MAGNETICS/SOLVERS.md` (Builds/Virtual_Breadboard)
- `04_TIME_AND_DYNAMICS/THE_SYSTEM.md`, `04_TIME_AND_DYNAMICS/DC_AC_RC_CYCLE.md`
- `09_TESTS/CELL_V1_MOTOR_IS_TERNARY.md`, `POSTER_CELL_MOTOR.md`, `POSTER_QUADRATIC_TOP.md`
- HEX-SPLIT: `LATTICE`, `THEORY`, `CIRCLE`, `SIX`, `GROUND`, `BODY`, `BRAIN_CELL`, `brain_2state.py`, `nerve_cell.py`
- `cell-v1/LOG.md` (hardware truth, currently blank), `cell-v1/CELL.md`, `cell-v1/HEX_SEATS.md`, `cell-v1/PHYSICAL_NET.md`, `cad/pcb_hex.svg`
- `Virtual_3D_Electronics/js/circuit.js`, `js/magnetics.js` (3D mesh magnetic solver)
- `../validation/SCIENCE_CONNECTIONS.md` (Builds repo research connection index, from README:2)
