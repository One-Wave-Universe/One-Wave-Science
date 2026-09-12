# Reverse recovery dynamics

Reverse recovery is not a second diode. It is the body diode **changing its mind** after it was forward.

While forward, the drift region is flooded with minority carriers. When voltage reverses, those carriers must leave before the junction can block. Until they do, current runs the *wrong way*. That pulse is Irr. The area under it is Qrr. The clock on it is trr.

```
        If
         |
         |      *  Irr (negative)
         |     / \
    -----+----/   \____  blocks
         |  ta  tb
              trr = ta+tb
```

Qa (ta): current falls through zero and to Irr peak — charge still being swept.  
Qb (tb): junction starts supporting reverse voltage; current returns to leak.  
Soft recovery: Qb ≈ Qa, di/dt gentle.  
Snappy: Qb tiny, current cuts off hard, layout L rings.  

Datasheet Qrr/trr are at a stated If, di/dt, Vr, temperature. They are not constants. More If or hotter die → more stored charge → fatter Qrr.

## Why CELL_V1 cares

A back-to-back pair *blocks DC* when both channels are OFF. Recovery happens in the gaps:

1. Dead time — current freewheels in **one** diode of the pair.
2. Opposite channel turns ON — that diode is slammed reverse.
3. Qrr dumps through the station into **NET_G**.

That dump is a one-way current pulse on the mid. The evaluator can name it LEFT or RIGHT. It is not a lean of the pair. It is leftover plasma.

Energy in the pulse is roughly `Vr × Qrr` per event. Average power `Vr × Qrr × f`. Even at bench volts, a fast edge + fat Qrr is a spike on I_G.

Layout inductance turns Irr into `V = L di/dt` overshoot on the rails. Snappy + long wires = a ring that looks like AC you did not program.

## Time scales vs the RC window

| process | typical silicon FET |
|---|---|
| trr | tens of ns |
| Coss ring | ns–low µs |
| CELL RC window | you choose (µs–ms on F0) |

If the RC window is milliseconds, one Qrr spike is a glitch, not the ternary result — **unless** you sample I_G at the edge. Sample after the window, or the receipt is the diode.

If you raise AC frequency until the period ≈ trr, recovery *is* the waveform. Then G0 is a rectifier with a hangover, not `-(0)+`.

## Soft vs snappy on the mid

Soft: I_G blip, then settles. Hold belt can still catch it if the window is longer than trr.  
Snappy: I_G blip + rail ring. V+-−V0 and V−-−V0 both jump. Looks like both gates spoke. Quit logic may fire. False.

Temperature: hot = slower, fatter Qrr. A cell that holds at 25 °C can glitch at 80 °C without any lattice change.

## What is not recovery

- Coss charging (majority, displacement current) — happens even if the diode never went forward.
- Channel current when Vgs is up — not Qrr.
- Mid-buffer lag — VGBUF too weak, not the FET.

Separate them: OFF-OFF with no prior forward current should show Coss, not Qrr. OFF-OFF after a forced diode current should show Qrr.

## F0 measurement (low V, current-limited)

1. Force a known If through one body diode (other FET OFF).  
2. Reverse with a controlled di/dt (series R to cap the spike).  
3. Scope: If, Irr peak, ta, tb, integral = Qrr, V_G, I_G.  
4. Repeat other diode.  
5. Repeat with both channels commanded ON through the same current (diode should be shunted; Qrr should collapse).  
6. Repeat at two temperatures if you can.

Pass: Qrr events finish well inside the RC window and I_G after the window is back in the hold belt.  
Fail: ternary bit follows Irr, not the window.

## Design implications (still a model, not a parts list)

- Keep F0 edges slow vs trr so recovery is visible and small.
- Do not sample stamp on the switching edge.
- Dead time as short as the driver allows *or* long and logged — never accidental.
- Matched pair: same part code, same If when you characterize Vf and Qrr.
- Magnetic sense after this. A coil will happily integrate Irr and call it flux memory.

## Falsify

- Hold receipt timestamped on an Irr peak.
- AC through G0 at f where period ≈ trr and calling that the oscillator.
- One FET of the pair running hot (its diode is doing the work).
