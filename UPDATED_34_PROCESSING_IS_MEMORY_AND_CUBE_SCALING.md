# UPDATED 34 — Processing Is Memory and Connected Cube Scaling

**Status:** Current architecture handoff extending Updated 33. This update records the latest VTC compute-memory and cube-scaling decisions without changing the invariant six-pair kernel.

## 1. Processing Is the Memory

The target machine does not separate processor and RAM in the conventional sense.

```text
conventional:
RAM stores state
CPU fetches state
CPU changes state
RAM stores new state

VTC target:
cell holds physical state
cell receives a relational differential
cell changes physical state
new state remains locally available
neighboring differentials act directly on that state
```

Therefore the intended primitive is simultaneously:

```text
state + memory + computation + transition
```

and a cluster is:

```text
distributed memory + distributed processing + routing
```

If magnetic memory is used, this remains an experimental implementation claim until write, retention, read, rewrite, disturbance, and propagation are measured.

## 2. Large Field / Void Split

The large-scale Field/Void split should preserve the same relational structure rather than introducing a conventional central CPU that micromanages every cell.

```text
                 shared reference / state relation
                            (0)
                             |
                  +----------+----------+
                  |                     |
              FIELD REGION          VOID REGION
              expression side       compression side
                  |                     |
                  +------ differential--+
                             |
                           route
```

Each region contains its own local persistent compute-state. There is no architectural requirement for a separate giant RAM bank attached to each processor region.

A sparse higher controller may remain binary where appropriate:

```text
0 = no intervention / let local network resolve
1 = intervene / trigger / reroute / reset
```

The richer local state remains ternary and relational.

## 3. Information Capacity vs. Recursive Reach

One trit contains three possible values and therefore:

```text
log2(3) ~= 1.585 bits
```

Recursive ternary branching gives addressing/control reach, not extra information magically stored in one trit.

```text
n trits -> 3^n possible ternary patterns/endpoints
```

Example:

```text
13 trits -> 3^13 = 1,594,323 possible patterns/endpoints
```

Keep these concepts separate:

- information per trit;
- number of configurations in an n-trit word;
- number of lower-level nodes a higher-level relation can address or condition.

## 4. Connected Cube Machine

The mature architecture scales through **connected cube modules**.

The cube is a recursive compute-memory module, not a conventional processor box with external RAM.

Each complete cube should expose the same relational contract that it consumes:

```text
Direction
Phase
Strength
Reference
```

and permit relations over six spatial faces where physically implemented:

```text
+X / -X
+Y / -Y
+Z / -Z
```

The external rule is:

> A complete cube must be usable by neighboring structure as one larger relational node.

This allows:

```text
triad
 -> 3-triad cluster
 -> volumetric cube
 -> face-connected cubes
 -> 3 x 3 x 3 cube block
 -> blocks of blocks
```

without changing the logical interface at each scale.

## 5. Scale Up and Scale Down

Recursion must work in both directions.

Upward aggregation:

```text
local differential
 -> shared differential
 -> triad/cluster relation
 -> cube relation
 -> cube-block relation
```

Downward conditioning:

```text
higher relation
 -> cube
 -> cluster
 -> triad
 -> local state transition
```

Most state resolution should remain local. Higher levels receive or send compact resolved relations/events rather than continuously mirroring every primitive value.

## 6. Four Views / Four Actions at Every Scale

The corrected distinction remains invariant:

```text
VIEWS = what is read
Direction
Phase
Strength
Reference

ACTIONS = what is done
Inward
Outward
Across
Over
```

For current compute routing:

- **Inward:** receive/return toward a local or lower-scale relation.
- **Outward:** express a resolved local relation toward a larger scope.
- **Across:** couple or compare peer/mirrored relations at the same scale.
- **Over:** cross a cluster/cube boundary so the resolved relation becomes input to another relation or scale.

These are operational semantics, not separate physical forces.

## 7. Bench Proof Needed Before Density Claims

The immediate proof remains small:

1. one opposed linked pair produces a stable measurable differential;
2. ternary `-1 / 0 / +1` regions are repeatable;
3. the result can condition the next identical stage;
4. retained state, if claimed, survives driver release and can be read with acceptable disturbance;
5. two/three triads demonstrate simple balanced-ternary arithmetic and recursive handoff;
6. replacing a primitive relation with a higher cluster does not require a fundamentally different surrounding interface.

Only after these pass should millions-of-cells density or custom 3D microfabrication be treated as engineering scale-up rather than proof of the primitive.

## 8. Microfabrication Direction

The long-term micro version is actual microfabrication, not merely a miniature PCB.

Candidate implementation families include:

- thin-film magnetic or magnetoresistive state elements;
- semiconductor differential sensing/drive;
- lithographic metal routing and reference structures;
- stacked dies / wafer bonding;
- vertical interconnect such as TSV or hybrid-bonded contacts;
- six-face package-level cube interconnect where practical.

The first custom fabrication should be a small test die containing many variants of the primitive geometry, followed by measurement and selection before attempting a dense connected cube.

## 9. Dependency Rule

Updated 34 does not replace the Updated 33 invariant kernel.

```text
shared reference -(0)+
 -> six-pair oscillator
 -> Views / Actions / Choices / Moves / States
 -> physical triad implementation
 -> processing-is-memory
 -> connected cube recursion
 -> large Field/Void regions
```

If a memory technology, magnetic material, packaging method, or processor implementation changes, the invariant relational architecture must remain separately testable.
