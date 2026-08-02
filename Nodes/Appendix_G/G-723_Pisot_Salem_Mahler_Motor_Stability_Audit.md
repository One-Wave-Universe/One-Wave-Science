---
node_id: "G-723"
canonical_name: "Pisot-Salem-Mahler Motor Stability Audit"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Spectral Audit / Expansion-Contraction-Rhythm Measurement"
claim_gate_detail: "BRONZE (external algebraic definitions) / YELLOW (motor-controller relevance)"
metadata_standard: "I-06"
---

# Node G-723: Pisot-Salem-Mahler Motor Stability Audit

**Dependencies**  
Upstream: G-722 Android Motor Memory Architecture, G-706 Validation  
Lateral: G-721d, G-721e  
Downstream: integer/substitution motor-controller experiments, G-723a advanced Mahler methods

## Purpose

This node audits structured recurrence matrices and substitution systems. It does not generate foundational movement.

## Pisot Side

A Pisot number `beta` is a real algebraic integer greater than one whose other algebraic conjugates have magnitude below one.

A Pisot-like controller offers the candidate pattern

\[
\boxed{\text{dominant expression}+\text{contracting internal correction}}.
\]

The plastic number is the smallest Pisot number and may be tested through G-721e. The golden ratio is another Pisot example.

## Salem Side

A Salem number `tau` is a real algebraic integer greater than one whose conjugates include `tau^-1`, with all remaining conjugates on the unit circle.

A Salem-like spectrum offers the candidate pattern

\[
\boxed{\text{expression}+\text{reciprocal return}+\text{persistent bounded phase modes}}.
\]

This is potentially relevant to gait, counter-rotation, alternating pressure, and balance rhythms. It is an analogy and design target until an actual controller is built.

## Mahler Measure

For

\[
P(x)=a\prod_j(x-\lambda_j),
\]

the multiplicative Mahler measure is

\[
\boxed{M(P)=|a|\prod_j\max(1,|\lambda_j|)}.
\]

The logarithmic measure is `m(P)=log M(P)`.

Mahler measure reports total algebraic expansion outside the unit circle. It does not report route identity, phase organization, transient non-normal growth, nonlinear safety, or physical balance.

## Required Spectral Report

Every qualifying integer or substitution recurrence should report:

- characteristic and minimal polynomial where available;
- complete eigenvalue list;
- spectral radius;
- Mahler measure and log measure;
- counts of contracting, near-unit, unit-circle, and expanding modes;
- reciprocal-pairing error;
- arguments of complex modes;
- finite-time Lyapunov estimates for the actual nonlinear controller;
- transient amplification;
- physical error and safety violations.

## Lehmer Boundary

Lehmer's conjecture asks whether non-cyclotomic integer polynomials have a universal Mahler-measure gap above one. The conjecture is open. Lehmer's number is the smallest known example above one, not a proven android threshold.

It may be used as a comparison case in an algebraic-controller benchmark. It may not be promoted to a universal motor-safety constant.

## Pisot-Salem Combination Test

A practical controller need not have an exact Pisot or Salem minimal polynomial. Test the broader spectral target:

\[
\lambda_{\mathrm{correction}}<0\quad\text{in Lyapunov rate},
\]

\[
\lambda_{\mathrm{rhythm}}\approx0,
\]

\[
\lambda_{\mathrm{drive}}>0\quad\text{only while commanded and bounded}.
\]

The controller should settle errors, preserve required rhythms, and terminate or hold directed expression without runaway growth.

## Falsifiers

Reject a spectral interpretation when it depends on arbitrary floating-point rounding into a prestigious algebraic family, when the full spectrum contradicts the claimed behavior, or when favorable eigenvalues fail to predict the nonlinear physical simulation.

## Reference Receipts

![Reference root moduli for Fibonacci, plastic, Tribonacci, and Lehmer polynomials.](../Nodes/G-723_Spectral_Validation/root_moduli.png)

`Nodes/G-723_Spectral_Validation/` stores numerical root, spectral-radius, and Mahler-measure receipts. They are algebraic regression examples, not android safety limits.
