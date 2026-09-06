# Point → Path → Field Recursive Scale Architecture

## Status

Architecture note capturing the current One-Wave cell/scale model. This is a design hypothesis and prototype target, not yet a claim of bench validation.

## Core distinction

The cell separates **state** from **direction**:

- **Binary state:** `Field | Void`
- **Polarity / direction:** chooses which way that state flows through the structure
- Direction is not an additional logical state.

So the basic interpretation is:

```text
state = Field or Void
polarity = route / flow direction
```

## Hex + center routing structure

The working geometry is one six-position outer structure around a central M4 router:

```text
             1
          /     \
        6         2
        |    M4   |
        5         3
          \     /
             4
```

The six outer positions can be viewed as three above and three below a center. M4 is the routing point between the mirrored halves.

The outer cells preserve Field/Void state. M4 does not need to be the memory itself; its job is to choose and coordinate the route through the combined structure.

## Ternary emerges from direction and mirroring

Ternary behavior is not treated as three unrelated stored voltage levels. Instead, ternary direction organizes the binary Field/Void states into a whole-system orientation.

The routing can resolve into two mirrored configurations with a neutral/hold relation between them:

```text
mirror A   ←   center / hold   →   mirror B
```

The important architectural separation is:

```text
Field / Void      = binary state
route direction   = polarity
mirrored whole    = ternary orientation
```

## Differential output

Once the two mirrored wholes are established, the next useful quantity is their difference:

```text
Δ = Mirror A - Mirror B
```

Conceptually:

```text
Mirror A dominates  →  +Δ
balanced relation   →   0
Mirror B dominates  →  -Δ
```

The differential is the resolved output of the complete local structure. The next scale should not need every internal switching detail; it receives the resolved relationship.

## Point → Path → Field

The scale rule is:

```text
Point → Path → Field
```

A point establishes or enters a path. The path resolves into a field. When that field is coherent/resolved, the entire lower-scale field becomes one effective point at the next scale.

```text
Scale n:
Point → Path → Field

Scale n+1:
Field(n) = Point(n+1)
Point(n+1) → Path(n+1) → Field(n+1)
```

Therefore the recursive ladder is:

```text
Point → Path → Field → Point → Path → Field → ...
```

## Compression across scale

The proposed scale boundary is a compression boundary:

```text
many lower-scale local relations
        ↓
resolved mirrored whole
        ↓
differential field
        ↓
one effective point for the next scale
```

This is the key scaling idea: **the Field of one scale becomes the Point of the next scale.**

The lower scale can retain its own internal state/memory, while the higher scale interacts with its resolved output as a single addressable state-point.

## Magnetic memory role

Magnetic memory is a candidate physical mechanism for retaining local Field/Void state after the routing event. The memory mechanism should be kept distinct from the routing rule:

- MOSFET/switching structure: changes or routes state
- magnetic element: retains state
- M4: coordinates route selection
- mirrored pair: produces the ternary orientation
- differential: produces the resolved local field
- resolved field: becomes the next-scale point

No assumption is made here that one magnetic element must intrinsically store three states. The ternary relation may emerge from the organization of multiple binary magnetic states.

## Prototype order

The architecture should be tested in this order:

1. Prove a reliable binary Field/Void cell.
2. Prove polarity can reverse routing without being confused with stored state.
3. Arrange cells around the six-position + M4 geometry.
4. Demonstrate two mirrored whole-system configurations.
5. Measure a repeatable signed differential between those mirrored configurations.
6. Add persistent magnetic state retention.
7. Treat the resolved differential field as one input point to a second-scale copy.
8. Test whether the same Point → Path → Field relation recursively survives scale-up.

## Current compact statement

```text
Binary chooses what:        Field | Void
Polarity chooses where:     flow direction
M4 chooses route:           path coordination
Ternary organizes whole:    mirrored orientation
Differential resolves it:   -Δ | 0 | +Δ
Field completes the scale:  Field(n) → Point(n+1)
```
