# Ledger b03: Builds/Virtual_Breadboard, layers 03 to 11 plus the 3D work register

Repo read: `/home/user/Builds/Virtual_Breadboard` (Builds repo, not One-Wave-Science). 51 of 51 slice files were read in full with line numbers.

**Slice-wide finding.** None of the 51 files cites a One-Wave node ID (no `X-nnn` pattern) or a Book chapter. A regex sweep over all 51 files (`[A-Z]{1,2}-[0-9]{2,4}`, `Ch…`, `Book`) returned zero real hits. So every "Upstream / Downstream / cites" line below lists **files**, not nodes.

**Naming collisions to keep in mind for the whole slice:**
- **Field / Void.** Here "Field" means the software *explorer* that "lists lean", and "Void" means the *checker* that may cut engage (FULL_SYSTEM_BUILD:9). This is not the canonical Field (curl / wake / compression / gradient).
- **Reinjection.** Here "reinjection" means "leftover B / remanence is the next cycle's baseline" (ROTATING_FIELD:12). This is not E-530 reinjection.
- **G.** Here "G" is the electrical mid-rail NET_G / BLUE / star. It is not gravity (g) and not a node prefix.

---

## 03_ELECTRICAL_CORE/MAP: Layer 03 Electrical Core (`03_ELECTRICAL_CORE/MAP.md`)
- Gate / lifecycle: "Status: implemented, generic, no build-specific logic found" (:10). Every capability row is marked PASSING.
- Upstream: `circuit.js` (solveLinear :465, MNA :920-1450, GMIN :109/:949, diagnose :262). Downstream / cites: `qualification.test.js`, `test/fault-states.test.js`, `04_TIME_AND_DYNAMICS/MAP.md`, `../00_RULES/architecture.md`.
- Core claim: :5-8 "Given these connected components, what are the electrical conditions? … No Field/Void/flashlight/nerve/motor logic belongs here." :24-35 describe a dt floor bug (`Math.max(dt,1e-6)`) that was fixed by changing the floor to 1e-12.
- Equations: none (narrative only: Gauss-Jordan, MNA stamping, convergence check `if (!changed) break`).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: only that "core B" is listed as a nonlinear device in the fixed-point loop (:16). Nothing else stated.
- Open / parked: no standalone nonlinear_solver / convergence / power_balance files exist (:39-44).
- Conflicts: none.

## MOSFET_BODY_DIODE: MOSFET body diode vs the mirrored station (`03_ELECTRICAL_CORE/MOSFET_BODY_DIODE.md`)
- Gate / lifecycle: design note with an F0 log list and falsifiers.
- Upstream: web refs [web:78], [web:79], [web:82]. Downstream / cites: CELL_V1 stations G0 / G+ / G−.
- Core claim: :12 "Channel OFF does not mean the part is open both ways… A single FET is not a mirrored gate." :27 back-to-back with common source gives "bidirectional blocking". :61 "G0 is the station that must not become a rectifier."
- Equations: loss ~ V × Qrr × f (:39). On-state drop Vsd = I×(2 Rds) (:29).
- Point / Path / Field role: none stated. The channel is a conduction *path* only in the electrical sense.
- Magnetism / gravity / rotation link: :71 "Do not close a magnetic feedback loop until those five traces exist." This is a gating rule for magnetic closure.
- Open / parked: the five F0 traces are not yet logged.
- Conflicts: none.

## REFERENCE_IS_THE_UPDATE: Reference at every step is the free update (`03_ELECTRICAL_CORE/REFERENCE_IS_THE_UPDATE.md`)
- Gate / lifecycle: principle statement. No test is attached.
- Upstream / Downstream: none cited.
- Core claim: :3 "You do not ship a new world each tick. You touch G again." :14 "Reinjection is this: next step inherits G and leftover B. Power stays at the floor until a lean spends."
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: "leftover B" is inherited between steps (:8, :14). Nothing is said about L or rotation.
- Open / parked: none.
- Conflicts: none. ("Reinjection" is the local usage, not E-530.)

## REVERSE_RECOVERY: Reverse recovery dynamics (`03_ELECTRICAL_CORE/REVERSE_RECOVERY.md`)
- Gate / lifecycle: model note plus an F0 measurement procedure. :77 says "still a model, not a parts list".
- Upstream / Downstream: CELL_V1 NET_G, I_G.
- Core claim: :32 "That dump is a one-way current pulse on the mid… It is not a lean of the pair. It is leftover plasma." :46 "Sample after the window, or the receipt is the diode."
- Equations: trr = ta + tb (:14). Energy ≈ Vr × Qrr per event, power Vr × Qrr × f (:34). V = L di/dt (:36).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: :83 "Magnetic sense after this. A coil will happily integrate Irr and call it flux memory."
- Open / parked: the six-step F0 Qrr measurement has not been performed.
- Conflicts: none.

## THREE_RAIL_VIRTUAL_GROUND: Three-Rail CENTER / Virtual Ground (`03_ELECTRICAL_CORE/THREE_RAIL_VIRTUAL_GROUND.md`)
- Gate / lifecycle: F0 prototype acceptance limits. :60 says these are "not fundamental constants".
- Upstream / Downstream / cites: `TLE2426_VIRTUAL_GROUND.md`, `../CELL_V1_FULL_BUILD.md`, `../09_TESTS/CELL_V1_SAFE_BRINGUP.md` (:66).
- Core claim: :15 "NET_G is made. It is not earth ground and it is not allowed to wander with the load." :21 one spine, with each station starred through a 10 Ω receipt.
- Equations: I_GX = [V(GX_TAP) − V(NET_G)] / 10 Ω (:38). NET_P = +2.5, NET_G = 0, NET_N = −2.5 relative (:8-10).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked: limits are prototype values only. Within 10 mV / 25 mV of half supply (:55-56).
- Conflicts: none.

## TLE2426_VIRTUAL_GROUND: TLE2426 as the mid host (`03_ELECTRICAL_CORE/TLE2426_VIRTUAL_GROUND.md`)
- Gate / lifecycle: part note for CELL_V1 steps P1–P2.
- Upstream: TLE2426 datasheet values (Fig. 17 stability). Downstream: NET_G home.
- Core claim: :3 "Output is Vin/2. It sources and sinks. That is why it can be G, and a two-resistor divider cannot." :36 the I_G budget is 20 mA through OUT.
- Equations: OUT = Vin/2. Spec table at :26-34.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked: above about 15 mA of imbalance this part is the wrong host (:74).
- Conflicts: none inside the slice. PART_DISCREPANCY_MATRIX:7-8 records that a TLE2426 stacked on a ±12 V real-0 star is a MIXED_CENTER conflict.

## DC_AC_RC_CYCLE: CELL_V1 DC / AC / RC Cycle (`04_TIME_AND_DYNAMICS/DC_AC_RC_CYCLE.md`)
- Gate / lifecycle: F0 sequence and outcome language.
- Upstream / Downstream: NET_G, HOLD node.
- Core claim: :3 "The cycle is not a one-way conveyor." :54 "The higher One-Wave mechanical language — push / squeeze / mirror / pull / tension — is a proposed interpretation of these measured relations. Do not substitute that language for voltage/current/time receipts."
- Equations: τ ≈ 1 k × 10 µF ≈ 10 ms (:39).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: :58-64 separate three storage modes: capacitor voltage (RC), inductor current (inductive decay), and "remanent field after drive removal = magnetic-hold candidate only after controls". **Hardware open/closed:** :51 "BREAK = reference/gate condition leaves the accepted window or the loop is intentionally opened."
- Open / parked: magnetic memory requires repeatable polarity reversal plus controls.
- Conflicts: none.

## DC_AC_RC_SPHERE: DC · AC · RC, three axes, one sphere (`04_TIME_AND_DYNAMICS/DC_AC_RC_SPHERE.md`)
- Gate / lifecycle: conceptual mapping only.
- Upstream / Downstream: none cited.
- Core claim: :4-6 DC = X ("opposed clothes"), AC = Y ("crossing"), RC = Z ("window"). :15 "Same three lines at every cell. No fourth axis."
- Equations: none.
- Point / Path / Field role: **Path**, in state space only. :11 "Walk A→B→C is rotation in the AC plane. STAY is a latitude." :13 "so the path has duration". Point and Field: none stated. The three axes are DC / AC / RC, not Point / Path / Field.
- Magnetism / gravity / rotation link: rotation here is a sequence rotation in an abstract state plane, not a body rotation.
- Open / parked: none.
- Conflicts: none explicit. Caution: this "three axes" scheme is a different triad from the canonical Point / Path / Field. It must not be read as that triad.

## 04 MAP: Layer 04 Time and Dynamics (`04_TIME_AND_DYNAMICS/MAP.md`)
- Gate / lifecycle: implemented as backward-Euler companions. All rows are PASSING.
- Upstream: `circuit.js` line refs. Downstream: `qualification.test.js`, `regression-builds/05,13`, `test/circuit.test.js` T-CORE-LOCK/HOLD.
- Core claim: :28-47 nine `Math.max(dt,1e-6)` sites were lowered to 1e-12. Before the fix, an LC tank rang at 1e-6/dt times the analytic 15915 Hz.
- Equations: none written out (references to the backward-Euler stamp).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: :23 "Magnetic core remanence through time … damped fixed-point relaxation … PASSING". This is a lumped model only.
- Open / parked: no built-in history recorder (:24). The delay primitive is intentionally absent (:56-59).
- Conflicts: none.

## THE_SYSTEM: The system (`04_TIME_AND_DYNAMICS/THE_SYSTEM.md`)
- Gate / lifecycle: summary statement.
- Upstream / Downstream: none cited.
- Core claim: :3 "One cell. Opposed DC. Bidirectional AC through the mid. RC is the window. Three windings are the ternary layer. Star is G. Process is memory." :13 "Hold is balance on G with the oscillator still live." :15 "Full flip is views up and torque down as the same crossing."
- Equations: none.
- Point / Path / Field role: none stated explicitly. "Torque down" is the action on a rotor, with no L bookkeeping.
- Magnetism / gravity / rotation link: windings A B C = G+ G0 G− make up the "TC-AC motor / nerve" (:9).
- Open / parked: none.
- Conflicts: none.

## 05 MAP: Layer 05 Measurement (`05_MEASUREMENT/MAP.md`)
- Gate / lifecycle: implemented in `simulate.js`. All rows are PASSING except the gaps below.
- Upstream: `simulate.js` function line refs. Downstream: `primitives.test.js`, `circuit.test.js`.
- Core claim: :5 "Observation only, never mutation."
- Equations: none.
- Point / Path / Field role: none stated. Field-vector measurement is absent.
- Magnetism / gravity / rotation link: :38-39 "Bx/By/Bz field-vector measurement … Not yet exposed."
- Open / parked: probe loading is MISSING. Bx/By/Bz is MISSING.
- Conflicts: none.

## 06 MAP: Layer 06 Reusable Primitives (`06_PRIMITIVES/MAP.md`)
- Gate / lifecycle: callable recipes, proven in `test/primitives.test.js`.
- Upstream / Downstream: `qualification.test.js`, `regression-builds/*`, `../00_RULES/physics_rules.md`, PR #15.
- Core claim: :5 "never a magical new component." :35-40 the "Ternary Cell" macro was removed as a Rule 6 violation.
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated. The "Reinjection" primitive is a storage cap plus Schmitt plus PMOS reconnect (:28). This is electrical, not E-530.
- Open / parked: recipes still live inside test files (:44-48).
- Conflicts: none.

## 07 MAP: Layer 07 Magnetics (`07_MAGNETICS/MAP.md`)
- Gate / lifecycle: mixed. Inductor, coupling and three-winding rows are PASSING. Bx/By/Bz, material and B-H rows are MISSING or NOT VERIFIED.
- Upstream: `circuit.js` toroid stamp, `js/magnetics.js`. Downstream: `test/magnetic-part-options.test.js`, `qualification.test.js` #19/#20, `primitives.test.js` P8, `regression-builds/14,15`.
- Core claim: :29-32 "magnetics model is explicitly a lumped mutual-inductance / square-loop-remanence approximation, not a field solver — it … doesn't compute a field at all. Bx/By/Bz is recorded as MISSING rather than faked." :41 "No energy gain is claimed."
- Equations: L_ij = sense_i·sense_j·k·√(Li·Lj) (:16). R = N·length·0.0531 Ω/m (:18). I = V/(BATTERY_RINT + N·length·0.0531), clamped at 2 A (:37-39).
- Point / Path / Field role: **Field is not implemented**: no field shape and no curl. Point: none stated. Path: none stated.
- Magnetism / gravity / rotation link: winding dot sense ±1 is the coupling sign. Round vs square figure-8 differ only by hypothesized copper length.
- Open / parked: Bx/By/Bz, material B-H library, and measured hysteresis / remanence for the figure-8 parts.
- Conflicts: none.

## ROTATING_FIELD: Rotating field, hold, reinjection (`07_MAGNETICS/ROTATING_FIELD.md`)
- Gate / lifecycle: design claim with a five-item bench test (:45-51). It is not yet passed.
- Upstream / Downstream: none cited by file.
- Core claim: :3-4 "Three windings at the star are a rotating magnetic field when you walk live-gate around A→B→C. That rotation … is how state is carried and how it is put back." :30 "If the core / rotor / remanence keeps an orientation, that is state hold. If it forgets the instant current dies, you had torque, not a hold loop." :32 "Reinjection: the next engage does not start from zero. It starts from the B that stayed."
- Equations: none. The table at :24-26 has the B-vector stepping 120° per seq.
- Point / Path / Field role:
  - **Field:** the rotating B vector, stepped by the three-phase walk (:10, :24-26). This is rotation of the field direction, not curl.
  - **Point:** implicit only. "core / rotor … keeps an orientation" (:30), and "actions DOWN (torque / spin from the same flip)" (:14). No L, I, inertia or ω is stated.
  - **Path:** the A→B→C sequence walk. A ride or orbit is not stated.
- Magnetism / gravity / rotation link: **hardware open/closed.** Drive ON (closed winding path) = torque. "Hold = all STAY. Drive current dies" (:30), meaning high-Z / open. Retention after opening is remanence. The canonical dL/dt law is not mentioned.
- Open / parked: bench steps 2–5. :51 "A toroid with one turn of hookup wire will fail 3."
- Conflicts: no direct contradiction. There is a **tension** with the canonical rule "Field curl is neither [point nor path]": :4 makes the rotating *field* the carrier of state, and :14 ties "spin" to the same flip, with no Point/Path/Field separation. Per the canonical rules this would be an incomplete three-rate description. It is not a stated exception.

## ROTATIONAL_HOLD_TEST: CELL_V1 Rotational / Magnetic Hold Test (`07_MAGNETICS/ROTATIONAL_HOLD_TEST.md`)
- Gate / lifecycle: "Sense first. Feedback later." (:3). Sense-only, with reinjection NONE (:15).
- Upstream: G0 after electrical tests pass. Downstream: CELL_V1_SAFE_BRINGUP P10.
- Core claim: :52 "If the signal follows current while powered and collapses with ordinary inductive/RC decay, the result is field coupling, not memory." :66 "a passing lumped simulation is not a 3-D magnetic-field proof."
- Equations: none.
- Point / Path / Field role: none stated. Bx/By/Bz is absent (:66).
- Magnetism / gravity / rotation link: four receipts are required: +pulse, −pulse, no-core control, and drive-off delayed sample (:24-27). **Open/closed:** :56 "Do not close active magnetic reinjection if…" lists the stop conditions.
- Open / parked: active feedback / reinjection is parked until sense passes (:68).
- Conflicts: none.

## SOLVERS: Equations and the solvers that run them (`07_MAGNETICS/SOLVERS.md`)
- Gate / lifecycle: reference. Triangulation within 2%.
- Upstream: `Virtual_3D_Electronics/js/parts.js`, `circuit.js`, `magnetics.js`, `physics.js`, `test/transient.test.js`, `test/corestate.test.js`. Downstream: `test/solver-triangulation.test.js`, `Virtual_Breadboard/js/triad3d.js`.
- Core claim: :3 "Two magnetic solvers… share the linear inductor step. They do not share a figure-8 threshold." :67 "Do not treat a breadboard pass as a check of the 3D mesh, or the reverse."
- Equations (verbatim):
  - Linear step: `AL = mu0*mui*Ae/le`, `L = AL*N^2` (:11-12). `I(t) = (V/R)(1 - exp(-t R/L))` (:18). `Va - Vb = R i + dλ/dt`, `λ = N*sense*Φ` (:24-25).
  - Breadboard toroid stamp: `V_i - R_i I_i - Σ_j (L_ij/dt) I_j = -Σ_j (L_ij/dt) I_j,prev` (:31).
  - 3D transient mesh: `Σ_b H_b l_b = Σ N*sense*thread*I`, `B = Br tanh(p/a) + (Bsat-Br) tanh(H/Hrev) + mu0 H`, `p moves only when |H-p| > Hc` (:49-53).
  - Breadboard figure-8: `Φ_large = phiLeg*(b2+b3)`, `Φ_small = phiLeg*b3`, `V = N dΦ/dt`, thresholds hcLarge = 2 and hcSmall (:59-64).
- Point / Path / Field role: **Field** is reduced to a magnetic-circuit (Σ H·l = NI) or a lumped flux. There is no spatial field and no curl. Point and Path: none stated.
- Magnetism / gravity / rotation link: none beyond hysteresis.
- Open / parked: the three figure-8 thresholds (2/4, ~2.67/4.97, 3/4.75/8) are unreconciled.
- Conflicts: none.

## SPINTRONICS_LOOP: Spintronics loop (`07_MAGNETICS/SPINTRONICS_LOOP.md`)
- Gate / lifecycle: conceptual.
- Upstream / Downstream: none cited.
- Core claim: :3 "Not a chute. Down is torque. Up is where it is and what it did." :21-22 "I_0 is already an UP line (vagus). Hall / encoder / search coil is the location UP line. Those two are the spintronic return. They are not a fourth winding."
- Equations: none.
- Point / Path / Field role:
  - **Point (implicit):** "UP spin: location, phase, I_0, Hall angle" (:9), which senses rotor position and phase.
  - "DOWN spin: winding current, torque, step" (:10) is the drive.
  - No L, inertia or rate split is stated.
- Magnetism / gravity / rotation link: "spin" is used for both the drive and the sensed rotor state. This is not quantum spin and not L bookkeeping.
- Open / parked: none.
- Conflicts: no direct conflict. The word "spin" is overloaded: it is not the canonical point spin with L = Iω.

## 08 MAP: Layer 08 Power (`08_POWER/MAP.md`)
- Gate / lifecycle: battery and power rows are PASSING. The general energy-closure check is MISSING.
- Upstream: `circuit.js` constants. Downstream: `qualification.test.js` Gate 7, `primitives.test.js` P5/P9/P10, `regression-builds/16`.
- Core claim: :30-35 the energy-accounting rule does not yet exist as a reusable check. This is described as an accounting-composition gap, not a physics gap.
- Equations: none (named functions only).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked: energy-balance closure.
- Conflicts: none.

## REINJECT_MIN_POWER: Minimal power via reinjection (`08_POWER/REINJECT_MIN_POWER.md`)
- Gate / lifecycle: design rule plus a measurement instruction (:38).
- Upstream / Downstream: none cited.
- Core claim: :3 "You pay for change. You should not pay rent on a state you already hold." :8 "leftover B remanence / rotor / MEM state for free". :36 "Reinjection only saves power if leftover state is real. If Hall dies when current dies, you have no battery in B."
- Equations: energy per click = ∫ rail current over pulse (:38, in words).
- Point / Path / Field role:
  - **Point (implicit):** :33 "Flight: nerve sends deltas, FC holds attitude." Attitude is held by the external flight controller.
  - Field: leftover B.
  - Path: none stated.
- Magnetism / gravity / rotation link: **hardware open/closed.** STAY = FETs off = "near zero drive" (:7). Hold is maintained by remanence, not by driving. "PWM to hold position: fail — that is rent" (:21).
- Open / parked: whether leftover B is real is not yet measured.
- Conflicts: none against the L rules. Soft risk: "state for free" (:8) could be misread as an energy exception. The text conditions it on real remanence (:36), and 07 MAP:41 / the work register disclaim energy gain.

## CELL_ACTUAL_BUILD: CELL_V1 actual first board (`09_TESTS/CELL_ACTUAL_BUILD.md`)
- Gate / lifecycle: build instructions. A first DMM receipt is expected.
- Upstream / Downstream: none cited.
- Core claim: :3 "Do A and law first. B and C copy A." :24-28 STAY = both pulldowns, +1 = P-gate, −1 = N-gate, "Never both jumpers."
- Equations: none. Expected I_0 ≈ 1.2 mA with one law 10 k pulled (:38).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated ("later coils", :33).
- Open / parked: stations B and C.
- Conflicts: none.

## CELL_SCHEMATIC_PRINT: CELL_V1 print (`09_TESTS/CELL_SCHEMATIC_PRINT.md`)
- Gate / lifecycle: schematic plus a gate-drive warning.
- Downstream: PART_DISCREPANCY_MATRIX:9, `regression-builds/23`.
- Core claim: :12 "+1 high ON STAY both OFF −1 low ON both ON illegal". :28 "Do not wire BLUE-referenced 0/5 V GPIO directly to these ±12 V gates."
- Equations: VGS ≈ ∓6 V (:20, :24).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: windings A/B/C to STAR (:4-6). No rotation physics.
- Open / parked: Nano requires a level-shifted driver.
- Conflicts: none.

## CELL_V1_BENCH: CELL_V1 bench, the actual board (`09_TESTS/CELL_V1_BENCH.md`)
- Gate / lifecycle: night 1 / night 2 receipts ("five numbers on paper", :72).
- Upstream / Downstream: TLE2426.
- Core claim: :43-44 "Unplug one 10 k. Current appears at OUT. V_G should barely move. That is lean. Plug it back. Current dies. That is hold."
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: :20 "Do not buy a coil pack." The coil is deferred (:76).
- Open / parked: G+ / G−, AC, sense coil, and actuator.
- Conflicts: none.

## CELL_V1_DO_IT: Do it (`09_TESTS/CELL_V1_DO_IT.md`)
- Gate / lifecycle: night 1 / night 2 receipts.
- Downstream / cites: `nerve_cell.py` (:113).
- Core claim: :59 "You just proved: balance holds, asymmetry moves, mid home." :113 "`nerve_cell.py` is the software ghost of this. It does not replace Night 1."
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: :101 "Do not add a toroid." :111 ESC motor later, on the same 0.
- Open / parked: copying the pair, Nano, ESC.
- Conflicts: none.

## CELL_V1_FULL: CELL_V1 full build (`09_TESTS/CELL_V1_FULL.md`)
- Gate / lifecycle: an 8-row pass table defines "the full cell" (:59-72).
- Upstream / Downstream: none cited.
- Core claim: :57 "No toroid required for the cell to be complete. No motor on these FETs." :89 "Illegal: Calling a toroid memory before row 1–7 exist on paper."
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: the motor is a "second machine" on an ESC (:74-81). Note: CELL_V1_MOTOR_IS_TERNARY:3 later reframes this ("Not a second machine").
- Open / parked: pass table unfilled.
- Conflicts: none against canon. There is an internal doc tension with CELL_V1_MOTOR_IS_TERNARY:3 and :39 (motor as second machine vs not).

## CELL_V1_MOTOR_IS_TERNARY: Motor is the ternary layer (`09_TESTS/CELL_V1_MOTOR_IS_TERNARY.md`)
- Gate / lifecycle: design plus a 5-row bench table.
- Downstream / cites: `nerve_cell.py` (:32).
- Core claim: :3 "Not a second machine. The three windings are the three gates." :34-35 "Hold for the cell: all three STAY, or currents at the star cancel so I_0 ≈ 0. Movement: live winding ±1, I_0 takes a sign, shaft may twitch." :74 "Hold is high-Z, not shorting the star to a rail."
- Equations: none.
- Point / Path / Field role: **Point (implicit):** "shaft may twitch" (:35). No L is given. Path and Field: none stated.
- Magnetism / gravity / rotation link: **hardware open/closed.** STAY = both OFF = high-Z (open winding) = hold. ±1 = one FET ON = closed winding loop through the star = torque. Shorting the star to a rail is explicitly *not* hold (:74).
- Open / parked: small-motor test.
- Conflicts: none against canon.

## CELL_V1_POSTER: One-Wave cell build poster (`09_TESTS/CELL_V1_POSTER.md`)
- Gate / lifecycle: poster.
- Core claim: :3 "Three windings = ternary layer. Star = G. Rotating B = reinjection + hold." :22-23 "Walk A→B→C to rotate B. All STAY = hold. Leftover B = next baseline."
- Equations: none.
- Point / Path / Field role: **Field:** rotating B. Point and Path: none stated.
- Magnetism / gravity / rotation link: same open (STAY) / closed (live) mapping as ROTATING_FIELD.
- Open / parked: none.
- Conflicts: none direct. Same Field-carries-state tension as ROTATING_FIELD.

## CELL_V1_SAFE_BRINGUP: CELL_V1 Safe Bring-Up (`09_TESTS/CELL_V1_SAFE_BRINGUP.md`)
- Gate / lifecycle: P0–P10 gated steps. :138 "Do not advance on a FAIL."
- Upstream / Downstream / cites: `../CELL_V1_FULL_BUILD.md` (:5), `../07_MAGNETICS/ROTATIONAL_HOLD_TEST.md` (:117).
- Core claim: :3 "Do not populate all three stations and then debug the pile." :117 P10 "No active magnetic reinjection yet."
- Equations: I_G0 = [V(G0_TAP) − V(G)] / 10 Ω (:64). τ ≈ 1 k·10 µF ≈ 10 ms (:94).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: magnetic sense only, at P10.
- Open / parked: all steps, with no receipts recorded here.
- Conflicts: none.

## CELL_V1_WORKING_PATH: How to make CELL_V1 work (`09_TESTS/CELL_V1_WORKING_PATH.md`)
- Gate / lifecycle: P0–P10 done-table. "Stop at the first fail" (:23).
- Downstream / cites: `LOCKED_CELL_TOPOLOGY_DC_AC_MIRRORED_GATES.md`, `CELL_V1_SAFE_BRINGUP.md`, `MOSFET_BODY_DIODE.md`, `REVERSE_RECOVERY.md`, `10_RECEIPTS/CELL_V1_RECEIPT_SCHEMA.json` (:99-103).
- Core claim: :3 "'Work' means the mid stays a mid, hold is balance, lean is a logged I_G, and Qrr does not get to vote. Not gravity." :66 "If the probe forgets when the channel opens, it was not memory."
- Equations: none (controller pseudocode at :70-77).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link:
  - **Gravity is explicitly excluded** (:3).
  - **Open/closed:** :66 "when the channel opens" means drive-off. Memory must survive the opened channel. :94 "Magnetic feedback before sense" is a known failure.
- Open / parked: P0–P10.
- Conflicts: none. This file is consistent with "magnetism does not become gravity".

## FULL_SYSTEM_BUILD: Full system, biology as the map, copper as the body (`09_TESTS/FULL_SYSTEM_BUILD.md`)
- Gate / lifecycle: build plus 6 first receipts (:67-74).
- Downstream / cites: `HEX-SPLIT/nerve_cell.py` (:50).
- Core claim: :3 "Not a medical device. Biology is how you read the layers." :20 "Rotating B is gait. Reinjection is proprioception: what the limb kept when you stopped pushing."
- Equations: none.
- Point / Path / Field role: none stated as Point/Path/Field. "Gait" = rotating B (field). The Hall "near the star / rotor" senses rotor position (:46).
- Magnetism / gravity / rotation link: :74 "All STAY after a walk. If Hall / rotor keeps a bias, hold+reinject is talking." Open (STAY) means retention.
- Open / parked: receipts 1–6.
- Conflicts: none. "Field explorer + Void checker" (:9) is the software naming collision noted at the top.

## HEAR_SEE: Hearing and vision (`09_TESTS/HEAR_SEE.md`)
- Gate / lifecycle: sense-organ design.
- Downstream / cites: BUCKET `senses.py`, `SPEAKER_BUILD.md`.
- Core claim: :21 "What leaves the eye is not a jpeg to Void. It is a lean candidate." :77 "Illegal: Vision model stamping engage."
- Equations: pseudocode at :52-54.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: Hall is an UP proprioception line (:12). Nothing else stated.
- Open / parked: none.
- Conflicts: none.

## 09 MAP: Layer 09 Tests (`09_TESTS/MAP.md`)
- Gate / lifecycle: "capability coverage is complete; physical test-file layout is not yet split" (:13).
- Upstream / Downstream: test files, `../00_RULES/update_rules.md`, `../10_RECEIPTS/generate_receipts.js`.
- Core claim: :11 "Every layer owns its tests. No eyeballing a waveform and calling it good."
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: magnetics tests are listed (:29).
- Open / parked: no `rules/` category exists.
- Conflicts: none.

## MOTOR_CELL_SPECS: Motor cell specs (`09_TESTS/MOTOR_CELL_SPECS.md`)
- Gate / lifecycle: F0 / F1 spec tables and pass numbers.
- Core claim: :21 "2N7000 is the bottleneck. Treat F0 as 80 mA class." :68 "Not a spec: Hover watts… PWM as hold."
- Equations: SS49E ~1.4 mV/G (:39).
- Point / Path / Field role: none stated. Hall "balance / where" (:39) is rotor-position sensing.
- Magnetism / gravity / rotation link: Hall read after the window. "Hall quiet / walk / STAY-after" (:63).
- Open / parked: F1.
- Conflicts: none.

## MOTOR_SENSOR_HEAD: Motor sensor head (`09_TESTS/MOTOR_SENSOR_HEAD.md`)
- Gate / lifecycle: design plus a pass description.
- Core claim: :3 "Every One-Wave winding / motor carries one puck." :65 "Puck does not stamp. Puck does not arm motors. Puck only UP."
- Equations: none.
- Point / Path / Field role: **Point (implicit):** "SS49E Hall on the bell … rotor where" (:22). No L is given.
- Magnetism / gravity / rotation link: :70 "STAY: vibe dies, Hall leftover optional." Balance is a pair of pucks (:40-51).
- Open / parked: PCB puck.
- Conflicts: none.

## NERVE_SENSE_FLIGHT: Nerve upgrade, eye, ear, mouth, flight (`09_TESTS/NERVE_SENSE_FLIGHT.md`)
- Gate / lifecycle: design plus build order (:112-118) and illegal claims (:122-128).
- Downstream / cites: `SPEAKER_BUILD.md`, BUCKET `loop.py`, `brain_2state.py`.
- Core claim: :78 "Lean +1 on a pair: one motor up, opposite down. STAY: hover clothes only." :89 "Field lists a lean, Void may refuse, FC does the fast inner loop."
- Equations: focus error (A+C)−(B+D). Tracking E−F (:29-30).
- Point / Path / Field role:
  - **Point (implicit):** the commercial FC "keeps the inner rate loop" (:84). The IMU is the "inner ear" (:78). Attitude rate is held externally.
  - Path and Field: none stated.
- Magnetism / gravity / rotation link: "gait / rotor: walk A B C or motor pair, DOWN rotate B" (:105). Gravity and hover are not linked to magnetism.
- Open / parked: flight is props-off only.
- Conflicts: none.

## NTC_BIAS_LIMITS: NTC bias current limits (`09_TESTS/NTC_BIAS_LIMITS.md`)
- Core claim: :10 target ΔT ≤ 0.3 °C. :45 "Treat any implied ΔT_sense > 0.5 °C as a wiring bug."
- Equations: ΔT = P/δ = I²R/δ (:5). P_max = δ × 0.3 K (:14). I ≈ 5/(R_fixed + R_ntc) (:27).
- Point / Path / Field role: none stated. Magnetism / gravity / rotation link: none stated.
- Open / parked: none.
- Conflicts: none.

## NTC_THERMAL_RUNAWAY: NTC thermal runaway (`09_TESTS/NTC_THERMAL_RUNAWAY.md`)
- Core claim: :3 "Two loops. Do not mix them." :30 "Void does not PWM a cooling cycle. It cuts engage. STAY is the cool-down."
- Equations: I ≈ 5 V / 20 k ≈ 0.25 mA (:17).
- Point / Path / Field role: none stated. Magnetism / gravity / rotation link: none stated (motor-cook loop :5 only).
- Open / parked: none.
- Conflicts: none.

## PART_DISCREPANCY_MATRIX: Part discrepancy matrix (`09_TESTS/PART_DISCREPANCY_MATRIX.md`)
- Gate / lifecycle: :3 "First record … not a claim that every line of every file was audited… Measured B-H is not claimed."
- Upstream / Downstream / cites:
  - Rules and bench files: `BENCH_REALITY_CONTRACT.md`, `js/bench-reality.js`, `01_PARTS/CELL_V1_PARTS_BOM.md`, `HEX_CELL_BOARD.md`, `PERFBOARD.md`, `js/board.js`, `js/components.js`, `07_MAGNETICS/SOLVERS.md`.
  - cell-v1 notes: `TRANSFLUXOR.md`, `PRIOR_ART_AND_TEST_TARGETS.md`, `MAGNETICS.md`, `PROVEN_PARTS_REFERENCES.md` R13, `OPTION_A_TOROID_THRESHOLD.md`, `USABLE_MEMORY_BENCH.md`, `HYSTERESIS_LOOP.md`, `LOG.md`.
  - Tests: regression-builds 22/23, and six test files: board-magnetic-parts, transfluxor-prior-art, magnetic-prior-art, cell-prior-art, triad3d, solver-triangulation.
- Core claim: :7 "±12 with a real 0 is not a historical leftover." :8 a TLE2426 on a dual-supply 0 is a MIXED_CENTER conflict. :16 square-loop facts: "Br stays… No idle fade. No release from saturation."
- Equations: L = AL·N², I = (V/R)(1−e^{−tR/L}) (:19).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link:
  - :13 "Equal turns, same sense, add. Opposite sense cancels."
  - :14 two sub-threshold currents together reach Br.
  - :16 square-loop remanence: no fade, no release. This is the model only, not a bench result.
- Open / parked (:23-27): BOM recount, 3D place/rotate, V_BUS reinjection, six-sector mismatch, tag-and-capture, diode PERMIT gate, round vs square law, and the blank `cell-v1/LOG.md`.
- Conflicts: none against canon. The internal conflict at :15 (Option A 0.10 V edge vs P1 0.45–0.55 V no-write) is recorded as "The conflict is the result."

## POSTER_CELL_MOTOR: Poster, cell plus 3-winding actuator (`09_TESTS/POSTER_CELL_MOTOR.md`)
- Core claim: :10 "Live one winding. Walk A-B-C rotates B. All STAY = hold."
- Equations: none.
- Point / Path / Field role: Field = rotating B. Point and Path: none stated.
- Magnetism / gravity / rotation link: STAY (open) = hold.
- Open / parked: none.
- Conflicts: none.

## POSTER_QUADRATIC_TOP: Quadratic plus top layer (`09_TESTS/POSTER_QUADRATIC_TOP.md`)
- Core claim: :17 "Override is Void cutting engage. It is not Gate-7. It does not stamp." :18 "Hold from the top is STAY on all windings plus leftover view state."
- Equations: none. "Oversight 6:1" (:7).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: Hall at the star is the first view device (:19).
- Open / parked: the memristor drops in later.
- Conflicts: none.

## SENSOR_CELLS: Sensor cells (`09_TESTS/SENSOR_CELLS.md`)
- Core claim: :23 "Output of a sensor cell is a Thought fragment: lean + live + 'ask engage'. It never stamps."
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: gate 2 is "balance: Hall or I vs the opposite cell" (:17).
- Open / parked: a three-analog board.
- Conflicts: none.

## SPEAKER_BUILD: Balanced One-Wave speaker (`09_TESTS/SPEAKER_BUILD.md`)
- Cites: `ONE_WAVE_CELL.md` (:30).
- Core claim: :3-6 "The cone is a winding pair… Hold = both phases STAY at mid → no DC in the coil → silence." :52 "Balanced pair cancels at the mid. Cone moves. Blue stays the reference."
- Equations: none (truth table at :18-24).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none beyond the coil drive. Open (STAY/STAY) = no current.
- Open / parked: audio PWM later.
- Conflicts: none.

## STEINHART_HART: Steinhart-Hart (`09_TESTS/STEINHART_HART.md`)
- Core claim: :15 "Void does not need 0.01 °C. It needs cooler / belt / hot."
- Equations: 1/T = A + B ln R + C (ln R)³ (:5). 1/T = 1/T0 + (1/β) ln(R/R0), with T0 = 298.15 K and β ≈ 3950 K (:11-13).
- Point / Path / Field role: none stated. Magnetism / gravity / rotation link: none stated.
- Open / parked: none.
- Conflicts: none.

## LATITUDE_LINUX_2026-10-05: Latitude Linux launch recovery (`10_RECEIPTS/LATITUDE_LINUX_2026-10-05.md`)
- Gate / lifecycle: :5 "replacement launch and model tests VERIFIED; old system-package removal BLOCKED."
- Core claim: :55 "Results prove implemented simulation behavior, not physical hardware qualification." The test counts are 49 / 80 / 26 / 23 builds, 100 checks (:44-52).
- Equations: none.
- Point / Path / Field role: none stated. Magnetism / gravity / rotation link: none stated.
- Open / parked: 1.0.0 removal is blocked (sudo blocklisted). Android not verified.
- Conflicts: none.

## PRACTICE_INTERFACE_2026-10-05: Human / AI practice interface receipt (`10_RECEIPTS/PRACTICE_INTERFACE_2026-10-05.md`)
- Gate / lifecycle: :114 "PARTIAL overall… DO NOT SCALE." Hard stop at :125.
- Upstream / cites: AGENTS.md, GENERAL_REFERENCE_RULES.md, AI_CANONICAL_START_HERE.md, One_Wave_Bench/BREADBOARD_CANONICAL_ARCHITECTURE.md, 11_INTERFACE/README.md, BENCH_REALITY_CONTRACT.md (:16-18).
- Core claim: :92-93 "Preserve electrical state on ordinary switch edits; do not reset capacitor/magnetic history." All scripts pass except ngspice, which is BLOCKED (:78).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: magnetic history is preserved across edits (:92-93). Nothing else stated.
- Open / parked: Electron smoke, screenshots, ngspice, CI, PR (:117-123).
- Conflicts: none.

## 10 README: Receipts (`10_RECEIPTS/README.md`)
- Core claim: :17-25 the generated receipts are gitignored. Permanence comes from the test suites staying green.
- Equations: none.
- Point / Path / Field role: none stated. Magnetism / gravity / rotation link: none stated.
- Open / parked: `regressions/` and `history/` are not automated. `circuit.test.js` has no structured records.
- Conflicts: none.

## SHOW_SOMEONE: What you can show (`10_RECEIPTS/SHOW_SOMEONE.md`)
- Cites: `experiments/brain_cell_001.json`, HEX-SPLIT `brain_2state.py`, `nerve_cell.py`.
- Core claim: :3 "Stage 1 VBB … passed a 5 V window-comparator cell. That is real. It is not CELL_V1." :19 "Until 1 is a receipt in this folder, the posters are maps."
- Equations: none.
- Point / Path / Field role: none stated. Magnetism / gravity / rotation link: none stated.
- Open / parked: four VBB stamps are still owed (:14-17).
- Conflicts: none.

## parts-workspace-regression-20261007: Parts workspace regression repair (`10_RECEIPTS/parts-workspace-regression-20261007.md`)
- Gate / lifecycle: :25 "RESOLVED scoped test regressions; broader engineering capability partial."
- Core claim: :14 "No physics or exit-status expectation weakened." :23-24 "not bench qualification".
- Equations: none (I_LED = 0.00933 A, V_anode = 1.912 V reported).
- Point / Path / Field role: none stated. Magnetism / gravity / rotation link: none stated.
- Open / parked: any solver change needs a fresh reference.
- Conflicts: none.

## solver-convergence: Solver convergence qualification receipt (`10_RECEIPTS/solver-convergence.md`)
- Core claim: an under-iterated diode must return `solver.converged === false` and emit `SOLVER FAILED:` (:10-12). GitHub Actions run 34672445791 passed (:14).
- Equations: none.
- Point / Path / Field role: none stated. Magnetism / gravity / rotation link: none stated.
- Open / parked: none.
- Conflicts: none.

## 11 MAP: Layer 11 Interface (`11_INTERFACE/MAP.md`)
- Cites: `../BUILDS/MAP.md`, `../00_RULES/architecture.md`.
- Core claim: :5-8 "The UI … does not own the physics… never make the UI compensate."
- Equations: none.
- Point / Path / Field role: none stated. Magnetism / gravity / rotation link: none stated.
- Open / parked: preset functions in `js/app.js` should move to BUILDS/ (:32-37).
- Conflicts: none.

## VISIBLE_AI_RUN: Visible AI / practice runs (`11_INTERFACE/VISIBLE_AI_RUN.md`)
- Cites: `INDEX_VISIBLE_RUN_WIRES.md`, `js/visible-run*.js`, `main.js`, `visible.js`, `experiments/visible_led_demo.json`.
- Core claim: :3-5 an AI test should open on screen. Headless mode stays available for CI.
- Equations: none.
- Point / Path / Field role: none stated. Magnetism / gravity / rotation link: none stated.
- Open / parked: none.
- Conflicts: none.

## 3D_CIRCUITRY_WORK_REGISTER: Virtual Breadboard 3D Circuitry Work Register (`3D_CIRCUITRY_WORK_REGISTER.md`)
- Gate / lifecycle: :3 "Status: OPEN. This is a task register, not a claim of completed implementation." Two P0 boxes are checked. Everything else is open.
- Cites: CELL_V1_CURRENT_BUILD_CANON.md, `09_TESTS/PART_DISCREPANCY_MATRIX.md`, `07_MAGNETICS/SOLVERS.md`, `js/triad3d.js`, `cell-v1/LOG.md`, and the test files.
- Core claim:
  - :21 "Do not present lumped mutual inductance as a spatial Bx/By/Bz field solver."
  - :22 "No energy-gain claims."
  - :28 "Require real bench calibration before labeling magnetic memory … or spatial field behavior validated."
  - :34 "Do not retune either solver so the numbers match."
- Equations: I = V / (1 + N·length·0.0531), with a 2 A clamp (:43).
- Point / Path / Field role: none stated. Field (spatial Bx/By/Bz) is explicitly not built (:21, :55).
- Magnetism / gravity / rotation link:
  - "Place/rotate" here means editor geometry rotation (:17, :24, :74). It is not physical rotation.
  - Remanence model: "Br stays… idle does not fade, and saturation does not release" (:47). This is the model only.
  - Lattice: "lattice layers" geometry is wanted (:15), and the "seven-cell flower" is deferred (:29). This is a board layout, not the bound-lattice physics.
- Open / parked (:49-56, :68-75): P0 audit, round vs square law, BOM, 3D editor, measured hysteresis, Bx/By/Bz, energy-gain claim, packaging, and figure-8 threshold reconciliation.
- Conflicts: none.

---

## Slice summary

**(a) Files in the slice that bear on Point, Path, Field, rotation, magnetism, gravity, inertia, mass, resistance, or lattice / locking.** No node IDs exist in this slice. Each line names the file and how it bears.

- **ROTATING_FIELD.** Field: the rotating B vector, made by the A→B→C three-phase walk, steps 120° per seq. Point is implicit only: "core / rotor … keeps an orientation". Open (STAY, drive dies) plus remanence = hold. Closed (live winding) = torque.
- **CELL_V1_POSTER / POSTER_CELL_MOTOR / FULL_SYSTEM_BUILD.** Same rotating-B claim. "Rotating B is gait". "Reinjection is proprioception". STAY = hold.
- **CELL_V1_MOTOR_IS_TERNARY.** Hardware open/closed made explicit:
  - STAY = both FETs OFF = high-Z (open winding) = hold.
  - ±1 = closed winding loop through the star = torque, "shaft may twitch".
  - Shorting the star to a rail is not hold.
- **SPINTRONICS_LOOP.** "DOWN spin" = winding current / torque / step. "UP spin" = location / phase / Hall angle (rotor Point state, sensed). There is no L = Iω.
- **REINJECT_MIN_POWER.** STAY (open) = near-zero drive. Leftover B (remanence / rotor / MEM) carries the state. "FC holds attitude." PWM-to-hold is a fail.
- **ROTATIONAL_HOLD_TEST.** Magnetic closure is gated: "Do not close active magnetic reinjection" until the four receipts pass. A lumped sim is not a 3-D field proof.
- **MOSFET_BODY_DIODE / REVERSE_RECOVERY.** "Do not close a magnetic feedback loop until those five traces exist." A coil can integrate Irr and fake flux memory.
- **DC_AC_RC_CYCLE.** BREAK = "loop intentionally opened". Remanent field after drive removal is only a magnetic-hold candidate.
- **DC_AC_RC_SPHERE.** Path in state space: "Walk A→B→C is rotation in the AC plane". The DC / AC / RC triad is *not* Point / Path / Field.
- **07 MAP / SOLVERS / 05 MAP / 3D_CIRCUITRY_WORK_REGISTER / PART_DISCREPANCY_MATRIX.** Field is not implemented spatially: Bx/By/Bz is MISSING and there is no curl. The magnetics are lumped L_ij or Σ H·l = NI plus a square-loop Br model (no fade, no release). The two solvers' figure-8 thresholds disagree. There are no energy-gain claims.
- **MOTOR_SENSOR_HEAD / MOTOR_CELL_SPECS / SENSOR_CELLS.** Point position is sensed only: Hall on the bell = "rotor where".
- **NERVE_SENSE_FLIGHT.** The attitude rate loop is delegated to a commercial FC, with the IMU as the "inner ear". Lean = differential motor pair.
- **CELL_V1_WORKING_PATH.** "Not gravity." This explicitly keeps magnetism / electrical work separate from gravity.
- **THE_SYSTEM.** "views up and torque down as the same crossing."
- **04 MAP.** Magnetic core remanence through time is PASSING as a lumped damped relaxation.
- **Mass, inertia, resistance (in the canonical "mass / organization" sense), and bound-lattice locking.** None stated in any slice file. "Lattice layers" and "seven-cell flower" in the work register are board geometry only.

**How the build implements Point / Path / Field (overall):**
- **Point:** not modeled. The rotor or shaft orientation is only sensed (Hall / encoder / IMU), and attitude is held by an external FC. There is no I, ω or L anywhere in the slice.
- **Path:** only as a sequence walk A→B→C (state-space "rotation in the AC plane") and as an electrical conduction path. There is no ride / orbit with "no L" bookkeeping.
- **Field:** a lumped magnetic model (mutual inductance; Σ H·l = NI mesh in the separate V3DE). The "rotating B" is the three-phase-stepped field direction. There is no spatial field and no curl.
- The three rates are therefore **not separated** in the hardware or sim docs. By the canonical rule this description is incomplete. No file claims a separation.

**How the build implements magnetic open/closed (overall):**
- **Open:** STAY = both FETs OFF = high-Z winding, drive current dies. Retention (remanence, rotor reluctance) must survive this to count as hold or memory.
- **Closed:** the live ±1 winding carries current through the star = torque / step.
- **Closing a magnetic feedback / reinjection loop is forbidden** until sense-only receipts pass (MOSFET_BODY_DIODE:71, ROTATIONAL_HOLD_TEST:56, :68, SAFE_BRINGUP P10, WORKING_PATH:94).
- **No file states the canonical dL/dt = 0 (open) / dL/dt = −γL (closed) law.** Any mapping of electrical open/closed to the canonical magnetic open/closed is unstated and should not be assumed.

**(b) Conflicts found.**
- **Against the canonical rules: none direct.** No file has magnetism becoming gravity, an expansion / scale factor, an exception to L bookkeeping, or gravity affecting point rotation. CELL_V1_WORKING_PATH:3 says "Not gravity."
- **Tensions (not hard contradictions):**
  1. **ROTATING_FIELD:3-4, :14 and CELL_V1_POSTER:3.** The rotating *field* is made the carrier of state, and "torque / spin" is tied to the same flip. There is no Point / Path / Field separation, which canon calls incomplete. Field curl is "neither", but here the field rotation carries state.
  2. **SPINTRONICS_LOOP:9-10.** "Spin" is overloaded (drive and sensed rotor state). It is not L = Iω.
  3. **REINJECT_MIN_POWER:8.** "state for free" risks being read as an energy / L exception. It is mitigated by :36 and by the no-energy-gain disclaimers (07 MAP:41, work register :22).
- **Terminology collisions** (flag only): "Field / Void" is software explorer / checker. "Reinjection" is local leftover-B / electrical reconnect, not E-530. "G" is the electrical mid-rail.
- **Internal build-doc tensions (not canon):**
  - CELL_V1_FULL:74-81 treats the motor as a "second machine". CELL_V1_MOTOR_IS_TERNARY:3, :39 says "Not a second machine".
  - The TLE2426 F0 path conflicts with the ±12 V real-0 star (PART_DISCREPANCY_MATRIX:7-8).
  - Option A 0.10 V edge vs P1 0.45–0.55 V no-write (PART_DISCREPANCY_MATRIX:15).
  - Three unreconciled figure-8 thresholds (SOLVERS:38-44).

**(c) Cross-references outside this slice that matter for point rotation or magnetism:**
- **Builds repo files:**
  - `Builds/Virtual_Breadboard/03_ELECTRICAL_CORE/G_SPINE.md`. It is in the 03 directory but **not in the slice list**. I read it: G is the spine, I_0 is vagus, "Reinjection lives in the cell (leftover B), not as charge stored in the spine".
  - `CELL_V1_FULL_BUILD.md`, `CELL_V1_CURRENT_BUILD_CANON.md`, `LOCKED_CELL_TOPOLOGY_DC_AC_MIRRORED_GATES.md`, `ONE_WAVE_CELL.md`, `BENCH_REALITY_CONTRACT.md`, `HEX_CELL_BOARD.md`, `PERFBOARD.md`.
  - `cell-v1/` notes: `MAGNETICS.md`, `TRANSFLUXOR.md`, `HYSTERESIS_LOOP.md`, `OPTION_A_TOROID_THRESHOLD.md`, `USABLE_MEMORY_BENCH.md`, `PROVEN_PARTS_REFERENCES.md`, `PRIOR_ART_AND_TEST_TARGETS.md`, `LOG.md` (blank).
  - `Virtual_3D_Electronics/js/{circuit,magnetics,parts,physics}.js`, `00_RULES/physics_rules.md`, `00_RULES/architecture.md`, `00_RULES/update_rules.md`.
- **HEX-SPLIT / BUCKET software:** `nerve_cell.py`, `brain_2state.py`, `senses.py`, `loop.py`.
- **One-Wave-Science files cited:** AGENTS.md, AI_CANONICAL_START_HERE.md, GENERAL_REFERENCE_RULES.md, One_Wave_Bench/BREADBOARD_CANONICAL_ARCHITECTURE.md (from PRACTICE_INTERFACE receipt).
- **No canonical node** (C-306, C-307, G-749, G-769, A-115, E-528, E-530, etc.) is cited by any slice file.
