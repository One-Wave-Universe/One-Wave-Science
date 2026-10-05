# ONE-WAVE CELL — combined

> **RETIRED PHYSICAL BUILD:** The `+12 V / 0 V / -12 V` AO3401A/2N7000
> circuit below is historical and must not be built or mixed with CELL_V1 F0.
> The sole current physical authority is the 5 V + TLE2426 build in
> `CELL_V1_FULL_BUILD.md`, `01_PARTS/CELL_V1_PARTS_BOM.md`,
> `02_CONNECTIONS/CELL_V1_NETLIST.md`, and
> `09_TESTS/CELL_V1_SAFE_BRINGUP.md`. Conceptual architecture text below is
> retained only for history.

Brain is two states. Body is three windings. Mid is G. Process is memory. Motor is the ternary layer. Spintronics goes down and up. This file is the merge.

Pointers if you still want the split sheets: `FULL_BODY_ARCHITECTURE.md`, `DETAILED_BUILD.md`, HEX-SPLIT `brain_2state.py` `nerve_cell.py` `BODY.md` `SIX.md` `GROUND.md`.

---

## 1. The machine

```
Field  explorer   lists lean + live     one 1
Void   checker    engage 0 or 1         the other 1
brainstem         live ∈ {0,1,2}

views UP          memristor / Hall-B / MEM
spin UP           location, I_0, phase
spin DOWN         torque, winding current

A B C             = G+ G0 G− = three nerves
STAR              = G = blue = vagus = I_0 home
```

```
BC-DC     engage
TC-AC     +1 / STAY / −1 on the live winding
QC-RC     views UP + actions DOWN, one seq
rotating B    walk A→B→C
hold          all STAY, leftover B
reinject      leftover B is next baseline
override      Void sets engage=0     not Gate-7
```

Bidirectional at the mid. Not a linear six-step conveyor. Feeling informs. Does not fire the FET.

`python HEX-SPLIT/brain_2state.py`  
`python HEX-SPLIT/nerve_cell.py`  
Thought.engage/live/lean → nerve.tick. I_0 and Hall → Void.

---

## 2. Schematic

```
+12 ─ highA ─ PA ─ winding A ┬
+12 ─ highB ─ PB ─ winding B ┤ STAR ═ BLUE ═ I_0 ═ supply 0
+12 ─ highC ─ PC ─ winding C ┴
            lows ─ −12

RED — 10k — BLUE — 10k — BLACK
Hall at STAR     MEM optional to BLUE
RC across station, never a cap in BLUE
```

| high | low | state |
|---|---|---|
| ON | OFF | +1 |
| OFF | OFF | STAY |
| OFF | ON | −1 |
| ON | ON | illegal |

Live one winding. Others STAY.

High = P-MOS source on +12, drain on PHASE. Low = 2N7000 source on −12, drain on PHASE.

**Do not connect a BLUE-referenced Nano GPIO directly to either gate on the ±12 V build.** A 0/5 V GPIO cannot make STAY with sources sitting at ±12 V: PMOS gate=5 V still gives VGS≈−7 V, and NMOS gate=0 V still gives VGS≈+12 V. That leaves both devices biased ON instead of OFF.

For the first physical bench proof, use local gate-to-source bias and manual commands:

- P-MOS OFF: 10 k gate→+12/source. P-MOS ON: add 10 k gate→BLUE, giving gate≈+6 V and VGS≈−6 V.
- 2N7000 OFF: 10 k gate→−12/source. 2N7000 ON: add 10 k gate→BLUE, giving gate≈−6 V and VGS≈+6 V.
- STAY: both command-to-BLUE resistors removed; gate-to-source resistors hold both devices OFF.
- Never install both ON-command resistors on one phase at once.

Nano control comes later through a proper level-shifted or isolated gate-drive stage. The permanent regression `23_dualrail_gpio_gate_guard.js` exists specifically to stop direct-GPIO drift from returning.

---

## 3. Parts

Dual ±12 V with current knobs (20 mA first, 50 mA only after the 1 k load receipts pass). 830 breadboard. 3× AO3401 breakout (P-MOS) + 3× 2N7000. 6× 220 Ω optional gate series resistors, 12× 10 k for the six gate-source/command divider legs, 2× 10 k 1% law, 4× 100 nF, 3× 1 k first load, 1 Ω shunt, DMM, USB 5 V, SS49E Hall. Optional: TLE2426 if only 9 V exists, 10 µF+100 k MEM, Nano only after gate-level shifting, small star motor after receipts. No 2212 on 2N7000.

For the first single-phase proof you only need one AO3401 + one 2N7000, four 10 k gate-network resistors, the two 10 k law resistors, and one 1 k load.

Single-9 V variant: TLE2426 IN=+9 COMMON=supply− OUT=BLUE. Then stay tiny current so OUT is not a motor return.

---

## 4. Build

Supply OFF. Knobs 20 mA for the first phase proof.

**A. Rails.** +12 RED, −12 BLACK, 0 BLUE. 100 nF at the posts. Two 10 k to BLUE. I_0 shunt in BLUE at home. ON. V+≈+12, V−≈−12, I_0≈0. Pull one 10 k: I_0 moves, G sits. Plug back.

**B. Star.** Three 1 k from PA PB PC to one knot on BLUE. For the very first proof, populate PA only.

**C. Nerve A — manual first, no Nano.** Wire the P-MOS gate with 10 k to +12/source and the 2N7000 gate with 10 k to −12/source. Verify both gates equal their own sources before power-on: that is STAY. Then command one device at a time by adding its separate 10 k gate→BLUE resistor. Expected approximate gate targets are +6 V for P-MOS ON and −6 V for NMOS ON. Table: STAY / +1 / STAY / −1 / STAY while recording I_0 and V_PA. Never both ON.

**D. B and C.** Copy only after A passes. Walk A+1, STAY, B+1, STAY, C+1.

**E. Hall** at star, 5 V vs BLUE. Log walk and STAY-after-walk.

**F. Brain scripts** on the laptop. You are both states. Do not connect Nano GPIO to the ±12 gate network until a separate level-shifted/isolated driver has its own receipt.

**G. Muscle.** Swap 1 k for coils or a small star motor only after the resistor-load receipts are clean. Star stays on BLUE. Raise the current knob from 20 mA toward 50 mA only if the measured load requires it and nothing pegs or heats.

---

## 5. Receipt

```
V+ ____  V− ____  VG ____
I_0 both 10k ____   pull one 10k ____
A STAY: VPA ____ I_0 ____
A +1:   VgateH ____ VPA ____ I_0 ____
A STAY: VPA ____ I_0 ____
A -1:   VgateL ____ VPA ____ I_0 ____
A STAY: VPA ____ I_0 ____
B+1 ____ C+1 ____
Hall quiet ____ Hall walk ____ Hall STAY after ____
override: body silent? ____
```

---

## 6. Illegal

Cap in BLUE. Two phases driven. Both FETs on one phase. Direct BLUE-referenced 0/5 V GPIO on ±12 gate nodes. Field forcing engage after Void said 0. Blind override (no I_0/Hall). Motor current through TLE OUT. Stamp on a switching spike.

---

## 7. Split-file index (merged into this, still on disk)

HEX-SPLIT: README, BODY, SIX, GROUND, BRAIN_CELL, brain_2state.py, nerve_cell.py, SYNC, clock_sync.py  
VBB: LOCKED_CELL_TOPOLOGY…, THE_SYSTEM, ROTATING_FIELD, SPINTRONICS_LOOP, TLE2426_VIRTUAL_GROUND, MOSFET_BODY_DIODE, REVERSE_RECOVERY, DETAILED_BUILD, FULL_BODY_ARCHITECTURE, CELL_V1_*, POSTER_*, STAGE1_PHYSICAL_BUILD, experiments/brain_cell_001.json
