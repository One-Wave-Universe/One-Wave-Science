# VIRTUAL BREADBOARD QUALIFICATION SUITE

The virtual breadboard must remain useful across the whole build program. New project requirements extend the simulator; they do not justify rewriting working subsystems.

## Fundamental circuit regressions

Keep these as permanent runnable tests.

1. DC source
2. resistor / Ohm's law
3. series / parallel resistor networks
4. voltage divider and loaded divider
5. LED + current limiting
6. diode forward/reverse behavior
7. simple rectifier
8. capacitor charge/discharge
9. RC low-pass
10. RC high-pass
11. inductor current ramp / flyback
12. LC/RLC storage and ringdown
13. MOSFET low-side switch
14. MOSFET high-side switch
15. push-pull / half bridge with shoot-through detection
16. full bridge / differential load
17. passive virtual ground and loaded midpoint sag
18. buffered / active virtual reference where supported
19. comparator threshold
20. comparator with hysteresis
21. basic relaxation oscillator
22. transformer / coupled coils
23. three coupled windings
24. battery discharge and source resistance
25. balanced differential load
26. reinjection storage loop

## Required measurement primitives

- node voltage
- differential voltage
- branch current
- source current
- instantaneous power
- integrated energy over time
- average current
- RMS voltage/current
- frequency
- phase difference
- duty cycle
- transient graph / scope trace
- battery energy/capacity remaining
- source/internal resistance effects
- temperature placeholder/model where supported
- machine-readable export

## Required reusable build primitives

### Shared-center differential primitive

Expose `+`, `CENTER`, and `-`. Both sides must be measurable relative to CENTER and directly against each other. Unequal loading must be able to disturb the center unless the chosen reference stage is designed to hold it.

### Field/Void validation primitive

A proposed state change must not become a committed output transition until its validation condition is satisfied. HOLD remains a real observable condition.

Implement this from ordinary simulated electronics / logic elements. Do not hide it behind an unexplained custom macro.

### Ternary resolved-state primitive

Externally expose `- / HOLD / +` from actual threshold/differential conditions.

### Hysteretic reinjection primitive

Storage decays naturally; lower threshold connects the source; upper threshold disconnects the source; record source duty cycle and energy.

### Energy-storage primitive

Support capacitor, inductor, and LC tests with explicit configurable losses.

### Balanced-load primitive

Matched branches with deliberate mismatch injection and separate common-mode/differential measurements.

### Phase-handoff primitive

One validated stage can enable another through real delay/RC behavior. Scope timing must expose the handoff rather than assuming ideal synchronization.

### Three-winding primitive

Three independently accessible winding models with polarity, coupling, phase, winding resistance, and independently measurable drive/sense behavior.

### Battery primitive

Nominal voltage, capacity, internal resistance, voltage sag, energy consumed, remaining capacity, and load-dependent runtime. A 9 V alkaline model is a priority because it is the first flashlight reference.

### LED primitive

Forward behavior, current, electrical power, and approximate relative light output. Red/blue/white channels must be distinguishable when the flashlight work reaches color testing.

## Standard test receipt

Every regression must produce:

```text
TEST:
EXPECTED:
ACTUAL:
TOLERANCE:
PASS/FAIL:
NOTES:
```

Waveforms alone are not a pass criterion.

## Update law for Claude / simulator work

Work in coherent subsystem batches, not giant rewrites and not one-line-at-a-time paralysis.

For each batch:

1. name one subsystem goal
2. identify its dependent regressions
3. preserve working behavior outside that subsystem
4. implement the smallest coherent set of changes that can satisfy the goal
5. rerun the affected fundamental regressions
6. run the new project-specific test
7. return actual measurements and failures
8. stop before starting the next subsystem

If a project build cannot be represented because the simulator lacks a physical behavior, add that behavior to the simulator and its regression suite. Do not change the proposed circuit merely to make the simulator pass.

## Flashlight qualification gate

Before the balanced flashlight is trusted in simulation, these must pass together:

`virtual ground -> differential measurement -> MOSFET switching -> energy storage -> hysteresis -> reinjection -> battery + LED runtime`

After this gate, the flashlight becomes the next regression fixture. Later, the speaker adds audio/noise/load behavior, and the three-winding nerve adds coupled magnetic behavior.
