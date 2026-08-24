---
node_id: "E-531"
canonical_name: "Moving Finite-Slope Orbital Network"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Field Mechanics, Cognition and Applied Extensions"
claim_gate_detail: "Formalized from UPDATED_39; UPDATED_38 finite-wake memory/assimilation framing is provenance only where superseded."
metadata_standard: "I-06"
---

# E-531 — Moving Finite-Slope Orbital Network

## Purpose
Formalize the current planetary test architecture in which every body carries a moving, body-specific finite displacement/slope region that is recomputed each timestep. No universal cutoff radius and no stored wake-memory term are assumed.

## Core State
For body `i`, define candidate potential and slope fields

`Phi_i(r,t)`

`S_i(r,t) = |grad Phi_i(r,t)|`.

Let the surrounding reference slope be `S_ref(r,t)`. The body's local contrast is

`DeltaS_i(r,t) = S_i(r,t) - S_ref(r,t)`.

Its active domain is

`Omega_i(t) = { r : B_i[DeltaS_i, grad DeltaS_i, curvature_i, ...] > 0 }`

where `B_i` is a yet-to-be-derived boundary functional. The active radius/range is an output of the state, not a hand-set constant.

## Overlap Rule
At target body `k`, construct the instantaneous local slope from all currently overlapping active domains:

`S_local,k(t) = SUM_j W_jk(t) S_j(r_k,t)`

with boundary weight `W_jk in [0,1]` determined by the finite-range law. The relational driver is

`DeltaS_k(t) = S_local,k(t) - S_ref,k(t)`.

The orbital response remains abstract until derived from the field dynamics:

`a_k(t) = -F_OW(DeltaS_k(t), K_eff,k(t))`.

## EM-Shell Modulation
Electromagnetic structure is not added as a gravity-like acceleration. It modifies the local displacement-shell response:

`K_eff,i(t) = K_0,i [1 + eta C_i(t)]`

with `C_i` built from independently measurable magnetic field strength, orientation, shell geometry, and relative state. Mercury may include an additional Sun-Mercury term:

`K_eff,Me = K_0,Me [1 + eta C_Me + eta_SM C_SM]`.

This is a hypothesis to test, not an established electromagnetic-gravitational coupling.

## Falsification Rules
The model fails its own architecture if it requires a universal planetary cutoff, independently tuned range for every planet, independent EM coefficients chosen solely to fit each orbit, fictitious global dipoles for Mars or Venus, or a Mercury term defined only after inspecting the residual it is meant to explain.

## Provenance and Supersession
`UPDATED_38_FINITE_WAKE_THREE_BODY_PERTURBATION_ARCHITECTURE.md` introduced the relational finite-wake test. Its stored-memory/assimilation interpretation is superseded by the instantaneous moving-network rule captured here. Its useful control requirements—ephemeris comparison, tautology checks, and predeclared residual testing—remain applicable.

## Dependencies
A-103 Differential; A-104 Gradient; D-412 Lattice Simulation Standard; D-413 Ground Lattice Orbital-Restoring Simulation; E-503 Pressure Gradient Form.
