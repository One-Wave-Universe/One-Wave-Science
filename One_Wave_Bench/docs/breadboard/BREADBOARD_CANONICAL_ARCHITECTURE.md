# VIRTUAL BREADBOARD — CANONICAL ARCHITECTURE

This file defines what the Virtual Breadboard is, how it is divided into layers, how work is assigned, and how one layer is repaired without rebuilding the whole simulator.

The Virtual Breadboard is a reusable simulation and measurement tool. It is not a collection of project builds. Flashlights, nerves, motors, speakers, cells, controllers, and other builds are things that are put onto the breadboard and tested with it. They are not part of the breadboard architecture.

Existing runnable bench systems remain in place. This document does not authorize a rewrite of working D-413, UI, receipt, chart, launcher, or other existing subsystems. New electrical capability is added by layer and must preserve existing regressions.

## 1. What the Breadboard owns

The Breadboard owns:
- rules;
- generic parts;
- physical connectivity/topology;
- electrical solving;
- time/transient behavior;
- measurements;
- reusable physical circuit primitives;
- magnetic behavior;
- source/power/energy behavior;
- test infrastructure;
- receipts;
- the operator interface.

The Breadboard does not own project intent.

An external build submits parts, parameters, wiring, initial conditions, requested runtime, measurements, and pass criteria. The Breadboard returns modeled electrical state, time evolution, measurements, warnings, failures, scope data, energy accounting, and receipts.

The Breadboard should know `9 V source + topology + load + measurements`, not `this is a flashlight`.

## 2. Canonical layer map

```text
VIRTUAL_BREADBOARD/
├── 00_RULES/
├── 01_PARTS/
├── 02_CONNECTIONS/
├── 03_ELECTRICAL_CORE/
├── 04_TIME_AND_DYNAMICS/
├── 05_MEASUREMENT/
├── 06_PRIMITIVES/
├── 07_MAGNETICS/
├── 08_POWER/
├── 09_TESTS/
├── 10_RECEIPTS/
└── 11_INTERFACE/
```

This map defines responsibility boundaries. Existing implementation files do not need to be physically moved simply to match the diagram. Moving files without a concrete implementation need is not progress.

External project builds remain outside these layers.

## 3. Layer 00 — RULES

Owns architecture, physics, update, testing, measurement, failure, and interface rules.

Core rules:

### 3.1 Modeled behavior over desired behavior
The simulator represents the modeled circuit behavior. Never alter the circuit or simulator answer merely because a project expected a different result.

### 3.2 No total rebuild
A local failure does not authorize redesigning the whole Breadboard. Preserve working layers.

### 3.3 Layer ownership
Every bug or requested capability must first be assigned to one responsible layer. Modify that layer only unless a concrete interface dependency requires a second layer.

### 3.4 Preserve passing behavior
Anything that passes becomes a permanent regression requirement.

### 3.5 Failure is valid output
The simulator must be able to expose bad behavior rather than silently protecting the user from it, including:
- shorts;
- excessive current;
- source/battery sag;
- center/reference movement;
- unstable oscillation;
- MOSFET shoot-through;
- battery depletion;
- capacitor discharge;
- inductive flyback;
- component losses;
- thermal rise where modeled;
- floating nodes and open circuits.

### 3.6 No unexplained magic primitives
Higher-level behavior must be assembled from lower-level physical capabilities. Do not hide Field/Void, ternary resolution, reinjection, or other behavior inside a macro that simply returns the desired answer.

### 3.7 Measurements determine PASS
Numerical measurements and declared tolerances determine PASS/FAIL. A pretty waveform is not a pass criterion.

### 3.8 Builds remain external
If an external build fails, determine which is true:
1. the simulator/model is wrong;
2. the submitted build/circuit is wrong;
3. the modeled circuit genuinely fails to do what was expected.

Do not automatically modify the Breadboard until a Breadboard-layer defect is demonstrated.

## 4. Layer 01 — PARTS

Owns individual generic component models.

Initial parts include:
- DC voltage source;
- current source where needed;
- resistor;
- capacitor;
- diode;
- red/blue/white LED models;
- N-channel MOSFET;
- P-channel/high-side MOSFET where supported;
- switch;
- inductor;
- comparator/threshold-capable element;
- battery;
- sensors where supported.

Each part defines only itself, including as applicable:
- pins/terminals;
- configurable parameters;
- state;
- voltage/current relationships;
- losses;
- operating limits;
- measurement exposure.

Examples:

```text
RESISTOR
R
V
I
P
tolerance
optional temperature coefficient
```

```text
MOSFET
gate
drain
source
Vgs
Vds
Ids
Rds_on
threshold behavior
off leakage
power dissipation
```

No part model may ask what project is using it.

If the MOSFET model is wrong, repair the MOSFET model and its tests. Do not rewrite measurement, magnetics, battery behavior, primitives, UI, or external builds.

## 5. Layer 02 — CONNECTIONS

Owns what is electrically connected to what.

Includes:
- node;
- wire;
- terminal/pin;
- rail;
- junction;
- ground/reference;
- breadboard-row connectivity;
- topology building;
- open-circuit detection;
- short detection;
- floating-node detection;
- branch discovery;
- loop discovery.

This layer creates topology. It does not calculate voltages/currents.

If two breadboard holes that should connect are treated as separate, fix this layer. Do not compensate in the electrical solver.

## 6. Layer 03 — ELECTRICAL CORE

Owns solving connected electrical networks.

Includes:
- DC solver;
- nodal solve;
- branch-current solve;
- nonlinear component solve;
- convergence;
- numerical tolerances;
- common/differential electrical state;
- power balance calculations needed by the core.

Responsibilities include:
- node voltages;
- branch currents;
- source/load interaction;
- Kirchhoff relationships;
- nonlinear operating points;
- solver convergence/error reporting.

This layer is generic. No Field/Void, flashlight, nerve, motor, or other project semantics belong here.

If parallel resistors produce the wrong total current, fix this layer or the responsible part model—not the UI or a higher primitive.

## 7. Layer 04 — TIME AND DYNAMICS

Owns anything that changes over simulation time.

Includes:
- timestep management;
- transient solver;
- numerical integration;
- capacitor state;
- inductor state;
- switching events;
- oscillator state;
- delays;
- RC timing;
- LC/RLC ringdown;
- history/state storage needed for transient execution.

DC and transient responsibilities remain intentionally separable.

If a DC operating point is correct but capacitor decay timing is wrong, fix this layer. Do not rewrite the DC solver unless evidence shows the DC state itself is wrong.

## 8. Layer 05 — MEASUREMENT

Owns observing modeled state.

Required measurement capabilities:
- node voltage;
- differential voltage;
- branch current;
- source current;
- instantaneous power;
- average power/current where required;
- integrated energy;
- RMS voltage/current;
- frequency;
- phase difference;
- duty cycle;
- transient/scope trace;
- battery energy/capacity remaining;
- source/internal-resistance effects;
- temperature where modeled;
- machine-readable export.

Meters observe. They do not change the modeled result unless meter loading is intentionally part of the model.

If raw electrical state is correct but the differential meter reports the wrong value, fix measurement. Do not change the solver to satisfy a broken meter.

## 9. Layer 06 — REUSABLE PRIMITIVES

Owns reusable circuit arrangements assembled from lower layers.

Examples:
- voltage divider;
- loaded midpoint/passive virtual ground;
- shared center;
- differential pair;
- balanced load;
- low-side switch;
- high-side switch;
- half bridge/push-pull;
- full bridge/differential load;
- RC delay;
- threshold;
- hysteresis;
- energy storage;
- reinjection loop;
- resolved `- / HOLD / +` state;
- phase handoff.

A primitive must be expandable/inspectable as ordinary parts and connections.

Example:

```text
reinjection
  -> storage element
  -> lower threshold
  -> upper threshold
  -> switching element
  -> source
  -> load
  -> measurements
```

Do not implement `FieldVoidChip()` or `ReinjectionMagic()` that bypasses lower-layer physics.

If a hysteresis network is wired incorrectly while its parts and solver work correctly, fix this layer.

## 10. Layer 07 — MAGNETICS

Owns coupled magnetic behavior beyond an isolated inductor.

Includes:
- single-coil magnetic state where modeled;
- coupled coils;
- transformer behavior;
- mutual inductance;
- winding polarity;
- coupling coefficients;
- three independently accessible windings;
- field-vector calculation where supported;
- Hall/field measurement where supported.

Progress in this order:

```text
single inductor
      ↓
two coupled coils
      ↓
transformer/coupling regression
      ↓
three independent windings
      ↓
field-vector measurement
```

Three-winding support must expose W1/W2/W3 independently with voltage, current, winding resistance, polarity, inductance, coupling, and phase.

Do not assume a field is spherical or has a desired path. Where field simulation exists, expose measurable `Bx`, `By`, and `Bz` and determine the actual vector path from the result.

## 11. Layer 08 — POWER

Owns source limits and energy accounting.

Includes:
- source models;
- battery models;
- internal resistance;
- capacity;
- voltage sag;
- source-current limits;
- energy storage accounting;
- losses;
- efficiency;
- thermal behavior where modeled.

Battery models should support:
- nominal voltage;
- capacity;
- internal resistance;
- voltage sag under load;
- energy consumed;
- remaining capacity;
- load-dependent runtime.

A 9 V alkaline reference remains a priority fixture because existing qualification work uses it, but the power layer must remain generic.

Energy accounting must be explicit:

```text
source energy
=
change in stored energy
+ load energy
+ modeled losses
+ declared numerical/model residual
```

If the accounting does not close within declared tolerance, warn or fail the run. Reinjection is not an energy source.

## 12. Layer 09 — TESTS

Tests mirror architecture ownership.

```text
09_TESTS/
├── rules/
├── parts/
├── connections/
├── electrical_core/
├── dynamics/
├── measurement/
├── primitives/
├── magnetics/
├── power/
└── integration/
```

Permanent baseline regressions include:
1. DC source;
2. resistor / Ohm's law;
3. series and parallel resistor networks;
4. voltage divider and loaded divider;
5. LED + current limiting;
6. diode forward/reverse behavior;
7. simple rectifier;
8. capacitor charge/discharge;
9. RC low-pass;
10. RC high-pass;
11. inductor current ramp/flyback;
12. LC/RLC storage and ringdown;
13. MOSFET low-side switch;
14. MOSFET high-side switch;
15. half bridge with shoot-through detection;
16. full bridge/differential load;
17. passive virtual ground/loaded midpoint sag;
18. active/buffered reference where supported;
19. comparator threshold;
20. comparator with hysteresis;
21. relaxation oscillator;
22. transformer/coupled coils;
23. three coupled windings;
24. battery discharge/source resistance;
25. balanced differential load;
26. reinjection storage loop.

A passing capability becomes a permanent regression rather than being redesigned on the next work pass.

## 13. Layer 10 — RECEIPTS

Every qualification test emits:

```text
TEST:
LAYER:
VERSION:
EXPECTED:
ACTUAL:
TOLERANCE:
PASS/FAIL:
DEPENDENCIES:
NOTES:
```

Valid capability states are only:
- MISSING
- IMPLEMENTING
- FAILING
- PASSING

`documented`, `planned`, `mostly done`, `should work`, and `architecture updated` do not mean implemented.

No worker may claim a physical capability works without a numerical receipt appropriate to that capability.

## 14. Layer 11 — INTERFACE

Owns operator presentation and controls.

Includes:
- schematic/breadboard editor;
- part palette;
- wire/placement controls;
- meters;
- oscilloscope view;
- run/stop controls;
- experiment request controls;
- import/export;
- status/errors/warnings;
- integration with existing ledger/chart infrastructure where appropriate.

The interface does not own physics.

If exported/raw solver values are correct but a graph is scaled incorrectly, fix the interface. Do not alter the physical model to make the graph look right.

## 15. Work division

Every task must state:

```text
TARGET LAYER:
SPECIFIC FAILURE OR CAPABILITY:
ALLOWED FILES:
DIRECT DEPENDENCIES:
TESTS TO RUN:
PASS CONDITION:
STOP CONDITION:
```

Suggested parallel ownership:
- Worker A: Parts/component models
- Worker B: Connections + Electrical Core
- Worker C: Time/Transient Dynamics
- Worker D: Measurement + Scope + machine-readable export
- Worker E: Power + Magnetics + advanced physical models
- Integrator: cross-layer interfaces + regression verification only

The Integrator is not authorized to broadly redesign working layers.

When a worker discovers a defect owned by another layer, reproduce it, issue a failure receipt, and hand it to the responsible layer. Do not casually patch around it.

## 16. Bug routing

- ambiguous architecture/update rule -> 00 RULES
- wrong resistor/MOSFET/capacitor/etc. model -> 01 PARTS
- wrong breadboard row/wire/node connectivity -> 02 CONNECTIONS
- wrong solved voltage/current despite correct topology/parts -> 03 ELECTRICAL_CORE
- wrong RC/LC/switching timing -> 04 TIME_AND_DYNAMICS
- correct modeled state but wrong meter/scope/export value -> 05 MEASUREMENT
- correct lower physics but wrong reusable circuit arrangement -> 06 PRIMITIVES
- wrong coupling/mutual-inductance/field behavior -> 07 MAGNETICS
- wrong battery sag/capacity/energy/loss behavior -> 08 POWER
- incorrect expected regression value -> 09 TESTS
- correct underlying values but incorrect presentation/control -> 11 INTERFACE

Do not fix a broken test by changing correct physics.

## 17. Cross-layer change rule

Before editing:

```text
PRIMARY LAYER:
SECONDARY LAYER IF REQUIRED:
WHY:
FILES EXPECTED TO CHANGE:
TESTS TO RUN:
```

A second layer is allowed only for a demonstrated interface dependency.

If a supposedly local bug suddenly requires broad edits across unrelated layers, stop and re-triage. That indicates scope drift or an architectural boundary problem.

## 18. Work cycle

Every update follows:

```text
OBSERVE FAILURE OR MISSING CAPABILITY
      ↓
IDENTIFY OWNING LAYER
      ↓
READ THAT LAYER'S RULES/CONTRACT
      ↓
REPRODUCE OR DEFINE THE MINIMAL TEST
      ↓
MAKE THE SMALLEST COHERENT FIX
      ↓
RUN OWNING-LAYER TESTS
      ↓
RUN DIRECT INTERFACE/DEPENDENCY REGRESSIONS
      ↓
SAVE RECEIPT
      ↓
MARK PASS OR FAIL
      ↓
STOP
```

Do not use this pattern:

```text
find local bug
  ↓
notice old code
  ↓
clean everything
  ↓
rewrite simulator
  ↓
lose prior behavior
```

## 19. No-rebuild protection

A total replacement is allowed only if all are true:
1. the current foundation is demonstrably incapable of a required capability;
2. the failure cannot be isolated to a layer/interface;
3. existing passing behavior has executable regressions;
4. the replacement reproduces those regressions;
5. the reason is documented before replacement begins.

`code is messy`, `I prefer another architecture`, and `a new build needs another feature` are not sufficient reasons.

Default action: repair or extend the responsible layer.

## 20. Capability build order

### Stage 1 — Foundation
Use Rules + Parts + Connections + Electrical Core + Measurement + Tests + Receipts.

Prove:
- DC source;
- resistor;
- series/parallel circuits;
- voltage divider;
- loaded midpoint;
- node voltage;
- differential voltage;
- branch/source current;
- power.

### Stage 2 — Dynamics
Add Time and Dynamics.

Prove:
- capacitor charge/discharge;
- RC behavior;
- inductor current/flyback;
- LC/RLC behavior;
- switching transitions.

### Stage 3 — Power
Add Power.

Prove:
- source resistance;
- battery sag;
- capacity/runtime;
- complete energy accounting.

### Stage 4 — Reusable primitives
Add/qualify:
- shared center;
- balanced/differential pair;
- MOSFET switching stages;
- threshold/hysteresis;
- reinjection.

### Stage 5 — Magnetics
Add/qualify:
- one winding;
- coupled pair;
- three windings;
- phase/coupling;
- field measurement where supported.

Do not jump to a higher layer to fake a lower capability that is still missing.

## 21. External-build contract

External builds submit:

```text
PARTS
PARAMETERS
CONNECTIONS
INITIAL CONDITIONS
RUN TIME / STOP CONDITION
REQUESTED MEASUREMENTS
PASS CRITERIA
```

The Breadboard returns:

```text
MODELED STATE
TIME EVOLUTION
MEASUREMENTS
WARNINGS
FAILURES
SCOPE/TRACES
ENERGY ACCOUNTING
RECEIPT
```

Project-specific build definitions must not be embedded into Breadboard physics, parts, or solver layers.

## 22. Final development rule

Locate the layer. Fix that layer. Test that layer. Check only the interfaces it touches. Save the receipt. Move forward.

Do not rebuild the whole Breadboard because one experiment exposes one missing or broken capability.
