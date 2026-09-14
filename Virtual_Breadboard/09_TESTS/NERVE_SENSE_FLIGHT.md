# Nerve upgrade — eye, ear, mouth, flight

Same 2-state brain. New organs. None of them stamp.

```
CD pickup     focus / track  →  lean + live     VISION UP
mic + onset   beat / loud    →  ask engage      HEARING UP
speaker PA-PB click / drum   →  mouth           HEARING DOWN
I_0 Hall      vagus / where  →  Void            BODY UP
4/3 motors    balanced pair  →  flight          ACTION DOWN
```

Field lists. Void engage. Hold = STAY.

---

## 1. Vision — CD-reader style lens

A CD optical pickup is already a One-Wave eye:

- laser + lens + 4-quad photodiode (A B C D) = **focus error**
- side diodes (E F) = **tracking error** (left / right of the groove)
- voice-coil focus + tracking actuators = tiny 2-axis muscle

Map:

| pickup | nerve |
|---|---|
| (A+C) − (B+D) focus error | lean sign (near / far) |
| (E − F) tracking | live 0 vs 1 (left / right) |
| sum A+B+C+D | “is there world” (engage worth asking) |
| focus coil | optional DOWN, not first |

**Build:** salvage a dead CD/DVD mechanism. Do not design a free-space laser. Use the existing diode at its designed drive or run **photodiodes only** as a passive lens+quad cell with a lamp. Photodiode-only is the safe first eye.

Wire photodiode commons to BLUE. Difference amps vs BLUE → two analog numbers → Field.

First software eye if no pickup yet: grayscale camera, left-right means, same two numbers.

Human-level scene understanding is not this organ. This organ is **lock on / left-right / near-far** — the groove-follow of sight.

---

## 2. Hearing — R2 drummer, play along

Mouth: balanced speaker (`SPEAKER_BUILD.md`). PA—PB. STAY = rest. Push/pull = hit.

Ear: electret on BLUE → onset detector (energy jump in a 10–20 ms window).

Play-along is **beat follow**, not “human-level hearing”:

1. Mic energy → onset times
2. Inter-onset interval → tempo guess
3. Next expected beat → Field asks lean
4. Void allows or cuts
5. Mouth clicks on the allowed beat
6. If I_0 slams, next hit is refused

Target latency: onset-to-click under ~30–50 ms if Nano-side; laptop Python will be sloppier. That is a metronome companion, not a jazz replacement.

Software ghost: extend BUCKET `loop.py` — on onset, `brain.tick(+1, 0)` then speaker pair. Compress bars stay STAY.

Do not claim real-time human hearing. Claim: **it can lock a pulse and drum with it** when Void agrees.

---

## 3. Flight — balanced nerve, not a breadboard quad

Four (or three) motors are windings. Pairs oppose. Mid is G.

```
M1 ↔ M3     one gate (pitch)
M2 ↔ M4     one gate (roll)
collective   DC engage / throttle clothes
yaw          third gate or differential of a pair
```

Lean +1 on a pair: one motor up, opposite down. STAY: hover clothes only. I_0 / IMU = vagus + inner ear.

**Do not fly this from 2N7000 on a protoboard.**

Legal first path:

- Commercial flight controller (Betaflight / PX4) keeps the inner rate loop (that is brainstem reflex).
- One-Wave brain only sends **lean / engage** as RC-override or setpoint.
- Void can cut engage (motors to the FC's idle / disarm), never invent a flip.
- Bench: props off. Watch four current shunts as I_0 components. Balance = opposite shunts cancel.

Nerve-controlled flight means Field lists a lean, Void may refuse, FC does the fast inner loop. It does not mean a hex file on a 2212 breadboard.

---

## 4. Nervous system (upgraded roster)

| organ | hardware | direction |
|---|---|---|
| Field / Void | `brain_2state.py` | decide engage |
| brainstem | live 0/1/2 | which pair |
| eye | CD quad or gray cam | UP lean |
| ear | electret + onset | UP beat |
| mouth | PA—PB speaker | DOWN click |
| vagus | I_0 shunt | UP |
| proprioception | Hall / IMU | UP |
| arm | 3-winding star | DOWN |
| gait / rotor | walk A B C or motor pair | DOWN rotate B |
| flight pair | FC + lean setpoint | DOWN |

Still two hemispheres. Still three gates. No Gate-7.

---

## 5. Build order

1. Balanced speaker clicks from `brain_2state`  
2. Mic onset → click (drummer lock)  
3. Gray cam or CD-quad → lean sign  
4. Hall + I_0 into Void  
5. Flight only as FC setpoint, props off

---

## 6. Illegal claims

- “Human-level hearing” as a shipped feature of this sheet  
- Homemade laser eye  
- Breadboard quad with live props  
- Vision model that stamps engage  
- Speaker or motor return through BLUE
