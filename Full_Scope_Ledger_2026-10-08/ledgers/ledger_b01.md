# Ledger b01 — Builds repo (`/home/user/Builds`), 29 files

All 29 files in slice b01 read in full (cat -n / Read, no limit). Line numbers refer to each file.
Convention: "Point/Path/Field role" lists only what the file states. Where I note a hardware analogue the file does not name, it is marked **[reviewer mapping, not stated]**.

---

## Builds PR template — Pull request checklist   (`/home/user/Builds/.github/PULL_REQUEST_TEMPLATE.md`)
- Gate / lifecycle: process file; no gate.
- Upstream: CLA.md, LOCK.md, RULES.md (L3, L7). Downstream / cites: none.
- Core claim: "lock list in LOCK.md / RULES.md is not reopened here." (L3); licenses CERN-OHL-S-2.0 / GPL-3.0+ / CC-BY-SA-4.0 (L9).
- Equations: none
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## Repo map — All One-Wave-Universe GitHub → four homes   (`/home/user/Builds/ALL_GITHUB_INTO_THREE.md`)
- Gate / lifecycle: "The map is locked." (L43).
- Upstream: none. Downstream / cites: repos One-Wave-Science, RABBIT-HOPPING, HEX-SPLIT, POINT-SPIN, GRAV-LAB, Great-Galactic-Library, Mythos-and-Stories, Bridge-Comand, BUCKET-R2, GCAC (L10-39).
- Core claim: "Builds / Science / Mythos / Bridge-Comand. No fifth bucket." (L3-4). GRAV_LAB *engineering benches* stay in Builds (L15); GRAV-LAB math/sim and POINT-SPIN go to Science (L34-35).
- Equations: none
- Point / Path / Field role: none stated (POINT-SPIN named only as a Science repo, L34).
- Magnetism / gravity / rotation link: none stated (GRAV-LAB split: benches here, math in Science).
- Open / parked / not-set items: title says "THREE" but body says four homes (L1 vs title filename) — naming inconsistency only.
- Conflicts: none.

## Anti-drift vocabulary — Do not translate this into the standard system   (`/home/user/Builds/ANTI_DRIFT.md`)
- Gate / lifecycle: rule file.
- Upstream / cites: none.
- Core claim: forbidden substitutions, e.g. "HOLD → off / zero / disabled / parked" (L8), "memory → log / receipt / checkpoint" (L10), "T6 → commit() in software as if the body had moved" (L11). "The thing is the lean in the path. Measure it or it is not there." (L17).
- Equations: none
- Point / Path / Field role: Path — "the lean in the path" is where the thing lives (L17). Point/Field none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## CELL_V1 architecture — Proposed CELL_V1 architecture   (`/home/user/Builds/ARCHITECTURE.md`)
- Gate / lifecycle: "Proposed"; Locked vs Open list (L132-138).
- Upstream: One-Wave-Science ("Science stays in One-Wave-Science", L5). Downstream / cites: `cell-v1/HELMHOLTZ.md` (L53, L136).
- Core claim: "State is carried by the settled physical loop after an event — differential bias, magnetic history, bus condition, and returned consequence. Not a weight file." (L3). Common shell = two plain round toroids, not figure-8 (L9-13). Nuclei by role (L17-20). Two pyramid systems: M4 base-to-base nucleus vs six-wedge cluster routing tip-to-tip inside / base-to-base between cells (L24-33). "Current hardware geometry is planar / 2D. Magnetic fields are 3D." (L37).
- Equations: `E_in = integral V(t) I(t) dt`; `E_rec = 1/2 C (V_after^2 - V_before^2)` (L106-107).
- Point / Path / Field role: none stated as Point/Path/Field. Field-like: toroid pair's "combined 3D field is the local body-state/nerve-control environment" — "candidate local body-state field, not yet a separately proven spherical component" (L43-48). Path: "hysteretic path layer" kept separate from uniform Helmholtz bias: "Uniform bias and path memory stay separate" (L57). CENTER = local differential reference (L77). [reviewer mapping, not stated: CENTER/nucleus ≈ point reference; six wedge routes + hysteretic path layer ≈ path; toroid/Helmholtz B volume ≈ field.]
- Magnetism / gravity / rotation link: Magnetism: toroids, figure-8 nuclei, Helmholtz pair "approximately uniform B in the volume where the cells sit" (L55). Hardware open/closed: toroids are closed magnetic circuits; Helmholtz is an open-volume near-uniform field (grad B ≈ 0 in the working volume) — neither linked to dL/dt in the file. Gravity: none. Rotation: none stated.
- Open / parked / not-set items: materials, turns, transistor topology, thermal fade, coupling, bus impedance, 3+3 winding, field strength, torque, recovery fraction, retention, scale-up, Helmholtz (L136). Field shape/coupling/spherical structure open (L49).
- Conflicts: none with canonical rules. Naming note: "FIELD/VOID body-interface pair" (L41) uses FIELD as a body side, not as the field curl/gradient rate — different sense of "Field".

## Avenues — Avenues   (`/home/user/Builds/AVENUES.md`)
- Gate / lifecycle: idea list; "Closed" list (L16-24).
- Upstream / cites: none.
- Core claim: magamp reset as write-depth knob (L7); "Faraday pulse *is* the sense of dλ/dt" (L8); "**Inertia as extra λ** — spinning or moving mass keeps current after PERMIT drops; regen onto V_BUS is mechanical hysteresis meeting iron hysteresis." (L9); "**120° and closed toroids** — keep mutual M small so axes oppose for real." (L10); "Cosmology in Builds" closed (L23).
- Equations: none (dλ/dt named).
- Point / Path / Field role: Point-like — spinning mass keeps current after drive drops (L9): a carried rotation persists; consistent with "a thing keeps the point spin it has". Path/Field: none stated.
- Magnetism / gravity / rotation link: closed toroids to minimise mutual inductance (L10) — hardware "closed" magnetic circuit. Rotation: mechanical inertia feeds regen (L9). Gravity: cosmology excluded (L23).
- Open / parked / not-set items: M "Measure M later" (L10); thermal redline (L12).
- Conflicts: none.

## Android brain/body — Android Current Brain/Body Architecture   (`/home/user/Builds/Android_Body/ANDROID_CURRENT_BRAIN_BODY_ARCHITECTURE.md`)
- Gate / lifecycle: "WORKING ARCHITECTURE / YELLOW until implemented and measured" (L3).
- Upstream: constellation / Rabbit-Hopping reconstruction (L140). Downstream / cites: M4, Jetson boundary (L188-192), RebuildReceipt (L157).
- Core claim: DC loop (polarity), AC loop (ternary), "**RC loop** — rotational/quadratic magnetic-state layer ... turn a resolved directional relation into a rotational state that can be held, routed, or used as the point/reference for the next scale." (L13-15). "a complete lower-scale resolved loop may become one effective point/reference for the next scale" (L17). Scale recurrence: "resolved lower-scale relation / rotation → becomes one effective point/reference at the next scale → new path / relation / boundary ... → next-scale choice and rotation" (L174-181). Magnetic memory (hold) vs spintronic action-down kept separate (L120-136).
- Equations: none.
- Point / Path / Field role: Point — resolved loop/rotation becomes "one effective point/reference" at next scale (L15, L17, L176). Path — "new path / relation / boundary is constructed" after the point (L179); Rabbit-Hopping traversal "with route/origin preserved" (L149). Field — none stated (Field/Void used as an organisational side, L41, L58-68). Three-winding motor → "rotating magnetic field / actuator motion" (L83).
- Magnetism / gravity / rotation link: magnetic memory = retention; spintronic = action-down (L122-136); RC loop = rotational magnetic-state (L15). Gravity: none. Does not separate point rotation vs path rotation.
- Open / parked / not-set items: chip count, cube topology, dual-pyramid geometry, memory device, spintronic device, commutation, sensory bandwidth, local vs escalate split (L222-230).
- Conflicts: (1) Terminology — uses "RC loop" for rotation (L15, L24, L216) while `CURRENT_BUILD_ORDER.md:152` says "Do not use `RC` for rotation". Internal Builds conflict, not a canonical-rule conflict. (2) Soft: "rotation" (L15, L175, L181) is not classified as point rotation (L-bearing) vs path rotation (ride); canonical requires the three rates kept separate — ambiguity, not an explicit contradiction.

## Android body spec — Android Body — Functional Recursive System Architecture   (`/home/user/Builds/Android_Body/Android_Body_Functional_Architecture.md`)
- Gate / lifecycle: "YELLOW (structure, real math throughout) / YELLOW (full implementation)" (L3); proof ladder Brown→Green→Yellow→Bronze→Silver→Gold via I-02 (L105-106).
- Upstream: G-719 (corrected groundings), B-213 and G-711 (failed audit), I-05, Books/Proposed_One_Wave_Consciousness, Books/Proposed_Android_Brain (L9-14). Downstream / cites: C-312, A-111, G-710, E-507, B-203, B-204, B-221, D-408, D-411, D-412, I-02, G-722 (table L121-131, L165).
- Core claim: Communication layer = A-111 neighbor-average "Delta_psi_i = <psi_j> - psi_i" (L35-38); Regulation = G-710 "Q_n = k_n * F_n" (L50-52); Three Oscillation scales via E-507 (L64-68); D-408 triangular/hex lattice, "3:1 planar axis-pair view <-> 6:1 directed-neighbor view" (L84-90).
- Equations: `Delta_psi_i = <psi_j> - psi_i`; `psi_i^{n+1} = psi_i^n + (1-gamma)(psi_i^n - psi_i^{n-1}) + beta_i(<psi_j^n> - psi_i^n)` (L35-39); `Q_n = k_n * F_n` (L50).
- Point / Path / Field role: none stated as Point/Path/Field. Six directed neighbor routes around one center (L84) [reviewer mapping: routes ≈ path, center ≈ point, not stated].
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: no simulation run (L147-148); B-221 six→three reduction partial (L144-146, L156-159); validation goals untested (L149-150).
- Conflicts: none.

## Build packet — Build packet   (`/home/user/Builds/BUILD.md`)
- Gate / lifecycle: geometry lock; "Stop at the first failed premise." (L45).
- Upstream / cites: REAL_WORLD_BUILD_HANDOFF.md, RULES.md, cell-v1/CELL.md, cell-v1/NUCLEUS_TOROID_TYPES.md, cell-v1/CELL_ASSEMBLED.md, GRANT_CELL.md, FULL_BUILD.md (L97-103).
- Core claim: "CELL_V1 is a hardware-first analog control-cell family with a common two-round-toroid body differential shell, a role-specific magnetic nucleus, live -/(0)/+ state around CENTER, and measured inductive return to V_BUS." (L7). CENTER != V_BUS (L25).
- Equations: none.
- Point / Path / Field role: none stated. "second compatible path" in build chain (L40).
- Magnetism / gravity / rotation link: magnetic nucleus + round toroids (L7-17); no gravity/rotation statement.
- Open / parked / not-set items: evidence list (L70-78); no free energy / fixed recovery / torque claims (L88-93).
- Conflicts: none.

## Builders hall — CELL_V1 builders hall sheet   (`/home/user/Builds/BUILDERS_HALL.md`)
- Gate / lifecycle: Phase I only; "Nothing in this sheet has been measured yet." (L9); pass/fail list (L86-94).
- Upstream / cites: GRANT.md, LOCK.md (L7).
- Core claim: "one small analog circuit that remembers a magnetic state and uses that state the next time it acts" (L13). Coupling: "Two windings, one shared flux. Each winding stays itself. The connection is the flux they share. The record of the meeting is a phase shift" (L67). Fail: "someone cut a path through the core and called the hole a connection" (L82).
- Equations: none (1.00 V span, 0.45–0.55 hold band, L13, L58).
- Point / Path / Field role: none stated. [reviewer mapping: shared flux between intact windings ≈ field coupling; keeping the core closed (L82) ≈ closed magnetic circuit.]
- Magnetism / gravity / rotation link: magnetic coupling through shared flux recorded as phase shift (L67-76); core must not be cut open (L82). Gravity: "a grant for a theory of gravity" is out of scope (L98). Rotation: none.
- Open / parked / not-set items: square-core figure-8 "If it cannot be wound, stop" (L35); turns not locked (L33).
- Conflicts: none.

## Build book — Build book — the 1 V cell   (`/home/user/Builds/BUILD_BOOK.md`)
- Gate / lifecycle: Phase I = steps 1–5 of §11 (L172).
- Upstream / cites: cell-v1/CELL.md, GRANT.md, cell-v1/PARTS.md, cell-v1/BREADBOARD.md, cad/pcb_hex.svg (L178-183).
- Core claim: top face = three leans + home 0.50 V with square-loop figure-8 on home (L13); bottom = V_BUS rail on hex edges + magnetic skin (Permalloy/ferrite foil) for long "group memory" (L15, L85-87). "The copper carries current. The foil keeps remanence after the current is gone. That is the lattice skin." (L85). "The iron is the home remembering." (L111). Later: "Ta/W/Pt strip under the 8 for spin-torque write" (L61).
- Equations: none ("Energy in vs energy back is a fraction ... Do not write 99", L160).
- Point / Path / Field role: none stated by name. [reviewer mapping: home/CENTER + figure-8 ≈ point; edge bus + skin ≈ path; not stated.]
- Magnetism / gravity / rotation link: remanence in square-loop ferrite and edge foil; spin-torque write deferred (L61). No gravity/rotation.
- Open / parked / not-set items: no KiCad file yet (L166); NiFe / spin-torque later (L61).
- Conflicts: none with canonical rules. Internal Builds note: BUILD_BOOK uses 10 kΩ drain loads, 100 kΩ gate resistors and a 10 kΩ divider for 0.50 (L38-40) while ARCHITECTURE.md:128 / MASTER_CURRENT_STATE.md:265-268 forbid resistor threshold ladders/dividers as CENTER; BUILDERS_HALL.md:20 says CENTER "is a conductor, not a resistor divider". Also "two rings touching = figure-8" (L42, L109) vs MASTER_CURRENT_STATE.md:178-179 "one-piece ... two-aperture figure-8". And point-up hex (L67) vs flat-top hex in CELL_V1_CURRENT_BUILD_CANON.md:37. LM339 mentioned as later option (L133) vs forbidden in MASTER L263.

## CELL_V1 canon — CELL_V1 — CURRENT BUILD CANON   (`/home/user/Builds/CELL_V1_CURRENT_BUILD_CANON.md`)
- Gate / lifecycle: "active build specification ... single source of truth" (L3-4); patch rule (L1042-1056); Phase 1–7 go/no-go (L806-852).
- Upstream / cites: none external.
- Core claim: "BUS + LEAN + MEMORY ... one recursive current system" (L13-15); "DC and AC are phases/components of RC" (L21); asynchronous, threshold-gated, no clock (L23-31); flat-top hex, side-centre ports A+ B+ C+ A− B− C− clockwise (L37-48); three memory depths: ternary hysteresis (short), square figure-8 (medium), connected lattice hysteresis path scoring (long) (L326-344); "Field and Void are both bidirectional" (L469-502); M4 = 2F+2V up / 2F+2V down (L508-528); §19 "Two opposed rotating components can combine into an oscillatory resultant ... balanced opposing rotations → AC-like oscillation, imbalance → DC-like bias, complete retained/reinjected process → RC" (L557-566); reinjection of collapse/back-EMF into own V_BUS (L574-602).
- Equations: `ΔE_BUS = ½ C (V_final² − V_initial²)` (L898); path score = normalized change in switching threshold from virgin baseline (L411); hysteresis thresholds partial_enter 0.40 / partial_exit 0.28 / full_enter 0.82 / full_exit 0.68 (L135-138).
- Point / Path / Field role: none stated by name. Path — "A path's physical state is its score" (L384), "path used → hysteretic state changes → future threshold changes → path becomes easier / harder" (L397-407), distributed path preference (L310-316). Point-like — square figure-8 = "recursive cell reference ... retained state against which the next event is read" (L289-294). Field — "Field half + Void half" are bidirectional organisational halves (L479-500), not a curl/gradient. Rotation — opposed rotations make AC, imbalance DC (L557-566), not split into point/path.
- Magnetism / gravity / rotation link: magnetic figure-8 topology, hysteresis, patterned permalloy lattice layer (L202-205, L419-439); ferrotoroidic four-state analogy only (L540-545); "automatic claim that any magnetic vortex is a quantum qubit" retired (L994). Gravity: none.
- Open / parked / not-set items: §32 list (L943-959): ternary figure-8 geometry, winding placement, power switch, motor envelope, reinjection schematic, CENTER extraction, magnetic material, coercive targets, lattice material, path-score metric, retention times, decay curves. Power stage OPEN (L172-183, L750-754).
- Conflicts: none with canonical rules. Internal Builds: flat-top hex (L37) vs point-up hex in LOCK.md:11, MASTER_CURRENT_STATE.md:118, BUILD_BOOK.md:67; "rounded/circular lobes" for ternary figure-8 (L204) vs square figure-8 medium memory (L277) — two different figure-8s, consistent internally but differs from ARCHITECTURE.md nucleus-by-role scheme (round = sensor, square = motor).

## Contributor License Agreement   (`/home/user/Builds/CLA.md`)
- Gate / lifecycle: legal.
- Upstream / cites: LICENSE (L19).
- Core claim: non-assignment license; hardware CERN-OHL-S-2.0, firmware GPL-3.0+, docs CC-BY-SA-4.0 (L21-23).
- Equations: none
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## Copyright and ownership   (`/home/user/Builds/COPYRIGHT.md`)
- Gate / lifecycle: legal.
- Upstream / cites: CLA.md, LICENSE, CITATION.cff (L11, L21, L35).
- Core claim: author Mark Wright Adlard; licences by work type (L5, L17-19).
- Equations: none
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: formal registration separate (L45).
- Conflicts: none.

## Build order — CURRENT BUILD ORDER — BALANCED DEVICES TO CELL ARCHITECTURE   (`/home/user/Builds/CURRENT_BUILD_ORDER.md`)
- Gate / lifecycle: CELL_V1 gates 0, A–N (L51-79); "No layer count becomes canon because it looks symmetric." (L81).
- Upstream / cites: CELL_V1_ANTI_DRIFT.md, UPDATED_63_CELL_V1_STATEFUL_MUSCLE_MEMORY_BUILD.md, CELL_V1_BUILD_PACKET.md, UPDATED_62_CELL_V1_HEX_FIRST_INTERNALS_AND_SCALING.md, **ARCHITECTURE_POINT_PATH_FIELD_SCALE_RECURSION.md** (L9-13).
- Core claim: "state = memory / state transition = processing / repeated successful state transition = physical path training" (L28-30); "V0 is reference only, never the recovery reservoir" (L45); Gate I "Closed rotation — distinguish traveling/circulating phase/state from simultaneous switching, ringdown, or standing oscillation; test reversal" (L69); Project 4 "DC -> AC -> ROTATION ... or `RMF` when a rotating magnetic field is actually measured. Do not use `RC` for rotation" (L149-152); "lower-scale resolved volume behaving as one next-scale point without erasing its internal history" (L209); build law "prove path -> prove rotation" (L225-226).
- Equations: none.
- Point / Path / Field role: Point — resolved volume behaves "as one next-scale point without erasing its internal history" (L209); a lower-scale structure "must expose a reusable next-scale interface" (L171). Path — physical path training, route bias (L33), "prove path" before "prove rotation" (L225-226). Rotation — Gate I separates "traveling/circulating phase" from standing oscillation (L69). Field — none stated.
- Magnetism / gravity / rotation link: RMF only when measured (L152); "depth coupling is measured, not drawn into existence" (L170); "measurable 3D coupling where magnetic hardware is involved" (L208). Gravity: none.
- Open / parked / not-set items: 3x3x3 candidate only (L173); 2+2 M4, 3/3/3, hemispheres conditional (L75-79).
- Conflicts: none with canonical rules (L209 is consistent with parent/child "child keeps its own state"). Internal Builds: contradicts RC-as-rotation usage in ANDROID_CURRENT_BRAIN_BODY_ARCHITECTURE.md:15 and MASTER_CURRENT_STATE.md:676-678.

## Engine pointer — Engine   (`/home/user/Builds/ENGINE.md`)
- Gate / lifecycle: pointer.
- Upstream / cites: One-Wave-Science `Engine/MODULAR_PHYSICS_ENGINE.md`; Science **D-414** (LIGO and CERN pipelines) (L4-6).
- Core claim: "Builds may consume the Field bus. Builds may not invent a second physics." (L6).
- Equations: none
- Point / Path / Field role: "Field bus" consumed from Science (L6); nothing else stated.
- Magnetism / gravity / rotation link: none stated (LIGO pipeline named only).
- Open / parked / not-set items: none.
- Conflicts: none.

## Full build — FULL BUILD — current validation path   (`/home/user/Builds/FULL_BUILD.md`)
- Gate / lifecycle: evidence gate 1–8 (L48-55); stop rules (L59-65).
- Upstream / cites: none.
- Core claim: locked list = hardware-first, no clock, CENTER ≠ V_BUS, round body toroids, nuclei by role (L7-16); motor path "square figure-8 ... common two-round-toroid body interface → field / actuator coupling → inductive return → V_BUS → effect on next event" (L22-39).
- Equations: none.
- Point / Path / Field role: none stated ("field / actuator coupling", L33, generic).
- Magnetism / gravity / rotation link: magnetic hysteresis, ferrite/toroidal cores, multi-winding systems as established tech (L84). No gravity/rotation.
- Open / parked / not-set items: no torque, efficiency, recovery %, higher-mind claims (L90).
- Conflicts: none.

## Gate colors — superseded name   (`/home/user/Builds/GATE_COLORS.md`)
- Gate / lifecycle: superseded.
- Upstream / cites: THE_BRICK_SYSTEM.md; One-Wave-Science `Governance_I_Series/THE_BRICK_SYSTEM.md` (L3-5).
- Core claim: "Superseded name. Use THE_BRICK_SYSTEM.md." (L3).
- Equations: none
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## Grant architecture   (`/home/user/Builds/GRANT.md`)
- Gate / lifecycle: Phase I ask (L6); Phase II hypotheses (L48).
- Upstream / cites: cell-v1/CELL_CURRENT.md, BUILDERS_HALL.md (L5, L8).
- Core claim: round figure-8 on tiling sensor/compute cell; square figure-8 on motor cell only; "two plain round body toroids, not figure-8s, six windings as mirrored 3+3, the other face reversing every sign" (L18-20); "three differential axes, tip to tip: **A** heat, **B** gyro and vibration as one differential, **C** magnetic gradient" (L21); "base-to-base joints that pay tension and are not a second differential" (L22); coupling "as a phase shift between two intact windings that share flux" (L42).
- Equations: none.
- Point / Path / Field role: none stated by name. Axis C senses "magnetic gradient" (L21) [reviewer mapping: field-gradient channel, not stated as Field rate]. Axis B "gyro" senses rotation (L21) — no point/path distinction stated.
- Magnetism / gravity / rotation link: C axis = magnetic gradient sensing; B axis = gyro (rotation rate) + vibration. No statement of open/closed gradient or dL/dt; no gravity.
- Open / parked / not-set items: flower, lattice, larger motor field Phase II (L48).
- Conflicts: none with canonical rules. Internal Builds: GRANT_MAP.md:13 says "Two outer round figure-8 toroidal structures" vs GRANT.md:20 / LOCK.md:8 / ARCHITECTURE.md:13 "not figure-8s".

## Grant brief — CELL_V1 — interview / validation brief   (`/home/user/Builds/GRANT_CELL.md`)
- Gate / lifecycle: "Proposed hardware architecture ... unproven until bench measurements exist" (L3).
- Upstream / cites: none.
- Core claim: two plain round body toroids common to all roles, not figure-8 (L21-25); nuclei by role incl. "M4 cell: two triangular toroidal loops base-to-base" (L31-35); "Current core hardware is planar / 2D; the magnetic fields are 3D." (L37); square figure-8 "for grid / lattice alignment" (L32).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: toroidal nuclei; "motor / field consequence" (L54). No gravity/rotation.
- Open / parked / not-set items: evidence list (L103-109).
- Conflicts: none.

## Grant map   (`/home/user/Builds/GRANT_MAP.md`)
- Gate / lifecycle: WP0–WP6 (L33-65); `cell-v1/LOG.md` is the measurement gate (L7).
- Upstream / cites: cell-v1/CELL.md, LOG.md, SQUARE_FERRITE.md, DIFFERENTIALS.md, NO_CLOCK.md, REINJECT_BUS.md, ACTUATORS.md, CELL_ASSEMBLED.md (L71-78).
- Core claim: "Square figure-8 toroidal nucleus — retained-state brain-side structure on the lattice-bus / vagus-nerve side" (L11); "Two outer round figure-8 toroidal structures — combined outer electrical / magnetic field" (L13); six outer windings mirrored 3+3 (L14).
- Equations: E_in, E_rec, E_loss named (L51).
- Point / Path / Field role: none stated; outer structures give "combined outer electrical / magnetic field" (L13), "larger differential field response" (L59).
- Magnetism / gravity / rotation link: magnetic field from outer shell; no gravity/rotation.
- Open / parked / not-set items: L94 list.
- Conflicts: none with canonical rules. Internal Builds: "Two outer round figure-8" (L13, L59, L85) conflicts with "not figure-8 toroids" in ARCHITECTURE.md:13, LOCK.md:8, GRANT_CELL.md:25, GRANT.md:20; square figure-8 as the single nucleus (L11) vs role-specific nuclei elsewhere.

## Grant Option A — Native Magnetic Substrate Gating   (`/home/user/Builds/GRANT_OPTION_A_BUILD_PLAN.md`)
- Gate / lifecycle: Phase I/II milestones (L33-34).
- Upstream / cites: none.
- Core claim: "the coercivity ($H_c$) of square-loop ferrite toroids defines the decision band edges directly" (L4); "Threshold trip is an instantaneous physical domain flip ($d\Phi/dt$)" (L10); lattice = muscle memory as remanent $B_r$, distributed intelligence via figure-8 read heads, strain sensing (L26-28); "Diode-Gated PERMIT ... two-of-three consensus" (L20).
- Equations: `V_threshold = (H_c · l_path) / (N · G_sense)` (L18).
- Point / Path / Field role: none stated. `l_path` = magnetic path length (L18) — magnetic-circuit path, not Path rate.
- Magnetism / gravity / rotation link: magnetic coercivity as logic; closed toroid magnetic path length sets threshold. No gravity/rotation.
- Open / parked / not-set items: dual-coercivity / bias-wound cores Phase II (L34).
- Conflicts: none with canonical rules. Internal Builds: "Eliminates 4 LM339 comparators, 18 ladder resistors" (L11) presupposes a comparator/ladder baseline that MASTER_CURRENT_STATE.md:262-267 already forbids — framing only.

## Grant schematics — Schematics and proposed build   (`/home/user/Builds/GRANT_SCHEMATICS.md`)
- Gate / lifecycle: ask.
- Upstream / cites: cad/cell0_grant.svg, cad/the_cell.svg, cad/pcb_hex.svg, OneWave_Schematics_and_Proposed_Build.pdf (L4-7).
- Core claim: "fund Cell-0 + bus return ... on the same two references (home is not the bus)" (L9).
- Equations: none
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: PDF local only (L7).
- Conflicts: none.

## House map   (`/home/user/Builds/HOUSE.md`)
- Gate / lifecycle: map.
- Upstream / cites: Bridge-Comand BRIDGE_COMMAND.md, hive-pipe/bridge_doctor.py (L23-24); cell-v1/, algorithms/, cad/, gcac/ (L8-11).
- Core claim: "Four public homes. No fifth junk drawer." (L3); POINT-SPIN, GRAV-LAB science math in Science (L27); "GRAV_LAB engineering benches copy into Builds; the math stays Science." (L29).
- Equations: none
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated beyond repo routing.
- Open / parked / not-set items: none.
- Conflicts: none.

## Referenced parts — CELL_V1 Referenced Parts and Visual Guide   (`/home/user/Builds/Hardware_Packets/CELL_V1_REFERENCED_PARTS_AND_VISUAL_GUIDE.md`)
- Gate / lifecycle: "current referenced visual/build companion" (L3); no-assumption rule (L24-30).
- Upstream / cites: CELL_V1_BUILD_PACKET.md, UPDATED_63_CELL_V1_STATEFUL_MUSCLE_MEMORY_BUILD.md (L3); PDF companion (L20); external: Boybat et al. 2018, CuCrP2S6 memristors 2023, Knowm SDC, TI TLE2426, Wolfspeed C3M0021120D / CGD15SG00D2, TI sluaa58 (L40-92).
- Core claim: flat-sides-only ports (L8-18); "physical path adaptation as the hardware muscle-memory analogue" (L34); Knowm memristor stateful path (L48-58); V0 = TLE2426 rail splitter, "reference only" (L62-72); back-to-back SiC nerve gate (L76-92); two current domains: state/training lane vs power/actuator lane (L102-112).
- Equations: none.
- Point / Path / Field role: Path — repeated traversal physically trains the stateful path (L34, L118-128). Point/Field none stated.
- Magnetism / gravity / rotation link: "Returned inductive/magnetic energy goes to a measured reservoir" (L132); "path -> rotation -> seven-cell flower" ordering (L146). No gravity.
- Open / parked / not-set items: test coil, steering device, C_REINJECT OPEN (L134); Knowm sold out (L52).
- Conflicts: none with canonical rules. Internal Builds: memristor (non-magnetic) stateful path vs AVENUES.md:28 "Memristor crossbar as the cell" listed under "Do not wander into"; TLE2426 active rail splitter for V0 vs "no op-amp" rule (MASTER_CURRENT_STATE.md:261) — the TLE2426 is an op-amp-based splitter.

## Visual packet notes   (`/home/user/Builds/Hardware_Packets/CELL_V1_VISUAL_PACKET_NOTES.md`)
- Gate / lifecycle: pointer.
- Upstream / cites: CELL_V1_referenced_parts_breadboard_visual.pdf, CELL_V1_REFERENCED_PARTS_AND_VISUAL_GUIDE.md (L1).
- Core claim: accompanies PDF (L1).
- Equations: none
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## Lock list — CELL_V1 lock list   (`/home/user/Builds/LOCK.md`)
- Gate / lifecycle: locks; 2026-10-04 addendum (L77-87).
- Upstream / cites: cell-v1/CELL_CURRENT.md (L79).
- Core claim: common two plain round toroids, not figure-8 (L7-8); nuclei by role (L16-20); "All present core geometry is planar / 2D. Magnetic fields are 3D." (L24); 1.00 V axis, CENTER 0.50, HOLD 0.45–0.55 (L28-30); "**A** heat, up and down. **B** gyro and vibration, one differential. **C** magnetic gradient only." (L81); "Tip to tip, plus against minus, is the differential. Base to base pays tension." (L82-83); "Plus half wound one way, minus half the other way. The other face flips every arrow and is the lattice." (L84); "The nucleus is the only bridge." (L85); "The compute cell tiles. The motor-control cell does not." (L87).
- Equations: none.
- Point / Path / Field role: none stated by name. [reviewer mapping: nucleus as "only bridge" between two star points ≈ point; base-to-base joints ≈ path coupling; C gradient channel ≈ field — not stated.]
- Magnetism / gravity / rotation link: C axis = magnetic gradient only; B = gyro; opposite winding sense per half (L84). No open/closed or gravity statements.
- Open / parked / not-set items: L64-73 list (materials, turns, coupling, write depth, 3+3, torque, scale-up).
- Conflicts: none with canonical rules. Internal Builds: point-up hex (L11) vs flat-top canon (CELL_V1_CURRENT_BUILD_CANON.md:37).

## Master state — CELL_V1 + ALGORYTHM-ZER0 — MASTER CURRENT STATE   (`/home/user/Builds/MASTER_CURRENT_STATE.md`)
- Gate / lifecycle: "current master handoff ... read first" (L3-5); Tests A–E (L815-957); Phase-I validation statement (L961-969).
- Upstream / cites: RULES.md, BUILD.md, ARCHITECTURE.md, cell-v1/CELL.md, REINJECT_BUS.md, REAL_WORLD_BUILD_HANDOFF.md, PARTS.md, BREADBOARD.md, PRIOR_ART_AND_TEST_TARGETS.md, algorithms/README.md, ALGORITHM_ZERO_PRESENTATION.md, IMPLEMENTATION_STATUS.md, FOUR_BRANCHES_AND_UNIVERSAL_RULES.md, LEAN_INTO_ZER0.md, thresholds.md, algorithm_zero_locked_canon.json (L660-666, L777-791).
- Core claim: point-up hex with six tapered sectors, tips converge to centre, bases are faces (L118-139); FIELD-side toroid + VOID-side toroid per cell (L147-157); first flower = motor-control centre + six sensor cells (L198-205); decision rules "two agree -> push / one voice -> wait / opposition -> HOLD / gap -> wait" (L214-217); "**POINT / PATH / FIELD are also separate scale concepts.**" (L228); dedicated hysteretic body-state layer (domain-wall) beneath cells (L348-396); Zer0 X/Y/Z/T, L1–L6, F↔V cross-mirror (L534-577); DC/AC/RC working use: "DC = void / sustained bias / return-side relation; AC = field rotation / changing opposed lean; RC = remainder / returned consequence" (L676-678).
- Equations: `L1 ⊂ L2 ⊂ L3 ⊂ L4 ⊂ L5 ⊂ L6` (L555); `(0)t -> interaction -> consequence -> resolve -> (0)t+1` (L572-576); `F1<->V6 ... F6<->V1` (L561-566).
- Point / Path / Field role: explicitly "POINT / PATH / FIELD are also separate scale concepts" (L228), separate from bands and CHOICE/PIVOT/FLIP (L226). Path — "shared hysteretic lattice/path already carries prior-use bias" (L328), "settled hysteretic path means the next event does not start from zero" (L333). "Y = STRUCTURE / ROTATION" Zer0 branch (L536). "AC = field rotation" (L677).
- Magnetism / gravity / rotation link: multi-aperture cores/transfluxors, magnetic majority logic, "rotating field behavior" in multiphase geometry prior art (L402-431); "Do not claim a specific square-loop isolation mechanism until it is built" (L990). Gravity: none.
- Open / parked / not-set items: L712-725 (materials, MOSFET topology, six-sector field geometry, toroid winding pattern, threshold mechanism, retention, recovery, torque/field strength, Zer0 mapping); Zer0 JSON vs canon conflict (L656-666); reset winding candidate only (L872).
- Conflicts: (1) Soft vs canonical: "POINT / PATH / FIELD are also separate scale concepts" (L228) — canon treats them as three separate *rates* of one node; calling them scale concepts is a different framing (not a direct contradiction of separateness). (2) Soft vs canonical: "AC = field rotation" (L677) — canon says field curl is neither point rotation nor path rotation; labelling a changing opposed lean "field rotation" blurs the three-rate split. (3) Internal Builds: RC/rotation terminology vs CURRENT_BUILD_ORDER.md:152; point-up hex (L118) vs flat-top canon; "one-piece ... two-aperture figure-8" (L178-179) vs BUILD_BOOK.md:42 "two rings touching"; sensor-ring flower (L200-201) vs CURRENT_BUILD_ORDER.md:71 "one center + six same-orientation identical cells".

## Migration map   (`/home/user/Builds/MIGRATION_MAP.md`)
- Gate / lifecycle: routing map; "This map is not evidence that hardware has been validated." (L29).
- Upstream / cites: Bridge-Comand, Science repos, Mythos-and-Stories, VTC_BUILD_ARCHITECTURE.md, One_Wave_Bench, Workshop (L7-24).
- Core claim: content-preserving routing table (L14-24); split mixed files "magnetics → Builds, SSH → Bridge" (L28).
- Equations: none
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## Miniverse expansion — Expanding the One-Wave Miniverse   (`/home/user/Builds/Miniverse/EXPAND_MINIVERSE.md`)
- Gate / lifecycle: software process; tests required before merge (L318-346).
- Upstream / cites: AI_CANONICAL_START_HERE.md, UPDATED_50_SCLFS_LATTICE_FRAME_BINDING_VERIFICATION_AND_MINIVERSE_RUNTIME.md, Miniverse/README.md, room3d/README.md, desktop/README.md, AI_JETSON_TOOL_GUIDE.md, room3d/EXPERIMENT_LAB.md, room_manifest.json (L11-16, L157, L221).
- Core claim: "The stationary lattice does not silently move when an occupant moves." (L44); "New physics visuals are experiments/simulations unless separately established." (L53); 37-cell room, Baseline Zero (L55, L194).
- Equations: none.
- Point / Path / Field role: none stated. Body part "rotation each axis -6.3..6.3 radians" (L114) is avatar orientation only.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: next expansion points are "software tasks, not established physics claims" (L367-381).
- Conflicts: none. (Note: Jetson / room-server / SSH content belongs to Bridge-Comand per HOUSE.md:16-21 and MIGRATION_MAP.md:22-24 — placement inconsistency only.)

---

## Slice summary

### (a) Nodes / chapters in slice bearing on Point, Path, Field, rotation, magnetism, gravity, inertia, mass, resistance, lattice organization or locking

Science node IDs cited in this slice (all in `Android_Body/Android_Body_Functional_Architecture.md` unless noted):
- **A-111** — neighbor-average field update `Delta_psi_i = <psi_j> - psi_i`; lattice communication (L35-39). Lattice organization.
- **G-710** — regulation `Q_n = k_n F_n` (L50). Not rotation/magnetism.
- **E-507** — scale invariance, same mechanism at three scales (L67). Scale recursion.
- **B-203 / B-204** — compression/expression (L72). Maps to CELL band scale.
- **B-221** — six-step MOVE/HOLD/BREAK/LOOP (L76-79). State transition only.
- **D-408 / D-411 / D-412** — triangular/hex lattice, 3:1 vs 6:1 counting, simulation receipts (L84-90). Lattice organization.
- **C-312** — operational hardware chain (L24-25, L99-100). Hardware pipeline.
- **I-02 / I-05** — proof ladder; consciousness reading routed to Books (L11, L105). Gate only.
- **G-719, B-213, G-711, G-722** — audit / grounding corrections, motor-memory boundary (L9-10, L43-57, L165). Not rotation.
- **D-414** — LIGO/CERN pipelines; "Builds may not invent a second physics" (`ENGINE.md:6`). Field-bus boundary.

None of the canonical rotation/magnetism nodes (C-306, C-307, C-311, C-319, C-320, G-749, G-750, G-769, A-115, E-528, E-530) is cited anywhere in this slice.

How the build hardware implements point / path / field and magnetic open/closed (what the docs state, then my mapping):
- **Point (stated):** `ANDROID_CURRENT_BRAIN_BODY_ARCHITECTURE.md:15,17,176`: a resolved loop or rotation becomes "one effective point/reference for the next scale". `CURRENT_BUILD_ORDER.md:209`: a resolved volume behaves "as one next-scale point without erasing its internal history". `MASTER_CURRENT_STATE.md:228`: POINT / PATH / FIELD are separate. Hardware: CENTER at 0.50 V, plus the nucleus or figure-8 "home" (`BUILD_BOOK.md:111`, `CELL_V1_CURRENT_BUILD_CANON.md:289-294`, `LOCK.md:85` "nucleus is the only bridge"). [reviewer mapping] No hardware element is assigned angular momentum L = Iω. The nearest is `AVENUES.md:9`: a spinning mass "keeps current after PERMIT drops". That matches the rule that a body keeps the point spin it already has.
- **Path (stated):** the hysteretic path layer and lattice path scoring (`CELL_V1_CURRENT_BUILD_CANON.md:380-411`, `MASTER_CURRENT_STATE.md:328-333`, `ARCHITECTURE.md:57`, `Hardware_Packets/...GUIDE.md:34`). Also the six wedge routes, tip-to-tip inside a cell and base-to-base between cells (`ARCHITECTURE.md:28-31`). `CURRENT_BUILD_ORDER.md:69,225-226` separates traveling or circulating phase (Gate I, "closed rotation") from standing oscillation, and orders "prove path → prove rotation". This is the closest the build comes to path rotation, the ride.
- **Field (stated):** the round body toroids' "combined 3D field" as a candidate body-state field (`ARCHITECTURE.md:43-48`). The Helmholtz shared near-uniform B (`ARCHITECTURE.md:51-57`). The outer shell's "combined outer electrical / magnetic field" (`GRANT_MAP.md:13`). The C axis is "magnetic gradient only" (`LOCK.md:81`, `GRANT.md:21`). The B axis is a gyro (`LOCK.md:81`).
- **Magnetic open/closed (hardware only):** the build uses closed magnetic circuits throughout:
  - closed toroids (`AVENUES.md:10`);
  - square-loop cores where the threshold is set by the magnetic path length (`GRANT_OPTION_A_BUILD_PLAN.md:18`);
  - "do not cut a path through the core" (`BUILDERS_HALL.md:82`);
  - coupling by shared flux between intact windings (`BUILDERS_HALL.md:67`).

  The open-volume elements are the Helmholtz uniform field and the 3D toroid fields ("planar 2D cores, 3D fields": `ARCHITECTURE.md:37`, `LOCK.md:24`, `GRANT_CELL.md:37`). **No doc states the canonical rules**: dL/dt = 0 for an open gradient, dL/dt = −γL for a closed one, "magnetism opens the point", or g = −α K_L ∇χ. None of these is stated in this slice.
- **Gravity:** excluded from Builds. Sources: "Cosmology in Builds" is closed (`AVENUES.md:23`); a gravity-theory grant is out of scope (`BUILDERS_HALL.md:98`); GRAV_LAB math stays in Science (`HOUSE.md:29`, `ALL_GITHUB_INTO_THREE.md:15,35`).
- **Lattice organization / locking:** the hex flower and lattice path scoring (`CELL_V1_CURRENT_BUILD_CANON.md:712-738`). "The compute cell tiles. The motor-control cell does not." (`LOCK.md:87`). The bound-lattice point-rate locking (Moon 1:1, Mercury 3:2) is not stated.

### (b) Conflicts found
Against the canonical rules there are no hard contradictions. Three soft or terminology tensions:
1. `MASTER_CURRENT_STATE.md:228` calls "POINT / PATH / FIELD" "separate scale concepts". The canon defines them as three separate rates of one node. The two framings differ.
2. `MASTER_CURRENT_STATE.md:677` says "AC = field rotation". The canon says field curl is neither point rotation nor path rotation, so this label blurs the three-rate split.
3. `ANDROID_CURRENT_BRAIN_BODY_ARCHITECTURE.md:15,175,181` uses "rotation" (the "RC loop") and `CELL_V1_CURRENT_BUILD_CANON.md:557-566` uses "opposing rotations". Neither says whether the rotation is point rotation (carries L) or path rotation (the ride).

Builds-internal inconsistencies (not canonical-rule conflicts, recorded for the orchestrator):
- **RC as rotation.** `ANDROID_...:15` and `MASTER_CURRENT_STATE.md:676-678` use RC for rotation. `CURRENT_BUILD_ORDER.md:152` says "Do not use `RC` for rotation".
- **Outer toroids.** `GRANT_MAP.md:13,59,85` says "two outer round figure-8". `ARCHITECTURE.md:13`, `LOCK.md:8`, `GRANT.md:20` and `GRANT_CELL.md:25` say the body toroids are not figure-8s.
- **Hex orientation.** `CELL_V1_CURRENT_BUILD_CANON.md:37` is flat-top. `LOCK.md:11`, `MASTER_CURRENT_STATE.md:118` and `BUILD_BOOK.md:67` are point-up.
- **Resistors and comparators.** `BUILD_BOOK.md:38-40` uses resistor loads and a divider to make 0.50 V, and `BUILD_BOOK.md:133` lists LM339 as an option. Against these: `BUILDERS_HALL.md:20` ("CENTER ... not a resistor divider"), `ARCHITECTURE.md:128`, and `MASTER_CURRENT_STATE.md:262-267`.
- **Figure-8 construction.** `BUILD_BOOK.md:42,109` uses "two rings touching". `MASTER_CURRENT_STATE.md:178-179` specifies a "one-piece two-aperture" core.
- **Hardware packet parts.**
  - `Hardware_Packets/CELL_V1_REFERENCED_PARTS_AND_VISUAL_GUIDE.md:48` uses a memristor stateful path, which `AVENUES.md:28` lists under "do not wander into".
  - The same guide (L62-70) uses the TLE2426, an active rail splitter, against the no-op-amp rule (`MASTER_CURRENT_STATE.md:261`).
- **Flower composition.** `MASTER_CURRENT_STATE.md:200-201` has a motor centre with six sensor cells. `CURRENT_BUILD_ORDER.md:71` has "six same-orientation identical cells".

### (c) Cross-references outside the slice that matter for point rotation or magnetism
- `ARCHITECTURE_POINT_PATH_FIELD_SCALE_RECURSION.md` — cited as authority 5 (`CURRENT_BUILD_ORDER.md:13`). This is the Builds doc most likely to state Point/Path/Field and rotation explicitly.
- `cell-v1/HELMHOLTZ.md` (`ARCHITECTURE.md:53`): the shared magnetic field, uniform B with ∇B ≈ 0.
- `cell-v1/CELL_CURRENT.md` (`GRANT.md:5`, `LOCK.md:79`): the A heat / B gyro / C magnetic-gradient axes.
- Further cell-v1 files: `cell-v1/SQUARE_FERRITE.md`, `ACTUATORS.md`, `REINJECT_BUS.md`, `NUCLEUS_TOROID_TYPES.md`, `CELL_ASSEMBLED.md`, `PRIOR_ART_AND_TEST_TARGETS.md`.
- Other Builds docs: `UPDATED_62_CELL_V1_HEX_FIRST_INTERNALS_AND_SCALING.md`, `UPDATED_63_CELL_V1_STATEFUL_MUSCLE_MEMORY_BUILD.md`, `CELL_V1_BUILD_PACKET.md`, `CELL_V1_ANTI_DRIFT.md`.
- `algorithms/FOUR_BRANCHES_AND_UNIVERSAL_RULES.md`: the Zer0 branch "Y = STRUCTURE / ROTATION".
- Science: `Engine/MODULAR_PHYSICS_ENGINE.md` and D-414 (Field bus, "no second physics"); `Governance_I_Series/THE_BRICK_SYSTEM.md`.
- Science repos: POINT-SPIN and GRAV-LAB (point spin and gravity math live there, not in Builds).
- A-111, E-507, D-408, D-411 (lattice / scale).
