---
node_id: "G-777"
canonical_name: "Repository Content Normalization and Authority"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Repository Governance / Content Placement"
claim_gate_detail: "YELLOW: canonical project structure or validation contract; empirical/domain-specific claims remain subject to stated tests and evidence boundaries."
metadata_standard: "I-06"
---

# G-777 — Repository Content Normalization and Authority

## Rule

Substantive One-Wave knowledge belongs in exactly one authoritative place:

- **Nodes/** for canonical, technical, mathematical, physical, architectural, governance, validation, hardware, and archival technical records.
- **Books/** for explanatory chapters, guides, narratives, learning material, presentation material, and human-readable synthesis.
- **Project-local documentation** may remain beside executable code only when it directly documents that executable project and is not a second canonical copy.
- **Root** is reserved for repository/tool entrypoints such as README, AGENTS, model-specific instruction files, changelog, and launch HTML.

## No satellite copies

Do not create parallel authority trees such as:
- Wiki copies of Nodes;
- AI-readable copies of Nodes;
- loose top-level UPDATED/AUDIT/ARCHITECTURE files;
- duplicate lock files beside their canonical Nodes;
- a second book folder for material already integrated into Books/.

Generated output may exist only when required by a runnable project, test, export, or build process. It must not become a second source of truth.

## Historical material

Historical technical records belong under:

`Nodes/Archive/`

They may preserve old wording, but they are not current canon unless explicitly promoted by a current node.

## Migration rule

When normalizing an old satellite file:

1. choose its one authoritative Node or Book destination;
2. move the content rather than copy it;
3. remove the original path in the same migration;
4. delete pure generated mirrors when the canonical source already exists;
5. update references where necessary;
6. do not silently preserve a second authority copy.

## Algorythm-Zer0 special lock

Exactly five Algorythm-Zer0 canon files are retained:
- G-772 X Control
- G-773 Y Structure / Rotation
- G-774 Z Depth
- G-775 T Time / Change + four-branch lock
- G-776 shared rules / thresholds / variables / transformations

Older Algorythm-Zer0 files are superseded and must not be recreated.

## Rabbit-Hop normalization

G-721 is a legacy index only. Canonical ownership is decomposed into G-764 through G-771, with sequence-family nodes consuming those normal nodes.

## Failure condition

Repository drift exists when the same substantive rule is maintained in two places with independent wording or authority.
