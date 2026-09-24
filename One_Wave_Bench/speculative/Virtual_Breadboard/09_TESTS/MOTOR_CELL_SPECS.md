# Motor cell specs

One winding + one sensor cell on one star. Two tiers. Do not mix them on one breadboard.

## F0 — bench nerve (what you build first)

| item | spec |
|---|---|
| Rails | ±12 V dual, or 9 V + TLE mid |
| Current cap | 50–100 mA supply knob |
| High FET | AO3401-class P-MOS, SOT-23 breakout |
| Low FET | 2N7000 / BS170, **200 mA cont., 500 mA pulse**, Rds ~1–5 Ω |
| Gate | 220 Ω series, 10 k pulldown to the rail that means OFF |
| Load first | 1 kΩ to star |
| Load next | coil or tiny star motor **stall < 80 mA** |
| Law R | 10 kΩ 1% +G and −G |
| I_0 shunt | 1 Ω 1 W |
| Pulse | RC window, then STAY |
| Hold current | ≈ law + puck electronics, not hover |

2N7000 is the bottleneck. Treat F0 as **80 mA class**, not 4 A class even if the P-MOS could.

## F1 — later actuator (PCB, not protoboard)

| item | spec |
|---|---|
| Rails | still ±12 or 4S only after receipts |
| FETs | matched half-bridge module or ≥4 A logic pair |
| Stall budget | set by module + current limit, not hope |
| Inner loop | commercial FC if flying |
| Nerve | still +1 / STAY / −1, one live pair |

## Sensor cell (built into the motor cell)

| channel | part | electrical |
|---|---|---|
| heat | 10 k NTC 3950 | divider to G, ~0.1 s tau |
| vibe | 20 mm piezo or analog IMU | vs G, AC couple ok |
| balance / where | SS49E | 5 V, OUT ~1.0–2.5 V, ~1.4 mV/G |
| puck power | 5 V vs G | few mA |

Heat trip (Void): NTC implying >70 °C can first. Vibe trip: hash ≫ walk-level. Balance: opposite pucks differ > belt.

## Timing

| | F0 |
|---|---|
| FET edge | slower than body-diode trr (don’t stamp the spike) |
| RC window | ms, not tens of ns |
| Hall sample | after window |
| STAY settle | before next lean |

## Pass numbers (write them)

```
V+ V− VG
I_0 STAY          < 1 mA plus puck
I_0 +1 pulse      < knob, G sits
NTC at STAY       ambient
NTC after 10 pulses   noted, not runaway
piezo at STAY     quiet
piezo at pulse    visible
Hall quiet / walk / STAY-after
```

## Not a spec

Hover watts. Human-level hearing. 2212 stall on 2N7000. PWM as hold.
