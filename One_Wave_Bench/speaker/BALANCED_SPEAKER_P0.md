# Balanced Speaker P0

Status: **hypothetical design; not simulated or bench tested**

## Goal

Build a practical low-power speaker test that compares a balanced differential
signal/drive path with a conventional reference at matched perceived volume.
The target is clean useful listening, low idle power, symmetry, and noise
rejection—not maximum loudness.

## Architecture

```text
audio input -> balanced sensor/input cell -> bounded gain state
            -> differential amplifier/control stage -> speaker motor
            -> current/cone/audio return -> new held state
```

The cone's mechanical rest position is centered. The user's volume setting is
a separate held state. Therefore HOLD does not force the volume to zero; it
means no new volume correction while the selected gain remains registered.

## P0 comparison

Build two paths using the same source, battery/supply, driver, enclosure,
program material, and listening position:

1. conventional known-good amplifier/control;
2. proposed balanced differential path.

Record idle power, average power at matched output, hum/noise, clipping,
distortion where measurable, cone asymmetry, temperature, and battery runtime.

## Sensor and action split

- Sensor cell: input level, output level, supply, current, temperature, and
  optional cone-position measurement.
- Brain/control cell: selected volume, limits, mute/sleep policy, and fault
  response.
- Action cell: differential electrical drive to the speaker motor.
- Mechanical speaker motor: centered rest, measured inward/outward behavior.

## Further development needed

- Select the speaker driver, enclosure, power target, battery/supply, and
  conventional reference amplifier.
- Choose or design a safe differential output stage; characterize DC offset
  before connecting the driver.
- Determine whether the proposed three-winding geometry adds a measurable
  benefit or only heat, mass, and complexity.
- Implement non-mechanical volume sensing without allowing accidental changes.
- Define the HOLD, mute, sleep, wake, clipping, overcurrent, and overtemperature
  states separately.
- Create VBB models/tests for differential audio drive and the speaker load.
- Bench-test at low power before any permanent perfboard build.

