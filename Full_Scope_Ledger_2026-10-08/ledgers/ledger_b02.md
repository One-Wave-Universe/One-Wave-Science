# Ledger b02 — Builds repo slice (35 files, all read in full)

Repo: `/home/user/Builds`. Every file below was read in full with line numbers (`cat -n`). Line numbers cite the file in question.
Note on method: the Builds docs are hardware/software build docs. Most do not use the canonical Point/Path/Field or open/closed-magnetism vocabulary. Where a doc is silent I write "none stated". Where I add an observation that is mine and not the doc's, it is marked **[observation]**.

---

## Miniverse — self-loop README   (`Miniverse/README.md`)
- Gate / lifecycle: runnable software prototype (`self_loop.py`, `test_self_loop.py`).
- Upstream: boot contract. Downstream / cites: `Miniverse/room3d/README.md`, `Miniverse/desktop/README.md`, `Miniverse/EXPAND_MINIVERSE.md`, Hive Pipe AI bridge.
- Core claim: "Permission is the contract, not a chat prompt." (L3). DROP / LOCAL / HOLD / FORWARD routing (L10-13); "Baseline Zero generation stays `0` inside this loop" (L14). Room binds one MUD state to a "37-cell stationary hex lattice" (L20).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none stated.
- Conflicts: none.

## Miniverse — desktop app   (`Miniverse/desktop/README.md`)
- Gate / lifecycle: install/runtime instructions for GTK3 + WebKitGTK laptop shell.
- Upstream: Jetson room server on 127.0.0.1:8787. Downstream / cites: `install_laptop.sh`.
- Core claim: SSH local forward laptop 18787 -> Jetson 8787 (L7-12); Jetson stays loopback-only, "Do not bind it to `0.0.0.0`" (L14-15); closing the app leaves Jetson state unchanged (L50-51).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## Miniverse — Experiment Lab   (`Miniverse/room3d/EXPERIMENT_LAB.md`)
- Gate / lifecycle: software ledger; evidence levels SIMULATION / CROSS-CHECK / VIRTUAL BREADBOARD / PUBLIC DATA ANALYSIS / PHYSICAL BENCH (L177-192); "Never promote one level to another without the corresponding evidence." (L194).
- Upstream: Miniverse 37-cell topology. Downstream / cites: Hive Pipe `python_run`, `cpp_compile_run`, Virtual Breadboard, CERN, GWOSC.
- Core claim: `lattice_pulse` "mixes each cell toward the mean of its legal neighbors and applies retention" (L29-30); claim boundary "not evidence that a physical One-Wave lattice exists" (L41-42). `reference_recovery`: "A scalar perturbation relaxing toward Baseline Zero" (L46).
- Equations: none written as formulas; parameters amplitude, coupling, retention, steps (L20-27); perturbation, retention, steps, tolerance (L50-56).
- Point / Path / Field role: none stated. (Neighbor-mean spreading is a graph signal, explicitly not physics.)
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: new experiment types follow a 10-step branch-step (L157-168).
- Conflicts: none.

## Miniverse — Lattice Body Physics Sandbox   (`Miniverse/room3d/LATTICE_BODY_PHYSICS.md`)
- Gate / lifecycle: "reduced software sandbox" governed by **D-412** (L3, L41).
- Upstream: D-412. Downstream / cites: M4, body sensor lattice (L16), CELL_V1 (L41).
- Core claim: a body on a lattice cell "contributes a bounded software mass/load derived from its voxel body volume and scale. The occupied lattice site displaces under that load. Neighbor coupling spreads the disturbance and creates derived strain and pressure." (L6). Boundary: "not evidence for a physical gravity law, particle model, or physical CELL_V1 mechanism" (L41).
- Equations (L32-35, verbatim):
  `neighbor restoring = stiffness * (neighbor_mean_u - u)`
  `acceleration = -body_load + neighbor_restoring - damping * v`
  `v_next = retention * (v + acceleration * dt)`
  `u_next = u + v_next * dt`
  State: u, v, `chi` "compression proxy", pressure, strain, load (L21-26).
- Point / Path / Field role: Field-side only: chi = "compression proxy", strain = "neighbor displacement differential", pressure (L23-25). No Point rotation, no Path.
- Magnetism / gravity / rotation link: "weight signal" and "software mass" are sensory values (L13-14); explicitly not a gravity law (L41). No rotation.
- Open / parked / not-set items: "Parameters are simulation controls and must remain independently testable." (L41).
- Conflicts: none. It uses `chi` and mass but disclaims gravity, so it does not contradict g = -alpha K_L grad chi. **[observation]** The `- damping * v` and `retention` terms are decay on lattice displacement, not on L. They should not be read as the closed-magnetism dL/dt = -gamma L.

## Miniverse — 3D Sandbox Room   (`Miniverse/room3d/README.md`)
- Gate / lifecycle: "software coordination/runtime prototype. It does not prove a physical One-Wave lattice." (L115-116).
- Upstream: Miniverse handoff (seven neighborhoods, L15). Downstream / cites: `EXPAND_MINIVERSE.md`, `EXPERIMENT_LAB.md`, `One_Wave_Bench/App_Center/Composite_Agent_Lab/AI_COUNCIL_PROTOCOL.md` (L121), Three.js.
- Core claim: "radius-3 triangular/hex lattice with 37 cells and six edge directions: A+, B+, C+, A-, B-, C-. The lattice does not move when an agent moves. Each AI/human body carries its current cell, facing, mirror state, and scale." (L10-13). "stationary-lattice + moving-active-frame software contract" (L116-117). Council: "M4 is chair/body state, Void is admin/inner oversight, Field is the sole outward voice/action" (L121).
- Equations: none.
- Point / Path / Field role: none stated in canonical terms. **[observation]** "facing" (L12) is a body attitude, and moving cell to cell is a route. Neither is tied to L or to a rate. "Drag to orbit" (L89) is the camera UI.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: "later lattice binding" (L5).
- Conflicts: none.

## ONE — compact cell summary   (`ONE.md`)
- Gate / lifecycle: compact build card.
- Upstream: none cited. Downstream / cites: repo URL only.
- Core claim: "Hex sandwich. Three differentials star to CENTER. Figure-8 (two square ferrites) *is* that CENTER — views up, actions down, 4×4 at the cross. Heavy-metal / copper strip under the 8 and under the hex bus lattice writes. Hex edges wear a magnetic skin (Permalloy / ferrite) so the lattice holds Br." (L6). "Two-of-three current-sum (1.5 / 1.2, GAP wait) permits PUSH/FLIP on heading windings. Those windings *are* the actuator. Hysteresis is the settled whole loop. Minor loop = cheap habit." (L6). Nodes "V_TOP · CENTER · V_BUS — never one pour." (L9).
- Equations: thresholds 1.5 / 1.2 only.
- Point / Path / Field role: none stated in canonical terms. Hardware: the magnetic skin on hex edges holds remanence Br (lattice memory). Heading windings are the actuator.
- Magnetism / gravity / rotation link: magnetism = retained Br / hysteresis as memory (L6, L18). No gravity, no point rotation.
- Open / parked / not-set items: "Pack only on ask." Buy list staged (L15).
- Conflicts: (intra-Builds) L15 "Then LM339 + 4066" contradicts `RULES.md` L29 "No op-amp. No LM339." and L18b "No comparators." No canonical-physics conflict.

## Origin and provenance   (`ORIGIN_AND_PROVENANCE.md`)
- Gate / lifecycle: authorship statement.
- Upstream: Git history (commits dated 2026-09-21, L15-22). Downstream / cites: COPYRIGHT.md, LICENSE, NOTICE, CITATION.cff, CLA.md.
- Core claim: CELL_V1 "originated and developed by **Mark Wright Adlard Adlard / One-Wave-Universe**" (L5). Records "magnetic/toroidal structures, mirrored differential gates, ternary lean, bus/reinjection system, motor-field geometry" (L7). Makes no claim to "pre-existing physical laws, standard electronic components" (L38).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: mentions "motor-field geometry" and "magnetic/toroidal structures" only as topics (L7).
- Open / parked / not-set items: none.
- Conflicts: none.

## PRINT — the cell   (`PRINT.md`)
- Gate / lifecycle: printable one-page cell card.
- Upstream / Downstream: none cited.
- Core claim: "Figure-8 square ferrite is the home (views up / actions down). Heavy-metal strip under the 8 and under the hex bus lattice writes. Lattice edges hold Br. ... Two-of-three permits PUSH/FLIP. Same windings can throw. Hysteresis is the settled loop." (L4). Three nodes V_TOP, CENTER, V_BUS (L7). Cell-0 breadboard: 9 V V_TOP, 2N7000 pair, 10k drains / 100k gates, CENTER wire through ferrite (L13).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: lattice edges hold Br (magnetic memory). Nothing on gravity or rotation.
- Open / parked / not-set items: none.
- Conflicts: (intra-Builds) L13 uses designed resistors (10k drains, 100k gates) on the Cell-0 bench. `RULES.md` L29 bans designed resistors only in the "CELL control, threshold, CENTER, or reinjection architecture", so this is a bench-fixture tension, not a definite conflict.

## Proposed Android Brain — Overview   (`Proposed_Android_Brain/00_Book_Overview.md`)
- Gate / lifecycle: "YELLOW proposed build / no consciousness claim" (L4).
- Upstream: Proposed One-Wave Consciousness book (L8). Downstream / cites: **G-721, G-721a, G-721b–G-721e, G-722, G-723, E-510–E-514** (wheel system), `-1(0)+1` (L22-28).
- Core claim: modules Dream Engine, M4 Weighing Service, Administrator, Reference Ground, Working Ground (L12-16). "These layers may exchange references but must not be collapsed into one mechanism." (L31). "No module gets unilateral irreversible control" (L35).
- Equations: none.
- Point / Path / Field role: none stated in canonical terms. G-721a–e are "route or rail candidates" (L24), i.e. route/path scheduling. E-510–E-514 "wheel system: harmonic and movement relation" (L27).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: everything is a proposal (L6).
- Conflicts: none.

## Proposed Android Brain Ch01 — Functional Runtime Architecture   (`Proposed_Android_Brain/Ch01_Functional_Runtime_Architecture.md`)
- Gate / lifecycle: PROPOSED BUILD (L3).
- Upstream: Ch00. Downstream / cites: **G-721, G-721a–e, G-722, G-723**, Gate 5 / Gate 6 (L65), Jetson mapping (L21-27).
- Core claim: "All gate relationships are duplex." (L17). Symbolic route: "word or cue -> G-721 mirrored alphabet coordinate path -> live -1(0)+1 branch choice -> ... G-722 procedural-memory ... -> wheel/body movement translation -> sensory correction" (L37-43). "A Fibonacci validator mismatch may stop or flag an exact programmed route. It may not force the body to continue" (L58). Commit only when "Gate 5 state report matches Gate 6 acceptance" (L63-65). "12:1 maximum imbalance is a proposed engineering ceiling, not a derived biological constant" (L78).
- Equations: none.
- Point / Path / Field role: "the wheel system translates route information into live movement geometry" (L54). That is route (Path) going to body movement. No L, no field curl.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: the 12:1 ceiling is unmeasured. Tests 1-6 (L90-95).
- Conflicts: none.

## Proposed Android Brain Ch02 — Body Interface and Hierarchical Control   (`Proposed_Android_Brain/Ch02_Body_Interface_and_Hierarchical_Control.md`)
- Gate / lifecycle: PROPOSED BUILD.
- Upstream: **C-312**, the existing Android Body book (L5). Downstream / cites: **D-411** (L25).
- Core claim: hierarchy local units -> 3:1 aggregation -> chains -> central -> fan-out (L10-14). "A 3:1 nerve aggregation ratio is not the 3:1 planar mirrored-axis count in D-411, and a 6:1 oversight ratio is not automatically sixfold lattice geometry." (L25).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: 3:1, 6:1 and 12:1 ratios "remain proposed design values until measured" (L25). Consciousness test definition "does not yet exist" (L29).
- Conflicts: none.

## Proposed Android Brain Ch03 — Hybrid Procedural Memory   (`Proposed_Android_Brain/Ch03_Hybrid_Procedural_Memory_and_Subconscious_Movement.md`)
- Gate / lifecycle: PROPOSED BUILD / SIMULATION REQUIRED (L3).
- Upstream: G-722 by content (Boltzmann + Hopfield). Downstream / cites: none by ID.
- Core claim: "Boltzmann proposes candidate movement patterns -> Hopfield settles ... -> local choice accepts, holds, counters, or redirects" (L20-22). "The zero state is active hold/reference, not absence." (L35). "Binary logic can allow, block, stop, isolate, or override. It is not the source of normal movement." (L39).
- Equations: `c_i ∈ {-1,0,+1}` (L31-33).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: six first experiments (L64-69). Failure conditions (L73).
- Conflicts: none.

## Proposed Android Brain Ch04 — Sequence Routing and Spectral Stability   (`Proposed_Android_Brain/Ch04_Sequence_Routing_and_Spectral_Stability.md`)
- Gate / lifecycle: PROPOSED BUILD / YELLOW CANDIDATES.
- Upstream: G-721a–e content (Fibonacci, Sturmian, episturmian, Arnoux-Rauzy, Plastic/Padovan, L11-15), G-723 content (Pisot/Salem/Mahler, L31). Downstream / cites: none by ID.
- Core claim: "These words schedule or validate route-family attention. They do not directly command actuator position." (L17). "three route axes correspond to six directed movements around one center. The `3:1` axis-pair view and `6:1` directed-neighbor view describe different counts of the same local geometry." (L27). "Elegant number theory does not promote a movement architecture." (L54).
- Equations: `Δq_t = c_t d_{x_t}, c_t ∈ {-1,0,+1}` (L24).
- Point / Path / Field role: route families are Path-like (directed step on a route axis). No Point rotation or Field.
- Magnetism / gravity / rotation link: none stated. "unit-circle rhythm" (L31) is a spectral term, not physical rotation.
- Open / parked / not-set items: Deninger, Rodriguez-Villegas and elliptic dilogarithms are held downstream (L37). Required benchmark (L41-50).
- Conflicts: none.

## Builds — root README   (`README.md`)
- Gate / lifecycle: index.
- Upstream: none. Downstream / cites: `validation/SCIENCE_CONNECTIONS.md`, `cell-v1/`, `cell-v1/CELL.md`, GRANT.md, RULES.md, THE_BUILD.md, provenance files.
- Core claim: "This editor/solver remains reality-first and hypothesis-independent; links do not imply validation." (L2).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## CELL_V1 Real-World Build Handoff   (`REAL_WORLD_BUILD_HANDOFF.md`)
- Gate / lifecycle: outside-review / builder handoff. Proposed; "all unmeasured performance remains open" (L686).
- Upstream: RULES.md locks. Downstream / cites: established precedents: transfluxors, magamps, majority logic, multiphase windings, flyback/DC-link, artificial spin ice, domain-wall tracks, core memory, fluxgate (L557-569).
- Core claim: CELL_V1 = nucleus + two mirrored body loops FIELD and VOID + A/B/C axes + six wedge routes + live CENTER + V_BUS + one domain-wall hysteretic body-state layer + event thresholds (L15-24). "tip-to-tip = intra-cell differential routing / base-to-base = inter-cell lattice routing" (L116-117). Route: "neighbor cell -> base-to-base shared face -> wedge body -> tip-to-tip local differential relation -> local brain / CENTER-referenced resolution -> opposite wedge -> base-to-base into next cell" (L131-139). "The two round FIELD/VOID toroids create a 3D magnetic field volume around the local cell." (L261). Muscle memory: "repeated physical route -> local domain-wall / hysteretic path settles differently -> same later action encounters a biased physical path" (L330-334). Whole loop (L386-408).
- Equations: none.
- Point / Path / Field role (hardware implementation, as stated):
  - Path: the six wedge routes and the domain-wall route ("continuous physical route", L127; "repeated physical route", L330). These are magnetic/electrical routes, not a body ride.
  - Field: the combined 3D field of the two FIELD/VOID toroids is "the candidate local body-state / nerve-control field" (L265-266). "FIELD" here is a body side, not field curl.
  - Point: none stated. Motor targets "wheel; propeller / rotor-type motion" (L307-308). "real torque / thrust" and "torque/thrust measured" (L522, L637). No L, no inertia, no spin keeping.
- Magnetism / gravity / rotation link: magnetism carries state (hysteresis, Br, domain walls, L339-344) and routing coupling. Rotation appears only as wheel/rotor motor targets. Gravity: none stated. Open/closed: no "open/closed magnetic gradient". **[observation]** The nearest hardware notion is the core switching state; this doc does not map it to dL/dt.
- Open / parked / not-set items: shared-CENTER topology without shorting A/B/C, an "Open engineering problem" (L253). Spherical component not locked (L267). Nucleus material, winding and coercivity not locked (L78). Nested layers deferred (L319). Ten immediate questions (L609-618).
- Conflicts: none against canonical rules. It is consistent with RULES.md (V_BUS is not memory, L685).

## RULES   (`RULES.md`)
- Gate / lifecycle: authoritative Builds lock list ("If it was decided, it is here.", L3).
- Upstream: none. Downstream / cites: **C-317** in Science, "Three-vortex / tension-skin analogy" (L30).
- Core claim: cell 1.00 V, middle 0.50 V, HOLD 0.45–0.55 V live (L6-8). Point-up hex, letters are edges (L12-14). Role nuclei: sensor = round figure-8, motor = square figure-8, M4 = double triangle base-to-base, five-mind = double pentagon, six-mind = double hexagon (L21-27). "Current core hardware stays **2D / planar**; its magnetic field is still 3D. **No comparators. All analog.**" (L28). Memory roles split: nucleus, hysteretic body-state layer, V_BUS (L31-36). "**DC is void.** **AC is field rotation.** **AC and mirrored DC.** RC is the remainder" (L46). Pyramid lock: tip-to-tip inside, base-to-base between (L69-70, L80-81). FIELD and VOID are both active (L72, L77-78).
- Equations: none.
- Point / Path / Field role: "AC is field rotation" (L46) is the only explicit rotation statement. It assigns rotation to the Field side (electrical AC). It does not claim a point L. Paths: shared cell-edge / lattice paths carry body-state history (L32).
- Magnetism / gravity / rotation link: planar hardware, 3D magnetic field (L28). Phase-I motor targets "wheel and propeller / rotor-style motion" (L36). No gravity.
- Open / parked / not-set items: nested muscle-memory layers deferred (L37). Numbering is out of order (31-38 sit before 33-34; 18b, 28b), but no content clash.
- Conflicts: none with canonical rules. **[observation]** "AC is field rotation" is an electrical naming. It must not be read as Field carrying L, which the canonical rule reserves for the Point.

## Build sequence   (`SEQUENCE.md`)
- Gate / lifecycle: ordered bench steps 0–9 plus "Not yet".
- Upstream / Downstream: none cited by ID.
- Core claim: "Same CENTER the whole way." (L3). D1 `D = DB − DC` vs CENTER, "Leftover Br on the toroid after you let go." (L9). "BUS ≠ CENTER." (L12). "Electrical rotation A→B→C. Still a slice, not a volume." (L21). "Figure-8 + lattice skin ... Magnetic skin on hex edges." (L29-30).
- Equations: `D = DB − DC`.
- Point / Path / Field role: none stated in canonical terms. "Electrical rotation A→B→C" (L21) is phase sequencing, not point rotation.
- Magnetism / gravity / rotation link: retained Br on the toroid and lattice skin (magnetic memory). Electrical phase rotation. No gravity.
- Open / parked / not-set items: "Hear. Drum. Volume / R27. SOT fab. QCD. Measured 99% recovery." (L36). **R27** is cited as the volume step.
- Conflicts: none.

## Status   (`STATUS.md`)
- Gate / lifecycle: "Proposed architecture." (L3).
- Upstream / Downstream: `cell-v1/WEIGHT_LEAN.md`, `NOT_SOFTWARE.md`, `NO_CLOCK.md`, `REINJECT_BUS.md`, `READINESS.md`, `CELL0.md`, `CELL_ASSEMBLED.md`, `algorithms/rabbit_hopping.py`, `cell-v1/HELMHOLTZ.md`.
- Core claim: locked: lean is the weight, no parameter file, no clock, return on the DC bus not CENTER, readiness, Cell-0 netlist, Rabbit addressing (L9-16).
- Equations: none.
- Point / Path / Field role: open field item: "Shared Helmholtz field as common magnetic weather ... Uniform bias volume only. Not path memory, not CENTER, not V_BUS, not RC." (L20). That separates a uniform field from path memory.
- Magnetism / gravity / rotation link: Helmholtz bias field is open, not locked (L20). No gravity or rotation.
- Open / parked / not-set items: the Helmholtz field (L20).
- Conflicts: none.

## THE ANDROID — Complete Build Specification   (`THE_ANDROID_COMPLETE_BUILD_SPECIFICATION.md`)
- Gate / lifecycle: spec with sections "WHAT'S LOCKED" (L675-689), "WHAT'S HYPOTHESIS" (L693-704) and "WHAT'S NOT CLAIMED" (L708-719).
- Upstream: One-Wave cosmology (sec 17). Downstream / cites: no node IDs. Parts: ALD1106, ALD110800/900, LM339, 74HC, Fair-Rite 2643000101, permalloy 80/20.
- Core claim: diff pair "Idiff = Iss · tanh(Vd / (2·n·Vt))" (L36). Three currents BC-DC / TC-AC / QC-RC: "DC and AC ... are phases of the same recursive current." (L99). Magnetic stack: per-cell hysteresis + ferrite read head + hex lattice group memory (L105-127). "Same metal writes the trace and returns the collapse. Reinjection is the write." (L127). Two-of-three law (L151-156). Lattice: "One continuous magnetic medium spanning the group." (L190). Flower ring "N1→N2→N3→N4→N5→N6→N1. Closed axis path that doesn't have to visit center." (L231); "Deep lean can circulate." (L238). Motor: axes A/B/C go to motor phases A/B/C, "Two-of-three commit naturally produces the six commutation steps" (L378-393). Cosmology (L538-545): "Mass effect → gravity → light → redshift → neutrino wave death. The cycle." "Gravity wake. Great attractor scale." "**Magnetism and gravity as one. The lattice reorients.**" Mapping: "Gravity wake curvature → Magnetic trace", "Lattice reorientation → Hysteresis" (L554-555). "The cell is the cosmology in miniature. Not metaphor. Structural mapping." (L557).
- Equations: `Idiff = Iss · tanh(Vd / (2·n·Vt))` (L36). Hysteresis thresholds partial 0.4/0.28, full 0.82/0.68 (L365-368). PERMIT at ±1.5 units (L180).
- Point / Path / Field role (hardware, as stated):
  - Path: ring circulation around the flower ("Closed axis path", L231; "Deep lean can circulate", L238).
  - Field: "Many flowers → field. One continuous mesh." (L215). Lattice = continuous magnetic medium (L190).
  - Point: none stated as L. Physical rotation only through the motor: "Phase II ... A→B→C sequencing · Rotation" (L594-595) and six-step commutation (L387-393). No inertia, no L.
- Magnetism / gravity / rotation link: L545 "Magnetism and gravity as one." L554 maps gravity-wake curvature to the magnetic trace.
- Open / parked / not-set items: hypotheses (L695-704), including "That the cosmology mapping is structural, not just analogical" (L704). Not claimed: "Cosmology", "Drum", "Hear", "Measured D" (L708-719).
- Conflicts:
  1. **Canonical:** L545 "Magnetism and gravity as one. The lattice reorients." and L554 "Gravity wake curvature → Magnetic trace" contradict "Magnetism does not become gravity" (g = -alpha K_L grad chi; magnetism only opens the point).
  2. **Internal:** L557 "Not metaphor. Structural mapping." contradicts the same doc's L704 (cosmology mapping is a hypothesis) and L716 ("Cosmology" not claimed).
  3. **Intra-Builds:** comparators and resistor ladders in the decision logic (L95 "Where: comparators", L175-177 "window/gap/sign comparators", L578, BOM L649-650 "LM339 ... Resistors (ladder) 18") contradict `RULES.md` L28 "No comparators. All analog." and L29 "No op-amp. No LM339. No designed resistors ... no resistor ladders". It also contradicts `REAL_WORLD_BUILD_HANDOFF.md` L682-683.
  4. **Intra-Builds:** L332-334 "The bus as muscle memory ... The bus voltage signature is the group's history" contradicts `RULES.md` L32b and `REAL_WORLD_BUILD_HANDOFF.md` L685 ("V_BUS carries energy/reinjection, not long-term muscle memory").
  5. **Intra-Builds / material fact:** L142 "Permalloy strip: 80/20 foil ... (high coercivity, personal trace)" and L141 "Ferrite ... (low coercivity, read head)" are inverted relative to `Virtual_3D_Electronics/PARTS_AUDIT.md` L37 (ferrite-43 Hc 0.36 Oe) and L40 (Square Permalloy 80 Hc 0.033 Oe).
  6. **Internal:** the hex diagram (L50-60) labels C− twice and its labels do not follow the stated clockwise order A+ B+ C+ A− B− C− (L63).
  7. **Intra-Builds:** drum and hearing are central to the spec (secs 9, 13, 14) but are "No drum. No hear." in `RULES.md` L29 and "Not yet" in `SEQUENCE.md` L36. The spec itself lists them as not claimed (L714-715).
  - Also: L542 mentions redshift inside a gravity/light chain without the E-528 path-loss framing. It does not assert expansion, so this is not a conflict, but it is unanchored.

## THE BRICK SYSTEM   (`THE_BRICK_SYSTEM.md`)
- Gate / lifecycle: pointer only. "Builds does not invent a second ladder." (L9).
- Upstream: Science `Governance_I_Series/THE_BRICK_SYSTEM.md` and `plates/brick_key.svg` (L5-7). Downstream: none.
- Core claim: evidence ladder metaphor: "Gray concrete freezes the Standard Model so it cannot drift. Red brick goes through the glass house only after a real experiment already threw it." (L11).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## THE BUILD — compact CELL_V1 map   (`THE_BUILD.md`)
- Gate / lifecycle: current compact build map; Phase I steps 1–8, "Stop at the first failed premise" (L90).
- Upstream: RULES.md. Downstream / cites: `cell-v1/CELL.md`, `cell-v1/NUCLEUS_TOROID_TYPES.md`, `cell-v1/CORES.md`, `GRANT_CELL.md` (L98-102).
- Core claim: "A hardware-first analog cell uses a common pair of plain round body toroids for differential connection, a role-specific magnetic nucleus for retained local state, a live -/(0)/+ differential around CENTER, and a shared V_BUS for measured inductive return and readiness — with no global clock and no software controller replacing the physical loop." (L7). Motor-control chain toroid -> square figure-8 -> A/B/C -> ternary -> toroid -> "motor / field consequence" -> V_BUS (L54-68). "Measure recovery; never assume 100%." (L77).
- Equations: none.
- Point / Path / Field role: none stated in canonical terms. "motor / field consequence" (L65) is the output stage.
- Magnetism / gravity / rotation link: the magnetic nucleus holds retained state (L83-84). No gravity or point rotation.
- Open / parked / not-set items: Phase I items 1–8 are unmeasured.
- Conflicts: none.

## Virtual 3D Electronics — Parts audit   (`Virtual_3D_Electronics/PARTS_AUDIT.md`)
- Gate / lifecycle: audit dated 2026-10-05; "results are MODELED, not bench measurements" (L13). `npm test` 432 checks, all PASS (L100).
- Upstream: manufacturer sheets (Fair-Rite, Micrometals, Magnetics, onsemi, Diotec, Vishay, Infineon, ALD), IEC 60205, IPC-2222B, NEMA MW 1000. Downstream: `js/catalog.js` VERIFICATION, `test/parts-audit.test.js`.
- Core claim: material values ferrite-43 µi 800, Br 2200 G, Hc 0.36 Oe (L37); ferrite-77 Hc 0.25 Oe (L38); Square Permalloy 80 Hc 0.033 Oe, Br/Bm ≥ 0.80 (L40); memory ferrite "CLASS / UNVERIFIED" (L41).
- Equations: iron-powder roll-off `µ/µi = 1/(1+(H/53 Oe)²)` (L39).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: core hysteresis parameters only. "Hysteresis loss of soft ferrite and iron powder is not modeled (anhysteretic)" (L91).
- Open / parked / not-set items: gaps (L91-96): no temperature model, no X7R DC-bias derating, no trr, non-row apertures UNMODELED, memory ferrite is a CLASS value.
- Conflicts: none against canonical rules. Its data contradicts the Android spec's coercivity labels (see that section, item 5).

## Virtual 3D Electronics — README   (`Virtual_3D_Electronics/README.md`)
- Gate / lifecycle: "MODELED from nominal datasheet / standards values. Not a bench measurement." (L5).
- Upstream: `validation/SCIENCE_CONNECTIONS.md` (L2, "links do not imply validation"). Rajchman & Lo 1956 (L33). Downstream: `js/physics.js`, `circuit.js`, `magnetics.js`, `semis.js`, `simulate.js`.
- Core claim: DC magnetics: "H = ΣNI / l per path, a square-loop leg switches when H ≥ Hc (short path around one hole vs long path around all holes is the transfluxor threshold mechanism ...), linear B = μ0·μi·H with saturation at Bsat, and L = AL·N²" (L33). Transient: hysteretic B(H) with viscous switching, "dB/dt is limited by the material's Sw" (L36); "A winding's EMF is N·dΦ/dt" (L37). Energy balance must close within 1% (L43); core energy vs ∫H·dB within 2% (L44). Core state persists between runs: "a set core stays set and a blocked core stays blocked" (L46).
- Equations: `H = ΣNI/l`; `B = μ0·μi·H`; `L = AL·N²`; `EMF = N·dΦ/dt`; energy check `∫H·dB`.
- Point / Path / Field role: none stated in canonical terms. The magnetic "path" here is the flux path around an aperture (short vs long path, L33), not a body ride.
- Magnetism / gravity / rotation link: magnetism = flux and hysteresis state of cores. No gravity, no rotation. **[observation]** Its "set" vs "blocked" transfluxor states (L46, L99-101) are the only open/closed-like magnetic states in the slice's hardware. The doc does not link them to point rotation or dL/dt.
- Open / parked / not-set items: known limits (L81-84): no pulse derating, non-row apertures UNMODELED, no soft-ferrite hysteresis or eddy loss, no avalanche model.
- Conflicts: none.

## Virtual Breadboard — Architecture   (`Virtual_Breadboard/00_RULES/architecture.md`)
- Gate / lifecycle: canonical layer architecture (00–11). Status system MISSING / IMPLEMENTING / FAILING / PASSING (L126-127).
- Upstream: none. Downstream / cites: `../LAYER_MAP.md`, the other rules files.
- Core claim: "A build uses the breadboard. A build does not become part of the breadboard." (L60). Rules 1–8 (L72-100). "It does not know 'this is a One-Wave flashlight.'" (L145-147). Stage 4 primitives "shared center, differential pair, MOSFET switching stages, hysteresis, reinjection" (L213-214); Stage 5 magnetics "one winding, coupled pair, three windings, phase, measurable field behavior" (L216-217).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: 07_MAGNETICS layer: "coupled coils, transformers, field behavior" (L41).
- Open / parked / not-set items: directory split is tracked debt (L62-68).
- Conflicts: none.

## Virtual Breadboard — Failure rules   (`Virtual_Breadboard/00_RULES/failure_rules.md`)
- Gate / lifecycle: process rule.
- Upstream: physics_rules.md, update_rules.md. Downstream: none.
- Core claim: "A failing test is data, not an emergency to paper over." (L9). Three-way triage: physics wrong / build wrong / circuit does not perform (L27-37). NMOS high-side self-referencing loop: the solver "correctly refused to converge"; the fix was a PMOS (L49-54).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## Virtual Breadboard — Interface rules   (`Virtual_Breadboard/00_RULES/interface_rules.md`)
- Gate / lifecycle: Layer 11 rule.
- Upstream: failure_rules.md. Downstream / cites: `../11_INTERFACE/MAP.md`, `../BUILDS/MAP.md`, `experiments/brain_cell_001.json`.
- Core claim: "The interface owns no physics" (L3). Presets (Cal board, Stage-1 ternary cell) are builds, per Rule 8 (L17-23). `js/app.js` (2400+ lines) mixes UI and presets, a known gap (L39-44).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: splitting app.js (L39-44).
- Conflicts: none.

## Virtual Breadboard — Measurement rules   (`Virtual_Breadboard/00_RULES/measurement_rules.md`)
- Gate / lifecycle: Rule 7.
- Upstream: architecture.md. Downstream / cites: `../05_MEASUREMENT/MAP.md`, `simulate.js` functions, `test/circuit.test.js` Test 47.
- Core claim: "Meters observe. Meters do not change the answer" (L12). Floating-reference trap: "always read the real voltage *difference*" (L54-55).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: real scope-probe loading is MISSING (L13-14).
- Conflicts: none.

## Virtual Breadboard — Physics rules   (`Virtual_Breadboard/00_RULES/physics_rules.md`)
- Gate / lifecycle: Rules 1, 5, 6.
- Upstream: architecture.md. Downstream / cites: `test/regression-builds/09_halfbridge_deadtime.js`, PR #15 (removed the Ternary Cell macro), `../LAYER_MAP.md`.
- Core claim: "Real behavior over desired behavior" (L3). Failure modes must be producible, including "center/reference movement" and "inductive flyback" (L17-30). No magic primitives: the hard-coded Ternary Cell was removed (L44-49). "This is an ordinary-electronics circuit simulator, not a finite-element field solver." (L72-73).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: "a field-vector Bx/By/Bz probe" and "arbitrary magnetic core material parameterization" are MISSING (L74-76).
- Open / parked / not-set items: the field-vector probe is missing (L75).
- Conflicts: none.

## Virtual Breadboard — Testing rules   (`Virtual_Breadboard/00_RULES/testing_rules.md`)
- Gate / lifecycle: Rule 4, permanent regression.
- Upstream: architecture.md. Downstream / cites: `circuit.test.js` (49), `qualification.test.js` (80), `primitives.test.js` (26), `run_regression_builds.js` (39 / 17 builds), `../09_TESTS/MAP.md`, `../07_MAGNETICS/MAP.md`.
- Core claim: "None of these get weakened to make a new change pass" (L14-15). Stage 5 magnetics is covered, but "Bx/By/Bz field-vector measurement specifically is MISSING" (L82-83).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: as above (L80-83).
- Open / parked / not-set items: the Bx/By/Bz probe.
- Conflicts: none.

## Virtual Breadboard — Update rules   (`Virtual_Breadboard/00_RULES/update_rules.md`)
- Gate / lifecycle: process rule; triage Types A–K (L38-50).
- Upstream: architecture.md. Downstream: `10_RECEIPTS/`.
- Core claim: "Every failure must first be classified into exactly one type" (L35). Type H is a magnetic problem, "Mutual coupling is wrong", fixed in `07_MAGNETICS` (L47). "If implementation suddenly needs five unrelated layers, **stop**." (L78).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: Type H routing only.
- Open / parked / not-set items: none.
- Conflicts: none.

## Virtual Breadboard — CELL_V1 F0 Parts BOM   (`Virtual_Breadboard/01_PARTS/CELL_V1_PARTS_BOM.md`)
- Gate / lifecycle: "F0 candidate list, not the current dual-rail bench" (L3). It is superseded for the bench by `BENCH_REALITY_CONTRACT.md` (+12 / 0 star / −12).
- Upstream: `../CELL_V1_FULL_BUILD.md`. Downstream: netlist.
- Core claim: "Three **logical** bidirectional Mirror stations (`G+`, `G0`, `G-`) ... **12 MOSFET devices** while remaining **3 logical Mirror gates / 6 traversals**." (L9). The TLE2426 midpoint "carries **imbalance current**, not the full board current" (L47). "A two-resistor divider is a bias hint, not a dynamic return rail." (L49). Magnetics: "later | ferrite ring + 20–50 turn sense winding or Hall probe | ... sense only until drive-off retention is proven" (L31).
- Equations: none (I_G = Vshunt / 10 Ω, L23).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: magnetic observation is deferred, sense only (L31).
- Open / parked / not-set items: MOSFET acceptance (L35-43). Retention is unproven.
- Conflicts: (intra-Builds) uses 1k arm limiters, 10 Ω shunts, an RC bleed of 100k (L22-26) and a TLE2426 midpoint. `RULES.md` L29 forbids "bleed paths ... as part of the intended mechanism". The doc frames these as an F0 bench fixture, and L3 says the current bench forbids TLE2426/vgnd stacking. This is a tension, not a canonical-physics conflict.

## Virtual Breadboard — Layer 01 Parts map   (`Virtual_Breadboard/01_PARTS/MAP.md`)
- Gate / lifecycle: status table (all PASSING).
- Upstream: architecture.md. Downstream / cites: `js/circuit.js` line refs, tests.
- Core claim: "A part ... does not know what project is using it." (L5-7). Ferrite toroid "mutual coupling via `k*sqrt(L_i*L_j)`" (L34). Square-loop memory core: "remanent flux state, real coercive threshold" (L35). MTJ angle sensor: "quadrature sin/cos pair" (L36).
- Equations: `M = k·sqrt(L_i·L_j)` (L34).
- Point / Path / Field role: none stated. **[observation]** The MTJ angle sensor (L36) is the only part that measures an angle. Nothing ties it to point rotation.
- Magnetism / gravity / rotation link: remanent-flux core and coupled toroids.
- Open / parked / not-set items: "arbitrary magnetic core *material* parameterization ... is MISSING" (L42-45).
- Conflicts: none.

## Virtual Breadboard — CELL_V1 Physical Netlist   (`Virtual_Breadboard/02_CONNECTIONS/CELL_V1_NETLIST.md`)
- Gate / lifecycle: companion netlist to `../CELL_V1_FULL_BUILD.md`.
- Upstream: CELL_V1_FULL_BUILD.md. Downstream: none.
- Core claim: NET_P +5 V, NET_G ~2.5 V CENTER spine, NET_N 0 V (L8-10). "Do not daisy-chain NET_G around the three stations." (L13). "All three station taps star independently to the same NET_G spine." (L68). "Only the mismatch between the upper and lower arms appears as `I_G`." (L98).
- Equations: `I_GX = (V(GX_TAP) - V(NET_G)) / 10 ohm` (L103). Count invariant 3 × 2 × 2 = 12 MOSFETs (L109-112).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: exact pinouts must come from the datasheet (L58).
- Conflicts: same F0 resistor/bleed tension as the BOM (L39-41: 1k, 10µF, 100k bleed). Not canonical.

## Virtual Breadboard — Layer 02 Connections map   (`Virtual_Breadboard/02_CONNECTIONS/MAP.md`)
- Gate / lifecycle: status table, PASSING.
- Upstream: architecture.md. Downstream / cites: `circuit.js` (`buildTopologyUnionFind`, `netlist`, `diagnose`), `js/board.js`, `../PERFBOARD.md`, tests.
- Core claim: wires and closed switches are "the only things that ever merge two node names" (L20-22). `diagnose()` names `noReference: true` (L35-37). Perfboard: "every pad its own cellId" (L55).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: no branch/loop discovery report (L80-82). `realDcEdges()` can give a false FLOATING (L83-89).
- Conflicts: none.

## Virtual Breadboard — G spine mechanics   (`Virtual_Breadboard/03_ELECTRICAL_CORE/G_SPINE.md`)
- Gate / lifecycle: electrical-core rule note.
- Upstream: netlist. Downstream: Void (reads I_0).
- Core claim: "G is not a ground pour you dump returns into. It is the **organizing reference** and the **only home** for leftover current." (L3). "Imbalance: I_0 = what the pairs did not cancel." (L14). Star, not daisy-chain: "two 'G' points disagree — fake lean" (L21). "Reinjection lives in the cell (leftover B), not as charge stored *in* the spine. Void reads I_0 at the home end. That is vagus for the whole stack." (L35-36).
- Equations: none (I_0 = uncancelled pair current, L14).
- Point / Path / Field role: none stated in canonical terms. The spine is a reference path, and IR drop along it "looks like lean" (L30).
- Magnetism / gravity / rotation link: "leftover B" holds reinjection in the cell (L35). No gravity or rotation.
- Open / parked / not-set items: the 9 V + TLE2426 spine (~20 mA) is F0 only (L28).
- Conflicts: (intra-Builds, minor) L3 calls G "the **only home** for leftover current". `THE_BUILD.md` L74-75 and `RULES.md` L22 send leftover/collapse current to V_BUS, and "CENTER != V_BUS". The two can be reconciled (G carries imbalance I_0; V_BUS gets inductive collapse), but the wording clashes.

---

## Slice summary

### (a) Nodes / chapters bearing on Point, Path, Field, rotation, magnetism, gravity, inertia, mass, resistance, lattice organization or locking

Node IDs cited in this slice:
- **D-412** (`Miniverse/room3d/LATTICE_BODY_PHYSICS.md` L41): governs the software lattice-body sandbox (software mass/load, chi compression proxy, strain). It is explicitly not a gravity law.
- **D-411** (`Proposed_Android_Brain/Ch02` L25): 3:1 planar mirrored-axis count. It is kept distinct from the 3:1 nerve ratio and from sixfold lattice geometry.
- **C-312** (`Ch02` L5): Android Body link (hierarchical control). No rotation content here.
- **C-317** (`RULES.md` L30): three-vortex / tension-skin analogy lives in Science, not Builds.
- **G-721, G-721a–e** (`00_Book_Overview` L22-24, `Ch01` L34-51, `Ch04`): symbolic route / rail grammars. Path-like route scheduling; "do not directly command actuator position".
- **G-722** (`00` L25, `Ch01` L41/L52, `Ch03`): Hopfield/Boltzmann procedural memory. Not physics.
- **G-723** (`00` L26, `Ch01` L53, `Ch04` L31): spectral audit. "does not generate movement".
- **E-510–E-514** (`00` L27): wheel system, "harmonic and movement relation". The wheel translates route into "live movement geometry" (`Ch01` L54).
- **R27** (`SEQUENCE.md` L36): Volume step, parked.
- Gate 5 / Gate 6 (`Ch01` L65): commit rule.

How the build hardware implements Point / Path / Field (as stated in the docs):
- **Point:** no doc implements point rotation with L = I omega, inertia axes, or spin keeping. Physical rotation appears only as motor output: wheel / propeller / rotor targets (`RULES.md` L36; `REAL_WORLD_BUILD_HANDOFF.md` L307-308, L522-525, L637), three-phase six-step commutation with "A→B→C sequencing · Rotation" (`THE_ANDROID...` L387-393, L594-595), and electrical phase rotation (`SEQUENCE.md` L21). Torque and thrust are to be measured. No L bookkeeping is described.
- **Path:** six tip-to-tip / base-to-base wedge routes (`RULES.md` L39-51; `REAL_WORLD_BUILD_HANDOFF.md` L94-139); the domain-wall body-state route that biases repeat traversal (`REAL_WORLD_BUILD_HANDOFF.md` L330-334; `RULES.md` L32); the flower ring as a "Closed axis path", where "Deep lean can circulate" (`THE_ANDROID...` L231-238); G-721 route grammars (brain book). These are routing and memory paths. None is described as a carrier-free ride in the G-769 sense.
- **Field:** the combined 3D field of the FIELD/VOID round toroids is the candidate local body-state field (`REAL_WORLD_BUILD_HANDOFF.md` L261-266). "AC is field rotation" (`RULES.md` L46). Planar hardware has a 3D magnetic field (`RULES.md` L28). The Helmholtz uniform bias field is open (`STATUS.md` L20). The lattice is "One continuous magnetic medium" (`THE_ANDROID...` L190). In software, chi is the compression proxy (`LATTICE_BODY_PHYSICS.md` L23). "FIELD" in Builds is mostly a body side (FIELD/VOID), not field curl.
- **Magnetic open / closed:** no doc in the slice states an open/closed magnetic gradient or dL/dt = 0 / -gamma L. Magnetism in the hardware is memory and routing: Br remanence, hysteresis, domain walls, the figure-8 nucleus, and transfluxor set/blocked states (`ONE.md` L6; `PRINT.md` L4; `SEQUENCE.md` L9; `Virtual_3D_Electronics/README.md` L33, L46; `01_PARTS/MAP.md` L35). **[observation]** The transfluxor "set" vs "blocked" core state is the closest hardware analog to open/closed, but no doc makes that mapping.
- **Mass / resistance / lattice locking:** software mass/load on the Miniverse lattice (`LATTICE_BODY_PHYSICS.md` L6). No resistance = mass/organization statement. No Moon 1:1 / Mercury 3:2 locking. "Resistance" in Builds means electrical resistors only.
- **Gravity:** only `THE_ANDROID_COMPLETE_BUILD_SPECIFICATION.md` (L541-545, L554), where it conflicts (below). `LATTICE_BODY_PHYSICS.md` explicitly disclaims a gravity law.

### (b) All conflicts found
Canonical:
1. `THE_ANDROID_COMPLETE_BUILD_SPECIFICATION.md:545` "Magnetism and gravity as one. The lattice reorients." and `:554` "Gravity wake curvature → Magnetic trace" contradict "Magnetism does not become gravity" (g = -alpha K_L grad chi).
2. `THE_ANDROID_COMPLETE_BUILD_SPECIFICATION.md:557` "Not metaphor. Structural mapping." contradicts its own `:704` (hypothesis) and `:716` (cosmology not claimed). The canonical risk is promoting the cell-to-cosmology mapping without evidence.

Intra-Builds (not canonical physics, but recorded):
3. Comparators, LM339 and resistor ladders: `THE_ANDROID...:95, :175-177, :578, :649-650` and `ONE.md:15` contradict `RULES.md:28-29` and `REAL_WORLD_BUILD_HANDOFF.md:682-683`.
4. "The bus as muscle memory" (`THE_ANDROID...:332-334`) contradicts `RULES.md:32b` and `REAL_WORLD_BUILD_HANDOFF.md:685`.
5. Coercivity labels inverted: `THE_ANDROID...:141-142` (ferrite low, permalloy high) vs `PARTS_AUDIT.md:37, :40` (ferrite-43 Hc 0.36 Oe > permalloy-80 Hc 0.033 Oe).
6. Hex diagram mislabels the edges (C− appears twice): `THE_ANDROID...:50-60` vs `:63`.
7. Drum and hearing as core features (`THE_ANDROID...` secs 9, 13, 14) vs `RULES.md:29` and `SEQUENCE.md:36`.
8. "G ... the only home for leftover current" (`G_SPINE.md:3`) vs leftover/collapse to V_BUS (`THE_BUILD.md:74-75`, `RULES.md:22`). Reconcilable, but the wording clashes.
9. F0 bench resistors, bleed and TLE2426 midpoint (`CELL_V1_PARTS_BOM.md:22-27`, `CELL_V1_NETLIST.md:38-41`) vs `RULES.md:29` (no bleed paths in the intended mechanism). The docs frame these as a bench fixture, and the BOM marks itself superseded (L3).

### (c) Cross-references outside the slice that matter for point rotation or magnetism
- `/home/user/Builds/cell-v1/HELMHOLTZ.md`: shared Helmholtz field, open (`STATUS.md` L20).
- `/home/user/Builds/cell-v1/CELL.md`, `cell-v1/NUCLEUS_TOROID_TYPES.md`, `cell-v1/CORES.md`, `GRANT_CELL.md`: nucleus and toroid magnetics (`THE_BUILD.md` L98-102).
- `/home/user/Builds/cell-v1/REINJECT_BUS.md`, `READINESS.md`, `WEIGHT_LEAN.md`, `CELL0.md`, `CELL_ASSEMBLED.md` (`STATUS.md`).
- `/home/user/Builds/validation/SCIENCE_CONNECTIONS.md`: Science node links (`README.md` L2, `Virtual_3D_Electronics/README.md` L2).
- `/home/user/Builds/Virtual_Breadboard/07_MAGNETICS/MAP.md` (Bx/By/Bz MISSING), `../LAYER_MAP.md`, `CELL_V1_FULL_BUILD.md`, `BENCH_REALITY_CONTRACT.md`.
- `/home/user/Builds/Miniverse/EXPAND_MINIVERSE.md`; `One_Wave_Bench/App_Center/Composite_Agent_Lab/AI_COUNCIL_PROTOCOL.md`.
- Science: **C-317** (three-vortex / tension-skin), **D-411**, **D-412**, **C-312**, **G-721–G-723**, **E-510–E-514**, **R27**; `Governance_I_Series/THE_BRICK_SYSTEM.md`.
