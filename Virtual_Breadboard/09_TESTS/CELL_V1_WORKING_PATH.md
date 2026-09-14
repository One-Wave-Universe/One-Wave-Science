# How to make CELL_V1 work

"Work" means the mid stays a mid, hold is balance, lean is a logged I_G, and Qrr does not get to vote. Not gravity. Not six pyramids on the first night.

Low voltage. Current-limited supply. Scope earth off NET_G.

## Done looks like this

| # | observable | pass |
|---|---|---|
| P0 | rails labeled `+ \| 0 \| −` | voltages in that order vs controller |
| P1 | buffered mid | V_G home = V_G far within the hold belt at I_G = 0 |
| P2 | mid stiffness | forced ±I_test into G; V_G stays in belt |
| P3 | balance | + and − equal vs G; I_G ≈ 0 |
| P4 | lean | one rail offset; I_G sign matches the lean |
| P5 | G0 pair OFF | no DC path except leak; no 0.7 V clamp |
| P6 | G0 pair ON | 2 Rds path; I_G still matches lean, not Vf |
| P7 | slow AC through G0 | both polarities; not a half-wave |
| P8 | recovery | Irr dies inside RC window; stamp sampled after window |
| P9 | G+ and G− added | P3–P8 still true |
| P10 | sense coil | traces P3 vs P4; coil is not memory until drive-off hold is shown |

Stop at the first fail. Do not add a floor.

## Build order (do not skip)

### 0. Harness

Bench supply with a hard current cap. Three wires. Two test points on NET_G (home / far). Differential measurements only: V+−V0, V−−V0, V+−V−, I_G through VGBUF sense.

### 1. Mid only — P1 P2

Buffered splitter or op-amp follower on VCC/2 (or true ± supply with 0 as a real rail — stronger, if you have it).
No FETs yet.
If a divider-only mid walks when you load it, you do not have Ground.

### 2. Passive pair — P3 P4

Two equal resistors + to G and − to G. No silicon.
Balance: I_G ~ 0. Offset one resistor or one rail: I_G appears, V_G holds.
This is the law without diodes. If this fails, MOSFET work is theater.

### 3. One bilateral station at G0 — P5 P6

Common-source back-to-back pair. Gates referenced to the common source. Defined OFF (pull so Vgs = 0). Series R on each drain so a mistake cannot dump the supply into G.

OFF: confirm no 0.7 V path either way.  
ON: confirm conduction both ways and I_G still tracks lean.

Drive slow. No dead-time experiments until P5/P6 pass.

### 4. RC window — P7 P8

Add R-C so the intended period is **much slower than trr** (ms vs tens of ns on F0).
AC small on top of DC bias.
Sample ternary *after* the window, never on the edge.
If the waveform half-waves, a diode is running the show — go back to P5.

### 5. G+ and G− — P9

Copy G0 twice. Star each station mid to the spine. Do not rim-walk G.
One gate live for a test; others OFF and logged.

### 6. Magnetics last — P10

Hall or coil as a probe. Compare hold vs lean. Then drive-off. If the probe forgets when the channel opens, it was not memory.

## Controller loop (software, after P7)

```
set rail offsets
wait RC window
read V+−V0, V−−V0, I_G
if |I_G| < belt: stamp hold
else: stamp lean sign
write receipt JSON
```

Controller sits at the home end of NET_G. It does not command −A after watching A. If it does, the pair is a puppet.

## Simulator first (same receipts)

Virtual Breadboard / SPICE: three rails, VGBUF as a voltage source + series Rout, two resistors, then two FET models with body diodes enabled.
Run P3–P8 in sim. If the model has no body diode, the sim is lying about P5/P8.

## What will make it fail (already known)

- Divider as return rail
- Scope earth on G
- Single FET called a gate
- Stamp on Irr
- AC period ≈ trr
- Three stations before one mid works
- Magnetic feedback before sense
- Linear step sequencer instead of crossing G both ways

## Repo files

Locked drawing: `LOCKED_CELL_TOPOLOGY_DC_AC_MIRRORED_GATES.md`  
Bring-up checklist: `CELL_V1_SAFE_BRINGUP.md`  
Diodes: `MOSFET_BODY_DIODE.md`  
Recovery: `REVERSE_RECOVERY.md`  
Receipt: `10_RECEIPTS/CELL_V1_RECEIPT_SCHEMA.json`
