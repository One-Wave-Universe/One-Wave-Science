# Algorythm-Zer0 — Primitive Specification

**Status:** Core primitives locked. Domain mappings belong outside this file and may evolve without redefining the primitive grammar.

Algorythm-Zer0 is a cumulative mirrored recursion. Each higher level **contains and preserves every level below it**.

The six levels are not six independent modules. They are six nested resolutions of one Field/Void process.

---

# P0. THE MIRROR PRIMITIVE

Every level is built around the same paired structure:

```text
FIELD
  ↕
GROUND / REFERENCE
  ↕
VOID
```

Compact form:

```text
1 > (0) < 1
```

Primitive rules:

- Field and Void are mirrored counterparts of one process.
- Ground/reference belongs to the pair and is carried through every higher level.
- Ground is active reference, not dead nothing and not a third committed polarity.
- Field carries the new/expressive side of the relation.
- Void carries the checking/compressive/action side of the relation.
- The paired sides may differ in phase/state while remaining one coupled process.
- Processing and retained memory are one continuing process.

No higher level may discard the Field/Ground/Void mirror.

---

# P1. LEVEL 1 — REFERENCED FIELD/VOID STATE

Level 1 is the smallest complete state:

```text
FIELD ↔ GROUND/REFERENCE ↔ VOID
```

Level 1 contains the reference and both mirrored sides. A bare Field, bare Void, or bare scalar is not a complete Algorythm-Zer0 state.

---

# P2. LEVEL 2 — BINARY CHOICE CONTAINS LEVEL 1

Level 2 adds one binary polarity decision while preserving Level 1:

```text
EXPRESS ↔ COMPRESS
```

Core flow:

```text
CURRENT FIELD
→ defines the live EXPRESS / COMPRESS choice
→ CHOICE
→ selected polarity contributes to the NEW FIELD
→ VOID mirrors/checks the same referenced process
```

Primitive rule:

```text
LEVEL 2 = LEVEL 1 + CHOICE
```

The choice is never detached from Field, Void, and Ground.

---

# P3. LEVEL 3 — PAIRED TERNARY CONTAINS LEVELS 1 + 2

Level 3 adds a ternary operation on each mirrored side.

Field ternary:

```text
MODULATE / HOLD / RESET
```

Void ternary:

```text
CONFIRM / DEFER / DENY
```

Equivalent Void wording:

```text
CONFIRM / ABSTAIN / REJECT
```

Repo wording is `CONFIRM / DEFER / DENY`.

Primitive rule:

```text
LEVEL 3 = LEVEL 2
        + FIELD TERNARY
        + VOID TERNARY
```

`HOLD` and `DEFER` are active middle conditions, not absence of activity.

The exact transition law is implementation-specific. The three-way structure is primitive.

---

# P4. LEVEL 4 — FOUR VIEWS UP / FOUR ACTIONS DOWN CONTAIN LEVELS 1 + 2 + 3

Level 4 adds four simultaneous/available view slots on the Field side and four mirrored action slots on the Void side:

```text
4 VIEWS UP
    ↑
 FIELD
    ↕
GROUND / REFERENCE
    ↕
  VOID
    ↓
4 ACTIONS DOWN
```

Primitive rule:

```text
LEVEL 4 = LEVEL 3
        + FOUR VIEW SLOTS
        + FOUR MIRRORED ACTION SLOTS
```

Each Level-4 slot carries the lower packet with it:

```text
Field/Void mirror
+ Ground/reference
+ binary Choice
+ Field ternary
+ Void ternary
+ current View/Action slot
```

The **number four and the mirrored View-up/Action-down relationship are primitive**.

The names assigned to the four slots are **not primitive**. A domain may map them as, for example:

```text
POINT / PATH / BOUNDARY / HORIZON
```

or another four-part coordinate system, provided all four slots preserve Levels 1–3.

Likewise, relation vocabularies such as:

```text
INWARD / OUTWARD / ACROSS / OVER
RESONATING / INVERTED
ATTRACTING / OPPOSING
PARALLEL / INTERSECTING
```

are mappings/readouts, not replacements for the Level-4 primitive.

---

# P5. LEVEL 5 — FIVE-STATE RETENTION CONTAINS LEVELS 1 + 2 + 3 + 4

Level 5 retains the complete Level-4 packet in one of five distinguishable process states.

Primitive rule:

```text
LEVEL 5 = LEVEL 4 + FIVE-STATE RETENTION
```

The **count of five and retention of the entire lower packet are primitive**.

A current software/process encoding is:

```text
IDLE
→ PRIMED
→ EXECUTING
→ VECTORING
→ RESOLVING
→ IDLE
```

A scale-oriented domain may instead map five retained positions as:

```text
MINI / SMALL / MIDDLE / LARGE / MACRO
```

Those labels are mappings. The primitive is a five-position retained-state layer containing Levels 1–4.

---

# P6. LEVEL 6 — RECURSION CONTAINS LEVELS 1 + 2 + 3 + 4 + 5

Level 6 recurs the complete retained Level-5 state.

Primitive rule:

```text
LEVEL 6 = LEVEL 5 + RECURSION
```

Current canonical six-step process encoding:

```text
BEGIN
→ BUILD 1
→ HOLD
→ BUILD 2
→ BREAK / RELEASE
→ LOOP
```

`LOOP` feeds back the **complete nested state**, not a stripped value.

Therefore the next Level-1 state may be a compressed address to everything resolved below it.

---

# P7. CUMULATIVE CONTAINMENT — MASTER RULE

```text
LEVEL 1
[FIELD ↔ GROUND ↔ VOID]

LEVEL 2
[LEVEL 1 + BINARY CHOICE]

LEVEL 3
[LEVEL 2 + PAIRED TERNARY]

LEVEL 4
[LEVEL 3 + FOUR VIEWS / FOUR ACTIONS]

LEVEL 5
[LEVEL 4 + FIVE-STATE RETENTION]

LEVEL 6
[LEVEL 5 + SIX-STEP RECURSION]
↺
```

Numerically:

```text
1
↓
1 + 2
↓
1 + 2 + 3
↓
1 + 2 + 3 + 4
↓
1 + 2 + 3 + 4 + 5
↓
1 + 2 + 3 + 4 + 5 + 6
↺
```

The `1` always means the complete Field/Ground/Void mirror primitive.

Nothing at a higher level is allowed to silently delete the lower-level reference, Choice, mirrored side, or retained state.

---

# P8. MINIMUM COMPLETE EXECUTION

```text
CURRENT RETAINED PROCESS
        ↓
FIELD ↔ GROUND/REFERENCE ↔ VOID
        ↓
FIELD DEFINES EXPRESS / COMPRESS CHOICE
        ↓
CHOICE CONTRIBUTES TO NEW FIELD
        ↓
FIELD: MODULATE / HOLD / RESET
VOID:  CONFIRM / DEFER / DENY
        ↓
4 VIEWS UP / 4 ACTIONS DOWN
        ↓
5-STATE RETENTION
        ↓
6-STEP RECURSION
        ↓
COMPLETE NESTED RESULT REMAINS AS PROCESS/MEMORY
        ↓
RESULT PARTICIPATES IN DEFINING NEXT FIELD
        ↺
```

---

# P9. PROCESS = MEMORY

The algorithm does not require a conceptual separation between processing and memory.

```text
retained state exists
→ new relation arrives
→ same nested state changes
→ changed state remains available
→ next relation acts on changed state
```

A complete retained packet can therefore include all lower-level coordinates rather than rebuilding them from scratch.

---

# P10. SCALE RECURSION

A compatible nesting rule is:

```text
POINT
→ PATH
→ ROTATION
→ FIELD
→ VOLUME
→ NEXT-SCALE POINT
↺
```

This is not one of the six numbered algorithm levels. It is a way of applying the same cumulative primitive across spatial/structural scale.

A resolved larger whole can become one point in a higher recursion while retaining access to its lower internal structure.

---

# P11. DOMAIN MAPPING CONTRACT

A domain mapping may assign concrete meanings to the primitives, but it may not redefine the nesting.

Every mapping must explicitly state:

```text
1. What are Field, Void, and Ground/reference?
2. What does Express/Compress mean here?
3. What causes Modulate/Hold/Reset?
4. What causes Confirm/Defer/Deny?
5. What are the four View slots?
6. What are the four mirrored Action slots?
7. What do the five retained states mean?
8. What does one six-step recursion accomplish?
9. What physical/software resource is conserved or bounded?
10. What observation/test would show the mapping is wrong?
```

Mappings belong in `Algorythm-Zer0-Domain-Mappings.md` or domain-specific files, not in this primitive specification.

---

# P12. ONE-LINE PRIMITIVE

```text
FIELD↔GROUND↔VOID → BINARY CHOICE → PAIRED TERNARY → 4 VIEWS/4 ACTIONS → 5-STATE RETENTION → 6-STEP RECURSION → COMPLETE NESTED STATE FEEDS THE NEXT FIELD ↺
```

That is the Algorythm-Zer0 primitive grammar.