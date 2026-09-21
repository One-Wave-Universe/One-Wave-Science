# Chapter 05 — Simulation Engine (BASIS v0.1)

**Status:** UNVERIFIED IMPLEMENTATION SPECIFICATION

## Purpose

BASIS v0.1 is the proposed numerical verification layer for One-Wave claims.

## Proposed stack

- Python
- NumPy
- SciPy
- iterative lattice-density loops
- vortex/state-transition models
- CSV telemetry
- reproducible parameter receipts

## BASIS contract

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
-> log telemetry
-> compare
-> classify result
```

## Required result classes

- PASS — predefined test passed
- FAIL — predefined test failed
- INCONCLUSIVE — test did not discriminate
- INVALID — setup, units, solver, or data invalidated the run
- DISMISSED — repeated valid tests contradict the hypothesis strongly enough to retire that formulation

## Minimum telemetry

Every run should record:
- model version;
- git SHA;
- parameters;
- seed where applicable;
- solver;
- timestep;
- tolerances;
- state traces;
- CSV output;
- output hashes;
- control result;
- comparison metric.

Existing validated simulators and Virtual Breadboard remain authoritative for their own numerical contracts.
