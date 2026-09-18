---
node_id: "G-767"
canonical_name: "Route Provenance and Exact Reconstruction"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Inverse Mapping / Reconstruction Receipt"
claim_gate_detail: "Exact inverse arithmetic is executable."
metadata_standard: "I-06"
---

# Node G-767: Route Provenance and Exact Reconstruction

## Purpose
Own the rule that a compressed/generated address must reconstruct its source when the full receipt is retained.

Double then shift:

[
X=2N+K+s
]

[
N=(X-K-s)/2.
]

Shift then double:

[
X=2(N+K)+s
]

[
N=(X-s)/2-K.
]

The wrapper is removed first, then the recorded operation order is reversed.

## Rule
No accepted compression or translation may discard enough information to make exact source reconstruction ambiguous.

## Failure
A route that reaches the right number but cannot recover its source and route-of-origin fails this node.
