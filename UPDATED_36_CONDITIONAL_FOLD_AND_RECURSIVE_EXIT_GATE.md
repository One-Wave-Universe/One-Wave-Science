# UPDATED 36 — Conditional Fold and Recursive Exit Gate

**Status:** Canonical architecture correction for Step 6 recursion control.

## Core rule

Step 6 is not an unconditional loop command. It is an **evaluation gate** that decides whether the resolved consequence is allowed to recurse.

The six-step process remains:

```text
BEGIN -> BUILD -> HOLD -> BUILD -> BREAK -> LOOP
```

but `LOOP` means **permission to recurse**, not automatic recurrence.

## Recursive spiral semantics

Each completed pass may carry its resolved consequence forward as the next local baseline, producing depth rather than flat repetition:

```text
resolved[n]
 -> conditional fold
 -> evaluate
 -> next baseline[n+1] OR hold OR break/reroute
```

The next layer must retain the useful shape of the consequence without blindly accumulating all prior error, noise, saturation, or historical state.

Therefore:

```text
reference[n+1] = bounded_compression(resolved[n])
```

not:

```text
input[n+1] = entire accumulated history
```

## Three Step-6 outcomes

### 1. CONTINUE

Continue is granted only when:

- a meaningful differential remains;
- the resolved trajectory is coherent;
- the result remains inside the permitted state/strength envelope;
- another pass is expected to do real work rather than merely repeat noise.

Action:

```text
RESOLVING[n] -> PRIMED[n+1]
```

The resolved consequence becomes the bounded baseline/reference for the next depth layer.

### 2. HOLD

Hold is selected when the differential has settled inside the neutral/equilibrium band or further recursion would add no useful change.

Action:

```text
RESOLVING -> IDLE
```

The state remains locally available as memory/reference. Hold does not erase the consequence; it stops propagation while preserving the successful resolved state.

### 3. BREAK / REROUTE

Break/Reroute is selected when any of the following occurs:

- differential magnitude exceeds the permitted envelope;
- recursive passes amplify instead of settle;
- the system oscillates without useful convergence;
- trajectory contradicts or destabilizes the active reference;
- saturation, resistance, or anomaly requires pressure relief.

Action:

```text
RESOLVING -> shared (0) reference -> reroute / escalate / terminate local recursion
```

The unstable result must not be directly re-injected as the next recursive baseline.

## Evaluation variables

A minimal simulation/testbench should observe at least:

```text
reference
differential
direction        # -1 / 0 / +1
strength
field_state
recursive_depth
consequence_delta
trajectory_coherence
```

Step 6 should evaluate three broad questions:

```text
1. DIRECTION — is the resolved vector still meaningful?
2. CHANGE    — is the new result materially different from the prior result?
3. BOUND     — is the result still inside the allowed envelope?
```

These resolve to:

```text
CONTINUE | HOLD | BREAK_REROUTE
```

## Five Field lifecycle states inside the recursion

The five Field lifecycle states remain:

```text
IDLE -> PRIMED -> EXECUTING -> VECTORING -> RESOLVING
```

Step 6 does not add a sixth lifecycle state. It evaluates the completed five-state consequence and determines the next relation:

```text
RESOLVING -> IDLE
RESOLVING -> PRIMED at depth n+1
RESOLVING -> boundary/reroute
```

## Relation to the operational stack

A working software or hardware interpretation may be staged as:

```text
1. ingestion / baseline relation
2. ternary vector resolution
3. view-action projection / relational expansion
4. five-state execution
5. null-return / equilibrium check
6. conditional fold and recursive permission
```

These are implementation semantics layered onto the canonical six-step oscillator and must not replace the invariant pair order.

## Stability principle

The architecture preserves **consequence and orientation** across recursive depth while bounding accumulated error.

The goal is not infinite recursion. The goal is a system that can:

```text
deepen when work remains,
settle when resolution is reached,
escape or reroute when local recursion becomes unstable.
```

This is the required escape valve for recursive operation.

## Validation rule

The first software simulation should intentionally exercise at least four cases:

1. stable convergence -> HOLD;
2. bounded useful trajectory -> CONTINUE;
3. non-convergent oscillation -> REROUTE;
4. runaway gain / envelope violation -> BREAK.

Only after those outcomes are distinguishable in simulation should the same control semantics be mapped onto a physical hardware testbench.
