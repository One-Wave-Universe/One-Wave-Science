---
node_id: "G-770"
canonical_name: "Bounded Doubling and Division Rail"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Scale Boundary / Exact Integer Reconstruction"
claim_gate_detail: "Bounded 1..12 to 12..24 rail is executable; broader scale claims remain open."
metadata_standard: "I-06"
---

# Node G-770: Bounded Doubling and Division Rail

## Purpose
Own the separately bounded historical scale rail.

```text
outward source domain: 1..12
inward address domain: 12..24
```

Even addresses divide directly:

```text
12->6, 14->7, 16->8, 18->9, 20->10, 22->11, 24->12
```

Odd addresses are shared wrappers and return both neighboring sources:

```text
13->6,7
15->7,8
17->8,9
19->9,10
21->10,11
23->11,12
```

Executable adapter:
`One_Wave_Bench/brain/rabbit_hop_scale_rail.py`.

This node does not generalize the bounded rail into a universal physical division law.
