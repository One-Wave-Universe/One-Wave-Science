---
node_id: "G-721b1"
canonical_name: "Sturmian Mechanical Word Generator"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Binary Sequence Generator / Mechanical Word"
claim_gate_detail: "BRONZE (Sturmian mathematics) / YELLOW (Rabbit-Hop scheduling use)"
metadata_standard: "I-06"
---

# Node G-721b1: Sturmian Mechanical Word Generator

## Parent
G-721b Sturmian Binary Branch Grammar.

## Purpose
Own only the binary mechanical-word generator used by G-721b. It does not own Rabbit-Hop coordinates, mirror sign, live choice, or Android movement.

For irrational slope `alpha` and intercept `rho`:

[
b_t=lfloor(t+1)alpha+hofloor-lfloor talpha+hofloorin{0,1}.
]

The output is an ordered binary trace.

## Inputs
- irrational `alpha`;
- intercept `rho`;
- sample length `N`;
- declared token convention.

## Output
[
(b_0,b_1,ldots,b_{N-1}).
]

## Boundary
This node generates tokens only. It does not choose Rabbit-Hop anchor generation `j_t`, does not choose sign, and does not authorize movement.

## Falsifiers
Reject a claimed run if generated tokens do not match the declared mechanical-word formula or if the implementation silently changes `alpha`, `rho`, token convention, or sample window.
