# Musical Universe — Chapter 2
# A Chord Is an Asymmetric Lean

**Status:** GRAY/YELLOW presentation draft  
**Does not promote:** E-511, E-512, E-513  
**Source nodes:** E-510, E-511, E-512, E-513, B-203, B-204, B-205, B-224  
**Depends on:** Ch1 address law (pyramid + Express/Compress). Tritone still banned as organizer.  
**Format:** Musical Universe Format Lock, 2026-09-08 (Mirror lock)

---

## Gray

Western theory calls a stack of simultaneous pitches a chord. It names qualities (major, minor, power, seventh) by which stickers sit how far from a chosen root.

E-511 already wrote the Gray procedure, then translated it:

1. Select the set.  
2. Move the chosen root to `(0)`.  
3. Read the other tones as signed positions on the E-510 clock.  
4. That signed pair is the Oscillation Window (E-512).

Two checked Gray data points (A as root, values corrected against E-510 — original build had sign and side backwards):

| Gray name | Window `(P_compress, P_expr)` |
|---|---|
| A major | `(-5, +4)` |
| A minor | `(-5, +3)` |

The fifth sits at −5 both times. The third moves: +4 major, +3 minor. One side holds, one side shifts. Two points only. Not a law.

Gray also uses “lean” for tonic / subdominant / dominant inside a key. That is E-514’s job. **This chapter does not mean that.** E-513 said so first. Do not merge the two leans.

## 2D

After Ch1, a tone is not a letter. It is a pyramid plus a polarity.

A “chord” in this lane is **more than one address sounding at once**, then re-centered so one address sits on `(0)`.

Re-center is not a new particle. It is E-511: pick a root wall, slide that wall to hold, read everyone else as signed pull.

```
root at (0)
compress side  <——  (0)  ——>  express side
```

If the two sides are equal in magnitude, the set is balanced. That is rare and it is a result, not a virtue.

If they are not equal, the set **leans**. That lean *is* the chord.

## 3D

Face sheet = Expression pulls (positive positions after re-center).  
Flip sheet = Compression pulls (negative positions after re-center).  
Mirror still only flips a wall. It does not invent a third sheet for “harmony.”

A triad in Gray is usually one compress-side neighbor plus one express-side neighbor around the held root. In One Wave that is: hold one pyramid’s rest, feel two off-center walls, one each side. The imbalance between those pulls is the lean.

Power set (root + one side only) has **no opposite pull to sum against**. E-513 marks that UNDEFINED, not “mysterious forward flip.” We keep the scope boundary. Do not force an answer.

## Mathematics

Window, from E-512, after E-511 re-center:

$$
W = (P_{-},\, P_{+})
$$

Lean, from E-513, generalized past a single pair:

$$
L = \sum |P_{i}<0| \;-\; \sum |P_{j}>0|
$$

$$
\begin{cases}
L > 0 & \text{backward lean — Compression dominates} \\
L < 0 & \text{forward lean — Expression dominates} \\
L = 0 & \text{no lean — balanced window}
\end{cases}
$$

Checked on the only two receipts the nodes own:

$$
L(\text{A major}) = |-5| - |4| = 1
$$

$$
L(\text{A minor}) = |-5| - |3| = 2
$$

Both lean backward. Minor leans harder *on this root, these two sets*. Pattern unconfirmed elsewhere.

Live choice under the hold:

$$
-1\;(0)\;+1
$$

A chord is what happens when more than one signed position is alive at once and `(0)` is busy being the root. Asymmetry is the information. Symmetry would be a rest that forgot it invited company.

Do not import Gray interval names into \(L\). Positions are signed clock steps after re-center, not “thirds” and “fifths” as identity.

## Predictions (kickable)

P1. **Re-center invariance.** Same set, different chosen root, must produce a different window. If \(L\) is identical for every chosen `(0)`, the operator is not E-511.

P2. **Two-point honesty.** Until a third quality (diminished, seventh, other root) is run through the same clock, “minor leans harder than major” stays a rumor with two friends.

P3. **Power set stays UNDEFINED.** Root + one side only shall not be assigned \(L\) by sneaking a fake opposite. Write a new definition or keep the gap.

P4. **Name collision.** If a sentence uses lean as E-514 key-function and E-513 window-asymmetry in the same breath without tags, burn it.

P5. **Receipt.** Commanded addresses + chosen root + computed \(W\) + computed \(L\) in one CSV. Ear-feel is not a receipt.

## Yellow Audit

| Claim | Gate | Status |
|---|---|---|
| Re-center operator | E-511 YELLOW | Informal A major / A minor only |
| Window as signed pair | E-512 YELLOW | Two data points |
| \(L\) as side-sum asymmetry | E-513 YELLOW | Matches those two points |
| Minor always leans harder | unconfirmed | One comparison |
| Power-set lean | UNDEFINED | Scope boundary |
| Lean ≠ E-514 function | locked | Two words, two nodes |
| Tritone-as-chord-color | rejected | Gray, not an ID |

Chapter cannot climb above E-513. Pretty voicings do not Bronze a sum.

## Future Work

1. Run \(L\) on one more quality and one more root before writing Chapter 3.  
2. Define a window for two-address sets without faking a missing side.  
3. Decide whether windows track across a sequence (progression) or only per hold.  
4. Confirm zero relationship to B-208 Threshold Windows except the English word.  
5. Bench: pick P1 as `(0)`, sound E2 and C6 (or whatever the clock maps), print \(W\) and \(L\).

## Closing Thoughts

A chord is not a stack. It is a hold with uneven arms. One side pulls harder. That bias is the lean. Balance is allowed. It is just quieter, and it is not what most of the Gray names were pointing at.

## Score Stave

Operator chain:

`E-510 clock → E-511 re-center to (0) → E-512 window (P−, P+) → E-513 L`

Worked (Gray stickers, two points only):

- A major → \(W=(-5,+4)\) → \(L=1\) backward  
- A minor → \(W=(-5,+3)\) → \(L=2\) backward  

Address reminder from Ch1: E# / C# are polarity on one pyramid. After re-center they become signed positions around hold. Still one wave. Still no devil interval running the show.
