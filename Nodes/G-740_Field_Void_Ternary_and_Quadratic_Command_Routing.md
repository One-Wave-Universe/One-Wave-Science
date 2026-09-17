---
node_id: "G-740"
canonical_name: "Field/Void Ternary and Quadratic Command Routing"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Legacy G-Series / Canonicalized Node"
claim_gate_detail: "Routing contract projected onto three physical bidirectional A/B/C mirrors; Views propagate up and Actions down through the same mirrors"
metadata_standard: "I-06"
---

# Node G-740: Field/Void Ternary and Quadratic Command Routing

## Scope boundary

This file is a **domain node**, not a replacement for Algorythm-Zer0.

Algorythm-Zer0 owns universal control primitives. This node owns one body/brain/sensor/action interpretation of those primitives. Domain-specific physics, biology, hardware, sensory, environmental, mental, and emotional mappings stay in nodes/chapters unless separately shown to be universal algorithm machinery.

Working semantic distinction:

```text
FIELD = active interactions
VOID  = unexpressed potential
```

The shared reference remains the comparison/balance relation between them; it is not a third polarity.

## Physical primitive lock

CELL_V1 uses exactly three physical bidirectional Mirror axes:

```text
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

These produce six directed edge interfaces, not six separate physical gates.

Any legacy six-position notation such as:

```text
M1 -> A1 -> M2 -> A2 -> M3 -> A3
```

is a **logical/receipt sequence only**. `M` and `A` describe read/view versus conditioning/action phases of the recurrence. They do not denote six distinct hardware gates.

## Direction invariant

The same three mirrors carry both directions:

```text
UP   = Views / state / relation toward higher resolution
DOWN = Actions / conditioning / Override toward lower/local state
```

There is no separate Action-gate hardware layer and no Field/Void identity swap.

The recurrence is:

```text
local retained state
 -> View UP
 -> local/higher resolution
 -> no intervention OR Action/Override DOWN
 -> resulting local state
 -> next View UP
```

The return is not a reset. The resulting physical configuration is the **new state**.

## Locked Field/Void routing vocabulary

Field and Void remain counterparts around the shared reference.

| Layer | Field | Void |
|---|---|---|
| Ternary | Express / Hold / Compress | Confirm / Defer / Deny |
| Quadratic Views UP | Direction / Phase / Strength / Reference | corresponding opposed/reference views |
| Quadratic Actions DOWN | Inward / Outward / Across / Over | corresponding opposed/override modes |

The four View names and four Action-mode names are descriptors, not extra gates.

`Defer` preserves Hold while evidence/readiness is insufficient. `Deny` may produce Override. `Confirm` permits continuation.

## Binary and ternary address space

Keep the route count separate from the hardware count:

```text
binary relation = YES / NO
ternary move = DOWN / HOLD / UP
2 x 3 = 6 route addresses
```

Ground/no committed binary choice is outside the six-route set.

`HOLD` is active balance, not absence.

For nerve/motor use, the same ternary relation is also the candidate local motion command: one orientation / balanced Hold / opposite orientation.

## Domain-state mapping

The same recursive control structure does **not** require every stage to describe the same kind of state. In the current body/brain interpretation, each stage resolves a different domain:

```text
CHOICE
  -> ENERGY STATE
     reserve, strain, reinjection capacity, available power,
     whether a condition is important enough to propagate

MOVE
  -> BODY STATE
     balance, tension, posture, motion, load, local reflex condition

VIEWS UP
  -> LANDSCAPE / ENVIRONMENT STATE
     current surroundings, spatial relation, objects, sound scene,
     terrain, threats, opportunities, external sensor organization

ACTIONS DOWN
  -> MENTAL / INTENT STATE
     selected or prepared intervention sent toward lower/local control

CONSEQUENCE
  -> EMOTIONAL / VALUE STATE
     whether the result was beneficial/costly, safe/dangerous,
     attractive/aversive, relieving/stressing, repeat/avoid weighted
```

The compact flow is:

```text
ENERGY
  -> BODY
  -> LANDSCAPE / ENVIRONMENT
  -> MENTAL / ACTION
  -> EMOTIONAL CONSEQUENCE
  -> RETAINED MEMORY / UPDATED REFERENCE
  -> next cycle
```

`CONSEQUENCE` is not a new physical gate. It is the evaluated result of the completed action/state transition and can alter retained memory/reference for the next Choice.

The mapping is currently a working architecture hypothesis. Exact variables, weights, thresholds, and biological correspondence remain open and belong in their appropriate nodes/chapters rather than being silently hard-coded into Algorythm-Zer0.

## DC / AC / reinjection relationship

At the nerve level:

```text
DC = supply + controlled recovery + reinjection
AC = alternating/recurring activity through the mirrored paths
TERNARY = local UP/HOLD/DOWN movement and motor command
QUADRATIC = Views UP / Actions DOWN
```

`V0` is the local electrical reference and must not be used as an energy reservoir or recovery dump.

A candidate supervisory policy is:

```text
within declared local limits -> continue / recover / reinject locally
outside declared limits -> Views UP -> higher resolution -> Action/Override DOWN
```

The exact limits and resource variables are experimental.

## Processing-memory contract

The active stateful path is intended to perform both processing and memory:

```text
state affects present flow
 -> present flow changes the same state
 -> changed state persists locally
 -> next pass encounters the changed state
```

The exact carrier is open. Memristive, hysteretic magnetic, spintronic/magnetoresistive, oscillatory, or other stateful implementations may be tested.

The architecture fails this contract if the claimed memory can be removed from the active A/B/C processing path without changing the operation.

## Decision and connection separation

Current physical-role contract:

```text
local measured differential / state = decision variable
stateful physical path = processing-memory candidate
true bidirectional switch = nerve-gate / connection candidate
```

Back-to-back MOSFETs or another true bidirectional switch may be used. SiC MOSFETs remain candidates where later power-domain properties are useful, but direct millivolt/microvolt gate control is not assumed; any interface must be explicit and measured.

## Three-way downward coordination hypothesis

A higher Override may coordinate three lower A/B/C path changes:

```text
one resolved Override
 -> A path conditioning
 -> B path conditioning
 -> C path conditioning
```

This is a fan-out/compression hypothesis, not three new physical gates. It remains experimental until one event reproducibly causes the intended three measured transitions.

## Count boundary

Keep these separate:

```text
physical mirrors: 3 bidirectional A/B/C axes
directed CELL_V1 interfaces: 6
route address space: 2 x 3 = 6
logical/receipt positions: optional six-position description
view descriptors: 4
action-mode descriptors: 4
```

No matching count may be used to invent another hardware layer.

## Compatibility boundary

Older text that says:

```text
3 Mirror gates + 3 Action gates = 6 physical gates
```

is superseded for CELL_V1 hardware.

If the old `M1/A1/M2/A2/M3/A3` names are retained in software receipts, each receipt must also identify:

1. physical axis `A`, `B`, or `C`;
2. physical direction `UP` or `DOWN`;
3. edge interface used (`A+`, `A-`, etc.);
4. View or Action descriptor, if any;
5. pre-state;
6. resulting state;
7. whether local reinjection continued or higher Override occurred.

The receipt fails if it implies six distinct physical Mirror/Action gates, sends Actions up, sends Views down, creates Gate 7, resets the old state automatically, or separates processing memory from the active stateful path without declaring a different experiment.
