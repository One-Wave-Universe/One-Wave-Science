# Primitive Convergence Rule

Status: governing architecture rule

## Purpose

Every higher-level project, domain version, simulator, controller, memory system, or software tool that uses the recurring One-Wave structural family should make the primitive build clearer over time.

The projects are not the primitive. They are different versions and stress-tests of recurring structure.

The job of comparison is to strip away domain-specific detail and ask what survives.

## Core convergence rule

For every project/version, record four things:

1. **What structural relation it uses**
2. **What is specific to that project/domain**
3. **What survives when compared with other versions**
4. **What this teaches us to build or test next at the primitive level**

Do not promote a feature into the primitive merely because one project uses it.

A feature becomes a stronger primitive candidate only when it recurs across different versions while preserving the same functional role despite changes in vocabulary, scale, timing, carrier, or implementation.

## Primitive candidate categories

The current recurring candidate structure includes:

- shared reference / center
- opposed or mirrored relations
- binary commitment or polarity choice
- ternary movement / resolution around Hold
- paired view/action flow
- fast local response plus slower oversight/override
- local state retention
- routing between scales or subsystems
- proposal versus acceptance/commitment
- consequence returning as the next reference
- receipts that preserve direction, phase, prior state, and route identity
- recursion: a completed unit can become a node in a larger unit

These are architecture candidates, not proof of a physical primitive.

## Version discipline

Different versions may implement the same structural role differently.

Examples:

- a software project may express Hold as a queue or deferred state;
- a motor controller may express Hold as zero net movement with active current/reference maintenance;
- a memory system may express Hold as retained attractor state;
- an animator may express Hold as unchanged frame exposure or preserved scene state;
- a physical primitive experiment may express Hold as an electrical or oscillatory center condition.

Same role does not require same mechanism.

## Project extraction template

Each project should eventually expose a small architecture receipt:

```text
PROJECT / VERSION:

INPUT:
LOCAL STATE:
REFERENCE:
BINARY RELATION:
TERNARY RESOLUTION:
VIEW UP:
ROUTING / TIMING:
OVERSIGHT:
ACTION DOWN:
CONSEQUENCE:
NEXT REFERENCE:
MEMORY / RECEIPT:

DOMAIN-SPECIFIC PARTS:
SHARED STRUCTURE CANDIDATES:
WHAT THIS CHANGES ABOUT THE PRIMITIVE BUILD:
NEXT PRIMITIVE TEST:
```

The exact fields may be adapted when a project does not use every layer, but missing layers must be explicit rather than silently invented.

## Convergence ladder

The primitive should become clearer through repeated comparison:

```text
project behavior
-> project receipt
-> compare across versions
-> remove domain-only features
-> identify recurring relation
-> encode smallest executable model
-> test failure cases
-> simplify again
-> physical/software primitive candidate
```

This is intentionally iterative. The primitive is not declared first and forced onto projects afterward.

## Build direction

The next work should therefore happen in two directions at once:

### Upward

Build useful project versions with explicit interfaces and receipts.

### Downward

Continuously compress what those projects teach back toward the smallest common build.

This creates a feedback loop:

```text
primitive candidate
-> project version
-> consequence / behavior
-> structural comparison
-> revised primitive candidate
```

## What not to do

- Do not treat every project detail as universal architecture.
- Do not treat matching numbers as evidence of identical structures.
- Do not make one project's vocabulary canonical for all other versions.
- Do not keep adding architecture layers without asking whether they simplify the primitive.
- Do not call project behavior proof of the primitive.
- Do not discard a useful version merely because its implementation differs from another version.

## Immediate next structure

1. Create architecture receipts for the current major versions: VTC, M4/droid control, memory reconstruction, bench primitive, and animator/software workflow.
2. Compare only functional roles, not names.
3. Build a cross-version invariant table.
4. Mark each candidate as:
   - appears in one version
   - appears in multiple versions
   - appears across scale/domain changes
   - required for reversibility or stable operation
5. Use that table to define the smallest next primitive simulation/build.
6. Change one primitive feature at a time and feed the result back into the project versions.

## Success condition

The repository is moving in the right direction when adding a project or experiment reduces uncertainty about the primitive rather than merely increasing the number of files.
