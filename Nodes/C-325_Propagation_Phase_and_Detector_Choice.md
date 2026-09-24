---
node_id: "C-325"
canonical_name: "Propagation Phase and Detector Choice"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Measurement / Wave Interaction"
claim_gate_detail: "GREEN standard phase mathematics / YELLOW distinct One-Wave interpretation"
metadata_standard: "I-06"
---

# C-325 — Propagation Phase and Detector Choice

## Dependencies

Upstream: A-110a Wave Equation Derivation, F-605 Interference, C-324 No Entanglement Detector Map.

## Core phase law

For

[
psi(x,t)=Acos(kx-omega t+phi_0),
]

the arrival phase is

[
phi_{m hit}=kx-omega t+phi_0.
]

A path-length change gives

[
Deltaphi=rac{2pi}{lambda}Delta L.
]

Thus frequency, path length, propagation speed, and time determine the phase available at the interaction.

## Detector boundary

Ordinary square-law detectors respond approximately to intensity:

[
Ipropto |E|^2.
]

They do not directly distinguish positive and negative electric-field sign.

Phase/sign tests therefore require a coherent reference such as interferometric, homodyne, or heterodyne detection.

## One-Wave hypothesis

"Choice" is assigned to the local interaction/readout event:

```text
propagating oscillatory state
-> accumulated Path phase
-> local detector/reference coupling
-> registered outcome
```

This is a physical interpretation only if it can be distinguished quantitatively from standard quantum-optical predictions.

## Point / Path / Field mapping

- Point = local oscillator state/phase.
- Path = accumulated propagation phase.
- Field = local interaction/reference environment.

## Failure condition

If every observable is mathematically identical to standard interference/quantum optics, retain this node as an interpretation/recovery map rather than a new physical law.

## Nobel-readiness link

See `NOBEL_READINESS/CHALLENGE_07_PHASE_CHOICE_DETECTION.md`.
