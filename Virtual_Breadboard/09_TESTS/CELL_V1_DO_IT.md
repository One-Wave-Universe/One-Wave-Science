# Do it

You, a 9 V or dual ±12 V supply with a current knob, a DMM, a breadboard.
Current knob at 50 mA before anything else. If the knob is missing, put 100 Ω in series with the brick and a fuse.

## Night 1 — mid and two resistors

Parts in front of you:
- TLE2426 (if single 9 V supply) **or** just the 0 V binding post (if you already have ±12 V dual)
- 2× 10 kΩ 1%
- 0.1 µF
- DMM

### If dual ±12 V (the supply in the posters)

```
+12 binding post  →  red rail
  0 binding post  →  blue rail     this IS G. Do not add a TLE.
-12 binding post  →  black rail

red  — 10k — blue
black — 10k — blue
```

One 0.1 µF from red to blue, one from black to blue, near the binding posts.

### If only 9 V

```
9V+ → TLE IN  and red rail
9V− → TLE COMMON and black rail
TLE OUT → blue rail = G
0.1 µF IN–COMMON

red  — 10k — blue
black — 10k — blue
```

### Measure (black DMM lead on blue)

Write these down. That is the receipt.

| what | probe | expect dual ±12 | expect 9V+TLE |
|---|---|---|---|
| V+ | red | ~+12 | ~+4.5 |
| V− | black | ~−12 | ~−4.5 |
| I_G | DMM in series in the blue wire at the supply/TLE end | ~0 mA | ~0 mA |

Pull **one** 10 k out.

| I_G | not zero. Sign tells you which resistor you pulled. |
| V+ and V− vs blue | still roughly half. G did not collapse. |

Plug it back. I_G dies.

If G walks more than ~50 mV when you pull the 10 k on the TLE version, the mid is weak. Stop.
If I_G was already tens of mA with both 10 k in, you have a wiring short. Stop.

You just proved: balance holds, asymmetry moves, mid home.

No FETs yet. That is a full night.

## Night 2 — one bilateral pair at G0

Add:
- 2× 2N7000 (same bag)
- 2× 100 Ω
- 2× 10 kΩ pulldown
- one 5 V source for the gates (USB 5 V is fine). Common of that 5 V is the MOSFET **common source**, not earth, unless common source is already blue.

```
red  — 100 Ω — D of FET A
black — 100 Ω — D of FET B
S of A tied to S of B          = common source
G of A tied to G of B          = gates
10 k from gates to common source     OFF
```

**First: leave gates at 0 V to common source. Pair OFF.**

Repeat Night 1 table. Must still hold.

Diode-mode DMM between the two drains:
- one way you may see ~0.6 V (one body diode + the other blocking)
- the other way you should **not** see a dead short
If both ways look like a single forward diode, you wired sources wrong or one FET is backwards.

**Then: ON.**
5 V from common source to the tied gates.
If you tied common source to blue, USB 5 V return goes to blue and USB 5 V goes to the gates.

Repeat Night 1 table again.
Equal 10 k → I_G still ~0.
Pull one 10 k → I_G appears, G stays.

That is bidirectional path + mid still Ground.

## What you do not do

- Do not add G+ or G− tonight.
- Do not add a toroid.
- Do not add a Nano.
- Do not add a motor.
- Do not PWM.
- Do not series-C the blue rail.

## After those two receipts exist

Copy the pair twice. Star every source/mid tap to blue with its own short jumper, not a daisy chain down the rim.
Then a Nano may watch I_G (shunt in the blue wire at the home end) and print hold/lean.
Then a bought ESC may spin a motor with its 0 bolted to the same 0 binding post — one star, not through the cell FETs.

`nerve_cell.py` is the software ghost of this. It does not replace Night 1.
