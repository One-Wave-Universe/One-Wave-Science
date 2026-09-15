# UPDATED 33 — Invariant Engine, VTC Build, and View/Action Correction

**Status:** Current implementation handoff. This update supersedes the old physical reading of `3 Mirror gates + 3 Action gates`.

## 1. Primary correction

The architecture has a hard boundary:

```text
PHYSICAL CELL
 -> logical / receipt vocabulary
 -> representation wrappers
 -> higher-scale/domain instantiations
```

The physical CELL_V1 primitive is **three bidirectional Mirror axes**, not six one-way physical gates.

```text
A+ <-> A-
B+ <-> B-
C+ <-> C-

3 physical bidirectional mirrors
= 6 directed edge interfaces
```

The clockwise hex order remains:

```text
A+ -> B+ -> C+ -> A- -> B- -> C-
```

Ports are on flat sides only.

### Anti-drift rule

> Any six-position software/process notation must project onto the three physical bidirectional A/B/C mirrors. It may not create three additional physical Action gates.

## 2. Six positions are logical/receipt positions, not six physical gates

Legacy notation may still describe a six-position recurrence:

```text
M1 -> A1 -> M2 -> A2 -> M3 -> A3 -> ...
```

but the letters now identify **what is being observed or done at a phase of the recurrence**, not six different physical gate devices.

Physical interpretation:

```text
Mirror A: A+ <-> A-
Mirror B: B+ <-> B-
Mirror C: C+ <-> C-

UP direction   = View / state / relation propagation
DOWN direction = Action / conditioning / Override propagation
```

The same mirror/path supports both directions.

Do not reconstruct this as:

```text
physical Mirror 1 -> separate physical Action 1
physical Mirror 2 -> separate physical Action 2
physical Mirror 3 -> separate physical Action 3
```

That physical interpretation is superseded.

## 3. Keep the different six-counts separate

```text
3 physical bidirectional mirrors
6 directed CELL_V1 edge interfaces
6 route addresses = 2 binary relations x 3 ternary moves
6 optional logical/receipt positions
```

Matching counts do not prove identity.

A winding count, MOSFET count, motor phase count, logical step count, and brain-layer count are separate engineering variables unless a measurement or derivation connects them.

## 4. Field / Void mirror rule

Field and Void remain opposed roles around a shared reference. A Mirror operation does not swap their ontology.

Views travel UP and Actions travel DOWN through the same physical mirror relation:

```text
local retained state
 -> View UP
 -> higher/local resolution
 -> Action or no-intervention DOWN
 -> resulting local state
 -> next View UP
```

The return is state-advancing, not an automatic reset.

## 5. Four Views

The current View descriptors are:

```text
Direction
Phase
Strength
Reference
```

They describe what can be measured/read while state propagates upward. They are **not four physical gates**.

## 6. Quadratic Actions

The current Action-mode vocabulary is:

```text
Inward
Outward
Across
Over
```

These are descriptors for downward/outward conditioning and routing. They are **not separate primitive hardware gates** and do not add to the three physical mirrors.

A higher-level Override is a downward action/conditioning event through the same bidirectional path structure.

## 7. Binary and ternary roles

The executable primitive keeps two binary relations and three ternary moves:

```text
BINARY: YES / NO
TERNARY: DOWN / HOLD / UP

2 x 3 = 6 route addresses
```

Ground/no committed binary choice remains outside the six-route set.

`HOLD` is active balance at the shared center/reference, not absence.

For nerve/motor use, ternary is also the candidate local motion grammar:

```text
DOWN  = drive/condition in one orientation
HOLD  = balanced hold / relaxed controlled center
UP    = drive/condition in the opposite orientation
```

The exact actuator implementation remains experimental.

## 8. DC / AC / nerve-level reinjection

The current nerve-level physical interpretation is:

```text
DC = supply + controlled energy recovery + reinjection
AC = alternating/recurring activity synthesized through the mirrored paths
TERNARY = local UP/HOLD/DOWN movement and motor command
QUADRATIC = Views UP / Actions DOWN
```

DC is not merely an initial bias that disappears after AC begins. It closes the candidate nerve-level power/recovery loop.

The local electrical reference `V0` is separate from the energy reservoir. Recovered inductive/magnetic energy must be steered into a controlled reservoir/DC link and measured; it must not be dumped into virtual ground.

A candidate local control policy is:

```text
within declared limits -> continue locally / recover / reinject
outside declared limits -> View UP -> higher resolution -> Action/Override DOWN
```

The exact resource variables and thresholds remain experimental.

## 9. Processing is memory

The target architecture is stateful compute-in-memory, not conventional `CPU -> RAM -> CPU` traffic.

```text
stateful path holds physical state
 -> current/signal passes through that state
 -> interaction changes the same local state
 -> changed state remains locally available
 -> next pass is processed through the changed state
```

Therefore the target primitive combines:

```text
state + memory + processing + routing
```

The architecture fails this rule if the claimed memory can be removed from the active processing path while leaving the operation unchanged.

The exact physical carrier is open. Memristive, hysteretic magnetic, spintronic/magnetoresistive, oscillatory, or other stateful paths may be tested. No named device is assumed to satisfy the whole requirement without write/retain/read/rewrite/propagation measurements.

## 10. Bidirectional nerve-gate connection

The nerve/connection element must support the intended bidirectional path.

Candidate implementation:

```text
mV / uV state or differential
 -> explicit measured interface if needed
 -> true bidirectional switch
 -> A/B/C path
```

Back-to-back MOSFETs or another true bidirectional switch are candidates. SiC MOSFETs may be used where their power, thermal, endurance, or switching properties are useful, but they are not assumed to directly resolve millivolt/microvolt information at the gate.

The switch is not automatically the processing-memory element.

## 11. Recursive interface

The same relational contract must survive scaling:

```text
OUTPUT relation of level n
=
valid INPUT relation for level n+1
```

and downward conditioning must close back into a new local state:

```text
UP -> resolution -> DOWN -> NEW STATE -> NEW UP
```

If every scale needs a new controller/decoder species, recursion has failed.

## 12. Point / Path / Rotation / Field / Volume

The physical scaling ladder remains:

```text
Point -> Path -> Rotation -> Field -> Volume -> next-scale Point
```

For CELL_V1:

```text
one hex
 -> edge-to-edge path
 -> closed/circulating route
 -> seven-cell / multi-cell field
 -> stacked 3D volume
 -> resolved next-scale point
```

The exact internal grain of a 3D volume remains experimental.

## 13. Flower and brain-scale candidates

The seven-cell flower is the first locked planar scale assembly: one center hex plus six identical surrounding hexes, all in the same orientation and connected flat-edge to flat-edge.

Current larger-scale candidates remain experiments, not canonized counts:

```text
normal + inverted
2 flowers
2+2
3+3
3 / 3 / 3
3+ / 3- / 3+
3 x 3 x 3
mirrored hemisphere volumes
```

Do not promote numerical symmetry into hardware fact until added depth/function is measured.

## 14. Hierarchical Field/Void split

At larger scale, Field and Void may be opposed processing regions sharing the same relational reference.

Most activity should stay local. Higher levels should receive resolved Views/events rather than micromanaging every local transition.

A released Override does not restore the old state by definition. The resulting local configuration is the new state and becomes the next upward relation.

## 15. First compute target

Balanced-ternary arithmetic remains a useful finite compute test because it exercises `-1/0/+1` without changing the physical architecture.

For two trits A and B, test all nine input combinations and measure sum/carry behavior where required.

The proof target is not merely arithmetic correctness. The same physical primitive must be able to:

1. retain a distinguishable local state;
2. use that state during processing;
3. leave the result retained locally;
4. drive another identical stage;
5. accept downward conditioning through the same bidirectional mirror path;
6. settle into a distinguishable new state;
7. emit the new state upward; and
8. recurse without an expanding translation layer.

## 16. Hardware proof sequence

Do not begin by building six different physical gates.

Use this order:

```text
prove one bidirectional stateful mirror path
 -> prove both directions on that same path
 -> prove retained state changes subsequent behavior
 -> reproduce as A/B/C
 -> verify A+<->A-, B+<->B-, C+<->C-
 -> verify six directed interfaces without six separate gate species
 -> test binary x ternary route behavior
 -> test View UP / Action DOWN recurrence
 -> test DC recovery/reinjection
 -> connect identical hexes
 -> build flower
 -> test stacked/volumetric recurrence
```

## 17. Deprecated physical interpretation

The following wording is retained only when discussing historical software/receipt labels and must **not** be used as the CELL_V1 physical architecture:

```text
3 physical Mirror gates + 3 physical Action gates = 6 physical gates
three Mirror/Action hardware pairs
six separate Mirror/Action devices in series
```

For CELL_V1 hardware, replace it with:

```text
3 physical bidirectional mirrors
6 directed interfaces
Views UP / Actions DOWN through the same mirrors
```

## 18. No internal Gate 7

No seventh internal route/gate is created by View, Action, Override, reinjection, return, memory, or higher-scale coordination.

Higher relations between complete systems may have their own names, but they must not be inserted as another physical CELL_V1 edge/gate.

## 19. Canonical dependency direction

```text
shared reference / DC energy context
 -> three physical bidirectional A/B/C mirrors
 -> local stateful processing-memory path
 -> binary relation + ternary UP/HOLD/DOWN route
 -> AC/rotation behavior where physically implemented
 -> Views UP / Actions DOWN through the same mirrors
 -> local recovery/reinjection or higher Override
 -> resulting new local state
 -> Point/Path/Rotation/Field/Volume recursion
```

Do not reverse this dependency direction, and do not resurrect six separate physical Mirror/Action gates from older terminology.
