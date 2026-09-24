# UPDATED 63 - CELL_V1 Board #1 Drive, Reference, and Nerve-Transfer Lock

**Status:** current Board #1 execution lock for physical validation.

This update does not alter the CELL_V1 geometry. It locks the first instrumented board used to prove the internal magnetic/electrical mechanism before scaling.

## Geometry remains primary

```text
CELL_V1 = one repeatable six-flat-edge hex
CLOCKWISE = A+ -> B+ -> C+ -> A- -> B- -> C-
FLOWER = seven identical same-orientation cells
SCALE = Point -> Path -> Rotation -> Field -> Volume -> next-scale Point
```

The A/B/C magnetic fixture is **inside one hex**. It does not replace the hex.

## Board #1 sequence

```text
1. +5 V protected DC link
2. quiet measured ~2.5 V electrical reference
3. reversible differential Drive stage for A/B/C
4. Sense + Memory pairs broken out and initially floating
5. characterize open Sense waveform
6. independently measure Memory write/retention threshold
7. test one A Sense -> B Memory transfer
8. only after that passes, test B -> C and C -> A
9. close the complete three-element nerve ring
10. only then add controlled reinjection into a DC-link/local reservoir
```

## H-bridge correction

A single ordinary half-bridge has one switching node. A true floating `Drive + / Drive -` winding therefore needs a full reversible differential stage such as an H-bridge, or an explicitly defined center-tapped/alternative winding topology.

Do not label two independent winding ends as two outputs from one ordinary half-bridge.

## Reference correction

The ~2.5 V VREF is a quiet electrical reference. With a true floating H-bridge, it is not the high-current Drive return.

Do not collapse these into one node:

```text
VREF
magnetic material
geometric center
earth/scope ground
DC-link energy reservoir
```

They are different physical/electrical roles.

## 18-terminal bench fixture

Current experimental three-element fixture:

```text
A: Drive +/- | Memory +/- | Sense +/-
B: Drive +/- | Memory +/- | Sense +/-
C: Drive +/- | Memory +/- | Sense +/-
```

This is 18 magnetic-fixture terminals total.

It is **not** the CELL_V1 external port count. The external cell remains six edge ports.

## Direct nerve-ring wiring remains candidate

Candidate links:

```text
A Sense +/- -> B Memory +/-
B Sense +/- -> C Memory +/-
C Sense +/- -> A Memory +/-
```

Do not lock these as direct copper until one transfer is measured. A Sense winding may have voltage but insufficient magnetizing current, or may be badly loaded by the receiving Memory winding.

Allowed outcome of the first experiment:

```text
DIRECT works -> keep it
DIRECT loads/collapses -> measure impedance/current need
then test passive match, transformer/resonant match, analog current buffer, or measured magnetic coupling
```

The coupling implementation can change. The required function is continuous measurable A->B state transfer.

## First hard nerve-transfer criterion

A->B passes only if:

```text
A Drive event
 -> measurable current/energy reaches B Memory path
 -> A Drive is removed and transient dies
 -> B retains a changed magnetic state
 -> the same later B probe differs from baseline
```

A simultaneous spike on B proves coupling only, not retained transfer.

## Reinjection lock

Correct:

```text
returned inductive/magnetic energy
 -> controlled steering
 -> DC-link/local reservoir capacitor
 -> later permitted event
```

Incorrect:

```text
returned energy -> 2.5 V VREF
```

State reinjection and energy reinjection are related but distinct measurements.

## One-Wave interpretation vs engineering proof

The One-Wave hypothesis interprets magnetism as reorganizing available lattice/superfluid pathways, with persistent organization providing history that changes later propagation.

Board #1 does not prove that substrate model. Board #1 tests the measurable hardware analogue:

```text
write
 -> remove drive
 -> retain magnetic state
 -> read
 -> old state changes new response
```

Only measured behavior advances to hardware canon.

## Authority

Use this update together with:

- `One_Wave_Bench/speculative/CELL_V1_BOARD_1_BASELINE_TEST_HARNESS.md`
- `One_Wave_Bench/speculative/CELL_V1_BUILD_PACKET.md`
- `One_Wave_Bench/speculative/CELL_V1_ANTI_DRIFT.md`
- `UPDATED_62_CELL_V1_HEX_FIRST_INTERNALS_AND_SCALING.md`
- `UPDATED_61_CELL_V1_REAL_HARDWARE_GROUNDING.md`
- `UPDATED_60_CELL_V1_HEX_EDGE_FLOWER_VOLUMETRIC_MEMORY_ARCHITECTURE.md`

If an older drawing routes flyback into virtual ground, equates the 18 bench terminals with the six cell ports, replaces the hex with a three-core fixture, or closes the full nerve ring before a single transfer is proven, this update supersedes that drawing.