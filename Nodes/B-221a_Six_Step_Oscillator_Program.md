---
node_id: "B-221a"
canonical_name: "Six-Step Oscillator Program — Begin Build Hold Build Break Loop"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "Implementation-canonical execution naming"
metadata_standard: "I-06"
---

# Node B-221a: Six-Step Oscillator Program

## Correction

For the current state-machine implementation, the six linear process labels are:

```text
1 BEGIN
2 BUILD
3 HOLD
4 BUILD
5 BREAK
6 LOOP
```

The oscillator begins from the middle/shared reference `(0)`, unfolds through the six coupled pair positions, returns/crosses the reference between pair states, and loops back into the next beginning.

This supersedes earlier implementation wording that used `MOVE` as Step 2. `MOVE` remains a representation/operator concept, not the canonical name of the second process step.

## Pair Mapping

```text
Step 1 BEGIN  = F1/V6
Step 2 BUILD  = V5/F2
Step 3 HOLD   = F3/V4
Step 4 BUILD  = V3/F4
Step 5 BREAK  = F5/V2
Step 6 LOOP   = V1/F6
                 -
              next BEGIN
```

These are six **coupled pair operations**, not twelve serial instructions.

## Oscillatory Geometry

```text
shared middle/reference -(0)+
 -> paired excursion
 -> return toward reference
 -> Mirror Gate crossover '-'
 -> phase/orientation shift
 -> next paired excursion
```

The two sides of each slash pair are simultaneous peak/trough positions of the same opposed relation.

## Relationship to the Three Moves

The six process steps are timing/process positions. The Three Moves are signed differential outcomes:

```text
LEFT / STAY / RIGHT = -1 / 0 / +1
```

Do not replace one structure with the other.

## Relationship to Five Modulation Levels

Each process step may carry one of the five coarse modulation levels `-2,-1,0,+1,+2`. These five levels describe strength/modulation; the five Field lifecycle states are `Idle -> Primed -> Executing -> Vectoring -> Resolving`; and the six steps describe process position.

## Yellow Audit

- Six-step implementation naming and pair mapping are canonical.
- Scale-specific physical meanings of Begin/Build/Hold/Break/Loop remain representations above the invariant kernel.
