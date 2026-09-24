# FULL BODY — nerve to brain — master build

One system. Biology is the map. Copper is the body.

## Architecture

```
                    FIELD (explorer)          VOID (override)
                         \                      /
                          \    OVERSIGHT 6:1   /
                           \   HOLD / engage  /
                            \                /
                             BRAINSTEM  live = 0/1/2
                                    |
                    views UP (memristor / Hall B / MEM)
                    spin UP  (location, I_0, phase)
                    spin DOWN (winding torque)
                                    |
                         G+ / A     G0 / B     G− / C
                           \          |          /
                            \         |         /
                             STAR = G = vagus = I_0
                                    |
                              actuator / muscle
```

```
BC-DC     engage
TC-AC     winding +1 / STAY / −1
QC-RC     views UP + actions DOWN, one seq
rotating B   walk A→B→C
hold+reinject leftover B is next baseline
```

Feeling informs. Does not fire the FET.
Override = engage 0. Not Gate-7.

## Schematic (the only cell)

```
+12 ── highA ─ PA ─ winding A ┬
+12 ── highB ─ PB ─ winding B ┤ STAR ═ BLUE ═ I_0 shunt ═ supply 0
+12 ── highC ─ PC ─ winding C ┴
              lowA/B/C ─ −12

RED — 10k — BLUE — 10k — BLACK

Hall at STAR (location UP)
Optional MEM/memristor from a view node to BLUE (state UP)
RC across each station, never in BLUE
One station live. Others both-OFF.
+1 high ON   STAY both OFF   −1 low ON   both ON illegal
```

High-side: P-MOS from +12, or a half-bridge chip. Nano 5 V does not turn on an N-MOS sitting at +12.

## Parts (buy)

| qty | part | role |
|---|---|---|
| 1 | dual ±12 V supply, current knobs | DC clothes |
| 1 | 830 breadboard + wire | body |
| 3 | P-MOS logic high (AO3401 breakout) or 3 half-bridge modules | nerve high |
| 3 | 2N7000 / BS170 | nerve low |
| 6 | 100–220 Ω | gate/drain |
| 6 | 10 kΩ | pulldown |
| 2 | 10 kΩ 1% | law +G / −G |
| 4 | 0.1 µF | decoupling |
| 3 | 1 kΩ | first muscle (to star) |
| 1 | DMM | I_0 and rails |
| 1 | 1 Ω 1 W optional | I_0 shunt |
| 1 | SS49E Hall + 5 V | location UP |
| 1 | 10 µF + 100 k | view MEM stand-in |
| 1 | USB 5 V | gates / Hall |
| 1 | Nano optional | print live/engage, read shunt |
| later | small 3-phase motor stall < knob | muscle |
| later | discrete memristor | replaces MEM |

2212 hover current is not this list.

## What you build in order (one table, not nights-as-religion)

1. Rails + two 10 k + I_0. Balance / pull-one-resistor.
2. Three 1 k to a star on blue. No FETs. Prove star is G.
3. One half-bridge on A. +1 / STAY / −1. I_0 sign.
4. B and C the same.
5. Walk A B C. Hall twitches around the star.
6. All STAY. Hall leftover? That is hold/reinject.
7. Nano prints engage/live/lean and I_0 / Hall. Field=you, Void=you until code.
8. Tiny motor only after 1–6 are numbers on paper.

## Software

```
HEX-SPLIT/nerve_cell.py     brainstem ghost (engage, live, lean → receipt)
HEX-SPLIT/clock_sync.py     stamp hold/commit
HEX-SPLIT/BODY.md           who this is
```

## File index (do not hunt)

**Law / geometry (HEX-SPLIT)**  
README, SHAPES, SIX, GROUND, BODY, LATTICE, THEORY, CIRCLE, SYNC, BRAIN_CELL, nerve_cell.py

**Cell contract (One-Wave-Science / Virtual_Breadboard)**  
LOCKED_CELL_TOPOLOGY_DC_AC_MIRRORED_GATES.md  
04_TIME_AND_DYNAMICS/THE_SYSTEM.md  
04_TIME_AND_DYNAMICS/DC_AC_RC_CYCLE.md  
03_ELECTRICAL_CORE/THREE_RAIL_VIRTUAL_GROUND.md  
03_ELECTRICAL_CORE/TLE2426_VIRTUAL_GROUND.md  
03_ELECTRICAL_CORE/MOSFET_BODY_DIODE.md  
03_ELECTRICAL_CORE/REVERSE_RECOVERY.md  
07_MAGNETICS/ROTATING_FIELD.md  
07_MAGNETICS/SPINTRONICS_LOOP.md  
07_MAGNETICS/ROTATIONAL_HOLD_TEST.md

**Build (09_TESTS)**  
CELL_V1_DO_IT.md  
CELL_V1_FULL.md  
CELL_V1_MOTOR_IS_TERNARY.md  
CELL_V1_BENCH.md  
CELL_V1_WORKING_PATH.md  
CELL_V1_SAFE_BRINGUP.md  
FULL_SYSTEM_BUILD.md  
CELL_V1_POSTER.md  
POSTER_CELL_MOTOR.md  
POSTER_QUADRATIC_TOP.md  
THIS FILE

**VBB experiment already real (different, smaller cell)**  
experiments/brain_cell_001.json — 5 V window comparator, not three windings  
STAGE1_PHYSICAL_BUILD.md — that cell in holes

## Biology legend

| body | board |
|---|---|
| hemispheres | Field / Void |
| brainstem | live 0/1/2 |
| vagus | I_0 |
| proprioception | Hall + leftover B |
| 3 motor nerves | A B C |
| muscle | star load |
| reflex hold | all STAY |
| veto | engage 0 |

## Done looks like

Paper with: V+, V−, V_G, I_0 at STAY, I_0 at A=+1, Hall at walk, Hall at STAY after walk.
Until those exist the posters are maps. This file is the map of the maps.
