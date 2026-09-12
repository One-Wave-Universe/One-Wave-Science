---
node_id: "G-740"
canonical_name: "Field/Void Ternary and Quadratic Command Routing"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Legacy G-Series / Canonicalized Node"
claim_gate_detail: "Computational routing contract; higher-order view/action modes do not alter the primitive 3-Mirror/3-Action gate cycle"
metadata_standard: "I-06"
---

# Node G-740: Field/Void Ternary and Quadratic Command Routing

## Primitive gate lock

This node is downstream of the canonical six-gate oscillator and may not redefine its count.

```text
6 steps = 6 gates = 3 Mirror gates + 3 Action gates

M1 -> A1 -> M2 -> A2 -> M3 -> A3 -> M1 ...
```

Mapped to the current step names:

```text
BEGIN = M1
BUILD = A1
HOLD  = M2
BUILD = A2
BREAK = M3
LOOP  = A3
```

Any quadratic views or named action modes below are descriptors available to those gate roles. They are **not extra primitive gates**.

## Locked Field/Void primitives

Field and Void remain present at every layer. They are counterparts, not substitutes.

| Layer | Field | Void |
|---|---|---|
| Ternary | Express / Hold / Compress | Confirm / Defer / Deny |
| Quadratic view modes | Direction / Phase / Strength / Reference | corresponding opposed/reference views |
| Quadratic action modes | Inward / Outward / Across / Over | corresponding opposed/override modes |

The four view modes and four action-mode words are a higher-order routing vocabulary. They describe what may be read or done within a gate operation; they do **not** mean four primitive Action gates. The primitive cycle still contains exactly three Action gates.

`Defer` is the Void middle choice. It preserves Hold while evidence, local readiness, or threshold support is insufficient. `Deny` can produce Override. `Confirm` permits resolved continuation. Override is not another primitive gate.

## Brain-first scope

This routing contract must operate as a closed brain/computer recurrence without requiring sensors, motors, actuators, or Android body feedback. Body-facing interfaces may be attached later, but they consume and produce the same relational contract rather than defining the cognition kernel.

## Direction invariant

A higher-order routing description may be written as:

```text
views/readouts available to a Mirror gate
 -> Mirror resolution
 -> one of the three Action gates
 -> resulting state
 -> next Mirror gate
```

Views travel upward as information. Actions travel downward/outward as consequences. There is no Field/Void identity swap and no view/action cross-switch.

The return is not a reset instruction. When downward conditioning is released or completed, the resulting configuration is the **new state**. That new state becomes part of the next Mirror-gate input:

```text
M -> A -> new state -> M -> A -> new state ...
```

A model that automatically restores the pre-action state on every return is not equivalent to this recurrence.

## Decision and connection separation

The local decision is carried by the measured differential / voltage swing relative to its reference. Connection hardware is downstream of that physical state variable and must not be silently promoted into the decision itself.

Current hardware-role contract:

```text
local differential / voltage swing = decision/state
persistent magnetic or oscillatory configuration = processing-memory candidate
bidirectional switch = nerve-gate / connection candidate
```

This distinction allows the same routing grammar to be tested with different physical implementations without changing the logical contract.

## Three-flip override hypothesis

The current physical hypothesis permits one higher-level Override event to coordinate three lower nerve-gate flips. This is a compression / fan-out relation, not three independent decisions and not a new three-gate layer:

```text
one resolved Override
 -> lower flip 1
 -> lower flip 2
 -> lower flip 3
```

The three-flip mapping remains experimental until measured in the physical build.

## Compatibility boundary

This node does not add a seventh gate and does not create a second six-gate system from `2 choices x 3 moves = 6` route addresses.

Keep these counts separate:

```text
primitive cycle: 3 Mirror gates + 3 Action gates = 6 gates = 6 steps
route address space: 2 choices x 3 moves = 6 route addresses
view modes: 4 descriptors
quadratic action modes: 4 descriptors
```

Only the first line is the primitive gate count.

The older mirrored notation

```text
F1/V6 - V5/F2 - F3/V4 - V3/F4 - F5/V2 - V1/F6
```

is interpreted through B-221a/C-301 as the six canonical positions, alternating Mirror and Action. It must not be read as six Mirror crossovers plus six actions.

## Micro receipt requirements

Each executable Micro receipt should retain:

1. canonical gate number `1..6`;
2. canonical role `Mirror` or `Action`;
3. canonical step label `BEGIN/BUILD/HOLD/BUILD/BREAK/LOOP`;
4. Field/Void relation used at that position;
5. optional higher-order view-mode annotations;
6. optional higher-order action-mode annotation on Action positions;
7. whether an Override was actually produced;
8. pre-action local state;
9. resulting new local state; and
10. that state as input to the next Mirror gate.

The receipt fails if it collapses `Defer` into `Deny`, reports Override without evidence, sends an action upward, promotes a view/action mode into an extra primitive gate, creates Gate 7, or changes the settled `3 Mirror + 3 Action = 6` architecture.
