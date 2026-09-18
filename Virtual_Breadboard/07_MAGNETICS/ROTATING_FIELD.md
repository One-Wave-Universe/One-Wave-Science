# Rotating-Field Experiment, Hold, and Recovery

**Status:** experimental magnetic/control test.  
**Reference baseline:** conventional three-phase motor commutation.

A sequence that energizes spatially separated A/B/C coils can produce a **stepped field-direction sequence** if the winding geometry and current polarity are correct. That must be measured.

Do not automatically call one-live-coil A→B→C stepping a conventional three-phase rotating magnetic field.

For a standard three-phase BLDC six-step drive, an electrical cycle is divided into six 60-degree sectors and two of the three phases are normally energized in each sector.

Reference:
https://onlinedocs.microchip.com/oxy/GUID-3AFF556D-77AD-488F-9A04-CD7AAB8F7DBC-en-US-1/GUID-A1DD3CA4-D59F-45CF-AA9F-EBBCB9EF37BA.html

## Experiment A — field-direction stepping

Use three physically separated coils with declared orientation.

```text
step 1 -> energize A with measured polarity/current
step 2 -> energize B with measured polarity/current
step 3 -> energize C with measured polarity/current
```

Measure with a Hall probe, vector magnetometer, or calibrated search-coil geometry.

Pass:
the measured field vector changes direction in the intended ordered sequence.

Fail:
only coil-local amplitude changes, or the measured direction does not follow the declared order.

This proves **stepped field direction**, not yet smooth rotation.

## Experiment B — conventional comparison

Build or model a conventional three-phase six-step sequence using an appropriate bridge/driver and the same or comparable coil geometry.

Compare:
- field-vector trajectory;
- current;
- ripple;
- torque/force if a rotor/load is present;
- reversal.

The One-Wave sequence earns a rotating-field claim only to the extent the measured field actually rotates.

## HOLD

All drive current removed is not automatically HOLD.

A persistent magnetic-state claim requires a drive-off measurement that exceeds:
- L/R decay;
- capacitor storage;
- diode/MOSFET reverse recovery;
- Hall offset/drift;
- thermal drift;
- instrument zero.

If the measured state falls to the control/noise floor, the system had driven field, not retained magnetic memory.

## Recovery / reinjection

Magnetic or inductive energy recovery is real engineering when energy is intentionally routed back to a DC-link/storage element through a defined path.

Measure:
- energy supplied to the event;
- reservoir energy before/after;
- recovered energy;
- energy reused later;
- losses.

The virtual midpoint/reference is not the recovery reservoir.

## Views and actions

Sensor return and actuator command may share one logical sequence identifier, but they remain different physical signal paths unless the hardware proves otherwise.

Do not label a shared timestamp or controller state as a shared physical current path.

## Required receipts

For each run record:
- winding geometry and polarity;
- current waveform;
- drive sequence;
- measured magnetic field vector or calibrated proxy;
- drive-off decay;
- reservoir voltage/energy if recovery is claimed;
- control run;
- temperature;
- PASS/FAIL reason.

G-778 applies.
