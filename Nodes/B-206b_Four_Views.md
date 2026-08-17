---
node_id: "B-206b"
canonical_name: "Four Views — Direction, Phase, Strength, Reference"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "Implementation-canonical; physical instantiations remain scale-specific"
metadata_standard: "I-06"
---

# Node B-206b: Four Views — Direction, Phase, Strength, Reference

## Correction

Earlier repository text incorrectly called **Inward, Outward, Across, Over** the Four Views. Those are Actions, not Views. The canonical separation is now:

- **Views = what the system reads about a state.**
- **Actions = what the system does with a state.**

See `B-206c_Four_Actions.md`.

## The Four Views

1. **Direction** — Which way is the resolved relation leaning or moving relative to the active reference. At the ternary routing layer this can be represented as `-1 / 0 / +1` = left / stay / right.
2. **Phase** — Where the oscillatory relation is in its cycle, including handedness/crossover orientation where the implementation tracks it.
3. **Strength** — How large or intense the relation is relative to its active reference. Five-state or finer threshold bands may be used as representations of this quantity, but they are not part of the invariant kernel.
4. **Reference** — The local baseline `(0)` against which Direction, Phase, and Strength are interpreted. Reference is carried at every recursive level; no state is interpreted as an absolute value without an active reference.

## Measurement Packet

A minimal view packet can be written as:

```text
ViewState {
    direction
    phase
    strength
    reference
}
```

This packet is descriptive. It does not itself command a transformation.

## Domain Independence

The same Four Views can describe a circuit, a wave packet, a cell, a lattice relation, a cognitive state, or another scale-specific system. Domain labels are wrappers above the invariant engine.

The kernel must not encode domain-specific meanings such as temperature, matter phase, planets, musical intervals, or biological labels into these four slots.

## Relationship to the Actions

```text
VIEW                         ACTION
what is read                 what is done

Direction                    Inward
Phase                        Outward
Strength                     Across
Reference                    Over
```

The columns are parallel four-part layers, not one-to-one semantic aliases. An Action may operate on all four Views simultaneously.

## Anti-Drift Rule

If replacing or deleting a domain representation changes the definitions of Direction, Phase, Strength, or Reference, that representation has leaked into the core architecture.

## Operational Chain

```text
state
 -> read Direction / Phase / Strength / Reference
 -> choose or resolve an Action
 -> produce consequence
 -> consequence becomes input/reference for the next relation
```

## Yellow Audit

- The four-slot measurement architecture is canonical for implementation.
- Exact physical sensors and mathematical coordinates remain implementation-specific.
- The relationship between these Views and any dimensional 1D/2D/3D/4D representation must be derived separately; it is not assumed here.
