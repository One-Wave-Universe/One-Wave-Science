---
node_id: "C-325"
canonical_name: "One-Wave V0-A Intrinsic Cell — Engineering Architecture and Simulation"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "PROPOSED_BUILD"
classification: "Engineering / Applied Hardware Node"
claim_gate_detail: "YELLOW (architecture, SPICE skeleton, and behavioral simulation) / superconducting operation, MTJ memory, full six-node field rotation, and physical-hardware energy savings are explicitly not proven"
metadata_standard: "I-06"
---

# Node C-325: One-Wave V0-A Intrinsic Cell — Engineering Architecture and Simulation

BOUNDARY STATEMENT (read first): this node is a proposed analog
engineering architecture for a single "intrinsic" One-Wave cell — one
that senses, resolves, times, remembers, modulates, reinjects, routes,
and loops without a conventional processor in the operating loop.
Package version `0.2-intrinsic-cell`. It makes no claim that the
architecture is proven in physical hardware; a behavioral (control-level)
simulation has been run and is recorded below, not a transistor-level or
magnetic SPICE proof.

**Core rule:** the cell is the processor. No Pico, Arduino, Jetson,
FPGA, software timer, external clock, or conventional CPU belongs in
the operating loop. External devices may measure or log only.

**Dependencies**
Upstream: A-101 Ground/Zero, B-201 Equilibrium Balance, B-205 Mirror, C-301 Mirror Gate, C-323 Primitive Continuous Mirrored Chain, C-324 One-Wave V0 Hex Cell
Lateral: C-312 Hierarchical Sensor-Control Architecture, C-315 Wave Reader V1, G-716 One-Wave Conversion Grammar
Downstream: C-326 One-Wave V0 Intrinsic Cell First-Organelle Build Wiring (supersedes this node's schematic/wiring section with a refined buildable version), Books/Engineer_The_Future/Vol1/Ch06

## Intrinsic Cell — Organs

1. **Dual-reference body** — VA, VREL, VB.
2. **Mirror Gate** — compare, zero/hold detection, ternary resolution, crossing event.
3. **Local Point oscillator** — autonomous phase and timing.
4. **Phase organ** — pass, hold, or flip handedness.
5. **Magnetic memory** — retain ternary orientation and preferred path.
6. **Five-state modulator** — Floor, Low, Middle, High, Ceiling.
7. **Mitochondria reinjection organ** — detect loss and restore energy at the reinforcing phase without rewriting memory.
8. **Neighbor coupler** — receive, isolate/resist, align, exchange, and locally reverse route handedness.

## Operating Loop

```text
dual-reference relation
-> Mirror Gate
-> ternary resolution
-> local phase event
-> state retention
-> five-state modulation
-> intrinsic reinjection
-> neighbor exchange
-> recursive return
```

## Scaling Path

```text
one organelle
-> two coupled organelles
-> three-cell rotational path
-> six-cell ring
-> six organelles + center coordinator
-> coupled host cells
```

The center coordinator is another One-Wave cell specialized for shared
reference, phase coordination, oversight, and field-level reinjection.
It is not a conventional CPU. See C-324 for the six-organelle host
layout this scaling path targets.

## Schematic and Wiring Plan

```text
VA --+
     +-- MIRROR GATE -- LOCAL OSCILLATOR -- PASS/HOLD/FLIP
VB --+                                          |
                                                 v
                                   MAGNETIC TERNARY MEMORY
                                                 |
                                                 v
                                     FIVE-STATE MODULATOR
                                                 |
                                                 v
                                  INTRINSIC REINJECTION ORGAN
                                                 |
                                                 v
                                       NEIGHBOR COUPLER
```

Implementation roles: balanced reference network; window comparator
and hysteresis; LC or active resonant loop; analog phase gating or
transistor inversion; electrical latch for first proof, later magnetic
memory; five-position analog modulation network; envelope detector;
phase-gated reinjection pulse stage; bidirectional coupling path. No
software decides when to refresh, hold, or flip.

C-326 carries the refined, breadboard-buildable version of this
section (Sections A-F, block schematic, and BOM) for the first single
organelle.

## Build Sequence

1. Dual references and relational center.
2. Mirror Gate with stable `-1 / 0 / +1`.
3. Autonomous local oscillator.
4. Local phase-crossing detector.
5. Intrinsic pass / hold / flip path.
6. Electrical state latch.
7. Five-state modulation.
8. Envelope-loss detector.
9. Phase-synchronous reinjection.
10. Magnetic memory with separate maintain and rewrite paths.
11. Two-cell exchange.
12. Three-cell rotational path.
13. Six-cell hex ring.
14. Center coordinator plus six organelles.

## Test Plan

**Architectural pass/fail:** the cell fails if it requires an external
processor or clock to keep operating. External instruments may observe
only.

**Required proofs:**
- stable dual references;
- reliable ternary resolution;
- autonomous oscillation;
- intrinsic phase crossing;
- pass / hold / flip generated locally;
- five distinct modulation levels;
- intrinsic reinjection maintains amplitude;
- maintenance does not rewrite memory;
- deliberate rewrite changes memory;
- neighbor transfer preserves polarity, phase, and modulation;
- local handedness can flip without forcing global reversal.

None of these proofs has a physical-hardware pass result yet. See
`Simulation Results` below for the behavioral (non-hardware) status.

## Intrinsic Ternary Language Mapping

The language names physical transitions; it does not control passive
hardware from a CPU.

```text
choice      = -1 | 0 | +1
level       = Floor | Low | Middle | High | Ceiling
handedness  = CCW | HOLD | CW
memory      = MAINTAIN | WRITE
route       = RECEIVE | ISOLATE | EXCHANGE
```

Primitive operations:

```text
SET_VREL, READ_MIRROR, HOLD, CHOOSE_NEG, CHOOSE_POS, SHIFT_LEVEL,
PASS_PHASE, FLIP_PHASE, ROTATE_POINT, ROTATE_PATH, ROTATE_FIELD,
LATCH_STATE, MAINTAIN_STATE, WRITE_STATE, REFRESH_RC, EXCHANGE,
ISOLATE, LOOP
```

Every instruction must correspond to a measurable transition inside
the cell.

## Component Roles

Intrinsic roles: comparator (relational sensing); hysteresis network
(stable center); resonator (local timing and Point rotation);
transistor/analog switch network (pass, hold, flip); latch or magnetic
element (memory); resistor/current ladder (five-state modulation);
envelope detector (loss sensing); phase-gated driver (reinjection);
bilateral coupling network (neighbor exchange).

Excluded from the operating loop: Pico, Arduino, Jetson, FPGA,
software refresh loop, external clock as permanent timing source.
Oscilloscopes, meters, computers, and function generators are
development tools only.

## Bill of Materials

See `C-325_V0A_Intrinsic_Cell_Engineering_Architecture/bom/V0A_BOM.csv`
for the full parts list (virtual ground, comparator, op amp, analog
switch, MOSFETs, LC resonator parts, oscillator, latch, envelope
detector, phase gate, pulse stage, and optional magnetic memory
components).

## SPICE Skeleton

`C-325_V0A_Intrinsic_Cell_Engineering_Architecture/spice/v0a_intrinsic_cell.cir`
is a behavioral analog skeleton (damped LC tank, tanh-gain drive,
diode envelope detector, threshold-switched reinjection) — a
starting point for a real transistor-level SPICE model, not a
component-accurate proof.

## Simulation Results

`C-325_V0A_Intrinsic_Cell_Engineering_Architecture/simulation/` holds a
behavioral (control-level) comparison, explicitly **not** a
transistor-level or magnetic SPICE proof, of four drive modes at
`F0 = 10 kHz`, `Q = 22`:

| Mode | Final amplitude | Mean amplitude (after 4 ms) | Normalized input energy vs. continuous |
|---|---|---|---|
| decay (no drive) | ~9.4e-7 | 0.00756 | 0.322 |
| continuous drive | 4.179 | 4.185 | 1.000 |
| phase-timed refresh | 0.838 | 0.878 | 0.344 |
| repeated restart | 3.834 | 8.534 | 4.145 |

This behavioral result shows phase-timed refresh can hold a lower but
sustained amplitude at roughly a third of the normalized input energy
of continuous drive, and that repeated restart is markedly less
energy-efficient than either. It validates the declared control-level
model only — it does not validate physical hardware energy savings,
magnetic memory, or any claim beyond this reduced model. See
`manifest.json` for the exact `not_proven` list.

## Sources and Part-Note Inconsistency

`docs/06_SOURCES_AND_PART_NOTES.md` in the imported package still lists
the Raspberry Pi Pico as supplying "capture, phase logic, five-level
control, and pulse timing" under its selection-logic notes, while the
package `README.md` and `manifest.json` state the Pico was removed
from the operating loop for this intrinsic revision (`manifest.json`
`removed` list). This is preserved as an internal inconsistency in the
imported source material, not resolved here — the **core rule** (no
processor in the operating loop) is binding; the stale Pico
selection-logic note is not.

## Failure / Revision Conditions

This node fails if any physical hardware built from it is described
as validated by the behavioral simulation above, if the Pico
selection-logic note is treated as current architecture, or if any of
the eleven required proofs in the Test Plan is marked passed without a
recorded, reproducible measurement.
