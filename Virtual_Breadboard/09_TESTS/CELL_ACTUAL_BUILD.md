# CELL_V1 — actual F0 board

## Locked build identity

This file names the **one realistic CELL_V1 build**. It does not define a
second shortcut circuit.

```text
Supply:       regulated 5 V, current limit 10–20 mA
NET_P:        +5.0 V absolute
NET_G:        TLE2426 OUT, approximately +2.5 V absolute (CENTER)
NET_N:        supply 0 V
Cell:         3 logical Mirror stations: G+, G0, G-
Traversals:   6 bilateral electrical legs
Switches:     12 N-MOSFETs total, two source-to-source per leg
Load:         resistor/RC qualification only; motor disconnected
```

The exact parts, nodes, and order are authoritative in:

1. `../01_PARTS/CELL_V1_PARTS_BOM.md`
2. `../02_CONNECTIONS/CELL_V1_NETLIST.md`
3. `../CELL_V1_FULL_BUILD.md`
4. `CELL_V1_SAFE_BRINGUP.md`
5. `../10_RECEIPTS/CELL_V1_RECEIPT_SCHEMA.json`

## Physical organization

Use one full-size solderless breadboard for F0. Put the TLE2426 and rail
decoupling at the controller/home end. Run NET_P and NET_N as supply buses.
Run NET_G as a star/reference spine from the midpoint host; each station tap
connects independently to NET_G through its own 10-ohm receipt shunt.

Build one complete G0 station first only as an assembly step. After G0 passes
P3–P7, copy that exact proven station to G+ and G-. The locked result is the
complete three-station cell, not the G0 construction checkpoint.

## Gate fixture

Each bilateral pair uses a floating, source-referenced manual gate fixture:

- two N-MOSFETs source-to-source, with their gates tied;
- 100 k from tied gates to the common-source node for defined OFF;
- floating approximately 3 V source, negative to common source;
- positive through one SPST switch and 220 ohm to the tied gates.

There are six independent fixtures—one for each upper/lower bilateral leg.
Never substitute a common ground-referenced GPIO during F0.

## Lock condition

CELL_V1 electrical F0 is not physically locked until every P0–P9 step in
`CELL_V1_SAFE_BRINGUP.md` has a completed receipt. Software/model passes are
not physical passes. The complete cell additionally requires P10 whole-state
quadratic memory, P11 manual differential reinjection, and P12 automatic analog
hysteretic reinjection. Those are required layers, not optional station-local
attachments.
