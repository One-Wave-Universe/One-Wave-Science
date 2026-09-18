# LOCK — the cell

## Sole physical build authority

CELL_V1 F0 is the **5 V + TLE2426 buffered-CENTER build** in
`CELL_V1_FULL_BUILD.md`. It contains three logical Mirror stations, six
bilateral legs, and twelve physical N-MOSFETs. The motor remains disconnected.

The older `+12 V / 0 V / -12 V` AO3401A/2N7000 documents are retired
alternatives and must not be combined with CELL_V1 F0.

Kitty Hawk / hive / slip-ship = GRAV play. Not this folder's job.

## Passed in software

| stamp | file | result |
|---|---|---|
| brain | HEX-SPLIT `brain_2state.py` | Field lists, Void cuts |
| nerve | HEX-SPLIT `nerve_cell.py` | one live winding, hold |
| 1 rails | `10_RECEIPTS/cell_v1_stamp1_rails.py` | I_0 0 / ±0.25 mA around virtual ground |
| 2 dummy | `10_RECEIPTS/cell_v1_stamp2_bridge.py` | STAY 0, +1 = +2.5 mA, −1 = −2.5 mA |

Ideal G. Ideal switches. That is the virtual lock for the *law*, not for body diodes or layout.

## Copper still owes

`09_TESTS/CELL_V1_SAFE_BRINGUP.md` P0–P9 at a 10–20 mA initial supply limit,
recorded in `10_RECEIPTS/CELL_V1_RECEIPT_SCHEMA.json`.

Complete-cell copper additionally owes P10 whole-state quadratic differential
memory, P11 manual bounded reinjection, and P12 analog hysteretic reinjection.
Memory follows the binary and ternary layers and encompasses the whole cell.

## Canonical read (stop hunting)

`CELL_V1_FULL_BUILD.md`
`01_PARTS/CELL_V1_PARTS_BOM.md`
`02_CONNECTIONS/CELL_V1_NETLIST.md`
`09_TESTS/CELL_V1_SAFE_BRINGUP.md`
`10_RECEIPTS/CELL_V1_RECEIPT_SCHEMA.json`

Run:

```
python Virtual_Breadboard/10_RECEIPTS/cell_v1_stamp1_rails.py
python Virtual_Breadboard/10_RECEIPTS/cell_v1_stamp2_bridge.py
```
