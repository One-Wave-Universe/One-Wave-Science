# Sensor Cell P0 — Views Up

Status: **interface specification; hardware and integration unvalidated**

## Purpose

The sensor cell observes. It converts paired measurements into a referenced
view for the brain or flight controller. The view travels upward through the
same bidirectional gate/interconnect later used for an admitted action in the
opposite direction. The sensor does not gain action authority merely because
the physical gate is shared.

```text
physical state -> paired sensing -> reference check -> shared bilateral gate -> View Up
```

## Minimum view packet

```json
{
  "axis": "x|y|z|yaw|device-specific",
  "direction": -1,
  "phase": 0.0,
  "strength": 0.0,
  "reference": 0.0,
  "quality": 0.0,
  "valid": true,
  "sequence": 0,
  "timestamp_us": 0,
  "source": "sensor-id"
}
```

Units, coordinate frame, range, and sign convention must be declared beside
the packet schema. `quality` does not repair bad data; it lets the receiver
HOLD, defer, or reject it.

## Candidate sensing blocks

- paired rail voltage and current sensing;
- 3-axis Hall or magnetometer sensing for `Bx`, `By`, and `Bz`;
- IMU acceleration and angular-rate sensing for mobile builds;
- wheel encoders for the rover;
- barometer/range/position input for vertical flight control;
- temperature sensing at windings, switches, batteries, and power stages;
- optional light and audio feedback for the flashlight and speaker.

No single sensor is the reference for every scale. The cell must declare what
it measures, what it cannot observe, and the conditions that make it invalid.

## Balanced registration

1. Measure both opposed channels at the same time where practical.
2. Subtract the declared reference to produce signed error.
3. Preserve common-mode movement as diagnostic data.
4. Calibrate offset, gain, axis alignment, temperature drift, and noise.
5. Register `x/y/z` orientation physically on the enclosure or frame.
6. Reject stale, impossible, saturated, or frame-mismatched samples.

## Acceptance tests

- Positive and negative physical inputs produce the expected signed view.
- A true HOLD band does not chatter between `-1` and `+1`.
- Reversed wiring or reversed axis registration fails visibly.
- Removing one sensor cannot manufacture a valid lean.
- Sequence and timestamp checks reject stale or repeated packets.
- Every recorded action can be paired with the view and reference that caused
  it.
- After an Action Down, sample the resulting state and label it as the **new
  View Up caused by/observed after that last action**, using the linked sequence
  identifier.
- The same physical/link gate passes a valid view upward and an admitted action
  downward without losing direction, reference, or sequence identity.

## Further development needed

- Freeze the packet schema and units in machine-readable form.
- Choose sensors for the flashlight, speaker, rover, and drone separately.
- Establish noise floors and deadbands from data rather than intuition.
- Build a calibration fixture for physical `x/y/z` registration.
- Implement sensor disagreement and degraded-quality handling.
- Prove that motor/ESC/coil noise cannot shift `V0` or fabricate direction.
- Define the turnaround/arbitration rule that prevents an upward view from
  reflecting back as an unauthorized action on the shared gate.
