# Balanced Base Cell P0

Status: **design specification; bench unvalidated**

## Purpose

The base cell is the smallest measurable balanced state. It presents two
opposed channels around one continuously measured center reference `V0`.

```text
negative side  <----  V0  ---->  positive side
      -1              0                 +1
   decrease          HOLD             increase
```

The cell does not decide what the state means. A flashlight may map it to
brightness, a speaker to requested gain, a sensor to signed error, and a rover
or drone to a bounded setpoint lean.

## Reference rule

`V0` is a measurement and control reference. It is **not** the normal load
current return. Route load current separately so that wire, connector, or load
drop cannot silently move the reference. Where practical, sense `V0` with a
high-impedance or Kelvin-style connection.

For every sample record:

```text
Vplus      = positive channel relative to V0
Vminus     = negative channel relative to V0
differential = Vplus - Vminus
common_mode  = (Vplus + Vminus) / 2
reference_error = measured V0 - declared V0
```

Balanced does not mean the two sides must always be equal. It means any
intended differential and any unintended common-mode/reference movement are
both visible.

## P0 hardware blocks

- bounded low-voltage source with current limiting;
- stable center/reference generator appropriate to the source and load;
- opposed positive and negative paths;
- separate load-current return;
- test points for `V+`, `V0`, `V-`, source current, and load current;
- voltage/current sensing on both sides;
- temperature sensing where a coil, MOSFET, LED, or power stage can heat;
- magnetic/Hall sensing only when a magnetic state is actually under test;
- protection sized for the real source and components.

MOSFET, Hall, TMR/MTJ, capacitive, or magnetic gates are candidate interfaces.
No candidate becomes canonical until its leakage, offset, hysteresis, heat,
noise, and failure state have been measured. Resistors remain allowed for LED
limiting, sensing, damping, bias, and protection where real physics requires
them.

## Cell state

| Ternary request | Meaning | Required behavior |
|---|---|---|
| `-1` | decrease / negative lean | Move one bounded step below the held target |
| `0` | HOLD | Apply no new differential step; preserve the admitted operating state |
| `+1` | increase / positive lean | Move one bounded step above the held target |

The at-rest state is the latest stable held state, not an automatic return to
an old zero. A safety STOP is separate: it may remove energy or replace the
held target according to the device's safety design.

## Acceptance tests

1. Verify polarity and labels before energizing a load.
2. Measure both sides relative to `V0`, then measure the differential directly.
3. Apply matched loads and record symmetry error.
4. Apply unequal loads and prove reference movement is exposed rather than
   hidden.
5. Request `-1`, `0`, and `+1`; confirm direction and bounded magnitude.
6. Release the user input during HOLD and verify that the selected state
   persists when persistence is required.
7. Interrupt or invalidate a sensor input and verify the configured safe state.
8. Record energy, heat, noise, saturation, and recovery.

Each result must contain `expected`, `actual`, `tolerance`, and `PASS/FAIL`.

## Further development needed

- Select and characterize a real `V0` implementation under unequal dynamic
  loads.
- Define voltage/current envelopes for each device class rather than sharing
  one arbitrary range.
- Bench-qualify the preferred bilateral magnetic/MOSFET nerve gate.
- Decide which held states require nonvolatile magnetic memory and which should
  remain ordinary controlled state.
- Add connector and wiring rules that prevent load current from sharing the
  reference conductor.
- Produce repeatable scope captures and a conventional control comparison.

