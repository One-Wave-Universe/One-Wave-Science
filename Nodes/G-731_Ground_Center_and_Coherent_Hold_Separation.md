# G-731 — Ground, Center, and Coherent Hold Separation

**Status:** YELLOW finite classifier / physical thresholds uncalibrated  
**Dependencies:** B-208, B-216, B-222, G-727–G-730

## Required separation

The following are not synonyms:

1. **Logical Ground:** no committed YES/NO relation and resolved activity below
   declared logical thresholds. This does not claim that the physical Field or
   vacuum contains no energy.
2. **Center residence:** position lies inside the shared-center band.
3. **Center crossing:** position is inside that band while movement is nonzero.
4. **Movement Hold:** net movement lies inside the speed band.
5. **Turning-point Hold:** movement is Hold while position is outside the center.
6. **YES/HOLD and NO/HOLD:** two distinct six-route addresses carrying the
   same movement projection but different binary relations.
7. **Coherent Hold:** a committed relation with movement Hold, phase lock,
   retained energy, and retained topology.

## Receipt fields

Every classification emits independent values for:

```text
logical_ground
at_center
movement
binary_relation
route
phase_locked
energy_retained
topology_retained
coherent_hold
turning_point_hold
center_crossing
```

This prevents a zero in one channel from erasing activity in another.

## Important consequences

- A fast center crossing is not movement Hold.
- A turning point may be movement Hold while far from the shared center.
- Zero velocity with lost phase, energy, or topology is not coherent Hold.
- YES/HOLD and NO/HOLD remain distinguishable.
- Uncommitted but measurable activity is not logical Ground.
- Logical Ground is outside the six committed routes.

## Open calibration

Center width, speed width, phase-lock threshold, retained-energy threshold,
topology threshold, and observation duration are demonstration parameters.
A6 and B1–B6 must derive or calibrate them under noise, delay, nonlinear
motion, phase slip, and Break/Loop events.

## Executable authority

- `One_Wave_Bench/logic_core/ground_hold_classifier.py`
- `One_Wave_Bench/logic_core/test_ground_hold_classifier.py`

The combined logic suite contains thirty-eight passing tests.
