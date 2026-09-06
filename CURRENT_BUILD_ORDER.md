# CURRENT BUILD ORDER — BALANCED DEVICES TO CELL ARCHITECTURE

This file is the current execution order for the practical build program. The rule is: useful device first, measure it honestly, then reuse the proven primitive at the next scale.

## Project 0 — Virtual Breadboard Qualification

Purpose: make the virtual breadboard trustworthy enough to test ordinary electronics and then the balanced builds.

Required permanent regressions:

1. DC source / resistor / divider
2. LED + current limiting
3. diode / rectifier
4. capacitor charge-discharge
5. RC low-pass / high-pass
6. inductor / flyback
7. LC/RLC ringdown
8. MOSFET low-side / high-side
9. push-pull / half bridge
10. full bridge / differential load
11. virtual ground under unequal load
12. comparator + hysteresis
13. oscillator
14. transformer / coupled coils
15. three coupled windings
16. battery discharge / runtime
17. reinjection storage loop
18. balanced differential cell

Every test must return `expected`, `actual`, `tolerance`, and `PASS/FAIL`. Do not rewrite the simulator per build. Add missing physics capabilities while preserving working behavior.

## Project 1 — Balanced 9 V Flashlight

This is the first useful physical proof device.

Goals:

- 9 V battery power
- stable shared center / virtual ground
- balanced differential power path
- low-loss storage
- hysteretic reinjection: sense drop -> inject energy -> restore target -> disconnect
- useful LED output at matched perceived brightness
- battery/runtime measurement against a conventional reference
- projected battery bars on the wall only when requested
- modular 3D-printed body and removable electronics tray

Success criterion: same useful light output with a measurable runtime / average-current advantage, or a clear measured explanation of where the losses occur.

## Project 2 — Balanced Speaker + Purpose-Built Amp

Do not chase maximum SPL. Optimize for the right listening volume, low idle power, battery life, symmetry, and noise/interference rejection.

Speaker targets:

- centered cone rest position
- mirrored / symmetric magnetic motor geometry
- modest excursion
- differential drive
- measurable inward/outward symmetry

Amp targets:

- differential signal path where practical
- low quiescent current
- strong common-mode noise rejection
- sleep/mute when silent
- built initially on breadboard/perfboard

Success criterion: same perceived volume with lower idle/average power and/or lower hum/noise/distortion than the reference implementation.

## Project 3 — Three-Winding Ternary Nerve

This is the nerve layer, not the brain cell.

Targets:

- three coupled windings
- ternary local control `- / HOLD / +`
- fast local actuation
- sensors remain separate inputs
- vagus-style regulation layer remains separate from motor-control nerves
- Hall/current/temperature sensing added as needed

Success criterion: reproducible local ternary control and measurable magnetic coupling without requiring higher brain layers to manage every transition.

## Project 4 — DC -> AC -> RC Three-Cell Stack

Current shorthand:

- `BC-DC` — balanced/binary choice represented as a differential DC state around center
- `TC-AC` — confirmation / out-and-back oscillation around center
- `QC-RC` — coordinated rotating relationship across axes

Test stack:

1. Cell 1: DC differential state
2. Cell 2: validated handoff into controlled AC / phase behavior
3. Cell 3: multi-axis field control / rotation

Use three-axis field measurement (`Bx`, `By`, `Bz`) to reconstruct the actual resultant vector. Do not assume field geometry from drawings.

## Project 5 — 3D Cell Geometry

Working geometry:

- hexagon = 2D slice / cross-section, not the whole object
- triangular relationships connect locally
- pyramid connections carry relationships between layers
- stacked layers form a cube coordinate scaffold
- the combined reachable / measurable field exists volumetrically inside that scaffold
- three independent axes are required for true 3D steering

First serious scale target: a `3 x 3 x 3 = 27` cell structure (R27 working name), only after the lower primitives are measurable.

## Project 6 — Parser-Matrix / Cheap Knockoff Brain

Software prototype before custom brain hardware.

Primitive thought pair:

- expressive parser: expands candidate interpretations / paths
- compressive parser: contracts, removes redundancy, keeps the stable representation

Local cluster:

- expressive + compressive + resolver/connector

Three clusters of three parsers form the first Point -> Path -> Field parser matrix.

Memory rule:

- parsers are processing and memory
- persistent parser states + transitions + links are the memory pattern
- recall = rebuild the relevant parser constellation from a cue
- do not depend first on a giant transcript archive

Higher hardware/software split:

- M4/router = fast routing, timing, synchronization, state handoff
- CPU = Administrator / oversight / commit decisions
- GPU = Dream / parallel generation and candidate simulation
- Hailo-8-class accelerator may be tested as an M4/inference-routing helper, but the architecture must not depend on one vendor device

Canonical whole-system lifecycle remains:

`Idle -> Primed -> Executing -> Vectoring -> Resolving`

## Project 7 — First Integrated Sphere / Cube Processing Test

Only begin after Projects 1-6 have produced reusable measurements.

A first sphere/cube test must demonstrate more than raw ternary storage. It should show:

- persistent local states
- relationship-dependent routing
- state change across paths
- partial-cue reconstruction
- measurable 3D field/state behavior where magnetic hardware is involved
- differential between two whole-network states as an explicit observable

## Build law

Do not turn each architecture update into a whole-repository rewrite. Work in coherent subsystem batches: one subsystem, its dependencies, its tests, then stop and measure. The simulator scales upward with the builds rather than being replaced for each build.
