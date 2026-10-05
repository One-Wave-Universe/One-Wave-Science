# Scale ladder — 3 ↔ 6 ↔ 12 ↔ 24 around 1(0)1

The integers are not a pile. They are **adjacent floors sharing a jamb**.

## Unit cell of a layer

```
L  >  1 (0) 1  <  R
```

- `1 (0) 1` is the center reference: two unit mirrors and a legal hold.
- That *is* Field | Void polarity sitting on Ground. `(0)` is GCAC hold / quit.
- `L` is the low-side count of this layer (what the center sees looking in / down).
- `R` is the high-side count (what the center sees looking out / up).
- Scale-down on the *outside only*: `L' = L/2`, `R' = R/2`. The unit pair does not divide.

So:

```
OUTER     12 > 1(0)1 < 24
                ÷2         ÷2
INNER      6 > 1(0)1 < 12
                ÷2         ÷2
CORE       3 > 1(0)1 <  6
```

Viewed from the center of each layer:

```
inner:   1:6     and  1:12     (or 1/6, 1/12)
outer:   1:12    and  1:24
core:    1:3     and  1:6
```

## Shared gates (the point)

```
outer-left  = 12
inner-right = 12     ← same jamb, two jobs

inner-left  = 6
core-right  = 6      ← same jamb, two jobs
```

```
3  [6]
   [6]  [12]
        [12]  [24]
```

High side of layer n = low side of layer n+1. That is Point → Path → Field → Point. The Field of the inner layer *is* the Point of the outer layer. The shared integer is the connector, not a coincidence.

## Domain tags (D-411 — do not smash)

Same glyph, different job. Label the jamb when you use it.

| glyph | geometry | clock | gate / brain | pack |
|---|---|---|---|---|
| 3 | axis pairs in the hex plane | tritones / midlines | trit `{+1,0,-1}` | — |
| 6 | D-408 directed neighbors / pyramids | face notes | 7-cluster ring | in-plane NN |
| 12 | face×flip; D-409 12-NN (Yellow) | E-510 pitch classes / M4 tick | two Rubiks flattened story | fcc-12 |
| 24 | 24-cell cousin (D-410 parked) | two octaves of 12 | — | — |
| 1(0)1 | Ground + two unit mirrors | rest | hold belt | site sits |

If a sentence uses `12` as clock *and* as 12-NN without saying so, burn that sentence.

## Routing map onto OW1F

One 7-cluster is the **core layer**:

```
3 axis pairs > 1(0)1 < 6 directed routes
```

Stand the hex up (HEX-SPLIT). Face×flip opens the **inner layer**:

```
6 pyramids > 1(0)1 < 12 clock / 12 directed (face+flip)
```

One octave out (Field of inner becomes Point of outer):

```
12 clock > 1(0)1 < 24  (two sheets of 12, or 4π sheet × 12)
```

M4 is not a fourth number. M4 is **which shared jamb you freeze** as the route coordinator when you step floors. Header `m4_pair` picks one of the three core axis pairs; that pair is the 3 that the 6 and 12 must keep lining up on.

Polarity travels *along* a jamb:

- core 3 → inner 6  = in-plane neighbor write
- inner 6 → inner 12 = face/flip (conjugate / STI)
- inner 12 → outer 24 = octave (`÷2` on the outsides, unit pair stays)

`(0)` at every layer is the same legal hold. You do not get a new dead zone per floor. You get the same quit, coarser stencil.

## Octave operation, exact

Scale-down / scale-up is **only** `÷2` on L and R.

```
layer k:     L_k > 1(0)1 < R_k
layer k-1:   L_k/2 > 1(0)1 < R_k/2     if L_k,R_k even
```

Stop at 3. Next `÷2` would be `1.5 > 1(0)1 < 3` — that is **not** a coordination count. That is a ratio test (octave vs 3:1 gate). Park it. 3 is the core floor of *counts*. Below 3 you are in continuous angle / q, not in neighbor census.

Scale-up past 24 is legal as `24 > 1(0)1 < 48` but D-410 / 24-cell is parked. Do not promote 48 until 24 has a receipt.

## Why 1:6 and 1:12 show up “for free”

They are the **center-outward** readings of two adjacent layers that share 12.

```
from inner center:   1 toward the 6-ring, 1 toward the 12-clock
from outer center:   1 toward the 12-clock, 1 toward the 24-sheet
```

12 is the shared gate, so both layers report a 1:12. That is not two theories. That is one jamb with two faces.

6 is the shared gate one floor in, so you also get 1:6 from the inner center and from the core looking out.

## Falsifiers

- If coarse lock@ at 12 does not track fine lock@ at 6 on the shared jamb, the connector is numeric only.
- If `÷2` on L,R moves the `(0)` (hold belt width changes with floor), the unit pair was not invariant — you divided Ground. Illegal.
- If 3:1 gate ratio and 3 axis-pairs are treated as one object in a lock receipt, D-411 violation.
- If 12-NN FCC and 12-clock lock together on a square control print, packaging won.
