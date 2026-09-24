# Chapter 3 - Hybrid Procedural Memory and Subconscious Movement

Status: PROPOSED BUILD / SIMULATION REQUIRED

## Goal

The android should perform learned movement without a top-down controller issuing every joint command. Local movement remains founded on `-1(0)+1` choice. Higher systems provide memory, route attention, safety, and correction.

## Memory Split

Exact memory preserves authoritative records such as permissions, maps, safety limits, source code, identity, audit logs, and system snapshots.

Generative memory preserves learned relationships needed to reconstruct context and action. It may interpret the archive; it may not silently replace it.

## Hopfield and Boltzmann Roles

Hopfield-style attractors reconstruct a coherent learned motor pattern from a partial cue. Boltzmann-style dynamics generate or explore plausible completions when the sensory state is incomplete or ambiguous.

```text
Boltzmann proposes candidate movement patterns
-> Hopfield settles toward a learned coherent pattern
-> local choice accepts, holds, counters, or redirects
```

Neither model is imported unchanged. Their useful principles must be implemented inside the One-Wave control architecture and tested against simpler alternatives.

## Subconscious Execution

For each local motor unit,

\[
c_i\in\{-1,0,+1\}.
\]

The zero state is active hold/reference, not absence. A remembered procedure supplies pressures and candidate relations; the local unit still evaluates present sensory feedback before committing movement.

## Top-Down Binary Boundary

Binary logic can allow, block, stop, isolate, or override. It is not the source of normal movement.

```text
choice proposes
-> binary safety checks
-> body commits or holds
```

## Exact Runtime

```text
sensory cue
-> exact-context lookup
-> generative procedural cue
-> route-family scheduling
-> Boltzmann candidates
-> Hopfield settling
-> local -1(0)+1 execution
-> binary safety audit
-> sensory result
-> correction memory and exact journal
```

## First Experiments

1. Pong paddle movement without conscious per-frame commands.
2. Reach toward a target with compensating spine, hip, and foot movement.
3. Maintain balance on a moving support.
4. Interrupt and safely cancel a learned motion.
5. Reconstruct a route from partial sensory cues.
6. Compare hybrid memory with Hopfield-only, Boltzmann-only, periodic, random, and ordinary top-down control.

## Failure Conditions

The design fails if it requires continuous central micromanagement, if generative memory overwrites exact records, if local hold is unavailable, or if the hybrid system produces no measurable advantage over a simpler controller.
