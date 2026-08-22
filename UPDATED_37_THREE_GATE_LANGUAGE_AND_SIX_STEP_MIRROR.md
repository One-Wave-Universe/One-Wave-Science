# UPDATED 37 — Three-Gate Language and Six-Step Mirror

**Status:** Canonical architecture update

## 1. Three Gate Classes

The clean gate language is:

```text
BINARY -> TERNARY -> QUADRATIC
   2         3           4
```

These are the three gate classes of the primitive.

A compact physical notation is:

```text
2-BDC -> 3-TAC -> 4-QRC
```

with the shorter equivalent:

```text
2DC -> 3AC -> 4RC
```

Definitions:

- **2-BDC / 2DC — Binary DC:** two-state directional DC choice / participation state.
- **3-TAC / 3AC — Ternary AC:** three-state asymmetric oscillating AC relation, including the neutral/hold relation.
- **4-QRC / 4RC — Quadratic Rotating Current:** four-state quadratic rotating-current relation; the target physical completion is a rotating magnetic-memory field/current state.

The hardware interpretation is experimental. These names define the architecture being tested; they do not by themselves prove that a breadboard implementation has achieved stable oscillation, rotation, or magnetic memory.

## 2. Six-Step Mirrored Use of the Three Gates

The three gate classes are traversed twice in mirrored order:

```text
2 -> 3 -> 4 -> 4 -> 3 -> 2
```

The six logical positions are:

```text
1. Binary
2. Ternary
3. Quadratic Action
4. Quadratic View
5. Ternary
6. Binary
```

Therefore the central quadratic pair is ordered:

```text
Quadratic Actions -> Quadratic Views
```

The first quadratic gate transforms state through the four Actions:

```text
Inward
Outward
Across
Over
```

The second quadratic gate reads the resulting relation through the four Views:

```text
Direction
Phase
Strength
Reference
```

Views and Actions remain separate layers and must not be collapsed into one four-state list.

## 3. Six Steps / Three Gates

The six-step cycle is made from three gate classes used twice:

```text
Binary pair:    Step 1 <-> Step 6
Ternary pair:   Step 2 <-> Step 5
Quadratic pair: Step 3 <-> Step 4
```

This gives the mirrored structural language:

```text
2B -> 3T -> 4QA -> 4QV -> 3T -> 2B
```

where `QA` is Quadratic Actions and `QV` is Quadratic Views.

## 4. State, Scale, and Recursive Language

Keep these axes separate:

- **FST — Field State Transitions:** `IDLE -> PRIMED -> EXECUTING -> VECTORING -> RESOLVING`.
- **VOS — Void Octave Scaling:** recursive scale position, separate from Field lifecycle state and separate from modulation/strength.
- **FR/VL — Field Root / Void Loop.**
- **VR/FL — Void Root / Field Loop.**
- **FRVL — Field-Recursive Void Loop.**
- **VRFL — Void-Recursive Field Loop.**

The root/loop notation identifies which side establishes the local root/reference and which side traverses the recursive loop. These are architecture labels and should not be silently substituted for the six invariant gate positions.

## 5. Anti-Drift Rule

Do not merge physical-current notation, logical gate notation, lifecycle state, octave scale, and recursive routing into one abbreviation.

Use the layers explicitly:

```text
PHYSICAL: 2-BDC -> 3-TAC -> 4-QRC
LOGICAL:  2B -> 3T -> 4QA -> 4QV -> 3T -> 2B
STATE:    FST
SCALE:    VOS
RECURSION: FR/VL | VR/FL | FRVL | VRFL
```

This keeps the language compact while preserving what each symbol actually describes.
