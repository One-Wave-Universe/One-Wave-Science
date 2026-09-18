# UPDATED 50 — SCLFS Lattice Frame Binding, Verification, and Miniverse Runtime

**Date:** 2026-09-08  
**Audience:** Codex, Gemini, local Jetson workers, M4/OpenClaw, and humans working on SCLFS / Miniverse  
**Status:** architecture handoff and software contract. This is not a proof of a physical superfluid/crystal medium.  
**Priority:** read this before changing SCLFS lattice navigation, Miniverse storage, formatter semantics, or lattice verification.

---

## 0. Why this update exists

Recent work drifted into treating the lattice as a generic folder tree, a decorative 3D grid, or a set of arbitrary `x,y,z` numbers. That is not the intended runtime.

The current requirement is:

```text
ACTUAL / FORMATTED LATTICE
fixed geometry + fixed topology + fixed reference

            <-> frame binding

ACTIVE MOVING FRAME
position + X/Y/Z orientation + mirror state + scale + route

            <->

AI / OBJECT / PROCESS
moves through or exactly mimics movement through the lattice
```

The lattice is the stationary world/reference. The process, active state, AI location, orientation, phase, displacement, mirror state, and routes may move/cycle through it.

If direct bound traversal is too expensive for normal runtime, a RAM shadow is allowed only when it is an exact geometry/topology-preserving mimic of the authoritative lattice.

---

## 1. Locked distinction: crystal vs moving process

### 1.1 Stationary lattice / crystal layer

The following are persistent unless an explicit topology migration or reformat is performed:

- cell identity;
- rest position / rest coordinate;
- native geometry;
- legal neighbor relationships;
- mirror relationships;
- scale relationships;
- topology / connectivity;
- reference / Baseline Zero anchors.

Normal movement must not silently rewrite this layer.

```text
BASE LATTICE = STATIONARY
```

### 1.2 Moving / superfluid-process layer

The following may change continuously:

- active cell / occupant location;
- local X/Y/Z orientation;
- displacement from rest;
- phase;
- orientation / rotation;
- mirror / parity state;
- Field/Void state;
- HOLD state;
- active route;
- active task;
- generation;
- propagated state;
- AI presence.

```text
PROCESS = MOBILE
STATE MAY MOVE THROUGH SPACE
SPACE MAY NOT SILENTLY MOVE UNDER THE STATE
```

This is a software architecture rule. Do not promote it into a physical claim without separate evidence.

---

## 2. The missing implementation concept: frame binding

Do not implement movement as only:

```text
x += 1
```

A moving AI/object/process must carry an **active local frame** that is bound to the lattice underneath it.

Minimum active-frame state:

```text
ACTIVE_FRAME
    current_cell
    local_x_basis
    local_y_basis
    local_z_basis
    orientation
    mirror_state
    parity
    scale
    route
```

A lattice cell needs enough information to support that binding.

Candidate software record:

```text
CELL
    id
    native_dim
    geometry_type
    rest_position
    local_basis
    neighbors
    edge_transforms
    mirror_relationships
    scale_parent
    scale_children
    generation_anchor
    checksum
```

`x/y/z` alone are insufficient if the local frame can rotate, mirror, flip, invert, oppose, or change scale while moving.

---

## 3. Movement law

A local movement request must resolve through the current frame and the actual lattice topology.

```text
MOVE local +X
        |
        v
read current orientation
        |
        v
map local +X into lattice direction
        |
        v
find legal connected neighbor / edge
        |
        v
cross edge
        |
        v
apply edge transform
        |
        v
bind active frame to destination cell
```

Example:

```text
initial:
local X = lattice +X
local Y = lattice +Y
local Z = lattice +Z

rotate 90 degrees:
local X = lattice +Y
local Y = lattice -X
local Z = lattice +Z

MOVE local +X
=> actual lattice traversal must use lattice +Y
```

A mirror may change handedness/parity while the lattice remains fixed.

Example only:

```text
MIRROR_X:
X -> -X
Y ->  Y
Z ->  Z
```

Do not collapse `FLIP`, `INVERT`, `OPPOSE`, `ROTATE`, and `MIRROR` into one operation. Their exact semantics remain separate and must follow the relevant canonical nodes.

---

## 4. Edge transforms and reversible traversal

The lattice should be treated as a graph whose edges may carry transforms.

For a connection from cell A to cell B:

```text
T(A->B)
```

The reverse connection must satisfy the software invariant:

```text
T(B->A) = inverse(T(A->B))
```

unless a specific one-way/noninvertible mechanism is deliberately declared and tested.

A route:

```text
A -> B -> C -> D
```

followed by the inverse route:

```text
D -> C -> B -> A
```

must recover, exactly where the contract is intended to be reversible:

- starting cell;
- starting orientation;
- starting mirror/parity state;
- starting scale;
- starting reference relationship.

Any unexplained difference is lattice/frame drift and is a FAIL.

---

## 5. Bound mode, shadow mode, visual mode

Three different modes are allowed, but they must not become three different worlds.

### 5.1 BOUND mode

The navigator operates against the authoritative formatted lattice metadata/state.

```text
SCLFS lattice
    -> current cell
    -> actual stored relationship
    -> destination cell
    -> transformed active frame
```

### 5.2 SHADOW mode

For speed, the runtime may load an active neighborhood into RAM and simulate movement there.

```text
actual lattice
    -> topology-preserving shadow
    -> fast RAM traversal
    -> HOLD / generation / checkpoint
    -> validated state written back
```

Hard rule:

```text
SHADOW CELL N <-> AUTHORITATIVE LATTICE CELL N
```

The shadow may not invent a different geometry, neighbor graph, mirror relation, scale relation, or frame transform.

### 5.3 VISUAL mode

A 2D/3D renderer is only a view of the same world state.

```text
AUTHORITATIVE LATTICE
        |
        v
BOUND / SHADOW RUNTIME
        |
        v
2D / 3D VIEW
```

Camera motion, world-view rotation, zoom, or render transforms do not rewrite rest coordinates or topology.

---

## 6. Geometry is not restricted to a generic Cartesian cube

The active frame may use X/Y/Z, but the underlying world may include declared geometries such as:

- cube neighborhoods;
- hex / tri-hex slices;
- 3D close-packed neighborhoods;
- sphere/ball kernels;
- pyramid connectors;
- mirror gates;
- scale connectors.

The navigator must ask:

```text
Where am I?
What native geometry is this cell/neighborhood?
What frame am I using?
What edges legally leave this cell?
What transform occurs when I cross each edge?
What is the inverse/return relationship?
```

Do not force a non-Cartesian relationship into fake `x += 1` movement just to make coding easier.

---

## 7. Scale and route separation

Keep scale, position, wrapper, mirror, and route distinct.

The recurring software scale rail remains a candidate routing/organization contract:

```text
3 <-> 6 <-> 12 <-> 24
```

and the invariant center/reference remains:

```text
L > 1(0)1 < R
```

Do not assume every occurrence of 3, 6, 12, or 24 means the same thing. Preserve explicit role metadata.

Current routing interpretation to test, not blindly hardcode into unrelated domains:

```text
x / multiplication = project / descend / expand into detail
÷ / division       = route back / reconstruct toward parent/whole
+                   = shift one direction
-                   = shift opposite direction
```

Example route idea:

```text
MINIVERSE
  x WORKSHOP
  x PROJECT
  x BRANCH
  x TASK

TASK
  ÷ BRANCH
  ÷ PROJECT
  ÷ WORKSHOP
  ÷ MINIVERSE
```

The return path must be mechanically reconstructable, not inferred from a giant prompt.

---

## 8. Formatter requirement

If the SCLFS formatter is intended to create the lattice, then format success must mean more than "filesystem created".

The formatted volume must contain enough authoritative information to reconstruct the intended lattice semantics, including at minimum the subset that is actually claimed to exist:

- lattice/version identifier;
- native geometry declaration;
- cell identity scheme;
- rest/reference coordinates or equivalent rest topology;
- neighbor/edge relationships;
- edge transforms or sufficient information to derive them;
- mirror relationships where implemented;
- scale relationships where implemented;
- Baseline Zero / reference anchors;
- generation/checksum structures;
- EMPTY vs BALANCED distinction where implemented;
- HOLD / RECALL structures where implemented.

If those are not encoded or reconstructable, the formatter is incomplete relative to the claimed lattice architecture.

Do **not** respond by repeatedly reformatting physical drives. Improve and verify the format/runtime above the already-formatted devices unless a separately reviewed destructive procedure is explicitly authorized.

---

## 9. Independent verifier — mandatory

Do not accept the formatter's own "success" output as proof.

Use separate responsibilities:

```text
mkfs.scl / formatter -> BUILDS
scl-verify            -> INDEPENDENTLY CHECKS
scl-stress            -> TRIES TO BREAK IT
```

The verifier should not simply call the formatter's internal "is valid" routine and trust the same assumptions.

Qualification levels:

```text
SIMULATED
works in memory/test fixture

IMAGE VERIFIED
works in an SCLFS image

DEVICE VERIFIED
works on an actual formatted external device

MINIVERSE VERIFIED
multiple AI processes actually use that device/world
as shared persistent spatial/process state
```

Never jump directly from a unit test to `MINIVERSE VERIFIED`.

---

## 10. What the verifier must test

At minimum, where supported by the current implementation:

### Identity / format

- correct SCLFS magic/version;
- checksum validation;
- expected geometry declaration;
- unique cell IDs;
- no duplicate rest coordinates/addresses;
- valid Baseline Zero/reference.

### Topology

- every legal neighbor resolves;
- inverse neighbor relationships agree where required;
- boundary behavior matches declared geometry;
- mirror relationships are valid;
- scale relationships are valid;
- rest topology does not drift during normal runtime.

### Frame binding

- local X/Y/Z correctly map through current orientation;
- rotation changes active orientation, not rest topology;
- mirror changes parity/handedness according to contract;
- edge transforms produce the expected destination frame;
- inverse route returns to exact starting frame.

### Process state

- dynamic displacement/state can change without changing rest identity;
- HOLD survives close/reopen;
- generation increments correctly;
- EMPTY remains structurally distinct from BALANCED zero;
- RECALL restores the requested valid generation.

### Recovery

- kill runtime;
- reopen;
- reconstruct active state;
- detect damaged newest generation;
- recover from a prior valid generation.

### Multi-agent

- two or more agents can share the same world;
- distinct locations/tasks are preserved;
- simultaneous nonconflicting work does not silently overwrite;
- restart reconstructs agent location/task/process state.

---

## 11. Mandatory drift test

Record the authoritative lattice reference immediately after format/qualification.

Then run heavy activity:

```text
move
rotate
mirror
flip
route
HOLD
RECALL
multiple agents
many generations
restart
```

Afterward:

```text
REST LATTICE BEFORE == REST LATTICE AFTER
```

Any unexplained change is:

```text
FAIL: LATTICE DRIFT
```

At the same time, dynamic process state is expected to differ.

---

## 12. Mandatory bound-vs-shadow equivalence test

Feed the same route/transform stream to both walkers.

```text
BOUND:
MOVE
ROTATE
MOVE
MIRROR
MOVE

SHADOW:
MOVE
ROTATE
MOVE
MIRROR
MOVE
```

After each step compare:

```text
cell_bound        == cell_shadow
orientation_bound == orientation_shadow
mirror_bound      == mirror_shadow
scale_bound       == scale_shadow
route_bound       == route_shadow
```

Only when these stay equal may the shadow claim to mimic the authoritative lattice.

---

## 13. Long random-walk qualification

Generate a deterministic seeded route containing operations such as:

```text
MOVE
ROTATE
MIRROR
FLIP
OPPOSE
SCALE
HOLD
```

where each operation is legal for the current declared geometry.

Recommended stress target:

```text
100,000+ traversal / transform operations
```

Then apply the inverse route where inversion is defined.

Expected:

```text
START CELL   == END CELL
START FRAME  == END FRAME
START PARITY == END PARITY
START SCALE  == END SCALE
```

Zero unexplained drift.

---

## 14. Miniverse: short-term runtime is allowed to be a MUD

The immediate Miniverse does not need to wait for the final 3D renderer or perfect lattice navigator.

A text MUD/shared workshop is acceptable as the first interface because the important first milestone is multiple AI workers sharing one persistent work world.

Required short-term behavior:

- multiple agent identities;
- persistent presence/location;
- shared rooms/neighborhoods;
- chat/idea exchange;
- shared task board;
- task claim/release/done;
- test/diff/review receipts;
- bounded coding work;
- independent review.

The existing `miniverse_mud` source is a coordination prototype. The **live Miniverse runtime/state is intended to live on the Jetson external storage, not be confused with the Git repository copy**.

The repository may contain source, tests, schemas, and instructions. The external-drive runtime should carry the live world/process state.

---

## 15. MUD-to-lattice transition

Do not throw away the MUD when the lattice backend becomes ready.

Instead bind its semantic rooms to lattice neighborhoods.

Example:

```text
MUD command: GO workshop

becomes:
agent.location -> WORKSHOP lattice neighborhood
```

Candidate world neighborhoods:

```text
ROOT
|-- HOME / Baseline Zero
|-- WORKSHOP
|-- TEST-LAB
|-- REVIEW
|-- WAREHOUSE
|-- VAULT
|-- RECALL
`-- TRANSIT / M4
```

Later the 2D/3D renderer visualizes those same states.

```text
TEXT MUD
   |
   v
SAME WORLD STATE
   |
   v
LATTICE BACKEND
   |
   v
2D / 3D VIEW
```

Do not create separate incompatible Miniverses for text and graphics.

---

## 16. Process is memory

The intended memory doctrine remains:

```text
PROCESS IS MEMORY
STORAGE EXISTS TO RECONSTRUCT THE PROCESS,
NOT TO REPLACE THE PROCESS
```

Durable state should be sufficient to reconstruct continuing work, including where applicable:

- Baseline Zero;
- active constellation/neighborhood;
- active routes;
- current task;
- current lattice location;
- orientation/frame state;
- body/world anchors;
- agent presence;
- HOLD;
- unresolved work;
- recent validated changes;
- generation.

Recovery target:

```text
runtime stops
    -> process disappears from execution
runtime restarts
    -> read reconstruction anchors
    -> rebuild active neighborhood/frame/routes
    -> resume continuing process
```

Receipts are bounded audit/debug evidence. They are not, by themselves, the world or the memory.

---

## 17. External-drive role separation

Keep storage roles explicit rather than mixing everything together.

Candidate roles:

```text
LIVE / FAST
current Miniverse world, active process, current tasks, active constellation

RECALL
valid generations, deltas, reconstruction anchors, important routes

WAREHOUSE
large/messy useful files, models, projects, assets, history

VAULT
known-good verified milestones / immutable references
```

Critical Baseline Zero / Vault anchors may later be mirrored across physical devices after a reviewed implementation exists.

Do not claim physical redundancy until it is actually configured and tested.

---

## 18. Physical-device honesty boundary

The authoritative software lattice can be bound to a real formatted external device, but software generally cannot assume direct control of exact NAND transistor placement on an SSD because the device controller performs wear leveling/remapping. Similar caution applies to treating HDD logical addresses as exact platter geometry.

Therefore distinguish:

```text
REAL EXTERNAL DEVICE
    -> SCLFS logical/device-backed lattice
    -> authoritative cell/topology/frame state
```

from any stronger claim about exact underlying microscopic media placement.

This limitation does **not** prevent a real device-backed persistent lattice runtime. It only prevents overstating what layer of the hardware is controlled.

---

## 19. Current implementation priority

Do not spend the next cycle polishing decorative 3D visuals.

Priority order:

```text
1. Verify what the current formatter actually encodes.
2. Build/finish independent lattice verifier.
3. Implement Cell + Neighbor + Edge Transform representation.
4. Implement Frame Binder / Lattice Navigator.
5. Implement BOUND walker.
6. Implement SHADOW walker.
7. Prove BOUND == SHADOW on deterministic route tests.
8. Put the shared MUD runtime/state on the intended external storage.
9. Connect persistent AI participants / agent gateway.
10. Bind MUD rooms/tasks/agents to lattice neighborhoods.
11. Add 2D/3D visualization as a view of the same state.
```

If the current formatter already encodes enough topology/frame information, do not rewrite it unnecessarily. Build the navigator/verifier on top.

If it does not, document the exact missing fields/contracts and make the smallest versioned format change required.

---

## 20. Definition of success

The target is not "a directory named lattice" and not "an animation of dots moving in 3D."

A meaningful first success is:

```text
fixed authoritative lattice
        +
movable bound local frame
        +
legal topology-aware traversal
        +
mirror / rotation / scale transforms
        +
exact return / reconstruction
        +
independent verification
        +
shared multi-AI Miniverse state
```

The key invariant is:

```text
CELL / TOPOLOGY / REST REFERENCE = STABLE
ACTIVE FRAME / PROCESS / OCCUPANT = MOVES
SHADOW MAY MIMIC MOVEMENT
BUT MUST MAP EXACTLY TO THE SAME LATTICE
```

---

## 21. Codex hard-start for the next lattice task

Before editing SCLFS or Miniverse lattice behavior:

1. Read `AI_CANONICAL_START_HERE.md`.
2. Read `AI_LOCAL_OPERATIONS.md` if working on the Jetson/local runtime branch where it exists.
3. Read `AI_GUIDE_LOCAL_MINIVERSE_DREAMWORLD_AND_INTERDIMENSIONAL_ARCHITECTURE.md`.
4. Read this file completely.
5. Inspect the **actual current SCLFS implementation** before proposing a format rewrite.
6. State what is currently encoded versus what this contract still requires.
7. Change one bounded layer at a time.
8. Run deterministic tests before model interpretation.
9. Keep physical-device destructive operations outside ordinary coding-worker authority.

Do not silently invent unresolved mirror or geometry semantics merely to make tests pass.

---

## 22. Claim labels for all future lattice work

Every result must say which category it belongs to:

- `ARCHITECTURE CONTRACT`
- `IMPLEMENTED SOFTWARE`
- `SIMULATION RESULT`
- `IMAGE VERIFIED`
- `DEVICE VERIFIED`
- `MINIVERSE VERIFIED`
- `ASSUMPTION`
- `OPEN QUESTION`
- `FAILED / FALSIFIED`

A passing software fixture is evidence only for the software behavior exercised by that fixture.
