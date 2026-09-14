# CELL_V1 Rotational / Magnetic Hold Test

**Sense first. Feedback later.**

CELL_V1 does not earn a magnetic-memory claim because a coil was added or because current continued briefly after switching. The first test separates ordinary electrical storage, inductive decay, and actual drive-off magnetic retention.

## F0 sense geometry

Use G0 only after its electrical balance/lean/RC tests pass.

```text
G0 current conductor: one pass through ferrite-ring aperture
sense winding:        20–50 turns insulated fine wire on the ring
sense output:         measurement instrument only
reinjection:          NONE in this test
```

A Hall probe may be used instead of or alongside the sense winding.

## Four mandatory receipts

Run the same timing window each time:

1. positive electrical pulse;
2. negative electrical pulse;
3. geometry/material control — ferrite removed, air/nonmagnetic substitute, or equivalent control;
4. drive removed, followed by a fixed delayed sample.

Record at minimum:

```text
G0 station current
G0 tap - NET_G
HOLD0 - NET_G
sense-coil or Hall reading while driven
sense reading immediately after drive removal
sense reading after the fixed delay
polarity of the preceding pulse
```

## Pass condition for a magnetic-hold candidate

A retained signal must:

- persist after electrical drive is removed;
- reverse consistently when the prior magnetic polarity reverses;
- exceed the no-core/nonmagnetic control;
- exceed instrument zero drift;
- survive a delay long enough to separate it from ordinary switching transients;
- not be explainable by the 10 uF RC branch or MOSFET reverse-recovery current.

If the signal follows current while powered and collapses with ordinary inductive/RC decay, the result is **field coupling, not memory**.

## Stop conditions

Do not close active magnetic reinjection if:

- NET_G moves outside its acceptance belt;
- the sense signal depends on probe placement more than drive polarity;
- MOSFETs or coil heat;
- the signal disappears when RC charge is accounted for;
- controls are missing.

## Spatial-model boundary

The current Virtual Breadboard magnetic primitives are lumped models. They do not yet compute a real spatial `Bx/By/Bz` field around this three-station geometry. Therefore a passing lumped simulation is not a 3-D magnetic-field proof.

Only after the sense-only experiment passes should a separate active-feedback/reinjection prototype be designed.
