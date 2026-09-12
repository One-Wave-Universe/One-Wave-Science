# NTC bias current limits

Self-heat:

    ΔT = P / δ = I² R / δ

δ = dissipation constant. Still air bead ~1 mW/K. Glued to a motor can ~2–5 mW/K.
R falls as it heats (NTC). Worst self-heat for a *fixed current* is at cold (high R). Worst for a *fixed voltage across the NTC* is as it warms (current climbs). A divider is in between.

Target: ΔT from sense current ≤ 0.3 °C so Void is watching the can, not the bead.

## Current cap (10 kΩ @ 25 °C)

P_max = δ × 0.3 K

| δ | P_max (0.3 °C) | I at 10 kΩ | I at 1 kΩ (hot) |
|---|---|---|---|
| 1 mW/K still air | 0.30 mW | 0.17 mA | 0.55 mA |
| 2.5 mW/K on metal | 0.75 mW | 0.27 mA | 0.87 mA |

Use the **still-air** column if the bead can hang. Use metal if it is truly glued.

F0 rule: **I_bias ≤ 100 µA** is safe in either column at 10 k. **≤ 250 µA** is acceptable glued, sloppy in air.

## Divider on 5 V

I ≈ 5 / (R_fixed + R_ntc)

| R_fixed | I @ 25 °C (10 k NTC) | P in NTC |
|---|---|---|
| 10 kΩ | 0.25 mA | 0.63 mW |
| 47 kΩ | 88 µA | 77 µW |
| 100 kΩ | 45 µA | 21 µW |

10 k + 10 k on 5 V is the edge of the 0.3 °C still-air budget. Prefer **47 k** fixed on 5 V. Do not bias from +12 with 10 k.

+12 through 10 k + 10 k NTC → 0.60 mA, ~1.8 mW in the NTC → several °C fake in air. Illegal.

## Hot end

At 70 °C a 10 k B=3950 NTC is ~2 kΩ. Divider current rises. Check P at that R too. 47 k + 2 k on 5 V → ~0.1 mA, P still small. 10 k + 2 k on 5 V → 0.42 mA, ~0.35 mW — ok on metal, rude in air.

## Void number

Treat any implied ΔT_sense > 0.5 °C as a wiring bug, not weather.
