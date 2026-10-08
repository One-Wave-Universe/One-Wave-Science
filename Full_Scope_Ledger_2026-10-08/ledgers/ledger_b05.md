# Ledger b05 — Builds repo (Virtual_Breadboard tail, WORK_BOARD, algorithms/, cad/, cell-v1/ A–H)

Slice: 41 files, all read in full (2,919 lines). Repo read: /home/user/Builds (read-only, no edits).

Global note for this slice: these are hardware/architecture documents for CELL_V1 and the Algorythm-Zer0 grammar. None of them carries a physics Point/Path/Field rate model, an L = I omega, a dL/dt law, a gravity law, or an open/closed magnetic-gradient rule. Where "POINT / PATH / FIELD" appears, the build docs define it as a **scale ladder** (larger coupled organization), not as three separate rates. That definitional difference is recorded as a conflict wherever it appears.

---

## Virtual Breadboard — Solver convergence contract   (`/home/user/Builds/Virtual_Breadboard/SOLVER_CONVERGENCE.md`)
- Gate / lifecycle: implemented contract (qualification test included, L21).
- Upstream: `Circuit.solve()`. Downstream / cites: `diagnose()`; SPICE_PARITY P1 item 2.
- Core claim: "must never silently accept an unfinished fixed-point state as a valid physical answer" (L3); `converged` true only when device state and linear system both converge (L7).
- Equations: `residualTolerance = absTolerance + relTolerance * maxEquationScale` (L13); residual from `A*x - b` (L12).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated (lists "core" state in L8 only as a nonlinear device state).
- Open / parked / not-set items: SPICE-style controls are "future" (L19).
- Conflicts: none.

## Virtual Breadboard — SPICE-parity upgrade ladder   (`/home/user/Builds/Virtual_Breadboard/SPICE_PARITY.md`)
- Gate / lifecycle: P1–P5, items 1–20 all marked IMPLEMENTED; acceptance rule L56-58.
- Upstream: MNA core. Downstream / cites: `js/spice-analysis.js`, `js/ac-analysis.js`, `js/bode-analysis.js`, `test/pole-zero-sanity.test.js`, `test/ngspice-crosscheck.test.js`, `test/ngspice-tolerances.json`.
- Core claim: "No feature is considered SPICE-grade because the waveform looks right" (L58); "One-Wave-specific hardware primitives stay above the generic electrical solver; they do not get hard-coded into the MNA mathematics" (L58).
- Equations: resonance `1/(2*pi*sqrt(L*C))` (L38); `H(jw)=Vout/Vin` (L37); RELTOL/VNTOL/ABSTOL defaults 1e-3, 1e-6 V, 1e-12 A (L32).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: "toroid/mutual-inductance and magnetic-memory models" in baseline (L15); "Toroid/magnetic-core integration remains on its existing dedicated dynamics" (L52). No rotation/gravity.
- Open / parked / not-set items: BJT not full Gummel-Poon (L43); MOSFET is not BSIM (L44); MOSFET/BJT ngspice parity explicitly not claimed (L54).
- Conflicts: none.

## G-744 Ternary cell — Stage 1 Real Millivolt Ternary physical build sheet   (`/home/user/Builds/Virtual_Breadboard/STAGE1_PHYSICAL_BUILD.md`)
- Gate / lifecycle: bench build sheet from `presetStage1TernaryParts()` (L3-7); Stage 1 only (L198).
- Upstream: simulator preset, button "Ternary cell (G-744)" (L5); README "Ternary cell (G-744)" section (L92). Downstream / cites: "Cal H" for group memory / toward-away neighbor coupling (L200).
- Core claim: window comparator (TLV3202) around V0 = 2.500 V with ±20 mV window, MEM output ~2.5 / 5.0 / 0 V for Hold / Right / Left (L172-180).
- Equations: none (expected voltages table only).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: group memory and neighbor coupling not covered (L198-201); SMD parts need breakouts (L39-49); ±40 mV lean source not a buyable part (L50).
- Conflicts: none with physics canon. Internal Builds tension: uses resistor dividers (R1-R4, L21-24) and an IC comparator as the decision element, against `CELL_V1_2026-09-28_CORRECTION.md:38` (no resistors in functional path), `BREADBOARD.md:14`, `CORES.md:59` and `IMPLEMENTATION_STATUS.md:112,119` (no comparator bank / hidden arbiter). It is a simulator-preset bench aid, not CELL_V1 hardware.

## Builds Work Board   (`/home/user/Builds/WORK_BOARD.md`)
- Gate / lifecycle: all items unchecked; P4 physical backend "Blocked until relevant CELL primitives have bench receipts" (L64).
- Upstream: none. Downstream / cites: `maps/ANIMATOR_PRODUCT_MAP.md`, `maps/CELL_V1_CONCEPT_MAP.md`, `maps/ANDROID_CELL_TO_CORTEX_MAP.md`, `maps/DIGITAL_CELL_TWO_STATE_BRAIN_LADDER.md`; work IDs W-001…W-404.
- Core claim: "Detailed scientific simulation work remains in One-Wave-Science" (L3); "Work is promoted by evidence, not by completion text" (L71).
- Equations: none.
- Point / Path / Field role: none stated (W-015 "common Field/Void state + receipt schema", L19, is Field/Void, not Point/Path/Field).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: every W item open.
- Conflicts: none.

## Algorythm-Zer0 — Presentation Authority   (`/home/user/Builds/algorithms/ALGORITHM_ZERO_PRESENTATION.md`)
- Gate / lifecycle: "Presentation-ready conceptual architecture. Implementation path remains open." (L3).
- Upstream: none. Downstream / cites: `FOUR_BRANCHES_AND_UNIVERSAL_RULES.md`, `thresholds.md`, `LEAN_INTO_ZER0.md`, `algorithm_zero_locked_canon.json` (L236-246).
- Core claim: four branches X Control / Y Structure-Rotation / Z Depth / T Time (L15-20); `L1 ⊂ … ⊂ L6` (L40); "the baseline moves" (L102); "Zer0 must not be presented as software memory for CELL_V1" (L179).
- Equations: `+ <-> (0) <-> -` (L59); `(0)t -> interaction -> consequence -> resolve -> (0)t+1` (L107); `6 × 6 × 6 × 6 = 1,296` (L144).
- Point / Path / Field role: none stated. Y branch is "STRUCTURE / ROTATION … axis, orientation, topology" (L18) — grammar vocabulary, no rate or L.
- Magnetism / gravity / rotation link: none stated beyond the Y branch label.
- Open / parked / not-set items: L212-222 (executable semantics, mapping, conflict resolution, physical binding, timing, completeness proof).
- Conflicts: none with physics canon. Internal: JSON canon vocabulary disagrees with this file for X and Y levels (L234-239).

## Algorythm-Zer0 — 42-term canon, four branches and Universal Rules   (`/home/user/Builds/algorithms/FOUR_BRANCHES_AND_UNIVERSAL_RULES.md`)
- Gate / lifecycle: all 15 rules "LOCKED" (L17-31).
- Upstream: none. Downstream / cites: used by FOUR_FIVE_SIX.md.
- Core claim: 21 Field + 21 Void per branch, 168 total (L7-9); Rule 11 "Two-of-three coherence… If it can't, HOLD" (L27); Rule 14 "Cost can't be externalized" (L30); Rule 15 Operator M4 "Express, Compress, Route" (L31).
- Equations: `Σk=1..6 k = 21` (L7-8); `Next State = T6(X1..6 ⊗ Y1..6 ⊗ Z1..6 ⊗ T1..5) → (0)t+1` (L99).
- Point / Path / Field role: none stated. Y-branch terms include AXIS, CLOCKWISE/COUNTERCLOCKWISE, ROTATE/STABILIZE/REVERSE, TRAJECTORY, ROUTE (L56-61) — vocabulary only. FIELD here means "active interactions" (L19), not field curl.
- Magnetism / gravity / rotation link: none stated (Z-L6 harmonic LOCK/SYNCHRONIZE/ENTRAINMENT/RESONANCE, L77, are vocabulary, no locking physics).
- Open / parked / not-set items: calibration columns "Domain-specific"/"Threshold-dependent" (L21, L27).
- Conflicts: none with physics canon. Note: Y-V6 term `EXPANSION` (L61) is a grammar primitive, not cosmological expansion; flag only to prevent misreading against the no-expansion rule.

## Algorythm-Zer0 — Implementation Status   (`/home/user/Builds/algorithms/IMPLEMENTATION_STATUS.md`)
- Gate / lifecycle: "architecture defined; implementation unresolved" (L3).
- Upstream: presentation docs. Downstream / cites: CELL_V1 mapping (L52).
- Core claim: no verified end-to-end implementation (L17); smallest demonstrator steps (L27-36); physical experiment must have "no software variable, comparator bank, or op-amp state machine perform[ing] the hidden decision" (L112).
- Equations: none.
- Point / Path / Field role: none stated. Candidate interfaces include "structural orientation", "direction", "magnitude", "hysteresis / retained bias" (L56-63), declared "not established" (L65).
- Magnetism / gravity / rotation link: precedents "multi-aperture hysteretic cores / transfluxors for history-dependent shared magnetic paths"; "magnetic majority / current-summing elements" (L84-85) — "not one-to-one matches" (L90).
- Open / parked / not-set items: whole physical mapping; failure tests L116-120; RC terminology unreconciled (L124).
- Conflicts: none.

## Zer0 and the lean — not memory   (`/home/user/Builds/algorithms/LEAN_INTO_ZER0.md`)
- Gate / lifecycle: rule file.
- Upstream: Zer0 canon. Downstream / cites: `lean_weight.py` (L11).
- Core claim: "Memory is the lean still in the path after the signal has passed" (L3); "If the pair is powered down long enough for the magnetic / analog state to fade, that number is a lie" (L11).
- Equations: none.
- Point / Path / Field role: none stated ("path" here = the physical signal path holding the lean).
- Magnetism / gravity / rotation link: magnetic/analog state fade (L11) only.
- Open / parked / not-set items: none.
- Conflicts: none.

## Rabbit Hopping — algorithm card   (`/home/user/Builds/algorithms/RABBIT.md`)
- Gate / lifecycle: external repo card.
- Upstream: none. Downstream / cites: github.com/One-Wave-Universe/RABBIT-HOPPING (L12).
- Core claim: reversible packet `(source_rank N, center T, wrapper W)` (L3); "Arithmetic is the artifact. Nested Point/Path/Field physics is tagged hypothesis, not a grant claim." (L14).
- Equations: none.
- Point / Path / Field role: only L14 — Point/Path/Field physics explicitly tagged hypothesis and kept out of the grant claim.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: P/P/F physics parked as hypothesis.
- Conflicts: none.

## Algorithms folder README   (`/home/user/Builds/algorithms/README.md`)
- Gate / lifecycle: index.
- Upstream: none. Downstream / cites: the five Zer0 files; `../cell-v1/PRIOR_ART_AND_TEST_TARGETS.md` (L12); RABBIT.md.
- Core claim: "Memory in the proposed CELL_V1 architecture is the retained lean / hysteretic state in the physical path" (L24).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: JSON canon conflict unreconciled (L16-18); no end-to-end implementation (L36).
- Conflicts: none.

## Software is not the body   (`/home/user/Builds/algorithms/SOFTWARE_IS_NOT_THE_BODY.md`)
- Gate / lifecycle: rule file.
- Upstream: One-Wave-Science `software-zer0` (L5). Downstream / cites: `LEAN_INTO_ZER0.md`, `cell-v1/NOT_SOFTWARE.md` (L14).
- Core claim: "The algorithm is the three analog differentials. DA, DB, DC. Same path computes and remembers." (L9); "If the pair is powered down and the iron forgets, the software log is a lie" (L12).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: "the iron forgets" (L12) — remanence fade only.
- Open / parked / not-set items: none.
- Conflicts: none.

## Algorythm-Zer0 — thresholds and gate bands   (`/home/user/Builds/algorithms/thresholds.md`)
- Gate / lifecycle: LOCKED, derived from xlsx (L3).
- Upstream: `Algorythm-Zer0-System-Rules-Thresholds-Variables-Transformations-LOCKED.xlsx`. Downstream / cites: none.
- Core claim: seven relational bands (L9-15); "Gaps between named bands are intentional transition regions and must not be auto-filled" (L17); commitment scale −3, −2, 0, +2, +3 (L25-29).
- Equations: `42 × 4 = 168` (L42).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none with physics canon. Internal: commitment scale omits ±1 (L25-29) while CELL.md:207-213 has ±1/±2/±3.

## CAD README   (`/home/user/Builds/cad/README.md`)
- Gate / lifecycle: KiCad "not in this folder yet" (L7).
- Upstream: none. Downstream / cites: `cell0_schematic.svg`, `the_cell.svg`, `../cell-v1/BREADBOARD.md`, `cell0.net`.
- Core claim: SVG drawings are the available drawings (L7).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: KiCad project.
- Conflicts: none.

## Ternary windings — motors and actuators   (`/home/user/Builds/cell-v1/ACTUATORS.md`)
- Gate / lifecycle: candidate, "subject to bench validation" (L14).
- Upstream: CELL_V1 decision. Downstream / cites: V_BUS.
- Core claim: "The actuator is not a second brain. It is the outer field expression of the same CELL_V1 decision." (L3); two plain round toroids, six windings 3+3 (L7-14).
- Equations: none.
- Point / Path / Field role: none stated. (State map: UP/PUSH, DOWN/PULL bias the field; FLIP "reverse the resolved axis relation", L21-25.)
- Magnetism / gravity / rotation link: motor field driven by the windings; HOLD/PASS "permit inductive return" (L24). No L, no open/closed rule.
- Open / parked / not-set items: torque, efficiency, field strength, recovery not claimed (L41).
- Conflicts: none.

## C-317 / C-321 analogy — not the grant mechanism   (`/home/user/Builds/cell-v1/ANALOGY.md`)
- Gate / lifecycle: analogy only (title).
- Upstream: One-Wave-Science **C-317 Boundary-Tension Weave**, **C-321** "three equal tensions meet at 120°" (L11). Downstream / cites: none.
- Core claim: "three diffs = three vortices. Hex 120°. Bus-side lattice + figure-8 = the tension skin" (L13); quark→vortex phase, gluon→tension-link, confinement→knot lock, proton→three-vortex knot, skin→σ_T (L5-9).
- Equations: none (σ_T named).
- Point / Path / Field role: none stated (vortex used as analogy, no rate assignment).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: whole analogy is outside the grant mechanism (L15).
- Conflicts: none.

## Analog networks vs this cell   (`/home/user/Builds/cell-v1/ANALOG_NN.md`)
- Gate / lifecycle: comparison note; "Us (already locked)" (L23).
- Upstream: none. Downstream / cites: none.
- Core claim: "One-cell memory = figure-eight shape on the middle. Group memory = skin on the shared edge. Two agrees = Kirchhoff" (L26-28).
- Equations: none.
- Point / Path / Field role: none stated ("Field" header L3 = research field).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## Choice bands   (`/home/user/Builds/cell-v1/BANDS.md`)
- Gate / lifecycle: band table.
- Upstream: CELL.md scale. Downstream / cites: `BANDS.png`.
- Core claim: "Seven live bands, ten wide. Six dead zones, five wide… 7×10 + 6×5 = 100" (L3); "Hold is 0.45–0.55 and it is live, not off" (L17).
- Equations: `7×10 + 6×5 = 100` (L3).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## Bidirectional gates   (`/home/user/Builds/cell-v1/BIDIR.md`)
- Gate / lifecycle: design note.
- Upstream: CELL. Downstream / cites: none.
- Core claim: each axis A/B/C is a back-to-back MOSFET path (L3-9); "FLIP is … one bidirectional flip — the same pair conducting the other way" (L23); "PASS = both ways off, collapse to V_BUS" (L25).
- Equations: none.
- Point / Path / Field role: none stated. Views read "CENTER / figure-8 / lattice Br" (L17).
- Magnetism / gravity / rotation link: lattice Br (remanence) is a view source (L17).
- Open / parked / not-set items: isolated-body FET "later" (L9).
- Conflicts: none with physics canon. Internal: views named BASELINE · DELTA · HEADING · RESULT (L15) vs REFERENCE, CHANGE, DIRECTION, RESULT in FOUR_BRANCHES:44 and FOUR_FIVE_SIX:22.

## Breadboard — minimum validation fixture   (`/home/user/Builds/cell-v1/BREADBOARD.md`)
- Gate / lifecycle: validation fixture, "not the final CELL_V1 geometry" (L3); "Change one thing -> test -> compare -> record" (L65).
- Upstream: CELL.md. Downstream / cites: none named.
- Core claim: "No resistor bias ladder is part of this fixture or architecture" (L14); retained-state write/probe test (L38-46); falsification tests: moving-reference boundedness, triadic coherence, sector mismatch (L72-96).
- Equations: `D = V(+) - V(-)` (L21).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: retained magnetic state after opposite writes (L38-46); "Magnetic-majority behavior is a candidate precedent, not a locked CELL mechanism" (L86); sector perturbed "thermally or magnetically" (L89).
- Open / parked / not-set items: retained-state premise must be revised if not distinguishable (L46).
- Conflicts: none with physics canon. Internal: CELL0.md uses resistor drain loads R1/R2 (CELL0:21-22).

## Bus-side lattice   (`/home/user/Builds/cell-v1/BUS_LATTICE.md`)
- Gate / lifecycle: Phase-II measurement question (L24).
- Upstream: CELL. Downstream / cites: none.
- Core claim: "V_BUS is the shared circulation / readiness / reinjection rail of the lattice" (L3); lattice state "is the coupled result of many cells' local retained state, gate leans, outer fields, returned energy, and neighbor interactions" (L22).
- Equations: none.
- Point / Path / Field role: none stated ("circulation" L3 is energy-rail circulation, not path rotation).
- Magnetism / gravity / rotation link: "not a single magnetic loop living on the bus" (L22).
- Open / parked / not-set items: collective behavior unmeasured (L24).
- Conflicts: none with physics canon. Internal: "two outer round figure-8 field structures" (L13) contradicts CELL.md:266 / CORES.md:11 ("common outer/body pair is not figure-8"); "one square figure-8 nucleus" per cell (L11) contradicts square = motor-control only (CELL.md:30, CELL_CURRENT.md:20,25).

## V_BUS state   (`/home/user/Builds/cell-v1/BUS_STATE.md`)
- Gate / lifecycle: anti-drift rule file.
- Upstream: CELL. Downstream / cites: none.
- Core claim: "V_BUS is not the muscle-memory store" (L3); "External supply replaces losses; recovered energy does not create energy" (L17); redline → prefer PASS, no new PUSH/FLIP (L27-29).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: sensing/threshold hardware is an implementation detail (L17).
- Conflicts: none.

## CELL — canonical CELL_V1 lock (authority)   (`/home/user/Builds/cell-v1/CELL.md`)
- Gate / lifecycle: "This file is the CELL_V1 authority. Detail files must agree with it." (L281); 2026-09-27 lock section supersedes older wording (L430-432); many items OPEN / BENCH.
- Upstream: none. Downstream / cites: all cell-v1 detail files.
- Core claim: hex of six tapered magnetic sectors A+ B+ C+ A− B− C− (L7); "CENTER / (0) is the shared active virtual-ground reference… balanced/confirmed, not OFF" (L9); "3 mirror gates = 1 loop = 1 flip" (L314); motor nucleus = transfluxor/multi-aperture mechanism class (L322).
- Equations: `OLD retained state + NEW incoming excitation -> shared magnetic transition -> NEXT retained state` (L327); recursive law `current difference -> action -> thresholded remainder -> reinjection correction toward balance -> changed retained hysteretic path -> bias on next difference` (L491-496).
- Point / Path / Field role: "**Scale:** POINT → PATH → FIELD = larger coupled organization. Scale promotion is not the same thing as moving from A to B to C." (L248); "POINT/PATH/FIELD are scale states and must not be collapsed into A/B/C." (L274). A live differential "may oscillate / circulate around CENTER while carrying a net lean" (L250). No rate, no L, no curl. Hardware has no point-rotation element.
- Magnetism / gravity / rotation link: "core / winding hardware is 2D / planar. The resulting magnetic field is inherently 3D" (L48); hysteretic body-state layer (L66-91); motor nucleus history dependence (L322-330). No open/closed magnetic gradient rule; no gravity. Y-mirrors CLOCKWISE/COUNTERCLOCKWISE not used here.
- Open / parked / not-set items: layer material/thickness/coercivity (L79); exact MOSFET (L317); body-state reference distribution (L439); base-to-base extra gate (L455); gate-local hysteresis implementation (L462); falsification list (L507-513).
- Conflicts: **L248, L274** define POINT/PATH/FIELD as a scale ladder ("larger coupled organization", "scale states"), whereas canon (G-749, G-769, C-319/C-320) defines Point / Path / Field as three separate rates (point rotation with L = I omega; path ride with no L; field curl). Different meaning under the same names. Internal: L33 "M4 is not a separate nucleus or cell role" vs CELL_V1_2026-09-28_CORRECTION.md:6 and CELL_ASSEMBLED.md:19.

## CELL-0 — primitive mirror + magnetic hold   (`/home/user/Builds/cell-v1/CELL0.md`)
- Gate / lifecycle: test plan T1–T6, logged in LOG.md (L65-72).
- Upstream: CELL. Downstream / cites: `REINJECT_BUS.md` (L13), `LOG.md`.
- Core claim: "`D = DB − DC` is the lean in the path"; "CENTER holds that lean (core on CENTER)"; loss goes to DC bus (L11-13); T5 "rails off: leftover field on the core matches last D sign" (L71).
- Equations: `D = DB − DC` (L11).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: square-loop memory/magamp ferrite on CENTER (L25) holds the lean as remanence (L71).
- Open / parked / not-set items: C_BUS added only after T5 (L49).
- Conflicts: none with physics canon. Internal: R1/R2 10k drain resistors and R3/R4 100k gate resistors (L21-30) vs CORRECTION.md:38 "No resistors in the intended CELL functional path" (R1/R2 are functional drain loads). Also "core on CENTER" (L12, L25) vs CELL_CURRENT.md:48 "The nucleus is the only bridge".

## Cell — assembled   (`/home/user/Builds/cell-v1/CELL_ASSEMBLED.md`)
- Gate / lifecycle: "proposed topology. `LOG.md` remains the hardware evidence gate" (L5); Phase-I bench gate L84-93.
- Upstream: CELL.md. Downstream / cites: LOG.md.
- Core claim: nucleus specialization by role (L17-21); "Their combined 3D magnetic field is the current candidate for the cell's local body-state field" (L47).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: two plain round toroids = FIELD/VOID interface, combined 3D magnetic field = local body-state field candidate (L47); domain-wall hysteretic layer (L49). No open/closed rule.
- Open / parked / not-set items: L97 full list (material, coupling, fade law, torque, retention…); "A separate literal sphere is not locked" (L51).
- Conflicts: none with physics canon. Internal: L19 "M4 cell -> dedicated two-pyramid / double-triangle nucleus" vs CELL.md:33.

## CELL current (2026-10-04)   (`/home/user/Builds/cell-v1/CELL_CURRENT.md`)
- Gate / lifecycle: "This file is the cell… It does not replace a measurement" (L3); "Nothing here has been measured" (L30).
- Upstream: `LOCK.md` (followed over `GRANT.md`, L20). Downstream / cites: `ALL_GITHUB_INTO_THREE.md` (L18), `DIFFERENTIALS.md` (corrected, L46); repos Builds, One-Wave-Science, Bench, Bridge-Comand, Mythos-and-Stories, One-Wave-Universe.
- Core claim: "`ALL_GITHUB_INTO_THREE.md` parks Rabbit Hopping, Hex Split, **Point Spin**, **Grav Lab**, and the Great Galactic Library under Science. They were not used to rewrite the cell." (L18). Axis assignments: A = heat (vertical), B = gyro and vibration, **C = "the magnetic gradient only. C+ against C−. A uniform field cancels. The lean is the difference."** (L36-38).
- Equations: none.
- Point / Path / Field role: none stated. B axis senses gyro rate (L37) — a rotation-rate sensor channel, not a point-rotation/L element. Point Spin explicitly parked out of the cell (L18).
- Magnetism / gravity / rotation link: C axis is a gradiometer differential (Förster pair instrument form, L38) — measures magnetic gradient, uniform B cancels. No open/closed or dL/dt rule. Gravity (Grav Lab) parked out (L18).
- Open / parked / not-set items: L54 (materials, turns, coupling, thermal fade, write depth, torque, recovery fraction).
- Conflicts: none with physics canon. Internal: L46 "base to base… is not a second differential. This corrects… `DIFFERENTIALS.md`" — DIFFERENTIALS.md:72-74 and HELMHOLTZ.md:57 still say differential surface.

## Three differentials diagram   (`/home/user/Builds/cell-v1/CELL_DIAGRAM.md`)
- Gate / lifecycle: diagram.
- Upstream: CELL0. Downstream / cites: none.
- Core claim: "Cell-0 is one of these. The cell at law is three." (L3); "Two-of-three reads those three D's. V_BUS never substitutes for CENTER." (L44).
- Equations: `D_A = DA+ − DA-`, `D_B`, `D_C` (L39-41).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: core A/B/C at + seats; "A- is the other end of core A. Not a second core." (L35-37).
- Open / parked / not-set items: none.
- Conflicts: none with physics canon. Internal: three separate cores A/B/C (L35) vs six-sector single hex (CELL.md:7); CENTER tied to V0 (L28).

## CELL_V1 authority correction 2026-09-28   (`/home/user/Builds/cell-v1/CELL_V1_2026-09-28_CORRECTION.md`)
- Gate / lifecycle: dated correction superseding contradictory M4 wording (L3); interface OPEN / BENCH (L11).
- Upstream: CELL.md. Downstream / cites: DOMAIN_WALL_FLOWER.md lists it as parent.
- Core claim: M4 = dedicated routing cell role, BASE ⇄ TIP ⇄ TIP ⇄ BASE (L6-10); "FIELD outer toroid ⇄ center nucleus/brain ⇄ VOID outer toroid… proposed Helmholtz-like coupling. Coupled cells may produce a larger distributed magnetic field. This is a hypothesis" (L23-25); permalloy Ni80Fe20 (L35); no resistors in functional path (L38).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: Helmholtz-like opposed toroid coupling, larger distributed magnetic field (hypothesis, L25); memory hierarchy short / mid / long (L33).
- Open / parked / not-set items: interface (L11), material (L35).
- Conflicts: none with physics canon. Internal: supersedes CELL.md:33.

## Two choices, three moves   (`/home/user/Builds/cell-v1/CHOICES_AND_MOVES.md`)
- Gate / lifecycle: rule file.
- Upstream: CELL. Downstream / cites: none.
- Core claim: choice = FIELD or VOID; moves = A, B, C differentials; "HOLD is not a third choice" (L16).
- Equations: `A = DA = A+ − A−`, `B = DB`, `C = DC` (L23-25).
- Point / Path / Field role: "POINT / PATH / FIELD at larger scale is not an alias for A/B/C." (L36) — again a scale reading.
- Magnetism / gravity / rotation link: none stated ("Same iron", L49).
- Open / parked / not-set items: none.
- Conflicts: L36 uses POINT/PATH/FIELD as "larger scale" (same scale-ladder definition as CELL.md:248), not the canon three-rate definition.

## Cores   (`/home/user/Builds/cell-v1/CORES.md`)
- Gate / lifecycle: rule file; bench quantities open (L57).
- Upstream: CELL. Downstream / cites: none.
- Core claim: common two plain round toroids + role-specific nucleus (L3-11); "planar / 2D hardware… magnetic fields are inherently 3D" (L49); "No comparator may become the hidden state machine" (L59).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: sensor nucleus "two opposed lobes carry the local retained magnetic history" (L17); M4 nucleus two triangular loops base-to-base (L29). No open/closed rule.
- Open / parked / not-set items: isolation, coupling, material, turns, field strength, retention, torque (L57).
- Conflicts: none with physics canon. Internal: M4 nucleus "base-to-base" (L29) vs CORRECTION.md:8 "Inside one cell: TIP ⇄ TIP".

## Memristor crossbars   (`/home/user/Builds/cell-v1/CROSSBAR.md`)
- Gate / lifecycle: comparison note.
- Upstream: none. Downstream / cites: none.
- Core claim: "We do not have (i,j) synapses. We have edges… Lattice hysteresis on that side is supposed to be common. That is group memory, not a sneak error." (L25).
- Equations: none (Ohm × Kirchhoff in prose, L5).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## DC / AC / RC   (`/home/user/Builds/cell-v1/DC_AC_RC.md`)
- Gate / lifecycle: rule file.
- Upstream: Zer0 Rule 12. Downstream / cites: none.
- Core claim: DC = committed flow, "Void"; **AC = "Drive across the dead zone… The turn." → "Field rotation"** (L10); lattice DC = brain reinjection loop; "Helmholtz, if built, is uniform bias. Scars stay in the hysteresis layer." (L35).
- Equations: none.
- Point / Path / Field role: AC is labelled "Field rotation" (L10) and step 2 "AC drive. Field rotates. D walks." (L52). This is the only file in the slice that assigns rotation to "Field". No point-rotation or path-ride role.
- Magnetism / gravity / rotation link: "Collapse still goes through the square figure-8 onto the lattice DC loop… the write into the shared hysteresis layer" (L44).
- Open / parked / not-set items: none.
- Conflicts: **L10, L52** "Field rotation / Field rotates" — canon: field curl is neither point rotation nor path ride; calling the AC excursion a field rotation blurs the three-rate split (Field here is the Zer0 FIELD side, but the wording collides with canon). Internal: L44 square figure-8 in the collapse path generally, and round figure-8 as "the differential / ternary side" (L43), vs square = motor-control-cell nucleus only (CELL.md:30).

## Differentials   (`/home/user/Builds/cell-v1/DIFFERENTIALS.md`)
- Gate / lifecycle: rule / proposal file.
- Upstream: CELL. Downstream / cites: DC_AC_RC.md; corrected by CELL_CURRENT.md:46.
- Core claim: "The lean is the three differentials… not their average" (L11-19); "Memory is that lean, held in the path" (L134).
- Equations: `DA = A+ − A−`, `DB`, `DC` (L14-16); `D = DB − DC`; `Idiff = Iss · tanh(Vd / (2 · n · Vt))` (L44-45).
- Point / Path / Field role: "POINT/PATH/FIELD belongs to larger scale organization and is not an alias for A/B/C" (L106). "Live orbit / lean": opposed sides "exchange / circulate current while the net difference stays near zero. A bias shifts that live orbit" (L100-102) — electrical circulation, not path ride.
- Magnetism / gravity / rotation link: "A three-phase motor is three of these differences timed around the hex" (L118). No magnetic open/closed.
- Open / parked / not-set items: none.
- Conflicts: L106 scale-ladder definition of POINT/PATH/FIELD (same as CELL.md:248). Internal: L72-74 neighbor joint "one differential surface" contradicted by CELL_CURRENT.md:46; L115 HOLD defined by D inside 0.45–0.55 mixes band axis with D.

## Domain-wall muscle memory — whole flower   (`/home/user/Builds/cell-v1/DOMAIN_WALL_FLOWER.md`)
- Gate / lifecycle: must-measure list (L50-59); Phase-I one layer (L46).
- Upstream: HEX_LATTICE.md, LATTICE_STRAIN_AND_MEMORY.md, FLOWER.md, CELL_V1_2026-09-28_CORRECTION.md (L7). Downstream / cites: none.
- Core claim: "One hysteretic sheet under all seven connected cells… A write on a shared edge is already a write on the neighbor" (L3); "Local nucleus Br = this cell's last lean. Sheet wall pattern = body's habit" (L29-30); "FIELD (nucleus flip) writes VOID (sheet). VOID biases the next FIELD flip." (L32).
- Equations: none.
- Point / Path / Field role: none stated (the "path" is the groove/route the flower walked, L27).
- Magnetism / gravity / rotation link: domain walls in permalloy moved by current/field, held by remanence (L25); "Every cell wears the same two plain-round Helmholtz-like body rings" (L11). No open/closed rule; this is the closest "shared organization" mechanism (one sheet couples all cells) but nothing on rate locking.
- Open / parked / not-set items: retention τ, crosstalk, localization (L52-58).
- Conflicts: none.

## The loop (EIGHT)   (`/home/user/Builds/cell-v1/EIGHT.md`)
- Gate / lifecycle: rule.
- Upstream: none. Downstream / cites: none.
- Core claim: "The new views are the last actions plus the consequence sent up… RESULT / send-up becomes BASELINE of the next pass." (L5, L9).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## Energy learns with the trace   (`/home/user/Builds/cell-v1/ENERGY_LEARN.md`)
- Gate / lifecycle: proposal ("honest sentence for a grant", L42).
- Upstream: none. Downstream / cites: none.
- Core claim: "The same hysteresis that is memory is the efficiency" (L3); "A full reversal (FLIP against Br) is a big loop. A PUSH that is already on that heading is a minor loop" (L5); "The remanence is the bias that saved you the extra volt" (L26).
- Equations: loop area `∮ H·dB` (L5).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: magnetic hysteresis loop size sets energy cost; deep heading = remanent offset.
- Open / parked / not-set items: none stated (unmeasured).
- Conflicts: none.

## Flower   (`/home/user/Builds/cell-v1/FLOWER.md`)
- Gate / lifecycle: rule.
- Upstream: none. Downstream / cites: parent of DOMAIN_WALL_FLOWER.
- Core claim: "The letters are the edges" (L3); 12 shared sides (L17); "All connected cells are the distributed intelligence. No supervisor. No polling. No clock." (L19).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: "The square figure-8 runs those sides: bus and lattice together" (L17).
- Open / parked / not-set items: none.
- Conflicts: none with physics canon. Internal: L17 square figure-8 runs the bus and lattice, vs BUS_LATTICE.md:5 ("V_BUS… is not the square figure-8 nucleus") and square = center motor nucleus only (CELL.md:149).

## Minor hysteresis and flux linkage   (`/home/user/Builds/cell-v1/FLUX_LINKAGE.md`)
- Gate / lifecycle: explanatory.
- Upstream: none. Downstream / cites: none.
- Core claim: "linked and kept → trace (hysteresis of the settled cell); linked and released → charge on the bus. Same λ. Two fates." (L29-32); major loop = FLIP, minor loop = habit (L11-17).
- Equations: `λ = NΦ` (L3); `v = dλ/dt` (L5); energy `∫ i dλ` (L5); `∮ H·dB` (L11).
- Point / Path / Field role: none stated. ("one Φ path around the 8", L23 — magnetic flux path.)
- Magnetism / gravity / rotation link: kept vs released flux linkage is the build's only "kept / released" magnetic split; it is about remanence vs flyback energy, not the canon open (dL/dt = 0) / closed (dL/dt = −γL) gradient rule.
- Open / parked / not-set items: none.
- Conflicts: none.

## Four, five, six   (`/home/user/Builds/cell-v1/FOUR_FIVE_SIX.md`)
- Gate / lifecycle: cell reading of Zer0 levels 4–6.
- Upstream: `algorithms/FOUR_BRANCHES_AND_UNIVERSAL_RULES.md` (L5). Downstream / cites: `cell-v1/SEVEN.md` (L86).
- Core claim: 4 views / 4 actions, 5 states / 5 scale, 6 nested recursion and "the hex that carries it" (L81-85); scale hardware reading "cell → cube → Rubik → two Rubiks → the body they make" (L54).
- Equations: `1 ⊂ 2 ⊂ 3 ⊂ 4 ⊂ 5 ⊂ 6` (L75).
- Point / Path / Field role: "POINT / PATH / FIELD stay scale language. They are not aliases for A, B, C." (L57).
- Magnetism / gravity / rotation link: none stated beyond "one shared hysteresis layer" (L77).
- Open / parked / not-set items: further memory scale only if one layer cannot keep two habits (L77).
- Conflicts: L57 scale-language definition of POINT/PATH/FIELD (vs canon three separate rates).

## Both ways (GATES)   (`/home/user/Builds/cell-v1/GATES.md`)
- Gate / lifecycle: 2026-09-27 lock section (L43-49); extra boundary gate OPEN / BENCH (L49).
- Upstream: CELL. Downstream / cites: none.
- Core claim: A/B/C bidirectional spatial axes, seven-band strength scale, ±3 protection regions (L5-33); "CHOICE/PIVOT/FLIP remain separate gate/control functions. POINT → PATH → FIELD remains a separate scale relation." (L35).
- Equations: none (band table only).
- Point / Path / Field role: L35 scale relation.
- Magnetism / gravity / rotation link: "Views up on the 8. Collapse still to V_BUS." (L41).
- Open / parked / not-set items: device/topology (L48); boundary gate (L49).
- Conflicts: L35 scale-relation definition of POINT/PATH/FIELD.

## Shared Helmholtz field   (`/home/user/Builds/cell-v1/HELMHOLTZ.md`)
- Gate / lifecycle: "Not locked as measured… open build claim. Bench has to earn it." (L5-7); build after Cell One (L75-77).
- Upstream: CORRECTION.md (Helmholtz-like). Downstream / cites: none.
- Core claim: Helmholtz pair gives "approximately uniform B" common bias volume (L11-13); "Shared weather and shared scars are different jobs" (L36); fail if it "walks CENTER into the bus, erases retained state, or forces every cell to the same lean" (L71).
- Equations: none (coil spacing ≈ one radius, L13).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: uniform B (zero gradient by design) as shared bias; "Uniform bias is a bad scar map" (L34). Does not say what a uniform/zero-gradient field does to rotation; no open/closed rule.
- Open / parked / not-set items: all bench numbers (L63-69).
- Conflicts: none with physics canon. Internal: L57 "That joint stays a differential surface" vs CELL_CURRENT.md:46.

## Hex bus architecture   (`/home/user/Builds/cell-v1/HEX_BUS.md`)
- Gate / lifecycle: proposal.
- Upstream: none. Downstream / cites: Rabbit addressing (L52); Red Blob Games cube coords (L21).
- Core claim: three separate shared structures (axis bus, hysteretic layer, power bus) plus local CENTER (L3-7); "Sharing V_BUS is how the lattice couples readiness without coupling memory" (L75); "Sag is a feature" (L79).
- Equations: `q + r + s = 0` (L18).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: "Honeycomb magnetic lattices… Different job" (L25). None otherwise.
- Open / parked / not-set items: none stated.
- Conflicts: none with physics canon. Note: L75 "CENTER is per-cell… Sharing CENTER would short every lean together" vs CELL.md:127 "Shared virtual-ground bus" across A/B/C within a cell — consistent at cell level, but HEX_BUS also says "(or per-axis)".

---

## Slice summary

### (a) Node IDs / chapters bearing on Point, Path, Field, rotation, magnetism, gravity, inertia, mass, resistance, lattice organization, locking
- **G-744 (Ternary cell)** — STAGE1_PHYSICAL_BUILD.md:5,92. Window-comparator ternary; no rotation/magnetism. "Cal H" cited for neighbor coupling (L200).
- **C-317 Boundary-Tension Weave**, **C-321 three equal tensions at 120°** — ANALOGY.md:11. Hex 120° tension skin as lattice-cohesion analogy; explicitly not the grant mechanism. No rate content.
- **M4 operator / M4 routing cell** — FOUR_BRANCHES:31; CELL.md:32-39; CORRECTION.md:5-11; CORES.md:25-37. Routing geometry (tip-to-tip / base-to-base); lattice organization, not rotation.
- **Algorythm-Zer0 Y branch "Structure / Rotation"** — vocabulary only (AXIS, CLOCKWISE/COUNTERCLOCKWISE, ROTATE/STABILIZE/REVERSE, TRAJECTORY, ROUTE); no physics.
- **Z branch L6 HARMONIC (LOCK, SYNCHRONIZE, ENTRAINMENT)** — vocabulary only; no rate-locking physics.
- **CELL.md (authority)** — POINT → PATH → FIELD defined as scale (L248, L274); magnetic layer / transfluxor history (L66-91, L322-330); 2D hardware, 3D field (L48).
- **CELL_CURRENT.md** — Point Spin and Grav Lab parked under Science, not used for the cell (L18); C axis = magnetic gradient differential, uniform field cancels (L38); B axis = gyro rate (L37).
- **DC_AC_RC.md** — AC = "Field rotation" (L10, L52).
- **FLUX_LINKAGE.md / ENERGY_LEARN.md** — flux "kept" (remanence) vs "released" (flyback to V_BUS); major vs minor hysteresis loops.
- **DOMAIN_WALL_FLOWER.md / HEX_BUS.md / BUS_LATTICE.md** — lattice organization: one shared hysteretic sheet couples all seven cells; V_BUS couples readiness, not memory.
- **HELMHOLTZ.md / CORRECTION.md** — shared uniform-B bias volume (hypothesis); FIELD/VOID toroids Helmholtz-like.
- **RABBIT.md** — "Nested Point/Path/Field physics is tagged hypothesis, not a grant claim" (L14).
- "Resistance" appears only as electrical resistors (STAGE1, CELL0, CORRECTION:38) and Zer0 T-L2 term `RESISTANCE` (FOUR_BRANCHES:89); none relates to resistance = mass / organization. Inertia, mass, angular momentum: not mentioned anywhere in the slice.

**How the build hardware implements Point / Path / Field:** it does not implement them as three rates. Build docs consistently treat POINT / PATH / FIELD as a **scale-promotion ladder** (CELL.md:248,274; CHOICES_AND_MOVES:36; DIFFERENTIALS:106; FOUR_FIVE_SIX:57; GATES:35), kept separate from A/B/C axes, the seven strength bands, and CHOICE/PIVOT/FLIP. No hardware element carries point rotation or L = I omega; no element is designated as path ride; no element is designated as field curl. The nearest hardware items are: B-axis gyro rate sensing (CELL_CURRENT:37), live "orbit"/circulation of current around CENTER (DIFFERENTIALS:100-102, CELL.md:250), and AC called "field rotation" (DC_AC_RC:10). RABBIT.md:14 and CELL_CURRENT:18 explicitly keep Point/Path/Field physics and Point Spin out of the build/grant.

**How the build hardware implements magnetic open / closed:** not stated. No file uses open/closed magnetic gradient, dL/dt = 0, or dL/dt = −γL. Nearest items: C axis as a magnetic-gradient differential where uniform field cancels (CELL_CURRENT:38); Helmholtz pair as deliberate uniform (zero-gradient) bias (HELMHOLTZ:11-13,34); flux "linked and kept" (remanence) vs "linked and released" (flyback to V_BUS) (FLUX_LINKAGE:29-32); major vs minor hysteresis loops (FLUX_LINKAGE:11-17, ENERGY_LEARN:5); transfluxor / multi-aperture shared-flux history (CELL.md:322, IMPLEMENTATION_STATUS:84). Gravity: none in the hardware; Grav Lab parked (CELL_CURRENT:18).

### (b) Conflicts found
Against canonical physics rules:
1. POINT / PATH / FIELD redefined as a scale ladder, not three separate rates — CELL.md:248, CELL.md:274, CHOICES_AND_MOVES.md:36, DIFFERENTIALS.md:106, FOUR_FIVE_SIX.md:57, GATES.md:35.
2. "Field rotation" / "Field rotates" for the AC excursion — DC_AC_RC.md:10, DC_AC_RC.md:52 (canon: field curl is neither point rotation nor path ride).
(No file states anything about L bookkeeping, gravity, expansion, redshift, or magnetism-becoming-gravity, so no conflicts there. FOUR_BRANCHES:61 term `EXPANSION` is a grammar word, not cosmology.)

Internal Builds inconsistencies (not physics canon, recorded for completeness):
3. Base-to-base joint: "not a second differential" (CELL_CURRENT.md:46) vs "differential surface" (DIFFERENTIALS.md:72-74, HELMHOLTZ.md:57).
4. M4: "not a separate nucleus or cell role" (CELL.md:33) vs dedicated role/nucleus (CORRECTION.md:6, CELL_ASSEMBLED.md:19); M4 nucleus base-to-base (CORES.md:29) vs TIP ⇄ TIP inside (CORRECTION.md:8).
5. Square figure-8 scope: motor-control only (CELL.md:30, CELL_CURRENT.md:20,25) vs per-cell / bus-and-lattice (BUS_LATTICE.md:11, FLOWER.md:17, DC_AC_RC.md:44); outer pair "round figure-8" (BUS_LATTICE.md:13) vs "not figure-8" (CELL.md:266, CORES.md:11).
6. Resistors in functional path: CELL0.md:21-30 and STAGE1_PHYSICAL_BUILD.md:21-25 vs CORRECTION.md:38 and BREADBOARD.md:14.
7. Comparator as decision element: STAGE1 TLV3202 vs IMPLEMENTATION_STATUS.md:112,119 and CORES.md:59.
8. View names: BIDIR.md:15 (BASELINE · DELTA · HEADING · RESULT) vs FOUR_BRANCHES.md:44 / FOUR_FIVE_SIX.md:22 (REFERENCE, CHANGE, DIRECTION, RESULT).
9. Commitment scale −3/−2/0/+2/+3 (thresholds.md:25-29) vs ±1/±2/±3 (CELL.md:207-213).
10. Zer0 JSON vocabulary vs human-readable canon (ALGORITHM_ZERO_PRESENTATION.md:234-239, algorithms/README.md:16).
11. Three separate cores A/B/C (CELL_DIAGRAM.md:35-37) vs one six-sector hex (CELL.md:7); core on CENTER (CELL0.md:12,25) vs "nucleus is the only bridge" (CELL_CURRENT.md:48).

### (c) Cross-references outside the slice that matter for point rotation or magnetism
- `ALL_GITHUB_INTO_THREE.md` — parks **Point Spin** and **Grav Lab** under Science (cited CELL_CURRENT.md:18). Primary pointer for where point-rotation and gravity work lives.
- `LOCK.md`, `GRANT.md` (Builds) — square vs round figure-8 dispute (CELL_CURRENT.md:20).
- `cell-v1/HEX_LATTICE.md`, `cell-v1/LATTICE_STRAIN_AND_MEMORY.md` — parents of domain-wall sheet (lattice organization / strain).
- `cell-v1/PRIOR_ART_AND_TEST_TARGETS.md` — transfluxor / magnetic-majority precedents.
- `cell-v1/REINJECT_BUS.md`, `cell-v1/LOG.md`, `cell-v1/SEVEN.md`, `cell-v1/NOT_SOFTWARE.md`.
- One-Wave-Science **C-317**, **C-321** (ANALOGY.md:11); One-Wave-Science `software-zer0` (SOFTWARE_IS_NOT_THE_BODY.md:5).
- RABBIT-HOPPING repo (Point/Path/Field physics tagged hypothesis).
- Virtual Breadboard README "Ternary cell (G-744)" section and "Cal H" (STAGE1:92,200); VB toroid/mutual-inductance and magnetic-memory models (SPICE_PARITY.md:15,52).
