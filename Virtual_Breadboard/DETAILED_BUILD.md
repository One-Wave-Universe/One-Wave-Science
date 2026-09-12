# DETAILED BUILD — 2-state brain + 3-winding body

This is the long sheet. Print it. Do not skim to the motor.
Current knob on the ±12 V supply: **50 mA** until section 8 is green.
Scope earth is **not** blue (G) unless you know the scope floats.

Related short doors: `FULL_BODY_ARCHITECTURE.md`, `09_TESTS/CELL_V1_DO_IT.md`, `HEX-SPLIT/brain_2state.py`, `HEX-SPLIT/nerve_cell.py`.

---

## 0. What you are building

```
brain_2state.py     Field lists lean/live     Void sets engage
nerve_cell.py       three windings + mid      process = memory
copper              ±12, three half-bridges   star = G = I_0
Hall                location UP
MEM/Hall leftover   views UP
winding current     actions DOWN
```

Biology map only: hemispheres = Field/Void, brainstem = live 0/1/2, vagus = I_0, three motor nerves = A B C, muscle = star load. Not a medical device.

---

## 1. Tools

- Dual ±12 V bench supply with **visible current knobs and a switch**
- DMM (voltage + mA). Two DMMs if you have them.
- Breadboard 830 (63 columns). Optional second board for the actuator later.
- Wire stripper, flush cutters, 22 AWG jumper kit
- Optional: USB 5 V supply, Arduino Nano + USB cable, SS49E Hall, soldering iron for SOT-23 breakouts only

---

## 2. Parts (exact enough to buy)

### Power and board
| qty | item | notes |
|---|---|---|
| 1 | dual tracking ±12 V 1 A supply, or two 12 V bricks with commons tied | knobs required |
| 1 | 830 breadboard |
| 1 | USB 5 V (wall or USB port) | gates + Hall only |
| 1 | pack 22 AWG jumpers |

### Law / mid
| qty | item | notes |
|---|---|---|
| 2 | 10 kΩ 1% 1/4 W | red–blue and black–blue |
| 4 | 100 nF ceramic 50 V | rail decouple |
| 1 | 1 Ω 1 W metal film | I_0 shunt at home end of blue |
| 1 | DMM leads with clips |

If you only have a **single 9 V** brick instead of ±12: add 1× **TLE2426CLP** (TO-92). Pins, flat toward you, left to right: IN, COMMON, OUT. IN=+9, COMMON=supply−, OUT=blue. 100 nF IN–COMMON. Then red is +9, black is supply−, blue is ~4.5 V. All later voltages scale. Prefer ±12 if you have it — 0 is then a real post, no TLE.

### Three nerves (half-bridges)
| qty | item | notes |
|---|---|---|
| 3 | AO3401A on SOT-23 breakout (P-MOS high) | source to +12, drain to PHASE |
| 3 | 2N7000 or BS170 (TO-92 N-MOS low) | drain to PHASE, source to −12 |
| 3 | 220 Ω | P-MOS gate series |
| 3 | 220 Ω | N-MOS gate series |
| 3 | 10 kΩ | P-MOS gate to +12 (OFF = high) |
| 3 | 10 kΩ | N-MOS gate to −12 (OFF = low, Vgs=0) |

2N7000 pinout, flat toward you, pins down, left to right: **S G D** (confirm your bag; some clones differ).
AO3401 breakout: follow **that board's silkscreen**. Typical AO3401: pin1 gate, pin2 source, pin3 drain. Source must go to +12.

Alternate: 3× cheap half-bridge modules (DRV8871-class or similar) with their GND tied to blue. Then skip discrete high/low per phase.

### First muscle
| qty | item |
|---|---|
| 3 | 1 kΩ 1/4 W | PHASE to STAR |

### Sense
| qty | item | notes |
|---|---|---|
| 1 | SS49E Hall | Vs=5 V, GND=blue, OUT to DMM or Nano A0 |
| 1 | 10 µF 16 V electrolytic + 100 kΩ | optional view MEM, + toward view node |

### Later muscle
Small 3-phase gimbal / 28 mm pancake whose **stall current < supply knob and FET rating**. Not a 2212 on 2N7000.

### Controller (optional)
Arduino Nano. 5 V USB. GND to **blue**. D2/D3/D4 = live A/B/C request. D5 = engage from Void (you, a switch, or serial). A0 = Hall. A1 = shunt amp if you add an INA219 later; until then I_0 is the DMM.

---

## 3. Board geography

Label three rails with tape:

```
top long rail     RED     +12
middle jumpers    BLUE    0 / G     (use a dedicated row of jumpers, not a power rail if you only have two)
bottom long rail  BLACK   −12
```

If the board has only two power rails, use the top rail for +12, bottom for −12, and a **column of connected jumpers** as BLUE down the center channel.

Columns (suggested, not sacred):

| columns | what |
|---|---|
| 1–5 | supply entry, 100 nF, law 10 k, I_0 shunt |
| 10–18 | station A |
| 25–33 | station B |
| 40–48 | station C |
| 55–63 | star, Hall, MEM, Nano header |

---

## 4. Section A — rails and law (no FETs)

1. Supply OFF. Current knobs 50 mA both sides.
2. +12 → RED column 1. −12 → BLACK column 1. 0 → BLUE column 1.
3. 100 nF RED–BLUE at col 1. 100 nF BLACK–BLUE at col 1.
4. 10 k RED–BLUE at col 3. 10 k BLACK–BLUE at col 3.
5. 1 Ω in **series in BLUE** between col 5 and col 6. Home side (col 5) is supply 0. Far side (col 6+) is cell G. DMM mA can replace this shunt while you watch I_0.
6. Supply ON.

### Measure, black DMM lead on BLUE far (cell G)

| point | expect |
|---|---|
| RED | +12.0 V ± 0.3 |
| BLACK | −12.0 V ± 0.3 |
| I_0 (through shunt or meter in blue) | < 0.2 mA |

7. Pull the RED 10 k. I_0 moves (sign depends on wiring). RED vs G still ~12. Plug back. I_0 dies.
8. Pull the BLACK 10 k. Opposite I_0. Plug back.

**Pass A:** steps 6–8 written down. Fail: I_0 already tens of mA with both 10 k in (short). Fail: G collapses (wrong 0).

---

## 5. Section B — star of resistors (still no FETs)

9. Tie one end of three 1 k together. That knot is STAR. Jumper STAR to BLUE far.
10. Other ends of the 1 k go to three empty nodes PA, PB, PC (cols ~12, 27, 42). For now those nodes float.
11. Measure STAR vs BLUE: ~0 V. I_0 still ~0.

**Pass B:** star is electrically G.

---

## 6. Section C — one nerve (phase A only)

12. P-MOS A: source → RED, drain → PA, gate → 220 Ω → control node GA. 10 k GA → RED (keeps P-MOS OFF).
13. N-MOS A: source → BLACK, drain → PA, gate → 220 Ω → control node NA. 10 k NA → BLACK (keeps N-MOS OFF).
14. Confirm 2N7000 S to BLACK, D to PA. Confirm P-MOS S to RED, D to PA.
15. Both gates at OFF default. Repeat Pass A. I_0 still ~0. PA should sit near mid or float quietly — not slammed to a rail.
16. **+1:** pull P-MOS gate toward BLACK (or to 0/blue through 220 Ω) so Vgs turns the P-MOS ON. N-MOS stays OFF. PA should approach +12. Current through 1 k A into STAR. I_0 takes a sign. G does not collapse.
17. Release to STAY. PA releases. I_0 dies.
18. **−1:** lift N-MOS gate toward BLUE or +5 vs BLACK so Vgs ≈ 5 V. P-MOS stays OFF. PA approaches −12. I_0 opposite sign.
19. Never drive GA and NA as ON together.

**Pass C:** table for A: STAY / +1 / −1 with I_0 and V_PA.

P-MOS ON level: you must pull the gate **below** +12 by several volts. A Nano GPIO 0/5 V referenced to BLUE can turn the N-MOS. It can turn the P-MOS only if 0 V on the gate vs +12 is enough (it is: gate at 0, source at +12, Vgs= −12). So: Nano GND = BLUE, Dpin HIGH = 5 V, Dpin LOW = 0.
- N-MOS ON: Dpin HIGH (5 V vs −12 is plenty).
- P-MOS ON: Dpin LOW (0 vs +12).
- STAY: N-MOS pin LOW, P-MOS pin HIGH (5 V vs +12 is only −7 V Vgs — **check your P-MOS Vgs(th)**. AO3401 is logic-level and should be ON at −4.5 V; 5 V vs 12 V = −7 V, usually ON. If STAY leaks, add a proper high-side translator later.)

Until Nano exists, use jumper clips: P-gate to BLUE for +1, N-gate to BLUE for −1, both at their pulldowns for STAY.

---

## 7. Section D — nerves B and C

20. Copy section C at PB and PC. Same pin discipline.
21. Pass C table for B. Pass C table for C.
22. Only **one** nerve commanded at a time. Other four FETs at STAY.
23. Walk: A+1 (0.5 s), STAY, B+1, STAY, C+1, STAY. Watch I_0 step. That is rotating command. Field walk.

**Pass D:** three tables + one walk without smoke or I_0 pegged at the knob.

---

## 8. Section E — location UP and views UP

24. SS49E: Vs to USB 5 V, GND to BLUE, OUT to DMM vs BLUE. Sit the package against the star knot or later against a coil.
25. Repeat the walk. OUT should change with each live winding if any field reaches the chip. Log three numbers.
26. All STAY after a walk. Watch Hall for 2–3 s. If it keeps a bias vs the pre-walk quiet, leftover B is talking (hold/reinject). If it dies immediately, memory is only current — still a valid first body.
27. Optional MEM: 10 µF + 100 k from a buffered view node to BLUE. Stage-1 style. Do not hang MEM on PA (that's the motor node).

**Pass E:** Hall log exists. Top layer is no longer blind.

---

## 9. Section F — 2-state brain on the desk

On the laptop, in HEX-SPLIT:

```bash
python brain_2state.py
python nerve_cell.py
```

You are Field (type the lean) and Void (type override). Hook later:

```
thought = brain.tick(want_lean, want_live, seen_i_g, seen_hall, override)
nerve.tick(thought.engage, thought.live, thought.lean)
```

Nano sketch (when you want GPIOs): three pins as P/N pairs per the ON rules in §6, serial print of Hall and a switch for override. Do not PWM a drone motor from this sketch.

**Pass F:** both scripts print and assert. You know which box listed the lean and which box cut engage.

---

## 10. Section G — actuator

28. Replace one 1 k with a small coil, then all three, then a small star motor. Stall current must stay under the knob. If the knob slams to 50 mA and rails droop, the motor is too big.
29. Star **must** stay on BLUE. Do not return winding current on a sneaky extra black wire to the supply.
30. Repeat Pass C/D/E with the motor. Walk A B C. STAY. Watch shaft and Hall.

**Pass G:** shaft or coil field follows live gate. I_0 still readable. G still sits.

---

## 11. Illegal (will fake the system)

- Capacitor in series in BLUE
- Both FETs of one phase ON
- Two phases +1 at once on this first body
- Motor current through the TLE OUT pin (if you used 9 V+TLE, motor return is supply− **and** you stay at tiny current)
- Calling Hall memory when it tracks only current
- Field script setting engage=1 after Void said 0
- IRLZ44 / 2212 on this breadboard

---

## 12. Receipt sheet (copy)

```
V+ ______   V− ______   VG ______
I_0 both 10k ______
I_0 pull red 10k ______
I_0 A+1 ______  A-1 ______  A STAY ______
I_0 B+1 ______  C+1 ______
Hall quiet ______  Hall A+1 ______  Hall after STAY ______
engage test override: body silent? ______
```

Fill that. The architecture is then on the bench, not only in markdown.
