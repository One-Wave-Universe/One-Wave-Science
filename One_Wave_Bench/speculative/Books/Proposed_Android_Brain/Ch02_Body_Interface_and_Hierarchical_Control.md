# Chapter 2 — Body Interface and Hierarchical Control

Status: PROPOSED BUILD

This chapter links the proposed Android Brain to C-312 and the existing Android Body book.

## Hierarchy

```text
local sensor/actuator units
-> 3:1 local aggregation candidate
-> positional chains
-> central coordination
-> targeted command fan-out
```

The hierarchy is distributed rather than dictatorial. Local units hold local state and perform fast responses. Higher layers modulate, coordinate, and correct selected units rather than micromanaging every movement.

## Timing Candidates

- local fast loop,
- slower oversight loop,
- deliberate full-system loop.

Ratios such as 3:1, 6:1, and 12:1 remain proposed design values until measured against hardware latency, stability, bandwidth, and power use. Every use must declare its domain. A 3:1 nerve aggregation ratio is not the 3:1 planar mirrored-axis count in D-411, and a 6:1 oversight ratio is not automatically sixfold lattice geometry.

## Consciousness Boundary

This architecture is allowed to be informed by the One-Wave consciousness hypothesis. The build itself only demonstrates implemented function. Any claim about consciousness requires a separate test definition that does not yet exist.
