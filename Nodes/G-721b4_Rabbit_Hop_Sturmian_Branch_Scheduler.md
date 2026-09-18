---
node_id: "G-721b4"
canonical_name: "Rabbit-Hop Sturmian Branch Scheduler"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Rabbit-Hop Route Scheduler / Two-Branch Adapter"
claim_gate_detail: "Sturmian sequence mathematics is external; Rabbit-Hop scheduling relevance remains testable"
metadata_standard: "I-06"
---

# Node G-721b4: Rabbit-Hop Sturmian Branch Scheduler

## Parent
G-721b Sturmian Binary Branch Grammar.

## Upstream
G-721 Rabbit-Hop core; G-721b1 token generator; G-721b2 validator; G-721b3 operation separation.

## Purpose
Map an already-generated Sturmian token onto one of the two Rabbit-Hop wrapper sides around a separately declared anchor.

For alphabet/source location `n_t`, declared anchor generation `j_t in {0,1}`, and Sturmian token `b_t`:

[
e_t=2(n_t+j_t)
]

[
o_t=e_t+(2b_t-1).
]

Thus:
- `b_t=0` selects the lower odd neighbor;
- `b_t=1` selects the upper odd neighbor.

## Critical separation
The Sturmian token selects a branch around a declared anchor. It does not choose:
- source identity;
- anchor generation `j_t`;
- mirror polarity;
- traversal direction;
- live `-1(0)+1` choice;
- final motor/joint action.

## Scheduling use
A validated Sturmian trace may supply nonperiodic balanced scheduling between two candidate branches. Compare its behavior against periodic, random, and learned schedulers.

## Required receipt
Each scheduled hop must retain:
- source `n_t`;
- `j_t`;
- `b_t`;
- `e_t`;
- `o_t`;
- sign/polarity;
- traversal direction;
- parent route receipt.

## Falsifier
Reject the scheduler if reconstruction cannot recover the declared source, anchor, and token exactly, or if the scheduling trace only works after post-hoc editing.
