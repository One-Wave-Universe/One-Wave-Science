# CELL_V1 Referenced Parts and Visual Guide

**Status:** current referenced visual/build companion to `One_Wave_Bench/speculative/CELL_V1_BUILD_PACKET.md` and `UPDATED_63_CELL_V1_STATEFUL_MUSCLE_MEMORY_BUILD.md`.

## Hard geometry lock

```text
PORTS: FLAT SIDES ONLY
CORNERS / VERTICES: NO PORTS

CLOCKWISE FROM TOP SIDE:
A+ -> B+ -> C+ -> A- -> B- -> C-

DIRECT MIRRORS:
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

The PDF companion is `CELL_V1_referenced_parts_breadboard_visual.pdf` in this folder. Any future visual that puts a port at a vertex is wrong and should be discarded.

## No-assumption rule

A part, value, mechanism, or scaling count enters the build only when it has at least one of:

1. a manufacturer datasheet / application note;
2. a peer-reviewed hardware result;
3. a measured CELL_V1 receipt.

If none exists, mark it **OPEN** rather than filling the gap by symmetry or intuition.

## Physical repeated-path / muscle-memory mechanism

The build uses **physical path adaptation** as the hardware muscle-memory analogue. Repeated successful traversal must alter the same stateful path that performs processing, so the next traversal is measurably different.

A software use counter is not sufficient.

Published precedents used here:

- Boybat et al., *Neuromorphic computing with multi-memristive synapses*, Nature Communications 9, 2514 (2018): physical phase-change-memory synapses show mean conductance evolution with potentiation pulse count across thousands of devices. https://www.nature.com/articles/s41467-018-04933-y
- *High-performance van der Waals antiferroelectric CuCrP2S6-based memristors*, Nature Communications (2023): consecutive pulses produce potentiation/depression and the paper explicitly reports a training effect on conductance. https://www.nature.com/articles/s41467-023-43628-x
- Knowm SDC memristors: resistance is tunable in both directions by applied polarity; tungsten-doped devices are described as analog-state-retaining devices. https://knowm.org/downloads/Knowm_Memristors.pdf

## Referenced parts for Rev A

### Stateful path

**Knowm M+SDC Memristor 8 Discrete 16 DIP**

- actual discrete SDC memristors in a 16-DIP package described by Knowm as ideal for breadboarding;
- W/Tungsten option described as analog state retention with modest/fast switching response;
- current Knowm web store status at time of this guide: **sold out**;
- do not substitute an unreferenced resistor network and call it equivalent memory.

Product: https://knowm.com/products/m-sdc-memristor-8-discrete-16-dip
Datasheet: https://knowm.org/downloads/Knowm_Memristors.pdf

The initial 50 kOhm series-protection value in the PDF is explicitly a **test-jig starting value** taken from Knowm endurance-characterization conditions, not an asserted final CELL_V1 optimum.

### V0 reference

**Texas Instruments TLE2426ILP**

- active rail-splitter part;
- 4-40 V input range;
- at 5 V input, nominal output is 2.5 V;
- 20 mA typical source and sink capability;
- TO-92/LP pin functions used in the visual: pin 1 OUT, pin 2 COMMON, pin 3 IN.

https://www.ti.com/product/TLE2426

V0 is a reference only. It is not the recovery/reinjection reservoir.

### Bidirectional SiC nerve / power gate

**2 x Wolfspeed C3M0021120D** in a back-to-back common-source configuration.

- active 1200 V C3M SiC MOSFET;
- 21 mOhm RDS(on) family rating at 25 C;
- TO-247-3 package;
- package pinout: 1 Gate, 2 Drain, 3 Source;
- Wolfspeed documents +15 V gate-drive operation for this family.

https://www.wolfspeed.com/products/power/sic-mosfets/1200v-silicon-carbide-mosfets/c3m0021120d/

**Wolfspeed CGD15SG00D2** is the referenced isolated single-channel gate driver used in the visual; Wolfspeed specifies +15 V / -3.3 V output and C3M support.

https://www.wolfspeed.com/products/power/gate-driver-boards/cgd15sg00d2/

Texas Instruments documents common-source back-to-back N-MOSFETs as a bidirectional switch whose opposed body diodes block both directions when the MOSFETs are OFF:

https://www.ti.com/lit/an/sluaa58/sluaa58.pdf

## Breadboard boundary

The low-current memristive state/training lane is breadboardable.

The TO-247 SiC pair is **not** treated as a solderless-breadboard part. It belongs on a proper external power fixture / perfboard / PCB with the referenced gate driver and safe layout.

The Rev A build therefore has two explicit current domains:

```text
STATE / TRAINING LANE
low-current stateful path
processing = memory
repeated pulses physically train the path

POWER / ACTUATOR LANE
back-to-back SiC nerve gate
motor / inductive load
DC recovery -> separate C_REINJECT / DC link
```

This split is explicit. It does not mean memory is separate from processing; memory remains in the active state path. It means a research memristor is not falsely asked to carry motor current.

## Muscle-memory pass conditions

A path-training claim passes only if repeated testing shows a reproducible physical change, such as one or more of:

- retained conductance change;
- activation-threshold shift;
- reduced drive energy for the same response;
- reduced latency;
- stronger route preference under the same differential;
- fewer higher-level interventions;
- measurable potentiation with one pulse family and depression/reversal with the opposite family.

Training must survive a declared retention interval and repeat over train/de-train cycles. Uncontrolled permanent lock-in is not accepted as useful muscle memory.

## DC recovery / reinjection

The DC recovery path is separate from V0. Returned inductive/magnetic energy goes to a measured reservoir / DC link and must be reused in a later permitted event with energy accounting.

The PDF deliberately leaves the test coil, steering device, and C_REINJECT value **OPEN** until measured load current/voltage/energy sets those values and the selected parts are checked against their datasheets.

## Immediate build order

```text
1. prove V0 under actual state-lane load
2. prove one A+ <-> A- stateful path
3. measure repeated-path potentiation and depression
4. prove one external back-to-back SiC bidirectional nerve gate
5. add measured inductive load + DC recovery reservoir
6. combine receipts without hiding either current domain
7. only then copy the same primitive to B and C
8. only then test path -> rotation -> seven-cell flower -> depth -> volume
```

No corner-connected build is an acceptable CELL_V1 revision.
