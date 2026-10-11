---
node_id: "E-530"
canonical_name: "White Energy Recirculation Loop"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Static Cosmic Circulation / Mirror-Gate Release"
claim_gate_detail: "YELLOW (demoted 2026-10-10: equations and Core Rule 10 kill tests not yet re-verified; prior claim: YELLOW (closed accounting and threshold model) / GREEN (quasar/white-hole identification))"
metadata_standard: "I-06"
---

# Node E-530: White Energy Recirculation Loop

**Dependencies**
Upstream: A-115 Unified Compression Field, C-301 Mirror Gate, E-527 Threshold-Triggered Relaxation Oscillator, E-528 Static Redshift Transport, E-529 Low-Coupling Return Mode, Book 5 Ch4
Downstream: future static-universe energy simulation, One-Wave Times

## Definition

**White Energy** is large-scale outward release and reinjection from an over-compressed reservoir through a Mirror-Gate event. The proposed astrophysical examples are quasar and white-hole-scale ejections.

White Energy is not expansion of space and is not a negative-pressure fluid.

## Compact Reservoir

Let \(U_C(t)\) be stored compact compression energy. Adapt the tested E-527 hybrid oscillator:

\[
\frac{dU_C}{dt}
=P_{\rm cap}+P_\nu-\lambda_CU_C-D_WhU_C,
\]

where \(h\in\{0,1\}\) is the release state.

Switching:

\[
h:0\to1\quad\text{when}\quad U_C\ge U_{\rm on},
\]

\[
h:1\to0\quad\text{when}\quad U_C\le U_{\rm off},
\qquad
U_{\rm off}<U_{\rm on}.
\]

The White Energy output power is

\[
P_W=D_WhU_C.
\]

This produces repeated capture/release only when recharge, state-dependent discharge, and hysteresis all exist.

## Cycle Conditions

The charging equilibrium is

\[
U_{\rm charge}=\frac{P_{\rm cap}+P_\nu}{\lambda_C}.
\]

The release equilibrium is

\[
U_{\rm release}=\frac{P_{\rm cap}+P_\nu}{\lambda_C+D_W}.
\]

A repeating White Energy cycle requires

\[
U_{\rm charge}>U_{\rm on},
\qquad
U_{\rm release}<U_{\rm off}.
\]

## Static Global Balance

Let \(E_W\) be energy currently traveling outward in the White Energy channel. Its balance is

\[
\frac{dE_W}{dt}=P_W-P_{W\to\chi}-\Phi_{W,\partial\Omega},
\]

where \(P_{W\to\chi}\) is reinjection into the compression field and \(\Phi_{W,\partial\Omega}\) is any boundary flux leaving the chosen accounting domain.

For a closed domain,

\[
E_{\rm tot}=E_\gamma+E_\chi+E_\nu+E_C+E_W,
\qquad
\frac{dE_{\rm tot}}{dt}=0.
\]

A stationary closed loop requires

\[
\langle P_W\rangle=\langle P_{W\to\chi}\rangle,
\]

and periodic compact-reservoir balance requires

\[
\langle P_W\rangle
=
\langle P_{\rm cap}+P_\nu-\lambda_CU_C\rangle.
\]

White Energy redistributes stored energy. It does not create volume or stretch distance.

## Cosmic Loop

**Local Recycling Mechanism** (per black hole or compressed region):

Compressed structure / lattice discontinuity
-> Boundary conditions create Propagating Light Mode (E-528)
-> Light propagates through friction; oscillations dampen via redshift (E-528: $\frac{d\nu}{d\ell}=-\kappa_\gamma\nu$)
-> Energy dissipated by friction returns directly to field (E-528: field receives $Q_{\gamma\to\chi}=c_L\kappa_\gamma u_\gamma$)
-> Wave flattening releases residual excitation into Low-Coupling Return Mode (neutrino birth; E-529)
-> Neutrino carries residual energy to compact compression reservoir ($Q_{\nu\to C}$; E-529)
-> Compact reservoir accumulates energy; at Mirror-Gate threshold ($U_C \ge U_{\rm on}$) undergoes Mirror crossing
-> Mirror-Gate crossing releases as White Energy ejection (M(ψ_C, ψ_E) → (ψ_E, −ψ_C))
-> White Energy reinjected into field and travels outward ($P_{W\to\chi}$)
-> Reinjected energy creates new boundary conditions, new compressed structures, new lattice discontinuities
-> Cycle repeats; no net expansion required

Energy accounting: $E_{\rm tot}=E_\gamma+E_\chi+E_\nu+E_C+E_W$ remains constant (E-530); local recycling occurs at each site where compression fails or accumulates.

## Yellow Audit

- Quasar/white-hole identification is Green.
- Reservoir parameters are not tied to measured astrophysical systems.
- The path from diffuse field energy into neutrino Return Modes is open.
- The path from Return Modes into compact reservoirs is open.
- The global static balance has not been simulated across a population.

## Bronze Requirement

Run a closed-domain simulation with photon transport loss, field storage, Return-Mode transport, compact capture, and threshold White Energy release. Total energy must remain constant within numerical tolerance while the system reaches a stationary circulation rather than secular growth or decay.
