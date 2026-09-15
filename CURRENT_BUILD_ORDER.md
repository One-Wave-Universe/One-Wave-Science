# CURRENT BUILD ORDER — BALANCED DEVICES TO CELL ARCHITECTURE

This file is the current execution order for the practical build program. The rule is: useful device first, measure it honestly, then reuse the proven primitive at the next scale.

## ACTIVE CELL_V1 validation track

The current CELL_V1 hardware work is governed by:

- `UPDATED_60_CELL_V1_HEX_EDGE_FLOWER_VOLUMETRIC_MEMORY_ARCHITECTURE.md`
- `CELL_V1_BUILD_PACKET.md`
- `CELL_V1_ANTI_DRIFT.md`
- `ARCHITECTURE_POINT_PATH_FIELD_SCALE_RECURSION.md`

This track does not erase the projects below. It tells the older three-winding, balanced-cell, and 3D work exactly what geometry and evidence they now feed.

### Geometry lock before any build

```text
PORTS: FLAT SIDES / EDGES ONLY
CLOCKWISE: A+ -> B+ -> C+ -> A- -> B- -> C-
OPPOSITES: A+<->A-, B+<->B-, C+<->C-
FLOWER: 7 identical cells, same orientation, edge-to-edge
```

Do not fabricate or simulate a corner-connected CELL_V1.

### CELL_V1 build gates

**A. One opposed magnetic axis** — prove write, retention, read, rewrite, and that old magnetic state changes the next standardized response.

**B. Reinjection on the same axis** — measure recoverable energy separately from magnetic retention; no unexplained gain.

**C. Full three-axis hex** — reproduce the same primitive on A, B, and C and package the six edge-center interfaces without changing the basic mechanism.

**D. Two/three-cell path** — quantify propagation loss, phase/delay, reference disturbance, and retained-state disturbance.

**E. Closed rotation** — distinguish a traveling/circulating phase/state from simultaneous switching, ringing, or a static loop.

**F. Seven-cell flower** — build one center + six surrounding identical cells, all same orientation, and demonstrate coupled paths/rotations while retaining local observability.

**G. Smallest 3D coupling** — measure useful depth coupling, reinforcement, opposition, and crosstalk before scaling farther.

**H. Candidate volume and mirror** — only after smaller gates pass, test `3 x 3 x 3` recursion and a mirror-flipped companion volume for whole-volume memory/comparison/reinjection.

Brain/M4 layer counts remain open. Do not make `2+2`, `3+3`, `3+ / 3- / 3+`, or `3 x 3 x 3` mandatory hardware until the smaller tests show what each added depth contributes.

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

CELL_V1 adds required qualification cases once the underlying component models are trustworthy:

19. hysteretic magnetic state write/read/retain/rewrite
20. history-dependent threshold/response
21. controlled inductive recovery into a measured reservoir
22. bidirectional axis pair around a virtual center
23. two-cell edge propagation
24. closed-loop phase propagation / rotation discrimination
25. seven-cell identical-orientation flower
26. minimal depth coupling / crosstalk test

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

This remains a useful motor/nerve analogue and component test. It is **not** the canonical CELL_V1 physical geometry.

Targets:

- three coupled windings
- ternary local control `- / HOLD / +`
- fast local actuation
- sensors remain separate inputs
- vagus-style regulation layer remains separate from motor-control nerves
- Hall/current/temperature sensing added as needed
- collect phase, switching, magnetic coupling, and recovery measurements that can feed CELL_V1 A/B/C axis design

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

This stack is an experimental decomposition of behavior. It must not overwrite the locked CELL_V1 flat-edge port geometry or be treated as proof that three separate physical cells are required for the final primitive.

## Project 5 — 3D Cell Geometry

Working geometry is now constrained by the CELL_V1 lock:

- one physical CELL_V1 is a six-flat-edge hex interface in its planar face;
- clockwise edge order is `A+ B+ C+ A- B- C-`;
- A/B/C are three opposed axes through the center;
- identical cells form the seven-cell flower without alternating orientation;
- the hex is the planar connectivity face of a volumetric-capable module, not permission to connect at vertices;
- horizontal relations use side-to-side connections;
- depth/vertical coupling must be measured rather than assumed from a drawing;
- three independent spatial degrees of freedom are required for true 3D steering/field reconstruction.

First serious **candidate** scale remains a `3 x 3 x 3 = 27` lower-unit structure, but `lower unit` is now explicitly open: one CELL_V1, one flower, or another proven packaged relation. The smaller scale must demonstrate Point -> Path -> Rotation -> Field before 27-unit counting is promoted to hardware.

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

CELL_V1 scaling is allowed to inform this software model, but hardware layer counts must not be reverse-engineered from parser counts without evidence.

## Project 7 — First Integrated Sphere / Cube Processing Test

Only begin after the lower projects and CELL_V1 gates have produced reusable measurements.

A first sphere/cube test must demonstrate more than raw ternary storage. It should show:

- persistent local states
- relationship-dependent routing
- state change across paths
- partial-cue reconstruction
- measurable 3D field/state behavior where magnetic hardware is involved
- differential between two whole-network states as an explicit observable
- evidence that the lower-scale resolved structure can serve as one next-scale point without erasing its internal state

## Build law

Do not turn each architecture update into a whole-repository rewrite. Work in coherent subsystem batches: one subsystem, its dependencies, its tests, then stop and measure. The simulator scales upward with the builds rather than being replaced for each build.

For CELL_V1 specifically:

```text
lock geometry
 -> prove one axis
 -> prove memory
 -> prove reinjection
 -> duplicate A/B/C
 -> prove path
 -> prove rotation
 -> prove seven-cell field
 -> prove depth
 -> then scale volume
```

If a lower gate fails, fix that gate instead of hiding the failure inside a larger brain-shaped build.
