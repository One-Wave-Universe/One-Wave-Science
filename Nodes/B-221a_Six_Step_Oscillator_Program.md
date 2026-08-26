---
node_id: "B-221a"
canonical_name: "Six-Step Oscillator Program — Begin Build Hold Build Break Loop"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "Implementation-canonical execution naming; physical cell mapping separated"
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

These are six **coupled logical pair operations**, not twelve serial instructions.

`/` means one simultaneous mirrored relation. The paired-exchange rule is defined by B-206.

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

## Computing-Primitive Boundary

The six logical pair positions are **not** six independent transistor-like gates inside one conventional cell.

The current physical interpretation from the VTC build is:

```text
one differential triad
= two physically linked/opposed mirror elements
+ one differential evaluator
= three active elements

three triads
= nine-element base cluster
= three physical Mirror Gates

3 physical Mirror Gates x 2 orientations/phases
= 6 logical pair positions
```

Therefore the counting layers must remain separate:

```text
physical primitive:       2 opposed mirror elements + differential evaluator
logical oscillator:       6 coupled pair positions
base physical cluster:    3 differential triads / 3 physical Mirror Gates
```

Do not collapse these into the statement `6 gates = 1 cell`.

## Differential Cell Interface

For computing, the current working interface is relational:

```text
signal/relation IN
 -> DC engage / nothing
 -> OUTWARD local expression
 -> local AC differential (-1 / 0 / +1)
 -> ACROSS shared differential between mirrored cells
 -> OVER connection / crossover
 -> next differential
```

Two mirrored cells each expose signal-in and expressed differential-out. Their shared differential becomes the relation consumed by the next stage.

Recursive-interface rule:

```text
OUTPUT relation of level n == INPUT relation expected by level n+1
```

This is why a complete higher-level cluster can behave externally like one larger relational node without requiring the next level to know its internal implementation.

## Relationship to the Three Moves

The six process steps are timing/process positions. The Three Moves are signed differential outcomes:

```text
LEFT / STAY / RIGHT = -1 / 0 / +1
```

Do not replace one structure with the other.

## Relationship to Five States

Each process step may carry one of the five coarse modulation states `-2,-1,0,+1,+2`. The five states describe strength/modulation; the six steps describe process position.

## Yellow Audit

- Six-step implementation naming and pair mapping are canonical within the current state-machine model.
- The distinction between logical pair positions, physical Mirror Gates, triads, and mirrored cells must remain explicit.
- The exact minimum physical hardware for one complete computing cell remains experimental.
- Two triads are a minimum candidate for time-shared arithmetic; three triads provide a clearer dedicated experimental cluster. Hardware measurement decides the minimum.
- Scale-specific physical meanings of Begin/Build/Hold/Break/Loop remain representations above the invariant kernel.
