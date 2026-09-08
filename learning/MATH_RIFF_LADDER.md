# Math Riff Ladder

## Purpose

Learn math the way a guitarist gets better: keep one riff just above the current skill level, repeat it until it stops feeling impossible, then raise the difficulty a little. New work should keep pulling older rules back in so nothing is learned once and abandoned.

The goal is not to memorize disconnected rules. The goal is to understand what each rule means, recognize when it applies, and reuse it inside harder problems.

---

# Problem-reference standard

**Every practice problem in this repo must include a `Uses:` line linking directly to every rule needed to solve it.**

Example:

`2s + 10 = 2t`

**Uses:** [5.2 Coefficients](#52-a-coefficient-means-multiplication) · [6 Balance rule](#level-6--the-balance-rule-for-equations) · [9 Equivalent equations](#level-9--equivalent-equations)

For mixed problems, list all important earlier rules too. The learner should never have to guess which rule a problem is testing.

If a new problem needs a rule that is not in this file yet, **add the rule first, then link the problem to it.**

---

## The learning loop

1. **Understand the idea first.** Know what the symbols and operations are actually doing.
2. **Play the current riff.** Work problems that are difficult enough to require attention but not so hard that every step is unfamiliar.
3. **Repeat with small changes.** Change numbers, signs, or one operation at a time.
4. **Mix in an older rule.** Every new skill should reuse something already learned.
5. **Explain why it works.** If the explanation is only “because that is the rule,” the idea is not finished yet.
6. **Raise the difficulty one notch.** Do not jump five levels at once.
7. **Return later.** Earlier rules come back inside new problems so recall gets stronger instead of fading.

A useful practice ratio is roughly:

- 60% current skill
- 25% older skills mixed back in
- 15% problems just above the current level

---

# Level 0 — Number sense

Before algebra, numbers themselves need to feel solid.

## 0.1 Numbers represent amounts or positions

A number can describe how much of something there is, or where something sits on a number line.

## 0.2 Zero

`0` means no amount or the reference point between positive and negative values.

## 0.3 Positive and negative numbers

Positive and negative values are opposite directions from zero.

Example:

`3 + (-3) = 0`

**Uses:** [0.2 Zero](#02-zero) · [0.3 Positive and negative numbers](#03-positive-and-negative-numbers) · [1.5 Adding opposites cancels](#15-adding-opposites-cancels)

## 0.4 Equal means same value

`=` does **not** mean “the answer comes next.” It means the value on the left is the same as the value on the right.

That idea becomes the foundation of equations and balance problems.

---

# Level 1 — Addition and subtraction

## 1.1 Addition combines change

Problem:

`3 + 2 = ?`

**Uses:** [1.1 Addition combines change](#11-addition-combines-change)

Answer: `5`

## 1.2 Subtraction reverses addition

Problem:

`5 - 2 = ?`

**Uses:** [1.2 Subtraction reverses addition](#12-subtraction-reverses-addition)

Answer: `3`

## 1.3 Addition and subtraction are inverse operations

They undo each other.

If `3 + 4 = 7`, then `7 - 4 = 3`.

## 1.4 Adding zero changes nothing

`a + 0 = a`

## 1.5 Adding opposites cancels

`a + (-a) = 0`

---

# Level 2 — Multiplication and division

## 2.1 Multiplication is repeated scaling

Problem:

`3 × 4 = ?`

**Uses:** [2.1 Multiplication is repeated scaling](#21-multiplication-is-repeated-scaling)

Answer: `12`

## 2.2 Multiplication by 1 changes nothing

`a × 1 = a`

## 2.3 Multiplication by 0 produces zero

`a × 0 = 0`

## 2.4 Division undoes multiplication

If `3 × 4 = 12`, then `12 ÷ 3 = 4` and `12 ÷ 4 = 3`.

## 2.5 Multiplication and division change scale

Multiplying by 2 doubles a value. Dividing by 2 cuts the value into two equal parts.

---

# Level 3 — Order of operations

Use this order:

1. Parentheses
2. Exponents
3. Multiplication and division, left to right
4. Addition and subtraction, left to right

Problem:

`2 + 3 × 4 = ?`

**Uses:** [1.1 Addition](#11-addition-combines-change) · [2.1 Multiplication](#21-multiplication-is-repeated-scaling) · [3 Order of operations](#level-3--order-of-operations)

Answer: `14`

The point of the rule is a shared notation system that removes ambiguity.

---

# Level 4 — Fractions

## 4.1 A fraction is division

`3/4` means `3 ÷ 4`.

The bottom number tells how many equal parts make the whole. The top number tells how many of those parts are being counted.

## 4.2 Equivalent fractions represent the same amount

`1/2 = 2/4 = 3/6`

Multiplying or dividing the top and bottom by the same nonzero number changes the writing but not the value.

## 4.3 Multiplying fractions

Problem:

`2/3 × 4/5 = ?`

**Uses:** [2.1 Multiplication](#21-multiplication-is-repeated-scaling) · [4.1 Fractions are division](#41-a-fraction-is-division) · [4.3 Multiplying fractions](#43-multiplying-fractions)

Answer: `8/15`

## 4.4 Dividing fractions

Dividing by a fraction asks how many of that fractional size fit into the first quantity.

`a/b ÷ c/d = a/b × d/c`

The meaning should come before the shortcut.

## 4.5 Adding fractions requires matching-sized pieces

You cannot directly add thirds and fifths because the pieces are different sizes. First rewrite them using a common denominator.

---

# Level 5 — Variables

## 5.1 A variable is a number whose value is not yet known or is allowed to change

`x`, `y`, `s`, and `t` are placeholders for values.

## 5.2 A coefficient means multiplication

`2x` means `2 × x`.

## 5.3 Like terms have matching variable parts

Problem:

`2x + 3x = ?`

**Uses:** [1.1 Addition](#11-addition-combines-change) · [5.2 Coefficients](#52-a-coefficient-means-multiplication) · [5.3 Like terms](#53-like-terms-have-matching-variable-parts)

Answer: `5x`

`2x + 3y` cannot normally be combined because `x` and `y` may represent different values.

---

# Level 6 — The balance rule for equations

If two sides are equal, performing the **same valid operation to both sides** keeps them equal.

## 6.1 Whatever you add to one side, add to the other

## 6.2 Whatever you subtract from one side, subtract from the other

## 6.3 Whatever you multiply one entire side by, multiply the other entire side by

## 6.4 Whatever you divide one entire side by, divide the other entire side by

Division by zero is never allowed.

Problem:

`x + 3 = 8`

**Uses:** [0.4 Equal means same value](#04-equal-means-same-value) · [1.2 Subtraction](#12-subtraction-reverses-addition) · [1.3 Inverse operations](#13-addition-and-subtraction-are-inverse-operations) · [6.2 Balance by subtraction](#62-whatever-you-subtract-from-one-side-subtract-from-the-other)

Solution: subtract 3 from both sides, giving `x = 5`.

---

# Level 7 — Undo operations in reverse order

To isolate a variable, reverse the operations that were applied to it.

Problem:

`2x + 6 = 14`

**Uses:** [1.2 Subtraction](#12-subtraction-reverses-addition) · [2.4 Division undoes multiplication](#24-division-undoes-multiplication) · [5.2 Coefficients](#52-a-coefficient-means-multiplication) · [6 Balance rule](#level-6--the-balance-rule-for-equations) · [7 Reverse-order undoing](#level-7--undo-operations-in-reverse-order)

Solution:

1. subtract 6 from both sides → `2x = 8`
2. divide both sides by 2 → `x = 4`

---

# Level 8 — Distributive property

Multiplication outside parentheses applies to every term inside.

`a(b + c) = ab + ac`

Problem:

`2(x + 3) = ?`

**Uses:** [1.1 Addition](#11-addition-combines-change) · [2.1 Multiplication](#21-multiplication-is-repeated-scaling) · [5.2 Coefficients](#52-a-coefficient-means-multiplication) · [8 Distributive property](#level-8--distributive-property)

Answer: `2x + 6`

The reverse direction is factoring: `2x + 6 = 2(x + 3)`.

---

# Level 9 — Equivalent equations

An equation can be rewritten into a different-looking equation that describes the same relationship.

Problem:

`2s + 10 = 2t`

**Uses:** [0.4 Equality](#04-equal-means-same-value) · [2.5 Scale](#25-multiplication-and-division-change-scale) · [5.2 Coefficients](#52-a-coefficient-means-multiplication) · [6.4 Balance by division](#64-whatever-you-divide-one-entire-side-by-divide-the-other-entire-side-by) · [9 Equivalent equations](#level-9--equivalent-equations)

Divide every term by 2:

`s + 5 = t`

Equivalent limited-tile form:

`s + 6 = t + 1`

**Uses:** [1.2 Subtraction](#12-subtraction-reverses-addition) · [6.2 Balance by subtraction](#62-whatever-you-subtract-from-one-side-subtract-from-the-other) · [9 Equivalent equations](#level-9--equivalent-equations)

Subtracting 1 from both sides returns `s + 5 = t`.

---

# Level 10 — Negative numbers and signs in algebra

## 10.1 Subtracting is adding the opposite

`a - b = a + (-b)`

## 10.2 Negative times positive is negative

`(-a)(b) = -ab`

## 10.3 Negative times negative is positive

`(-a)(-b) = ab`

One negative reverses direction; a second reversal restores the original direction.

---

# Level 11 — Exponents and roots

## 11.1 Exponents mean repeated multiplication

`x² = x × x`

`x³ = x × x × x`

## 11.2 Square roots undo squaring

Problem:

`x² = 25`

**Uses:** [2.1 Multiplication](#21-multiplication-is-repeated-scaling) · [10.3 Negative times negative](#103-negative-times-negative-is-positive) · [11.1 Exponents](#111-exponents-mean-repeated-multiplication) · [11.2 Square roots](#112-square-roots-undo-squaring)

Answer: `x = 5` or `x = -5`.

---

# Level 12 — Coordinates and graphs

A coordinate `(x, y)` gives two pieces of positional information.

- `x` controls horizontal position.
- `y` controls vertical position.

Problem:

Find four points satisfying `x + y = 7`.

**Uses:** [1.1 Addition](#11-addition-combines-change) · [5.1 Variables](#51-a-variable-is-a-number-whose-value-is-not-yet-known-or-is-allowed-to-change) · [6 Balance rule](#level-6--the-balance-rule-for-equations) · [12 Coordinates and graphs](#level-12--coordinates-and-graphs)

Answers include `(0,7)`, `(1,6)`, `(2,5)`, `(3,4)`.

---

# Level 13 — Ratios, rates, and proportions

A ratio compares quantities.

`2:3`

A proportion says two ratios describe the same relationship.

`2/3 = 4/6`

Rates are ratios involving different units, such as miles per hour or beats per minute.

---

# Level 14 — Slope and change

Slope measures how one quantity changes relative to another.

`slope = change in y / change in x`

or

`m = Δy / Δx`

This is the beginning of thinking about motion, trends, waves, rates, and eventually calculus.

---

# Level 15 — Systems of equations

Two equations can constrain the same variables at once.

Problem:

`x + y = 7`

`x - y = 1`

**Uses:** [1.1 Addition](#11-addition-combines-change) · [1.2 Subtraction](#12-subtraction-reverses-addition) · [5.1 Variables](#51-a-variable-is-a-number-whose-value-is-not-yet-known-or-is-allowed-to-change) · [6 Balance rule](#level-6--the-balance-rule-for-equations) · [9 Equivalent equations](#level-9--equivalent-equations) · [15 Systems](#level-15--systems-of-equations)

The solution must satisfy **both** equations. Methods such as substitution and elimination find the intersection of those constraints.

---

# Level 16 — The next riffs

After the beginning rules are solid, move into:

- inequalities
- absolute value
- powers and exponent laws
- radicals
- linear functions
- systems
- quadratics
- geometry
- trigonometry
- vectors
- probability
- complex numbers
- logarithms
- limits
- derivatives
- integrals
- differential equations
- linear algebra

Do not treat these as a race. Each new topic should reuse earlier rules.

---

# Spiral practice plan

Every practice block contains three layers.

## A. Warm-up: old riffs

Use 2–4 short problems from earlier material.

## B. Main riff: current skill

Spend most of the session on the concept currently being learned.

## C. Stretch riff: one step harder

Finish with one or two problems combining the current rule with earlier ones.

### Riff 1

`x + 3 = 8`

**Uses:** [1.2 Subtraction](#12-subtraction-reverses-addition) · [6.2 Balance by subtraction](#62-whatever-you-subtract-from-one-side-subtract-from-the-other)

### Riff 2

`2x = 10`

**Uses:** [2.4 Division](#24-division-undoes-multiplication) · [5.2 Coefficients](#52-a-coefficient-means-multiplication) · [6.4 Balance by division](#64-whatever-you-divide-one-entire-side-by-divide-the-other-entire-side-by)

### Riff 3

`2x + 3 = 13`

**Uses:** [1.2 Subtraction](#12-subtraction-reverses-addition) · [2.4 Division](#24-division-undoes-multiplication) · [5.2 Coefficients](#52-a-coefficient-means-multiplication) · [6 Balance rule](#level-6--the-balance-rule-for-equations) · [7 Reverse-order undoing](#level-7--undo-operations-in-reverse-order)

### Riff 4

`2(x + 3) = 14`

**Uses:** [2.4 Division](#24-division-undoes-multiplication) · [6 Balance rule](#level-6--the-balance-rule-for-equations) · [7 Reverse-order undoing](#level-7--undo-operations-in-reverse-order) · [8 Distribution](#level-8--distributive-property)

### Riff 5

`2(x + 3) - 4 = 14`

**Uses:** [1.1 Addition](#11-addition-combines-change) · [1.2 Subtraction](#12-subtraction-reverses-addition) · [2.4 Division](#24-division-undoes-multiplication) · [6 Balance rule](#level-6--the-balance-rule-for-equations) · [7 Reverse-order undoing](#level-7--undo-operations-in-reverse-order) · [8 Distribution](#level-8--distributive-property)

### Riff 6

Solve a two-equation system containing the operations above.

**Uses:** [6 Balance rule](#level-6--the-balance-rule-for-equations) · [7 Reverse-order undoing](#level-7--undo-operations-in-reverse-order) · [8 Distribution](#level-8--distributive-property) · [9 Equivalent equations](#level-9--equivalent-equations) · [15 Systems](#level-15--systems-of-equations)

The difficulty rises, but the old material never disappears.

---

# Rule for getting stuck

When a problem suddenly feels impossible, find the **first step that stopped making sense**. Drop back exactly one layer and rebuild that piece.

- If adding fractions fails, return to [4.1 Fractions](#41-a-fraction-is-division) and [4.5 Common denominators](#45-adding-fractions-requires-matching-sized-pieces).
- If solving equations fails, return to [0.4 Equality](#04-equal-means-same-value), [1.3 Inverse operations](#13-addition-and-subtraction-are-inverse-operations), and [6 Balance](#level-6--the-balance-rule-for-equations).
- If distribution fails, return to [2.1 Multiplication](#21-multiplication-is-repeated-scaling) before [8 Distribution](#level-8--distributive-property).
- If elimination fails, return to [6 Balance](#level-6--the-balance-rule-for-equations), [9 Equivalent equations](#level-9--equivalent-equations), then [15 Systems](#level-15--systems-of-equations).

Do not restart all of mathematics. Repair the missing connection, then return to the riff.

---

# Master rule

> **New math should be old math arranged in a slightly harder pattern.**

Keep the challenge just above the current skill level, repeat until the pattern becomes recognizable, then expand it. Keep earlier rules alive by pulling them into newer problems again and again.
