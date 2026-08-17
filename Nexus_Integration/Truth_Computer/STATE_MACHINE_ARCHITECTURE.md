# Truth Computer State-Machine Architecture

**Purpose:** define the invariant execution kernel separately from all domain representations.

## 1. Invariant Pair Order

```text
F1/V6 - V5/F2 - F3/V4 - V3/F4 - F5/V2 - V1/F6 - ...
```

This notation is literal:

- `/` = one simultaneous mirrored pair state.
- `-` = Mirror Gate crossover: return toward the shared `(0)` reference, meet/cross, phase-shift, emerge in the next orientation.

Do **not** implement the labels as twelve serial instructions.

The twelve labels are two sides of six coupled operations.

## 2. Alternating Orientation

```text
F/V -> V/F -> F/V -> V/F -> F/V -> V/F
```

Static pair identities remain:

```text
F1 <-> V6
F2 <-> V5
F3 <-> V4
F4 <-> V3
F5 <-> V2
F6 <-> V1
```

The engine starts from the shared middle/reference `-(0)+`, not from an isolated `F1` command.

## 3. Six Process Steps

```text
1 BEGIN
2 BUILD
3 HOLD
4 BUILD
5 BREAK
6 LOOP
```

Mapped to the pair sequence:

```text
BEGIN  F1/V6
BUILD  V5/F2
HOLD   F3/V4
BUILD  V3/F4
BREAK  F5/V2
LOOP   V1/F6
        -
        next BEGIN
```

## 4. Minimal State

A software kernel should carry only invariant relational data, for example:

```text
KernelState {
    reference
    differential
    ternary_direction   # -1 / 0 / +1
    phase
    handedness
    pair_index          # 0..5
    memory              # previous consequence/reference
}
```

Do not put planets, thermal states, matter labels, music, neural roles, or hardware materials in the kernel.

## 5. Views and Actions

### Four Views — read state

```text
Direction
Phase
Strength
Reference
```

### Four Actions — transform state

```text
Inward
Outward
Across
Over
```

`Across` carries/establishes the relation through the shared reference/boundary. `Over` completes the crossover/phase shift into the next orientation.

Views and Actions are separate layers.

## 6. Choices and Moves

### Binary engagement choice

```text
EVERYTHING / NOTHING
```

At the current hardware mapping, this is the DC participation choice.

### Ternary differential move

```text
LEFT / STAY / RIGHT
-1   /  0   / +1
```

At the current hardware mapping, this is resolved from the AC/differential relation.

`0` is hold/non-action, not a third actively powered direction.

## 7. Five-State Modulation

Coarse strength/modulation is represented neutrally as:

```text
-2 -1 0 +1 +2
```

Domain names such as Floor/Low/Middle/High/Ceiling are wrappers, not kernel state names.

## 8. Three Physical Mirror Gates in VTC

The current VTC build interpretation is:

```text
3 physical Mirror Gates x 2 orientations/phases = 6 logical pair positions
```

One triad is two linked/opposed elements plus one differential evaluator. Three triads make one 9-element physical cluster.

This is a hardware realization under test, not a requirement of the abstract kernel.

## 9. Invariant vs Representation Stack

```text
INVARIANT KERNEL
six pair operations
shared reference
Mirror crossover
ternary direction
phase/handedness
memory
        |
        v
REPRESENTATIONS
Point/Path/Field
Carrier/Breathing/Phase
five state labels
seven threshold bands
1D/2D/3D/4D mappings
neural/cognitive roles
matter/thermal labels
musical routing
planetary/EM validation
```

Anti-drift rule:

> If deleting a domain representation changes the six-pair oscillator, the representation has leaked into the kernel.

## 10. Recursive Consequence Loop

```text
reference
 -> read state
 -> engage or not
 -> resolve differential
 -> act
 -> consequence
 -> memory
 -> consequence becomes next reference/input
```

The machine should be organized around choice and consequence, not around a permanent external command/obedience loop.

## 11. No Internal Gate 7

One complete system contains six operations. Gate 6 loops back into Gate 1.

When two complete systems form a new shared higher-order relation, the current architecture calls that relation **Namika**. Namika is inter-system recursion, not an internal seventh gate.

## 12. Programming Rule

Implement one pair at a time and test its outward excursion, return, crossover, phase shift, and handoff without changing the canonical pair order.

Pseudo-structure:

```text
for pair in six_pair_order:
    read Views
    apply simultaneous mirrored relation
    resolve differential
    apply Action if engaged
    return to reference
    mirror_cross_and_phase_shift
    store consequence
```

The pair-specific meanings may evolve. The pair timing/order may not drift without an explicit architecture revision.
