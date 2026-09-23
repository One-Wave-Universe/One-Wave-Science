# CELL_V1 — CURRENT BUILD CANON

**Status:** active build specification  
**Purpose:** single source of truth for the current CELL_V1 architecture  
**Rule:** do not silently rewrite locked items. Proposed changes must be patches that identify what they replace and why.

---

## 1. CORE SUBSTRATE

CELL_V1 is built around:

**BUS + LEAN + MEMORY**

These are one recursive current system:

- **DC** = directed / biased / bus component.
- **AC** = oscillating / lean component.
- **RC** = the complete recursive current loop containing DC and AC.

DC, AC, and RC are **not three unrelated current systems**. DC and AC are phases/components of RC.

CELL_V1 is **asynchronous and threshold-gated**.

There is:
- no clock controlling state,
- no timing-based commutation,
- no software commutation table,
- no lookup table deciding when a transition happens.

A transition occurs because the physical state crosses a threshold. Timing, latency, settling, and response can be measured, but timing does not command the transition.

---

## 2. HEX GEOMETRY

Flat-top hexagon.

Connections are at the **centers of the six sides, never the corners**.

Clockwise from the top:

1. **A+** — top
2. **B+** — upper-right
3. **C+** — lower-right
4. **A−** — bottom
5. **B−** — lower-left
6. **C−** — upper-left

Mirror pairs:

- **A+ ↔ A−**
- **B+ ↔ B−**
- **C+ ↔ C−**

The three mirrored pairs are the three physical axes.

```text
                 A+
                  |
          C−             B+
            \           /
             \         /
              \ CENTER
              /       \
             /         \
          B−             C+
                  |
                 A−
```

The geometry is designed to repeat directly:

**1 cell → 2 cells → 7-cell flower → larger lattice**

The seven-cell flower is part of the scaling proof, not decoration.

---

## 3. THREE DIFFERENTIAL AXES

Each cell contains three mirrored state channels:

- A+/A−
- B+/B−
- C+/C−

Together these create the local ternary movement/state system.

Each axis participates in:
- differential decision,
- magnetic coupling,
- winding/current expression,
- return/reinjection.

The low-level differential transistor pair is **not literally the motor winding**.

Correct physical wording:

> Each A/B/C differential state channel and its associated electromagnetic winding form one phase channel.

The decision stage determines the lean. The winding is the electromagnetic expression of the same state.

---

## 4. STATE DOMAIN

Internal lean/state scale:

**0–1 V full scale**

Nominal center:

**0.50 V**

Current bands:

| Band | Voltage |
|---|---:|
| Terminal compression | 0.00–0.10 V |
| Extreme compression | 0.10–0.20 V |
| Dead zone | 0.20–0.25 V |
| Strong compression | 0.25–0.35 V |
| Dead zone | 0.35–0.40 V |
| Moderate compression | 0.40–0.45 V |
| CENTER / HOLD | 0.45–0.55 V |
| Moderate expression | 0.55–0.60 V |
| Dead zone | 0.60–0.65 V |
| Strong expression | 0.65–0.75 V |
| Dead zone | 0.75–0.80 V |
| Extreme expression | 0.80–0.90 V |
| Terminal expression | 0.90–1.00 V |

Existing hysteresis parameters retained for testing:
- partial_enter = 0.40
- partial_exit = 0.28
- full_enter = 0.82
- full_exit = 0.68

These are state thresholds, not timer settings.

---

## 5. ELECTRICAL FUNCTIONS: DECISION, GATE, POWER

The hardware has three physical jobs, but they remain part of one state event.

### Decision — ALD1106

Current candidate:
- ALD1106 matched N-channel MOSFET array

Role:
- mirrored differential lean sensing,
- low-current analog decision,
- A/B/C state comparison.

It does **not** carry winding current.

### Low-level gating — ALD110800

Current candidate:
- ALD110800 zero-threshold N-channel array

Role:
- low-level state gating where needed,
- small-signal coupling,
- gate assistance/interface where justified.

It does **not** carry motor winding current.

### Power expression — ENGINEERING OPEN

The earlier AO3400A/AO3401A pair is **not locked as the ≤1 V solution**.

Required power-stage behavior:
- governed by the ≤1 V state architecture,
- carries useful winding current,
- participates in active reinjection,
- does not introduce a separate logical control step,
- supports the eventual motor power envelope.

The power device is the **physical muscle/expression of the state**, not another controller.

---

## 6. TERNARY MAGNETIC SIDE

The ternary side contains six signed paths:

- A+
- A−
- B+
- B−
- C+
- C−

These are three mirrored pairs.

The ternary side is not only a live summing element. It also needs local hysteretic movement/power memory.

Current architectural direction:
- a mirrored **figure-8 magnetic topology** for the ternary side,
- likely rounded/circular lobes for even A/B/C coupling,
- six signed winding contributions distributed across the mirrored structure.

Exact geometry and winding placement remain engineering-open.

The ternary element should retain useful information about:
- recent direction,
- speed,
- load,
- effective power level,
- under-drive,
- over-drive,
- recovered-energy tendency.

---

## 7. WHY TERNARY MEMORY MATTERS

The ternary/motor side should learn both:

**where to move**  
and  
**how much power the movement actually needs**

Conceptual cycle:

```text
movement request
      ↓
direction + speed + load
      ↓
hysteretic learned power bias
      ↓
phase current
      ↓
actual movement
      ↓
too weak / matched / excessive
      ↓
memory shifts
      ↓
collapse / excess → V_BUS
```

Repeated use should move the physical state closer to the previously useful energy envelope rather than rediscovering it from zero every time.

---

## 8. SHORT-TERM MEMORY

Functional short-term memory is the **ternary / motor-side hysteresis**.

It is intended to adapt relatively quickly.

It remembers:
- recent movement,
- recent directional preference,
- speed band,
- recent load,
- useful power bias,
- whether the last event was under-powered or wasteful,
- recent recovery tendency.

Functional definition:

**short-term memory = recent movement / energy bias**

The actual retention time is to be measured.

---

## 9. MEDIUM-TERM MEMORY

The deeper local brain/reference element is the **square figure-8 hysteretic structure**.

Canonical shape:

```text
     ┌───────────┐   ┌───────────┐
     │           │   │           │
     │  LOBE 1   │ X │  LOBE 2   │
     │           │   │           │
     └───────────┘   └───────────┘
```

Role:
- recursive cell reference,
- previous resolved state,
- local processing history,
- retained state against which the next event is read,
- bus/lattice-side brain memory.

Functional definition:

**medium-term memory = retained local recursive reference**

Exact material, coercivity, dimensions, gaps, winding geometry, and readout remain to be bench-qualified.

---

## 10. LONG-TERM MEMORY

When cells are connected, the hysteretic lattice becomes the long-term memory layer.

Repeated paths alter the physical magnetic/electrical state of the connected substrate.

It is intended to support:
- distributed path preference,
- body-state history,
- accumulated route bias,
- learned motor patterns,
- muscle memory,
- distributed intelligence.

Functional definition:

**long-term memory = distributed hysteresis path scoring**

This is only distributed memory when the cell buses/lattice are actually connected.

---

## 11. THREE MEMORY DEPTHS

```text
SHORT TERM
ternary / motor hysteresis
recent movement + power bias

        ↓ reinforcement

MEDIUM TERM
square figure-8 cell memory
recursive retained reference

        ↓ repeated use

LONG TERM
connected lattice hysteresis
distributed path scoring / muscle memory
```

These are functional memory classes, not claimed biological-equivalent durations.

Actual retention, reinforcement, decay, overwrite, and recovery curves must be measured.

---

## 12. MEMORY REINFORCEMENT

The physical state is the memory. It is not copied into a software register.

Conceptual rule:

```text
used once
   ↓
small retained shift

used repeatedly
   ↓
larger retained bias

strongly repeated
   ↓
preferred state / route

unused or opposed
   ↓
decay / weakening / reversal
```

Exact behavior is determined by material, geometry, coupling, and threshold placement.

---

## 13. HYSTERESIS PATH SCORING

The lattice should store path history physically.

A path's physical state is its score.

Candidate measurable variables:
- switching-threshold shift,
- coercive shift,
- remanent magnetic bias,
- impedance change,
- magnetoimpedance change,
- propagation threshold,
- required drive energy.

Conceptual rule:

```text
path used
   ↓
hysteretic state changes
   ↓
future threshold changes
   ↓
path becomes easier / harder
   ↓
future routing changes
```

Initial experimental score candidate:

> **path score = normalized change in switching threshold from virgin baseline**

This metric is not locked until bench results identify the most reliable observable.

---

## 14. LATTICE MEMORY LAYER

Practical candidate stack:

```text
electrical hex lattice
       ↓
thin insulating separation
       ↓
patterned hysteretic magnetic layer
       ↓
support substrate
```

Candidate room-temperature approaches:
- patterned permalloy,
- flexible magnetic thin film,
- artificial toroidal / patterned magnetic structures,
- other room-temperature hysteretic materials.

Cryogenic ferrotoroidic materials are useful prior art but are **not the Phase-I implementation target**.

The magnetic layer may mirror the electrical hex topology so each edge/path has localized history.

---

## 15. LOCAL TOROIDAL ↔ DISTRIBUTED LATTICE STATE

Current conceptual direction:

```text
local cell magnetic state
        ↓
expressed into lattice
        ↓
distributed lattice state changes
        ↓
hysteretic path history remains
        ↓
lattice state returns / biases cell
        ↓
next local magnetic state
```

Short form:

**cell brain → body lattice → cell brain**

The lattice is not only interconnect. It is intended to become a history-bearing body substrate.

---

## 16. FIELD AND VOID ARE BOTH BIDIRECTIONAL

Do **not** map:
- Field = information out
- Void = action back

That is retired.

Correct rule:

Both Field and Void:
- send information,
- receive information,
- act,
- return state,
- participate in recombination.

```text
local state
   ↓
Field half + Void half
   ↓
both propagate
   ↓
both interact
   ↓
both return
   ↓
recombine
   ↓
next local state
```

The two mirrored halves operate concurrently.

---

## 17. M4 STRUCTURE

M4 retains the mirrored four-up / four-down structure.

### Views / up
- 2 Field
- 2 Void
- total = 4 views

### Actions / down
- 2 Field
- 2 Void
- total = 4 actions

```text
2 Field + 2 Void UP
        ↓
interaction / resolution
        ↓
2 Field + 2 Void DOWN
```

Both Field and Void participate in both directions.

Existing conceptual labels may be used:
- Views: BASELINE, DELTA, HEADING, RESULT
- Actions: PULL, PUSH, FLIP, PASS

The hardware mapping of these labels must remain tied to measurable physical states.

---

## 18. FOUR-STATE / FERROTOROIDAL ANALOGY

Useful established analogy:
- two independent binary degrees of freedom can produce four retained magnetic states.

CELL_V1 can use this as a physical state-model analogy for M4 and mirrored Field/Void structure.

Do **not** claim that CELL_V1 has already reproduced the exact material physics of a specific ferrotoroidic system.

Engineering target:
- room-temperature,
- measurable,
- stable enough to read,
- coupled bidirectionally between local cell and lattice.

---

## 19. OPPOSING ROTATIONS AND OSCILLATION

Two opposed rotating components can combine into an oscillatory resultant.

Working interpretation:
- balanced opposing rotations → AC-like oscillation,
- imbalance between them → DC-like bias,
- complete retained/reinjected process → RC.

Therefore:

**RC contains DC + AC**

DC, AC, and RC must not be represented as three independent electrical subsystems.

---

## 20. REINJECTION

Reinjection is fundamental and local.

The winding does not simply dump stored magnetic energy.

Its collapse/back-EMF must return into the cell's own **V_BUS** loop through the active power topology.

```text
state
 ↓
phase power
 ↓
winding
 ↓
motion / electromagnetic action
 ↓
collapse + back-EMF
 ↓
actively gated return
 ↓
V_BUS
 ↓
next state
```

No separate reinjection controller.

No separate normal dump subsystem.

Drive and return are two phases of the same recursive state/power event.

---

## 21. V_BUS

For one cell, V_BUS is:
- local reinjection bus,
- local energy condition,
- local body-state contribution.

For a connected lattice, linked buses become part of:
- distributed body state,
- cross-cell interaction,
- distributed intelligence,
- muscle memory,
- accumulated path history.

Important:

> A single cell does not by itself equal distributed intelligence. The distributed function appears when cell buses/lattice paths are connected.

---

## 22. CONTROL MODES

CELL_V1 must support three modes through the **same state interface**.

### Autonomous
Brain/lattice state drives the cell.

### Commanded
External command biases/imposes the same ordinary state interface.

### Assisted
External input and retained local state both contribute.

Do not add a second downstream motor-controller architecture for commanded operation.

All modes use the same cell state path.

---

## 23. MOTOR / MUSCLE MEMORY

Current favored functional model:

**coarse trigger + stacked local memory + distributed completion**

A learned skill should not require a higher-level controller to replay every motor detail.

Conceptual chain:

```text
high-level cue
      ↓
sequence / movement target
      ↓
short-term motor bias
      ↓
medium-term local reference
      ↓
long-term lattice path scores
      ↓
distributed completion
      ↓
movement
```

Later experiments should distinguish:
- detailed trajectory storage,
- stacked-trigger completion,
- or a mixture of both.

---

## 24. TWO-STATE-MACHINE BRAIN

Above the physical cell/lattice is the larger mirrored brain architecture:

- Field state machine
- Void state machine

They are complementary roles operating against the same recursive state architecture.

They interact with:
- cell state,
- local memory,
- distributed body/lattice state,
- recall/rebuild,
- subconscious loop,
- deliberate/commanded control.

---

## 25. SUBCONSCIOUS LOOP

The subconscious layer is intended to handle:
- learned motor routines,
- reflex,
- reconstruction from partial cues,
- body-state influence,
- sequence completion,
- automatic power adaptation,
- habitual paths.

Higher-level control should not need to micromanage every motor output.

---

## 26. SCALING

The architecture is designed to repeat without adding a new central controller.

Build sequence:

```text
one cell
   ↓
two coupled cells
   ↓
seven-cell flower
   ↓
larger lattice
```

The seven-cell flower:
- one center cell,
- six surrounding cells.

Scaling requirement:
- local state remains local,
- memory remains measurable,
- coupling occurs through canonical edge interfaces,
- no new global clock,
- no external lookup controller,
- the same Field/Void and reinjection rules survive coupling.

---

## 27. CURRENT HARDWARE / PART STATUS

### Decision
- ALD1106 — current candidate for matched differential sensing.

### Low-level gating
- ALD110800 — current candidate for zero-threshold small-signal gating.

### Power
- **OPEN**
- must satisfy the ≤1 V state-control requirement without becoming a separate controller.
- eventual motor voltage/current must be supported.
- must provide controlled active return into V_BUS.

### AO3400A / AO3401A
- not canonical as the final ≤1 V power solution.
- may remain bench alternatives if used with a different gate condition.
- do not list them as guaranteed ≤1 V power switches.

### ALD110900
- retired from the canonical P-channel role.
- do not describe it as the P-channel counterpart.

---

## 28. MATERIAL STATUS

### Ternary / motor-memory magnetic element
Engineering-open:
- material,
- coercivity,
- exact figure-8 geometry,
- six-winding placement,
- retention/decay.

Target behavior:
- faster/adaptive local hysteresis,
- movement/power bias.

### Square figure-8 local brain/reference
Engineering-open:
- room-temperature magnetic material,
- exact dimensions,
- gap geometry,
- winding geometry,
- read/write coupling.

Target behavior:
- more persistent local recursive reference.

### Lattice memory
Engineering-open:
- continuous vs patterned film,
- permalloy or alternative material,
- thickness,
- substrate,
- edge coupling,
- electrical/magnetic spacing.

Target behavior:
- distributed hysteresis path scoring.

---

## 29. BUILD ORDER

### Phase 1 — One axis
Prove:

**≤1 V state/lean → threshold transition → useful phase current → winding action → active collapse/reinjection → retained local bias**

### Phase 2 — Three axes
Build A/B/C mirrored phase system.

Prove:
- positive / negative / HOLD,
- threshold-driven phase behavior,
- no timing controller.

### Phase 3 — Ternary local memory
Add hysteretic motor-memory element.

Prove:
- direction bias,
- speed/load power memory,
- adaptation from repeated use.

### Phase 4 — Square figure-8 local brain/reference
Add deeper local retained reference.

Prove:
- write,
- retention,
- next-event influence.

### Phase 5 — Lattice memory layer
Add connected hysteretic path layer.

Prove:
- path scoring,
- reinforcement,
- decay/competition,
- measurable effect on future routing.

### Phase 6 — Two cells
Prove canonical edge-to-edge interaction.

### Phase 7 — Seven-cell flower
Prove that local rules survive scaling and that distributed lattice state becomes measurable.

Each phase is go/no-go and should not silently redefine the previous phase.

---

## 30. PRIMARY MEASUREMENTS

### State / threshold
- lean voltage,
- threshold crossing,
- CENTER/HOLD behavior,
- hysteresis width,
- threshold-to-transition latency.

### Winding / power
- phase voltage,
- phase current,
- winding resistance,
- winding inductance,
- load,
- speed where applicable,
- temperature.

### Motor-memory
- required current for repeated identical action,
- energy per action,
- speed/load correspondence,
- shift in useful-power threshold,
- under/over-drive correction.

### Local magnetic memory
- coercive threshold,
- remanent state,
- retention,
- write endurance,
- next-event bias.

### Reinjection
- V_BUS before event,
- V_BUS after event,
- winding energy before collapse,
- recovered bus energy,
- switching loss,
- thermal loss.

For a capacitor bus:

**ΔE_BUS = ½ C (V_final² − V_initial²)**

Recovery fraction must compare recovered energy against an explicitly measured/estimated available energy denominator.

### Lattice path scoring
- threshold shift,
- remanence shift,
- impedance/magnetoimpedance shift,
- response-energy shift,
- route-selection change after repeated traversal.

---

## 31. LOCKED / NEAR-LOCKED ITEMS

Treat these as authoritative unless explicitly patched:

- flat-top hexagon,
- connections at edge centers, not corners,
- A+ → B+ → C+ → A− → B− → C− clockwise,
- A+↔A−, B+↔B−, C+↔C− mirror axes,
- three A/B/C differential axes,
- 0–1 V internal lean/state domain,
- CENTER/HOLD around 0.50 V,
- threshold gating,
- no timing-based state control,
- no global clock,
- BUS + LEAN + MEMORY core substrate,
- DC and AC are components of RC,
- phase power is physical expression of the state, not a separate controller,
- collapse/back-EMF feeds the cell's own V_BUS reinjection loop,
- autonomous/commanded/assisted control use the same state interface,
- Field and Void both send, receive, and act,
- M4 = 2F + 2V views up and 2F + 2V actions down,
- square figure-8 is the deeper local brain/reference memory geometry,
- ternary side requires local hysteretic movement/power memory,
- connected lattice uses hysteresis path scoring,
- short-term / medium-term / long-term functional memory hierarchy,
- seven-cell flower is part of scaling validation,
- no separate conventional downstream motor controller.

---

## 32. ENGINEERING-OPEN ITEMS

Do not guess these into canon:

- exact ternary figure-8 geometry,
- circular vs rounded-square ternary lobes,
- exact A+/A− B+/B− C+/C− winding placement,
- final ≤1 V-compatible power switch/topology,
- motor voltage/current envelope,
- exact synchronous reinjection schematic,
- exact CENTER electrical extraction,
- magnetic material selection,
- magnetic dimensions / coercive targets,
- lattice memory material and thickness,
- continuous vs patterned lattice memory sheet,
- exact path-score metric,
- short/medium/long retention times,
- reinforcement / decay / overwrite curves,
- exact room-temperature toroidal/non-toroidal implementation.

---

## 33. TO-BE-MEASURED / TESTED

These are experimental questions, not reasons to rewrite the architecture:

- Does the three-axis cell commutate/useful phase-actuate under threshold control?
- Does the ternary hysteresis learn recent movement and useful power?
- Does the square figure-8 hold a stable enough local reference?
- Does local retained state affect event N+1?
- Can active power switching return measurable collapse/back-EMF energy to V_BUS?
- Does repeated lattice traversal create a measurable path score?
- Does the lattice produce stable cross-cell coupling?
- Do two cells preserve local state while interacting?
- Does the seven-cell flower preserve the same local rules?
- Which memory layer actually maps to which measured retention timescale?

---

## 34. RETIRED / DO NOT REINTRODUCE SILENTLY

- corner connections on the hex,
- timing-based commutation,
- clocked state gating,
- Field-only views / Void-only actions,
- DC, AC, RC as three independent current systems,
- ALD110900 described as P-channel,
- AO3400A/AO3401A claimed as the locked ≤1 V power solution,
- small-signal ALD arrays carrying the actual motor winding current,
- a separate conventional motor controller bypassing CELL_V1,
- a separate normal reinjection controller,
- whole-lattice distributed-intelligence claims for a single isolated cell,
- cryogenic ferrotoroidics as the required Phase-I material,
- automatic claim that any magnetic vortex is a quantum qubit.

---

## 35. PHASE-I SUCCESS CHAIN

Minimum physical proof:

```text
0–1 V lean/state
      ↓
threshold crossing
      ↓
same-state power expression
      ↓
phase winding
      ↓
magnetic state / movement
      ↓
collapse/back-EMF
      ↓
active return to V_BUS
      ↓
retained short-/medium-term state
      ↓
next event is measurably biased
```

Then:

```text
one cell
  ↓
two cells
  ↓
seven-cell flower
  ↓
measurable lattice path scoring
```

---

## 36. CURRENT ONE-SENTENCE DESCRIPTION

> **CELL_V1 is a threshold-gated hexagonal electromagnetic cell in which bus, lean, and memory operate as one recursive current system; local ternary hysteresis remembers recent movement and efficient power, a square figure-8 retains deeper recursive state, the winding's collapse/back-EMF reinjects into the cell's own V_BUS, and connected cells form a hysteretic lattice whose scored paths provide distributed long-term body/muscle memory.**

---

## 37. CANON CHANGE RULE

Future AI work must not regenerate this document from memory.

For any change:

1. identify the exact section,
2. quote the current rule,
3. state the proposed replacement,
4. explain why,
5. identify dependent sections,
6. apply only after approval,
7. record the change.

**Patch the canon. Do not silently rewrite it.**
