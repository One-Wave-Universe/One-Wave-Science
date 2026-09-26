---
node_id: "G-764"
canonical_name: "Combined-State Lattice Simulator Foundation"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Simulation Foundation / Continuous-Lattice Discretization / Data Alignment"
claim_gate_detail: "YELLOW — equations, combined-state receipt, real-data metadata anchors, and controls defined; physical lattice spacing and nonlinear bound modes remain open"
metadata_standard: "I-06"
---

# G-764 — Combined-State Lattice Simulator Foundation

## Purpose

Define the lowest simulator that all later One-Wave structures must grow from.

The primitive is not a cell and not a particle. It is one local degree of freedom of a numerically discretized continuous medium. Many sites evolve together and resolve into a measurable **combined state**.

## Dependencies

- Chapter 01 — Continuous Lattice Mechanics
- Chapter 05 — Simulation Engine / BASIS
- D-408 sixfold lattice geometry
- D-417 hexagonal lattice interaction dynamics
- E-531 dual-harmonic propagation boundary
- G-728 C1/D1/E1/E3 work queue
- `sims/00_CANONICAL_INGEST_RULE.md`

## Minimal site state

For site i:

[
X_i=(q_i,dot q_i,phi_i,mathbf{x}_i,h_i)
]

where:

- (q_i): signed local displacement/excitation about reference
- (dot q_i): local rate
- (phi_i): phase derived from the simulated oscillatory state, not from a particle label
- (mathbf{x}_i): numerical lattice coordinate
- (h_i): retained local history receipt

No physical lattice spacing is assumed.

## First lawful coupled equation

The first control-class lattice equation is:

[
ddot q_i + 2zetaomega_0dot q_i + omega_0^2 q_i
+ lambda q_i^3
=
c_L^2(Delta_h q)_i + d_i(t)
]

with the six-neighbor triangular-lattice Laplacian

[
(Delta_hq)_i = rac{1}{a_{m num}^2}sum_{jin N(i)}(q_j-q_i).
]

For the first simulator set (a_{m num}=1). It is a numerical coordinate, not a derived physical lattice constant.

The linear control is obtained by (lambda=0). The nonlinear term must be ablated before any stable-knot claim.

## Combined-state receipt

The simulator must not stop at local nodes.

For N active sites define:

[
Q=rac{1}{N}sum_i q_i,
qquad
A_{m rms}=sqrt{rac{1}{N}sum_iq_i^2},
]

[
V_{m rms}=sqrt{rac{1}{N}sum_idot q_i^2},
]

and a phase-coherence receipt

[
C_phi=
left|rac{1}{N}sum_i e^{iphi_i}ight|.
]

The combined state is:

[
X_{m whole} =
(Q,A_{m rms},V_{m rms},C_phi,E,Gamma,Omega).
]

(E) is the declared numerical energy ledger, (Gamma) is circulation/vorticity diagnostic, and (Omega) is the octave/scale receipt.

A resolved whole may only become a next-scale point after its projection error is measured.

## Real metadata alignment

The first external anchors are stored in:

`sims/00-lattice-primitive/metadata-anchors.json`

They include:

- GW170817 GPS 1187008882.4
- H1/L1/V1 detector identities
- 4096 Hz and 16384 Hz strain sample rates
- CMS 8 TeV DoublePhoton Run 194115 / Event 651938592 / LS 702
- CMS tracker-hit record 12220 as a simulated detector-geometry reference

These values constrain ingest cadence and provenance. They do not define lattice spacing, site energy, or a mass scale.

## Why GWOSC is the first calibration target

GWOSC strain is already a signed continuous measurement stream around a reference and therefore tests propagation with fewer reconstruction layers than collider events.

First calibration target:

1. drive one boundary/site from a short real strain segment;
2. preserve its exact sample cadence;
3. compare input/output lag, spectral content, dispersion, coherence, and energy bookkeeping;
4. run linear Gray/control lattice;
5. only then enable One-Wave nonlinear/history terms.

CERN is the second target for collision/excitation-field geometry.

## Octave rule

For frequency analysis:

[
f_n=2^n f_0.
]

For a derived amplitude or geometry view:

[
A_n=2^nA_0,qquad r_n=2^nr_0
]

only when that transform is explicitly enabled.

These three operations are separate.

## Current falsification gates

Before proton-knot, quark-vortex, ATP, or higher-scale simulations:

1. zero state stays zero;
2. energy drift is bounded in the undamped control;
3. measured group velocity converges with timestep refinement;
4. sixfold anisotropy is measured, not ignored;
5. combined-state projection error is reported;
6. randomized/reflected controls are available;
7. real-data ingest preserves source samples exactly;
8. nonlinear localized modes survive perturbation and solver refinement before being named knot/vortex candidates.

## Build order

LATTICE SITE
→ COUPLED LATTICE
→ COMBINED STATE
→ REAL WAVE INGEST (GWOSC)
→ COLLISION EXCITATION INGEST (CERN)
→ STABLE LOOP/VORTEX SEARCH
→ PROTON-LIKE / QUARK-LIKE HYPOTHESIS TESTS
→ ATP / BIOENERGETIC TRANSFER
→ larger physics.

