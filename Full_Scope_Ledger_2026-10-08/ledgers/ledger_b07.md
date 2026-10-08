# Ledger b07 — Builds repo (`/home/user/Builds`), 36 files, all read in full

Scope note: this slice is the Builds (engineering) repo, not One-Wave-Science. Almost no file carries Science YAML gate metadata. "Nodes cited" means One-Wave-Science node/chapter IDs named in the file; local work-package IDs (L0..L12, G0..G7, C1..C10, etc.) are listed separately as "local IDs" and are not Science nodes. Where a file says nothing about Point / Path / Field or magnetism, the entry says "none stated". The build-hardware reading of point/path/field and magnetic open/closed is collected in the Slice summary, section (d).

---

## cell-v1 — Views Up & Actions Down, 4x4 lattice couplings   (`cell-v1/VIEWS_ACTIONS.md`)
- Gate / lifecycle: none (no front matter; architecture prose).
- Upstream: none cited. Downstream / cites: no Science nodes. Local terms: BASELINE/DELTA/HEADING/RESULT views; PULL/PUSH/FLIP/PASS actions.
- Core claim: "The lattice is the full body state. It is one continuous magnetic medium spanning the entire collective group." (L3). "These sixteen couplings are not a software lookup table. They are sixteen physical analog routing paths through the figure-8 read/write stack." (L56). "The last action down becomes the new view up" (L62).
- Equations: views use $d\Phi/dt$ (L14, L30); recursion View Up -> Action Down -> Lattice Changes -> New View Up (L64). No physics equation beyond dPhi/dt.
- Point / Path / Field role: none stated in canonical terms. Hardware reading: the figure-8 read head is a local reader/writer on one shared magnetic medium (L9, L24). "Route inward/outward" (L28-29) are routing actions. "Write at cell 1 propagates across the shared medium to cell 7" (L72) is a field/medium propagation statement. No point spin, no L, no path ride.
- Magnetism / gravity / rotation link: FLIP = "Invert magnetic domain orientation" (L30); PUSH = "deepen trace past $H_c$" (L29); PASS = "No write, let state stand (coast)" (L31); RESULT = "Remanence state post-write" (L16). No gravity, no rotation.
- Open / parked / not-set items: none declared. No evidence status given.
- Conflicts: none with the canonical rules. Internal tension: it calls the hardware magnetic medium "the lattice" (L3) with no qualifier, while `validation/TRANSFLUXOR_MULTISCALE_TRIANGULATION.md:19` requires material lattice, domain pattern, flux-network topology and the One-Wave lattice to be kept as "FOUR different concepts". It also gives no evidence class, which `CELL_V1_CONCEPT_MAP.md:23` requires.

## cell-v1 — CELL_V1 View / Action Stack   (`cell-v1/VIEW_ACTION_STACK.md`)
- Gate / lifecycle: none in front matter. Validation boundary (L149-175) marks the integrated stack as experimental.
- Upstream: `PROVEN_PARTS_REFERENCES.md` (L165), reference IDs R1-R8 (L168-173). Downstream / cites: no Science node IDs.
- Core claim: "three paired differentials ... BC–DC ... TC–AC ... QC–RC" (L5-9). "All three preserve the same active CENTER/(0) reference" (L11). BC–DC "is the point/state layer" (L19). QC–RC "is the higher rotating/field relation" (L36). "No IC/chip implementation is required" (L50). "never promote a mechanism-level reference into proof of the complete CELL loop" (L175).
- Equations: `B_view = X x_hat + Y y_hat`; `|B_view|^2 = X^2 + Y^2`; `theta = atan2(Y, X)` (L43-45).
- Point / Path / Field role: The file itself uses "point" and "field" as layer names. Point = BC–DC "point/state layer" (L19), i.e. a signed polarity state, not a spinning point with L. Path = TC–AC "alternating out-and-back physical traversal around CENTER" (L23) and "etched hysteretic lattice paths = distributed muscle memory" (L132-133); "process/path history is the memory mechanism" (L146). Field = QC–RC rotating magnetic vector from two orthogonal components in the "square figure-8 toroidal nucleus" (L38-45). No L = I omega, no inertia, no resistance.
- Magnetism / gravity / rotation link: rotation here is rotation of a field vector angle theta (L45), from resolver/rotating-field precedents R1/R3 (L168). Hysteretic memory via ferrite R4 and domain-wall paths R5/R6 (L172). Reinjection via inductive return to V_BUS, R8 (L135, L173). No gravity.
- Open / parked / not-set items: "Exact winding geometry and whether the square figure-8 realizes the required vector field remain bench/simulation targets" (L48). Eight first tests (L153-160). Mapping from four actions to A/B/C is experimental (L171). Whether a MOSFET switches at ≤1 V gate drive is untested (L196). Reinjection that does not disturb CENTER is experimental (L173).
- Conflicts: no direct contradiction. Risk of conflation: "rotating" at QC–RC (L9, L36, L116) is field-vector rotation (field curl / direction), and L19 calls BC–DC "the point/state layer". Canon keeps point rotation (G-749, carries L), path rotation (G-769) and field curl separate. Nothing here claims L, so these must not be read as point rotation. Terminology: "RC" means "rotating-current" here (L9), "last hold" in `gcac/THEORY.md:4`, and resistor-capacitor in `hardware/wave_reader_v1.md:15`.

## cell-v1 — WEIGHT = LEAN   (`cell-v1/WEIGHT_LEAN.md`)
- Gate / lifecycle: none.
- Upstream / downstream: none cited.
- Core claim: "0.45–0.55 V is HOLD. 100 mV of wobble ... Not a commit." (L5). Seven-level commit table (L9-17). "Gaps stay dead. 0.00–0.10 and 0.90–1.00 = terminal. Not ±4." (L19-20).
- Equations: voltage band table only (L11-17).
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none declared.
- Conflicts: none with the canonical rules. Internal: "Gaps stay dead" (L19), yet +1 (0.55–0.60) and −1 (0.40–0.45) share their edges with HOLD (0.45–0.55) with no dead gap, while the other bands are separated by gaps (for example 0.60–0.65 and 0.35–0.40). L22 says "±1 is the first step out of the wobble", so the shared edges at 0.45 and 0.55 are ambiguous.

## digital-cell — L0 Digital Cell   (`digital-cell/README.md`)
- Gate / lifecycle: "software reference contract, not proof of analog CELL physics" (L14).
- Upstream: **W-010** (L3, "Deterministic executable reference for W-010"). Downstream: DCACRC-IR REFERENCE/DIFF/LEAN semantics (L22).
- Core claim: "FIELD and VOID are explicit signed candidate values" (L5); `difference = FIELD - VOID` (L7).
- Equations: `difference = FIELD - VOID`; difference > t -> POSITIVE; < −t -> NEGATIVE; else HOLD (L7-12).
- Point / Path / Field role: FIELD is used as a signed software value, not a physical field. Point/Path: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: no completed IR compiler (L22).
- Conflicts: none.

## foreman — One-Wave Foreman Workstation   (`foreman/README.md`)
- Gate / lifecycle: job lifecycle `IDLE → PRIMED → EXECUTING → VECTORING → RESOLVING → DONE` (L20); DONE needs acceptance criteria plus a receipt (L22).
- Upstream / downstream: Builds, One-Wave-Science, Bridge-Comand (L5); planned adapters (L28-34). No nodes.
- Core claim: "The Foreman does not decide scientific truth and does not mark work complete from prose." (L5).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: five planned adapters (L30-34).
- Conflicts: none.

## gcac — GCAC README   (`gcac/README.md`)
- Gate / lifecycle: none. Copied from the old GCAC repo (L3).
- Upstream / downstream: gate.py, ladder.py, ternary.py (L6-8).
- Core claim: relocation note only.
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: old repo can be deleted (L3).
- Conflicts: none.

## gcac — GCAC theory   (`gcac/THEORY.md`)
- Gate / lifecycle: falsifier stated (L6).
- Upstream / downstream: none.
- Core claim: "Millivolt = action you can override. Microvolt feeling inverted, does not fire the gate." (L3). "DC = hold. AC = drive across dead zone. RC = last hold." (L4).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: "if a MOSFET pair cannot keep a 5-unit dead belt under Jetson rail noise, the chart is cosplay" (L6). This is untested.
- Conflicts: none with the canonical rules. Terminology: "RC = last hold" (L4) disagrees with `VIEW_ACTION_STACK.md:9`, where QC–RC is the rotating-current relation.

## hardware — Wave Reader V1   (`hardware/wave_reader_v1.md`)
- Gate / lifecycle: "UNVERIFIED HARDWARE PROPOSAL — build/test/dismiss" (L3).
- Upstream / downstream: none cited. Hardware: ADS131A02 ADC, 128 kSPS, Jetson Orin, HP EliteDesk 800 G4 Mini (L25-29).
- Core claim: a measurement-first acquisition path (L7). "Do not label traces as reinjection, memory, Field, Void, lattice density, or wave collapse solely from shape." (L64).
- Equations: none.
- Point / Path / Field role: none stated. The "optional field or coil-current channel" (L38) is a measurement channel only.
- Magnetism / gravity / rotation link: none stated beyond the optional coil-current/field probe.
- Open / parked / not-set items: every component is unqualified until checked (L31); eight qualification tests (L53-60).
- Conflicts: none.

## jetson-brain — Jetson GPU FIELD Adapter Plan   (`jetson-brain/JETSON_GPU_FIELD_PLAN.md`)
- Gate / lifecycle: gold comparison gate (L22-32).
- Upstream / downstream: the reference FIELD backend; Foreman receipts (L20).
- Core claim: "GPU speed alone does not promote an implementation." (L32).
- Equations: none.
- Point / Path / Field role: FIELD = GPU parallel compute; VOID = CPU control and validation (L13-20). This is software mapping only.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: GPU adapter not built.
- Conflicts: none.

## jetson-brain — Jetson Two-State Brain Runtime   (`jetson-brain/README.md`)
- Gate / lifecycle: v0 deterministic CPU backend (L20).
- Upstream / downstream: loop_router.py; seven planned adapters (L39-45).
- Core claim: "This is an engineering mapping, not a claim that CPU/GPU hardware physically embodies Field/Void." (L11). Router law `OBSERVE → FIELD → VOID → RESOLVE → EMIT/HOLD → RECEIPT → REENTER` (L24).
- Equations: none.
- Point / Path / Field role: FIELD = GPU, VOID = CPU (L7-8). Software only.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: all Jetson adapters are planned only.
- Conflicts: none.

## jetson — AI Jetson Tool Guide   (`jetson/AI_JETSON_TOOL_GUIDE.md`)
- Gate / lifecycle: operational guide; Hive Pipe calls require `intention` and `consequence` (L3-6).
- Upstream: AI_BRIDGE_START_HERE.md, AI_CODE_BRIDGE.md, JETSON_AI_ACCESS.md, Miniverse/room3d docs (L12, L143, L156, L180-184, L320). No Science nodes.
- Core claim: terminal path `client -> HTTPS/MCP -> gateway.py -> terminal_parser.py -> Jetson process` (L17). Six Miniverse moves A±/B±/C± (L169).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## jetson — Jetson Access and Terminal Entry Point   (`jetson/JETSON_ACCESS_AND_TERMINAL.md`)
- Gate / lifecycle: operational rules (L5-12).
- Upstream: README.md, AI_CANONICAL_START_HERE.md, AI_FOREMAN_WORK_REGISTER.md, MEGA_CITY_LOOPER_OBJECTIVE.md, Virtual_Breadboard collaboration and log files (L127-132).
- Core claim: "Do not guess a Jetson IP address." (L7). "The experimental lattice/storage architecture is a later track." (L108).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: the lattice/storage track is parked until integrity is proven (L108).
- Conflicts: none.

## jetson — Jetson AI Access, canonical bidirectional paths   (`jetson/JETSON_AI_ACCESS.md`)
- Gate / lifecycle: 12-step acceptance test (L368-385).
- Upstream: AI_BRIDGE_START_HERE.md, AI_CODE_BRIDGE.md, External_Work/README.md. No nodes.
- Core claim: one canonical gateway, Hive Pipe on :8765 (L44-57); SSH is the independent recovery route (L273-274).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## jetson — Jetson DeepSeek Brain Buddy   (`jetson/JETSON_DEEPSEEK_BRAIN_BUDDY.md`)
- Gate / lifecycle: verified acceptance receipt (L187-198).
- Upstream: GENERAL_REFERENCE_RULES.md, AI_CANONICAL_START_HERE.md, **I-06** `Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md` (L14-18, L138-140).
- Core claim: "DeepSeek must use the One-Wave repository as its first authority" (L9). "Every flip returns through reference." (L161). Must "report gate/lifecycle from YAML/front matter" (L142).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none.

## jetson — Jetson Gemini minimal-token worker   (`jetson/JETSON_GEMINI_MINIMAL.md`)
- Gate / lifecycle: escalation order (L10-20).
- Upstream: GEMINI.md, GEMINI_TASK_TEMPLATE.md, scripts (L28-33). No nodes.
- Core claim: "External model output is a candidate/review, not self-validating evidence." (L180-181).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: Miniverse agent gateway is a later step (L163-167).
- Conflicts: none.

## jetson — Jetson Orin + OpenClaw Runtime Contract   (`jetson/JETSON_OPENCLAW_RUNTIME.md`)
- Gate / lifecycle: branch-step law, three-strike rule, hard stop (L100-176).
- Upstream / downstream: none cited.
- Core claim: "Field and Void do not own the loop. They operate inside the bounded step selected by M4." (L42). Field = GPU priority (L54-68); Void = CPU oversight that issues ALLOW/CORRECT/OVERRIDE/HOLD/ESCALATE (L70-83).
- Equations: none.
- Point / Path / Field role: Field and Void are software roles only. Point/Path: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none.
- Conflicts: none with the canonical rules. Terminology: "M4" here is the OpenClaw orchestration layer (L27), but in `maps/CELL_V1_CONCEPT_MAP.md:13` M4 is a hardware routing nucleus. `validation/SCIENCE_CONNECTIONS.md:28` notes that the canonical M4 meaning still has to be checked.

## maps — Android Cell → Body → Cortex   (`maps/ANDROID_CELL_TO_CORTEX_MAP.md`)
- Gate / lifecycle: "engineering hypotheses ... not claims that the android reproduces biological cortex" (L26).
- Upstream / downstream: local IDs D1-D10 (L36-45). No Science nodes.
- Core claim: a scale ladder from CELL to BODY (L4). "Each scale must expose a compressed state/interface to the next scale" (L6).
- Equations: none.
- Point / Path / Field role: none stated. CLUSTER/LATTICE appears only as a scale rung (L4).
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: all work packages D1-D10.
- Conflicts: none.

## maps — Animator product map   (`maps/ANIMATOR_PRODUCT_MAP.md`)
- Gate / lifecycle: gold acceptance list (L9-21).
- Upstream / downstream: local IDs A1-A10. No nodes.
- Core claim: "It is not a physics simulator." (L4).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: A1-A10.
- Conflicts: none.

## maps — CELL_V1 canonical concept map   (`maps/CELL_V1_CONCEPT_MAP.md`)
- Gate / lifecycle: "architecture intent, not proof that the integrated cell works" (L23).
- Upstream: `cell-v1/CELL_V1_2026-09-28_CORRECTION.md` (L3, authority). Downstream: local IDs C1-C10 (L26-35).
- Core claim: "FIELD half ⇄ CENTER/reference/nucleus ⇄ VOID half" (L6). "Three mirrored differential axes A/B/C surround the cell." (L8). "Shared lattice represents collective body state. Only unresolved/excess conditions need propagate upward." (L20-21).
- Equations: none.
- Point / Path / Field role: none stated in canonical terms. Hardware reading: CENTER/nucleus is the local reference point (a hysteretic nucleus, L11-15); "shared body/path hysteresis" (L19) is a path-memory layer; the two outer round toroids are the "common FIELD/VOID body differential interface" (L16).
- Magnetism / gravity / rotation link: hardware is two-aperture figure-eight hysteretic nuclei (square for the centre motor cell, round for six sensor cells, L11-12). M4 routing is "TIP⇄TIP internally and BASE⇄BASE between cells" (L13). M5 is pentagonal, M6 hexagonal (L14-15). No gravity, no rotation.
- Open / parked / not-set items: "Geometry, thresholds, materials, coupling, reinjection and stability require bench validation." (L23).
- Conflicts: none with the canonical rules. The M4 term clash is noted above.

## maps — Digital CELL + Two-State Brain ladder   (`maps/DIGITAL_CELL_TWO_STATE_BRAIN_LADDER.md`)
- Gate / lifecycle: "not evidence that the physical analog CELL works" (L5); L12 "not a claim of consciousness" (L73).
- Upstream: Algorythm-Zer0 (L133-135). Downstream: local IDs L0-L12. No Science nodes.
- Core claim: "FIELD — expressed/current/external-facing candidate state. VOID — compressed/latent/internal-facing counterstate." (L11-12). Software cycle (L18-28).
- Equations: none.
- Point / Path / Field role: FIELD and VOID are software states. Point/Path: none stated.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: the build order L0 to L12 (L137-144).
- Conflicts: none.

## maps — Hyperbolic Evolution Chamber   (`maps/HYPERBOLIC_EVOLUTION_CHAMBER.md`)
- Gate / lifecycle: real-world lock gate: REJECTED / HOLD / SIMULATION-SUPPORTED / BUILD-CANDIDATE; "Only physical receipts can later produce bench-supported status" (L97-103).
- Upstream: "must consume the One-Wave Science assumption/transformation contracts" (L20). Local IDs G0-G7 goblins. No Science node IDs.
- Core claim: "A simulated survivor is a build candidate, not proof that the physical device works." (L7). "Rendering never changes solver state." (L24). "Do not silently impose hyperbolic spacetime/physics on ordinary CELL simulations." (L39).
- Equations: none.
- Point / Path / Field role: none stated. The capability list includes "fields / potentials" and "magnetic / hysteretic state" (L28-30) as solver modules.
- Magnetism / gravity / rotation link: the magnetic/hysteretic state is a module (L30). No gravity, no rotation law.
- Open / parked / not-set items: whole build order (L172-184).
- Conflicts: none.

## maps — Sensory Cortex + DC/AC/RC program   (`maps/SENSORY_CORTEX_DC_AC_RC_PROGRAM.md`)
- Gate / lifecycle: "No dream output may be relabeled as measured real-world evidence." (L61).
- Upstream / downstream: local IDs H0-H6, V0-V6, S1-S12. No Science nodes.
- Core claim: DCACRC-IR primitives REFERENCE, DIFF, LEAN, COUPLE, INTEGRATE, GATE, FIELD, EMIT, SOURCE (L10-18).
- Equations: primitive signatures only, for example `DIFF A B -> D`, `INTEGRATE x tau -> h` (L11-14).
- Point / Path / Field role: `FIELD group -> combined` means a combined-state projection (L16). `GATE condition -> path` is a threshold route (L15). Software only; no point.
- Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: S11 analog backend waits until CELL primitives pass (L74).
- Conflicts: none.

## skills — Gemini Brain Buddy skill   (`skills/gemini-brain-buddy/SKILL.md`)
- Gate / lifecycle: completion requires `one-wave-gemini-receipt/v1` with `status=COMPLETE` (L27). Proof run 36585092067 (L39-45).
- Upstream: RESOLUTION_PROTOCOL.md, grounded-peer-dialogue.yml. No nodes.
- Core claim: "repo lens always comes first. Metadata is second. External measured data is third." (L14). "Never upgrade a scientific claim merely because Gemini agrees with it." (L49).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: none stated (it mentions CERN/GWOSC data sources only, L24).
- Open / parked / not-set items: none.
- Conflicts: none.

## two-ai-dialogue — Live Dialogue Adapter Contract   (`two-ai-dialogue/ADAPTER_CONTRACT.md`)
- Gate / lifecycle: LIVE acceptance needs six items (L46-52).
- Upstream / downstream: requests/*.json; Bridge-Comand fallback (L42). No nodes.
- Core claim: "Do not request or store hidden chain-of-thought." (L23).
- Equations: none. Point / Path / Field role: none stated. Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none. Conflicts: none.

## two-ai-dialogue — AI-to-AI Invocation Contract   (`two-ai-dialogue/AI_INVOCATION_CONTRACT.md`)
- Gate / lifecycle: "canonical operating instruction" (L3); COMPLETE / HOLD / FAILED (L64-72).
- Upstream: brain_buddy.py, SKILL.md, GEMINI_BRAIN_BUDDY_ROUTE.md, gemini_adapter.py (L26-28, L89-92). No nodes.
- Core claim: "None of these alone proves a physical/scientific claim discussed by the AIs." (L110).
- Equations: none. Point / Path / Field role: none stated. Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none. Conflicts: none.

## two-ai-dialogue — Continuation Status   (`two-ai-dialogue/CONTINUATION_STATUS.md`)
- Gate / lifecycle: Current HOLD, OpenAI HTTP 429 on request `cell-v1-needs-001`, run 36496957876 (L20-23).
- Upstream / downstream: RESOLUTION_PROTOCOL.md. No nodes.
- Core claim: "Do not erase this HOLD or mark the feature complete merely because a later workflow is green." (L49).
- Equations: none. Point / Path / Field role: none stated. Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: the live alternating runner is not finished (L36-47). Conflicts: none.

## two-ai-dialogue — Gemini Brain Buddy Route Authority   (`two-ai-dialogue/GEMINI_BRAIN_BUDDY_ROUTE.md`)
- Gate / lifecycle: "canonical route authority" (L3); seven-item proof of success (L26-33); verified 2026-09-29 at commit a29b36c (L39-45).
- Upstream / downstream: RESOLUTION_PROTOCOL.md. No nodes.
- Core claim: "repo lens first, metadata second, external measured wave data third" (L9).
- Equations: none. Point / Path / Field role: none stated. Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none. Conflicts: none.

## two-ai-dialogue — One-Wave Lens for Peer AIs   (`two-ai-dialogue/ONE_WAVE_LENS.md`)
- Gate / lifecycle: "interpretation contract, not evidence that One-Wave is physically correct" (L3).
- Upstream / downstream: none cited.
- Core claim: "One-Wave does not assume fundamental particles." (L8). Derivation ladder `LATTICE/BASE STATE -> PROPAGATION -> COUPLING/INTERFERENCE -> STABLE DYNAMIC STRUCTURE -> STRUCTURE-STRUCTURE INTERACTION -> SCALE/COMPRESSION -> OBSERVABLE` (L14). "FIELD means expressed/current interaction/state. VOID means counterstate/unexpressed potential." (L18).
- Equations: none.
- Point / Path / Field role: "path" appears only in the ontology list (L8). The "spin/angular response" observable is named (L10). No point / path / field rate separation is stated.
- Magnetism / gravity / rotation link: none stated beyond "spin/angular response" as an observable class (L10).
- Open / parked / not-set items: "The lattice is a candidate substrate/model under test" (L13).
- Conflicts: none. Note: L18 defines FIELD as "expressed/current interaction/state". That is a software/ontology reading and differs from the canonical Field = curl/wake/compression/gradient rate. It is not a contradiction but it is a different sense of the word.

## two-ai-dialogue — Peer Advice Pathways   (`two-ai-dialogue/PEER_ADVICE_PATHWAYS.md`)
- Gate / lifecycle: Gemini PROVEN; OpenAI HOLD (L35-43).
- Upstream / downstream: provider registry; Bridge-Comand (L92). No nodes.
- Core claim: "Mode changes roles, not evidence standards." (L88).
- Equations: none. Point / Path / Field role: none stated. Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: OpenAI awaits a COMPLETE receipt (L43). Conflicts: none.

## two-ai-dialogue — Two-AI Dialogue Box v0   (`two-ai-dialogue/README.md`)
- Gate / lifecycle: v0 proves orchestration only (L35).
- Upstream: CONTINUATION_STATUS, PEER_ADVICE_PATHWAYS, provider-registry.json, RESOLUTION_PROTOCOL, AI_INVOCATION_CONTRACT (L47-51). It is called a small proof before the Hyperbolic Evolution Chamber (L3).
- Core claim: the loop `QUESTION → CHATGPT → GEMINI → … → RESOLVE → FINAL` (L13).
- Equations: none. Point / Path / Field role: none stated. Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: live model transport (L35). Conflicts: none.

## two-ai-dialogue — Repository Reading Protocol   (`two-ai-dialogue/REPO_READING_PROTOCOL.md`)
- Gate / lifecycle: six evidence classes (L18-24).
- Upstream / downstream: Builds vs One-Wave-Science vs Bridge-Comand scopes (L7-9).
- Core claim: "Newer explicit corrections override contradictory older notes." (L12). "A commit or passing software test does not prove a physical theory." (L26).
- Equations: none. Point / Path / Field role: none stated. Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none. Conflicts: none.

## two-ai-dialogue — Resolution Protocol   (`two-ai-dialogue/RESOLUTION_PROTOCOL.md`)
- Gate / lifecycle: terminal states AGREED_RESOLUTION / AGREED_NEXT_ACTION / HOLD / MAX_TURNS / FAILED (L7-11).
- Upstream / downstream: none.
- Core claim: "The AIs may agree on a falsifiable experiment without agreeing that the underlying physical claim is true." (L45).
- Equations: none. Point / Path / Field role: none stated. Magnetism / gravity / rotation link: none stated.
- Open / parked / not-set items: none. Conflicts: none.

## validation — Reality-first simulation and validation contract   (`validation/REALITY_FIRST_CONTRACT.md`)
- Gate / lifecycle: "Mandatory design/validation policy" (L3). Evidence statuses UNMODELED / UNCALIBRATED / NUMERICALLY VERIFIED / REFERENCE MATCH / BENCH QUALIFIED / PHYSICALLY VERIFIED (L18).
- Upstream / downstream: governs REALITY_VALIDATION_ROADMAP.md, Virtual_Breadboard/SPICE_PARITY.md, 3D_CIRCUITRY_WORK_REGISTER.md, BENCH_REALITY_CONTRACT.md, Virtual_3D_Electronics/PARTS_AUDIT.md (L41). No Science node IDs.
- Core claim: "The physical world, not One-Wave, is the reference. The software must be able to refute One-Wave." (L7). "Missing magnetic hysteresis, 3D spatial field ... must produce UNMODELED, not a fabricated PASS." (L25).
- Equations: none.
- Point / Path / Field role: none stated.
- Magnetism / gravity / rotation link: the acceptance criteria include hysteresis loops and spatial magnetic-field examples (L32). The 2/4 ampere-turn idealized transfluxor card and the geometry-based 3D thresholds are different assumptions and must not be retuned to agree (L43).
- Open / parked / not-set items: One-Wave CELL_V1 models load only after the instrument is qualified (L37).
- Conflicts: none.

## validation — Reality-validation roadmap   (`validation/REALITY_VALIDATION_ROADMAP.md`)
- Gate / lifecycle: "PARTIAL, OPEN" (L3). Evidence status at L59-63: CELL_V1 measured magnetic memory, Maxwell gradient, moving CENTER and reinjection are **UNVERIFIED**.
- Upstream: Virtual_Breadboard BENCH_REALITY_CONTRACT, SOLVER_CONVERGENCE, SPICE_PARITY, 3D_CIRCUITRY_WORK_REGISTER; Virtual_3D_Electronics README and PARTS_AUDIT; RULES.md; `cell-v1/CELL.md` (L4). No Science node IDs.
- Core claim: "the breadboard's ideal figure-eight 2/4 ampere-turn threshold card is not the 3D geometry-dependent threshold; tests must NOT force them to agree" (L10). "no digital control chips, op-amp/comparator brain, or clock in CELL_V1" (L35).
- Equations: energy ledger "source + initial storage = dissipation + final storage + useful output + bounded numerical error" (L55).
- Point / Path / Field role: none stated in canonical terms. Hardware reading: Gate C (L37-42) separates ordinary toroids, round two-aperture sensory nuclei, square two-aperture motor nuclei, the common two-round-toroid body interface, and six wedges. It requires "actual 3D Bx/By/Bz and H-field solving" (L39) and states "A mutual-inductance number is not a field map." (L39). Field = spatial B/H field. "Distinguish CENTER reference drift, V_BUS return energy, and separate body-state magnetic retention" (L42).
- Magnetism / gravity / rotation link: "Test Maxwell-style winding gradient versus uniform field with field probes; never infer field balance merely from reversed winding labels." (L41). Magnetic acceptance test: "identical probe after different writes produces reproducibly distinct response" (L53). No gravity, no point rotation.
- Open / parked / not-set items: KiCad/ngspice/FEM parity is OPEN (L62). Current-main performance is NOT YET VERIFIED (L61). The next smallest action is at L65.
- Conflicts: none.

## validation — Builds ↔ One-Wave Science connection map   (`validation/SCIENCE_CONNECTIONS.md`)
- Gate / lifecycle: "ACTIVE navigation reference, not a physics validation result ... single Builds-side index" (L3).
- Upstream: Science GENERAL_REFERENCE_RULES.md, AI_CANONICAL_START_HERE.md, RESEARCH_EVIDENCE_CONNECTION_GRAPH.md, V1_VERIFICATION_MATRIX.md (L9-12). **Nodes cited:** C-311 Electric–Magnetic Duality (L18); D-401 Flux (L19); C-319 Magnetic Lattice Reorganization (L20); C-320 Magnetic Compression Path Coupling (L21); G-749 Point Rotation and Angular Momentum Receipt (L22); G-769 Path Rotation (L23); Chapter 09 `09_Transfluxor_Magnetic_Reorganization_and_Point_Rotation.md` (L24, L42); C-325 Transfluxor Magnetic Solver Triangulation (L24); G-766 Discrete Lattice Dispersion and Octave Emergence Proof (L25); E-511 Chord Rotation (L26); chapter `09_HARMONIC_RABBIT_ALGORITHM_BRIDGE.md` (L26, L28); RABBIT_HOPPING_TRANSLATOR_HYPOTHESIS_QUESTIONS.md and DREAMSCAPE_TRANSLATOR_OPEN_WORK.md (L27).
- Core claim: routing contract `Science hypothesis and equations → Builds fixture and numerical solver → independent reference solver → measured physical experiment → immutable receipt → Science verification matrix / owning node` (L33). "No assumed physics from musical indexing, arithmetic wrappers or pretty 3D field lines." (L35).
- Equations: none.
- Point / Path / Field role: G-749 is labelled "Point-frame rotation / angular momentum" (L22), which matches the canonical point rotation carrying L. G-769 is labelled "Geometric path turning" (L23), which matches the canonical path rotation. The file keeps them in separate rows. Field: C-311, D-401, C-319 and C-320 are magnetic field, flux and lattice-path topics. E-511 is "Chord Rotation ... (not a magnetic law)" (L26). Rabbit Hopping is "not spatial (x,y,z) or magnetic field law" (L27).
- Magnetism / gravity / rotation link: G-749 and G-769 are both routed to the "Magnetic and torque comparison" doc (TRANSFLUXOR_MULTISCALE_TRIANGULATION.md) (L22-23). C-311 duality is "unverified as fundamental emergence" (L18). No gravity.
- Open / parked / not-set items: "do not yet constitute automated receipt synchronization, a finished 3D FEM engine, or physical validation" (L44). The canonical semantics of Algorithm Zero / FIELD/VOID / M4 "must be checked" (L28).
- Conflicts: none with the canonical rules. Gap: the Builds target named for G-749 and G-769 (`TRANSFLUXOR_MULTISCALE_TRIANGULATION.md`) never mentions L = I omega, G-749, G-769, inertia axes, or open/closed dL/dt. So there is no Builds fixture yet that tests point rotation or path rotation.

## validation — Transfluxor multiscale triangulation   (`validation/TRANSFLUXOR_MULTISCALE_TRIANGULATION.md`)
- Gate / lifecycle: "RESEARCH DESIGN — NOT PHYSICALLY VALIDATED" (L2). Governed by REALITY_FIRST_CONTRACT (L3).
- Upstream: external references 1-6, Rajchman & Lo 1956 through mumax+ 2025 (L6-11); Virtual_Breadboard/MAGNETIC_SOLVER.md, Virtual_3D_Electronics/README.md, test/solver-triangulation.test.js (L56). No Science node IDs in this file; SCIENCE_CONNECTIONS points G-749, G-769, C-319 and G-766 here.
- Core claim: five distinct physical scales plus a hypothesis layer (L13-19). "One-Wave's 'lattice reorganization' and 'point rotation' require explicit observables and an independent constitutive law before being treated as additional physics. Ordinary material lattice, magnetic-domain pattern, flux-network topology and hypothesized underlying One-Wave lattice are FOUR different concepts." (L19).
- Equations: `V=RI+N dPhi/dt` (L14); `div B=0, curl H=J_free, B=mu0(H+M)`, `curl A=B` (L16); `m=M/Ms`, LLG torque/precession and damping (L17); energy audit `E_source+E_initial = E_final+E_dissipated+E_mechanical+E_radiated` (L37); `L=AL*N^2` given as the inadequate single constant (L15).
- Point / Path / Field role: Field = spatial B/H, curl H = J_free, vector potential A (L16). Path = closed Ampère paths, flux continuity, shared legs, block/set/read flux paths (L6, L15, L32). Point: the domain scale (LLG precession of m, L17) and the mechanical scale (rotor torque, L18) are both kept apart from the One-Wave "point rotation" hypothesis (L19). "do not equate magnetic-moment precession to macroscopic rotor motion" (L18). "do not infer rotation solely from magnetic-field circulation" (L46).
- Magnetism / gravity / rotation link: magnetic force/torque comes from field energy or the Maxwell stress tensor (L18). Rotation must be measured as torque, angle and work (L46). Damping exists only inside LLG (L17); there is no dL/dt rule. No gravity.
- Open / parked / not-set items: benchmark 7 asks for at least one One-Wave prediction "DIFFERENT from calibrated Maxwell + material micromagnetics. If predictions coincide, mark observationally indistinguishable, not verified." (L47). All deliverables are open (L49-53).
- Conflicts: none. The file is consistent with canon that field curl is not point rotation (L18, L46), and it keeps "point rotation" behind an independent constitutive law (L19).

---

## Slice summary

### (a) Nodes and chapters in this slice that bear on Point, Path, Field, rotation, magnetism, gravity, inertia, mass, resistance or lattice organization
All Science node IDs in this slice come from `validation/SCIENCE_CONNECTIONS.md` and `jetson/JETSON_DEEPSEEK_BRAIN_BUDDY.md`. Builds files are not nodes.
- **G-749** (SCIENCE_CONNECTIONS:22): "Point-frame rotation / angular momentum". Point rate with L. Its Builds target is the transfluxor triangulation, which has no L test.
- **G-769** (SCIENCE_CONNECTIONS:23): "Geometric path turning". Path rate. Same Builds target and the same gap.
- **C-311** (L18): electric–magnetic duality, "unverified as fundamental emergence". Field side; routed to SPICE parity and the 3D solver.
- **D-401** (L19): flux, Faraday coupling, winding polarity. Field/flux; routed to the magnetic solver.
- **C-319** (L20): magnetic lattice/path reorganization hypothesis. Lattice organization and magnetic path; routed to the transfluxor doc, which keeps "lattice reorganization" behind an independent constitutive law (TRANSFLUXOR:19).
- **C-320** (L21): compression / restoring-field coupling. Field compression; routed to the reality-first contract.
- **Chapter 09** `09_Transfluxor_Magnetic_Reorganization_and_Point_Rotation.md` (L24, L42): magnetism together with point rotation.
- **C-325** (L24): transfluxor solver triangulation (FEM, LLG, blind holdout).
- **G-766** (L25): lattice dispersion / octave emergence, a lattice hypothesis.
- **E-511** (L26): chord rotation, explicitly "not a magnetic law".
- **Chapter 09_HARMONIC_RABBIT_ALGORITHM_BRIDGE** (L26, L28): harmonic and addressing bridge; not a physics law.
- **W-010** (digital-cell/README:3): software L0 cell; FIELD − VOID signed difference. No physics.
- **I-06** (JETSON_DEEPSEEK:18): node metadata and alias resolution. Governance only.
- Builds docs that bear on hardware magnetism and lattice: VIEWS_ACTIONS, VIEW_ACTION_STACK, CELL_V1_CONCEPT_MAP, REALITY_VALIDATION_ROADMAP, TRANSFLUXOR_MULTISCALE_TRIANGULATION, REALITY_FIRST_CONTRACT. None of them mentions gravity, mass, inertia, resistance as mass/organization, or Moon/Mercury locking.

### (b) Conflicts found
No file contradicts the canonical rules. Gravity, expansion, redshift, L bookkeeping, parent/child transport and kappa_R are never stated in this slice. Internal and terminology issues:
1. `cell-v1/VIEW_ACTION_STACK.md:19,36,45`: BC–DC is called "the point/state layer" and QC–RC "rotating/field". The rotation is of a field-vector angle theta = atan2(Y,X), not point spin with L. The canon keeps point, path and field-curl separate; reading this layer as point rotation would conflate them. The file makes no L claim.
2. `cell-v1/VIEWS_ACTIONS.md:3` calls the hardware magnetic medium "the lattice" with no qualifier. Within the slice, `validation/TRANSFLUXOR_MULTISCALE_TRIANGULATION.md:19` requires four distinct lattice concepts.
3. "RC" means three different things: rotating-current (`VIEW_ACTION_STACK.md:9`), "last hold" (`gcac/THEORY.md:4`) and resistor-capacitor (`hardware/wave_reader_v1.md:15`).
4. "M4" means two things: a hardware routing nucleus (`maps/CELL_V1_CONCEPT_MAP.md:13`) and the OpenClaw orchestrator (`jetson/JETSON_OPENCLAW_RUNTIME.md:27`). `validation/SCIENCE_CONNECTIONS.md:28` flags this as unchecked.
5. `cell-v1/WEIGHT_LEAN.md:13-15,19`: "Gaps stay dead", but the ±1 bands share their edges with HOLD at 0.45 V and 0.55 V.
6. Gap rather than conflict: `validation/SCIENCE_CONNECTIONS.md:22-23` routes G-749 and G-769 to `TRANSFLUXOR_MULTISCALE_TRIANGULATION.md`, which contains no L = I omega, inertia-axis, path-ride or open/closed dL/dt test.

### (c) Cross-references outside this slice that matter for point rotation or magnetism
- Science: G-749, G-769, C-311, D-401, C-319, C-320, C-325, G-766, Chapter 09 (Transfluxor ... Point Rotation), RESEARCH_EVIDENCE_CONNECTION_GRAPH.md, V1_VERIFICATION_MATRIX.md (all from SCIENCE_CONNECTIONS).
- Builds, not in this slice: `cell-v1/CELL_V1_2026-09-28_CORRECTION.md` (the CELL map authority), `cell-v1/CELL.md`, `PROVEN_PARTS_REFERENCES.md` (R1-R8: resolver, synchro, rotating-field, ferrite hysteresis, domain-wall paths, inductive return), `Virtual_Breadboard/MAGNETIC_SOLVER.md`, `Virtual_Breadboard/SPICE_PARITY.md`, `Virtual_Breadboard/BENCH_REALITY_CONTRACT.md`, `Virtual_Breadboard/test/solver-triangulation.test.js`, `Virtual_3D_Electronics/README.md`, `Virtual_3D_Electronics/PARTS_AUDIT.md`, `Virtual_Breadboard/3D_CIRCUITRY_WORK_REGISTER.md`.

### (d) How the build hardware implements Point / Path / Field and magnetic open / closed (as stated in the docs; nothing added)
- **Point:** the local reference point is CENTER/(0), an active balanced virtual-ground reference (VIEW_ACTION_STACK:145), held in a two-aperture figure-eight hysteretic nucleus (square for the motor cell, round for sensor cells; CELL_V1_CONCEPT_MAP:11-12). BC–DC is called "the point/state layer" (VIEW_ACTION_STACK:19), but it is a signed polarity state. **No hardware doc implements point spin, L = I omega, inertia axes, or resistance as mass/organization.** Physical rotation is only to be claimed from measured rotor torque, angle and work (TRANSFLUXOR:18, 46).
- **Path:** TC–AC out-and-back traversal around CENTER (VIEW_ACTION_STACK:23). Etched hysteretic lattice paths as "distributed muscle memory" (VIEW_ACTION_STACK:132-133, 143). "process/path history is the memory mechanism being tested" (VIEW_ACTION_STACK:146). Closed Ampère flux paths and shared legs (TRANSFLUXOR:15). M4 TIP⇄TIP / BASE⇄BASE routing (CELL_V1_CONCEPT_MAP:13). PULL/PUSH as inward/outward routing (VIEWS_ACTIONS:28-29). This is a path of flux and memory, not the canonical G-769 ride with no L.
- **Field:** QC–RC two orthogonal winding components form a rotating magnetic vector, `B_view = X x̂ + Y ŷ`, `theta = atan2(Y,X)` (VIEW_ACTION_STACK:38-45). The shared continuous magnetic medium (VIEWS_ACTIONS:3, 72). Spatial Bx/By/Bz and H with div B = 0, curl H = J_free (REALITY_VALIDATION_ROADMAP:39; TRANSFLUXOR:16). A Maxwell-style winding gradient versus a uniform field is to be tested with probes (ROADMAP:41).
- **Magnetic open / closed:** **no doc in this slice states the canonical open (dL/dt = 0) / closed (dL/dt = −gamma L) rule or uses the words open/closed for magnetism.** The nearest hardware operations the docs name, given without mapping them to canon, are:
  - Rajchman–Lo transfluxor block / set / read of aperture flux paths (TRANSFLUXOR:6, 42);
  - FLIP (domain inversion), PUSH (past H_c), PASS (no write, coast) (VIEWS_ACTIONS:29-31);
  - one FLIP per three-mirror-gate loop (VIEW_ACTION_STACK:194);
  - LLG damping at the domain scale (TRANSFLUXOR:17).
  All of these are UNVERIFIED (ROADMAP:63).
- **Gravity:** none stated anywhere in the slice.
