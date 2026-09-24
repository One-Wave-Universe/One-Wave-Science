# Wave Reader V1 Hardware Specification

**Status:** UNVERIFIED HARDWARE PROPOSAL — build/test/dismiss

## Purpose

Wave Reader V1 is a measurement-first acquisition path for observing voltage, current, and field-related signals from experimental One-Wave hardware.

## Proposed signal-acquisition pipeline

```text
sensor / probe
-> input protection
-> RC anti-alias filtering
-> reference-aware differential acquisition
-> ADC capture
-> timestamp
-> calibration transform
-> raw + processed storage
-> comparison / visualization
```

## Proposed V1 components

- **ADC:** ADS131A02 differential ADC
- **Proposed sample rate:** 128 kSPS
- **Anti-alias filtering:** RC input filter arrays
- **Primary compute target:** NVIDIA Jetson Orin
- **Additional edge compute target:** HP EliteDesk 800 G4 Mini

These are proposed hardware choices and are not considered qualified until electrical compatibility, timing, driver support, channel count, noise, and throughput are verified.

## Minimum acquisition channels

1. DUT signal
2. reference node
3. supply/recovery rail
4. optional field or coil-current channel

## Required measurements

- absolute voltage relative to instrument ground;
- differential voltage relative to declared circuit reference;
- current where relevant;
- actual sample rate;
- usable bandwidth;
- noise floor;
- ADC reference stability;
- calibration source/date.

## V1 qualification tests

1. Capture a known calibration waveform.
2. Verify amplitude and frequency error.
3. Confirm 128 kSPS mode if supported in the selected configuration.
4. Measure effective noise and ENOB in the actual front end.
5. Confirm differential/common-mode input limits.
6. Save raw samples and metadata.
7. Reproduce capture after restart on the Jetson.
8. Repeat on the HP EliteDesk path if retained.

## Evidence rule

Do not label traces as reinjection, memory, Field, Void, lattice density, or wave collapse solely from shape. Raw observables come first; interpretation is a separate tagged layer.

## Dismissal rule

Any component choice or interpretation that fails the declared acceptance test should be marked failed/superseded rather than protected because it is part of the hypothesis.
