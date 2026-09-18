# Motor Cell Specs

**Status:** experimental actuator interface.  
**Authority:** G-778 Build Logic / Research / Reference Validation Standard and `Virtual_Breadboard/BENCH_REALITY_CONTRACT.md`.

Do not use the logic-test breadboard as a motor power stage.

## F0 — bench nerve / command proof

This tier proves the command and sensing logic with a resistive or very small inductive dummy load.

| item | current authority |
|---|---|
| Supply | nominal 5 V protected/current-limited source |
| Mid/reference | TLE2426 or equivalent measured midpoint, signal/reference duty only |
| Initial load | 1 kΩ resistive dummy load |
| Switching | low-current MOSFET pair only after VGS is measured |
| Gate | explicit series resistor + OFF bias appropriate to the actual topology |
| Current | low mA first; midpoint imbalance kept well below TLE2426 capability |
| Measurement | supply current, midpoint drift, VGS, branch current, temperature |
| Motor | **not connected in F0** |

The TLE2426 is a rail splitter/reference part, not a motor return.

Reference:
https://www.ti.com/product/TLE2426

A 2N7000/BS170 may be useful for low-current switching experiments, but it is not the basis for a motor-current rating. Do not infer a safe motor stall current from a headline absolute-maximum transistor number.

## F1 — real actuator / motor tier

Move off the solderless breadboard.

Use:
- a proper three-half-bridge driver / ESC / motor-control module;
- a power source sized to the motor;
- explicit current limit or over-current protection;
- intentional freewheel/flyback paths;
- dead time where the chosen switching scheme requires it;
- rotor-position feedback, back-EMF logic, or a declared open-loop startup method;
- thermal monitoring.

Conventional three-phase BLDC six-step commutation is the comparison baseline. It divides an electrical cycle into six 60-degree sectors and typically energizes two of the three phases in each sector.

Reference:
https://onlinedocs.microchip.com/oxy/GUID-3AFF556D-77AD-488F-9A04-CD7AAB8F7DBC-en-US-1/GUID-A1DD3CA4-D59F-45CF-AA9F-EBBCB9EF37BA.html

## Ternary command mapping

The One-Wave command grammar may be tested as:

```text
DOWN / HOLD / UP
```

but that is a controller abstraction, not a motor topology.

A valid test must define how those three commands map to the real driver:
- direction/current/torque request;
- active braking or zero torque;
- opposite direction/current/torque request.

## Sensor cell

Candidate sensing may include:
- NTC temperature sensing;
- Hall magnetic/position sensing;
- encoder;
- current shunt;
- accelerometer/IMU;
- search coil.

Each sensor must use its actual datasheet transfer function and calibrated threshold. Placeholder thresholds such as “hash >> walk-level” are not acceptance criteria.

## Pass criteria

F0 passes when:
- the midpoint remains within its declared hold belt;
- VGS is sufficient for the claimed switch state;
- measured current matches the modeled range;
- no unexpected heating occurs;
- the DOWN/HOLD/UP command states are electrically distinguishable.

F1 passes only when:
- the motor/actuator responds reproducibly;
- current, voltage, phase/sector, position/torque where applicable, and temperature are recorded;
- a conventional driver/control case is available as a comparison;
- no power current is routed through the virtual midpoint.

## Not a spec

The following are not valid specifications by themselves:
- hover watts inferred from symmetry;
- “spintronic” without an actual spintronic device;
- motor stall current on a 2N7000 logic-test stage;
- PWM automatically equaling HOLD;
- a motor turning as proof of magnetic memory.
