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

`Defer` is the Void middle choice. It preserves Hold while evidence, actuator
readiness, or threshold support is insufficient. `Deny` produces Override.
`Confirm` permits the resolved command. Override is not a fourth ternary.

## Direction invariant

\[
(\text{Field views}+\text{Void views})
\xrightarrow{\text{quadratic up}}
\text{brain command}
\xrightarrow{\text{quadratic down}}
(\text{Field actions}+\text{Void actions})
\]

Oversight travels upward as view information. Override travels downward as an
action. There is no Field/Void identity swap and no view/action cross-switch.

## Compatibility boundary

This node does not add a seventh route or alter the settled binary-by-ternary
six-route address space. The paired ternaries describe Field/Void processing;
the quadratic layer describes four views up and four actions down. Existing
Field/Void boundaries remain intact.

## Micro receipt requirements

Each executable Micro receipt must retain:

1. the Field ternary proposal;
2. the Void ternary resolution;
3. paired Field/Void four-view data on the upward leg;
4. paired Field/Void four-action data on the downward leg;
5. whether a Void Override was actually produced; and
6. the measured consequence returned as the next reference.

The receipt fails if it collapses `Defer` into `Deny`, reports Override without
Deny, sends an action upward, sends a view downward, or changes the settled
six-route projection.
