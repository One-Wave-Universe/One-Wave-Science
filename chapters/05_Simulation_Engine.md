# Chapter 05 — Simulation Engine (BASIS v0.1)

**Status:** implementation specification

## Objective
Provide a minimal runtime contract for testing One-Wave hypotheses without allowing domain language to bypass units, state definitions, or baseline comparisons.

## BASIS v0.1 contract
Each simulation declares:

```text
B  Boundary conditions
A  Active state variables
S  Step / solver rule
I  Invariants and measured outputs
S  Stop / falsification criteria
```

## Runtime lifecycle
```text
load model
-> validate schema
-> initialize state
-> run control
-> run hypothesis variant
-> record receipts
-> compare
-> classify result
```

## Required result classes
- PASS: stated test passed
- FAIL: stated test failed
- INCONCLUSIVE: test could not discriminate
- INVALID: units, solver, setup, or data made the run unusable

## Reproducibility receipt
Every run should record model version, git SHA, parameters, seed where applicable, solver, timestep, tolerances, output hashes, and comparison metric.

## Integration
This chapter is a specification layer. Existing validated simulators and Virtual Breadboard remain authoritative for their own numerical contracts.
