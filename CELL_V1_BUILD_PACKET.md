# CELL_V1 Build Packet

**Purpose:** bench-to-lattice build packet for the current CELL_V1 hardware target.

**Authority:** geometry is governed by `UPDATED_60_CELL_V1_HEX_EDGE_FLOWER_VOLUMETRIC_MEMORY_ARCHITECTURE.md` and the red-line summary in `CELL_V1_ANTI_DRIFT.md`.

**Status:** experimental build plan. Individual ancestor mechanisms exist in hardware, but the combined CELL_V1 has not yet been demonstrated.

## 1. What this build is trying to prove

CELL_V1 is not successful merely because six LEDs blink or a motor turns.

The physical prototype must establish this chain:

```text
local electrical event
 -> magnetic state transition
 -> retained remanent state after drive removal
 -> retained state changes the next electrical response
 -> returned/recovered energy can be measured
 -> state can propagate through identical edge-connected cells
 -> paths can form a stable rotation
 -> rotations can couple into a larger field
```

The primary scaling target is:

```text
Point -> Path -> Rotation -> Field -> Volume -> next-scale Point
```

## 2. Geometry — do not improvise

All six connection ports are centered on the **flat sides/edges** of the hex.

```text
CLOCKWISE:
A+ -> B+ -> C+ -> A- -> B- -> C-

OPPOSITES:
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

No port is located at a corner/vertex.

Every cell in the seven-cell flower is the same orientation. Shared flat edges connect matching letters with opposite polarity.

## 3. Target physical package

The scaling target is a compact two-part cell.

### Electronic/top half

- six edge-center interfaces;
- bidirectional switching/routing;
- integrated or co-located MOSFETs;
- gate-drive protection;
- current/voltage sensing;
- electrical center/reference distribution;
- local test points during development.

### Magnetic/bottom half

- one or more hysteretic magnetic paths associated with the A/B/C axes;
- write/drive winding(s);
- maintaining/reinjection winding(s);
- separate sense winding(s) for the instrumented prototype when useful;
- measurable remanence/hysteresis;
- thermal/mechanical support.

Do not force the first breadboard to look like the final chip. Prove the physics with accessible components first, then integrate.

## 4. Low-voltage bench frame

Current practical candidate:

```text
Supply: +5 V nominal, current limited
Electrical center: 2.5 V buffered/reference node
A/B/C signals: measured as differential quantities around the center
```

The `+` and `-` labels are opposed axis orientations, not raw instructions to connect +5 V directly to ground.

Do not reopen the retired +/-12 V design for CELL_V1.

## 5. Prototype parts categories

Exact part numbers remain open until the required voltage/current, magnetic material, switching speed, and winding energy are measured.

Use categories first:

- current-limited 5 V bench supply or protected USB-derived supply;
- buffered 2.5 V reference / rail-splitter suitable for the measured load;
- low-voltage MOSFETs appropriate to the selected current range;
- proper gate resistors/pull-downs and, when a half-bridge is used, shoot-through/dead-time protection;
- ferrite or another magnetic material with **measurable remanence/hysteresis**;
- magnet wire for drive/write, memory/reinjection, and sense windings;
- Schottky or otherwise appropriate low-loss steering devices for the recovery path;
- low-ESR capacitor for a measured reinjection reservoir;
- current-sense resistor or current probe;
- oscilloscope probes at the electrical and sense-winding test points;
- Hall/field probe if available;
- temperature measurement at the MOSFETs and magnetic element;
- fusing/current limiting appropriate to the bench source.

An ordinary switching-supply ferrite may be useful for induction tests but may retain too little remanence to function as useful memory. Measure it rather than assuming it stores state.

## 6. Rev A — one-axis magnetic-memory proof

Build only the A axis first.

```text
A+ EDGE / DRIVE ---- switch ---- write winding ----+
                                                    |
                                               HYSTERETIC
                                               MAGNETIC PATH
                                                    |
A- EDGE / DRIVE ---- switch ---- opposed winding --+

                    sense winding -> oscilloscope
                    memory/reinject winding -> recovery test
```

The drawing is functional, not a final winding polarity prescription. Winding dot orientation must be documented during the build.

### Test A1 — baseline

Record:

- supply voltage;
- center-reference voltage;
- A+ and A- quiescent voltages/currents;
- sense-winding baseline;
- core temperature.

### Test A2 — positive write

Apply one controlled A+ write pulse. Record magnitude, duration, current, sense waveform, and energy estimate.

### Test A3 — retention

Remove the write drive completely. After defined delays, perform the weakest read that can distinguish state without rewriting it.

Pass condition: a reproducible state-dependent response persists after the drive is removed.

### Test A4 — old state changes new response

Starting from the retained A+ state, apply a standardized probe/new pulse and record its threshold, delay, current, sense waveform, or another agreed observable.

Reset/rewrite to the opposite state and repeat the identical probe.

Pass condition: the later response depends reproducibly on the earlier retained state.

### Test A5 — opposite write

Apply an A- write pulse and verify that the magnetic/electrical readback changes in the expected opposite or distinguishable direction.

### Test A6 — repeatability

Repeat the A+/A- write/read cycle enough times to quantify:

- state margin;
- variation;
- drift;
- heating;
- write energy;
- retention time over the tested interval.

Do not call one anomalous pulse memory.

## 7. Rev B — reinjection proof on the same axis

Add a controlled recovery path:

```text
inductive / magnetic return
        -> steering element
        -> C_REINJECT
        -> measured controlled release
        -> later permitted winding event
```

Measure independently:

```text
E_in
E_stored estimate
E_returned to reservoir
E_delivered from reservoir into later event
losses
```

Pass condition: recovered energy is measurable and is deliberately reused in a later permitted event.

Fail condition: the claimed benefit depends on unexplained net energy gain or on hiding source current in the reference network.

## 8. Rev C — three opposed axes in one CELL_V1

Only after one axis has passed memory and recovery tests, reproduce it for B and C.

The cell then exposes:

```text
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

All six connections remain on flat edge centers.

For each axis record the same memory and reinjection receipt so a good A axis cannot hide a failing B or C axis.

Required test points:

```text
TP_REF       electrical center
TP_A+ / A-   A-axis electrical state
TP_B+ / B-   B-axis electrical state
TP_C+ / C-   C-axis electrical state
TP_MA/MB/MC  magnetic/sense observables
TP_R         reinjection reservoir
```

## 9. Rev D — path propagation

Connect two identical CELL_V1 modules flat-edge to flat-edge using the canonical matching rule.

Prove that a state/transition in cell 1 changes cell 2 through the intended connection while recording:

- amplitude loss;
- phase/delay;
- noise;
- reference disturbance;
- unwanted coupling to the other four edges;
- retained-state disturbance.

Then extend to three cells.

A scalable path must survive multiple transfers without requiring a different special-purpose cell at each position.

## 10. Rev E — closed rotation

Arrange a small closed path using identical edge interfaces.

The required evidence is not just oscillation. Distinguish among:

- simultaneous switching;
- damped ringing;
- standing oscillation;
- traveling/circulating state/phase;
- controlled reversal of the circulation.

A claimed field rotation needs phase-resolved measurements around the loop.

## 11. Rev F — seven-cell flower

Build one center CELL_V1 with six identical surrounding cells.

Rules:

- same orientation for all seven;
- flat-edge connections only;
- no adapter cells;
- individual cell testability retained;
- center/reference behavior logged per cell.

Test in increasing complexity:

1. one outer cell -> center;
2. center -> one outer cell;
3. two-edge path through center;
4. perimeter path among surrounding cells where geometry permits;
5. closed/circulating patterns;
6. competing or intersecting paths;
7. retained-state effect on a later whole-flower pattern.

## 12. Rev G — 3D / volumetric test

Do not jump directly to a full brain stack.

Start with the smallest vertical/depth coupling that distinguishes:

- useful coupling;
- reinforcement;
- opposition/cancellation;
- uncontrolled crosstalk.

A current candidate scale is `3 x 3 x 3`, but the exact lower-scale unit remains open. Prove the interface at the smaller scale first.

A mirror-flipped companion volume is a later candidate for whole-volume memory/checking/reinjection.

## 13. Brain and M4 integration remain downstream

Do not hard-code the following into the first CELL_V1 PCB:

- `2 normal + 2 inverted` as mandatory M4 depth;
- `3 normal + 3 inverted` as mandatory brain depth;
- `3+ / 3- / 3+` as mandatory hemisphere depth;
- one dedicated nerve layer;
- one fixed vertical polarity-flip interval.

Those are architecture candidates. They become hardware requirements only when measurements show the function that each extra layer performs.

## 14. Mandatory safety / failure controls

- current-limit every early prototype;
- prevent MOSFET shoot-through;
- provide an intentional inductive-energy path before switching coils;
- instrument the virtual/electrical center so reference collapse cannot masquerade as a state transition;
- stop on unexpected MOSFET or winding heating;
- do not hot-plug unknown coil configurations into an unprotected bridge;
- record winding polarity/dot convention before changing connections;
- do not connect an oscilloscope ground clip in a way that shorts a floating node or center reference;
- use isolated/differential measurement where the circuit requires it.

## 15. Required receipt for every serious test

```text
test_id
date / build revision
cell_id / axis / edge
schematic revision
core material / geometry
winding turns and polarity
supply and current limit
center-reference voltage
MOSFET / switch configuration
command pulse
measured voltage/current waveform
sense-winding / field waveform
retained-state readback
neighbor response when connected
reinjection reservoir waveform
energy accounting
temperature
PASS / FAIL
unexpected behavior
next single change
```

Change one thing, test immediately, compare with the active goal, and do not stack multiple unexplained changes into the same trial.

## 16. First decisive build

The immediate physical build is **not** the 27-unit volume.

It is:

```text
ONE A+ <-> A- AXIS
+
HYSTERETIC MEMORY
+
INSTRUMENTED REINJECTION
+
LOW-VOLTAGE DIFFERENTIAL REFERENCE
```

Once that behaves reproducibly, copy it into B and C without changing the primitive. That is the shortest path to a real CELL_V1 rather than another diagram.
