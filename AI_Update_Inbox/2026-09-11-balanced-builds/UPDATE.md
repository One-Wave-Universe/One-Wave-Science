# Update: Balanced Device and Cell Build Packet

- Update ID: `2026-09-11-balanced-builds`
- Repository: `One-Wave-Universe/One-Wave-Science`
- Base branch: `main`
- Base SHA: `e17c68d81eb9a61ba1afdddc451cbc72b16a305c`
- Operation: additive documentation
- Status: proposed for review

## Purpose

Add the current balanced base-cell, sensor-cell, action/nerve-cell, brain-cell,
speaker, rover, and drone plans while making every missing simulation, bench
measurement, integration decision, and safety gate visible.

## Invariants

- One reference is carried through each handoff.
- `V0` is not the normal load-current return.
- HOLD preserves the current admitted target; it is not automatic zero output.
- Views travel up and admitted Actions travel down through the same
  bidirectional gate; direction does not create a second gate family.
- Each last Action Down produces a physical result that returns as the new View
  Up; the return is neither an echo nor an automatic reset.
- Three complete nerve cycles feed one higher-brain function; safety and native
  controller override may preempt the group immediately.
- Brain, sensor, and three-winding action/nerve cells remain distinct.
- Native vehicle controllers retain stabilization, mixing, arming, and
  failsafes.
- Gyro-fed native stabilization remains active inside a calibrated safe
  envelope; external leans are clipped/rejected and cannot suppress it.
- Proposed geometry, magnetic switching, and reinjection remain unvalidated
  until measured against controls.

## Test boundary

This update contains documentation checks only. It records no new simulator,
bench, rover, or flight result.
