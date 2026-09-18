---
node_id: "G-766"
canonical_name: "Opposite-Parity Wrapper and Shared Boundary"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Parity Connector / Nested Address Boundary"
claim_gate_detail: "Exact integer relation; cross-domain meaning remains adapter-specific."
metadata_standard: "I-06"
---

# Node G-766: Opposite-Parity Wrapper and Shared Boundary

## Purpose
Own the mandatory connector around a selected TOP.

For any TOP `X`:

```text
X-1 | X | X+1
```

Every complete route chooses one of the two wrapper sides:

[
sin{-1,+1}.
]

Wrapper parity must oppose TOP parity.

Adjacent original nests can share a wrapper:

[
2N+1=2(N+1)-1.
]

A shared boundary is a connection address, not permission to discard either source receipt.

## Separation
TOP offset `K` and wrapper `s` are different operations and remain different fields.
