# Node I-06: Canonical Node Metadata and Alias Resolution

**Gate:** GREEN
**Lifecycle:** ACTIVE
**Classification:** Repository Governance

## Purpose

Every active node and root axiom must expose one machine-readable metadata block. Gate color, lifecycle state, and audit commentary are separate fields. A status sentence may not carry all three jobs.

## Canonical Metadata

Every file directly under `Nodes/` or `Root_Axioms/` begins with YAML front matter containing:

```yaml
node_id: "B-201"
canonical_name: "Equilibrium Balance"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "Previous mixed-status detail, or None"
metadata_standard: "I-06"
```

## Gate Rule

Allowed gate values are:

```text
BROWN, GRAY, GREEN, YELLOW, BRONZE, SILVER, GOLD, RED
```

For active A-G nodes, the ordinary ladder is Brown -> Green -> Yellow -> Bronze -> Silver -> Gold. Gray remains the Standard-Model comparison track for chapters. A node containing external Gray reference material still receives a node gate, with the comparison role stated separately. Red remains governed by I-02.

A composite node receives the most conservative gate among its load-bearing claims. More advanced subclaims remain in `claim_gate_detail`; they do not silently promote the whole node.

## Lifecycle Rule

Allowed lifecycle values are:

```text
ACTIVE, ACTIVE_HYPOTHESIS, PROPOSED_BUILD, HELD, BLOCKED, SUPERSEDED, HISTORY
```

Lifecycle does not change gate. `HELD` is not a color. `BLOCKED` is not a color. `CANDIDATE` is commentary or a promotion target, not a gate.

## Alias Rule

Legacy short IDs do not become duplicate nodes. They resolve through `LEGACY_ID_ALIAS_REGISTRY.json`. Each alias must identify a canonical target or an explicit historical disposition. Title verification outranks assumed numeric offset.

## Duplicate-Name Rule

Duplicate display terms are permitted only when every affected node carries an explicit `distinct, do not merge` note and `DUPLICATE_NAME_DISAMBIGUATION.md` records the distinction.

## Failure Conditions

The metadata layer fails if an active node lacks front matter, uses an unapproved gate/lifecycle, duplicates an active ID, or cites an ID that resolves to neither a canonical target nor a declared historical disposition.
