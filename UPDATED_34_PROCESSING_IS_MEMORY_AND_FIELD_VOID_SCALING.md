# UPDATED 34 — Processing Is Memory and Field/Void Scaling

**Status:** Current architectural handoff extending Updated 33. This update records the latest compute/memory interpretation without changing the invariant six-pair oscillator.

## 1. Core Correction: Processing Is the Memory

The target VTC/Wave Computer architecture is not conventional `CPU -> RAM -> CPU` execution.

The intended primitive is stateful:

```text
physical cell holds state
 -> receives a relational/differential input
 -> changes state locally
 -> resulting state remains physically available
 -> neighboring/next-scale relation reads that state
```

Therefore the target cell combines:

```text
STATE + MEMORY + PROCESSING + ROUTING
```

The processing substrate is also the working memory substrate. There is no required separate main-RAM layer for the local compute network.

This is an architectural target until the physical primitive demonstrates write, retain, read, rewrite and propagation experimentally. Magnetic persistence/remanence may supply the state-storage mechanism, but must be measured rather than assumed.

## 2. Local vs. Supervisory Control

Local cells/clusters retain the richer relational state:

```text
ternary direction: -1 / 0 / +1
views: Direction / Phase / Strength / Reference
```

A higher supervisory layer should remain sparse where possible:

```text
0 = do not intervene / let local network resolve
1 = intervene / trigger / reroute / reset
```

The binary supervisory decision is not the local compute state. It is an oversight/engagement decision over a locally stateful ternary network.

## 3. Field / Void at Processor Scale

At large scale, Field and Void are two opposed processing regions operating on the same relational reference rather than two conventional CPUs with giant separate RAM banks.

```text
                 SHARED REFERENCE / RELATION
                           (0)
                            |
               +------------+------------+
               |                         |
            FIELD                       VOID
      expression / expansion     compression / reduction
      local persistent state     local persistent state
               |                         |
               +------ differential -----+
                            |
                         ROUTING
```

Each side's working memory is primarily the persistent physical state of the cells/clusters contained in that side.

Field and Void must expose the same external relational contract so their outputs can be compared or recursively reused:

```text
Direction
Phase
Strength
Reference
```

## 4. Same Primitive at Multiple Scales

The recursion remains:

```text
mirror relation
 -> local differential
 -> shared differential
 -> higher relation
```

At higher scale, an entire cluster/cube may occupy the role that one lower-level cell occupied, provided its external interface remains compatible.

Hard scalability rule:

> `OUTPUT relation at level n == INPUT relation expected at level n+1`.

The same must work in reverse for downward routing/decomposition.

## 5. Four Actions in the Recursive Compute Path

The current action interpretation remains:

```text
INWARD  = receive/return a relation toward local processing/reference
OUTWARD = express the locally resolved relation
ACROSS  = combine opposed/mirrored outputs into a shared differential
OVER    = pass/cross that resolved relation into the next cell, cluster or scale
```

These remain Actions, not Views.

The Four Views remain:

```text
Direction
Phase
Strength
Reference
```

## 6. DC / AC Functional Split

The current physical interpretation remains two-layered:

```text
DC decision:
EVERYTHING / NOTHING
engage      / no assertion

AC/differential decision:
LEFT / STAY / RIGHT
-1   /  0   / +1
```

Signal path:

```text
signal IN
 -> DC engagement
 -> OUTWARD expression
 -> local AC differential
 -> ACROSS shared differential
 -> OVER connection gate
 -> next differential
```

The two mirror cells each accept signal-in and express a local differential-out. Their combined/shared differential becomes the next-scale input relation.

## 7. Connected Cube Scaling

The machine scales as connected cube modules rather than one indefinitely enlarged monolithic structure.

Inside a cube, the target recursion remains based on triads and 3-of-3 grouping. Between cubes, the same relational interface must be exposed on physical faces as engineering permits.

Conceptual face directions:

```text
+X / -X
+Y / -Y
+Z / -Z
```

Each cube should be externally usable as one larger relational node.

This enables:

```text
one cube
 -> face-connected cubes
 -> 3 x 3 x 3 = 27-cube block
 -> blocks of blocks
```

Compute density should eventually come from many microfabricated stateful primitives inside each cube, not from requiring millions of hand-sized cubes.

## 8. Microfabrication Direction

The long-term micro version is not a PCB miniaturization.

Target path:

```text
measured breadboard primitive
 -> microfabricated/thin-film stateful triad test structures
 -> repeated triad test die
 -> stacked dies / 3D bonded micro-module
 -> six-face connected cube package
 -> cube lattice
```

Candidate technologies may include mixed-signal semiconductor structures, patterned magnetic or magnetoresistive elements, thin-film interconnect, vertical interconnect and 3D die/wafer bonding. The implementation is intentionally not frozen until the bench primitive is measured.

## 9. First Hardware Proof That Matters

The most important proof is not a large cube. It is a small recursive chain showing:

1. a physically linked/opposed mirror relation;
2. reliable `-1 / 0 / +1` differential resolution;
3. state retention if memory is claimed;
4. the retained/resolved state directly participates in the next computation;
5. the output drives the next identical relational stage without an external processor reconstructing the state;
6. two lower differentials can form a higher differential using the same interface.

If those pass, `processing = memory` is supported at the primitive level and scale-up becomes an engineering replication problem rather than an architectural redesign.

## 10. Information vs. Addressing Reach

One trit still contains only three states and therefore `log2(3) ~= 1.585` bits of information.

Recursive branching gives addressing/control reach:

```text
n ternary decisions -> 3^n possible endpoints
```

This does not make one trit equal millions of bits. The architectural benefit sought is that local stateful compute can reduce the amount of centralized control required while permitting hierarchical routing over many cells.

## 11. Dependency Protection

Updated 34 extends, but does not replace, Updated 33.

Canonical dependency direction remains:

```text
shared reference -(0)+
 -> six-pair invariant oscillator
 -> Views / Actions / Choices / Moves / modulation
 -> triad physical implementation
 -> stateful processing-is-memory primitive
 -> recursive differential cluster
 -> connected cube
 -> Field/Void higher-scale split
 -> sparse supervisory control
 -> domain applications
```

Do not reinterpret the Field/Void processor split as evidence that the invariant kernel contains conventional separate CPUs or mandatory external RAM.
