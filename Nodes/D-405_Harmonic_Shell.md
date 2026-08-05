---
node_id: "D-405"
canonical_name: "Harmonic Shell"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Geometry, Resonance, and Simulation"
claim_gate_detail: "YELLOW — GEOMETRY FORMALIZED; ENERGY INTERPRETATION OPEN"
metadata_standard: "I-06"
---

# Node D-405: Harmonic Shell

Dependencies:
Upstream: D-402 Resonant Mode, A-110 Oscillation
Downstream: Books — atomic shells, electron orbital model, proton charge radius;
            D-407 calibration reanalysis; CCD-01

Definition:
A Harmonic Shell is a bounded standing-wave geometry whose closed path contains
an integer number of wavelengths.

Shell condition:

2 pi R = n lambda,  n in Z+

where:
R = shell radius,
lambda = wavelength along the closed path,
n = integer winding/shell count.

Mathematics — variable-radius, fixed-wavelength family:

R_n = n lambda/(2 pi)
DeltaR = R_(n+1)-R_n = lambda/(2 pi).

This defines equally spaced shell-center radii if lambda is held fixed.

## Critical model distinction

There are two different quantization problems that must not be mixed:

1. Variable radius, fixed lambda:
   R_n = n lambda/(2 pi).
   Here n counts how many copies of the same wavelength fit around successively
   larger closed paths.

2. Fixed boundary radius, variable wavenumber:
   k_n = n/R.
   Here n changes the allowed wavenumber and can generate a dispersion-based
   frequency/energy ladder.

The original node used Model 1 geometry but borrowed Model 2 energy intuition.
For Model 1:

k_n = n/R_n = 2 pi/lambda,

so k_n is independent of n. Therefore E_n=hbar omega(k_n) alone gives no
nonzero adjacent-shell energy spacing.

A nonzero energy ladder requires an additional derived model, for example:

- E_n = n epsilon_lambda from an action/energy per wavelength;
- radial eigenvalues k_(r,n) from a boundary-value equation;
- curvature/pressure/surface/coupling energy depending on R_n;
- nonlinear collective-mode energy.

D-405 currently quantizes geometry. It does not yet quantize energy.

## Connection to D-407

D-407 removes a false calibration fork: neutron-profile width sigma is not
shell-center spacing. Under an unproved adjacent-shell assumption, the neutron
radii select a provisional n=7,8 assignment and lambda approximately 0.6594 fm.
This is a conditional sensitivity-test value, not a measured constant.

## CCD-01 relationship

The shell condition may contribute to a minimum-action derivation only after the
energy/action assigned to one closed wavelength is derived. Geometry alone does
not establish S_min=hbar.

Operational Chain:
Resonant Mode + closed-path wavelength condition => Harmonic Shell geometry
=> [energy model still required] => quantitative atomic/nuclear structure

Yellow Audit:
- closed-path geometry and uniform center spacing are explicit;
- variable-radius versus fixed-radius quantization is now separated;
- current geometry does not create an n-dependent k spectrum;
- lambda is not independently measured;
- D-407's 0.6594 fm candidate is conditional on an unproved 7/8 adjacency;
- action/energy per shell is not derived;
- radial stability hierarchy is not established;
- relationship to the neutron two-profile model remains conditional.

Future Work:
Derive the physical boundary-value problem that decides between fixed-R
wavenumber quantization, variable-R winding shells, or radial eigenmodes.
Derive shell energy from lattice pressure, curvature, coupling, or action.
Recover the neutron-profile fit and uncertainties before treating D-407 as a
calibration.
Apply only the derived model to atomic and carbon calculations.
