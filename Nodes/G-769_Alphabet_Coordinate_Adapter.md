---
node_id: "G-769"
canonical_name: "Alphabet Coordinate Adapter"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Symbolic Domain Adapter / Alphabet"
claim_gate_detail: "A-Z mapping and executable round-trip exist; semantic use remains application-specific."
metadata_standard: "I-06"
---

# Node G-769: Alphabet Coordinate Adapter

## Upstream
G-764 through G-768.

## Purpose
Own only the alphabet label mapping into the shared reversible address grammar.

Forward:

```text
A=1, B=2, ... Z=26
```

Inverted:

```text
Z=1, Y=2, ... A=26
```

[
N_{inv}=27-N.
]

Executable adapter:
`One_Wave_Bench/brain/rabbit_hop_alphabet.py`.

Whole-run display layouts may use:

```text
A-Z (0) Z-A
Z-A (0) A-Z
```

The alphabet adapter does not own the shared route arithmetic and does not imply that a letter equals any other domain label occupying the same numeric address.
