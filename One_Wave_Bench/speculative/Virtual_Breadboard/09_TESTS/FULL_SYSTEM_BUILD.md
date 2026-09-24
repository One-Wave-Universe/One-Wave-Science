# Full system — biology as the map, copper as the body

Not a medical device. Biology is how you *read* the layers. The board is still ±12 V, current-limited.

## Map

| body | board |
|---|---|
| Left / right cortex | Field explorer + Void checker — two `1`s of `1(0)1` |
| Midline / corpus energy | G, blue rail, star |
| Brainstem | picks live winding 0/1/2 |
| Vagus (afferent home) | I_0 in the blue wire at the controller end |
| 3 motor nerves | windings A B C = G+ G0 G− |
| Muscle / spindle | small star motor or three coils |
| Reflex hold | all STAY, leftover B |
| Voluntary lean | one winding ±1 |
| Feeling | inverted under the write — informs, does not fire the FET |
| Heart of the step | RC window, stamp after it |

DC clothes. AC is the nerve. RC is the synapse window. Rotating B is gait. Reinjection is proprioception: what the limb kept when you stopped pushing.

## Real parts (buy this)

**Power**
- Dual ±12 V bench supply **with current knobs** (or two 12 V bricks + a 0 V common). Set cell to 50–100 mA until the table is green.
- USB 5 V brick for gate logic only.

**Mid / law**
- Hookup, breadboard 830.
- 2× 10 kΩ 1% (law resistors + to G and − to G).
- 4× 0.1 µF ceramic rail caps.
- DMM that reads mA. Optional 1 Ω 1 W as I_0 shunt in blue at home.

**Three stations (the nerves)**
- 6× 2N7000 or BS170 (same bag).
- 6× 100 – 220 Ω gate / drain resistors.
- 6× 10 kΩ pulldown.
- High-side: 2N7000 cannot switch +12 as high-side N without a driver. First-pass cheat that works: **3× P-MOS high (AO3401 on a SOT-23 breakout, or TP2104 if you find THT) + 3× 2N7000 low.** Or 3× cheap half-bridge modules whose 0 is blue.

**Load (the muscle)**
- First: 3× 1 kΩ from each phase to star (no motor).
- Then: three small coils, or a **tiny** 3-phase gimbal / 28BYJ-style only if stall current < your knob and FET rating. A 2212 drone motor is later, on a bought ESC whose 0 is the same blue post.

**Sense (vagus + eyes)**
- DMM I_0.
- Optional analog Hall (SS49E or similar) near the star / rotor.
- Optional Nano: 3 GPIOs for live-gate, analog pin across the 1 Ω shunt. Prints hold/lean. Does not drive a drone.

**Brain (software)**
- `HEX-SPLIT/nerve_cell.py` is the brainstem ghost: engage, live, lean → receipt.
- Field lists lean. Void can set engage=0. You are both until the board is live.

## Wire (full)

```
+12 — highA — PHASE A — winding A ┬
+12 — highB — PHASE B — winding B ┤ STAR ═ BLUE ═ I_0 ═ supply 0
+12 — highC — PHASE C — winding C ┴
                 lowA/B/C to −12

RED — 10k — BLUE — 10k — BLACK
```

+1 high ON. STAY both OFF. −1 low ON. Never both ON.
One live winding. Walk A B C to rotate B.

## First receipts (ball rolling)

1. All STAY. I_0 ≈ 0. Rails ±12 vs blue.
2. A = +1. I_0 takes a sign. Blue sits.
3. A = −1. Opposite sign.
4. B = +1. Other nerve.
5. A then B then C +1. Hall or your eyes: field / twitch walks.
6. All STAY after a walk. If Hall / rotor keeps a bias, hold+reinject is talking.

Fill that. Then you have a nervous system in copper, not a poster.
