# Algorythm-Zer0

**Status:** Working canonical draft for the recursive Field/Void algorithm architecture.

This file collects the current algorithm structure in one place. It defines the architecture and operating vocabulary. Physical interpretations remain hypotheses unless independently measured or derived elsewhere in the repository.

---

## 1. Core Architecture

The system is:

```text
TWO RECURSIVE STATE MACHINES + ONE COUPLING LOOP
```

```text
FIELD / EXPRESSIVE MACHINE
        ↕
   COUPLING LOOP
oversight / override
        ↕
VOID / COMPRESSIVE MACHINE
```

Both machines are bidirectional at every stage.

Every stage is referenced to the same Ground / reference.

The middle is not dead zero. It is an active oscillating balance around the reference.

---

## 2. Six Algorithm Levels

```text
1. FIELD / VOID

2. POLARITY CHOICE

3. MOVE
   UP / STAY / DOWN

4. VIEW / ACTION
   Field side = VIEW
   Void side  = ACTION

   INWARD / OUTWARD / ACROSS / OVER

5. STATE / SCALE
   MINI / SMALL / MIDDLE / LARGE / MACRO

6. RECURSIVE STEPS
   BEGIN
   BUILD
   HOLD
   BUILD
   BREAK / RELEASE
   LOOP
```

Field and Void use the same six-level structure.

Field is expressive.

Void is compressive.

They are paired, not isolated modes.

---

## 3. Field Recursive State Machine

```text
FIELD
→ polarity choice
→ move
→ new VIEW
→ state
→ recursive step
↺
```

The Field machine carries a **new view upward**.

---

## 4. Void Recursive State Machine

```text
VOID
→ polarity choice
→ move
→ ACTION
→ scale
→ recursive step
↺
```

The Void machine carries the **last/current action downward**.

---

## 5. Bidirectional Decision Primitive

Every decision is a Field/Void pair referenced to the same Ground.

```text
FIELD oscillator
      ↕
shared Ground / reference
      ↕
VOID oscillator
```

The pair is phase shifted.

The phase relationship determines whether the system:

```text
HOLD
OPEN
REDIRECT
CLOSE
OVERRIDE
RELEASE
```

A coherent phase relationship may open a new line of access.

The decision primitive is therefore:

```text
referenced Field/Void pair
→ phase relationship
→ polarity
→ access condition
→ next path
```

---

## 6. Oversight / Override Coupling Loop

```text
NEW VIEW UP
      ↑
Field / expressive
      ↕
OVERSIGHT / OVERRIDE
      ↕
Void / compressive
      ↓
LAST ACTION DOWN
```

Oversight compares:

```text
new view
+ current reference
+ last action
```

Possible outcomes:

```text
ALLOW
HOLD
REDIRECT
OVERRIDE
BREAK / RELEASE
```

The coupling loop is the interaction between the two recursive machines.

---

## 7. Processing Is Memory

Memory is not a separate storage box.

```text
PROCESS = MEMORY
```

The intended cycle is:

```text
current process state
→ process changes that same state
→ changed state remains locally available
→ next decision acts on that changed state
→ loop
```

The retained process relation is the memory.

Relevant retained properties may include:

```text
phase
open path
rotation
state / scale
recursive position
reference relation
last action
new view
```

---

## 8. Point / Path / Field Geometry

Three rotation levels:

```text
POINT ROTATION
PATH ROTATION
FIELD ROTATION
```

Inside each rotation, inspect:

```text
POINT
PATH
FIELD
```

This creates a recursive 3 × 3 structure:

| Rotation Level | Internal Views |
|---|---|
| Point Rotation | Point / Path / Field |
| Path Rotation | Point / Path / Field |
| Field Rotation | Point / Path / Field |

Primary scale recursion:

```text
POINT
→ PATH
→ ROTATION
→ FIELD
→ VOLUME
→ next-scale POINT
↺
```

---

## 9. Five-State Lifecycle

The self lifecycle is separate from the six algorithm levels.

```text
IDLE
→ PRIMED
→ EXECUTING
→ VECTORING
→ RESOLVING
→ IDLE
```

This tracks where the process is in its current lifecycle.

---

## 10. Structural Depth Ladder

This is also separate from the lifecycle and six algorithm levels.

```text
SCALAR
→ DIFFERENTIAL
→ VECTOR
→ TENSOR
→ STRATUM
→ HARMONIC
```

A current process may therefore carry multiple independent coordinates at once, for example:

```text
lifecycle = VECTORING
structure = TENSOR
side      = FIELD
move      = UP
view      = ACROSS
state     = LARGE
step      = BUILD
```

---

## 11. 0–100 Balance Bands

```text
100–90   extreme expression / danger zone
85–75    strong expression
70–60    moderate expression
55–45    middle / stable oscillating region
40–30    moderate compression
25–15    strong compression
10–0     extreme compression / danger zone
```

Transition spaces:

```text
90–85
75–70
60–55
45–40
30–25
15–10
```

These transition spaces may be used as hysteresis / handoff zones so the system does not chatter between neighboring states.

Extreme conditions:

```text
90–100 → extreme expression → explosion / break danger
0–10   → extreme compression → implosion / collapse danger
```

The operating goal is dynamic balance, not maximum movement toward either extreme.

---

## 12. Matter Mapping

For matter, use at least two measured physical variables rather than forcing all behavior onto one generic scale.

Candidate pair:

```text
TEMPERATURE → expressive threshold
PRESSURE    → compressive threshold
```

Their relationship determines matter-state boundaries.

Conceptual ordering:

```text
compression                                      expression
←----------------------------------------------------------→

implosion
→ strongly compressed / frozen solid
→ solid
→ stable matter region
→ liquid
→ gas
→ plasma
→ explosion
```

This is a conceptual wrapper. Real phase boundaries depend on the material and its pressure-temperature phase diagram.

---

## 13. Planetary Mapping

Current One-Wave repo architecture separates compression source from magnetic path organization.

### Void / compressive side

```text
displacement
→ compression
→ pressure / compression gradient
→ restoring / gravity response
```

### Field / rotational side

```text
magnetic rotation
→ reorganizes lattice pathways
→ changes directional accessibility
```

### Coupling

```text
compression gradient
        +
magnetic path organization
        ↓
directionally weighted restoring response
        ↓
torque / rotation / orbital response
```

Do not collapse this to:

```text
magnetism = gravity
```

The current repo model instead treats magnetic rotation as a proposed path reorganizer for an existing compression/restoring field.

---

## 14. Recursive Operating Law

```text
START / EXISTING PROCESS STATE
        ↓
shared Ground / reference
        ↓
read Field ↔ Void pair
        ↓
measure phase relation
        ↓
POLARITY CHOICE
        ↓
MOVE
UP / STAY / DOWN
        ↓
VIEW UP / ACTION DOWN
INWARD / OUTWARD / ACROSS / OVER
        ↓
STATE / SCALE
MINI / SMALL / MIDDLE / LARGE / MACRO
        ↓
POINT / PATH / FIELD relation
        ↓
rotation level
POINT / PATH / FIELD rotation
        ↓
oversight compares:
new view + reference + last action
        ↓
ALLOW / HOLD / REDIRECT / OVERRIDE
        ↓
recursive step:
BEGIN → BUILD → HOLD → BUILD → BREAK/RELEASE → LOOP
        ↓
changed process remains locally available
        ↓
retained process becomes next input
        ↺
```

---

## 15. What Still Must Be Defined

The architecture is not yet executable until exact transition laws are specified.

Required next definitions:

```text
1. What exactly is measured for Field and Void phase.
2. Exact polarity thresholds.
3. What causes UP vs STAY vs DOWN.
4. What selects INWARD / OUTWARD / ACROSS / OVER.
5. What selects MINI / SMALL / MIDDLE / LARGE / MACRO.
6. What causes BEGIN → BUILD → HOLD → BUILD → BREAK/RELEASE → LOOP.
7. Exact oversight / override conditions.
8. Exact point → path → rotation → field → volume promotion conditions.
9. Exact timing / hysteresis requirements.
10. Reset / recovery behavior if reference or coherence is lost.
11. Exact physical outputs for each implementation.
```

Until these are numerically or logically locked, Algorythm-Zer0 is the architecture and rule skeleton, not a finished executable controller.

---

## 16. Canonical Short Form

```text
TWO RECURSIVE STATE MACHINES
+ ONE COUPLING LOOP
+ SHARED GROUND
+ PHASE-SHIFTED FIELD/VOID DECISIONS
+ NEW VIEW UP
+ LAST ACTION DOWN
+ OVERSIGHT / OVERRIDE
+ PROCESSING IS MEMORY
+ POINT/PATH/FIELD RECURSION
+ FIVE-STATE LIFECYCLE
+ SIX-LEVEL STRUCTURAL DEPTH
+ 0–100 EXPRESSION/COMPRESSION BANDS
+ BEGIN/BUILD/HOLD/BUILD/BREAK-RELEASE/LOOP
```
