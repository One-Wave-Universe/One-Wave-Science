---
node_id: "B-221a"
canonical_name: "Six-Step Oscillator Program — Begin Build Hold Build Break Loop"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "Implementation-canonical execution naming; state axes governed by Updated 44"
metadata_standard: "I-06"
---

# Node B-221a: Six-Step Oscillator Program

## Correction

For the current state-machine implementation, the six process labels are:

```text
1 BEGIN
2 BUILD
3 HOLD
4 BUILD
5 BREAK
6 LOOP
```

The oscillator begins from the middle/shared reference `(0)`, unfolds through the six coupled pair positions, returns/crosses the reference between pair states, and loops back toward the next beginning.

This supersedes earlier implementation wording that used `MOVE` as Step 2. `MOVE` remains a movement/operator concept, not the canonical name of the second oscillator gate.

## Pair Mapping

```text
Step 1 BEGIN  = F1/V6
Step 2 BUILD  = V5/F2
Step 3 HOLD   = F3/V4
Step 4 BUILD  = V3/F4
Step 5 BREAK  = F5/V2
Step 6 LOOP   = V1/F6
```

These are six **coupled pair operations**, not twelve serial instructions.

Later executable work in `Nodes/G-739_Six_Gate_Trajectory_Extraction.md` constrains these labels further: they are measured stability regions around a bidirectional oscillator. A complete sequence must not be fabricated when the measured evidence does not support a gate.

## Relationship to the Three Moves and Six Routes

The oscillator gates are not the route address space.

Current executable authority in `UPDATED_43_TWO_CHOICE_THREE_MOVE_SIX_ROUTE_LOGIC.md` defines:

```text
2 binary choices x 3 ternary moves = 6 routes
```

with ternary movement:

```text
DOWN / HOLD / UP = -1 / 0 / +1
```

The number six occurs in both structures, but the meanings are different.

## Relationship to Five-State Self Lifecycle

The five-state self lifecycle is separately defined by `Nodes/G-742_Nonverbal_Loop_Continuity_and_Language_Adapter.md`:

```text
IDLE -> PRIMED -> EXECUTING -> VECTORING -> RESOLVING
```

These behavioral lifecycle states are independent of the six oscillator-gate positions.

## Relationship to Five Commitment/Readout States

Updated 43 owns the current downstream five-state commitment/readout interpretation:

```text
-3(0)3+ = full disagree
-2(0)2+ = partial disagree
1:1      = unity / Hold reference
+2(0)2- = partial agree
+3(0)3- = full agree
```

The transition map into these states remains unresolved until derived or calibrated. They must not be multiplied into the primitive six-route count.

Older neutral `-2,-1,0,+1,+2` modulation notation is compatibility shorthand only. It is not the canonical five-state structure.

## Scale Boundary

Scale labels such as `Micro / Small / Medium / Large / Macro` are not aliases for lifecycle, commitment, route, or oscillator-gate state. A scale mapping must be declared by the domain or derivation that uses it.

## Yellow Audit

- Six oscillator gates remain `Begin -> Build -> Hold -> Build -> Break -> Loop`.
- G-739 governs their measured trajectory interpretation.
- Updated 43 governs the two-choice/three-move six-route primitive and the downstream five commitment/readout states.
- G-742 governs the five-state self lifecycle.
- Matching counts must not collapse independent structures.
- `UPDATED_44_STATE_AXIS_AUTHORITY_AND_EVOLUTION_RULE.md` is the terminology/evolution authority when older wording conflicts.
