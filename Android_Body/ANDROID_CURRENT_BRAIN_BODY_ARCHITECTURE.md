# Android Current Brain/Body Architecture

Status: WORKING ARCHITECTURE / YELLOW until implemented and measured

Purpose: consolidate the current Android build direction in one place without treating the Jetson as the brain. Jetson remains a perception test platform for real hearing and seeing. This document defines the current brain/body organization to be implemented and tested.

## 1. Brain primitive: the loop

The brain starts at the smallest reusable hardware loop, not at a Jetson or monolithic processor.

Current working chip-function sequence:

1. **DC loop** — binary/polarity choice around a local center reference.
2. **AC loop** — alternating ternary directional choice, represented functionally as negative / hold / positive (for example left / stay / right or down / stay / up depending on the controlled axis).
3. **RC loop** — rotational/quadratic magnetic-state layer. Its job is not to erase the lower choices but to turn a resolved directional relation into a rotational state that can be held, routed, or used as the point/reference for the next scale.

The exact semiconductor implementation, chip count, and packaging remain engineering questions. The architecture rule is that a complete lower-scale resolved loop may become one effective point/reference for the next scale.

## 2. Loop -> cube -> connected brain structure

The current scaling hierarchy is:

```text
DC / AC / RC loop functions
        ↓
loop chips / loop modules
        ↓
stacked cube
        ↓
multiple cubes
        ↓
dual-pyramid connection structure
        ↓
two Rubik-style brain structures first
        ↓
possible third Rubik structure later if testing justifies it
```

"Rubik" here names the intended 3D recursive connection organization, not a claim that a toy cube geometry is already the final circuit layout.

The **dual-pyramid connections** are the current working connection model between cube-scale structures. They must preserve bidirectional Field/Void traffic and make the origin, direction, and scale of a packet recoverable rather than flattening every connection into one undifferentiated bus.

## 3. M4 router

M4 is the fast routing layer between the connected brain structures and the body.

Its current job is:

- route state upward and action downward;
- preserve which local control/sensory branch a packet came from;
- coordinate timing and handoffs between loops and scales;
- avoid centralizing every local decision that can be completed safely in the body;
- carry memory-rebuild receipts and reconstructed state to the correct branch;
- keep command and sensory return associated as a pair.

M4 is not the motor power stage and is not the perception hardware itself.

## 4. Body: inverted/flipped underlying Field/Void intelligence

The body is not a dumb actuator shell. It is the lower-scale, distributed recurrence of the same Field/Void organization used in the brain.

Working rule:

- **views/state travel up**;
- **actions/commands travel down**;
- the body-side implementation is the **inverted and flipped underlying Field/Void structure**;
- local body branches may compare, hold, route, and respond before escalating everything to the brain;
- higher levels receive compressed, branch-identified state rather than an unstructured flood of raw sensor values.

This is a distributed-control architecture claim to be tested, not a claim of biological identity.

## 5. Ternary nerve and three-winding motor control

The current motor-control primitive is:

```text
ternary nerve command
        ↓
3-phase / three-winding power driver
        ↓
three motor windings
        ↓
rotating magnetic field / actuator motion
```

The ternary nerve carries the command relation, not the motor power.

At minimum the command space is:

- negative direction;
- hold/stay;
- positive direction.

For a rotary actuator this may map to reverse rotation / hold or brake / forward rotation. Exact commutation is a motor-driver implementation detail and must be derived from the real motor and driver used.

## 6. Paired control + sensory line ("vagus" return)

Every local control branch is paired with a sensory return branch.

```text
M4 / higher control
      │
      ├── action-down control line ──> local nerve/driver/actuator
      │
      └── state-up sensory line <──── local sensors on that same branch
```

The sensory line is functionally called the **vagus sensory line** in the current architecture. It is not required to be one literal global wire and is not a claim that the robot duplicates biological vagus anatomy.

Each control branch should keep its own relevant feedback physically/logically associated with the command branch. Examples may include position, angle, current/load, temperature, contact/pressure, proximity, tilt, or fault state.

Core rule:

**control line + attached sensory return = one local nerve pair**

This lets M4 route command/sense pairs without reconstructing their relationship after the fact.

## 7. Magnetic memory vs spintronic action

Keep two magnetic roles distinct.

### Magnetic memory

Magnetic memory is the hold/retention role. A resolved state may be written into a persistent magnetic state and survive after the active write command is removed.

### Spintronic/quadratic action-down path

Spintronic behavior belongs to the action-down command path in the current design direction. It is not automatically the same thing as magnetic memory.

Therefore do not collapse:

```text
magnetic hold == spintronic command
```

They are separate functions unless a future real device demonstrably performs both.

## 8. Memory recall and rebuild integration

The existing constellation / Rabbit-Hopping reconstruction work is part of the brain architecture, not a detached software trick.

Current intended path:

```text
partial/local cue
    ↓
constellation entry / associative neighborhood
    ↓
Rabbit-Hopping traversal with route/origin preserved
    ↓
reconstruction / completion
    ↓
ambiguity handling only where needed
    ↓
validation against current sensory/context state
    ↓
RebuildReceipt
    ↓
M4 routes reconstructed state to the correct loop/cube/body branch
```

Rules:

1. Reconstruction must preserve route-of-origin and scale where possible.
2. A rebuilt memory is not automatically trusted; it is checked against current sensory/context evidence.
3. Ambiguity remains explicit instead of being silently converted into certainty.
4. Memory is useful when it can re-enter the live control loop at the right branch and scale.
5. The processing path itself may carry state/history, but persistent magnetic memory and software/associative reconstruction are not to be conflated until hardware tests establish an actual bridge.

## 9. Scale recurrence

Working recurrence rule:

```text
resolved lower-scale relation / rotation
                ↓
becomes one effective point/reference at the next scale
                ↓
new path / relation / boundary is constructed
                ↓
next-scale choice and rotation
```

This is the current bridge between the DC/AC/RC loop concept, cube stacking, and larger Rubik-style organization.

## 10. Jetson boundary

Jetson is **not the new brain architecture**.

Jetson's role is a perception and sensor test bench for real-world hearing and seeing, including camera/microphone processing and experiments needed to understand what information the Android brain/body should receive.

Perception output may feed the Android architecture through a defined interface, but the Android brain must not be structurally defined as "whatever runs on Jetson."

## 11. Implementation order

Do not attempt the whole architecture at once.

1. Prove one centered DC/polarity loop with real components.
2. Prove the AC/ternary negative-hold-positive decision.
3. Prove magnetic retention independently of the decision circuit.
4. Prove a real handoff from ternary decision to retained magnetic state.
5. Prove one paired control/sensory nerve branch.
6. Prove ternary command into a real three-winding motor driver.
7. Connect several local nerve pairs through M4 while preserving branch identity.
8. Feed memory `RebuildReceipt` output back through M4 to the correct branch and test it against live sensory state.
9. Package proven loops into a cube-scale module.
10. Test cube-to-cube dual-pyramid routing before expanding to two complete Rubik-style structures.
11. Add a third Rubik structure only if a measured architectural need appears.

## 12. Reality-first rule

The architecture does not get to dictate simulator or bench results.

- virtual breadboard physics should be independent of One-Wave expectations;
- known circuits calibrate the simulator first;
- novel DC/AC/RC and body-control circuits are then tested against that neutral model;
- bench measurement overrides the model when they disagree;
- failures update the architecture instead of being hidden by special-case simulator behavior.

## 13. Current open engineering questions

- whether DC, AC, and RC functions become six distinct fabricated chips, fewer multifunction chips, or repeated cell arrays;
- exact cube topology and physical interconnect;
- exact dual-pyramid connection geometry and arbitration rules;
- what persistent magnetic device is best for the memory role;
- what spintronic device, if any, provides a practical action-down advantage;
- how the three-winding motor command maps to concrete commutation hardware;
- bandwidth and encoding of the paired sensory return;
- how much local body intelligence should terminate decisions locally versus escalate to M4;
- how software associative memory maps onto eventual hardware memory without losing validation and receipts.

These are to be resolved by prototype and measurement, not filled in by assumption.
