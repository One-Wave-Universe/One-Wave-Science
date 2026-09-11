# Balanced QC-RC Rover and Drone P0

Status: **system plan; no vehicle build or flight evidence**

## Decision

Use a conventional supported flight controller as the hard real-time authority.
It owns sensor fusion, attitude/rate stabilization, motor allocation, arming,
pilot takeover, and failsafes. The One-Wave brain/sensor/nerve layer may send
only bounded high-level setpoint leans through a supervised adapter. It never
sends raw motor outputs.

This follows the current PX4 architecture, where quaternion attitude control,
rate control, and control allocation remain inside the flight stack:

- https://docs.px4.io/main/en/flight_stack/controller_diagrams
- https://docs.px4.io/main/en/flight_modes/offboard
- https://docs.px4.io/main/en/config/safety

ArduPilot may be used instead if selected for the prototype; companion systems
exchange telemetry and commands with the autopilot through MAVLink:

- https://ardupilot.org/dev/docs/companion-computers.html

## Authority stack

```text
pilot / safety switch
        |
native flight controller + native failsafes
        |
bounded setpoint adapter  <=== shared bidirectional link ===> One-Wave brain
        |                     Actions Down / Views Up
flight telemetry + sensor cells
        |
ESCs / motors / airframe
```

The native controller can reject or replace an external request at every step.
A lost, late, repeated, frame-mismatched, or out-of-envelope packet cannot
change the target.

At the One-Wave contract level, telemetry Views Up and admitted setpoint
Actions Down are opposite directions through the same bidirectional gate/link.
The transport may be MAVLink or another supported controller interface, but it
must preserve message direction and authority so telemetry cannot be mistaken
for a command.

The link may flip directions fast enough to appear continuous, but the native
flight controller—not this shared link—keeps the hard real-time stabilization
loop. Log update rate, round-trip latency, and jitter. Any missed deadline,
stale view, or expired action invokes HOLD or the configured native recovery
mode rather than extrapolating a new motor command.

The One-Wave companion groups three completed nerve cycles beneath one
higher-brain function. This 3:1 grouping applies only to the experimental
setpoint/measurement layer. It does not divide, replace, or slow the native
flight controller's attitude and rate loops. Native failsafes and pilot
override may preempt the group at any point.

### Balance while moving

For P0, the native flight controller is the implemented fast nerve layer:

```text
fast nerve/controller cycles: correct balance around the current target
higher-brain function:         lean the target for lift or direction
new fast cycles:               keep balance around the leaned target
```

Climb is not a raw increase to every motor and direction is not a raw motor
imbalance. They are bounded attitude/vertical setpoint changes. The controller
uses its measured state to allocate the corrections required to remain stable
while following the new target.

### Gyro safe envelope

The IMU gyroscopes provide the fast roll, pitch, and yaw-rate views used by the
native controller to maintain balance. Define safe attitude, angular-rate,
setpoint-slew, and recovery limits for the chosen airframe in simulation and
conventional flight testing; do not invent universal degree limits in this
architecture document.

Every higher-brain lean is clipped or rejected inside that calibrated envelope.
It cannot suppress gyro stabilization. A stale, saturated, implausible, or
disagreeing gyro signal invokes the selected native-controller fault/recovery
path and blocks new external leans.

## Balanced movement mapping

Each logical axis is expressed around its current admitted target:

| Axis | `-1` lean | `0` HOLD | `+1` lean |
|---|---|---|---|
| X / roll | bounded left lean | keep current roll target | bounded right lean |
| Y / pitch | bounded rear lean | keep current pitch target | bounded forward lean |
| Z / vertical | bounded descent request | hold altitude/vertical target | bounded climb request |
| Yaw | bounded turn left | keep heading/rate target | bounded turn right |

The adapter must translate these logical labels into the selected controller's
declared coordinate frame and sign convention. Do not assume drawing direction
equals firmware direction.

HOLD does not set motor output to zero. During hover it preserves the altitude
or zero-vertical-speed target while the native controller continuously adjusts
thrust to stay stable.

## Rover-first QC-RC build

The R2-style bucket rover is the first physical mobility host because it can
exercise the complete packet and authority path without flight consequences.

P0 blocks:

- stable wheeled chassis with differential drive;
- flight-controller/autopilot or compatible supervised controller;
- wheel encoders and IMU;
- manual controller with immediate takeover/stop;
- companion computer only after manual driving and native stabilization work;
- current, voltage, temperature, and command/response logging;
- optional decorative shell kept clear of cooling and stop access.

Rover tests: forward/back, left/right, HOLD-current-target, obstacle/sensor
invalid, command timeout, manual override, and recovery. Run one axis at a time.

## Quad-X drone build

P0 blocks:

- conventional proven Quad-X frame, motors, ESCs, propellers, and power system;
- supported Pixhawk-class or equivalent flight controller;
- calibrated IMU and altitude/position sensors appropriate to the test area;
- RC/manual pilot link and configured hardware safety/kill path;
- telemetry link;
- optional Jetson companion after the airframe flies stably without it;
- independent logs from flight controller and companion adapter.

Experimental magnetic switching, three-winding power stages, or reinjection do
not enter the ESC/motor power path during P0. Test them independently under
non-flight loads. Reinjection is an energy-recovery hypothesis, not an assumed
power source or endurance gain.

## Validation ladder

1. Software-in-the-loop simulation of packet, HOLD, limits, timing, and link
   loss.
2. Recorded telemetry replay with One-Wave outputs disconnected.
3. Props-off bench integration.
4. Rover ground tests with manual override.
5. Conventional airframe manual/native-controller flight with the experimental
   layer disabled.
6. Tethered or otherwise appropriately contained test as required by the test
   team and site.
7. One small external setpoint lean on one axis, immediate HOLD, measured
   comparison, then stop.
8. Expand only after repeated passes and experienced flight review.

## Mandatory acceptance tests

- Axis polarity and coordinate-frame registration.
- Gyro bias, vibration, saturation, disagreement, and safe-envelope enforcement.
- HOLD preserves the selected target and active stabilization.
- Setpoint magnitude, slew, duration, and mode limits.
- Stale/repeated/invalid packet rejection.
- External-link loss returns to the configured native recovery mode.
- Immediate pilot/manual override.
- Native battery, position, sensor, and data-link failsafes cannot be suppressed
  by the experimental layer.
- Every request, admission/rejection, measured response, reference, saturation,
  and energy measurement shares one sequence identifier.

## Further development needed

- Select PX4 or ArduPilot and one exact supported controller/airframe.
- Freeze coordinate frame, modes, setpoint types, limits, and timeout behavior.
- Implement and test the view/action packet adapter in simulation.
- Test turnaround, sequence, collision, and stale-direction handling on the
  shared bidirectional link.
- Establish measured update-rate, worst-case latency, and jitter budgets while
  the native controller remains stable under link delay and loss.
- Prove three experimental nerve-cycle receipts feed one higher-brain function
  without delaying native stabilization or override.
- Demonstrate HOLD, climb/descent, and one directional lean while logging that
  native balance correction remains active throughout each target change.
- Calibrate the gyro/attitude safe envelope for the selected controller and
  airframe, then prove out-of-range external leans are clipped or rejected.
- Define indoor/outdoor position and altitude sensing for the first site.
- Recruit an experienced autopilot integrator and pilot/test lead.
- Build the rover wiring diagram and parts list before purchasing duplicates.
- Produce an independent safety review and site-specific test checklist.
- Prove the conventional airframe before enabling any external leans.
