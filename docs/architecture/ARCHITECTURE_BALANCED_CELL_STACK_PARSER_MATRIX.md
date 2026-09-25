# BALANCED CELL STACK + PARSER MATRIX ARCHITECTURE

This note captures the current working architecture that emerged from the balanced-device discussion. It is a build hypothesis, not yet a validated physical brain-cell claim.

## 1. Balanced differential primitive

The simplest electrical primitive is not "three magical logic levels." It is a center-referenced differential system.

Working interpretation:

- Field proposes / leans one way
- Void provides the opposed validation/check relation
- the gate does not advance until the required differential condition is validated
- CENTER / HOLD is a real resolved condition

Electrical shorthand:

`above center = +`

`at center = HOLD / 0`

`below center = -`

The center reference remains continuously present. A branch may stop conducting without becoming conceptually disconnected from the reference system.

### Differential is the gate language

Every gate/stage must expose a measurable differential against the same continuously present CENTER reference.

A gate is therefore not a naked binary condition. Its local state is a reference-resolved relation:

```text
D = V(local+) - V(local-)
```

with both sides interpreted relative to the same CENTER / virtual ground.

The required progression is three differentials, not three unrelated circuits:

```text
D1 = BC-DC differential
D2 = TC-AC differential
D3 = QC-RC rotation/axis differential
```

Each new stage adds a relationship while preserving the previous reference. No handoff may invent a new local zero.

## 2. BC-DC -> TC-AC -> QC-RC

Current build ladder:

### BC-DC — Differential 1

Balanced/binary choice represented as a stable DC differential around the center reference.

```text
(+D1) ---- CENTER ---- (-D1)
```

Purpose: prove a point/state.

The first gate must expose the actual signed displacement from CENTER rather than merely reporting "on/off."

### TC-AC — Differential 2

Validated DC state is handed into an out-and-back oscillating relationship around the **same** CENTER.

The second point/path closes the relationship into an AC loop:

```text
+D2(t) -> CENTER -> -D2(t) -> CENTER -> +D2(t) ...
```

Purpose: prove transition/path, reversal, zero crossing, and phase without losing the D1 reference.

The TC-AC gate therefore has its own measurable differential while remaining reference-resolved to the same CENTER as BC-DC.

### QC-RC — Differential 3

A third independently measurable differential coordinates the confirmed phase relationships into rotation / axis behavior.

```text
D1 = point/state relation
D2 = opposed oscillation / phase relation
D3 = axis/rotation relation
```

`RC` here is the working architecture label for rotating/recursive coordination, not radio frequency.

Purpose: prove controlled rotation / field behavior.

For the electrical precursor, the minimum requirement is a center-referenced drive vector with independently measurable axis differentials. Two phase-shifted AC axes can trace a rotating vector in a plane. A third independently driven center-referenced axis can tilt/precess that drive vector through three dimensions.

This remains an **electrical drive-vector result** until magnetic field-vector measurement exists.

Engineering question: can each handoff preserve the same reference, timing, phase, and validation without an ambiguous intermediate state?

### Three differentials / three gate receipts

Every transition should retain at least:

```text
reference_id = CENTER
D1 = measured BC-DC differential
D2 = measured TC-AC differential + phase
D3 = measured QC-RC axis/rotation differential + phase
```

If one of those is missing, the next stage does not have enough information to claim a reference-resolved handoff.

## 3. Three-cell stack experiment

Start with three measurable stages:

1. **Cell 1 — D1 / DC differential**: establish the validated point/state.
2. **Cell 2 — D2 / AC handoff**: produce controlled out-center-in behavior and measurable phase around the same CENTER.
3. **Cell 3 — D3 / rotation / axis coordination**: add an independently measurable axis differential and drive multiple magnetic components.

All stages expose test points and share the same defined reference strategy. Do not infer a 3D field from a 2D schematic.

When magnetic hardware is introduced, use a 3-axis field measurement:

`B(t) = (Bx(t), By(t), Bz(t))`

The measured vector trajectory, not the drawing, determines whether the result is circular, elliptical, planar, volumetric, stable, or unstable.

The electrical drive differentials and magnetic field components are related measurements, not interchangeable labels. A valid implementation should eventually be able to show both:

```text
Ddrive(t) = (Dx(t), Dy(t), Dz(t))
B(t)      = (Bx(t), By(t), Bz(t))
```

## 4. Slice -> pyramid -> cube -> field

Working geometry:

- a hexagon is a **slice / cross-section**, not the complete volumetric object
- triangular relationships are local connections inside a slice
- pyramid connections extend those relationships between layers
- stacked slices create depth
- a cube is the X/Y/Z coordinate scaffold
- the combined field/state volume is generated by the relationships across the stack

The physical orientation may or may not be functionally necessary. This must be tested by comparing the same topology laid flat versus physically stacked/oriented.

## 5. First R27 target

Working first serious volumetric scale:

`3 x 3 x 3 = 27 cells`

R27 is not equated to 27 conventional bits.

If each cell has three independently resolvable states, the instantaneous local-state count alone is:

`3^27 = 7,625,597,484,987`

That number does **not** prove usable information capacity. Physical constraints, coupling, invalid states, symmetry, and noise will remove many theoretical combinations.

The architecture is interested in more than local symbols:

- cell states
- cell-to-cell relationships
- path selection
- phase/timing relationships
- routing state
- whole-field pattern
- differential between successive whole-field patterns

A fair conventional comparison must reproduce the full behavior, not merely provide a register with the same raw state-bit count.

## 6. Magnetic memory / maintained state

Two different mechanisms must remain distinct:

### Passive magnetic retention

A material with hysteresis/remanence can retain a state after drive is removed.

### Dynamically maintained / reinjected state

A state may also be maintained by feedback:

`set state -> observe decay -> lower threshold -> reinject -> restore -> disconnect`

This resembles refresh memory. It does not remove physical losses and must be benchmarked against continuous excitation.

The reinjection trigger is the **measured differential state**, not elapsed time.

For a future field cell, a candidate test is to define an allowed reference-resolved `Dx/Dy/Dz` drive band and, once field-vector measurement exists, an allowed `Bx/By/Bz` state band. Measure whether selective reinjection maintains those bands reproducibly and efficiently.

## 7. Nerve layer is not the brain cell

The three-winding ternary control belongs to the fast nerve / local actuation layer.

Working separation:

- three-winding ternary nerve: fast local `- / HOLD / +` control
- bidirectional MOSFET pair: candidate low-loss local nerve gate for bilateral routing
- sensors: proximity, tilt/angle, current, temperature, pressure, position, vibration, field, etc.
- vagus-style regulation layer: slower body-state regulation / escalation
- M4: routes and synchronizes information between lower and higher layers
- higher brain cell remains a separate unsolved primitive

Do not silently rename the three-winding nerve as the brain cell.

## 8. Parser matrix — software hive version

The software experiment mirrors the balanced principle without pretending the software is the physical cell.

### Balanced parser pair

Two separate parser/processor programs:

- **expressive parser**: expands possibilities, interpretations, candidate links, candidate paths
- **compressive parser**: contracts, removes redundancy, checks stability, preserves the smallest useful representation

The differential between their outputs is meaningful state.

### Three-parser local cluster

Add a third role:

- resolver / connector: determines whether the local result becomes a committed point / next path connection

Working local thought cell:

`expressive + compressive + resolver`

### First parser field

Three clusters of three parsers:

`3 clusters x 3 parsers = 9 parsers`

This is the first complete Point -> Path -> Field software experiment.

## 9. Parsers are processing and memory

Memory should live in parser state rather than beginning as a separate giant transcript store.

Working rule:

- processing = parser-state transition
- memory = persistent parser state + links + transition structure
- recall = cue-driven reconstruction of the relevant parser constellation

Video-game analogy: store anchors, object/state relationships, links, transforms, and local context; rebuild the needed local scene/state instead of keeping the entire world continuously expanded.

Candidate per-parser retained state:

- parser ID / role
- current active/inactive or local state
- previous transition
- linked parser IDs
- local context tags
- confidence / relationship strength where required
- lifecycle / timestamp metadata where useful

The minimum sufficient retained state should be discovered experimentally rather than assumed.

## 10. Router / Admin / Dream hardware split

Current heterogeneous prototype split:

- **M4 / router**: fast routing, timing, synchronization, attention/event handoff
- **CPU / Administrator**: lifecycle, constraints, arbitration, validation, commit decisions
- **GPU / Dream**: parallel candidate generation, reconstruction, simulation, possibility search

A Hailo-8-class M.2 accelerator may be tested as a fast inference/routing helper, but M4 is an architectural role, not a specific chip.

Canonical whole-system lifecycle:

`Idle -> Primed -> Executing -> Vectoring -> Resolving`

Small parsers may remain much simpler locally while the whole coordinated system follows this lifecycle.

## 11. What counts as progress

Do not claim the full architecture because the pieces individually exist.

Progress is:

1. build a useful balanced device
2. measure D1 / BC-DC against CENTER
3. measure D2 / TC-AC around the same CENTER
4. measure D3 / QC-RC electrical axis rotation around the same CENTER
5. carry only the proven rule upward
6. add real Bx/By/Bz magnetic-field measurement before claiming 3D field shape
7. test state maintenance and differential-triggered reinjection
8. test parser-state reconstruction
9. only then integrate into the first volumetric cell network

The architecture is explicitly designed so hardware devices, the virtual breadboard, and parser experiments teach the same later cell problem from different directions.
