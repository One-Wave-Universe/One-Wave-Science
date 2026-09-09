# Rules are rules… cause we’re fucking tools!

This is the working rulebook for the learning system.

When we hit a block, stop and write the rule out simple and straight, including exactly when to use it.

For every blocked rule, write:

- **Rule:** what you do.
- **When to use it:** what situation triggers it.
- **Why it works:** one plain sentence.
- **Example:** one clean example.
- **Don’t confuse it with:** the nearest similar rule.

No unexplained jumps. If a rule trips us up, stop and add it here until the logic is clean.

---

## Core decision path

1. **Balanced or unbalanced to solve?**
2. **Isolate the coefficients.**
3. **Remove matched pairs.**
4. **Double trouble.**

If blocked, identify which kind of problem it is before applying a move.

---

## 1. Balance rules

### Rule
Keep one existing equation true by making equal adjustments.

### When to use it
When you are changing one equation and want the equality to stay true.

### Moves
- Add the same amount to both sides.
- Subtract the same amount from both sides.
- Multiply both sides by the same amount.
- Divide both sides by the same nonzero amount.

### Why it works
Both sides change by the same amount or scale, so the equality is preserved.

### Don’t confuse it with
The comparison/gap rule below. That is not the same kind of move.

---

## 2. Match / remove rules

### Rule
If the same chunk appears in both places being compared, remove the matched chunk and compare what remains.

### When to use it
When both expressions contain an identical part that is blocking the useful comparison.

### Example
`4c + 2c` and `4c + 2s + 2t` both contain `4c`.

**Bye-bye 4c. Bye-bye 4c.**

### Why it works
The same part contributes the same amount in both places, so it cannot cause the difference between them.

---

## 3. Split a bigger chunk to expose a match

### Rule
Break a larger chunk into smaller parts that still add back to the same amount.

### When to use it
When a larger coefficient contains the exact smaller coefficient you need to match.

### Example
`6c = 4c + 2c`

### Why it works
Nothing changed in value; the same amount was only rewritten in a more useful shape.

---

## 4. Build / scale rules

### Rule
Scale a whole relationship to manufacture the shape you need.

### When to use it
When the target has more copies of a variable group than the relationship you already have.

### Example
If the target is `2s + 2t` and you have:

`2c + s + t = 12`

make two copies:

`4c + 2s + 2t = 24`

### Why it works
You are making the exact number of copies needed by the target.

### Mnemonic
**When in trouble, double the double.**

Do not double blindly. Double because the target needs doubles.

---

## 5. Isolation rules

### Rule
Remove whatever is attached to the target until the target is by itself.

### When to use it
When the exact thing you want is already present but has extra baggage attached.

### Example
From:

`4c + 2s + 2t = 24`

if the target is `2s + 2t`, the blocking part is `4c`.

### Why it works
You are separating the wanted part from the parts that are not part of the target.

---

## 6. Replacement rules

### Rule
If two things are known to be equal, either one can stand in for the other.

### When to use it
When a known relationship gives you a useful value or chunk already present elsewhere.

### Example
If:

`3c = 7`

then `3c` and `7` can replace each other wherever that exact chunk appears.

### Why it works
They are two names for the same amount.

---

## 7. Comparison / gap rule

### User name
**Targeted bullshit / imposed false symmetry.**

### Rule
When two separate totals do not match, measure the real gap between them and use that exact gap to build a comparison at the same total level.

### When to use it
When you have two different true relationships, their totals are different, and you need to relate the expressions directly.

### Example

`3c = 7`

`2c + s + t = 12`

The totals differ by:

`12 - 7 = 5`

So the 7-level can be raised to the 12-level with the real gap:

`7 + 5 = 12`

Since `3c = 7` and `2c + s + t = 12`:

`3c + 5 = 2c + s + t`

Remove the matched `2c`:

`c + 5 = s + t`

If the target is doubled:

`2s + 2t = 2c + 10`

### Why it works
The `+5` is not a random number. It is the exact measured gap between the two original totals.

### Important warning
This is **not** the normal balance rule where you do the same thing to both sides of one existing equation.

It is a new comparison built from two different true totals.

The imposed amount must be the real gap. No arbitrary fudge number.

### Concrete mental model
Two different things are priced differently. One totals 7 and one totals 12. If you want to put them on the same comparison level, the 7-side needs exactly 5 more.

That is the imposed symmetry.

---

## 8. Target-combination rule

### Rule
Solve the exact combination the problem asks for. Do not automatically solve every variable separately.

### When to use it
When the target is a bundle such as `s + t`, `2s + 2t`, or another combined subsystem.

### Example
If the problem asks for `2s + 2t`, you do not have to find `s` and `t` separately if the combined amount can be derived directly.

### Why it works
The combined relationship can be determined even when the individual values are unnecessary.

---

## 9. Check rules

Before accepting a move, ask:

- Am I preserving one existing equality, or building a new comparison?
- Did I change both sides when this was a balance move?
- If I used a gap, is it the real measured gap?
- Did I invent a number just to make things look equal?
- Did I remove only genuinely matched parts?
- Did I scale the whole relevant group?
- Did I build the exact target shape I need?
- Am I solving extra variables that the problem never asked for?

---

## Current worked pattern

Given:

`3c = 7`

`2c + s + t = 12`

Target:

`2s + 2t`

Direct comparison route:

1. Measure the gap: `12 - 7 = 5`.
2. Put the two expressions on the same total level: `3c + 5 = 2c + s + t`.
3. Remove matched `2c`.
4. `c + 5 = s + t`.
5. Target is doubled, so double the whole result.
6. `2c + 10 = 2s + 2t`.

Answer: `2c + 10`.

---

## Standing learning rule

If we hit a block, do not just repeat the algebra procedure.

Write out:

- the rule,
- exactly when it is used,
- what problem it solves,
- why the move is allowed,
- one concrete example,
- and what similar-looking rule it must not be confused with.
