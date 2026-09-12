# Balanced One-Wave speaker

The cone is a winding pair. It sits **between** two phases, not from a phase to earth.
Hold = both phases STAY at mid → no DC in the coil → silence.
Lean = phases opposite → current through the coil → click / tone.
I_0 at blue is still vagus. If the pair is balanced, I_0 stays quiet while the cone moves.

```
+12 ─ highA ─ PA ───── speaker ───── PB ─ highB ─ +12
            lowA ─ −12                    lowB ─ −12

BLUE = G = reference only
RED — 10k — BLUE — 10k — BLACK
```

Phase C unused, or used as a second smaller cone later.

| A | B | cone |
|---|---|---|
| STAY | STAY | hold, silence |
| +1 | −1 | push |
| −1 | +1 | pull |
| +1 | +1 | both to +12, no voltage across coil, illegal-as-sound |
| both ON on one side | | shoot-through |

That is ternary audio: + / 0 / − across the coil.

## Parts

Same cell FETs as `ONE_WAVE_CELL.md` for **two** stations (A and B).

| qty | item |
|---|---|
| 1 | 8 Ω small speaker (or 32 Ω headphone element — easier) |
| 1 | 47–100 Ω 1 W in series with the speaker on first bring-up |
| 1 | 100 µF bipolar (or two 220 µF electrolytics back-to-back) in series if you want to block leftover DC |

50 mA knob. 8 Ω straight to ±12 will eat the supply. Series R first. 32 Ω headphone element is kinder.

## Wire

1. Rails + two 10 k + I_0 as already built.
2. Station A and station B only.
3. Speaker + 47 Ω between PA and PB. No speaker lead to BLUE.
4. STAY/STAY. Listen. DMM across the coil ~0 V. I_0 ~0.
5. A=+1, B=−1. Click. Voltage across coil. I_0 should stay smaller than a single-ended drive to ground would be.
6. Swap +1/−1. Opposite click.
7. Slow toggle (hand jumpers or Nano ~2 Hz) = drum. Audio-rate PWM later, after the clicks are honest.

## Why this is One-Wave

Single-ended speaker to ground dumps return into G. That slams vagus. Balanced pair cancels at the mid. Cone moves. Blue stays the reference. Hold is silence with the oscillator still allowed to sit.

BUCKET drum = this click on a stamp. Compress bars = STAY. Express = one push-pull click.

## Illegal

Speaker from PA to BLUE as the only return. That is not balanced.  
No series R on an 8 Ω at 12 V.  
Audio PWM before STAY/STAY measures 0 V across the coil.
