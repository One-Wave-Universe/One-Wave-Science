# CELL_V1 full build

±12 V dual supply. Current knob 50 mA for the cell. Motor current on a separate breaker/ESC.

```
+12 ─────────────────────────────────── RED
         |                |                |
        100              100              100
         |                |                |
        D A              D A              D A          2N7000
         S═S             S═S             S═S          sources tied per station
        D B              D B              D B
         |                |                |
        100              100              100
         |                |                |
-12 ─────────────────────────────────── BLACK

         G+               G0               G−

0 ─────═════════════════════════════  BLUE  → controller
         |                |                |
        tap              tap              tap          short jumper per station, star

RED — 10k — BLUE — 10k — BLACK     always fitted (the law resistors)
```

Each station:
- 2× 2N7000, sources common, gates common
- 10k gate to that common source (OFF)
- 100 Ω in each drain
- common source jumpered **straight to blue** (this build: pair sits on G)
- ON = 5 V from blue to that station's gate tie (USB 5 V return on blue)
- RC **across the station**, not in the blue wire: 10k + 0.1 µF from red to blue at that station, optional
- 0.1 µF red–blue and black–blue at the supply posts

Blue rail is one piece of wire from the 0 binding post to the controller end. No capacitor in that wire. No daisy-chain of 0 down the rim — three short taps.

Controller end of blue: DMM in series = I_0.

Only **one** station ON at a time for the first logs. Other two gates at 0 V to blue.

## Parts (cell only)

| qty | part |
|---|---|
| 1 | dual ±12 V supply, current knobs |
| 1 | 830 breadboard |
| 6 | 2N7000 |
| 6 | 100 Ω |
| 6 | 10 kΩ pulldown |
| 2 | 10 kΩ 1% law resistors |
| 3 | 10 k + 0.1 µF optional RC across station |
| 4 | 0.1 µF rail decoupling |
| 1 | DMM |
| 1 | USB 5 V for gates |

No IRLZ44 on this board. No toroid required for the cell to be complete. No motor on these FETs.

## Pass table (cell is full when this is filled)

| # | setup | I_0 | Vred vs blue | Vblack vs blue |
|---|---|---|---|---|
| 1 | all gates OFF, both 10k in | ~0 | ~+12 | ~−12 |
| 2 | all OFF, pull red 10k | nonzero + | still ~12 | still ~12 |
| 3 | all OFF, both 10k in again | ~0 | | |
| 4 | G0 ON, both 10k | ~0 | | |
| 5 | G0 ON, pull one 10k | nonzero, G sits | | |
| 6 | G0 OFF, G+ ON, same as 4–5 | | | |
| 7 | G0 OFF, G− ON, same as 4–5 | | | |
| 8 | two stations ON at once | I_0 messy or huge — quit. Don't stamp. |

That is the full cell.

## Motor (second machine, not required for the cell)

Bought ESC or a proper 3-half-bridge module. 2212 windings to the ESC only.
ESC 0 and cell 0 meet at the **supply 0 post**. One bolt. No motor current through 2N7000 or through the I_0 shunt of the cell.
Cell current knob stays 50 mA. ESC has its own limit.
High-side of a homemade inverter needs a boot driver. If you don't have one, buy the ESC.

Nano later: three GPIOs, one per station gate, 0/5 V vs blue. Read I_0 if you add a 1 Ω shunt at the home end and keep currents tiny. Do not PWM a 2212 from that Nano.

## Illegal on this full board

- Cap in the blue rail between stations
- Motor phase on a cell drain
- Two stations driven opposite and calling it hold
- IRLZ44 in the cell positions
- Calling a toroid memory before row 1–7 exist on paper
