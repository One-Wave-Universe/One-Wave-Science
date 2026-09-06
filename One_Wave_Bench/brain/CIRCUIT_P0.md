# P0 circuit — what you actually solder

## Rails and (0)

Two rails `+V` / `-V`. Midpoint is HOLD. A raw resistor divider is not a ground: it sags when a winding takes current. Use a rail-splitter (TLE2426, 4–40 V in, ~20 mA sink/source) or an op-amp buffered divider. That chip *is* the virtual ground. If the midpoint moves when you load a winding, ternary is dead.

True millivolt *decision* bands sit on top of this as comparators. The power rails for P0 should be something a FET will actually switch: start ±2.5 V or a single 5 V split. Sense mV. Do not demand 50 mV half-bridges on day one.

## Three windings = three half-bridges

Each of U V W:

```text
+V --- high FET -- winding -- low FET --- -V
                 |
                (0) only through the load, never hard-tied
```

P0 drive law (one legal ternary):

- UP:   U to +V, W to -V, V open/HOLD
- DOWN: U to -V, W to +V, V open/HOLD
- HOLD: all three open, midpoint unloaded

Never +V and -V on the same winding at once. That is shoot-through, not 3:1.

A cheap 3-phase BLDC driver (DRV8323-class or a brushed-up L6234 / tiny DRV8313) is this drawing in one package. Use it. Do not hand-wire six gates until the law is proven.

## Bidirectional / body diode

A single MOSFET conducts backwards through its body diode. "Bidirectional SiC nerve gate" means **two FETs back-to-back** (sources common or drains common) so neither diode sneak-paths HOLD. P0: two jellybean N-FETs back-to-back per throw, or accept diode leak and measure it. SiC is P2 endurance, not P0.

## Dead band (the 5-unit idea, in volts)

Window comparator on each winding current or on midpoint current:

- inside the window = HOLD
- above = UP request
- below = DOWN request

Hysteresis so it does not chatter. That is Schmitt, not poetry. Map window width later onto 100-90 … 15-0 if you want. First just pick 50 mV and write it down.

## Who drives gates

MCU or even three GPIO + dead-time is Administrator. M4 software must not own those pins. Dream proposes a move byte. Admin writes INH / INL.

## What to buy first

- bench supply or 5 V USB + TLE2426
- three LEDs + resistors as fake windings, then three small inductors
- six small MOSFETs or one 3-phase driver eval
- two current-sense resistors, one scope or DMM

Done when midpoint holds and STOP is all open.
