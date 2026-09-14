# NTC thermal runaway

Two loops. Do not mix them.

**Motor cook:** copper and core heat faster than they shed. Current stays, resistance of copper *rises* (PTC-ish), torque drops, you push harder, heat climbs. Insulation and bearings die. The NTC is there to *see* this.

**NTC self-heat:** the sense current heats the bead. NTC resistance *falls* as it warms, so a voltage divider can dump *more* current into it, so it warms more. The reading runs away from the motor. Void then cuts a healthy winding, or never sees the can.

Self-heat grows with bias current and falls as the bead couples to a heat sink. Tens of µA vs tens of µA is tens of mK; sloppy mA bias is a fake fever.

## Divider that does not feed itself

```
5 V — 10 k (fixed) — sense node — NTC 10 k @ 25 °C — G
```

At 25 °C, current ≈ 5 V / 20 k ≈ **0.25 mA**. Power in the NTC ≈ 0.6 mW. Prefer 47 k–100 k fixed if the ADC still resolves it — current drops, self-heat drops.

Do not put the NTC across 5 V alone. Do not bias from +12 into a 1 k. That is how the sensor becomes the heater.

Keep the bead **on the metal**, not hanging in air on long leads (leads = another R and a different tau).

## What Void does

- Rising NTC (falling R) past the hot belt → engage 0. Pulse already spent is over; no new lean.
- NTC still climbing at STAY → something is still ON or the can is dumping leftover heat. Wait.
- NTC already hot before the first pulse → do not arm.
- Opposite sensor cell much cooler → that winding, not the room.

Void does not PWM a cooling cycle. It cuts engage. STAY is the cool-down.

## Falsify

- Bead in still air reads 10 °C above the can you can touch.
- Bias current > ~1 mA in a 10 k NTC.
- Heat trip only after smoke.
- Field using “hot” as a lean to drive more.
