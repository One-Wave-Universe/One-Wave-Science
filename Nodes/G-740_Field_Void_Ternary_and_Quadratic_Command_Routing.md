---
id: G-740
title: Field/Void Ternary and Quadratic Command Routing
status: proposed-build
tier: green-hypothesis
claim_boundary: computational routing contract; not literal neuroanatomy
---

# Node G-740: Field/Void Ternary and Quadratic Command Routing

## Locked primitives

Field and Void remain present at every layer. They are counterparts, not
substitutes.

| Layer | Field | Void |
|---|---|---|
| Ternary | Express / Hold / Compress | Confirm / Defer / Deny |
| Quadratic view | four Field views | four Void views; Oversight is the Void view |
| Quadratic action | four Field actions | four Void actions; Override is the Void action |

`Defer` is the Void middle choice. It preserves Hold while evidence, local
readiness, or threshold support is insufficient. `Deny` produces Override.
`Confirm` permits the resolved continuation. Override is not a fourth ternary.

## Brain-first scope

This routing contract must operate as a closed **brain/computer recurrence**
without requiring sensors, motors, actuators, or Android body feedback.
Body-facing interfaces may be attached later, but they consume and produce the
same relational contract rather than defining the cognition kernel.

## Direction invariant

One local recurrence is:

\[
(\text{Field views}+\text{Void views})
\xrightarrow{\text{quadratic up}}
\text{higher brain relation}
\xrightarrow{\text{quadratic down}}
(\text{Field actions}+\text{Void actions})
\xrightarrow{\text{return}}
\text{new local state}.
\]

Oversight travels upward as view information. Override travels downward as an
action. There is no Field/Void identity swap and no view/action cross-switch.

The return is not a reset instruction. When the downward conditioning is
released or completed, the resulting configuration is the **new state**. That
new state becomes the next upward signal / relation:

```text
UP -> resolution -> DOWN -> NEW UP -> resolution -> DOWN -> NEW UP ...
```

A model that automatically restores the pre-override state on every return is
not equivalent to this recurrence.

## Decision and connection separation

The local decision is carried by the measured differential / voltage swing
relative to its reference. Connection hardware is downstream of that physical
state variable and must not be silently promoted into the decision itself.

Current hardware-role contract:

```text
local differential / voltage swing = decision/state
persistent magnetic or oscillatory configuration = processing-memory candidate
bidirectional switch = nerve-gate / connection candidate
```

This distinction allows the same routing grammar to be tested with different
physical implementations without changing the logical contract.

## Three-flip override hypothesis

The current physical hypothesis permits one higher-level Override event to
coordinate three lower nerve-gate flips. This is a compression / fan-out
relation, not three independent decisions:

```text
one resolved Override
 -> lower flip 1
 -> lower flip 2
 -> lower flip 3
```

On the return, the Override condition is reduced / removed and the resulting
lower configuration is read as the next state upward. The three-flip mapping
remains experimental until measured in the physical build; this node records
the routing meaning, not proof of hardware simultaneity.

## Compatibility boundary

This node does not add a seventh route or alter the settled binary-by-ternary
six-route address space. The paired ternaries describe Field/Void processing;
the quadratic layer describes four views up and four actions down. Existing
Field/Void boundaries remain intact.

The mirrored logical positions may be read as:

```text
1/6 -> 2/5 -> 3/4 | 4/3 -> 5/2 -> 6/1
```

where `/` is a simultaneous mirrored pair and the central `3/4 <-> 4/3`
relation marks the mirrored reversal. The two sides' corresponding `6`
positions are each other's mirrored `6`; this is not ordinary serial counting
and does not create extra physical gates.

## Micro receipt requirements

Each executable Micro receipt must retain:

1. the Field ternary proposal;
2. the Void ternary resolution;
3. paired Field/Void four-view data on the upward leg;
4. paired Field/Void four-action data on the downward leg;
5. whether a Void Override was actually produced;
6. the pre-override local state;
7. the lower connection / nerve-gate consequence where implemented;
8. the resulting **new** local state after return / release; and
9. that new state as the next upward reference / relation.

The receipt fails if it collapses `Defer` into `Deny`, reports Override without
Deny, sends an action upward, sends a view downward, changes the settled
six-route projection, silently restores the old state after every return, or
requires Android/body hardware to close the brain recurrence.
