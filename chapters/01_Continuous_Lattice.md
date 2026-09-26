# Chapter 01 — Continuous Lattice Mechanics

**Status:** UNVERIFIED HYPOTHESIS — current simulation foundation

## Core premise

One-Wave proposes a continuous medium. The numerical lattice is only a discretization used to test that proposal. A discrete grid is not evidence that nature has a discrete lattice spacing.

The immediate target is the smallest model that can grow from local states into a measured combined state.

## Primitive state

At numerical site (i):

[
X_i=(q_i,dot q_i,phi_i,mathbf{x}_i,h_i).
]

(q_i) is signed displacement/excitation about a declared reference. No particle identity is required.

## Geometry

The first 2D numerical stencil uses a triangular lattice with six nearest neighbors:

[
mathbf a_1=a_{m num}(1,0),qquad
mathbf a_2=a_{m num}(1/2,sqrt3/2).
]

For the first runs (a_{m num}=1). It is dimensionless numerical spacing until an independent physical calibration exists.

## Baseline dynamics

Use a control equation that is standard enough to debug:

[
ddot q_i+2zetaomega_0dot q_i+omega_0^2q_i+lambda q_i^3
=c_L^2(Delta_hq)_i+d_i(t),
]

[
(Delta_hq)_i=rac{1}{a_{m num}^2}sum_{jin N(i)}(q_j-q_i).
]

Run (lambda=0) first. Nonlinear structure is added only after the linear lattice passes conservation and dispersion tests.

## Local to combined state

The simulator must report both local nodes and the resolved whole:

[
Q=N^{-1}sum_iq_i,
quad
A_{m rms}=sqrt{N^{-1}sum_iq_i^2},
quad
V_{m rms}=sqrt{N^{-1}sum_idot q_i^2}.
]

If a phase is defined from the oscillator state,

[
C_phi=left|N^{-1}sum_i e^{iphi_i}ight|.
]

A higher-scale point is not created by declaration. It is created only when a projection (P(X_1,ldots,X_N)	o X_{m whole}) has a measured reconstruction/projection error.

## Point → Path → Field → Resolved Whole

POINT:
one local lattice state.

PATH:
ordered transport/history through linked sites.

FIELD:
the full distributed state and its gradients/circulation.

RESOLVED WHOLE:
a compact combined-state receipt that preserves the observables needed by the next scale.

This replaces any shortcut that jumps directly from a node to a named physical object.

## Octave / scale handling

Frequency octave:

[
f_n=2^nf_0.
]

Amplitude scaling and geometry scaling are independent derived transforms and must never overwrite source measurements.

## Real-number anchors

The first metadata anchors are deliberately measurements, not fitted theory constants:

- GW170817: GPS 1187008882.4; H1/L1/V1; public strain at 4096 Hz and 16384 Hz.
- CMS DoublePhoton: 8 TeV pp; Run 194115; Event 651938592; LS 702.
- CMS record 12220: tracker-hit coordinates from simulated 8 TeV collision samples, useful for detector-geometry tests.

These constrain input cadence, provenance, and later comparisons. They do not derive a physical lattice constant.

## Current simulator target

The current target is **coupled lattice → combined state → real waveform ingest**.

Proton knots, quark vortices, ATP, gravity, and larger structures are downstream targets. They may not be hard-coded into the primitive.

## Required verification packet

Every run declares:

- dimensionality and boundaries;
- state variables and units;
- governing equation;
- numerical spacing and timestep;
- solver;
- conservation/dissipation ledger;
- metadata source;
- control model;
- combined-state projection;
- octave transform, if used;
- falsification criterion.

## Immediate tests

1. zero-input hold;
2. single impulse and radial propagation;
3. two-source interference;
4. reflected boundary;
5. periodic boundary;
6. timestep refinement;
7. sixfold anisotropy map;
8. combined-state receipt;
9. real GWOSC sample ingestion;
10. CERN excitation-field ingestion.

## Canon links

- `Nodes/G-764_Combined_State_Lattice_Simulator_Foundation.md`
- `Nodes/D-417_Hexagonal_Lattice_Interaction_Dynamics.md`
- `Nodes/E-531_Dual_Harmonic_Propagation_Operator.md`
- `chapters/05_Simulation_Engine.md`
