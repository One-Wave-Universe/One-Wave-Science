---
node_id: "G-764"
canonical_name: "Reversible Address Packet"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Address Grammar / Receipt Contract"
claim_gate_detail: "Executable arithmetic exists; domain mappings remain separate."
metadata_standard: "I-06"
---

# Node G-764: Reversible Address Packet

## Purpose
Own the label-independent packet shared by Rabbit-Hop domain adapters.

A complete packet is:

```text
source identity | TOP | wrapper
```

The source identity is retained separately from the generated address.

Canonical executable source:
`One_Wave_Bench/brain/rabbit_hop_core.py`.

## Receipt fields
- source rank;
- route family;
- signed K;
- wrapper side;
- polarity;
- traversal direction;
- TOP address;
- wrapper address.

Equal numeric addresses do not erase the receipt fields that produced them.

## Boundary
This node owns packet identity only. It does not own alphabet labels, musical notes, motor actions, memory semantics, or physical interpretation.
