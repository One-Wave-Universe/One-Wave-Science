---
node_id: "C-326"
canonical_name: "One-Wave V0 Intrinsic Cell — First Organelle Build Wiring"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "PROPOSED_BUILD"
classification: "Engineering / Applied Hardware Node"
claim_gate_detail: "YELLOW (breadboard-buildable schematic, wiring, and BOM defined) / no physical build has yet passed the C-325 test plan"
metadata_standard: "I-06"
---

# Node C-326: One-Wave V0 Intrinsic Cell — First Organelle Build Wiring

BOUNDARY STATEMENT (read first): this is a **buildable first
organelle** schematic, designed to prove seven specific claims listed
below. It is not yet the complete six-organelle-plus-coordinator host
cell described in C-324. Do not build seven copies until one organelle
passes the test plan in C-325.

**Dependencies**
Upstream: C-325 One-Wave V0-A Intrinsic Cell Engineering Architecture (this node supersedes C-325's Schematic and Wiring Plan section with a refined, breadboard-buildable version of the same architecture), C-301 Mirror Gate
Lateral: C-324 One-Wave V0 Hex Cell
Downstream: Books/Engineer_The_Future/Vol1/Ch06

## What This Schematic Is

Designed to prove:

1. dual-reference relational center;
2. stable ternary Mirror Gate;
3. autonomous local oscillation;
4. five-state envelope/state-strength target;
5. intrinsic phase-synchronous reinjection;
6. separate maintain and rewrite paths;
7. later magnetic retention and neighbor coupling.

## Non-Negotiable Architecture

No Pico, Arduino, Jetson, FPGA, or software timing in the operating
loop. Oscilloscope and computer are measurement tools only.

## Section A — Dual References

Current-limited 5 V supply:

```text
5 V -- 10 kOhm --+-- 10 kOhm -- 0 V
                 |
               VREL
```

Buffer VREL before loading it heavily. Create adjustable `VHIGH` and
`VLOW` around VREL with two 10 kOhm trim pots or a stable resistor
network.

```text
VREL  ~= 2.50 V
VHIGH ~= 2.70 V
VLOW  ~= 2.30 V
```

## Section B — Mirror Gate

One LM393B dual comparator as a window comparator:

```text
Comparator A: TANK_SENSE > VHIGH
Comparator B: TANK_SENSE < VLOW
```

Resolved state:

```text
HIGH asserted only -> +1
neither asserted    -> 0 / HOLD
LOW asserted only   -> -1
```

Add positive feedback resistors later for hysteresis after basic
operation works. LM393B outputs are open collector, so use pull-up
resistors.

## Section C — Autonomous Point Loop

```text
L = 10 mH
C = 22 nF
```

Near 10.7 kHz nominal. Use a CD40106B Schmitt inverter section as the
active sustaining element for the first proof. The oscillator must run
without a processor or external clock.

## Section D — Envelope / State Strength

Rectify the oscillator output with a diode and RC envelope detector.
Compare the envelope against one of five target references: Floor,
Low, Middle, High, Ceiling. For the first physical test, manually
select the target with a five-position switch or jumper ladder. Later,
the cell must select it intrinsically.

## Section E — Phase-Synchronous Reinjection

```text
INJECT = LOSS_REQUEST AND PHASE_MATCH
```

`LOSS_REQUEST` comes from the envelope detector (envelope below
target). `PHASE_MATCH` comes from the oscillator's own crossing
signal. Use a small MOSFET pulse stage through a current-limiting
resistor; begin with 220 Ohm. The pulse must reinforce the present
phase. Opposite polarity is a deliberate FLIP operation, not
maintenance.

## Section F — Magnetic Memory Experiment

Closed core with separate windings: sense, maintain, rewrite/flip,
neighbor-coupling. Start with ferrite. Compare mu-metal and
nanocrystalline cores in separate material experiments. Do not assume
one material wins every job.

## Block Schematic

`C-326_V0_Intrinsic_Cell_First_Organelle_Build_Wiring/One_Wave_V0_Block_Schematic.svg`
is the visual block diagram: VA/VB references into the Mirror Gate,
Point Loop oscillator, Phase Organ (Pass/Hold/Flip), Magnetic Memory,
5-State Modulation, Mitochondria/Reinjection organ, and Neighbor port.

## Bill of Materials

See
`C-326_V0_Intrinsic_Cell_First_Organelle_Build_Wiring/BOM.csv` — LM393B
window comparator, CD40106B oscillator/phase shaping, MCP6004
buffering, CD4053B optional analog routing, 2N7000 reinjection
switches, LC resonator parts, ferrite/mu-metal/nanocrystalline cores
for magnetic memory experiments, trim pots, decoupling, envelope
diodes, a five-position target switch, breadboards, a current-limited
5 V supply, and an oscilloscope.

## Failure / Revision Conditions

This node fails if a six-organelle build (C-324) is attempted before
this single organelle passes the seven-item proof list above, or if
any of those seven items is marked passed without a recorded,
reproducible measurement.
