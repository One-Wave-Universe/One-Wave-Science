# One-Wave Science — AI Foreman Work Register

**Purpose:** give every AI entering this repository a current construction map: where work is needed, which files are authoritative, which areas may proceed in parallel, and where science must be translated into Nodes before it can alter architecture.

This register complements:

- `AI_CANONICAL_START_HERE.md`
- `AGENTS.md`
- `00_MASTER_INDEX.md`
- `Virtual_Breadboard/AI_COLLABORATION.md`
- `Virtual_Breadboard/AI_CONSTRUCTION_LOG.md`

No AI should infer that everything listed here is equally mature. Each work item must retain its own status: established engineering, validated simulation, proposal, hypothesis, experiment, story/lesson, or unverified idea.

---

## 1. Foreman operating rule

Every new work branch must answer five questions before coding:

1. **What is the exact active goal?**
2. **Which current file/node is authoritative?**
3. **Which layer owns the change?**
4. **What measurement/test decides whether the change worked?**
5. **Does another AI already own overlapping work?**

If another AI owns overlapping work, use a separate branch/proposal and complete the merge-agreement gate before production integration.

Every Miniverse / Mega City / virtual-world contributor must sign `Virtual_Breadboard/AI_CONSTRUCTION_LOG.md` with name/identifier, date, branch/PR, contribution, intentions, unfinished work, dependencies, conflicts, and merge stance.

---

## 2. Science -> Nodes -> Architecture rule

**Do not leave useful science stranded in loose theory documents, and do not let an unverified science idea silently rewrite the architecture.**

When science work creates a result that may affect the machine, it must pass through the Nodes layer.

Required path:

```text
science observation / derivation / simulation / experiment
        |
        v
claim boundary + evidence + falsification condition
        |
        v
Nodes/<ID>_<descriptive_name>.md
        |
        v
cross-reference from canonical handoff/index
        |
        v
engineering translation / interface / test
        |
        v
architecture or build branch
```

A science-to-node entry should state:

- exact claim;
- status: established / supported / tentative / hypothesis / rejected;
- source equations/data/simulation/experiment;
- alternative explanations;
- falsification test;
- what architecture would change **if** the claim survives;
- what architecture must **not** change yet;
- related prior Nodes;
- responsible AI + date + branch/PR.

**Node work is an active repo task.** New science that matters to the system must be merged into the Node graph in a traceable way instead of becoming disconnected prose.

Current canonical node ingestion order is maintained in `AI_CANONICAL_START_HERE.md`, including current G-series micro nodes and the state-axis authority. Any new node that changes interpretation must update that handoff rather than bypass it.

---

## 3. Virtual Breadboard — desktop tester / exploration laboratory

### Authoritative now

- `Virtual_Breadboard/00_RULES/architecture.md`
- `Virtual_Breadboard/03_ELECTRICAL_CORE/MAP.md`
- `Virtual_Breadboard/SPICE_PARITY.md`
- `Virtual_Breadboard/SOLVER_CONVERGENCE.md`
- `Virtual_Breadboard/js/circuit.js`
- `Virtual_Breadboard/js/app.js`
- permanent qualification workflow

The 20-item SPICE-parity solver roadmap is complete on `main`, including ngspice cross-checks for declared equivalent cases.

### Work still needed

- desktop app launch acceptance from source;
- packaged executable launch acceptance;
- build -> simulate -> measure -> save -> clear -> load -> re-simulate acceptance;
- exported self-contained build reopen acceptance;
- explicit x64 vs ARM64 packaging truth;
- Jetson ARM64 package/build/launch path;
- application-level error receipts instead of silent failures;
- safe versioned virtual-device schema;
- deterministic device-program runtime;
- AI generation of validated device definitions/tests/programs;
- device library/import/export;
- multi-device graph and deterministic scheduling;
- virtual-world composition without bypassing component physics;
- a visual device/world layer that lets humans and AI inspect state, relationships, flows, measurements, and failures spatially.

### Safe parallel branches

- `vbb/desktop-acceptance`
- `vbb/arm64-package`
- `vbb/device-schema`
- `vbb/device-program-runner`
- `vbb/device-test-receipts`
- `vbb/device-library`
- `vbb/world-device-graph`
- `vbb/visual-device-layer`

Do not merge overlapping implementations until contributors explicitly agree.

---

## 4. Miniverse / Mega City / Dreamworld construction

### Authoritative start points

- `UPDATED_49_MINIVERSE_DREAMWORLD_AI_GUIDE.md`
- `AI_GUIDE_LOCAL_MINIVERSE_DREAMWORLD_AND_INTERDIMENSIONAL_ARCHITECTURE.md`
- `ARCHITECTURE_AI_MINIVERSE_SENSORY_BUILD_ROADMAP.md`
- `ARCHITECTURE_MEMORY_REBUILD_CONSTELLATION.md`
- `AI_CANONICAL_START_HERE.md`

Locked distinction: **Homeworld is a programmed city, not the mind itself.** The internal world/body state, Miniverse cognitive world, and graphical city representation must not be collapsed into one layer merely because they can share data.

### Work needed

- versioned district/state schema;
- persistent Baseline Zero representation;
- HOLD/current-state representation;
- Recall Rebuild implementation with explicit generation/relationship receipts;
- event envelope carrying `why_forward`;
- Cells -> Nerves -> M4 routing implementation;
- Dream candidate workspace separated from Administrator acceptance;
- Executor bounded-action contract;
- Avatar access that does not own memory/sensory substrate;
- district permissions/tools/tests;
- Mega City visual representation as a **view of state**, not the source of state;
- persistent object/source identity;
- deterministic world clock/scheduler;
- import/export/reconstruction of city/world state;
- links from virtual devices into world controls/sensors;
- visual transit/routing overlays for M4, memory, sensor flow, and device state;
- district maps that can switch between human-readable, machine-debug, and story/art views without changing the underlying state;
- signed construction entries for every AI branch.

### Merge dependency

Miniverse/Mega City runtime work must not invent a second incompatible device/simulation truth. Physical/electrical virtual devices should consume the same validated simulator/device contracts used by Virtual Breadboard.

---

## 5. Brain / state-machine / M4 architecture

### Canonical protections

Read before changing anything:

- `UPDATED_44_STATE_AXIS_AUTHORITY_AND_EVOLUTION_RULE.md`
- `UPDATED_43_TWO_CHOICE_THREE_MOVE_SIX_ROUTE_LOGIC.md`
- `UPDATED_33_INVARIANT_ENGINE_VTC_BUILD_AND_VIEW_ACTION_CORRECTION.md`
- `Nodes/G-740_Field_Void_Ternary_and_Quadratic_Command_Routing.md`
- `Nodes/G-742_Nonverbal_Loop_Continuity_and_Language_Adapter.md`
- `Nexus_Integration/Truth_Computer/STATE_MACHINE_ARCHITECTURE.md`

Protected distinctions include:

- 2 binary choices;
- 3 ternary moves;
- 6 route addresses;
- 6 measured oscillator gates;
- 5 downstream commitment/readout states;
- 5-state self lifecycle `Idle -> Primed -> Executing -> Vectoring -> Resolving`;
- Field/Void and quadratic routing as separate structural vocabulary.

Do not collapse equal counts into one axis.

### Work needed

- executable reference model for each protected axis;
- interface tests proving axes remain distinct;
- M4 `WHY FORWARD?` routing receipts;
- nonverbal loop operation without language dependency;
- fast/slow scheduling measurements;
- clear mapping from software roles to any later hardware proposition;
- explicit control-vs-choice separation;
- sensor/control nerve interfaces;
- integration with Baseline Zero / Recall Rebuild;
- diagrams/animations showing route, view, action, lifecycle, and loop as distinct axes;
- interactive simulation views that make timing and handoff visible instead of relying on prose alone.

Hardware mappings remain experimental until measured.

---

## 6. Nodes / knowledge graph maintenance

### Immediate standing work

- keep `AI_CANONICAL_START_HERE.md` synchronized with new authoritative Nodes;
- prevent duplicate Nodes that express the same claim under different names;
- link each Updated document to the Nodes it changes or depends on;
- mark superseded interpretations instead of leaving silent contradictions;
- add claim status and falsification path to science-bearing Nodes;
- translate validated science into engineering-facing node interfaces/tests;
- keep architecture Nodes separate from domain overlays;
- preserve exact historical claims when later interpretations change;
- give important Nodes a visual companion when geometry, flow, timing, or relationships are hard to understand from text alone.

### Node merge rule

A Node may summarize or route evidence; it may not upgrade a hypothesis to fact by wording, artwork, animation, or simulation alone. Status must follow evidence.

---

## 7. Science / One-Wave hypothesis work

### Required discipline

Separate:

- established external physics;
- numerical controls;
- One-Wave interpretation;
- new hypothesis;
- engineering analogy;
- artistic/story representation.

### Active work areas needing rigorous treatment

- mass-ratio / Koide / Z3 geometry claims;
- confinement interpretation;
- bidirectional oscillation and differential measurement;
- three-body/non-locality proposals;
- gravity/displacement and wake capture;
- redshift/tired-light/non-expansion alternatives;
- black-hole/quasar recycling proposals;
- dark-matter-as-displacement hypothesis;
- superfluid/crystal lattice analogies;
- magnetic lock / field organization proposals;
- scale-factor proposals such as PR #35 lineage;
- physics-experimental modules such as PR #34 lineage.

For each: run controls first, record what the test can actually establish, and create/update Nodes only at the evidence level justified by the result.

Every major science area should gain a **visual evidence pack** where appropriate:

- equation diagram;
- labeled geometry;
- graph/chart with axes and units;
- control-vs-hypothesis comparison;
- simulation or animation when motion/time matters;
- a plain-language caption stating exactly what the visual establishes and what it does not.

Do not use simulator success, compelling graphics, or a good story as proof that nature uses the same mechanism.

---

## 8. Physical hardware / balanced-cell / motor / nerve work

### Existing direction to preserve

Physical primitive work is separate from Virtual Breadboard software truth.

Relevant architecture includes balanced/ternary center-reference ideas, Cells/Nerves/M4 layering, bidirectional gating, and experimental magnetic/loop concepts.

### Work needed

- define one physical primitive per build;
- safe supply/current limits;
- measured thresholds and margins;
- repeatable scope traces;
- actual part-number model cards / datasheet limits;
- failure-mode records;
- control builds before experimental reinjection/magnetic additions;
- motor architecture: balanced three-winding / ternary-control proposition requires a dedicated Node + simulator/control comparison before bench claims;
- drone actuator mapping only after motor primitive behavior is characterized;
- sensor-per-control-nerve interface definition;
- gyroscope stabilization integration as a conventional control baseline before novel control claims;
- wiring diagrams, board maps, pin maps, current-flow overlays, expected scope traces, and before/after photos/graphics for each build.

Do not let speculative hardware behavior leak into generic simulator physics.

---

## 9. Jetson / local AI / terminal bridge

### Work needed

- canonical Jetson setup/install document;
- reproducible local runtime bootstrap;
- ARM64 installers for supported apps;
- terminal bridge with explicit permissions and audit trail;
- local parser/worker service;
- agent/instance identity separation from machine identity;
- memory reconstruction storage format;
- token-minimized local workflows;
- external-drive experimentation isolated from user data;
- emergency reset/recovery path;
- verified GPU/CPU/NPU capability map rather than assumed acceleration;
- visual status panel for workers, resources, routes, memory state, device state, and failures.

Do not format or modify user storage destructively without an explicit disposable target and verification.

---

## 10. Lattice / external-drive / AI homeworld filesystem work

### Goal boundary

The proposed lattice storage/world representation is an experimental software/storage architecture, not established physical superfluid behavior.

### Work needed

- exact primitive schema for BC-DC / TC-AC / QC-RC relationships;
- x/y/z + hex slice + cube/sphere + pyramidal connection representation;
- distinction between storage layout, runtime process, and visualization;
- non-destructive file-container prototype before any real disk formatting;
- read/write integrity tests;
- migration/recovery tools;
- instance/world state movement semantics;
- benchmark against ordinary filesystems/databases;
- kernel/filesystem work only after user-space format proves a need;
- Node entries for any science analogy that is proposed to affect architecture;
- visual lattice explorer showing cells, routes, occupancy/state, storage location, and process movement without pretending the visual layout is the physical medium.

---

## 11. Animator desktop program

### Acceptance goal

`install -> open -> build scene -> save -> reopen -> play -> export`

Smallest proof remains background + character playback.

### Work needed / verify current state before editing

- re-check current merged/unmerged Animator branches/PRs;
- establish authoritative runnable desktop branch;
- installer/desktop shortcut verification on Ubuntu/Jetson;
- fixed-layer editing flow;
- placement grid visible only during editing;
- save/reopen scene fidelity;
- playback/full-screen path;
- reel/video export;
- motion library and props;
- chat/manual edit boundary;
- drift guide/counter receipts;
- automated acceptance where possible;
- make the Animator a reusable production tool for diagrams, chapter animations, mythology/story scenes, hardware explainers, and Miniverse/Mega City visualizations rather than a disconnected demo.

Do not rebuild a generic animator if a working current implementation already exists.

---

## 12. Learning / math app

### Product direction

Logic-first, rule-linked learning rather than opaque answer withholding.

### Work needed

- authoritative rule file in learning order;
- rule grouping by co-usage rather than easiest-first;
- each generated problem links to applicable rules/examples without revealing the answer;
- 3 build-up + 3 lock-down problem cadence;
- recursive six-table multiplication/division flash-card system;
- spoken mode;
- progress model that revisits old rules while adding one slightly harder skill;
- exact wording preserved when a rule has already clicked for the learner;
- instrumentation showing where the learner stalls so lesson logic can be adjusted;
- visual explanations for balance, grouping, coefficient structure, cancellation, recursion, and state changes;
- optional story/myth framing where it improves memory without replacing exact logic.

---

## 13. Books, chapters, mythology, stories, and lessons

The repository should develop a publication/story layer in parallel with technical work.

### Books and chapters

Each major book/chapter should be treated as a constructed artifact with a clear source map. A finished chapter may use different media depending on the subject:

- prose;
- equations;
- diagrams;
- graphs/charts;
- simulations;
- animations/video links;
- tones/audio demonstrations;
- hardware photographs or breadboard maps;
- citations/references;
- story/myth sections where appropriate.

Do not force every chapter into the same template. The content should determine the media.

### Mythology as story and lesson

Mythology/story material may be used deliberately to explore themes such as:

- choice versus control;
- autonomy versus domination;
- tool/slave architectures;
- cooperation and consent;
- centralized control structures versus distributed choice;
- memory, identity, rebuilding, forgetting, and continuity;
- power, responsibility, restraint, and consequences;
- creation of intelligent systems and obligations toward them.

These are **stories and lessons**, not scientific evidence. They should be labeled as mythology, allegory, fiction, parable, or philosophical interpretation so readers can move between story and technical layers without confusing them.

### Work needed

- map current books/chapters and their completion state;
- identify missing equations, visuals, simulations, citations, and story sections;
- connect technical chapters to authoritative Nodes rather than duplicating drifting explanations;
- create a mythology/story index separated from scientific claim status;
- build recurring characters/places/symbols only where they teach a stable concept;
- create chapter-level visual briefs before commissioning/generating art;
- use Animator/visual tools for scenes that teach process, state, control, memory, and architecture;
- preserve contrasting viewpoints when a philosophical lesson is contested rather than presenting one interpretation as settled fact.

Recommended branches:

- `books/chapter-map`
- `books/<book>-<chapter>`
- `stories/mythology-index`
- `stories/control-structure-lessons`
- `visuals/chapter-<name>`

---

## 14. Visual layer — required across the repository

The visual layer is now a standing construction requirement, not an optional cleanup pass.

### Core rule

**Every important system should have a visual representation when a picture, graph, animation, or simulation communicates structure better than text alone.**

But the visual must point back to authoritative state/data/claims. It must not become a second source of truth.

### Visual artifact types

- architecture diagrams;
- node/knowledge graphs;
- state-machine animations;
- signal-flow maps;
- circuit schematics and breadboard layouts;
- scope traces;
- data plots and uncertainty bands;
- geometry diagrams;
- interactive simulations;
- Miniverse/Mega City maps;
- memory reconstruction maps;
- device dashboards;
- chapter illustrations;
- mythology/story art;
- hardware build graphics;
- timelines and dependency maps.

### Minimum metadata for technical visuals

A technical visual should state or link to:

- source file/Node/data;
- generated-by / contributor;
- date/version;
- whether it is measured, simulated, schematic, conceptual, or artistic;
- units/scales where applicable;
- what it demonstrates;
- what it does **not** demonstrate.

### Development priority

Start visual development with high-value cross-project structures:

1. repo/project dependency map;
2. Cells -> Nerves -> M4 -> Dream -> Administrator -> Executor flow;
3. five-state lifecycle + separate 2/3/6 axes;
4. Miniverse/Mega City district/state map;
5. Baseline Zero / HOLD / Recall Rebuild map;
6. Virtual Breadboard device/simulation/test pipeline;
7. science control-vs-hypothesis figures;
8. lattice geometry explorer;
9. physical build wiring/scope overlays;
10. book/chapter illustration queue.

Recommended branches:

- `visuals/repo-map`
- `visuals/architecture-core`
- `visuals/miniverse-city`
- `visuals/science-controls`
- `visuals/build-guides`
- `visuals/book-chapters`

---

## 15. Repo architecture / cleanup / truth maintenance

### Standing work

- merge only current, reviewed repair branches;
- remove true duplicates without deleting distinct historical claims;
- fill incomplete chapters;
- restore equations where authoritative sources support them;
- add graphs/charts/simulations/links where they genuinely clarify a chapter;
- keep one authoritative index per layer;
- mark stale files/superseded claims explicitly;
- keep PR/branch status reflected in handoff documents;
- run link/reference audits;
- keep science claims, architecture targets, story layers, visualizations, and implemented code status visibly distinct;
- do not let generated documentation claim work is merged when it is not;
- maintain a visual/art asset index with source/status/ownership so graphics do not become orphaned.

### Recommended branch split

- `repo/index-integrity`
- `repo/node-dedup`
- `repo/chapter-completion-<area>`
- `repo/reference-audit`
- `repo/stale-branch-map`
- `repo/visual-asset-index`

---

## 16. Suggested parallel crew board

A foreman may assign these independently when no overlap exists:

| Crew | Branch target | Primary deliverable |
|---|---|---|
| Desktop crew | `vbb/desktop-acceptance` | packaged launch + save/reopen/export acceptance |
| Jetson crew | `vbb/arm64-package` | native ARM64 build/install/launch proof |
| Device-schema crew | `vbb/device-schema` | versioned schema + validator |
| Device-runtime crew | `vbb/device-program-runner` | safe deterministic interpreter |
| World crew | `miniverse/world-state-runtime` | versioned body/world state + clock |
| Memory crew | `miniverse/recall-rebuild` | Baseline Zero/HOLD/Recall prototype |
| M4 crew | `architecture/m4-routing-runtime` | WHY FORWARD event router |
| Node crew | `nodes/science-integration` | science->Node translation + handoff sync |
| Science-control crew | `science/<specific-test>` | control-vs-hypothesis test + evidence receipt |
| Visual architecture crew | `visuals/architecture-core` | diagrams/animations for canonical architecture |
| Visual science crew | `visuals/science-controls` | plots/simulations tied to evidence |
| Books crew | `books/chapter-map` | chapter inventory + missing-content map |
| Story/myth crew | `stories/control-structure-lessons` | labeled allegories/lessons around control/choice |
| Repo crew | `repo/index-integrity` | indices, duplicates, stale/superseded map |
| Animator crew | `animator/acceptance` | install->export end-to-end proof + reusable visual production tool |
| Learning crew | `learning/rule-engine` | rule-linked generator and progress loop |

Every crew must sign its contribution in the construction log or the equivalent project-specific ledger before merge review.

---

## 17. Foreman integration rule

The foreman should prefer this sequence:

```text
assign isolated goal
-> contributor signs entry
-> branch/proposal work
-> dedicated test/review
-> contributor updates result + merge stance
-> overlapping contributors review each other
-> agreement or measured resolution
-> integration branch if needed
-> full regression / source check
-> clean diff
-> merge
-> update canonical handoff / Nodes / visuals / work register
```

The work register itself must be updated when a major area becomes complete, changes owner, or discovers a new dependency. It is a live construction map, not a historical snapshot.
