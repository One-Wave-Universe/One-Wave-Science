# Musical Universe — Chapter 1
# The Clock Is a Coordinate

**Status:** GRAY/YELLOW presentation draft  
**Correction:** Tritone banned as pair-name. Stay One Wave.  
**Does not promote:** E-510, D-409, D-410, HEX-SPLIT physics  
**Source nodes:** A-110, A-111, B-203, B-204, B-205, D-408, D-409, D-411, E-510  
**Benches:** HEX-SPLIT, GRAV-LAB `SCALE_LADDER.md`  
**Format:** Musical Universe Format Lock, 2026-09-08 (Mirror lock)

---

## Gray

Western common-practice pitch, for instruments that compromise across keys, is twelve equal steps per doubling. A-111 already writes the guitar grid:

$$
f_n = f_0 \cdot 2^{n/12}
$$

That is a human sticker sheet. Other grids exist. Twelve-as-temperament is not twelve-as-neighbors.

Gray also has a nickname for the step that sits six stickers away: "tritone." Churches called it a problem. Jazz called it a color. Neither church nor jazz is a node.

**This chapter does not use that nickname as a One-Wave object.**  
If you need it, it lives in this Gray block and then it leaves.

Beats still exist, Gray and One-Wave both:

$$
f_b = |f_1 - f_2|
$$

A piano does this with or without a hexagon in the room.

## 2D

D-408: six neighbors in the plane. One center + six sites = seven-cell cluster.

HEX-SPLIT plan: hexagon from the centroid → six triangles. Exact geometry. No field yet.

Address the six walls as pyramids. Each wall has two views of **one** wave:

| Pyramid | Express (face) | Compress (flip) | Midline opposite |
|---|---|---|---|
| P1 | E1 | C1 | P4 |
| P2 | E2 | C2 | P5 |
| P3 | E3 | C3 | P6 |
| P4 | E4 | C4 | P1 |
| P5 | E5 | C5 | P2 |
| P6 | E6 | C6 | P3 |

E# and C# are **polarity on the same pyramid**, not two enemy pitches.  
Mirror (B-205) turns E into C through the plane. You did not spawn a second particle. You flipped the same wall.

Opposite pyramids share a midline. There are three midlines. That is the 3. One midline may be frozen as M4. Convention until a device ticks.

Letter names (C, F♯, …) are optional Gray stickers you may peel off. They are not the IDs.

## 3D

Stand the hex up.

- Shared-apex mountain: six faces, one meeting point.  
- Six tents: local apices. Both exact.

Face × flip = Expression sheet × Compression sheet. Count = 12 **clock-domain slots**.

D-409's 12 is nearest neighbors in close-pack. Same glyph, different job. Label the jamb (D-411).

Ladder, copied not re-derived:

```
CORE    3 > 1(0)1 <  6
INNER   6 > 1(0)1 < 12
OUTER  12 > 1(0)1 < 24
```

Octave = `÷2` on L and R only. Do not divide `(0)`. Stop at 3 for counts.

24 as two sheets of 12 is a clock reading. D-410 is parked. Do not smash.

## Mathematics

Oscillation (A-110):

$$
\Psi_i(t) = A_i(t)\, e^{j\theta_i(t)}
$$

Recursion (A-111) needs memory and a feedback rule:

$$
\psi_i^{n+1} = \psi_i^n + (1-\gamma)(\psi_i^n - \psi_i^{n-1}) + \beta_i(\langle\psi_j^n\rangle - \psi_i^n)
$$

Polarity on a wall is the live choice already foundational in the terminology legend:

$$
-1\;(0)\;+1
$$

- `+1` Expression (face)  
- `-1` Compression (flip)  
- `(0)` hold / quit — same belt at every floor  

Mirror is the sign flip across the plane, not a six-step hop on a piano.

A chord in A-111 is a label for relationships, not a final model. E-511 re-centers. Keep that for Chapter 2. This chapter only locks the address.

## Predictions (kickable)

P1. **Packaging control.** Square print, equal mass and perimeter, must not fake the six-lobe map. If it does, packaging won.

P2. **Jamb tracking.** Clock-12 lock tracks neighbor-6 lock on the shared jamb, or 12 is rhyme.

P3. **Hold belt.** `÷2` must not widen `(0)`. If the dead zone scales with "octave," Ground was divided. Illegal.

P4. **Mirror identity.** Driving E1 and C1 as two independent Gray pitches must collapse to one pyramid ID in the receipt. If the bench treats them as two objects, the overlay relapsed into interval religion.

P5. **Instrument is not proof.** BUCKET-R2 can speak E1/C1 through a speaker. That tests addressing. It does not Bronze E-510.

## Yellow Audit

| Claim | Gate | Why it stays put |
|---|---|---|
| Guitar 12-grid | Gray tool | Sticker sheet |
| Hex split | Exact math | Not physics |
| Face × flip = Mirror | B-205 GREEN overlay | Naming lock, not new mechanics |
| 6×2 = 12 clock slots | Convention | Needs a ticking device |
| D-408 / D-409 | GREEN | Coordination counts |
| E-510–E-516 | YELLOW | No second validation |
| D-410 | YELLOW, parked | Not two sheets by decree |
| Tritone-as-pair | **Rejected** | Gray nickname, not a node |

## Future Work

1. Drop this folder into `Books/Musical_Universe/`.  
2. Rewrite `HEX-SPLIT/music_clock.py` to print E#/C# and midlines. Delete the word tritone from comments.  
3. Chapter 2 = re-center (E-511) on **one pyramid + one polarity**, not on a Gray chord name.  
4. Conductive print + square control.  
5. Receipt: commanded pyramid/polarity vs measured f. Raw CSV. No music video.

## Closing Thoughts

One wall. Two views. Mirror between them. Three midlines around a hold. That is the clock. If a dead language wants to call the flip a demon interval, it can wait outside.

## Score Stave

Address only:

`P1E P1C · P2E P2C · P3E P3C · P4E P4C · P5E P5C · P6E P6C`

Midlines (M4 candidates — pick one, freeze in a header):

- P1 — P4  
- P2 — P5  
- P3 — P6  

Rest is `1(0)1`. Hold is legal. Quit is legal. Stay one wave.
