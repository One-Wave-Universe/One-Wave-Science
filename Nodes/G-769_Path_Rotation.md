---
node_id: "G-769"
canonical_name: "C3 Path Rotation"
namespace: "NODE"
gate: "BROWN"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Legacy G-Series / Canonicalized Node"
claim_gate_detail: "split-gate: kinematic turning GREEN; not a planetary orbit"
metadata_standard: "I-06"
---

# G-769 — C3 Path rotation

The path is the ride. It is not the point.

A path is a sequence of centers. At each interior center the turn is the angle between the incoming edge and the outgoing edge. A closed regular hexagon turns \(2\pi\). A straight ride turns \(0\).

The receipt carries turning, corner count, mean edge, and curvature. It does not carry \(L\). The magnetic gradient is not applied. The gravity coefficient on the point is \(0\).

Code: `One_Wave_Bench/logic_core/path_rotation.py`.

Point spin stays in G-749. An open magnetic gradient leaves \(L\) unchanged. A closed one resists it. Passing a gravity vector into that rate does not change the rate.

## Not claimed

This is not an ephemeris. This is not a wake law. The assimilation boundary is still not derived.
