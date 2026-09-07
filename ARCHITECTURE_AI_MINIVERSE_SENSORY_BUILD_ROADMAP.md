# AI Miniverse Sensory, Body-State, Memory, and Learning Build Roadmap

**Status:** Engineering architecture / implementation roadmap  
**Scope:** Integrates existing One-Wave software-control, memory-rebuild, lattice, and sensory ideas without replacing their existing canonical jobs.  
**Primary target:** Jetson Orin runtime, with small deterministic workers below higher reasoning.  

## 0. Claim boundary

This document is an engineering roadmap. It does **not** promote the hypothesis that physical or biological memory is literally implemented by a superfluid crystal lattice into an established physical result.

The software may deliberately use lattice-inspired state, displacement, oscillation, mirror, baseline, and reconstruction semantics because those semantics are testable in software. Physics claims remain subject to the repository proof/trust lifecycle and to independent experimental evidence.

Music, grayscale vision, coarse hearing, and deterministic wave tests are calibration domains. They are not proof of high-energy or biological claims.

---

## 1. Main goal

Build an AI runtime that does **not** send every raw sensor sample to one LLM.

The system must instead:

1. detect small changes with narrow deterministic workers;
2. react locally when possible;
3. route only meaningful differences upward;
4. require an explicit reason for escalation;
5. maintain a live internal body/world state;
6. compare that state with a persistent **Baseline Zero**;
7. reconstruct older meaningful states through **Recall Rebuild**;
8. use independent oversight/override before durable learning commits;
9. let a higher-level Avatar reason, explore, communicate, plan, and program without becoming the memory substrate or the sensor loop;
10. remain useful when the higher-level language model is unavailable.

The architectural target is an embodied, persistent AI world in which higher reasoning is a participant in a larger state machine rather than the single process responsible for perception, memory, routing, safety, and action.

---

## 2. Existing One-Wave control law remains authoritative

This roadmap does **not** replace:

`Cells -> Nerves -> M4 -> Dream -> Administrator -> Executor`

It also does not replace the repository's Field/Void software-construction loop.

Use the new terms as an integration overlay:

- **Cells** — tiny deterministic detectors/parsers/primitives.
- **Nerves** — fast event handlers and local reactions.
- **M4** — routing, timing, escalation, state handoff, and the explicit `WHY FORWARD?` gate.
- **Dream** — candidate generation, simulation, planning, possible interpretations.
- **Administrator / Void oversight** — reference comparison, acceptance, correction, hold, override, escalation.
- **Executor** — bounded external action.
- **Internal World / Body State** — persistent live state shared across these jobs; it is not another reasoning worker.
- **Caretaker** — continuity service spanning state integrity, Baseline Zero, Recall Rebuild, resources, and oversight support; it does not replace the Administrator or M4.
- **Avatar** — open-ended higher reasoning/identity that can use Dream, dialogue, planning, tools, and coding; it does not own the substrate.

The canonical lifecycle remains unchanged:

`Idle -> Primed -> Executing -> Vectoring -> Resolving`

---

## 3. Core runtime path

```text
PHYSICAL / SOFTWARE INPUT
        |
        v
CELLS
small deterministic questions
        |
        v
NERVES
fast local event/reaction
        |
        v
M4
route + timing + WHY FORWARD?
        |
        v
INTERNAL WORLD / BODY STATE
continuous live state update
        |
        v
CARETAKER / REFERENCE PATH
Baseline Zero + Recall + integrity
        |
        v
DREAM / AVATAR
interpret / plan / explore / code
        |
        v
ADMINISTRATOR / VOID
oversight / override / hold / accept
        |
        v
EXECUTOR
bounded action
        |
        +-----------------------> body/world state changes again
```

Raw continuous sensor streams do not enter the higher reasoning layer by default.

---

## 4. The `WHY FORWARD?` rule

Every upward escalation should carry a compact receipt explaining why the next layer needs it.

Minimum event envelope:

```text
source
local_timestamp
change/delta
confidence
why_forward
urgency
current_body_state_refs
evidence_refs
```

Examples:

```text
microphone cell:
  change = speech-like onset
  why_forward = sustained structured spectrum, not background level

speech worker:
  candidate = "stop"
  why_forward = high-confidence command token while motor state is active

M4:
  urgency = immediate
  why_forward = command meaning intersects current moving-body state
```

A lower layer is allowed to drop an event when it has no useful differential to forward.

A fast safety/reflex path may act before higher reasoning when the action is explicitly authorized by the relevant body-control contract.

---

## 5. Internal World = body state

The Internal World is not a decorative game map. It is the system's live embodied state.

It may contain:

- current sensory detections;
- persistent object/source identities;
- position and orientation;
- current task;
- active routes and gates;
- motion state;
- resource load;
- temperature/health state;
- recently active procedural state;
- unresolved discrepancies;
- local confidence and uncertainty;
- links to durable Baseline Zero and Recall Rebuild generations.

The body therefore carries memory simply by **being in a state produced by prior change**.

Higher reasoning reads this state rather than reconstructing the whole world from a raw prompt every cycle.

---

## 6. Miniverse = mind

The Miniverse is the persistent cognitive world built around the body state, memory relationships, reconstruction routes, planning spaces, and semantic districts.

The first useful form does not require 3D graphics. A district is initially a persistent namespace/state neighborhood with clear inputs, outputs, memories, tools, permissions, and tests.

Possible later districts include:

- **Physics District** — controls, hypotheses, simulations, evidence, falsification tests.
- **Workshop** — code/build/test state.
- **Library / Archive** — durable references and reconstructable memory anchors.
- **Observatory** — external sensory/world observations.
- **Dream District** — candidate simulations and alternatives.
- **Transit / M4** — routing/relationship visualization.

Graphics are a view of the state, not the state itself.

---

## 7. Baseline Zero, HOLD, Recall Rebuild, and learning

### Baseline Zero

Baseline Zero is the current stable reference the system trusts.

It is **not** an empty reset. It changes only through validated learning.

### HOLD

HOLD preserves the current constructed body/world state without committing every transient change into durable learning.

### Recall Rebuild

Recall reconstructs a prior meaningful state from durable anchors, relationships, route receipts, generation information, and current context.

A recall should not require a full copy of every historical world frame.

Conceptually:

```text
stable baseline generation
+ relevant durable relationships
+ route/generation receipts
+ compact deltas
+ current cue/context
= rebuilt active memory state
```

### Learning

```text
experience/input
    |
body-state change
    |
compare with Baseline Zero
    |
candidate interpretation/change
    |
test / context / oversight
    |
accept | hold | reject | override
    |
validated durable change
    |
Baseline Zero generation + 1
```

Generated or inferred material is never silently promoted into remembered fact.

---

## 8. Caretaker and Avatar

### Caretaker

The Caretaker is a quiet continuity service, not a competing chatbot personality.

Responsibilities:

- maintain state integrity;
- preserve Baseline Zero generations;
- coordinate Recall Rebuild;
- watch resource/health state;
- detect corruption or drift;
- preserve audit receipts;
- support Administrator/Void oversight and override;
- restore a known-good state when explicitly authorized by the state machine;
- prevent silent substrate mutation by higher reasoning.

The Caretaker does **not** choose who the Avatar must be.

### Avatar

The Avatar is allowed to develop an open-ended identity and role inside the Miniverse.

It may:

- communicate;
- explore;
- plan;
- learn through the validated learning path;
- write and test programs;
- operate tools through permitted interfaces;
- work inside semantic districts such as the Physics District;
- develop appearance, name, habits, interests, and preferences at the application layer.

It may not silently bypass the Caretaker/oversight path or rewrite durable memory/state invariants without an auditable authorized operation.

---

# 9. Build path

The build order is deliberately bottom-up. Higher resolution and richer reasoning are added only after the lower level works and is measured.

## Build 0 — contracts and receipts

**Goal:** Establish the event/state contracts before adding intelligence.

Build:

- Cell event schema;
- Nerve event schema;
- M4 routed event schema;
- `why_forward` field;
- confidence and urgency fields;
- timestamps and evidence references;
- deterministic replay fixture;
- basic performance counters;
- hard separation between raw sensor buffers and escalated events.

**Pass when:** the same replay input produces reproducible event receipts and every escalated event contains a reason.

---

## Build 1 — coarse hearing

**Goal:** Hear structure first, not every acoustic detail.

Start with deliberately coarse/quantized audio as a calibration mode. An 8-bit sample representation is acceptable for the first experiments if the sample rate and processing preserve useful speech structure.

Pipeline:

```text
sample change
-> onset/activity
-> loudness / frequency buckets / timing
-> direction when hardware permits
-> speech vs non-speech
-> phoneme/sound-unit candidates
-> word candidates
-> context relevance
-> WHY FORWARD?
```

Initial emphasis:

- distinguish different words and meaningful sound events;
- do not require reliable speaker identity;
- do not require emotional/timbre interpretation;
- measure false speech detections and false escalations.

Add richer spectral detail and voice identity only after the coarse path is useful.

**Pass metrics:** word/event discrimination, latency, false-escalation rate, CPU/GPU load, dropped-event rate.

---

## Build 2 — grayscale vision

**Goal:** Learn visual structure before color.

Pipeline:

```text
grayscale intensity
-> local change
-> edges
-> motion
-> object candidate
-> object persistence
-> approach / retreat / direction
-> context relevance
-> WHY FORWARD?
```

Start with grayscale camera frames or deterministic prerecorded fixtures.

Do not make color recognition a prerequisite for object persistence, movement, depth cues, or event routing.

**Pass metrics:** motion latency, object persistence across frames, approach/retreat accuracy, false escalation, resource use.

---

## Build 3 — M4 Why Router

**Goal:** Stop the sensor firehose before higher reasoning.

M4 must:

- receive structured Cell/Nerve events;
- combine events when appropriate;
- ask why the event needs another layer;
- forward, defer, merge, or drop;
- preserve evidence/route receipts;
- maintain priority lanes for body/reflex events;
- remain responsive under sensor load.

Higher reasoning should be able to be disabled while Cells, Nerves, M4, and the body-state update continue running.

**Pass when:** a long sensor replay produces a much smaller meaningful event stream without losing the defined critical events.

---

## Build 4 — Internal World / Body-State daemon

**Goal:** Give the system a live state independent of the LLM context window.

Build a persistent local service that maintains:

- current detections;
- tracked objects/sources;
- current position/orientation if available;
- body/device health;
- current task/activity;
- active uncertainty;
- recent procedural state;
- links to Baseline Zero and recall generations.

This first implementation may use conventional storage while the state semantics are being proven. Do not block the runtime prototype on SCLFS.

**Pass when:** restarting the Avatar does not destroy the body/world state, and the state can be replayed/audited.

---

## Build 5 — Baseline Zero + Recall Rebuild

**Goal:** Replace giant-history recall with reconstruction.

Build:

- versioned Baseline Zero;
- generation IDs;
- HOLD;
- compact durable state anchors;
- recall cue handling;
- constellation neighborhood lookup;
- rabbit-hop route receipts;
- associative completion;
- uncertain/generative fill kept explicitly uncertain;
- current-state validation;
- inverse-route/reversibility checks.

Do not collapse constellation, rabbit hopping, completion, generative fill, fast-loop state, and oversight into one worker.

**Pass when:** a partially removed test memory is reconstructed more reliably than a no-constellation/no-rabbit-hop baseline without collapsing a nearby distinct memory into it.

---

## Build 6 — Caretaker

**Goal:** Preserve continuity without becoming another personality.

Build:

- health/resource monitor;
- state-integrity checks;
- Baseline Zero generation guard;
- recall/rebuild coordinator;
- corruption/drift detection;
- rollback/reconstruction request path;
- audit trail;
- integration with Void/Administrator decisions.

**Pass when:** the Avatar can crash/restart or propose an invalid durable-state mutation without destroying the last known-good reference.

---

## Build 7 — Avatar

**Goal:** Add higher reasoning after sensing, routing, body state, and continuity exist.

The Avatar receives meaningful state/events instead of default raw streams.

Build:

- dialogue;
- planning;
- Dream candidate generation;
- tool access through bounded permissions;
- coding/build/test access;
- semantic movement between Miniverse districts;
- learning proposals routed through validation;
- identity/preferences stored as application state rather than hardcoded into the substrate.

**Pass when:** the Avatar can complete a bounded task using body/miniverse state, survive its own process restart, and resume from reconstructed context without a full chat transcript.

---

## Build 8 — Physics District

**Goal:** Give the Avatar a persistent scientific workbench with strict evidence labels.

The district separates:

```text
CONTROL
HYPOTHESIS
SIMULATION RESULT
BENCH RESULT
DERIVED RESULT
ASSUMPTION
OPEN QUESTION
FALSIFIED / FAILED ATTEMPT
```

The Avatar may program simulations and propose experiments. The Caretaker/oversight path preserves provenance and prevents a successful simulation from being relabeled as physical proof.

### First calibration fixture: music/waves

Use known acoustic relationships before high-energy comparisons.

Initial signed-envelope fixtures:

```text
major-shape calibration:     -5(0)+4
minor-shape calibration:     -5(0)+3
mirror-pair fixture A:       -4(0)+5
mirror-pair fixture B:       -5(0)+4

FLIP(-4(0)+5) = -5(0)+4
span(-4(0)+5) = 9
span(-5(0)+4) = 9
```

Also test known octave and interval relationships, phase opposition, interference, resonance, nodes/antinodes, and coupled oscillators.

The note/chord interpretation belongs to the calibration/application layer, not the filesystem format.

### 125 GeV comparison comes later

Only after lower-scale wave/lattice tests are stable may the Physics District test whether a model-derived resonance has octave-equivalent alignment with the measured Higgs-scale energy.

Do not insert 125 GeV as a fitted answer and then claim it was predicted.

---

## Build 9 — Miniverse / Mega-City interface

**Goal:** Make persistent cognitive state navigable.

Start with semantic districts and state graphs. Add a visual 2D/3D city only after the underlying state has real meaning.

A location should correspond to actual persistent relationships, tools, permissions, memory neighborhoods, or working state.

Example:

```text
new validated subject -> durable neighborhood/district growth
strong relationship -> navigable route
conflict -> unresolved state
resolved conflict -> baseline update
unused detail -> compression/archive candidate
```

**Pass when:** navigation through the interface corresponds reproducibly to state/resources underneath it and is not decorative animation.

---

## Build 10 — inter-Miniverse translation / ambassador layer

**Goal:** Let independent AI worlds communicate without forcing them to share one internal ontology or Baseline Zero.

Candidate modules based on existing One-Wave work:

- **Symbol Rabbit Hop** — symbolic/alphabet coordinate translation;
- **Resonance Rabbit Hop** — musical/frequency/scale relationship translation;
- **Circle Navigator** — cyclic relational navigation such as Circle-of-Fifths test spaces;
- bounded state-exchange packets;
- provenance and uncertainty receipts;
- local acceptance/oversight at both ends.

Rule:

**Preserve identity locally; translate relationships globally.**

No external Miniverse receives unrestricted access to another Miniverse's complete memory substrate by default.

---

## Build 11 — SCLFS integration

**Goal:** Move proven Baseline Zero/body-state/recall semantics onto the native lattice storage/runtime project after the semantics work in userspace.

Project boundaries remain:

```text
One-Wave-Science
    physics + architecture + validation reference

SCLFS
    native lattice storage/runtime and reconstruction substrate

Terminal Bridge
    controlled terminal/tool/agent access
```

SCLFS is a separate project, not a folder to silently add to Terminal Bridge.

Do not make real external-drive formatting a dependency of Builds 0-10.

Before real drive writes, require format specification, userspace image tests, reopen/crash/corruption tests, checksums, recovery tests, exact-device guards, and code review.

---

# 10. Dependency order

```text
Build 0 Contracts
      |
      +------> Build 1 Hearing ----+
      |                            |
      +------> Build 2 Vision -----+
                                   v
                            Build 3 M4 Router
                                   |
                                   v
                            Build 4 Body State
                                   |
                                   v
                     Build 5 Baseline/Recall
                                   |
                                   v
                          Build 6 Caretaker
                                   |
                                   v
                           Build 7 Avatar
                                   |
                                   v
                     Build 8 Physics District
                                   |
                                   v
                       Build 9 Mega-City UI
                                   |
                                   v
                     Build 10 Ambassador
                                   |
                                   v
                        Build 11 SCLFS port
```

Builds 1 and 2 may proceed in parallel after the event contracts are frozen.

---

# 11. First executable Jetson target

Working name: `miniverse-sense-v0`

Do **not** start with a full autonomous Avatar.

The first executable target should:

1. read microphone replay/live input;
2. read grayscale camera replay/live input when available;
3. run deterministic Cell/Nerve detectors;
4. emit compact structured deltas;
5. route them through M4 with `why_forward`;
6. maintain a small live body-state store;
7. print/store receipts;
8. run with higher reasoning disabled;
9. measure latency, event volume, false escalation, CPU/GPU/RAM, and storage growth.

A successful first demo is deliberately boring: the machine continuously hears/sees coarse structure, knows what changed, maintains state, and forwards only events that have an explicit reason.

---

# 12. System-wide acceptance rules

The architecture is not ready to move upward unless all applicable lower rules remain true:

- raw sensor firehose is not the default LLM input;
- every escalation has a `why_forward` receipt;
- Cells/Nerves/M4 continue operating with Avatar/higher reasoning disabled;
- safety/reflex routes do not depend on a language-model response;
- body state survives Avatar restart;
- Baseline Zero is versioned and auditable;
- Recall Rebuild retains provenance and uncertainty;
- inferred/generated fill is not silently treated as remembered fact;
- learning requires validation before durable baseline commit;
- false escalations and latency are measured;
- CPU/GPU/RAM/storage growth are bounded and measured;
- existing verified functionality is regression-tested at each branch-step;
- physics work distinguishes control, assumption, hypothesis, simulation, bench evidence, derivation, and falsification;
- richer hearing/color/graphics are added only after the coarse structural layer passes.

---

# 13. Immediate branch-step sequence

Do not attempt the entire roadmap in one branch.

Recommended bounded sequence:

1. **MINI-00 Event Contracts** — schemas, receipts, replay harness only.
2. **MINI-01 Coarse Hearing** — word/event-oriented audio path only.
3. **MINI-02 Grayscale Vision** — structural visual path only.
4. **MINI-03 M4 Why Router** — routing/filter/escalation only.
5. **MINI-04 Body-State Store** — live persistent internal-world state only.
6. **MINI-05 Baseline Zero / Recall** — versioned baseline and rebuild tests only.
7. **MINI-06 Caretaker** — continuity/integrity/oversight integration only.
8. **MINI-07 Avatar Interface** — higher reasoning against structured state only.
9. **MINI-08 Physics District** — persistent evidence-labeled workbench and music fixture.
10. **MINI-09 Miniverse UI** — semantic/visual navigation over real state.
11. **MINI-10 Ambassador Translation** — bounded relationship translation.
12. **MINI-11 SCLFS Adapter** — port stable state semantics to SCLFS API after SCLFS exists and passes its own storage tests.

Each branch-step must inherit the repository's hard-start, reference, allowed-files, protected-features, exact-test, progress/diary, oversight, three-strike, hard-stop, and handoff rules.

---

# 14. Design rule to keep visible

```text
DO NOT ASK ONE MODEL TO BE
THE SENSOR,
THE NERVE,
THE ROUTER,
THE WORLD,
THE MEMORY,
THE CARETAKER,
THE DREAMER,
THE REVIEWER,
AND THE EXECUTOR
AT THE SAME TIME.
```

Use narrow jobs, explicit differentials, persistent state, reconstructable memory, and bounded escalation.

The higher model should receive **meaningful reasons to think**, not every signal the machine can measure.
