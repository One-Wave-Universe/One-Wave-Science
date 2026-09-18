---
node_id: "G-721b2"
canonical_name: "Sturmian Validation Properties"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Sequence Validator / Complexity-Balance-Aperiodicity"
claim_gate_detail: "BRONZE (external Sturmian mathematics) / YELLOW (finite-receipt application)"
metadata_standard: "I-06"
---

# Node G-721b2: Sturmian Validation Properties

## Parent
G-721b Sturmian Binary Branch Grammar.

## Purpose
Own the tests that distinguish a valid Sturmian trace from a merely binary or visually similar sequence.

For an infinite Sturmian word:

[
p(m)=m+1
]

for every factor length `m`.

Equivalent characterizations include aperiodicity plus balance under standard conventions.

## Finite-receipt tests
1. token legality: `b_t in {0,1}`;
2. factor complexity for every declared tested length;
3. balance: equal-length factors differ in count of `1` by at most one;
4. recurrence-gap report;
5. explicit period search;
6. empirical token frequency against the declared slope convention.

## Finite-sample rule
Finite samples may undercount factors at large `m`. Every report must state sample length and tested factor range.

## Fibonacci special case
G-721a is one fixed Sturmian special case. Token-frequency conventions must remain explicit: the familiar Fibonacci fixed point and its complement use complementary symbol frequencies.

## Falsifiers
Reject the exact Sturmian claim when valid-range complexity, balance, or aperiodicity fails, or when a match appears only after deletion, reordering, selective windows, or post-hoc complementing.
