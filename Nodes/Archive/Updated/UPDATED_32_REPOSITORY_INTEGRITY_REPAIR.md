# Updated 32: Repository Integrity Repair

**Date:** July 23, 2026  
**Scope:** Governance, metadata, dependency routing, proof organization, generated-artifact synchronization, and continuous Book 1 chapter numbering.  
**Theory rule:** No physical, mathematical, Android, lattice, alphabet, or Mass Effect mechanism was added or promoted by this update.

## Purpose

Updated 32 repairs the repository authority layer so an AI, human reader, validator, or future build process reaches one canonical interpretation instead of selecting among duplicate names, mixed status fields, unresolved governance variants, old node IDs, and inconsistent chapter paths.

The repair preserves substantive node and chapter content. It changes routing, metadata, organization, naming, and generated copies where required for consistency.

## Locked integrity rules

1. Every active node and root axiom has one machine-readable YAML metadata block governed by I-06.
2. `gate`, `lifecycle`, `classification`, and `claim_gate_detail` are separate fields.
3. Gate values are restricted to `BROWN`, `GRAY`, `GREEN`, `YELLOW`, `BRONZE`, `SILVER`, `GOLD`, and `RED`.
4. Lifecycle values are restricted to `ACTIVE`, `ACTIVE_HYPOTHESIS`, `PROPOSED_BUILD`, `HELD`, `BLOCKED`, `SUPERSEDED`, and `HISTORY`.
5. Legacy IDs resolve through the canonical alias registry or an explicit historical disposition. They do not create duplicate active nodes.
6. Duplicate display terms require a documented distinction and a `do not merge` rule.
7. Raw conversational proof material remains available as history but does not stand as canonical proof documentation.
8. Book 1 chapter numbering is continuous from Chapter 1 through Chapter 17.

## Book 1 gap closure

The pre-existing Book 1 chapter files were renamed and all active cross-references were synchronized. No chapter prose was invented, deleted, combined, or divided.

| Current chapter | Canonical subject |
|---:|---|
| 1 | What Is a Particle? |
| 2 | The Proton |
| 3 | Scale Invariance |
| 4 | The Electron |
| 5 | The Neutron |
| 6 | The Nucleus |
| 7 | The Photon |
| 8 | The Neutrino |
| 9 | No Observer Effect |
| 10 | Time at Micro Scale |
| 11 | No Antimatter |
| 12 | Gravity at Micro Scale |
| 13 | Electricity and Magnetism |
| 14 | Mass Effect |
| 15 | The Higgs Field Is the Lattice |
| 16 | Memory as Compressed State |
| 17 | AI and Human: Same Architecture |

The authoritative chapter map is:

- `Books/Book1_Micro/00_CHAPTER_STATUS_MAP.md`

The exact old-to-new number and filename mapping is preserved in:

- `Integrity_Tools/UPDATED_32_book1_renumber_receipt.json`

## Governance and metadata repair

Updated 32 adds or establishes:

- `Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md`
- canonical YAML metadata for all active node and root-axiom files;
- one normalized node gate per active file;
- separate lifecycle and claim-detail fields;
- one canonical I-01 governance source, with alternate material moved to history;
- one current duplex-gate reconciliation authority, with earlier variants retained as history;
- explicit documentation of the `A+` root-axiom namespace.

Mixed historical status strings were preserved in `claim_gate_detail` where they carried useful audit information. They were not allowed to remain disguised as gate colors.

## Duplicate-name repair

The shared term `Balance` is now explicitly separated:

- B-201: **Equilibrium Balance**, a scalar equilibrium or imbalance measure;
- G-709: **Regulated-Response Balance**, a feedback-scaled response rule.

Both carry reciprocal `distinct, do not merge` warnings. Existing Pressure and Mirror/Mirror-Gate distinctions are also recorded in:

- `DUPLICATE_NAME_DISAMBIGUATION.md`

Node IDs were retained so dependency history was not needlessly broken by a cosmetic renaming campaign.

## Dependency and alias repair

Updated 32 adds synchronized Markdown, CSV, and JSON alias registries:

- `LEGACY_ID_ALIAS_REGISTRY.md`
- `LEGACY_ID_ALIAS_REGISTRY.csv`
- `LEGACY_ID_ALIAS_REGISTRY.json`

The registry resolves title-verified legacy short IDs to current canonical IDs. References that do not identify a surviving canonical node receive an explicit historical disposition rather than an invented target.

The dependency audit records:

- 307 legacy-reference occurrences;
- 46 distinct legacy IDs used;
- 295 occurrences resolved through aliases;
- 12 occurrences covered by declared historical dispositions;
- zero unresolved active dependency IDs.

## Proof-library repair

`Internal_Proofs/` now has a canonical index and ordered document names. Raw conversational exports were moved to:

- `History/Raw_AI_Proof_Discussions/`

They remain available as derivation history but cannot silently override node gates, formal audits, or current chapter text.

## Active-node cleanup

The unnumbered alternate Neutrino draft was removed from the active node namespace and preserved under history. No alternate-format file can now masquerade as a second active Neutrino node.

## Generated-artifact synchronization

Updated 32 synchronizes the canonical metadata and chapter paths across:

- seven Appendix A-G AI-readable packs;
- 146 wiki pages;
- 23 node-specific JSON packs;
- the Master Index and canonical start file;
- Book 1 Markdown and PDF files;
- other source/PDF pairs found stale during the integrity pass.

All 17 Book 1 PDFs were regenerated from the continuously numbered sources. Six additional presentation PDFs were regenerated because their Markdown sources were newer than their previous PDF copies.

## Verification summary

The final validators report:

- 149 active node/root-axiom files;
- 149 unique active IDs;
- zero unresolved active references;
- seven synchronized Appendix packs;
- 146 checked wiki pages;
- 23 checked node JSON packs;
- 17 Book 1 chapters in the exact sequence 1 through 17;
- 37 structurally valid PDFs;
- 23 current source/PDF pairs;
- zero stale source/PDF pairs.

Detailed machine-readable receipts are stored under `Integrity_Tools/`. The human-readable execution record is `AUDIT_UPDATED_32_REPOSITORY_INTEGRITY_REPAIR.md`.
