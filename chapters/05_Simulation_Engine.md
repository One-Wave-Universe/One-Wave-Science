# Chapter 05 — Simulation Engine (BASIS v0.2)

**Status:** UNVERIFIED IMPLEMENTATION SPECIFICATION

## Purpose

BASIS is the numerical verification layer for One-Wave claims. The active target is now the combined-state lattice foundation defined in G-764.

## BASIS contract

```
B  Boundary conditions
A  Active state variables
S  Step / solver rule
I  Invariants and measured outputs
S  Stop / falsification criteria
```

## Current Stage-00 engine contract

### Boundary
Declare one of:
- fixed;
- reflecting;
- periodic;
- driven edge.

### Active state
Per site:
- q
- qdot
- phase receipt where defined
- coordinate
- history receipt
- neighbor list

Whole state:
- Q
- RMS amplitude
- RMS rate
- phase coherence
- energy ledger
- circulation/vorticity diagnostic
- octave receipt
- projection error

### Step rule

The baseline is the six-neighbor lattice equation in Chapter 01/G-764.

Required solver order:
1. linear undamped control;
2. linear damped control;
3. driven control;
4. nonlinear candidate;
5. history/hysteresis candidate.

Do not start with the nonlinear hypothesis.

### Invariants / measurements

Minimum:
- finite-state check;
- energy drift;
- max amplitude;
- propagation lag;
- phase/group velocity estimate;
- anisotropy versus direction;
- spectral power;
- coherence;
- combined-state projection error.

### Stop / falsification

A run is INVALID if:
- non-finite values appear;
- timestep convergence fails;
- the same model changes materially with purely numerical orientation;
- data cadence/provenance is lost.

A hypothesis formulation FAILS its current target if:
- the claimed structure disappears under refinement;
- a control explains the same feature;
- a scale feature is created only by octave rescaling;
- source metadata cannot be reproduced exactly.

## Real data adapters

### GWOSC first

Use strain h(t) at its published cadence.

Reference event:
- GW170817
- GPS 1187008882.4
- H1, L1, V1
- 4096 and 16384 Hz public streams

The simulator must preserve the original sample stream and store any resampling as a separate derived dataset.

### CERN second

Reference recorded event:
- CMS DoublePhoton 8 TeV
- Run 194115
- Event 651938592
- LS 702

Use detector measurements/excitations before reconstructed object labels.

## Runtime lifecycle

```
load model
-> validate schema
-> load metadata anchor
-> initialize local lattice
-> run control
-> compute combined state
-> run hypothesis extension
-> ingest real measurement
-> compare
-> log telemetry
-> classify result
```

## Required result classes

- PASS
- FAIL
- INCONCLUSIVE
- INVALID
- DISMISSED

## Minimum telemetry

Every run records:
- model version;
- git SHA;
- source metadata and checksum where available;
- parameters and units;
- seed;
- solver;
- timestep and numerical spacing;
- tolerances;
- local state traces;
- combined-state traces;
- energy/error receipts;
- octave settings;
- control comparison;
- output hashes.

## Promotion boundary

Do not advance the active simulator target to proton-knot/quark-vortex searches until the coupled lattice and combined-state receipts pass the Stage-00 tests in G-764.
