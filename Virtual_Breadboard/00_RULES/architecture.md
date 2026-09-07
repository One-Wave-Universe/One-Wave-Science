# Virtual Breadboard — Canonical Layered Architecture

## Purpose

The Virtual Breadboard is a reusable simulation and measurement tool.

It is not a collection of project builds.

Flashlights, nerves, motors, cells, speakers, controllers, and other builds are things
that are put onto the breadboard and tested with it.

The breadboard itself provides:

- rules
- parts
- connectivity
- electrical physics
- time/transient behavior
- measurements
- reusable physical primitives
- magnetic behavior
- power behavior
- test infrastructure
- receipts

The system must be organized so one broken layer can be repaired without rebuilding
the entire simulator.

## Fundamental architecture

```
VIRTUAL_BREADBOARD/
│
├── 00_RULES/                 authority layer (this directory)
├── 01_PARTS/                 individual physical components
├── 02_CONNECTIONS/           topology: what's connected to what
├── 03_ELECTRICAL_CORE/       DC solving: given topology, what are V/I?
├── 04_TIME_AND_DYNAMICS/     transient/time-varying behavior
├── 05_MEASUREMENT/           observation, never mutation
├── 06_PRIMITIVES/            reusable arrangements built from lower layers
├── 07_MAGNETICS/             coupled coils, transformers, field behavior
├── 08_POWER/                 sources, batteries, energy accounting
├── 09_TESTS/                 tests mirror the architecture, one dir per layer
├── 10_RECEIPTS/              every test produces a receipt
└── 11_INTERFACE/             UI sits on top, owns no physics
```

External builds remain separate:

```
BUILDS/
├── flashlight/
├── nerve/
├── motor/
├── speaker/
├── cell/
└── ...
```

A build uses the breadboard. A build does not become part of the breadboard.

**Status note (see `../LAYER_MAP.md`):** this directory tree is the canonical target.
The current codebase (`js/circuit.js`, `simulate.js`, `js/app.js`, `js/board.js`,
`js/components.js`, `js/ai.js`) predates this canon and implements most of layers
01-08 as one coupled module rather than as physically separate directories. That is
a real, tracked architecture debt — see `../LAYER_MAP.md` for the file-by-file
mapping and `failure_rules.md` / this file's "No-rebuild protection" section for why
it is repaired incrementally, layer by layer, rather than rewritten in one pass.

## Core rules

**Rule 1 — Real behavior over desired behavior.** The simulator represents the
modeled physics. Never alter circuit behavior merely because a proposed build was
expected to work differently.

**Rule 2 — No total rebuild.** Working layers remain intact. A failure in one layer
does not authorize redesigning the rest of the simulator.

**Rule 3 — Layer ownership.** Every bug or update must first be assigned to one
responsible layer. Modify that layer only, unless an actual interface dependency
requires another change.

**Rule 4 — Preserve working behavior.** Anything already passing remains a permanent
regression requirement.

**Rule 5 — Failure is valid output.** The simulator must allow shorts, excessive
current, voltage sag, center movement, unstable oscillation, component overload,
MOSFET shoot-through, battery depletion, capacitor discharge, inductive flyback,
losses, and thermal rise where modeled. Do not silently correct bad circuits.

**Rule 6 — No unexplained magic primitives.** Higher-level behavior must be
constructed from lower-level physical capabilities.

**Rule 7 — Measurements determine PASS.** Visual appearance does not determine
success. Numerical measurements and declared tolerances determine PASS or FAIL.

**Rule 8 — Build definitions remain external.** A flashlight failure does not mean
"change the breadboard until the flashlight works." Determine whether (1) the
breadboard physics is wrong, (2) the build definition is wrong, or (3) the real
circuit simply does not perform as expected. Those are different outcomes.

(Full text and worked examples for each rule: see `physics_rules.md`,
`failure_rules.md`, `testing_rules.md`, `measurement_rules.md`, `interface_rules.md`.
Process rules — how a worker applies these day to day — are in `update_rules.md`.)

## Work cycle

Every update follows exactly this loop:

1. Observe failure
2. Identify responsible layer
3. Read that layer's rules
4. Reproduce failure
5. Make smallest coherent fix
6. Run layer tests
7. Run direct dependency regressions
8. Save receipt
9. Mark PASS or FAIL
10. Stop

Not: find bug → notice old architecture → clean everything up → rewrite simulator →
lose previous behavior.

## Status system

Every capability has only four valid states: **MISSING**, **IMPLEMENTING**,
**FAILING**, **PASSING**. Not "planned-ish," "mostly done," "architecture updated,"
"documented," "should work," or "probably fixed." Documentation is not
implementation.

## Permanent regression rule

The first time something passes: PASS → receipt saved → test becomes permanent.
Future work must keep it passing. That is how the breadboard accumulates capability
instead of relearning the same thing repeatedly.

## Build interaction rule

External builds submit: parts, parameters, connections, initial conditions, runtime,
requested measurements, pass criteria.

The breadboard returns: electrical state, time evolution, measurements, warnings,
failures, scope data, energy accounting, receipt.

The breadboard does not contain project intent. It does not know "this is a One-Wave
flashlight." It knows "9V source connected to these components in this topology with
these requested measurements." That separation must remain absolute.

## Worker ownership

For parallel work, divide workers like this:

- **Worker A** — Parts + component models
- **Worker B** — Connections + electrical solver
- **Worker C** — Time/transient dynamics
- **Worker D** — Measurement + scope + exports
- **Worker E** — Power + magnetics + advanced physical models
- **Integrator** — Interfaces between layers only, regression verification, no broad
  redesign

When one worker finds a problem owned by another layer: do not fix that other
layer's code casually. Create a failure receipt and hand it to the responsible
layer. Example: a measurement worker discovers voltage samples look wrong, checks
raw solver output, and finds the raw output is already wrong — the fix is a
receipt against the electrical-core layer, not a patch inside the scope math that
would hide the real bug.

## Integration contracts

Layers communicate through explicit contracts:

```
PARTS            → component equations/state
CONNECTIONS      → circuit topology
ELECTRICAL CORE  → solved electrical state
TIME             → state at t and t+Δt
MEASUREMENT      → observations
POWER/MAGNETICS  → specialized physical state
INTERFACE        → presentation
```

A layer may depend downward. It must not reach upward. A MOSFET model must never
ask "is this being used in the flashlight?"

## No-rebuild protection

A total rewrite is allowed only if ALL of these are true:

1. The current foundation is demonstrably incapable of supporting a required
   capability.
2. The problem cannot be isolated to a layer/interface.
3. Existing regression behavior has been captured.
4. The replacement can reproduce those regressions.
5. The reason is documented before work starts.

"Code is messy" is not sufficient. "I'd organize it differently" is not sufficient.
"A new project needs a feature" is not sufficient. Default action is: repair or
extend the responsible layer.

## First build order

**Stage 1** — 00 Rules, 01 Parts, 02 Connections, 03 Electrical Core, 05
Measurement, 09 Tests, 10 Receipts. Prove: DC source, resistor, series circuit,
parallel circuit, voltage divider, loaded midpoint, node voltage, differential
voltage, branch current, power.

**Stage 2** — Add 04 Time and Dynamics. Prove: capacitor, RC, inductor, LC/RLC,
switching.

**Stage 3** — Add 08 Power. Prove: source resistance, battery sag, capacity,
energy accounting.

**Stage 4** — Add 06 Primitives. Prove reusable: shared center, differential pair,
MOSFET switching stages, hysteresis, reinjection.

**Stage 5** — Add 07 Magnetics. Prove: one winding, coupled pair, three windings,
phase, measurable field behavior.

The interface can be improved alongside this work, but interface work may never
redefine physical results.

(See `../LAYER_MAP.md` for where the current codebase already sits against these
stages — short version: Stages 1-5's *capabilities* are already proven by the
existing test suites, but not yet organized into these physical directories.)

## Final development rule

The breadboard grows like this:

```
RULE → PART → CONNECTION → PHYSICS → TIME → MEASUREMENT → PRIMITIVE
     → SPECIALIZED PHYSICS → TEST → RECEIPT
```

Every repair goes back to the exact layer responsible for it. Never restart from
the top because something near the bottom changed. Never rebuild the whole
breadboard because one experiment exposed one missing capability. Locate the
layer. Fix the layer. Test the layer. Check its interfaces. Save the receipt.
Move forward.
