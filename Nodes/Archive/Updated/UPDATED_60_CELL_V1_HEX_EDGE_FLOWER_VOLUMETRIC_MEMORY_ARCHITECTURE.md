# UPDATED 60 — CELL_V1 Hex-Edge Flower, Magnetic State, Reinjection, and Volumetric Scaling

**Status:** Current canonical CELL_V1 hardware-geometry consolidation and experimental build target.

This update locks the geometry that has repeatedly drifted in diagrams while keeping unproven brain/M4 depth choices explicitly open. It does **not** claim that the complete CELL_V1 has been physically demonstrated. It defines what must be built and measured next.

## 1. Authority and scope

For CELL_V1 physical geometry, this file supersedes any older diagram or note that:

- places electrical or magnetic lattice ports on hex corners/vertices;
- uses a clockwise side order other than `A+ -> B+ -> C+ -> A- -> B- -> C-`;
- rotates or alternates individual cells merely to make a seven-cell flower connect;
- requires a different cell type for different positions in the flower; or
- treats M4 as a mandatory physical center component of every CELL_V1 hex.

This file does **not** replace the separate canonical distinctions among binary choice, ternary movement, six route addresses, six process gates, five-state lifecycle, View/Action direction, M4 runtime, or higher cognitive roles. Those remain governed by their existing authority files.

## 2. LOCKED — the CELL_V1 six-edge geometry

Connections are located at the centers of the six **flat sides / edges** of the hexagon.

**There are no lattice connections at corners or vertices. Corners are structural only.**

Clockwise side order is locked as:

```text
A+ -> B+ -> C+ -> A- -> B- -> C-
```

The three exact opposite pairs are therefore:

```text
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

Each letter defines one straight mirrored axis through the cell center.

A schematic must be read by flat side, not by vertex:

```text
                      [ A+ EDGE ]
                 __________________
                /                  \
 [ C- EDGE ]   /                    \   [ B+ EDGE ]
              /                      \
              \                      /
 [ B- EDGE ]   \                    /   [ C+ EDGE ]
                \__________________/
                      [ A- EDGE ]
```

The labels above represent **edge-center ports**. The six geometric corners shown by the line intersections have no port function.

## 3. LOCKED — identical-cell flower tiling

A seven-cell flower is one center hex plus six surrounding hexes.

Every hex uses the **same physical orientation and the same edge order**:

```text
A+ B+ C+ A- B- C-
```

No alternate cell rotation, no alternate wiring convention, and no adapter cell is required.

When identical cells share a flat side, the opposed normals naturally mate matching letters with opposite polarity:

```text
A+ | A-
B+ | B-
C+ | C-
```

This is the first required two-dimensional scaling rule.

## 4. Current physical construction target — electronic top, magnetic bottom

The present hardware target is a compact chip/module with two tightly coupled halves.

### Top / electronic half

- integrated or co-located MOSFET switching for the six bidirectional edge paths;
- gate-drive and local protection circuitry;
- local voltage/current sensing;
- six edge-center electrical interfaces;
- routing between the three opposed axes A, B, and C;
- connection to the local electrical center/reference.

### Bottom / magnetic half

- ferrite or another measured hysteretic magnetic medium;
- drive/write winding geometry;
- memory/maintaining/reinjection winding geometry;
- separate sense winding during prototype development where useful;
- retained magnetic state through remanence/hysteresis;
- coupling back to the electronic half through vias/traces/windings/sensors.

The integrated-chip form is the scaling target. Early bench prototypes may use discrete MOSFETs and separate cores so the individual mechanisms can be measured before packaging them.

## 5. Electrical center and magnetic state are separate physical quantities

The current bench architecture keeps an **electrically established center reference**. A 5 V supply with a 2.5 V buffered center is a practical low-voltage candidate for testing.

Do not revive the retired `+/-12 V` design merely to obtain a positive and negative label.

The `+` and `-` edge labels describe opposed orientation relative to the local differential reference and magnetic axis; they are not permission to short raw supply rails together.

The magnetic medium does **not** become electrical ground merely because it stores magnetic history.

## 6. Magnetic state — how old and new become new

The retained state lives in the hysteretic magnetic material, not in the MOSFET gate.

A useful experimental state relation is:

```text
M(n+1) = HYSTERESIS( M(n), u(n+1) )
```

where:

- `M(n)` is the remanent magnetic state before the new event;
- `u(n+1)` is the new electrical/magnetic drive event;
- `HYSTERESIS(...)` is the **measured nonlinear response of the actual material**, not ordinary linear addition;
- `M(n+1)` is the remanent state remaining after the event ends.

The required physical behavior is:

```text
old remanent state
        +
new drive pulse
        ->
transition along the material hysteresis path
        ->
new remanent state
        ->
next event begins from that new state, not from zero
```

That is the candidate primitive for physical memory and repetition-dependent response.

## 7. Memory and reinjection may share hardware but require separate proof

Two measurements are required.

### Magnetic memory

A previous event must leave a persistent state that changes a later read or transition.

Minimum proof:

```text
write -> remove drive -> retain -> read -> rewrite -> repeat
```

### Reinjection

Recoverable energy/signal from a prior transition must be deliberately routed into a later permitted event instead of being completely dumped.

Candidate flow:

```text
drive
 -> magnetic / inductive storage
 -> field collapse or return
 -> steering / reservoir
 -> controlled reinjection
 -> later transition
```

If one winding performs both maintaining-memory and reinjection functions, that is acceptable only after both effects are independently measurable.

Reinjection is energy recovery/recirculation, **not free energy**. Required accounting includes input energy, stored energy, returned energy, delivered reinjection energy, and losses.

For a passive recovery event the measured returned energy must not exceed the energy made available to the recovery path without an identified external source.

## 8. CELL_V1 is not merely a motor commutator

Three-phase / three-winding motor hardware is a useful ancestor because it demonstrates A/B/C rotating-field organization and six power-switch positions. CELL_V1 must remain more general.

A cell may participate in:

- a motor/actuator path;
- a sensory path;
- a local reflex path;
- a memory path;
- a brain-like processing lattice;
- a larger point/path/field structure.

The six edge ports therefore should be treated as bidirectional coupled interfaces rather than hardwired as one fixed six-step motor sequence.

## 9. LOCKED design objective — Point -> Path -> Rotation -> Field -> Volume

The primary scalability goal is:

```text
POINT
 -> PATH
 -> ROTATION
 -> FIELD
 -> VOLUME
 -> next-scale POINT
```

Working definitions:

- **Point:** one local edge/cell state or one resolved lower-scale state.
- **Path:** propagation of a state change through connected edge ports and cells.
- **Rotation:** a stable traveling/circulating phase/state around a closed path rather than simultaneous uniform switching.
- **Field:** multiple local rotations/paths coupled into a coherent larger relation.
- **Volume:** horizontal, vertical, and depth-coupled fields interacting in 3D.
- **Next-scale point:** a completed lower-scale field/volume exposed through a compact relational interface to a larger scale.

The older Point -> Path -> Field recursion remains useful, but CELL_V1 now explicitly requires the intermediate question: **can the path form a stable physical rotation?**

## 10. Seven-cell flower as the first field unit

The seven-cell flower is the first compact planar structure for testing collective behavior:

```text
six identical outer CELL_V1 hexes
             around
one identical center CELL_V1 hex
```

Required properties:

- every cell keeps identical edge labeling and orientation;
- every shared connection is flat-edge to flat-edge;
- spatial identity of each of the seven cells remains observable;
- the flower must support local state propagation without forcing all seven cells into one indistinguishable node;
- closed paths around/through the flower must be measurable for phase and direction.

The center cell may eventually serve as a local combined-state participant, but it must not erase the directional information of the surrounding six cells.

## 11. OPEN but strong current direction — 3 x 3 x 3 volumetric expansion

The current higher-scale candidate is a three-dimensional recurrence:

```text
3 x 3 x 3 = 27 lower-scale units
```

The exact grain of `unit` is **OPEN**. It may ultimately be:

- one physical CELL_V1;
- one seven-cell flower;
- one resolved flower/block exposed as a next-scale point; or
- another experimentally justified packaged submodule.

Do not silently convert `3 x 3 x 3` into a final brain-cell count until the scale boundary is measured.

The architectural goal is that the same point/path/rotation/field rule continues along X, Y, and Z rather than changing logic when depth is added.

## 12. OPEN — mirrored volumetric copy for memory and reinjection

A leading candidate is:

```text
PRIMARY 3D VOLUME
        <->
MIRROR-FLIPPED 3D VOLUME
```

The mirror volume may provide:

- complementary/opposed magnetic state;
- retained whole-volume history;
- checking/comparison against the current volume;
- reinjection/return paths into the next update;
- a larger-scale old-state/new-state relation.

This is a hypothesis to test, not a proven necessity.

## 13. OPEN — layer-count and brain/M4 candidates

The following ideas are **not locked** and must remain alternatives until a smaller prototype establishes why the extra depth is needed:

- one normal flower + one inverted flower as a minimal memory/return pair;
- two normal + two inverted flowers as a shallower fast M4/nerve candidate;
- three normal + three inverted flowers as a deeper higher-brain candidate;
- three blocks of three flower layers, such as `3+ / 3- / 3+`, with the opposite hemisphere `3- / 3+ / 3-`;
- a dedicated third/nerve layer;
- a middle seven-cell flower acting as a combined-state plane;
- replacing flat layer counting with full `3 x 3 x 3` volumetric recursion.

Do not turn any of these counts into canon because their numerical symmetry is attractive. Each additional layer/block must earn its existence by measurable function.

## 14. M4 relationship

Existing M4 architecture remains the fast routing/timing relationship carrying Views upward and Actions downward.

For CELL_V1 hardware integration:

- M4 does not have to occupy the geometric center of each hex;
- M4 may be implemented as a higher-scale fast-routing block built from the same primitive family;
- a four-layer or other shallower M4 realization is an open hardware hypothesis;
- the View-UP / Action-DOWN direction rule remains conceptually distinct from the number of physical CELL_V1 layers.

## 15. OPEN — mirrored hemispheres and crossed body routing

A current brain-scale candidate is that left and right hemispheres use complementary/mirror-flipped volume organizations, with major control paths crossing:

```text
left hemisphere  <-> right body
right hemisphere <-> left body
```

Local reflex/nerve loops should remain local enough to stabilize the body without requiring the highest cognitive layer to micromanage every actuator event.

Biology provides precedents for contralateral motor control, bilateral coordination, layered processing, and local reflex/CPG loops. Biology does **not** validate the exact CELL_V1 hex, magnetic hysteresis mechanism, `2+2`, `3+3`, nine-layer, or `3 x 3 x 3` counts.

## 16. Existing hardware families that contribute real mechanisms

No known published build combines all CELL_V1 functions into one cell. Useful demonstrated ancestors include:

| Hardware family | Demonstrated mechanism useful to CELL_V1 | What it does not prove |
| --- | --- | --- |
| Mark Tilden / BEAM nervous networks | local analog delay/reflex cells, sensor modulation, sequencing loops, direct motor output without a central CPU | magnetic nonvolatile state and CELL_V1 geometry |
| Saturable reactors / magnetic amplifiers | magnetic core state controls a larger electrical power path; control/bias/maintaining windings | six-edge brain cell or self-powering loop |
| Transfluxor ferrite memory | remanent magnetic state changes later magnetic/electrical behavior; multi-path cores | CELL_V1 MOSFET integration or scaling law |
| Three-phase regenerative motor drives | A/B/C phase organization, six switch positions, recoverable energy returned to a DC link | hysteretic brain memory |
| Spintronic/domain-wall devices | prior pulses can alter persistent later electrical response | macroscopic CELL_V1 packaging |
| Coupled physical oscillators / analog CPGs | distributed phase coordination and rhythmic output | the proposed hex/magnetic memory architecture |

Reference starting points:

- Tilden nervous networks: <https://patents.google.com/patent/US5325031A/en>
- Saturable-reactor motor control: <https://patents.google.com/patent/US2958816A/en>
- Transfluxor magnetic memory: <https://patents.google.com/patent/US3376427A/en>

These precedents justify component mechanisms, not the combined CELL_V1 claim.

## 17. Validation ladder — make scale earn itself

The build should advance only after the prior level passes.

### Gate A — one magnetic axis

Prove one `A+ <-> A-` axis can write, retain, read, reverse, and alter the next response.

### Gate B — two cells

Prove a transition in cell 1 measurably changes the permitted response in cell 2 through an edge connection.

### Gate C — three-cell path

Prove state/phase information survives at least three transfers with quantified loss, delay, and distortion.

### Gate D — closed rotation

Create a closed path and distinguish a traveling/circulating pattern from simple simultaneous switching or ringing.

### Gate E — seven-cell flower

Demonstrate coupled local paths/rotations while retaining individual cell state observability.

### Gate F — stacked/3D structure

Demonstrate X/Y/Z coupling and show that vertical/depth connections add controlled behavior rather than uncontrolled cancellation/crosstalk.

### Gate G — mirrored volume

Demonstrate that a mirror-flipped copy retains or returns information/energy that changes a later whole-volume state in a reproducible way.

### Gate H — recursive scale

Expose the resolved lower-scale structure as one higher-scale relational point and show that Point -> Path -> Rotation -> Field can occur again without replacing the primitive.

## 18. Mandatory measurements

At minimum, record where applicable:

```text
time
cell_id / edge_id
edge axis A/B/C and polarity +/-
electrical center/reference voltage
edge voltage and current
MOSFET command and actual switching state
write-pulse magnitude/duration
sense-winding response
retained magnetic readback
phase/delay to neighbor
reinjection reservoir voltage/current
energy in / stored / returned / delivered / lost
temperature
faults / saturation / unknowns
```

Unknown remains unknown. Do not infer magnetic state or field rotation solely from a symmetric drawing.

## 19. Hard anti-drift block

```text
CELL_V1 CANONICAL PHYSICAL HEX

PORT LOCATION:
  FLAT SIDES / EDGES ONLY
  NEVER CORNERS / VERTICES

CLOCKWISE EDGE ORDER:
  A+ -> B+ -> C+ -> A- -> B- -> C-

DIRECT OPPOSITES:
  A+ <-> A-
  B+ <-> B-
  C+ <-> C-

FLOWER:
  7 IDENTICAL CELLS
  SAME ORIENTATION
  EDGE-TO-EDGE CONNECTIONS
  NO ADAPTER / ALTERNATE CELL TYPE

PRIMARY SCALE GOAL:
  POINT -> PATH -> ROTATION -> FIELD -> VOLUME -> NEXT-SCALE POINT

MAGNETIC STATE:
  RETAINED IN HYSTERETIC MATERIAL

REINJECTION:
  MEASURED RECOVERY / RECIRCULATION
  NOT UNEXPLAINED GAIN

BRAIN / M4 LAYER COUNTS:
  OPEN UNTIL MEASURED FUNCTION REQUIRES THEM
```

Any generated image, schematic, simulator, PCB, or prose that violates the port location or edge order above is geometrically wrong and should be rejected rather than rationalized.

## 20. Immediate next physical proof

Do **not** begin by fabricating the full brain stack.

The smallest decisive experiment remains one opposed magnetic axis with instrumented memory and recovery:

```text
A+ drive/write
 -> hysteretic core state
 -> remove drive
 -> read retained state
 -> measure next A+/A- response
 -> reverse write
 -> verify changed/reversed retained response
 -> measure recoverable energy separately
```

Once that is real, duplicate the same axis architecture into B and C, package the six flat-edge interfaces into one hex, then build the seven-cell flower.
