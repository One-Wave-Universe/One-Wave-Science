# UPDATED 61 - CELL_V1 Real-Hardware Grounding

**Status:** Current physical implementation correction. Geometry from Updated 60 remains locked. This file changes the preferred *bench implementation* by grounding it in hardware families that have actually been built.

## 1. What stays locked

Nothing in this update changes the CELL_V1 hex interface.

```text
PORTS: flat sides / edges only
CLOCKWISE: A+ -> B+ -> C+ -> A- -> B- -> C-
OPPOSITES: A+ <-> A-, B+ <-> B-, C+ <-> C-
FLOWER: seven identical cells, same orientation, edge-to-edge
```

The six edge ports are the **external relational interfaces of the cell**. They are not automatically six separate magnetic windings.

That distinction is now mandatory.

## 2. Correction to the earlier bench picture

The preferred first magnetic implementation is **not** three ordinary toroids with six arbitrary windings on each toroid.

The better grounded target is:

```text
A multifunction magnetic element
B multifunction magnetic element
C multifunction magnetic element

arranged as a symmetric three-axis group
+
three-phase-style six-switch power stage
+
separate electrical reference
+
DC-link / reinjection reservoir
```

Each A/B/C magnetic element is derived from demonstrated features of:

- fluxgate magnetic sensors;
- saturable reactors / magnetic amplifiers;
- transfluxor ferrite memory;
- planar magnetic memory structures;
- three-phase MOSFET motor bridges;
- regenerative DC-link energy recovery.

The complete CELL_V1 combination remains experimental.

## 3. Real build precedent - fluxgate magnetic element

A modern fluxgate current sensor has been built with a toroidal magnetic core carrying multiple functionally distinct windings, including:

```text
excitation winding
feedback winding
induction / sense winding
```

A demonstrated example is described in:

- Sensors 2025, "Design and Characterization of a Self-Oscillating Fluxgate-Based Current Sensor for DC Distribution System Applications"
- <https://www.mdpi.com/1424-8220/25/8/2360/html>

This directly supports the idea that one magnetic element can simultaneously have a drive/excitation role, a separate sense role, and a feedback role.

It does **not** prove nonvolatile CELL_V1 memory because conventional fluxgate cores are normally driven cyclically for sensing.

## 4. Real build precedent - magnetic amplifier / saturable reactor

Magnetic amplifiers and saturable-reactor motor controls used magnetic cores with different windings for different jobs.

A particularly relevant built design specifies:

```text
bias winding
control / maintaining winding
power windings
```

and describes a maintaining winding that keeps the reactor saturated after the initiating start signal is removed.

Reference:

- US2958816A, Saturable reactor motor control circuits
- <https://patents.google.com/patent/US2958816A/en>

Another magnetic-amplifier motor-control design uses control windings magnetically coupled to reactor windings to control saturation and power flow:

- US2844779A
- <https://patents.google.com/patent/US2844779A/en>

This is strong precedent for a small magnetic/control path governing a larger electrical path.

It does **not** prove the CELL_V1 memory or scaling law.

## 5. Real build precedent - transfluxor nonvolatile magnetic memory

Transfluxors are closer to the memory requirement than ordinary toroids.

A demonstrated transfluxor memory element used magnetic material with a substantially square hysteresis loop and separate apertures / paths for control and read functions. Implementations included:

```text
write winding
read winding
sense winding
remanent magnetic state
non-destructive readout behavior
```

Reference:

- US3328785A, Transfluxor memory employing common read-write circuits
- <https://patents.google.com/patent/US3328785A/en>

A separate planar implementation used magnetic sheet material patterned into transfluxor elements with printed write, read, inhibit, bias, and sense conductors:

- US3206733A, Memory systems having flux logic memory elements
- <https://patents.google.com/patent/US3206733A/en>

This is the strongest direct precedent for CELL_V1's requirement that a prior magnetic state survive and influence a later electrical/magnetic event.

It also warns against assuming that one plain toroid is automatically the best memory geometry. Multi-aperture or otherwise separated magnetic paths may be necessary.

## 6. Real build precedent - three-phase six-MOSFET bridge

The six-transistor power section is standard engineering when it is used as **three half-bridges**:

```text
A high-side + A low-side
B high-side + B low-side
C high-side + C low-side
```

Texas Instruments currently sells three-phase gate drivers specifically designed to drive six external N-channel MOSFETs. Examples include DRV8363-Q1 and DRV8334.

References:

- <https://www.ti.com/product/DRV8363-Q1>
- <https://www.ti.com/product/DRV8334>

Therefore six MOSFETs are well grounded for a three-axis A/B/C power stage.

They are **not** enough for six totally independent bidirectional winding channels. The winding interconnection and switching requirements determine switch count.

## 7. Real build precedent - DC-link regeneration

Regenerative motor drives return energy from an inductive motor/load into the DC link during braking or deceleration.

An Infineon industrial inverter reference explicitly describes energy being transferred back into the DC-link capacitor during motor braking/deceleration, raising the DC-bus voltage.

Reference:

- Infineon REF-22K-GPD-INV-EASY3B user guide
- <https://www.infineon.com/dgdl/Infineon-UG2020_28_REF-22K-GPD-INV-Easy3b-UserManual-v01_00-EN.pdf?fileId=5546d46277fc7439017802de2ffb672a>

This establishes the correct engineering precedent for CELL_V1 reinjection:

```text
returned inductive / magnetic energy
 -> bridge / steering path
 -> DC-link or local reservoir capacitor
 -> later permitted power event
```

The virtual reference is **not** the energy dump or reservoir.

## 8. Grounded A/B/C magnetic-element target

The current preferred bench element is a multifunction magnetic device, not a six-winding counting exercise.

Candidate functions per A/B/C element:

```text
POWER / DRIVE winding or conductor
CONTROL / WRITE winding
SENSE winding
FEEDBACK / MAINTAIN winding
```

A first implementation may combine functions where the real magnetic topology allows it, but the prototype should keep them separate enough to measure cause and effect.

The exact number of physical windings remains experimental.

The important rule is functional separation:

```text
DRIVE changes magnetic condition
WRITE intentionally establishes retained state
SENSE reads state with minimum disturbance
FEEDBACK / MAINTAIN applies controlled correction or return
```

If one winding performs two roles, document and measure both roles instead of renaming the same waveform after the fact.

## 9. Grounded three-element workbench arrangement

A useful test fixture is:

```text
                 [ A ELEMENT ]
                      /\
                     /  \
                    /    \
          [ C ELEMENT ]--[ B ELEMENT ]
                    \    /
                     \  /
                      \/
               ELECTRICAL REFERENCE
```

The three magnetic elements may be physically arranged symmetrically around the reference for a clean experimental layout.

However:

- 120 electrical degrees in a three-phase system does not prove that three separate toroids must physically sit 120 degrees apart;
- the central geometric point does not create virtual ground by itself;
- the electrical reference must be built and measured as an electrical circuit node;
- returned energy must go to the DC-link / reinjection reservoir, not into the reference node.

## 10. Shared magnetic floor - demoted from assumption to experiment

A shared ferromagnetic or magnetic-film substrate remains an interesting later test, but it is **not** part of the first required prototype.

Real magnetic-memory precedents show that persistent magnetic films and planar magnetic structures are possible, but they use engineered materials, anisotropy, geometry, and bias conditions.

Therefore this claim is forbidden without measurement:

```text
"ordinary nanoparticle sheet automatically becomes shared muscle memory"
```

The correct experiment is:

```text
apply known magnetic write event at A
remove drive
measure local remanent state
measure state at B and C locations
apply standardized later probe
compare response with and without prior write
```

Only if the substrate shows repeatable spatially resolved history dependence does it become part of the CELL_V1 memory architecture.

## 11. Revised physical stack

Current grounded stack:

```text
TOP / ELECTRONICS
- six-MOSFET three-half-bridge A/B/C power stage where appropriate
- gate driver / dead time / protection
- current and voltage sensing
- separate low-noise reference generation and measurement

MIDDLE / MAGNETIC ELEMENTS
- A multifunction magnetic element
- B multifunction magnetic element
- C multifunction magnetic element
- drive/write/sense/feedback functions derived from measured need

ENERGY LAYER
- DC-link / reinjection capacitor
- steering / clamp / synchronous recovery path
- energy accounting

OPTIONAL EXPERIMENTAL BOTTOM LAYER
- patterned/shared magnetic substrate only after single-element retention works
```

This stack is much closer to demonstrated engineering than the previous literal `3 rings x 6 windings` picture.

## 12. Six CELL_V1 edge ports are not six coils

This is now an explicit anti-drift rule.

```text
A+, B+, C+, A-, B-, C-
```

are the six external edge interfaces of the hex cell.

They may map through electronics into three magnetic axes, but there is no requirement that each edge label correspond to one separate physical winding.

Similarly, the functional windings on an A/B/C magnetic element do not replace or reorder the six canonical hex edges.

Keep these layers separate:

```text
HEX INTERFACE GEOMETRY
        !=
MAGNETIC WINDING COUNT
        !=
MOSFET COUNT
```

## 13. Revised first physical proof

Before building three magnetic elements, prove **one multifunction magnetic element**.

Minimum fixture:

```text
current-limited low-voltage source
        |
controlled drive path
        |
multifunction magnetic element
   |        |        |
 WRITE    SENSE   FEEDBACK
   |        |        |
command   scope    controlled return
                    |
              reservoir capacitor
```

Required sequence:

1. characterize ordinary inductive behavior with memory disabled / absent;
2. write magnetic state in one direction;
3. remove drive;
4. read state with the weakest practical interrogation;
5. reverse the write and repeat;
6. show the retained state changes a standardized later response;
7. separately measure returned energy into the reservoir;
8. only then copy the element into A/B/C.

## 14. What this update establishes and does not establish

### Established by real-world precedent

- multiple functional windings can coexist on one magnetic core;
- magnetic saturation can control larger electrical power paths;
- remanent ferrite state can store information and affect later readout;
- multi-aperture magnetic structures can separate write/read/sense paths;
- six MOSFETs can form a three-phase A/B/C bridge;
- inductive/motor energy can be returned to a DC-link capacitor.

### Still unproven for CELL_V1

- the exact A/B/C magnetic-core geometry;
- exact winding count and turn ratios;
- whether a toroid, E-core, multi-aperture ferrite, planar film, or hybrid is best;
- shared-substrate memory;
- analog reinjection benefit at cell scale;
- stable rotating field/state through CELL_V1 paths;
- seven-cell flower collective state;
- volumetric `3 x 3 x 3` recursion;
- mirrored-volume brain memory;
- M4 and higher-brain physical layer counts.

## 15. Build rule

Do not invent symmetry where real hardware already tells us what to test.

Use the existing technologies as the floor:

```text
fluxgate -> separate excitation / sense / feedback
magnetic amplifier -> control of power through magnetic saturation
transfluxor -> remanent memory + separated magnetic paths
3-phase bridge -> six-switch A/B/C power routing
DC link -> measured energy return and reuse
```

Then test what CELL_V1 adds on top of that floor.
