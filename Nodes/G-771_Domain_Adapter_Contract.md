---
node_id: "G-771"
canonical_name: "Reversible Domain Adapter Contract"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Cross-Domain Adapter Interface"
claim_gate_detail: "Software contract is testable; cross-domain physical identity is not claimed."
metadata_standard: "I-06"
---

# Node G-771: Reversible Domain Adapter Contract

## Upstream
G-764 through G-770.

## Purpose
Define how any new domain joins the shared address system without duplicating arithmetic.

A domain adapter must:
1. map its label/state to a declared source identity;
2. call the shared G-764/G-765 core;
3. retain the full route receipt;
4. preserve mirror, inversion, wrapper, and traversal fields separately;
5. provide exact reverse reconstruction where the mapping is intended to be reversible;
6. add round-trip tests;
7. state what domain information is lost, if any.

## Existing adapters
- alphabet: G-769 / `rabbit_hop_alphabet.py`;
- music: E-510 / E-514 plus `rabbit_hop_music.py`;
- guitar neck: `rabbit_hop_neck.py`;
- bounded scale rail: G-770.

A shared numeric address does not prove that two domain labels are equivalent. It proves only that they were translated into the same declared address under the retained receipt.
