# Latest Balanced Build Status — 2026-09-11

This is the current honest boundary between definitions, simulations, software
contracts, and physical evidence.

| Build | Defined now | Existing evidence | Current status | Smallest next proof |
|---|---|---|---|---|
| Balanced base cell | `cells/BALANCED_CELL_P0.md` | Earlier VBB differential/virtual-ground tests | Partly simulated; new contract bench-unvalidated | Unequal-load `V0` and differential test with recorded tolerance |
| Sensor cell | `cells/SENSOR_CELL_P0.md` | Existing simulator/sensor utilities, not one frozen packet | Specification only | Machine-readable packet plus polarity/stale-data tests |
| Three-winding action/nerve cell | `cells/ACTION_NERVE_CELL_P0.md` | Python command-shape unit test and VBB coupled-winding models | Software shape tested; physical behavior unvalidated | Characterize one/two/three windings with current, heat, and `Bx/By/Bz` logs |
| Brain cell | `brain/BRAIN_CELL_P0.md` | Separate triad, routing, command-memory, and test modules exist | Pieces exist; end-to-end recurrence unvalidated | Recorded Views Up -> decision -> bounded Action Down -> replay test |
| Flashlight | Existing `flashlight/` documents | 5 V VBB topology reported; no matched-output physical result | Simulated topology only | Valid 9 V control path and matched-brightness energy comparison |
| Speaker | `speaker/BALANCED_SPEAKER_P0.md` | No integrated simulation or bench data | Hypothetical design | Conventional reference plus low-power differential-drive simulation |
| QC-RC rover | `mobility/QC_RC_ROVER_DRONE_P0.md` | Architecture only | Proposed | Controller choice, wiring map, simulator, then manual ground test |
| QC-RC drone | `mobility/QC_RC_ROVER_DRONE_P0.md` | Architecture only | Proposed; no flight evidence | Native-controller software-in-loop HOLD/lean/link-loss test |
| Magnetic/non-contact switching | Candidate in flashlight/cell documents | Individual magnetic concepts; no complete qualified switch | Development needed | Leakage, hysteresis, bilateral conduction, heat, and failure-state bench test |
| Reinjection | Existing flashlight simulation claims and lock document | No physical net-energy advantage | Experimental | Source/storage/load energy accounting against continuous-drive control |
| Shared up/down gate | Cell and brain contracts | Bilateral-gate concept; no integrated turnaround test | Defined, unvalidated | Rapid Action Down/new View Up alternation with measured cycle rate, latency, jitter, and no role confusion |

## Recommended build order

1. Finish the Virtual Breadboard qualification tests required by
   `CURRENT_BUILD_ORDER.md` without removing existing working behavior.
2. Freeze the balanced view/action packet and test it with recorded data.
3. Run the brain-cell recurrence headlessly with deterministic replay.
4. Test the same bounded HOLD/lean protocol in a flight-controller simulator.
5. Build the rover and prove manual override, timeout, and sensor-invalid paths.
6. Complete flashlight and speaker control comparisons on low-voltage benches.
7. Establish a conventional stable drone before connecting external setpoints.
8. Test one bounded flight lean only after the earlier gates pass.

## Claims boundary

- Drawings and aligned geometry are proposals, not field measurements.
- Three triangles or three axes may be useful coordinate relationships; they do
  not prove a new physical effect by themselves.
- `BC-DC`, `TC-AC`, and `QC-RC` remain working engineering shorthand whose
  useful behavior must be tied to measurements.
- The five lifecycle states are process stages, not proof of a five-level
  physical primitive.
- No runtime, efficiency, lift, stability, spherical-field, or reinjection
  benefit is accepted without a conventional control and recorded result.
