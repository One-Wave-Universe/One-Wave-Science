---
node_id: "G-765"
canonical_name: "Route Families and Operation Order"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Reversible Arithmetic / Route Grammar"
claim_gate_detail: "Arithmetic identities are executable; interpretation is domain-specific."
metadata_standard: "I-06"
---

# Node G-765: Route Families and Operation Order

## Purpose
Own the three canonical route families used by G-764 packets.

```text
ORIGINAL           TOP = 2N
DOUBLE_THEN_SHIFT  TOP = 2N + K
SHIFT_THEN_DOUBLE  TOP = 2(N + K)
```

`K` is any integer on the generalized families. ORIGINAL requires `K=0`.

Operation order is part of route identity.

Two different routes may meet:

[
2N+2m=2(N+m).
]

Numerical equality does not mean route equality.

## Failure
Dropping parentheses, rejecting legal signed K, or collapsing equal destinations into one route fails this node.
