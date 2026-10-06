# Learner App — Rough Draft Rules 001–002

> **STATUS: ROUGH DRAFT / LEARNER-CURRICULUM NOTES**
>
> This document captures the first teaching rules as they were discovered in conversation. It is intentionally concrete, visual, and concept-first. Wording, names, jokes, and sequencing are provisional.
>
> The parser/problem-builder in `Learner_App/` is deterministic infrastructure. This file is curriculum/teaching content and must not be mistaken for engine behavior.

---

## Core teaching law — math truth must be explainable

Do not teach a symbolic move as magic shorthand first.

For every move the learner should be able to answer:

1. **What changed?**
2. **Why is that move allowed?**
3. **What stayed true?**
4. **What cancelled or reduced, and to what identity?**
5. **When is this move not allowed?**

Do not stack extra abstraction, vocabulary, or notation just to make an explanation appear complete. Reduce to the smallest clear truth first, then compress into standard shorthand only after the learner understands what the shorthand is hiding.

Examples:

- Teach `x × 3` before compressing it to `3x`.
- Show `3 ÷ 3 = 1` and then `x × 1 = x` instead of saying the 3 simply "moves" or "disappears."
- Treat `=` as a truth claim that can be checked, not merely as "the answer comes next."

---

# Rule 001 — The Equal Sign Is a Mirror

## Learner-facing name

**M4 Rule 1 — Call bullshit where you see it.**

## Pattern

**IF you see `=` → THEN check both sides as a mirror claim.**

The `=` sign says:

> **The value on the left and the value on the right are the same.**

It does not mean "the answer comes next."

## Visual

```text
LEFT | = | RIGHT
  4  | = | 1 + 3
  4  | = |   4
```

The mirror matches, so the statement is true.

```text
LEFT | = | RIGHT
  5  | = | 2 + 4
  5  | = |   6
```

The mirror does not match, so the statement is false.

## Compressed learner rule

> **SEE `=` → MIRROR BOTH SIDES → IF THEY DO NOT MATCH, CALL BULLSHIT.**

## What it does

Gives the learner a concrete meaning for equality before equation-solving rules are introduced.

## Why it works

An equation is a statement that two expressions have equal value. If the two sides do not evaluate to the same value, the statement is false.

## Only when

Use this rule whenever `=` is being used as mathematical equality.

## Do not teach as

- "The answer is on the right."
- "Move stuff across the equals sign."
- "Just do the same trick the teacher did."

Those phrases may become shorthand later, but they are not the underlying reason.

## Three first checks

Ask only: **mirror match or bullshit?**

```text
5 = 2 + 3
4 + 1 = 6
7 = 10 - 3
```

The learner should judge the truth of the equality before solving for unknowns is introduced.

---

# Rule 002 — Equalateral Reduction to Solve

> **Working custom name.** `Equalateral Reduction to Solve` is learner-app terminology for preserving an equivalent equation while using inverse operations to isolate the unknown. The name is provisional and should not be confused with the geometry word `equilateral`.

## Purpose

**TO SOLVE:** clear away what is attached to the unknown without breaking the `=` mirror.

This "to solve" purpose is essential. The learner should know what the operation is accomplishing and why it is being used.

## Pattern

**IF an operation is attached to `x` → THEN use the inverse operation on both sides of the `=` mirror → reduce the inverse pair to its identity → continue until `x` is alone.**

Core inverse pairs:

```text
+  ↔  -
×  ↔  ÷
```

Core identities used in these first rules:

```text
n + (-n) = 0
n - n    = 0
n ÷ n    = 1       (for n ≠ 0)
x × 1    = x
x + 0    = x
```

## Why both sides?

The original equation is a truth claim. If only one side is changed, the original relationship is generally destroyed.

Example starting truth:

```text
x + 2 = 5
```

Do **not** simply erase `+2` from the left.

Instead, apply the matching inverse reduction to both sides:

```text
x + 2 = 5
    -2 = -2
-------------
x     = 3
```

The learner sees the reduction crossing the mirror as a matched operation.

Standard mathematics underneath the visual:

```text
(x + 2) - 2 = 5 - 2
x + 0       = 3
x           = 3
```

---

## Version A — Addition attached to x

### IF

Something is added to `x`.

### THEN

Subtract the same amount from both sides.

```text
x + 3 = 8
    -3 = -3
-------------
x     = 5
```

Expanded truth:

```text
(x + 3) - 3 = 8 - 3
x + 0       = 5
x           = 5
```

### What it does

Reduces the added amount to zero so the unknown is exposed.

---

## Version B — Subtraction attached to x

### IF

Something is subtracted from `x`.

### THEN

Add the same amount to both sides.

```text
x - 3 = 5
    +3 = +3
-------------
x     = 8
```

Expanded truth:

```text
(x - 3) + 3 = 5 + 3
x + 0       = 8
x           = 8
```

### What it does

Reduces the subtraction pair to zero so the unknown is exposed.

---

## Version C — Multiplication attached to x

### Teach the expanded form first

Before teaching `3x`, show what it means:

```text
x × 3 = 12
```

Then divide the whole left expression and the right side by 3:

```text
x × 3 = 12
    ÷3 = ÷3
-------------
x × 1 = 4
x     = 4
```

The important visible chain is:

```text
x × 3 ÷ 3
    ↓
x × 1
    ↓
x
```

Nothing disappeared by magic.

```text
3 ÷ 3 = 1
x × 1 = x
```

Only after this is understood should the app compress:

```text
x × 3
```

into standard shorthand such as:

```text
3x
```

### IF

`x` is multiplied by a nonzero number.

### THEN

Divide both sides by that same number.

### What it does

Reduces the multiplier to `1`, leaving `x × 1`, which is just `x`.

---

## Version D — Division attached to x

### IF

`x` is divided by a nonzero number.

### THEN

Multiply both sides by that same number.

```text
x ÷ 3 = 4
    ×3 = ×3
-------------
x     = 12
```

Expanded truth:

```text
(x ÷ 3) × 3 = 4 × 3
x × 1       = 12
x           = 12
```

### What it does

Reduces the divisor relationship back to the multiplicative identity `1` so the unknown is exposed.

---

## The naked-x teaching moment

Optional playful learner copy after Version C:

```text
x × 3 = 12
    ÷3 = ÷3
-------------
x × 1 = 4
x     = 4
```

The coefficient/multiplier is gone because it was reduced to `1`, not because it vanished.

Possible visual joke:

> Naked `x`, multiplier stripped away, staring through the `=` mirror at `4`:
>
> **"Am I an X... or am I a 4?"**
>
> **DUALITY IS REALITY**

The joke is optional. The mathematical point is not:

- `x` is the unknown symbol.
- `4` is the value that makes the original equation true.
- `x = 4` does **not** mean the symbols `x` and `4` are the same kind of thing; it means the value represented by `x` is 4 in this equation.

---

## Field / Void metaphor — optional teaching layer

The learner may describe an inverse pair as a `field` and its `void`:

```text
+2  with  -2  →  0
×3  with  ÷3  →  ×1
```

If this language is used, the app must also show the standard mathematical meaning:

- `-2` is the **additive inverse** of `+2`.
- dividing by `3` reverses multiplication by `3` for nonzero `3`.
- the inverse is not a hidden term secretly present in the written equation; it is an operation we are allowed to apply while preserving equivalence when we apply it to both sides.

The metaphor may help memory. It must never replace the mathematics.

---

# Teaching order for the first session

Do not dump all vocabulary at once.

```text
1. `=` means mirror / same value.
2. Three easy mirror-match checks.
3. Introduce the goal: TO SOLVE = expose the unknown without breaking the mirror.
4. `x + n` → subtract n from both sides.
5. `x - n` → add n to both sides.
6. `x × n` → divide both sides by n; visibly pass through `x × 1`.
7. `x ÷ n` → multiply both sides by n.
8. Only then introduce compressed notation such as `3x` and vocabulary such as coefficient.
```

The learner should not advance merely because an answer was entered correctly. The learner should be able to explain the move.

---

# Draft problem-linking behavior

Every generated learner problem should be able to link to the exact rule(s) needed without revealing that problem's answer.

For example:

```text
Problem: x + 7 = 11
Reference: Rule 001 — The Equal Sign Is a Mirror
Reference: Rule 002A — Addition attached to x
Example: use a different numeric example, not the current answer
```

The reference system should provide:

- recognizable pattern
- action
- what it does
- why it works
- only-when condition
- do-not-use-when condition
- worked example using different numbers
- prerequisite rules
- related/inverse rule

---

# Open questions / not final yet

- Final spelling/name for `Equalateral Reduction to Solve`.
- Whether `Call bullshit where you see it` is default learner copy, optional tone pack, or internal design language.
- Exact visual design of the `=` mirror gate.
- Exact wording of `field/void` metaphor and whether it ships in the default curriculum.
- Number of successful explanation/reasoning checks required before progression.
- How the six-step recursive flashcard system revisits Rules 001 and 002 while later rules are being learned.

---

## Hard stop for this draft

This document intentionally stops after the first two conceptual rules. Do not add coefficients, distribution, fractions, systems of equations, or later algebra rules until Rules 001 and 002 are reviewed and stabilized.
