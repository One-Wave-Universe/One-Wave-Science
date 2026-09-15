# LOCK — the cell

Kitty Hawk / hive / slip-ship = GRAV play. Not this folder's job.

## Passed in software

| stamp | file | result |
|---|---|---|
| brain | HEX-SPLIT `brain_2state.py` | Field lists, Void cuts |
| nerve | HEX-SPLIT `nerve_cell.py` | one live winding, hold |
| 1 rails | `10_RECEIPTS/cell_v1_stamp1_rails.py` | I_0 0 / ±1.2 mA |
| 2 dummy | `10_RECEIPTS/cell_v1_stamp2_bridge.py` | STAY 0, +1 = +12 mA, −1 = −12 mA (ideal battery gate drive) |
| 3 real gate bias | `test/regression-builds/24_cell_v1_manual_gate_bias_station_a.js` | STAY ~0, +1 = **+12.6 mA**, −1 = **−12.6 mA** (real AO3401A/2N7000 model cards, real 10k/10k manual gate-bias network) |

Ideal G. Ideal switches. That is the virtual lock for the *law*, not for body diodes or layout.

Stamp 2 assumed an ideal battery drives each gate for free. The actual
bench build (CELL_ACTUAL_BUILD.md / CELL_SCHEMATIC_PRINT.md) instead makes
each ON command by adding a second 10k gate-to-BLUE resistor, and that
resistor draws its own ~0.6 mA divider current from the same BLUE rail
I_0 is measured on. Stamp 3 is the corrected prediction for the circuit
that will actually get built. **Expect ~12.6 mA, not 12 mA, on the real
DMM** — a reading near 12 mA instead of 12.6 mA on the real board is the
thing worth double-checking, not the other way around.

**Both-ON does not show up on I_0.** Stamp 3 also confirms the shoot-through
path (RED -> qp -> pa -> qn -> BLACK) never touches BLUE at all, so a DMM
watching only I_0 would see almost nothing wrong while the circuit cooks
itself (real-model result: every device/resistor in that path driven far
past its rating, supply current-limited at 2 A -- a real brownout). Do not
trust I_0 alone to catch a both-ON mistake; watch for supply brownout,
heat, or smell, and never build a both-ON state to "see what I_0 does."

## Copper still owes

BUILD_25 steps 1–11 at 50 mA. Expect stamp 3's numbers on a DMM, not stamp 2's.

## Canonical read (stop hunting)

`ONE_WAVE_CELL.md`  
`DETAILED_BUILD.md`  
`BUILD_25.md`  
`09_TESTS/CELL_ACTUAL_BUILD.md`  
`09_TESTS/CELL_SCHEMATIC_PRINT.md`  
`FULL_BODY_ARCHITECTURE.md`  
`LOCKED_CELL_TOPOLOGY_DC_AC_MIRRORED_GATES.md`

Run:

```
python Virtual_Breadboard/10_RECEIPTS/cell_v1_stamp1_rails.py
python Virtual_Breadboard/10_RECEIPTS/cell_v1_stamp2_bridge.py
node Virtual_Breadboard/test/run_regression_builds.js
```
