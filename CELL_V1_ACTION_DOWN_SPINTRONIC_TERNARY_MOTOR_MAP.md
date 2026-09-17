# CELL_V1 — Action Down / Spintronic / Ternary Motor / Reinjection Map

**Status:** working architecture map; experimental until bench-validated

**Purpose:** preserve the current cell-to-motor architecture so it does not have to be reinvented from chat history. This file separates analog processing, Action-Down state, ternary motor control, motor power, and energy reinjection while keeping them in one recursive loop.

---

## 0. Do not drift these rules

1. **Brain Cell V1 stays analog and low-current.**
2. **Processing = retained path change = muscle memory = state reinjected into the next pass.**
3. **Quadratic remains Views Up / Actions Down.**
4. **Spintronics is the current candidate for the Action-Down state/command layer.** It is not assumed to source motor winding current directly.
5. **Ternary motor control is the three-winding A/B/C control structure.**
6. **The motor power layer uses bidirectional switching sized for the actual winding current.**
7. **Recoverable electrical/magnetic energy is routed back into the reinjection path wherever practical instead of being deliberately burned off.**
8. The design target is to minimize wasted power. Real hardware will still have measurable resistive, switching, magnetic-core, bearing, acoustic, and other losses. Do not label those losses as recovered unless measured.
9. One independent motor keeps its own local three-winding power stage and current feedback.
10. A motor cluster may coordinate multiple local motor units while each motor retains its own local power/reinjection loop.
11. Matching counts do not collapse layers: four quadratic channels are not the same thing as three motor windings.
12. This document records the architecture hypothesis and test sequence; it does not claim the complete chain has already been proven.

---

## 1. Whole recursive path

```text
ANALOG / MEMRISTIVE BRAIN CELL
processing + retained path state
        |
        v
      VIEW UP
analog condition communicated upward
        |
        v
        M4
quadratic coordination
Views Up / Actions Down
        |
        v
   ACTION DOWN
candidate: spintronic magnetic state / command
        |
        v
LOW-POWER ELECTRICAL READOUT / GATE COMMAND
        |
        v
BIDIRECTIONAL MOSFET / INVERTER POWER STAGE
        |
        v
TERNARY A / B / C WINDING CONTROL
        |
        v
MOTOR / ACTUATOR
        |
        +---------------------> mechanical result
        |
        +---------------------> sensor feedback
        |
        +---------------------> recoverable inductive / regenerative energy
                                  |
                                  v
                           REINJECTION LOOP
                                  |
                                  +----> local supply / storage / next drive event
                                  +----> next processing cycle
```

Central rule:

```text
STATE / COMMAND != POWER DELIVERY
POWER DELIVERY != POWER DISPOSAL
```

The command layer chooses and holds the action state. The switching layer moves power. Recoverable energy returns through a controlled reinjection path.

---

## 2. Brain Cell role

Current Brain Cell V1 remains:

```text
continuous analog input
        |
        v
stateful / memristive path
        |
        v
retained conductance changes
        |
        v
next traversal is altered
        |
        +---------------------> memory / processing / reinjection
```

The first brain-cell experiment does **not** require a motor or spintronic device. It proves the retained analog-processing primitive first.

Locked perimeter geometry remains:

```text
A+ -> B+ -> C+ -> A- -> B- -> C- -> A+
```

Across-cell mirrors:

```text
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

Connections are on the six sides/edges, never the corners.

---

## 3. Quadratic / M4 role

Logical role:

```text
VIEWS UP
   |
   v
M4 / QUADRATIC
   |
   v
ACTIONS DOWN
```

Current working physical geometry:

```text
NORMAL VOLUME
2 x 2 x 2 = 8 flowers
organized as 4 + 4

MIRRORED / INVERTED VOLUME
2 x 2 x 2 = 8 flowers
organized as 4 + 4

TOTAL WORKING M4 GEOMETRY = 8 + 8 = 16 flowers
```

Do not interpret the 16 physical flower units as 16 different quadratic functions. The logical quadratic function remains the four-view/four-action structure; the extra physical depth is a volumetric implementation hypothesis to test.

---

## 4. Action Down candidate: spintronics

Working hypothesis:

```text
M4 resolves an Action Down
        |
        v
spintronic element changes / holds magnetic state
        |
        v
that state is read electrically
        |
        v
readout biases / commands the appropriate power gate
```

Potential useful properties to investigate experimentally:

- persistent or semi-persistent magnetic state;
- low-energy state switching;
- differential / multistate response;
- magnetic state naturally coupling conceptually to the motor-control layer;
- electrical readout suitable for driving a separate power switch.

Do **not** assume a spintronic element can directly drive a motor winding. The first Action-Down experiment should be low-power:

```text
one Action-Down state
        -> one spintronic device
        -> one readable output
        -> one MOSFET gate command
        -> dummy load first
```

Only after that bridge is measured should it be attached to a motor-power stage.

---

## 5. Ternary motor control

For body/motor implementation:

```text
TERNARY = THREE-WINDING MOTOR CONTROL
```

Local motor structure:

```text
                ACTION COMMAND
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
          A           B           C
          |           |           |
          v           v           v
      WINDING A   WINDING B   WINDING C
          \           |           /
           \          |          /
              ROTATING FIELD
                   |
                   v
                 MOTOR
```

The three windings are the ternary physical control structure. Actual commutation may require multiple semiconductor switches per winding/phase. Do not confuse "three windings" with "three total transistors."

---

## 6. Reinjection is part of the motor power architecture

The motor stage should be designed so recoverable energy has an intentional return path.

Sources of recoverable energy include:

```text
winding inductive energy
motor back-EMF during deceleration
energy released when current is redirected between phases
regenerative mechanical energy when the load drives the motor
```

Desired path:

```text
WINDING / MOTOR
      |
      v
bidirectional switching / synchronous recirculation
      |
      +----> immediate local winding recirculation
      |
      +----> local DC bus / storage capacitor
      |
      +----> battery / permitted storage path
      |
      +----> next commanded A/B/C drive event
```

Avoid a default design where recoverable energy is simply dumped into a resistor or clamp unless that is required for protection during an experiment.

### Physical accounting rule

```text
ENERGY IN
  =
MECHANICAL OUTPUT
+ RECOVERED / REINJECTED ENERGY
+ MEASURED LOSSES
+ CHANGE IN STORED ENERGY
```

The goal is:

```text
maximize useful output
+
maximize recoverable reinjection
+
minimize measured losses
```

Do not claim zero-loss or 100% recovery from the architecture alone. Measure the actual recovered fraction.

---

## 7. Local motor unit vs motor cluster

### One local motor unit

```text
Action Down state
    |
spintronic command candidate
    |
local gate/control interface
    |
A/B/C bidirectional power stage
    |
three-winding motor
    |
current / position / back-EMF sensing
    |
local reinjection path
```

### Motor cluster

A motor cluster may coordinate multiple local motor units:

```text
                 MOTOR CLUSTER
              shared coordination
          /          |           \
         v           v            v
     MOTOR 1      MOTOR 2      MOTOR 3 ...
       |             |             |
     A/B/C         A/B/C         A/B/C
       |             |             |
  local recovery local recovery local recovery
```

The cluster determines coordinated action; it does not force all motors to share one power inverter unless the physical design specifically requires electrically locked motors.

---

## 8. Feedback returns through the same recursive architecture

Motor execution is not the end of the loop.

```text
ACTION DOWN
    |
    v
MOTOR ACTION
    |
    +----> current / phase / back-EMF
    +----> position / balance / load sensors
    +----> local retained processing state
    |
    v
VIEW UP
    |
    v
M4 / higher processing
```

Power and information are different quantities, but both participate in recursion:

```text
INFORMATION LOOP:
state -> action -> sensor result -> next state

ENERGY LOOP:
supply -> winding -> mechanical/magnetic storage -> recoverable return -> next drive
```

Do not collapse those into one literal electrical conductor without a measured circuit showing that it works.

---

## 9. Smallest validation sequence

Do not build the complete brain-to-motor chain at once.

### Experiment A — Brain Cell V1

Prove:

```text
repeated analog processing
-> retained physical path change
-> later identical input responds differently
```

### Experiment B — Action Down V1

Prove:

```text
low-power command
-> spintronic state change
-> persistent/readable output
-> MOSFET gate-level command
```

No motor required yet; use a safe dummy load.

### Experiment C — One ternary motor unit

Prove:

```text
three command channels
-> A/B/C power stage
-> controlled three-winding field
-> measured motor response
```

### Experiment D — Reinjection

Measure:

```text
energy delivered to winding
energy returned by recirculation / regeneration
energy remaining in storage
mechanical output where measurable
losses
```

PASS requires a repeatable, measurable return of recoverable energy to the local bus/storage/next drive event.

### Experiment E — Close the loop

```text
brain state
-> View Up
-> M4
-> Action Down
-> spintronic command
-> ternary motor
-> sensor result
-> View Up

AND

motor/winding recoverable energy
-> reinjection path
-> next drive cycle
```

Only after the individual bridges pass should the full recursive loop be claimed as demonstrated.

---

## 10. Current architecture summary

```text
MEMRISTIVE / ANALOG
= processing history / learned path / retained state

BINARY
= threshold: remain local vs communicate upward

QUADRATIC / M4
= Views Up / Actions Down

SPINTRONIC
= current candidate for low-power Action-Down magnetic state / command

TERNARY
= three-winding A/B/C motor-control structure

MOSFET / INVERTER
= actual motor-current switching layer

REINJECTION
= controlled recovery/recirculation of recoverable electrical/magnetic energy into local storage, supply bus, or the next drive event

MOTOR CLUSTER
= coordinates multiple independently powered/recovered local motor units
```

---

## 11. Things still deliberately open

- exact spintronic device family for Action Down;
- whether the best first device is MTJ/STT-MRAM, SOT-MRAM, domain-wall, Hall/spin-Hall structure, or another accessible spintronic component;
- exact interface between spintronic readout and MOSFET gate driver;
- exact A/B/C bidirectional inverter topology;
- motor winding geometry and voltage/current target;
- local energy-storage element and allowable bus-voltage rise during regeneration;
- protection path for energy that cannot be accepted by storage;
- measured recovery efficiency;
- exact mapping of four quadratic Action-Down channels into one or more ternary motor units.

Do not fill these by analogy. Select them from the next physical experiment and measurements.

---

## 12. Immediate next hardware order

```text
1. Finish Brain Cell V1 one-axis A+ / A- proof.
2. Select one accessible spintronic Action-Down device.
3. Build Action-Down V1 with a dummy MOSFET load.
4. Design one three-winding motor power stage with bidirectional current paths.
5. Add measured recirculation/regeneration into a local DC bus/storage element.
6. Only then combine Action Down + ternary motor + reinjection.
7. Scale to a motor cluster after one local motor unit passes.
```

This order preserves the architecture without pretending untested bridges are already solved.