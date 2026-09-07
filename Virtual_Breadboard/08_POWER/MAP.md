# Layer 08 — Power

## Canon

Real source limitations and energy accounting. Battery models: nominal voltage,
internal resistance, available capacity, voltage sag, energy consumed, remaining
capacity, load-dependent runtime. Energy accounting must close within a declared
tolerance or the run receives a warning/FAIL.

## Status

| Capability | Location | Status | Test |
|---|---|---|---|
| Nominal voltage | `battery.value` | PASSING | — |
| Internal resistance | `BATTERY_RINT` (`circuit.js`) | PASSING | `qualification.test.js` #1 |
| Source current limit (brownout) | `BATTERY_MAX_CURRENT` | PASSING | `test/circuit.test.js` Test 4, T-POWER-NETWORK |
| Available capacity / Coulomb counting | `_batteryChargeC` tracking in the battery post-solve block | PASSING | `qualification.test.js` Gate 7, `test/circuit.test.js` T-BATTERY-CAPACITY |
| Voltage sag under load (droop) | `BATTERY_RINT` divider + `batteryEmfScale()` knee curve (`circuit.js:143`) | PASSING (flat-then-knee, not a linear droop — matches how a real primary cell behaves) | `qualification.test.js` #1 |
| Energy consumed | `_batteryEnergyJ` tracking, exposed via `res.batteryStates` | PASSING | `qualification.test.js` Gate 7 |
| Remaining capacity / state of charge | `bs.socFraction` in `batteryStates` | PASSING | `qualification.test.js` Gate 7, `regression-builds/16_battery_led_runtime.js` |
| Load-dependent runtime | derived: SOC depletes faster under heavier load, self-limiting as EMF droops | PASSING | `qualification.test.js` Gate 7 |
| 9V-alkaline-class reference capacity | documented as `BATTERY_9V_ALKALINE_AH = 0.5` (the "flashlight reference" the spec asked for), cross-checked against the simulator's own depletion model at a time-compressed scale | PASSING | `primitives.test.js` Primitive 9 |
| Losses (resistive, ESR, DCR) | `capacitorESR`, `inductorDCR`, `BATTERY_RINT`, MOSFET `RDS(on)` — all real, already covered under `01_PARTS` | PASSING | see `01_PARTS/MAP.md` |
| Efficiency (LED light-output wall-plug efficiency) | `LED_WALLPLUG_EFFICIENCY` (`circuit.js:101`) | PASSING | `qualification.test.js` Gate 7, `primitives.test.js` Primitive 10 |
| Explicit energy-balance closure check (source energy = stored-energy change + load energy + losses + declared residual) | not computed as one dedicated cross-check across an arbitrary circuit | **MISSING as a general-purpose check** — though the underlying pieces (integrated source energy via `Sim.integrateEnergy`/`Sim.powerFromVI`, per-component loss tracking) all exist and are individually proven; `primitives.test.js` Primitive 5's LC-exchange check is the closest existing example (`peakEarly`/`peakLate` totalenergy trend), but it's per-build, not a reusable "close the energy budget" primitive | `primitives.test.js` Primitive 5 (partial) |
| Thermal (self-heating, tempco) | `THERMAL_SPEC`, `updateTemp()` (`circuit.js:576`), resistor/MOSFET/H-bridge self-heating | PASSING for the parts it's modeled on | `test/circuit.test.js` T-THERMAL |

## Known gap worth calling out explicitly

The canon's energy-accounting rule ("If energy accounting does not close within
declared tolerance, the run receives a warning or FAIL") does not yet exist as a
standalone, reusable check any build could invoke. Every individual piece
needed to build it already exists and is tested (integrated source energy,
per-part loss tracking, stored-energy formulas). This is real, scoped future
Layer-08 work — not a physics gap, an accounting-composition gap.
