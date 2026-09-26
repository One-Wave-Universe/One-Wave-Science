# Stage 02 — Path

Stage 02 links measured excitation points into candidate paths without assuming a particle ontology.

## Input

Each point comes from Stage 01:

- event id
- detector subsystem/channel
- x, y, z
- measured signal or deposited energy
- optional time
- provenance

## Path construction

A path is an ordered relation between points.

Candidate ordering rules are tested separately:

1. radial detector-layer order
2. nearest-neighbor geometric continuity
3. time order, when timestamps exist
4. conventional reconstructed-track order for comparison only

The raw points never change.

## One-Wave path state

For adjacent points i -> j:

- displacement: dr = r_j - r_i
- segment length: ds = |r_j-r_i|
- direction: u = dr/ds
- amplitude ratio: A_j/A_i
- turning angle
- local phase-like angle phi = atan2(y,x)
- octave scale index n
- scale factor 2^n

## Octave rule

All scale transforms are explicit:

scale(n)=2^n

Geometry scaling and amplitude scaling are independent switches.

A path feature is interesting only if its normalized structure persists across selected octave scales and survives shuffled/reflected/event-mixed controls.

## Output

- raw point list
- ordered path list
- segment lengths
- angular change
- amplitude profile
- cumulative path length
- scale-normalized path signature
- provenance
