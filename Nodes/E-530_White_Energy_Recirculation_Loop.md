---
node_id: "E-530"
canonical_name: "White Energy Recirculation Loop"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Static Cosmic Circulation / Mirror-Gate Release"
claim_gate_detail: "YELLOW (closed accounting and threshold model) / GREEN (quasar/white-hole identification)"
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

```text
Mass Effect / compressed structure
-> gravity and extended compression
-> Propagating Light Mode loses energy (redshift)
-> field reservoir
-> Low-Coupling Return Modes
-> compact compression reservoir
-> Mirror-Gate threshold
-> White Energy ejection
-> field reinjection
-> new structure and Mass Effect
```

## Yellow Audit

- Quasar/white-hole identification is Green.
- Reservoir parameters are not tied to measured astrophysical systems.
- The path from diffuse field energy into neutrino Return Modes is open.
- The path from Return Modes into compact reservoirs is open.
- The global static balance has not been simulated across a population.
- UNACCOUNTED SINK: `lambda_C * U_C` in the `dU_C/dt` equation has no
  destination anywhere in the stated system. `P_cap` and `P_nu` are
  transfers in (they should appear as matching drains in whichever
  channel's own balance equation sources them), and `D_W*h*U_C` correctly
  reappears as `P_W`, the source term in `dE_W/dt`. But `lambda_C*U_C`
  does not reappear as a `+lambda_C*U_C` term in `E_gamma`, `E_chi`,
  `E_nu`, or `E_W`'s equations, and is absent from the Cosmic Loop
  diagram. As currently written, this term breaks the claimed
  `dE_tot/dt = 0` for `E_tot = E_gamma+E_chi+E_nu+E_C+E_W` -- energy
  leaves the compact reservoir through it with no accounted destination.
  Either `lambda_C` must be shown to be exactly zero, or an explicit
  `+lambda_C*U_C` source term needs to be added to one of the other four
  channels' balance equations (most likely E_chi, if it represents
  leakage back into the general compression field outside the
  Mirror-Gate/White-Energy release channel) before the Bronze
  Requirement's "total energy must remain constant" claim can be tested
  at all -- right now the system as written cannot pass that test even
  in principle, independent of simulation.

## Downstream use: AGN ejection-selectivity (Book 5 Ch4)

Book 5 Ch4 now uses this node's existing `h` hysteresis (on above
`U_on`, off below `U_off`) as its candidate answer for why only some
active galactic nuclei produce strong ejections: an object whose
`P_cap`/`P_nu` never pushes `U_C` above `U_on` simply never switches on,
without needing a different mechanism from one that does. This is a new
claim resting on this node's existing math, not a change to it -- but it
means the unaccounted-sink problem above must be fixed before that
downstream claim can be trusted numerically, since it changes `U_C`'s
own trajectory.

## Bronze Requirement

Run a closed-domain simulation with photon transport loss, field storage, Return-Mode transport, compact capture, and threshold White Energy release. Total energy must remain constant within numerical tolerance while the system reaches a stationary circulation rather than secular growth or decay.

Prerequisite, per the Yellow Audit's unaccounted-sink item: give `lambda_C*U_C` an explicit destination (or set it to zero) before running this simulation. As the equations are currently written, no simulation of this system can pass the "total energy remains constant" test, since the ODE itself does not conserve `E_tot` -- this is a modeling gap to fix first, not something a longer or more careful simulation run would reveal.
