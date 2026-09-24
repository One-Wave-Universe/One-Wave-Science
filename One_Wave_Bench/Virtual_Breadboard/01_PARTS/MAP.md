# Layer 01 — Parts

## Canon

A part knows about itself (pins, parameters, operating state, electrical
relationships, losses/limits where modeled, measurement exposure). It does not
know what project is using it.

## Status: implemented, not yet physically split

Every part below lives inside `js/circuit.js`'s single `Circuit` class, as one
`c.type === '<name>'` branch inside three shared per-part sections: the DC/AC
stamp loop (~line 950-1290), the post-solve current/state computation (~line
1850-2090), and small helper functions near the top of the file (~line 100-460).
No part is yet its own file/module. That is real, tracked debt (see
`../00_RULES/architecture.md`'s No-Rebuild Protection) — not a reason to leave it
unmapped.

| Part | Stamp | Current/state readback | Spec/helpers | Status | Covering tests |
|---|---|---|---|---|---|
| Resistor | `circuit.js:953` | `circuit.js:1854` | plain Ohm's law + power-rating warning | PASSING | `qualification.test.js` #2, `regression-builds/01_resistor_divider.js` |
| Capacitor | `circuit.js:996` | `circuit.js:1865` | `capacitorESR`/`capacitorLeakageR`/`capInitialV` (`circuit.js:229-256`) | PASSING (real ESR, leakage, initial condition) | `qualification.test.js` Gate 4, `primitives.test.js` Primitive 5 |
| Inductor | `circuit.js:1342` (stamp, in the time/dynamics extra-row block) | `circuit.js:1915` | `inductorDCR` (`circuit.js:210`) | PASSING (real DCR, continuous current) | `qualification.test.js` Gate 4, `regression-builds/05_lc_ringdown.js` |
| Diode / LED | `circuit.js:1023` | `circuit.js:1860` | `forwardVoltage`/`forwardRon` (`circuit.js:458-462`), `ledLightOutputW`/`LED_WALLPLUG_EFFICIENCY` (`circuit.js:101`) | PASSING (real Vf + dynamic Ron, per-color light output) | `qualification.test.js` #4/#5, `primitives.test.js` Primitive 10 |
| NMOS / PMOS | `circuit.js:1037` | `circuit.js:1925` | `mosfetSpec`/`NMOS_PARTS`/`PMOS_PARTS` (`circuit.js:343`), `MOSFET_OFF_LEAKAGE_G` | PASSING (real Vth, RDS(on), gate cap, body diode, off leakage) | `qualification.test.js` Gate 3, #12, #13 |
| Switch / pushbutton | union at `circuit.js:657` (no stamp — a closed switch is a wire) | `circuit.js:1900` | — | PASSING | `test/circuit.test.js` Test 7, 9 |
| Potentiometer | `circuit.js:978` | `circuit.js:1898` | — | PASSING | `test/circuit.test.js` (pot precision tests) |
| Battery / diffsource | `circuit.js:1202` | `circuit.js:1202+` (current computed alongside the battery block) | `BATTERY_RINT`, `BATTERY_MAX_CURRENT`, `batteryEmfScale` (`circuit.js:143`) | PASSING (internal resistance, current-limit brownout, Coulomb-counted capacity, knee discharge) | `qualification.test.js` Gate 7, #1, `primitives.test.js` Primitive 9 |
| AC source | `circuit.js:1264` | `circuit.js:1919` | `wave()` (`circuit.js:451`), `AC_RINT` | PASSING | `qualification.test.js` #8/#9/#19/#20 |
| Comparator (TLV3202-class) | `circuit.js:1100` | `circuit.js:1979` | `COMPARATOR_SPEC` (`circuit.js:364`) | PASSING (real Vos offset, propagation delay, push-pull output with current limit) | `qualification.test.js` #16, `primitives.test.js` Primitive 2/3 |
| Schmitt trigger | `circuit.js:1186` | `circuit.js:2073` | `SCHMITT_SPEC` (`circuit.js:434`) | PASSING (real, distinct upper/lower thresholds) | `qualification.test.js` Gate 5, #18 |
| H-bridge | `circuit.js:1137` | `circuit.js:2021` | `HBRIDGE_SPEC` (`circuit.js:401`) | PASSING (thermal shutdown, body diodes) | `qualification.test.js` #14 |
| Latching relay | `circuit.js:964` | `circuit.js:1964` | `LATCHRELAY_SPEC` (`circuit.js:306`) | PASSING | `test/circuit.test.js` (latch relay tests) |
| Ferrite toroid | in the time/dynamics extra-row block (`circuit.js:1369`) | `circuit.js:1923` | mutual coupling via `k*sqrt(L_i*L_j)` | PASSING | `qualification.test.js` #19/#20 |
| Square-loop memory core | `circuit.js:1400`-ish (Faraday's-law induced-voltage block) | `circuit.js:1962` | remanent flux state, real coercive threshold | PASSING | `test/circuit.test.js` T-CORE-LOCK/HOLD/GATE-MEM/etc. |
| MTJ angle sensor | `circuit.js:1272` | `circuit.js:1921` | quadrature sin/cos pair | PASSING | `test/circuit.test.js` Test 14 |
| Virtual ground (vgnd/TLE2426-class) | `circuit.js:1223` | `circuit.js:1902` | `VGND_RINT`, `VGND_MAX_CURRENT` | PASSING (real load regulation + current limit, rail-clamped) | `qualification.test.js` Gate 1 |

## Known gaps (MISSING, not silently assumed)

- Resistor/MOSFET RDS(on) temperature coefficients exist (`RESISTOR_TEMPCO`,
  `MOSFET_RDSON_TEMPCO`, self-heating via `THERMAL_SPEC`), but arbitrary magnetic
  core *material* parameterization beyond the fixed `hcAmpTurns`/`switchTau`
  model is MISSING — carried over from pre-existing backlog item "Magnetic core
  real material parameterization" (still pending in the task tracker).
- No standalone per-part documentation file exists yet (this table is the first
  one) — a future Layer-01 worker's job is to give each part its own file under
  `01_PARTS/<part>/`, not to change any of the physics above while doing it.
