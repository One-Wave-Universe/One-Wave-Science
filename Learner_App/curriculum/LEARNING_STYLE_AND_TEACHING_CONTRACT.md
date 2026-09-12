# Learner App — Learning Style and Teaching Contract

> **Purpose:** This file defines how the math learner must teach. It is not a math rule list and it is not a flash-card specification.
>
> The app should treat this as a teaching contract: if a lesson is technically correct but violates this teaching order, the lesson is still wrong for this learner.

---

## Core learning style

The learner is **logic-first, structure-first, then symbols**.

The learner does not reliably learn from:

> "Here is the rule. Apply it because that is the rule."

The learner needs to understand the structure underneath the rule before the symbolic shortcut becomes useful.

The teaching order is:

```text
concrete situation
    ↓
what is actually true
    ↓
what changed / what stayed the same
    ↓
why a move is legal
    ↓
perform one move
    ↓
verify that the relationship is still true
    ↓
only then compress it into a rule or shorthand
```

A symbolic procedure must be the compressed form of understood logic, not a substitute for understood logic.

---

# Teaching laws

## 1. Concrete before abstract

Do not begin with vocabulary such as coefficient, inverse operation, elimination, distribution, or substitution when the learner does not yet understand the thing the word describes.

Start with something the learner can track directly.

Example:

Instead of beginning with:

> "Subtract 3 from both sides to isolate the variable."

first establish:

```text
x + 3 = 8
```

The left side contains an unknown amount plus 3. The right side says that whole amount is worth 8.

If the goal is to find the unknown part, the attached 3 has to be removed. But the equation is claiming the two whole sides have the same value. Removing 3 from only one side would change that claim. Therefore remove 3 from both whole sides.

Only after that logic is clear should the lesson compress the move into:

> "Subtract 3 from both sides."

---

## 2. Cause before procedure

Every move must answer **why this move is being made** before asking the learner to repeat it.

Bad teaching:

> "Move the 3 over and change the sign."

Required teaching:

> "The 3 is attached to the unknown by addition. We want to expose the unknown. Subtracting 3 cancels that attachment. We perform the same subtraction on the other side so the equality remains true."

The learner should never be expected to trust a unexplained transformation merely because it produces the correct answer.

---

## 3. Every rule needs a trigger

A rule must be written as a usable condition, not as a vague slogan.

Required form:

```text
IF this situation is present
THEN this move is allowed
BECAUSE this relationship makes it valid
DO NOT use it when these conditions are not true
```

Example:

```text
IF the same added amount is attached to the unknown
AND the goal is to remove that added amount,
THEN subtract that amount from both sides,
BECAUSE the subtraction cancels the attachment while equal treatment preserves equality.
```

Rules must say exactly when they apply and when they do not.

---

## 4. No magic numbers

A number must never appear in a solution without an origin.

If the learner sees `+5`, `×2`, `÷3`, or any other operation, the lesson must be able to answer:

- Where did that number come from?
- What relationship made it useful?
- Why is that operation legal here?
- What does the operation accomplish?

Do not introduce a convenient number and explain it afterward. Derive it from the visible structure first.

---

## 5. One move at a time

Do not stack several algebra transformations into one line while the learner is still building the logic.

For each move:

```text
1. identify the structure
2. choose one legal move
3. perform it
4. show what cancelled, reduced, matched, or changed
5. verify that the mathematical relationship is still true
6. continue
```

If the learner becomes confused, return to the last line whose logic was completely clear. Do not pile more notation on top of the confusion.

---

## 6. Comparison is a primary reasoning tool

Teach the learner to notice:

- what both expressions share
- what is extra
- what changed
- what stayed fixed
- what can be paired
- what difference remains after matching parts are removed

Example with shared terms:

```text
4c + something
6c + something
```

Do not merely announce that `6c - 4c = 2c`.

First expose the structure:

```text
6c = 4c + 2c
```

Now the learner can see the common `4c` and the extra `2c`.

The symbolic subtraction is then a compressed description of that comparison.

---

## 7. Shortcuts come after understanding

Standard algebra shortcuts are allowed only after the underlying action is understood.

Examples:

- show `x × 3` before relying on `3x`
- show `3 ÷ 3 = 1` and `x × 1 = x` before saying a multiplier "goes away"
- show why both sides are changed before using "do the same thing to both sides" as a memorized phrase
- show matched structure before using cancellation notation

The goal is eventually to make the learner fast. Speed comes from compression **after** understanding, not from skipping understanding.

---

## 8. Correct answers are not enough

A learner can guess correctly or copy a procedure without understanding it.

Before treating a rule as learned, the app should sometimes ask for reasoning checks such as:

- What are you trying to remove or expose?
- Why can this operation be used here?
- Why must the other side change too?
- What became `0` or `1`?
- What stayed true after the move?
- Where did this number come from?

The app should distinguish **answer correctness** from **logic understanding**.

---

## 9. Mistakes diagnose missing logic

Repeated errors should not automatically produce more copies of the same problem.

If the learner misses the same kind of move repeatedly, identify the missing logical step and reduce the lesson to that step.

Examples:

```text
wrong sign repeatedly
→ check whether inverse/cancellation is understood

random multiplier repeatedly
→ check whether the source of the multiplier is understood

changes only one side
→ return to what `=` claims before continuing

confusion over 6c and 4c
→ expand 6c as 4c + 2c and compare the matched portion
```

The app should repair the missing concept rather than punish the learner with repetition.

---

# Required lesson shape

A new math rule should normally be taught in this order:

```text
1. Situation
   What are we looking at?

2. Truth
   What is already true before we touch anything?

3. Goal
   What are we trying to expose, compare, remove, or find?

4. Structure
   What matches? What differs? What is attached to what?

5. Legal move
   What single change can we make?

6. Reason
   Why is that change mathematically valid?

7. Visible result
   What cancelled, reduced, split, combined, or remained?

8. Verification
   Did the mathematical relationship stay true?

9. Compression
   What short rule or standard notation describes what we just understood?

10. Boundary
    When must this rule NOT be used?
```

Do not skip directly from Situation to Compression.

---

# Problem progression

New work should sit just above the learner's demonstrated understanding rather than jumping ahead because a curriculum sequence says it is time.

Problems should reuse earlier logic while adding one new piece at a time.

A problem may reference the exact rules needed, but the reference must not reveal the answer to the current problem.

The learner should be able to open a rule reference and get:

```text
pattern / trigger
why it works
one legal move
what the move accomplishes
when not to use it
a worked example using different values
prerequisite rules
related rules
```

If the learner is not moving smoothly through material that should already be understood, treat that as a signal to improve the explanation or locate the missing prerequisite.

---

# Language rules

Prefer direct language tied to visible structure.

Useful language includes:

- attached to
- matching part
- extra part
- same value
- remove the matched pair
- split this so we can see what is shared
- expose the unknown
- this changed
- this stayed true
- this number came from...

Avoid unexplained phrases such as:

- move it across
- flip the sign
- just cancel it
- bring it over
- because that is the formula
- this is the rule, memorize it

Those phrases may be used later as compression only when the learner already knows the full logic they stand for.

---

# Hard boundary: logic learner vs. flash cards

**Do not mix the math-logic curriculum with the flash-card system.**

They serve different jobs.

```text
Math logic learner
= build understanding
= explain structure
= derive rules
= reason through legal moves
= diagnose conceptual gaps

Flash-card system
= recall
= repetition
= speed
= automatic retrieval of already-understood facts
```

Flash cards must not be used to paper over a concept the learner does not understand.

The math learner must work without the flash-card subsystem. The flash-card subsystem may later practice facts that have already been understood, but it is not part of the explanation, rule sequence, or conceptual progression defined here.

Do not add flash-card cadence, recursion, multiplication-table scheduling, or recall drills to curriculum rule files.

---

# Definition of a good lesson for this learner

A lesson is successful when the learner can look at a new problem and say, in their own words:

```text
I see what is happening.
I know what I am trying to find.
I know which parts matter.
I know why this move is allowed.
I know what the move changes.
I know what it does not change.
I can check whether I broke the relationship.
```

Only then should the app try to make the process faster or more compact.
