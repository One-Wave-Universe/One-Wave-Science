# CELL_V1 — Action Down / Spintronic / Ternary Motor / Reinjection Map

**Status:** working architecture map; experimental until bench-validated

**Purpose:** preserve the current cell-to-motor architecture so it does not have to be reinvented from chat history. This file separates analog processing, Action-Down state, ternary motor control, motor power, shared energy circulation, stress escalation, and reinjection while keeping them in one recursive loop.

---

## 0. Do not drift these rules

1. **Brain Cell V1 stays analog and low-current.**
2. **Processing = retained path change = muscle memory = state reinjected into the next pass.**
3. **Quadratic remains Views Up / Actions Down.**
4. **Spintronics is the current candidate for the Action-Down state/command layer.** It is not assumed to source motor winding current directly.
5. **Ternary motor control is the three-winding A/B/C control structure.**
6. **The motor power layer uses bidirectional switching sized for the actual winding current.**
7. **Recoverable electrical/magnetic energy is routed back into the reinjection path wherever practical instead of being deliberately burned off.**
8. **The design target is a shared energy loop:** local units may take energy from and return energy to a common bus through controlled bidirectional gates.
9. **The quiet reference and the high-current energy bus are conceptually related but electrically distinct.** Do not force motor return current through the precision 2.5 V reference node.
10. **Local stress is a signal, not merely a failure.** Rising current, temperature, load, bus pressure, storage limits, or repeated correction may trigger a View-Up request for higher authority to reduce or redistribute demand.
11. **Hard protection remains local and immediate.** Higher authority is for coordination; it must not be required before a dangerous overcurrent/overvoltage/overtemperature cutoff acts.
12. The design target is to minimize wasted power. Real hardware will still have measurable resistive, switching, magnetic-core, bearing, acoustic, and other losses. Do not label those losses as recovered unless measured.
13. One independent motor keeps its own local three-winding power stage and current feedback.
14. A motor cluster may coordinate multiple local motor units while each motor retains its own local power/reinjection loop.
15. Matching counts do not collapse layers: four quadratic channels are not the same thing as three motor windings.
16. This document records the architecture hypothesis and test sequence; it does not claim the complete chain has already been proven.

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
        +---------------------> sensor + stress feedback
        |
        +---------------------> recoverable inductive / regenerative energy
                                  |
                                  v
                           SHARED ENERGY / REINJECTION BUS
                                  |
                                  +----> another local demand
                                  +----> local/shared storage
                                  +----> next drive event
                                  +----> next processing cycle
```

Central rules:

```text
STATE / COMMAND != POWER DELIVERY
POWER DELIVERY != POWER DISPOSAL
REFERENCE BUS != HIGH-CURRENT ENERGY BUS
LOCAL STRESS != FAILURE; IT CAN BE A VIEW-UP SIGNAL
```

The command layer chooses and holds the action state. The switching layer moves power. Recoverable energy returns through a controlled reinjection path. Local units may exchange energy through a shared bus while higher layers coordinate demand when the system approaches limits.

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
      +----> shared DC energy bus
      |
      +----> local/shared storage capacitor
      |
      +----> battery / permitted storage path
      |
      +----> another subsystem that currently needs energy
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

## 7. Shared energy loop

The common-line idea is implemented as a **shared energy bus**, not by using the precision reference conductor as the motor-current return.

```text
                    SHARED ENERGY BUS
        +-----------------+-----------------+
        |                 |                 |
        v                 v                 v
   LOCAL UNIT 1      LOCAL UNIT 2      LOCAL UNIT 3
 bidirectional gate bidirectional gate bidirectional gate
        |                 |                 |
        v                 v                 v
      motor             motor             storage
        |                 |                 |
        +------ returned recoverable energy-+
```

A local unit may:

```text
TAKE energy when commanded action requires it
RETURN energy when winding/back-EMF/regeneration makes energy available
HOLD/RECIRCULATE energy locally when that is the lowest-loss path
```

The design target is **proportional gated exchange**, not uncontrolled circulating current.

### Voltage-control authority

To stop branches from fighting each other:

```text
ONE BUS-VOLTAGE AUTHORITY
        +
LOCAL CURRENT / POWER CONTROL
```

An op-amp/comparator/control loop may sense bus voltage and generate control error, while the bidirectional MOSFET/converter stage carries the actual power current.

### Reference vs energy bus

```text
QUIET REFERENCE
= shared measurement / comparison center
= low-current precision node

SHARED ENERGY BUS
= high-current take / return / reinjection path
= energy distribution node
```

They can use the same system-wide definition of zero/balance, but they are not the same conductor unless a measured design later proves a safe combined implementation.

---

## 8. Local motor unit vs motor cluster

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
current / position / back-EMF / temperature sensing
    |
local reinjection path <-> shared energy bus
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
  take/return     take/return    take/return
       \             |             /
        +------ SHARED ENERGY BUS--+
```

The cluster determines coordinated action; it does not force all motors to share one power inverter unless the physical design specifically requires electrically locked motors.

---

## 9. Stress / exhaustion as View-Up escalation

Biological analogy: muscle burn, fatigue, strain, or exhaustion can be treated as a model for **local stress becoming information for a higher controller**. The machine implementation should use measurable variables, not subjective labels.

Candidate local stress inputs:

```text
current rising toward limit
temperature rising
motor torque/load rising
repeated corrective effort
bus voltage approaching limit
storage nearly full or nearly empty
reinjection capacity saturated
position/balance error persisting
local energy demand remaining high
```

Working control rule:

```text
NORMAL RANGE
-> local loop handles it

ELEVATED / PERSISTENT STRESS
-> View Up: request coordination / reduced demand

HARD SAFETY LIMIT
-> immediate local protection
```

Higher authority may respond with an Action Down such as:

```text
reduce torque/current target
slow command rate
redistribute load to another motor/limb/unit
change routing or gait
pause lower-priority action
increase available storage/load for regenerative energy
reduce regenerative command if the shared bus cannot accept more energy
```

This creates a machine analogue of exhaustion without waiting for damage:

```text
"I can still operate, but continuing at this rate is pushing my local state toward its limit."
```

The exact stress function, thresholds, weighting, hysteresis, and escalation timing remain experimental.

---

## 10. Feedback returns through the same recursive architecture

Motor execution is not the end of the loop.

```text
ACTION DOWN
    |
    v
MOTOR ACTION
    |
    +----> current / phase / back-EMF
    +----> position / balance / load sensors
    +----> temperature / energy / bus stress
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
state -> action -> sensor/stress result -> next state

ENERGY LOOP:
supply/shared bus -> winding -> mechanical/magnetic storage -> recoverable return -> shared bus -> next demand
```

Do not collapse those into one literal electrical conductor without a measured circuit showing that it works.

---

## 11. Growth / modular development target

The long-range machine target is **simple repeatable cells and local rules producing larger organized structures**, rather than hand-designing every final global behavior into one controller.

Conceptual progression:

```text
ONE CELL
reference + state + input/output + local energy + stress sensing
        |
        v
NEIGHBOR CONNECTION
        |
        v
LOCAL CLUSTER
        |
        v
SPECIALIZED CLUSTER
brain / pathway / M4 / motor / sensory roles
        |
        v
LARGER BODY / MACHINE
```

Useful biology-inspired principles to copy in simpler engineering form:

```text
biology                     machine design target
----------------------------------------------------------------
nerve signal              -> electrical/field signal
muscle strain             -> current/load/temperature sensing
pain/exhaustion           -> stress threshold + View Up
blood circulation         -> shared energy distribution/reinjection bus
metabolism                -> storage + conversion + power allocation
reflex                    -> fast local loop
brain oversight           -> higher coordination loop
muscle memory             -> retained analog/stateful processing path
homeostasis               -> closed-loop regulation around references
```

This is an architectural analogy, not a claim that the hardware already reproduces biology.

The machine may eventually be able to expand by adding repeated compatible cells/modules. Self-assembly, autonomous growth from raw materials, self-repair, and developmental specialization are **future research targets**, not current demonstrated capabilities.

---

## 12. Smallest validation sequence

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

### Experiment D — Reinjection / shared bus

Measure:

```text
energy delivered to winding
energy returned by recirculation / regeneration
energy transferred to another load or storage
bus-voltage stability
mechanical output where measurable
losses
```

PASS requires a repeatable, measurable return of recoverable energy to the local/shared bus, storage, another demand, or the next drive event without destabilizing the bus.

### Experiment E — Stress escalation

Prove:

```text
local stress variable rises
-> local controller remains stable
-> threshold is crossed
-> View Up is emitted
-> higher authority reduces/redistributes demand
-> local stress falls
```

Hard protection must still operate independently if a safety limit is crossed.

### Experiment F — Close the loop

```text
brain state
-> View Up
-> M4
-> Action Down
-> spintronic command
-> ternary motor
-> sensor/stress result
-> View Up

AND

motor/winding recoverable energy
-> shared reinjection bus
-> another demand / storage / next drive cycle
```

Only after the individual bridges pass should the full recursive loop be claimed as demonstrated.

---

## 13. Current architecture summary

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
= actual motor-current switching and bidirectional gate layer

SHARED ENERGY BUS
= common controlled take/return path for recoverable power

REINJECTION
= controlled recovery/recirculation of recoverable electrical/magnetic energy into another load, storage, supply bus, or next drive event

STRESS / EXHAUSTION SIGNAL
= measurable local condition that can escalate through View Up before failure

MOTOR CLUSTER
= coordinates multiple independently controlled local motor units connected to the wider energy and information architecture

GROWTH TARGET
= repeat simple compatible cells/modules and allow larger organization to emerge through local connection rules and higher-level coordination
```

---

## 14. Things still deliberately open

- exact spintronic device family for Action Down;
- whether the best first device is MTJ/STT-MRAM, SOT-MRAM, domain-wall, Hall/spin-Hall structure, or another accessible spintronic component;
- exact interface between spintronic readout and MOSFET gate driver;
- exact A/B/C bidirectional inverter topology;
- motor winding geometry and voltage/current target;
- shared-bus nominal voltage and allowable voltage excursion;
- local/shared energy-storage element;
- bus-voltage authority/control law;
- local proportional take/return current-control law;
- protection path for energy that cannot be accepted by storage or another active load;
- measured recovery efficiency;
- exact stress variables and threshold combination;
- stress hysteresis/dwell and escalation timing;
- exact mapping of four quadratic Action-Down channels into one or more ternary motor units;
- which cell properties must be identical for scalable repeated construction and which may specialize by position/state.

Do not fill these by analogy. Select them from the next physical experiment and measurements.

---

## 15. Immediate next hardware order

```text
1. Finish Brain Cell V1 one-axis A+ / A- proof.
2. Select one accessible spintronic Action-Down device.
3. Build Action-Down V1 with a dummy MOSFET load.
4. Design one three-winding motor power stage with bidirectional current paths.
5. Add a shared DC energy bus with measured recirculation/regeneration.
6. Add bus-voltage control plus local current take/return control.
7. Add one measurable local stress signal and View-Up escalation test.
8. Combine Action Down + ternary motor + reinjection + stress feedback.
9. Scale to a motor cluster only after one local motor unit passes.
10. Only then test repeated compatible cell/module growth and specialization rules.
```

This order preserves the architecture without pretending untested bridges are already solved.