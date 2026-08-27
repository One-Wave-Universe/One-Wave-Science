# C1 — Deterministic Path Motion Fitter

**Status: RUNTIME PASS**

## Production problem exposed
The first forest walk proved that manual size stations look jumpy. Depth and size must be generated from one continuous path instead.

## What C1 adds
- Fit an existing consecutive pose run to a start/end path.
- Start/end X positions.
- Start/end feet/base depth.
- Optional smoothstep easing near the near/far ends.
- Reverse-path button for the return walk.
- Existing pose artwork is preserved.
- Manual scale is preserved.
- Existing background calibration continues to control automatic perspective size from feet depth.

## Runtime verification
Chromium test passed:
- 7-frame forward depth progression was monotonic and eased from 0.90 to 0.50.
- reverse path reproduced the mirrored 0.50 to 0.90 progression.
- pose image identity remained unchanged across all frames.
- manual scale remained unchanged across all frames.
- zero page errors.

## Next
C2 — Walk cadence / pose-beat fitter.
