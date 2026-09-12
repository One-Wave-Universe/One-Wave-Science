# MOSFET body diode vs the mirrored station

A discrete power MOSFET is a three-terminal package with a **fourth junction already inside it**. That junction is the body diode. It is not optional. It is the p–n from p-body to n-drain (n-channel). The body is almost always bonded to source in the package, so the diode sits **source → drain** (anode at source for n-MOS).

```
n-MOS, OFF, Vgs = 0

  drain  ◀──|◆──▶  source     diode ON if V_source > V_drain + Vf
                  body
```

Channel OFF does **not** mean the part is open both ways. One polarity still conducts ~0.7 V through silicon. That is a one-way leak. A single FET is not a mirrored gate.

## Why CELL_V1 uses two, sources common

```
rail A — D1  S1══S2  D2 — rail B
              |        |
            diode    diode     arrows oppose
```

Sources tied, gates tied (or driven as one). When both channels are OFF:

- current A→B forward-biases FET1's diode and **reverse-biases FET2's**
- current B→A forward-biases FET2's diode and **reverse-biases FET1's**

No DC path either way except leakage. That is bidirectional *blocking*.  [web:78]

When both channels are ON, current uses two Rds(on) in series. Drains and sources are interchangeable. Diode is shunted by the channel; Vsd collapses from ~0.7 V to I×(2 Rds).

Common-drain (sources out) is the other legal pairing. Same opposed diodes. Gate drive reference changes. Do not mix the two drawings in one station.

## What the diode still does when you thought it was gone

**Dead time / both-OFF window**  
If an inductive or RC current is already flowing and you open both channels, the current has nowhere legal to go until the diodes take it. One diode in the pair will forward for that instant. The other is reverse. You just wrote a **unidirectional kick** through G. Hold is not a diode kick.

**Reverse recovery (Qrr, trr)**  
A body diode that was forward-conducting stores minority charge. When the opposite FET turns on and slams that diode reverse, the stored charge dumps as a reverse spike (Irr) for tens of ns before the junction blocks. Loss ~ V × Qrr × f. Snappy recovery + layout L → voltage spike. GaN HEMTs have no p–n body diode and no Qrr of this kind; silicon does.  [web:79][web:82]

On CELL_V1 that spike is a lie on `I_G` and a possible false LEFT/RIGHT.

**Vf asymmetry**  
Two diodes are never twins. One Vf 0.65 V, the other 0.72 V, and the mid already leans. That is not Field/Void. That is unmatched silicon. Measure both Vsd at the same If before you name a lean.

**Coss / Crss**  
Even with diodes blocked, drain capacitances still couple AC across the OFF pair. High dV/dt into a floating mid looks like oscillation that isn't the intended AC layer.

**Body effect**  
If you ever float body (4-terminal die), Vsb shifts Vth. Packaged 3-pin parts hide this by shorting body to source — and that short *is* why the diode polarity is fixed.

## Mapping onto the cell

| event | diode if single FET | diode if back-to-back OFF | wanted cell |
|---|---|---|---|
| hold, balanced | one side still a 0.7 V clamp | both blocked except leak | mid quiet, I_G ~ 0 |
| lean, channel ON | channel + maybe diode | 2×Rds, diode shunted | imbalance on spine |
| AC through G | half-wave rectifier | both ways only if channels ON in time | crossing, not a rectifier |
| dead time | freewheel one way | one diode of the pair freewheels | log it; do not call it hold |

G0 is the station that must not become a rectifier. If the AC layer half-waves on the mid, you built a diode, not `-(0)+`.

## What to log on F0 (low voltage, current-limited)

- Vsd of each FET at a small forced If (diode polarity check)
- I_G with both gates OFF, rails biased (leak + mismatch)
- I_G with both gates ON, forced balance (should drop)
- a slow AC through G0: look for half-wave on V+-−V0 vs V−-−V0
- one controlled dead-time: capture whether I_G spikes one way

Do not close a magnetic feedback loop until those five traces exist.

## Falsify

- A "hold" that is actually one body diode conducting ~0.7 V.
- AC through G0 that is a half-wave.
- I_G spike on every polarity change that matches Qrr timing, not the RC window.
- Single FET called a mirrored gate.
