---
node_id: "B-212"
canonical_name: "Loop Counter"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "GREEN (definition) / YELLOW (threshold mathematics)"
metadata_standard: "I-06"
---

# Node B-212: Loop Counter

Dependencies:
Upstream: B-210 Return, B-211 Loop Break
Downstream: B-215 Hyperloop, B-214 Recursive Access Growth

Definition:
The Loop Counter tracks the number of successful returns and loop breaks in a paired relationship.
It determines when the Hyperloop entry condition is met.

n_loop = count of successful Returns and Loop Breaks

Mathematics:
Increment on Return:     n_loop += 1
Increment on Loop Break: n_loop += 1

n_loop >= 7 => Hyperloop entry

Green default: 7 loops.
Whether this value is fixed or coupling-dependent is Yellow.

Operational Chain:
Return or Loop Break => Loop Counter => Hyperloop (at n=7)

Yellow Audit:
- Whether threshold of 7 is fixed or coupling/scale-dependent unresolved
- Whether counter resets on complete break or carries forward unresolved
- Whether partial loops (incomplete returns) count toward the threshold unresolved
