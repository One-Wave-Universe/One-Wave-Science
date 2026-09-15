---
node_id: "G-741"
canonical_name: "Crazy Town — Balanced-Rail Nested-Loop Physical Build Proposition"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Legacy G-Series / Canonicalized Node"
claim_gate_detail: "unbuilt low-voltage electronics proposition using three bidirectional A/B/C mirrors; no demonstrated computing, actuator, or biological equivalence"
metadata_standard: "I-06"
---

# Node G-741: Crazy Town Build Proposition Experiment

## Purpose

Map a measurable physical build for nested Field/Void computation using a local balanced reference, nerve-level DC power/recovery/reinjection, alternating activity through three bidirectional A/B/C mirrors, ternary UP/HOLD/DOWN control, quadratic Views UP, and quadratic Actions/Override DOWN through those same mirrors.

This node is an experiment plan, not a claim that the circuit has been built or shown to compute.

## Physical geometry lock

The CELL_V1 hardware primitive is:

```text
CLOCKWISE FLAT EDGES:
A+ -> B+ -> C+ -> A- -> B- -> C-

THREE PHYSICAL BIDIRECTIONAL MIRRORS:
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

There are **three physical mirrors**, not three Mirror gates plus three separate Action gates.

The same physical paths carry both directions:

```text
UP   = Views / state / relation
DOWN = Actions / conditioning / Override
```

Six edge interfaces are directed ends of three bidirectional mirrors.

## Protected logical boundary

The route address space remains:

\[
b\in\{-1,+1\},\qquad d\in\{-1,0,+1\},\qquad 2\times3=6.
\]

Interpretation:

```text
binary = YES / NO relation
ternary = DOWN / HOLD / UP
```

Ground/no committed binary relation is outside the six-route set.

No threshold, quadratic measurement, confirmation stage, return stage, memory function, reinjection stage, or nerve-gate implementation may silently create a seventh route.

## Build stack

| Build | Candidate physical function | State retained | Measured output |
|---|---|---|---|
| P0 | balanced `+ / V0 / -` reference | local reference | drift, noise, signed differential |
| D0 | DC supply/recovery/reinjection reservoir | energy state | delivered and recovered energy |
| B1 | binary local relation | polarity/commitment relative to reference | YES/NO relation |
| A0 | alternating/recurring path activity | phase + polarity | recurrence around reference |
| T1 | ternary local command | DOWN / HOLD / UP | selected motion/path response |
| M3 | three bidirectional A/B/C mirrors | path + retained physical state | six directed interfaces |
| Q1 | quadratic sensing | Direction / Phase / Strength / Reference | paired Views UP |
| C1 | higher/local resolution | nested receipt | no-intervention or Override |
| Q2 | quadratic conditioning | downward relation | Actions / Override DOWN |
| N1 | true bidirectional nerve-gate connection | connection state | A/B/C path change |
| R1 | recovery/reinjection + return | resulting local state | NEW state + energy receipt |

## P0 — balanced reference

Every information voltage is measured relative to the local reference:

\[
v_{state}=v_{signal}-V_0.
\]

`V0` is a reference, not an energy reservoir and not a switching-current dump.

Receipts must record signed displacement, reference drift, noise, amplitude, phase, threshold, and prior state.

## D0 — DC is the nerve-level power/reinjection loop

DC does not disappear once alternating activity begins.

Current candidate role:

```text
DC source/reservoir
 -> supplies local nerve activity
 -> mirrored switching / stateful path performs work
 -> recoverable inductive/magnetic energy is steered back to the controlled DC reservoir
 -> next local cycle draws from that reservoir
```

Energy recovery must be measured. No gain may be inferred from reference motion or unaccounted stored energy.

## B1 — binary relation

The binary relation is two-way:

```text
YES / NO
```

Do not redefine NO as missing signal or Ground. Ground/no committed choice is separate.

The physical encoding of YES/NO may be polarity, orientation, phase relation, or another measured differential, but that encoding must be declared and testable.

## A0 — AC/alternating recurrence

Alternating activity is produced through switching/coupling of the physical paths; DC does not spontaneously become AC.

The experiment must measure whether the chosen topology produces a repeatable recurrence around the same reference and whether phase/orientation remains distinguishable.

If a rotating magnetic field is claimed, the phase relationship producing rotation must be measured rather than inferred from the existence of AC alone.

## T1 — ternary controls local movement and motor/actuator command

The ternary relation is:

```text
DOWN
HOLD
UP
```

`HOLD` is an active balanced center, not absence.

At the nerve/body interface the same ternary relation is the candidate motor/actuator grammar:

```text
one orientation / balanced Hold / opposite orientation
```

The exact motor topology, winding count, phase drive, and torque behavior remain experimental.

## M3 — three physical bidirectional mirrors

The physical CELL_V1 path is:

```text
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

Do not build six sequential Mirror/Action devices.

Legacy six-position labels may still be emitted by software receipts, but each label must map back to one of the three physical axes and one of the two directions.

## Processing is memory

The active path is intended to retain the state it just processed:

```text
local state affects current/signal path
 -> path interaction changes the same local state
 -> changed state remains locally available
 -> next pass encounters the changed state
```

The exact stateful element is open. Candidate classes include memristive, hysteretic magnetic, spintronic/magnetoresistive, oscillatory, or other stateful structures.

The processing-memory claim is rejected if the memory can be removed from the active path without changing the operation.

Any retained-state claim must demonstrate write, retain, read with bounded disturbance, rewrite, and propagation/interaction with another stage.

## Q1 — quadratic Views UP

The accumulated state is described upward using:

\[
Q_{up}=(\text{Direction},\text{Phase},\text{Strength},\text{Reference}).
\]

Views go UP through the same A/B/C mirror structure. They are descriptors, not additional gates.

## Q2 — Actions / Override DOWN

After local or higher resolution, conditioning travels DOWN through the same mirror structure.

Action-mode vocabulary may include:

```text
Inward
Outward
Across
Over
```

These words do not create another hardware layer.

A candidate local policy is:

```text
local state/resources within declared limits
 -> no higher intervention
 -> complete local action/recovery/reinjection

local state/resources outside declared limits
 -> Views UP
 -> higher resolution
 -> Action/Override DOWN
 -> local path changes
```

The resource variables and thresholds must be explicitly measured.

## N1 — bidirectional nerve gate

The connection element must block/pass both intended directions without a body diode silently defeating the command.

Back-to-back MOSFETs or another true bidirectional switch are candidates.

SiC MOSFETs may be tested where power, thermal, endurance, or switching properties matter. Direct millivolt/microvolt gate control is not assumed; any required gate-drive interface must be explicit and measured.

The bidirectional switch is a connection candidate, not automatically the processing-memory element.

## Three-axis downward coordination hypothesis

One resolved higher Override may coordinate A/B/C conditioning:

```text
one Override
 -> A path condition
 -> B path condition
 -> C path condition
```

This is a fan-out relation through the three existing mirrors, not three new Action gates. It remains experimental until measured.

## R1 — return, recovery, reinjection, and new state

The return path is not restoration of the old state.

```text
old local state
 -> local binary/ternary relation
 -> alternating/path interaction
 -> retained state changes
 -> local continuation OR higher Override
 -> recoverable energy returns to controlled DC reservoir
 -> resulting configuration remains
 -> resulting configuration is the NEW local state
 -> new state becomes the next View UP
```

The target recurrence is:

```text
NEW STATE -> UP -> resolution -> DOWN or local continuation -> recovery/reinjection -> NEW STATE
```

## First staged experiment

1. Characterize `V0` drift/noise with no switching load.
2. Characterize the DC source/recovery reservoir separately from `V0`.
3. Demonstrate one true bidirectional path and measure leakage in both blocked directions.
4. Add a stateful path element and prove that previous activity measurably changes the next pass.
5. Demonstrate both directions through that same physical mirror.
6. Reproduce the mirror as A/B/C and preserve `A+ B+ C+ A- B- C-` edge order.
7. Demonstrate the six directed edge interfaces without six separate physical gate devices.
8. Demonstrate binary YES/NO without collapsing NO into Ground.
9. Demonstrate ternary DOWN/HOLD/UP and active Hold.
10. Measure any claimed AC recurrence/phase behavior.
11. Measure quadratic Views UP from Direction/Phase/Strength/Reference.
12. Apply Actions/Override DOWN through the same physical mirrors.
13. Verify that resulting local state remains and becomes the next upward state.
14. Measure returned energy into the DC reservoir and calculate reinjection efficiency.
15. Only after local behavior passes should motor/actuator loads and higher volume scaling be connected.

## Minimum receipts

Record at least:

- timestamp;
- physical axis A/B/C;
- edge direction `+ -> -` or `- -> +`;
- local `V0`;
- binary relation;
- ternary command;
- differential;
- phase;
- threshold/hysteresis;
- retained pre-state;
- retained post-state;
- switch state;
- View descriptors;
- Action/Override state;
- delivered DC energy;
- recovered DC energy;
- reinjection efficiency;
- whether processing-memory behavior persisted into the next pass.

## Pass conditions

- exactly three physical bidirectional A/B/C mirrors are preserved;
- all six directed interfaces are distinguishable without inventing six separate physical gates;
- YES and NO remain distinguishable from Ground;
- DOWN/HOLD/UP are distinguishable and Hold is active;
- state retained in the active path measurably affects the next pass;
- blocked bidirectional paths remain within declared leakage bounds;
- Views travel UP and Actions/Override travel DOWN through the same physical mirrors;
- DC recovery/reinjection is measured separately from the reference;
- return produces a distinguishable new state rather than an automatic reset.

## Failure conditions

Reject or revise the topology if:

- a diagram or build creates six separate physical Mirror/Action gates;
- connections move to hex corners;
- edge order changes;
- NO collapses into Ground;
- Hold becomes simply no signal;
- AC or rotation is asserted without measured phase behavior;
- processing memory is actually a disconnected storage block;
- MOSFET leakage determines the state;
- recovered energy is dumped into `V0`;
- a SiC gate requires an undeclared interpretation/driver layer;
- Views and Actions use different claimed mirror hardware;
- return merely resets the old state;
- or the architecture depends on unmeasured brain-layer counts.
