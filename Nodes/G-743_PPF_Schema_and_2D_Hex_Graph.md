---
artifact_id: "G-743"
parent_node_id: "G-743"
title: "PPF Schema and 2D Hex Graph Trail"
namespace: "NODE_ARTIFACT"
lifecycle: "ACTIVE"
metadata_standard: "I-06"
---

# G-743 — PPF Schema and 2D Hex Graph Trail

**Brick:** Yellow
**Closes (partial):** G-728 C1 schema, G-728 D1 graph
**Does not close:** C2-C10 rotations/ablations, D2-D8 transforms, plots against a Gray control

## What was added

1. `One_Wave_Bench/logic_core/ppf_schema.py` implements `X_s={P_s, gamma_s, F_s; children}` with units and frames `{ground, local, path}`.
2. `One_Wave_Bench/logic_core/hex_lattice_graph.py` builds D-408 disk, seven-cell, 6 directed neighbors, 3 axis pairs, incidence, Laplacian for `3 > 1(0)1 < 6`.
3. Tests: `test_ppf_schema.py` (5), `test_hex_lattice_graph.py` (7).

## Math receipts

- Neighbor distance on unit lattice is 1.
- Seven-cell Laplacian row-sums are 0.
- Smallest Laplacian eigenvalue is 0; next is positive.
- Seven-cell edge count is 12.

## Explicit non-claims

Schema nesting is not rotation physics. A 2D graph is not 3D or 4D. Matching 3/6 counts is not a Mirror-Gate derivation. No hardware identity is asserted.

## Next

C2 Point rotation; C3 Path circulation; D2 FCC/HCP graphs; D4 spectra.
