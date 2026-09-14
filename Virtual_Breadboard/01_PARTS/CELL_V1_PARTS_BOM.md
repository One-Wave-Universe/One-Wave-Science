# CELL_V1 F0 Parts BOM

Low-voltage, current-limited bench prototype. This BOM implements the explicit physical topology in `../CELL_V1_FULL_BUILD.md`.

## Count boundary

Three **logical** bidirectional Mirror stations (`G+`, `G0`, `G-`) are implemented as two electrical legs per station, two source-to-source MOSFETs per bilateral leg. Therefore F0 uses **12 MOSFET devices** while remaining **3 logical Mirror gates / 6 traversals**.

| Qty | Part / value | Function | F0 note |
|---:|---|---|---|
| 1 | regulated 5 V supply | NET_P to NET_N | start current limit <=20 mA |
| 1 | TLE2426-class rail splitter | NET_G midpoint | 4 V minimum input; source/sink midpoint, not load power return |
| 1 | 100 nF ceramic | rail-splitter bypass | IN to COMMON, close to device |
| 1 | 10 uF electrolytic | local supply bulk | IN to COMMON; verify polarity |
| 12 | N-MOSFETs | 4 per logical Mirror station | 2N7000-class is F0 candidate only if measured ON at chosen floating gate voltage |
| 6 | floating ~3 V gate sources or isolated drivers | one per bilateral pair | temporary CR2032-class gate source is acceptable for manual F0 |
| 6 | SPST switches / removable jumpers | manual pair enable | controller replacement comes later |
| 6 | 220 ohm | gate series resistors | one per bilateral pair |
| 6 | 100 k | gate-to-common-source pulls | defined OFF; never leave gate floating |
| 6 | 1 k 1% | main mirrored arm limiters | RU/RL, two per station |
| 3 | 10 ohm 1% | station tap -> NET_G receipt shunts | I_G = Vshunt / 10 ohm |
| 3 | 1 k | RC feed | station tap -> HOLD node |
| 3 | 10 uF | RC storage | HOLD node -> NET_G |
| 3 | 100 k | RC bleed | HOLD node -> NET_G |
| 1 | 2.2 k | midpoint stiffness test load | moved P->G then G->N, never permanent |
| 1 | 2.2 k | temporary lean helper | parallel with 1 k gives ~688 ohm |
| several | labeled test pins | P, N, G-home, G-far, station taps, HOLD nodes | use before LEDs |
| 1 | fuse / resettable protection or reliable supply limit | fault protection | no mains wiring on breadboard |
| later | ferrite ring + 20–50 turn sense winding or Hall probe | magnetic observation | sense only until drive-off retention is proven |

## MOSFET acceptance before buying/building around it

The first MOSFET choice is not accepted because its threshold number looks small. It must pass the actual G0 fixture:

- OFF in either direction: no normal body-diode conduction through the bilateral block;
- ON in either direction: stable milliamp conduction at the available floating `VGS`;
- no heating;
- repeatable forward/reverse current;
- pinout verified from the exact manufacturer's datasheet.

If a through-hole 2N7000-class device will not enhance sufficiently from the temporary ~3 V floating gate source, use a genuine lower-threshold logic-level N-MOSFET or a higher isolated gate drive that remains below the device's `VGS(max)`.

## Center-host budget

Balanced P-to-N station current should mostly bypass the TLE2426 OUT pin. The midpoint host carries **imbalance current**, not the full board current. Stay comfortably below its source/sink capability during F0 and log `I_G` through the station shunts.

A two-resistor divider is a bias hint, not a dynamic return rail.
