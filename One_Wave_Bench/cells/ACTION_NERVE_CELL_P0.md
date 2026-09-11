# Three-Winding Action / Nerve Cell P0 — Actions Down

Status: **software contract exists; physical cell unvalidated**

## Purpose

This is the fast local action layer. It accepts an already-authorized bounded
request through the same bidirectional gate that carries measured return
upward, then expresses the request through three coupled windings or a
compatible actuator adapter. It is not the brain and does not create its own
goal.

```text
authorized Action Down => shared bilateral gate => three phases
measured return       <= same bilateral gate  <= sensor/reference
```

## Locked distinction

- **Brain cell:** compares views and grants, defers, denies, or overrides.
- **Action/nerve cell:** performs a bounded local action and returns measurement.
- **Sensor cell:** observes the action and sends the view upward.

Existing software contract:

```text
One_Wave_Bench/brain/nerve_three_winding.py
One_Wave_Bench/brain/test_nerve_three_winding.py
```

That code proves only command-shape rules. It is not evidence that a physical
three-winding motor, magnetic switch, or nerve is stable or efficient.

## Ternary action

| Command | Local meaning |
|---|---|
| `-1` | Apply one bounded negative/decrease lean |
| `0` | HOLD the current admitted target; no new correction |
| `+1` | Apply one bounded positive/increase lean |

Three windings remain independently measured. `3:1` names the local
three-phase/one-reference relationship. It does not grant authority and does
not turn the windings into a brain.

There is one bilateral gating action, used in both directions. Do not draw a
separate "up gate" and "down gate" unless a physical isolation test later
requires two components. The brain/controller owns the direction change and
admission decision.

After the admitted Action Down changes the physical state, the sensor reads the
result and sends a **new View Up** through that same gate. The new view must cite
the last action sequence so the loop can compare requested change with actual
change.

The gate can flip direction rapidly so a person may not notice the handoff, but
the controller must still measure and budget the real turnaround delay. The
local action rate cannot exceed the rate at which a trustworthy new view and
higher-level admission can return.

## P0 hardware blocks

- three characterized windings on a declared geometry/core;
- current and temperature measurement per winding;
- shared reference sensing that does not carry normal winding current;
- reversible/bilateral switching candidate per phase;
- voltage transient and flyback protection;
- independent emergency energy removal;
- local controller or adapter that enforces current, temperature, slew, and
  duration limits;
- sensor-return path independent of the command path.

Magnetic/non-contact switching is a development target. Until it is proven,
the physical prototype may use conventional protected switching as the control
baseline, clearly labeled as a control rather than claimed One-Wave proof.

## Drone and rover boundary

On a drone, this experimental cell never bypasses the native flight controller
or sends raw motor commands. The flight controller retains stabilization,
mixing, arming, and failsafes. The experimental layer may request only bounded
setpoint leans through a supervised interface.

On the rover, the same rule applies at lower risk: a drive controller retains
current limiting and stop authority while the nerve request changes bounded
speed or steering targets.

## Acceptance tests

1. Verify phase identity, polarity, resistance, and insulation unpowered.
2. Characterize one winding, then two, then three—one change per test.
3. Log commanded state, all three currents, field vector, temperature, and
   mechanical response on one sequence identifier.
4. Prove HOLD does not command a zero-output reset.
5. Prove local limit enforcement and higher-level override.
6. Disconnect the command stream and verify the declared recovery behavior.
7. Compare measured response with a conventional actuator/control baseline.

## Further development needed

- Physical winding geometry, turns, wire gauge, core, resistance, inductance,
  saturation, and thermal envelope.
- A tested bilateral switch with known leakage and failure behavior.
- Closed-loop current control that preserves the reference.
- Measured `Bx/By/Bz` reconstruction instead of inferred field drawings.
- Adapter contracts for speaker, rover, and flight-controller setpoints.
- Turnaround timing, collision avoidance, and direction tagging for the shared
  bidirectional gate.
- Measured cycle frequency, worst-case round-trip latency, and jitter limits for
  each target device.
- Fault injection for stuck phase, open phase, shorted phase, bad sensor, and
  lost higher-level command.
