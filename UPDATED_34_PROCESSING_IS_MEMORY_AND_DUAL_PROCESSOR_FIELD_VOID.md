# UPDATED 34 — Processing Is Memory + Field/Void Processor Split

Status: ACTIVE architectural update

This update records the latest hardware/computing architecture decisions so future AI work does not drift back toward conventional CPU/RAM assumptions.

## 1. Processing Is Memory

The target machine is not organized as:

```text
RAM stores state
CPU fetches state
CPU computes
RAM writes result
```

The target machine is organized as:

```text
cell holds state
cell receives a differential relation
cell changes state
new state remains physically stored in the cell
```

Therefore the physical state-transition medium is simultaneously:

```text
MEMORY + LOGIC + STATE TRANSITION
```

A cluster is therefore distributed memory and distributed processing in the same physical structure.

For magnetic implementations, the design goal is a persistent local state that can be read and updated differentially without requiring a separate write-back RAM stage.

## 2. Required Hardware Proof

The decisive hardware test is not merely that a ternary output can be generated. The cell must demonstrate all three of the following:

1. hold a distinguishable physical state after the immediate drive is removed;
2. participate in a differential computation using that state;
3. leave the resulting state physically stored in the same local structure.

If those conditions fail, the architecture is only ternary logic with external memory. If they succeed, it is stateful compute-in-memory.

## 3. Field / Void Processor-Level Split

At larger scale, Field and Void are modeled as two processor-scale roles operating on the same relational state around a shared reference.

```text
                SHARED REFERENCE / STATE
                         (0)
                          |
             +------------+------------+
             |                         |
         FIELD SIDE                 VOID SIDE
         expressive                 compressive
             |                         |
             +------------+------------+
                          |
                    differential
                          |
                       routing
```

Field role:
- propose / express;
- expand candidate state;
- explore possible continuation;
- drive outward expression.

Void role:
- compress / compare;
- constrain against reference;
- reject, stabilize, or redirect;
- evaluate what survives.

The higher-level differential resolves the relation between the two sides.

## 4. Local Memory Belongs to the Processing Fabric

Field and Void should not be treated as conventional processors attached to giant external RAM banks.

Each side carries its working state in the persistent local cells/clusters it operates on:

```text
FIELD REGION
= local persistent state
+ local ternary compute
+ local routing

VOID REGION
= local persistent state
+ local ternary compute
+ local routing
```

A small supervisory controller may still have registers/cache or configuration memory, but it is not the main state store of the machine.

## 5. Binary Oversight Remains Sparse

The upper controller does not need to micromanage the local ternary state.

Target split:

```text
LOCAL NETWORK
-1 / 0 / +1
Direction / Phase / Strength / Reference

HIGHER OVERSIGHT
0 / 1
intervene / do not intervene
```

The local network resolves direction and state. The upper controller only decides whether to override, reroute, reset, or remain silent.

## 6. Recursive Scale Contract

Every scale must expose the same relational interface it consumes.

```text
INPUT RELATION
Direction
Phase
Strength
Reference
        |
local state transition
        |
OUTPUT RELATION
Direction
Phase
Strength
Reference
```

This must hold for:
- one triad;
- one 3-triad cluster;
- one cube;
- a connected cube block;
- larger recursive cube assemblies.

A higher-scale cluster should be able to substitute for a lower-scale element at the interface level without requiring a new logical grammar.

## 7. Cube Scaling

The physical growth path remains connected modular cubes:

```text
triad
-> 3-triad cluster
-> cube
-> face-connected cubes
-> 3x3x3 cube block
-> larger recursive cube lattice
```

Each cube should preserve six-direction spatial connectivity (+/-X, +/-Y, +/-Z), shared reference continuity, and the same relational packet/interface.

## 8. Canonical Reminder

Do not collapse these layers:

```text
DC CHOICE      = EVERYTHING / NOTHING
AC DIFFERENTIAL = LEFT / STAY / RIGHT = -1 / 0 / +1
4 VIEWS         = Direction / Phase / Strength / Reference
4 ACTIONS       = Inward / Outward / Across / Over
```

The processing-is-memory update does not replace the invariant six-pair oscillator or the three physical Mirror-Gate / three-triad cluster interpretation. It clarifies where state lives and how computation is expected to propagate through the physical machine.
