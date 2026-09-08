# Balanced Flashlight — State-Driven Reinjection Lock

## Purpose

This file locks the actual One-Wave flashlight architecture so a conventional
LED driver, timer loop, or binary-control IC cannot silently replace it again.

The flashlight is the first useful hardware host for the same balanced cell
architecture used later by BC-DC -> TC-AC -> QC-RC experiments.

## One reference, end to end

There is one continuously present virtual-ground / CENTER reference for the
whole chain.

```text
source rails
   |
   +---- +
   |
 CENTER / virtual ground = 0 reference
   |
   +---- -
```

Every state and handoff is resolved relative to this same reference:

```text
BC-DC (+ / 0 / -)
    -> TC-AC oscillation around the same 0
    -> QC-RC coordinated/rotating axes around the same 0
    -> state measurement around the same 0
    -> reinjection back into the same referenced state
```

No stage gets to invent a fresh local zero and still claim reference
continuity.

## Reinjection is state-triggered, not time-triggered

Canonical analogy: a bucket slowly empties under load. When the level gets low
enough, the state itself opens the refill path. The bucket fills back above its
allowed band, the refill path disconnects, and the bucket coasts again.

```text
FULL / state high
   |
source disconnected
   |
useful load consumes stored energy
   |
state decays naturally
   |
LOW THRESHOLD
   |
reinjection path opens
   |
short refill / restoration
   |
HIGH THRESHOLD
   |
reinjection path disconnects
   |
COAST
```

The elapsed time between events is an outcome of load, storage, losses, and
state. Time is not the trigger.

## Natural threshold first

A discrete MOSFET threshold is a legitimate first primitive because its gate
responds to an actual electrical differential. A single MOSFET threshold by
itself behaves more like a regulating valve than a true refill-and-coast loop,
so the final system needs real hysteresis.

The preferred One-Wave hysteresis source is magnetic state / coercivity where
possible, not a binary Schmitt-trigger IC.

Candidate progression:

1. discrete MOSFET threshold valve;
2. storage element and measured decay;
3. square-loop magnetic state with remanence / coercive thresholds;
4. magnetic-state-controlled reinjection gate;
5. prove lower threshold -> reinject -> upper threshold -> disconnect;
6. compare source energy against continuous drive at matched useful output.

## No binary controller IC in the prototype control path

Do not use an SN74/logic gate, binary MCU state machine, or comparator package
as the thing that *creates* the ternary/quadratic behavior for this experiment.
Those devices may remain elsewhere in the Virtual Breadboard as controls or
calibration references, but they are not the One-Wave flashlight controller.

The intended behavior comes from:

- balanced differential electrical state;
- MOSFET conduction thresholds;
- capacitance / inductance / coupled winding dynamics;
- magnetic remanence / coercivity;
- phase relationships;
- measured differential state around CENTER.

## Minimize resistive loss

Do not use resistor networks as the control architecture.

A resistor is allowed where real physics requires it, including:

- LED current limiting when the modeled/physical LED needs it;
- unavoidable winding resistance;
- a deliberately measured sense path where no lower-loss alternative exists;
- damping/protection required to keep a real circuit stable;
- a conventional reference circuit used only for comparison.

Every avoidable resistor should be treated as a loss candidate because its
power becomes heat.

## Persistent non-mechanical user controls

The flashlight should not require a conventional mechanical on/off or up/down
button as its canonical interface.

The user changes a stored state through a non-mechanical sensing interaction.
Candidate physical interfaces, in order of practical prototyping difficulty:

1. capacitive-touch/electric-field sensing from the user's finger;
2. Hall / magnetic position sensing;
3. MTJ/TMR magnetic state / angle sensing;
4. later field-coupled interfaces if bench evidence supports them.

The sensor changes the state; releasing the finger does not automatically
restore the old setting. Wherever the user leaves the state becomes the new
held setting until changed again.

The Virtual Breadboard may model the resulting electrical/magnetic state first
even when it does not yet model a human finger directly.

## Two user state axes

### X axis — wavelength / color

```text
RED  <-  NEUTRAL  ->  BLUE
 -             0             +
```

The exact LED/color implementation must remain independently measurable.
This axis is a user state coordinate, not a claim that arbitrary optical
wavelength can be generated continuously by one LED.

### Y axis — light level

```text
DARK  <-  BALANCED/NORMAL  ->  BRIGHT
  -              0                 +
```

Brightness is independently measurable from the color axis.

The shared centered state is therefore at minimum a 2D user-state plane:

```text
                 BRIGHT
                   +Y
                    |
RED  -X -------- CENTER -------- +X  BLUE
                    |
                   -Y
                  DARK
```

This state plane is not yet a 3D magnetic-field claim.

## BC-DC -> TC-AC -> QC-RC

### BC-DC — point/state

Establish and measure a stable differential state around the single CENTER:

```text
+ / CENTER / -
```

Purpose: prove the reference-resolved point/state.

### TC-AC — path/phase

Hand the validated differential into an out-and-back oscillation around the
same CENTER.

Purpose: prove reversible path, phase, and zero crossing without losing the
reference.

### QC-RC — coordinated rotation

Coordinate multiple independently driven phase relationships into a rotating
relationship across axes.

Two phase-shifted AC axes can produce a rotating drive vector in a plane. A
third independently driven axis can tilt/precess that drive vector through 3D.
The electrical drive vector must remain referenced to the same CENTER.

Do not claim a spherical or volumetric magnetic field from a schematic.

Required eventual measurement:

```text
B(t) = (Bx(t), By(t), Bz(t))
```

The measured trajectory decides whether the result is circular, elliptical,
planar, precessing, volumetric, spherical-like, unstable, or something else.

## Current Virtual Breadboard capability boundary

Already available and tested in the VBB:

- buffered virtual ground;
- differential +/CENTER/- measurement;
- MOSFET threshold switching;
- capacitor and inductor storage;
- H-bridge reversible inductive drive;
- coupled multi-winding toroid model;
- three-winding shared-core behavior;
- square-loop magnetic memory core with persistent remanent state;
- MTJ/TMR-style quadrature electrical sensor interface.

Still missing as of this lock:

- a true spatial magnetic-field solver / Bx-By-Bz field-vector measurement;
- a complete magnetic-state-driven reinjection circuit proving LOW -> refill
  -> HIGH -> disconnect without a binary controller IC;
- full integrated X/Y user-state -> AC -> rotating-field flashlight build.

Do not fake those missing capabilities.

## Conventional flashlight is only a control

Any ordinary continuously driven or Schmitt-controlled LED flashlight remains
useful only as a reference/control for matched-brightness energy comparison.
It must not be labeled the One-Wave balanced flashlight prototype.

## Pass order

1. Same CENTER reference survives every stage.
2. BC-DC differential state is stable and asymmetric loading is visible.
3. MOSFET/storage bucket decays from a held state without a timer.
4. LOW state produces reinjection.
5. Reinjection raises state through a distinct HIGH threshold.
6. Source disconnects and a measurable coast interval exists.
7. Stored state remains after the user's non-mechanical input is removed.
8. X color state and Y brightness state remain independently measurable.
9. TC-AC crosses the same CENTER with measurable phase.
10. QC-RC produces a rotating electrical drive vector.
11. Only after Bx/By/Bz capability exists may a 3D magnetic-field trajectory
    be claimed or classified.
12. Compare energy/runtime against the conventional reference at matched useful
    output.
