# CELL_V1 5 V physical-lock branch step

- MAIN GOAL: define one realistic, buildable CELL_V1 without competing power architectures.
- HARD START: `main` at `3267902531a6e9b0d896c8d0d2933cf378511192`.
- ACTIVE BRANCH: `cell-v1/lock-5v-tle2426-build`.
- SELECTED AUTHORITY: regulated 5 V supply with TLE2426-class buffered CENTER.
- COMPLETE CELL: three opposing differential Mirror pairs about NET_G, one whole-state quadratic memory after ternary resolution, and analog differential reinjection.
- BUILD ORDER: midpoint host, passive receipt, one complete G0 station, then exact G+/G- copies.
- HARD BOUNDARY: motor disconnected; RC is not memory; magnetic/memristive whole-state retention and analog reinjection require separate physical receipts.
- PROTECTED TEST: `CELL_V1_SAFE_BRINGUP.md` P0–P9 with a receipt at every step.
- SOFTWARE CHECKS: 5 V virtual-ground stamp 1; 1 k virtual-ground load stamp 2; regressions 20 and 21.
- RETIRED ALTERNATIVE: `+12 V / 0 V / -12 V` AO3401A/2N7000 shortcut.
- HARD STOP: documentation agrees on one physical topology and consistency checks pass.
