---
node_id: "B-225"
canonical_name: "Five-Level Modulation Around Reference"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Resolution / Formalization Node"
claim_gate_detail: "Implementation-canonical coarse state bands; domain labels remain representations"
metadata_standard: "I-06"
---

# Node B-225: Five-Level Modulation Around Reference

## Correction

Earlier versions mixed a five-step transformation narrative with the five-level modulation layer. The current implementation architecture separates them.

The **five modulation levels** describe coarse strength modulation of one relation around its active middle/reference:

```text
+2
+1
 0
-1
-2
```

or equivalently:

```text
upper-2
upper-1
middle/reference
lower-1
lower-2
```

They are not five new primitive forces and they are not the six execution steps.

## Kernel-Neutral Meaning

- `+2` = strong state on one side of reference
- `+1` = moderate state on that side
- `0` = middle/reference band
- `-1` = moderate state on the opposite side
- `-2` = strong state on the opposite side

Exact thresholds are implementation-specific.

## Representation Wrappers

Different domains may map the same five-band structure into easier human labels, for example:

```text
Spatial: Floor / Low / Middle / High / Ceiling
Thermal: Frozen / Cold / Middle-Warm / Hot / Fire
```

These are strength representations, not invariant primitives. Matter-state, thermal, biological, or other domain mappings must not be hard-coded into the kernel.

## Distinction from Recursive Octave Scale

The recursive five-position octave scale is a separate axis:

```text
Micro -> Small -> Medium -> Large -> Macro
Macro[n] -> Micro[n+1]
```

`Macro` closes the current loop/trunk and becomes `Micro` at the next larger loop/trunk. These octave positions must not be used as aliases for the `-2,-1,0,+1,+2` modulation levels or for the five Field lifecycle states.

## Distinction from Seven Threshold Bands

The five-level layer is **coarse modulation**. A separate seven-band envelope may be used for finer confidence/intensity/trigger resolution. The two structures must not be collapsed into one.

A currently discussed seven-band representation is:

```text
100-90
85-75
70-60
55-45
40-30
25-15
15-0
```

This remains a representation/candidate threshold map until calibrated for a concrete implementation.

## Relationship to Views and Moves

```text
Direction = Three Moves (-1/0/+1)
Strength  = may be represented by the Five-Level modulation
Phase     = oscillatory position/crossover relation
Reference = local middle/baseline
```

The five modulation levels therefore primarily refine **Strength**, while Direction remains ternary. They are distinct from the Field lifecycle states `Idle -> Primed -> Executing -> Vectoring -> Resolving`.

## Relationship to Six Steps

The six-step oscillator can carry any one of these five modulation levels through each operation. The count `5` is not a replacement for the six-pair timing grammar.

## Yellow Audit

- Separation of five-level modulation from the five Field lifecycle states and six-step execution is resolved.
- Neutral `-2,-1,0,+1,+2` labels are canonical for implementation.
- Domain-specific labels and numerical thresholds require independent calibration.
