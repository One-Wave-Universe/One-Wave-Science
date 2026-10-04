---
node_id: "G-769"
canonical_name: "Blind Hoyle-State Three-Alpha Attack"
namespace: "NODE"
gate: "BROWN"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "External Benchmark / Nuclear Three-Body Attack"
metadata_standard: "I-06"
---

# G-769 — Blind Hoyle-State Three-Alpha Attack

**Status:** ATTACK DEFINED — NOT SOLVED  
**Gate:** BROWN until an independently calibrated One-Wave model produces a held-out prediction  
**Purpose:** use carbon-12's Hoyle state as an external falsification benchmark for One-Wave micro/PPF/lattice mathematics.

## Question

Can the existing One-Wave framework, without inserting the measured carbon-12 answer, generate a three-alpha-like metastable collective mode with the observed qualitative quantum-number/decay structure and a quantitatively correct energy after one independently established absolute-scale calibration?

A resemblance, triangle picture, 3/6 count, octave relation, or fitted resonance is not a solution.

## Canonical One-Wave chain under attack

```text
D-409 native 3D close-packed coordination
 -> C2/C3/C4 Point/Path/Field rotation
 -> C5/C6/C7 nested PPF
 -> C8 non-double-counted rotation ledger
 -> E6 stable nonlinear localized/recurrent modes
 -> F1 four-interaction state
 -> F2 positive work metric and cross-couplings
 -> F5 independently derived absolute energy scale
 -> F7 micro PPF / alpha-like composite candidate
 -> H7 relational three-body coordinates
 -> Hoyle held-out resonance test
```

The chain may fail at any link. Failure identifies missing or incorrect One-Wave machinery; it must not be patched by importing the held-out target.

## Standard-control state

The physical benchmark is a three-alpha nuclear resonance problem. The attack must retain standard three-body coordinates:
- two Jacobi vectors;
- hyperradius and hyperangle;
- total orientation;
- exchange symmetry for three identical alpha clusters;
- center-of-mass removal;
- continuum/resonance boundary treatment.

The Gray control should use an accepted three-alpha calculation or reproducible literature-grade control before One-Wave terms are enabled.

## Blind-target protocol

### Development-visible information

Allowed while constructing the solver:
- the target system is carbon-12 / three alpha;
- conserved quantum numbers and particle identities required to formulate the control;
- standard physical constants needed by the Gray control;
- numerical convergence criteria;
- generic resonance-search methodology.

### Held-out scoring information

Do not use these to choose One-Wave parameters:
- exact Hoyle excitation energy;
- exact offset above the three-alpha threshold;
- measured width;
- detailed branching fractions;
- radius/shape observables;
- energies of proposed rotational excitations.

A scorer may reveal them only after the One-Wave parameter set and calibration are frozen.

## One-Wave state proposal

Represent three independently obtained alpha-like localized solutions as (Phi_1,Phi_2,Phi_3). Do not hand-draw them into a triangle. Build the composite state

[
X_{3\alpha}=(\boldsymbol\rho,\boldsymbol\lambda,R,\alpha,\Omega;
\Phi_1,\Phi_2,\Phi_3;\Gamma_{PPF},W)
]

where (oldsymbol\rho,oldsymbol\lambda) are Jacobi coordinates, (R) is hyperradius, (alpha) a hyperangle, (Omega) the orientation variables, (Gamma_{PPF}) the nested rotation/circulation ledger, and (W) the F2 work metric.

The candidate energy must be computed from the same frozen One-Wave functional used for the isolated constituents:

[
E_{3\alpha}^{OW}=W[X_{3\alpha}]
]

and the resonance observable is relative to the independently calculated three-constituent threshold,

[
\Delta E_{OW}=E_{3\alpha}^{OW}-3E_{\alpha}^{OW}.
]

This subtraction is essential: a fitted absolute offset cannot manufacture a near-threshold resonance.

## Missing mathematics exposed by the attack

The current repo does not yet justify a numerical Hoyle prediction. Blocking work is:

1. G-728 C2-C8: intrinsic, path and field rotation plus nested PPF and a no-double-count ledger.
2. G-728 D2/D4: native 3D FCC/HCP graph and spectral/isotropy comparison.
3. G-728 E6: stable nonlinear localized modes with continuation/Floquet/Lyapunov tests.
4. G-728 F1/F2: explicit four-interaction state and unit-consistent positive work metric.
5. G-728 F5: absolute energy calibration derived independently of carbon-12.
6. G-728 F7: a reproducible alpha-like composite built from lower-level micro states rather than declared as an input.
7. A nuclear three-body Gray control compatible with H7 coordinates and resonance extraction.

## First executable attack

Do not wait for the entire speculative micro model before testing the geometry.

### Attack 1 — geometry/resonance null test

Use the D-409 3D lattice as a numerical carrier and place three identical generic localized modes on it. Compare:
1. no mutual coupling;
2. pairwise isotropic coupling;
3. the frozen One-Wave candidate coupling once F1/F2 exist.

Sweep initial shape without privileging triangle, chain, or bent-arm configurations. Measure:
- survival time;
- recurrence;
- hyperradius;
- hyperangle distribution;
- permutation symmetry;
- rotation ledger;
- energy/work conservation;
- resonance poles or phase-shift/time-delay proxy;
- sensitivity to lattice orientation, spacing, timestep and boundaries.

A geometry that appears only for one grid orientation is a numerical artifact, not carbon structure.

### Attack 2 — constituent-ablation test

Replace one alpha-like localized mode with:
- a phase-scrambled mode of equal energy;
- a broadened mode;
- a pointlike control;
- a nonlocalized wave packet.

If the claimed resonance is unchanged, the proposed internal PPF/micro structure is not doing explanatory work.

### Attack 3 — blind quantitative score

After F5 calibration is frozen from non-carbon data, run the carbon calculation once and record:
- predicted threshold-relative resonance energy;
- predicted (J^\pi) classification where the model supports it;
- width/lifetime proxy;
- dominant sequential versus direct breakup behavior;
- geometric/radial observables;
- uncertainty from numerical and calibrated parameters.

Then unblind and compare with experimental data.

## Pass / fail

**Advance:** one shared parameter set and independently calibrated scale produce a converged near-threshold three-body resonance and additional held-out observables without carbon-specific retuning.

**Hold:** a robust dimensionless resonance exists but F5 absolute calibration is not yet independently available.

**Fail/revise:** the resonance requires the measured Hoyle energy, a carbon-specific correction coefficient, a preferred lattice orientation, hand-selected triangle geometry, or disappears under refinement/control ablations.

## Immediate conclusion

This node defines an attack, not a solution. The strongest present result is diagnostic: the Hoyle benchmark compresses several open One-Wave problems into one falsifiable chain and makes F5 absolute scale and H7 relational three-body state unavoidable.

## Dependencies

- `Nodes/G-728_Mathematics_Attack_Laundry_List.md`
- `Nodes/D-409_Twelvefold_3D_Close_Packed_Coordination.md`
- `Nodes/G-766_Discrete_Lattice_Dispersion_and_Octave_Emergence_Proof.md`
- `Nodes/G-745_Zone_Edge_125GeV_Lattice_Constant_Hypothesis.md`
- `chapters/01_Continuous_Lattice.md`

## Evidence boundary

Experimental nuclear values are scoring data, not One-Wave derivations. This node must remain BROWN until executable results exist. A successful numerical fit alone is not evidence of a new physical law.
