---
node_id: "G-721d"
canonical_name: "Arnoux-Rauzy Strict Multi-Route Validation"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Strict Episturmian Validator / Multi-Route Complexity Audit"
claim_gate_detail: "BRONZE (external word mathematics) / YELLOW (android movement validation)"
metadata_standard: "I-06"
---

# Node G-721d: Arnoux-Rauzy Strict Multi-Route Validation

**Dependencies**  
Upstream: G-721c Episturmian Grammar, G-706 Validation  
Lateral: D-411 Mirrored Axis-Pair Counts  
Downstream: ternary triangular-route tests, higher-alphabet route experiments

## Definition

A `k`-letter Arnoux-Rauzy word is a strict episturmian word with exactly one left-special and one right-special factor of each length, each extending through the full alphabet under the standard definition.

Its factor complexity is

\[
\boxed{p(m)=(k-1)m+1}.
\]

For `k=2`, this reduces to the Sturmian value `m+1`. For `k=3`,

\[
\boxed{p(m)=2m+1}.
\]

## Ternary Route Test

The triangular 2D lattice has three undirected route axes. A ternary Arnoux-Rauzy scheduler can label those route families while `-1(0)+1` supplies signed direction or hold.

Two different `2n+1` forms must remain separate:

- `p(n)=2n+1` counts route-language factors of length `n` in the ternary strict word;
- the alphabet packet value `2n+1` is the odd recursive rail for letter index `n`.

Shared form is a comparison target, not variable identity.

## Directive Condition

For a strict standard construction, every alphabet symbol must recur infinitely often in the directive sequence. Finite simulation reports approximate this by recording route coverage and maximum recurrence gap over a declared window.

## Required Validation

1. factor complexity `p(m)=(k-1)m+1` over the finite-test range;
2. unique left-special and right-special factors at each tested length;
3. full-alphabet extension of the special factors;
4. recurrence of every route symbol;
5. reversal-language check inherited from episturmian structure;
6. separate balance measurement;
7. separate frequency and unique-ergodicity measurement.

## Guardrails

Arnoux-Rauzy structure does not guarantee a universal strong balance constant. Some examples are well balanced; others can be highly imbalanced. Balance is measured, not assumed.

A torus rotation or Rauzy-fractal realization is available for important substitutive examples such as Tribonacci, but is not an automatic property of every Arnoux-Rauzy directive system.

## Android Use

This validator asks whether a multi-route subconscious scheduler remains recurrent and minimally organized without falling into a short periodic loop. It does not prove that the resulting movement is safe, graceful, or physically efficient.

## Falsifiers

Any failure of the exact complexity or special-factor conditions rejects an exact Arnoux-Rauzy label. A controller may still be useful under another classification; useful behavior does not grant a mathematical family name by diplomatic immunity.

## Reference Receipts

The directory `Nodes/G-721_Sequence_Validation/` contains finite regression tests for Fibonacci, a generic Sturmian mechanical word, the Tribonacci Arnoux-Rauzy reference word, and the plastic/Padovan substitution.

![Finite route-word factor complexity receipts.](../Nodes/G-721_Sequence_Validation/factor_complexity.png)

The finite Tribonacci reference matches `p(n)=2n+1` through the declared test range. This validates the code and reference construction, not android movement.
