---
node_id: "G-721b"
canonical_name: "Sturmian Binary Branch Grammar"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Binary Route Grammar / Branch-Trace Validator"
claim_gate_detail: "BRONZE (external word mathematics) / YELLOW (rabbit-route and android relevance)"
metadata_standard: "I-06"
---

# Node G-721b: Sturmian Binary Branch Grammar

**Dependencies**  
Upstream: G-721 Mirrored Alphabet Packet, G-721a Fibonacci Reference Validator  
Lateral: G-706 Validation, G-720 No Control But Self-Control  
Downstream: G-721c, G-721d, Android procedural route tests

## Purpose

G-721a provides one fixed Fibonacci-word regression path. This node generalizes the ordered two-branch grammar to the Sturmian family.

For irrational slope `alpha` and intercept `rho`, a lower mechanical word is

\[
\boxed{b_t=\lfloor(t+1)\alpha+\rho\rfloor-\lfloor t\alpha+\rho\rfloor\in\{0,1\}}.
\]

The selected recursive rail is

\[
\boxed{r_t=2n_t+b_t}.
\]

Thus the packet provides the available rails `2n` and `2n+1`; the Sturmian word supplies their ordered branch grammar.

## Role Separation

- `n` identifies the alphabet location;
- `2n` and `2n+1` are available recursive rails;
- `b_t` selects one branch for a declared route grammar;
- mirror sign identifies coordinate side;
- live `-1(0)+1` choice still decides movement or hold;
- binary oversight may audit or block but does not generate choice.

## Validation Properties

An infinite binary word is Sturmian when its factor complexity is

\[
\boxed{p(m)=m+1}
\]

for every factor length `m`. Equivalent characterizations include aperiodicity plus balance, and coding by irrational rotations under appropriate conventions.

For finite receipts, test:

1. packet legality `b_t in {0,1}`;
2. observed factor complexity up to a declared maximum length;
3. balance: equal-length factors differ in `1` count by at most one;
4. recurrence gaps;
5. period search;
6. empirical symbol frequency against the declared slope convention.

Finite samples can undercount factors at large `m`; reports must state sample length and tested range.

## Fibonacci Special Case

The Fibonacci word is a Sturmian special case, but slope values depend on token convention. The common fixed point `0100101001...` has one-symbol frequency `1/phi^2`; its complement has the corresponding frequency `1/phi`.

Therefore `1/phi` and `1/phi^2` are complementary conventions, not the same number.

## Mirror and Reverse

Coordinate sign mirror, route reversal, and token complement are separate operations:

\[
(n,r)\mapsto(-n,-r),
\]

\[
(b_0,\ldots,b_{N-1})\mapsto(b_{N-1},\ldots,b_0),
\]

\[
b\mapsto1-b.
\]

No operation implies either of the other two without a declared bridge.

## Android Use

A Sturmian trace may schedule two competing movement branches with nonperiodic balanced recurrence. It does not directly command a joint. It supplies a candidate timing/route grammar whose effect must be compared with periodic, random, and learned controls.

## Falsifiers

Reject the exact Sturmian claim when factor complexity, balance, or aperiodicity fails in the valid finite-test range, or when alignment appears only after token deletion, reordering, selective windows, or post-hoc complementing.
