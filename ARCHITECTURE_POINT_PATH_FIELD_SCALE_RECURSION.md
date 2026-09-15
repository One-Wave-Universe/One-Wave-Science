# Point -> Path -> Rotation -> Field Recursive Scale Architecture

## Status

Architecture note capturing the current One-Wave CELL_V1 scale model.

This remains a design hypothesis and prototype target, not a claim of bench validation. CELL_V1 physical geometry is now governed by:

- `UPDATED_60_CELL_V1_HEX_EDGE_FLOWER_VOLUMETRIC_MEMORY_ARCHITECTURE.md`
- `CELL_V1_ANTI_DRIFT.md`
- `CELL_V1_BUILD_PACKET.md`

## 1. Core distinction

The cell separates state from direction/orientation:

- **Field / Void relation:** local paired state role;
- **polarity / direction:** which opposed end of an axis is active or being traversed;
- **magnetic history:** retained local physical state from prior drive;
- direction is not automatically an additional logical state.

The physical CELL_V1 port labels describe three mirrored axes rather than six unrelated states.

## 2. LOCKED CELL_V1 hex geometry

Connections occur at the centers of the six **flat sides/edges**, never at corners/vertices.

Clockwise edge order:

```text
A+ -> B+ -> C+ -> A- -> B- -> C-
```

Directly opposite through the center:

```text
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

The three lettered pairs are three intersecting mirrored axes.

A schematic must preserve the distinction between side centers and corners:

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

The bracketed labels are the ports. The vertices formed by the outline have no connection role.

## 3. Identical hexes form the seven-cell flower

The first planar scale-up is one center cell with six identical surrounding cells.

All seven cells use:

- the same orientation;
- the same clockwise edge order;
- flat-edge-to-flat-edge connections;
- no adapter or alternating cell type.

Identical cells naturally present matching letters with opposite polarity at shared sides:

```text
A+ | A-
B+ | B-
C+ | C-
```

This geometry should be treated as the baseline before inventing higher stack rules.

## 4. M4 is not the mandatory geometric center of every CELL_V1

Older versions of this file drew six outer positions around a central M4 router. That picture is superseded for **physical CELL_V1 geometry**.

The hex center is where the three A/B/C axes intersect geometrically and where local electronic/magnetic relationships may couple. M4 remains a higher-level fast routing/timing architecture and may eventually be implemented from the same primitive family, but CELL_V1 does not require a separate M4 component in the middle of every hex.

This correction changes the hardware geometry only. It does not remove the existing M4 View-UP / Action-DOWN routing role.

## 5. Physical state update

The working memory candidate is local hysteresis/remanence.

```text
M(n+1) = HYSTERESIS( M(n), u(n+1) )
```

`M(n)` is the old remanent magnetic state. The new drive `u(n+1)` pushes the material from that actual starting point. After the drive is removed, the resulting remanence becomes `M(n+1)`.

Therefore:

```text
old physical state + new event -> new physical state
```

is a history-dependent transition, not ordinary scalar addition.

The MOSFET routes/drives current; the hysteretic medium is the current candidate for retained state.

## 6. Revised scale rule

The primary scale rule is now stated more explicitly as:

```text
Point -> Path -> Rotation -> Field -> Volume
```

The older compact form `Point -> Path -> Field` remains the compression summary, but a CELL_V1 hardware implementation must answer whether paths can form stable rotations rather than skipping directly from path to an assumed field.

### Point

One local edge/cell state, or one completed lower-scale relation exposed as a compact next-scale interface.

### Path

A state transition propagates through connected CELL_V1 edge ports while preserving enough identity, phase, direction, and reference to affect the next cell.

### Rotation

A closed path supports a traveling/circulating phase/state pattern rather than only simultaneous switching, ringing, or a static loop.

### Field

Multiple local paths/rotations become coupled into a coherent larger relation while local states remain observable.

### Volume

Fields couple horizontally and through depth so X/Y/Z relationships can reinforce, oppose, intersect, or redirect in a controlled three-dimensional structure.

## 7. Recursive scale boundary

The original recursion remains:

```text
Scale n:
Point -> Path -> Rotation -> Field

Scale n+1:
resolved Field/Volume(n) = Point(n+1)
Point(n+1) -> Path(n+1) -> Rotation(n+1) -> Field(n+1)
```

The key compression principle is unchanged:

```text
many lower-scale relations
        ↓
resolved coherent structure
        ↓
compact relational interface
        ↓
one effective point at the next scale
```

The lower scale may retain internal physical memory while the higher scale interacts with its resolved relation.

## 8. Seven-cell flower as the first collective field test

The flower is not one seven-input lump. It is seven spatially distinct CELL_V1 modules.

Required questions:

1. Can one outer cell alter the center cell without destabilizing the reference?
2. Can a path pass through the center and emerge predictably?
3. Can perimeter/closed paths sustain a measurable traveling phase?
4. Can multiple paths coexist or intersect without collapsing all seven states into one?
5. Does retained magnetic history alter a later whole-flower response?

The seven cells may collectively form a higher state, but that state must be derived from measured local relationships rather than by shorting all seven into one node.

## 9. Magnetic memory and reinjection across scale

Memory and reinjection are connected but distinct requirements.

### Memory

```text
write -> remove drive -> retain -> read -> rewrite
```

The previous physical state changes the next response.

### Reinjection

```text
stored/returning energy
 -> measured recovery path
 -> reservoir or maintaining path
 -> controlled later event
```

A lower-scale cell, flower, or volume may eventually expose retained history upward, but a larger-scale memory claim must not be inferred merely because each individual element is magnetic.

## 10. Candidate 3 x 3 x 3 volume

The current strong scaling candidate is:

```text
3 x 3 x 3 = 27 lower-scale units
```

The word **unit is deliberately unresolved**. It may mean one CELL_V1, one seven-cell flower, or another experimentally justified packaged relation.

The test is not whether 27 is aesthetically satisfying. The test is whether the same local relation survives in X, Y, and Z and whether a completed volume can expose a compact next-scale state.

## 11. Candidate mirrored volume pair

A later candidate is:

```text
PRIMARY VOLUME <-> MIRROR-FLIPPED VOLUME
```

Possible jobs for the mirror volume:

- retained whole-volume history;
- complementary/opposed state;
- comparison/checking;
- return/reinjection;
- old-state/new-state interaction at the next scale.

This is OPEN until physical or simulation tests show that a mirror copy produces useful state separation rather than redundant duplication or destructive cancellation.

## 12. Open brain/M4 depth candidates

Do not convert current numerical ideas into permanent topology without tests.

Still open:

```text
normal + inverted
2 normal + 2 inverted
3 normal + 3 inverted
3+ / 3- / 3+
3- / 3+ / 3-
3 x 3 x 3 volumes and mirrored copies
```

A shallower M4 implementation may make sense for faster routing; a deeper higher-brain structure may make sense for more recursive state formation. Those are functional hypotheses, not established layer counts.

## 13. Hemispheres and body — candidate higher-scale relation

A candidate whole-system arrangement uses complementary/mirrored left and right hemisphere structures and predominantly crossed body routing:

```text
LEFT higher structure  <-> RIGHT body
RIGHT higher structure <-> LEFT body
```

Local nerve/reflex loops remain local and fast.

This is compatible with broad biological motifs such as contralateral control and bilateral/local coordination, but biology does not establish CELL_V1 geometry, magnetic memory, or any proposed stack count.

## 14. Prototype order

The architecture should be tested in this order:

1. Prove one opposed axis (`A+ <-> A-`) can write, retain, read, rewrite, and alter the next response.
2. Measure reinjection separately from retention.
3. Reproduce the same mechanism on B and C without changing the primitive.
4. Package the six edge interfaces into one canonical CELL_V1 hex.
5. Connect two identical cells and quantify propagation.
6. Extend to three cells and quantify accumulated loss/delay/distortion.
7. Close a path and demonstrate traveling/circulating state rather than only ringing.
8. Build the seven-cell flower and measure coupled paths/rotations.
9. Add the smallest depth coupling and measure reinforcement/opposition/crosstalk.
10. Only then test a 3 x 3 x 3 candidate volume and mirror-flipped companion.
11. Treat a resolved lower-scale field/volume as one input point to a second-scale copy and test whether the recursion survives.

## 15. Current compact statement

```text
CELL GEOMETRY:
  A+ -> B+ -> C+ -> A- -> B- -> C-
  flat edges only

OPPOSED AXES:
  A+ <-> A-
  B+ <-> B-
  C+ <-> C-

MEMORY:
  old remanent state conditions the next transition

SCALE:
  Point -> Path -> Rotation -> Field -> Volume

RECURSION:
  completed lower-scale Field/Volume -> next-scale Point

M4:
  fast higher routing / timing role, not mandatory cell-center geometry

BRAIN DEPTH:
  open until function is measured
```
