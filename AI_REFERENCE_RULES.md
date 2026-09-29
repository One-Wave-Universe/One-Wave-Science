# AI Reference Rules

## Purpose
Prevent drift by forcing every AI workflow to reference the project state before reasoning.

## Required Order

1. Reference first.
2. Load Baseline Zero.
3. Identify current goal.
4. Check existing repo structures and instructions.
5. Only then propose changes.

## Baseline Zero

Baseline Zero contains:

- current repo state
- project goals
- current decisions
- receipts
- known limits

Baseline Zero is a starting reference, not automatic truth.

## Never Flatten Layers

CANON != LOGIC != BENCH != BUILD

Simulation != reality.
Idea != build.
Build != verified result.

## Bridge Rule

When connecting tools or agents:

reference -> investigate -> compare -> receipt -> authorized update

Do not replace existing systems with summaries.
Do not assume missing until the relevant layer has been checked.

## Memory Rule

Memory is a path back to reference.
Memory is not authority.

## Failure Rule

If evidence is missing:
HOLD.

Unknown is a valid output.
