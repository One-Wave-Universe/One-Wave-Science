---
node_id: "B-224"
canonical_name: "Two Choices — Everything or Nothing"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "Implementation-canonical engagement choice; physical realization remains open"
metadata_standard: "I-06"
---

# Node B-224: Two Choices — Everything or Nothing

## Definition

The first/binary choice is whether the local operation participates at all:

```text
EVERYTHING = engage / assert / open the operation
NOTHING    = do not engage / high-Z / non-action
```

This choice is distinct from the ternary directional result in `B-223`.

## Two-Level Decision Model

```text
DC choice
├── NOTHING
│   └── no active operation; preserve/hold the local relation
└── EVERYTHING
    └── AC/differential resolution
        ├── LEFT  (-1)
        ├── STAY   (0)
        └── RIGHT (+1)
```

Therefore:

```text
DC = whether to participate
AC differential = how/direction if participating
```

## Zero Is Not a Third DC Choice

`0` belongs to the ternary differential layer. It is a no-assertion/hold outcome around the shared reference. It must not be implemented by inventing a third powered DC direction.

In a physical driver, `NOTHING` may be represented by a high-impedance state after transients decay. The exact circuitry is implementation-specific.

## Correction of Earlier Wording

Earlier repository text treated **Compression / Expression** as the two fundamental choices. That mixed the engagement layer with the action layer. Compression/expression-like behavior is handled by Actions/representations, especially Inward and Outward, while the binary engagement choice is Everything/Nothing.

## Consequence Loop

```text
choice
 -> action / non-action
 -> consequence
 -> memory/reference update
 -> next field of choices
```

Choice is meaningful only in relation to consequence and the next reference state.

## Yellow Audit

- Everything/Nothing is canonical for the implementation architecture.
- Exact electrical implementation of `NOTHING` requires validation for leakage, inductive decay, and passive coupling.
- The relationship to physical systems outside the compute architecture remains a representation claim and must be tested separately.
