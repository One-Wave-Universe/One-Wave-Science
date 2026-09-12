# CELL_V1 parts (categories, not a shopping cart)

Low-voltage, current-limited bench only. Categories to fill with measured parts after F0.

| Block | Role |
|---|---|
| Power | Current-limited bench supply. Fuse. Emergency disconnect. |
| Rails | Three labeled conductors: `+` / `0` / `−` |
| Virtual ground | Buffered rail-splitter or dedicated mid buffer, sized for transient `I_G` |
| Gate stations | Three bilateral blocks (back-to-back MOSFET pair or equivalent) |
| Drive | Gate resistor, defined OFF pull, no floating gates |
| RC field | R+ C+ / R0 C0 / R− C− per station |
| Sense | Differential measurement of V+−V0, V−−V0, V+−V−; current into mid buffer |
| Magnetic | Sense coil or Hall first. Do not close magnetic feedback until sense is logged. |
| Safety | Thermal watch, protected test points |

A resistor divider is a bias hint, not a return rail.
