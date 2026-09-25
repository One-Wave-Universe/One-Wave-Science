# UPDATED 34 — Processing-Is-Memory and Connected Cube Scaling

**Status:** Current implementation handoff extending UPDATED 33. This file records the latest VTC architecture decisions so the repository does not drift back toward conventional CPU/RAM assumptions.

## 1. Processing Is the Memory

The target VTC architecture does not separate processor state from working memory in the conventional `CPU -> RAM -> CPU` pattern.

```text
cell holds physical state
 -> cell receives a differential relation
 -> cell evaluates/changes its own physical state
 -> the new state remains locally available
 -> neighboring cells/clusters read that state relationally
```

The target primitive therefore combines:

```text
state + memory + transition/logic
```

and a cluster combines:

```text
distributed memory + distributed processing + routing
```

If magnetic remanence or another persistent physical mechanism is used, retention must be experimentally demonstrated. The architecture requires write, retain, read, rewrite, and propagation behavior; it must not merely assume that a pickup voltage is static memory.

## 2. Sparse Higher-Level Control

Because local cells/clusters carry their own state and perform local ternary resolution, a higher controller should not micromanage every `-1/0/+1` state.

The intended split is:

```text
LOCAL NETWORK
-1 / 0 / +1
Direction / Phase / Strength / Reference

HIGHER OVERSIGHT
0 = no intervention / allow local resolution
1 = intervene / trigger / reroute / override
```

This keeps the richer ternary dynamics local while allowing a simpler binary supervisory decision when needed.

## 3. Field / Void as Opposed Processing Regions

At larger scale, Field and Void are implemented as two opposed processing regions operating on the same relational state around a shared reference.

```text
             SHARED REFERENCE / STATE
                       (0)
                        |
             +----------+----------+
             |                     |
          FIELD                  VOID
       expressive side       compressive side
             |                     |
             +------ differential--+
                        |
                     routing
```

The two sides may each contain their own persistent local cell state. They do not require separate conventional RAM banks if the physical computing cells themselves retain state.

The large-scale relation is therefore the same recursive pattern as the low-level triad: opposed states around a reference, resolved through differential interaction.

## 4. Recursive Interface Rule

Every scale must consume and expose the same relational contract:

```text
Direction
Phase
Strength
Reference
```

and use the same canonical Actions:

```text
Inward
Outward
Across
Over
```

The hard scalability test is:

> A complete lower-level cluster can be replaced by a higher-level cluster without forcing the surrounding system to understand the cluster's internal implementation.

Equivalently:

```text
OUTPUT relation of level n == INPUT relation expected by level n+1
```

The same rule must work downward as well as upward.

## 5. Scale Up and Scale Down

Upward recursion:

```text
local differential
 -> shared differential
 -> triad relation
 -> 9-element cluster relation
 -> cube relation
 -> cube-cluster relation
```

Downward recursion:

```text
higher relation
 -> select/condition cube
 -> local cluster
 -> triad
 -> local physical state/action
```

Most activity should remain local. Higher levels receive resolved relations/events instead of raw state from every primitive.

## 6. Connected Cube Machine

The long-term machine is a network of **connected cube modules**, not one indefinitely enlarged folded monolith.

The internal folded/stacked structure creates one cube module. The machine scales by connecting those cubes face-to-face.

A cube should expose relational interfaces over the six spatial faces as engineering permits:

```text
+X / -X
+Y / -Y
+Z / -Z
```

with shared-reference continuity and differential/event paths carried through the module boundary.

The core abstraction is:

> A complete cube is externally usable as one larger relational node.

This allows:

```text
1 cube
 -> connected cubes
 -> 3 x 3 x 3 = 27-cube block
 -> blocks of blocks
```

without redesigning the logical interface at every scale.

## 7. Internal 3-of-3 Geometry

Current hierarchy:

```text
3 physical elements -> 1 triad
3 triads -> 9-element base cluster
3 cluster orientations/planes -> 27-position internal volume
```

The 27 positions are not intended to be 27 conventional processors. They are recursively related state/compute regions using the same differential architecture.

## 8. DC / AC / Connection Sequence

The current cell-scale flow is:

```text
SIGNAL / RELATION IN
 -> DC decision: EVERYTHING / NOTHING
 -> local expression OUTWARD
 -> AC differential: LEFT / STAY / RIGHT = -1 / 0 / +1
 -> ACROSS: mirrored outputs form shared differential
 -> OVER: resolved relation crosses the connection boundary
 -> NEXT DIFFERENTIAL
```

The two mirrored cells each have signal-in and differential-out. Their shared differential becomes the next-scale relation. Combined differentials must feed an identical interface rather than a new gate species.

## 9. Four Views and Four Actions — Do Not Re-Mix

Canonical Views describe the state:

```text
Direction
Phase
Strength
Reference
```

Canonical Actions transform/route it:

```text
Inward
Outward
Across
Over
```

Earlier material calling Inward/Outward/Across/Over "Views" is superseded.

## 10. Three Physical Mirror Gates per Base Cluster

One base cluster contains three triads and therefore three physical Mirror Gates:

```text
1 triad = 2 linked/opposed mirror elements + 1 differential evaluator
3 triads = 9 active elements
3 physical Mirror Gates x 2 traversal orientations/phases = 6 logical pair positions
```

The six logical pair positions remain:

```text
F1/V6 - V5/F2 - F3/V4 - V3/F4 - F5/V2 - V1/F6
```

Do not reinterpret this as six physically separate mirror-gate devices.

## 11. Microfabricated Version

The actual micro version is not defined as a PCB miniaturization. The intended long-term path is true microfabrication using an appropriate combination of:

- lithographically patterned conductors;
- thin-film magnetic or magnetoresistive elements if validated;
- semiconductor differential/sense circuitry;
- stacked dies or wafer bonding;
- vertical interconnect such as TSV or hybrid bonding;
- packaged six-face or equivalent inter-module connectivity.

Conceptual progression:

```text
breadboard measured primitive
 -> microfabricated triad test structures
 -> repeated triad test die
 -> stacked 3D module
 -> cube package
 -> connected cube lattice
```

The first custom fabrication should be a test die containing many variants of the primitive geometry/process, not a million-cell final cube before the primitive is characterized.

## 12. Proof-of-Concept Priority

Before custom wafer money is spent, the bench proof must show:

1. mechanically/electromagnetically linked opposed response;
2. stable differential `-1 / 0 / +1` regions;
3. a resolved differential can condition/drive the next identical stage;
4. retained state if magnetic memory is claimed;
5. the same interface works from one triad to the next cluster level;
6. simple balanced-ternary arithmetic including sum and carry where required.

The strongest early demonstration is not merely storage. It is a stateful compute chain in which the physical state participates in the next computation without a conventional external RAM write-back cycle.

## 13. First Arithmetic Target

One-trit balanced-ternary addition remains the first compute target.

```text
inputs: A,B in {-1,0,+1}
outputs: sum trit + carry trit where required
```

Examples:

```text
+1 + (-1) -> 0
+1 + +1 = +2 = (+1 x 3) + (-1 x 1)
-1 + -1 = -2 = (-1 x 3) + (+1 x 1)
```

Ternary does not remove carry. A trit contains `log2(3) ~= 1.585` bits of information. Recursive `3^n` growth describes addressing/control reach, not the information content of one trit.

## 14. Canonical Dependency Direction

```text
shared reference -(0)+
 -> six-pair invariant oscillator
 -> Views / Actions / Choices / Moves / five-state modulation
 -> triad physical primitive
 -> recursive differential interface
 -> processing-is-memory cluster
 -> connected cube module
 -> cube lattice
 -> Field/Void large-scale split
 -> sparse supervisory control
```

Do not reverse this dependency direction or reintroduce a conventional CPU/RAM assumption as if it were required by the architecture.
