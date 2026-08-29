---
node_id: "B-225"
canonical_name: "Five-Level Modulation Compatibility Around Reference"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Resolution / Formalization Node"
claim_gate_detail: "Legacy coarse modulation compatibility; current five-state authorities are Updated 43 and G-742"
metadata_standard: "I-06"
---

# Node B-225: Five-Level Modulation Compatibility Around Reference

## Current status

This node preserves an older neutral five-level modulation shorthand without allowing it to replace newer state definitions.

Older work used:

```text
+2
+1
 0
-1
-2
```

as a generic coarse strength relation around a local reference. That notation may still be useful in a declared local model, but it is **not the repository's canonical five-state structure**.

## Current five-state authorities

`UPDATED_43_TWO_CHOICE_THREE_MOVE_SIX_ROUTE_LOGIC.md` owns the downstream five commitment/readout states:

```text
-3(0)3+ = full disagree
-2(0)2+ = partial disagree
1:1      = unity / Hold reference
+2(0)2- = partial agree
+3(0)3- = full agree
```

`Nodes/G-742_Nonverbal_Loop_Continuity_and_Language_Adapter.md` separately owns the five-state self lifecycle:

```text
IDLE -> PRIMED -> EXECUTING -> VECTORING -> RESOLVING
```

These are independent axes and neither may be replaced by the legacy `-2,-1,0,+1,+2` shorthand.

## Relationship to the six-route primitive

Updated 43 defines:

```text
2 binary choices x 3 ternary moves = 6 routes
```

The five commitment/readout states are downstream interpretations of route history. They are not primitive choices and must not be multiplied into the route count.

## Relationship to six oscillator gates

`Nodes/G-739_Six_Gate_Trajectory_Extraction.md` defines the measured oscillator labels:

```text
BEGIN -> BUILD(coherent) -> HOLD -> BUILD(unstable) -> BREAK -> LOOP
```

Those six measured regions are also separate from both five-state axes.

## Scale boundary

Older examples sometimes grouped `Micro / Small / Mid / Large / Macro` with five-level modulation. Do not do that. Scale labels are a separate domain/recursive description and require their own declared mapping. A matching count of five is not evidence that the axes are interchangeable.

## Representation wrappers

`Floor / Low / Middle / High / Ceiling`, thermal names, percentages, and the neutral `-2..+2` ladder may be used only as explicitly declared representation or calibration wrappers. They do not define the invariant kernel by themselves.

## Views and strength

The four-view contract still includes `Strength`, but its concrete encoding must name which representation is being used. A caller may not silently assume that `Strength` means this legacy five-level ladder.

## Yellow Audit

- Legacy `-2,-1,0,+1,+2` modulation is compatibility-only.
- Updated 43 is authoritative for five commitment/readout states.
- G-742 is authoritative for the five-state self lifecycle.
- G-739 is authoritative for measured six-gate oscillator classification.
- Scale remains a separate declared axis.
- `UPDATED_44_STATE_AXIS_AUTHORITY_AND_EVOLUTION_RULE.md` governs conflicts among older state terminology.
