# UPDATED 63 — CELL_V1 Stateful Muscle-Memory Build

**Status:** Current physical build architecture. Geometry and three-bidirectional-mirror rules are locked. Stateful carrier, path training law, reinjection efficiency, motor topology, and higher-layer counts remain experimental until measured.

## 1. Physical primitive

One CELL_V1 is one repeatable hex with six flat-edge directed interfaces in this clockwise order:

```text
A+ -> B+ -> C+ -> A- -> B- -> C-
```

The physical mirror pairs are:

```text
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

This is **three physical bidirectional mirrors**, not six separate physical gates.

Views/state/relation travel **UP** and Actions/conditioning/Override travel **DOWN** through the same three mirrors.

## 2. The active path is the memory and the process

CELL_V1 does not use the conventional primitive:

```text
processor -> separate memory -> processor
```

The target primitive is:

```text
current path state affects current flow
 -> current flow changes that same path state
 -> changed state remains locally available
 -> next traversal encounters the changed path
```

Therefore:

```text
state = memory
state transition = processing
repeated state transition = path training / muscle-memory analogue
```

A memristive, hysteretic magnetic, spintronic/magnetoresistive, phase-retaining, or other stateful carrier may be tested. No named device is assumed to satisfy the architecture until write, retain, read, rewrite, repeated-path training, and propagation are measured.

## 3. Repeated paths create muscle-memory behaviour

The build must test whether repeated successful traversal of the same route physically biases that route for future use.

Target behaviour:

```text
route selected
 -> route is traversed
 -> same active stateful path changes slightly
 -> successful repetition accumulates the change
 -> later traversal requires less intervention
 -> trained route becomes faster / lower-threshold / lower-drive / more persistent
```

At least one physical training metric must change reproducibly with repetition, for example:

- lower activation threshold;
- lower required drive energy;
- shorter decision/settling latency;
- greater retained conductance or magnetic/phase bias;
- greater probability of the same route winning under the same differential;
- fewer higher-level Override events for the same repeated task.

A software counter by itself is **not** muscle memory. If the stateful path is reset and the trained advantage disappears, that is acceptable evidence that the path carried the training. If the hardware path is unchanged and only software remembers the repetition, the physical muscle-memory requirement has not been met.

The build must also characterize unlearning/correction:

```text
unused path -> relaxes or remains bounded
failed/strained path -> is not blindly reinforced
higher Override -> can weaken, reverse, or redirect the learned bias
```

The exact reinforcement and decay law is experimental and must be derived from measurements rather than chosen because it looks biologically convenient.

## 4. Nerve-level energy and command flow

The current nerve-level physical sequence is:

```text
DC POWER / RECOVERY / REINJECTION
            |
            v
three bidirectional A/B/C mirrors
            |
            v
AC / recurring alternating path behaviour
            |
            v
TERNARY local command
DOWN / HOLD / UP
            |
            v
STATEFUL PATH TRANSITION
(processing + memory + training)
            |
            +---- within local limits ----> recover/reinject locally through DC loop
            |
            +---- strained/out of limits -> Views UP -> higher resolution
                                               |
                                               v
                                      Actions / Override DOWN
                                      through the SAME mirrors
                                               |
                                               v
                                         new local state
```

`V0` / the electrical center is a reference. It is not the recovery reservoir and must not be used as a power dump.

Returned inductive/magnetic energy is steered into a measured DC-link/reinjection reservoir and deliberately reused in a later permitted event.

## 5. Binary, ternary, quadratic roles

Keep the roles separate without multiplying hardware gates.

### Binary nerve relation

At nerve level the binary supervisory outcome is a two-way relation such as:

```text
LOCAL CONTINUE / REINJECT
        vs
ESCALATE / REQUEST HIGHER INTERVENTION
```

The physical threshold for that choice must be measured. Resource strain may include voltage margin, current, temperature, energy-reservoir state, unresolved oscillation, path conflict, or another explicitly instrumented variable. Do not invent an invisible `resource` scalar.

### Ternary local movement and motor command

```text
DOWN
HOLD
UP
```

The same ternary relation is the candidate local motor/actuator command grammar:

```text
one direction
balanced active HOLD
opposite direction
```

HOLD is an active balanced state, not a missing command.

### Quadratic routing

Views travel upward:

```text
Direction
Phase
Strength
Reference
```

Actions/conditioning travel downward through the same three mirrors. Higher-order action-mode names may describe the result, but they do not create another physical gate set.

## 6. Bidirectional nerve gates

Each A/B/C connection must support the intended bidirectional path:

```text
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

Back-to-back MOSFETs or another true bidirectional switch are candidates where a single MOSFET body diode would defeat blocking in one direction.

SiC MOSFETs remain candidates for later nerve/power domains where their switching, thermal, endurance, or power properties are useful. They are not assumed to directly resolve millivolt/microvolt information states; required gate-drive circuitry must be explicit and measured.

The nerve switch is connection hardware unless experiment shows that the same physical element also supplies the required retained processing state.

## 7. AC, rotation, and motor coupling

DC supplies and recovers energy. Switching/recurrence produces the AC behaviour. Phase-coordinated A/B/C activity may then be tested for a rotating magnetic/electromagnetic result.

Do not use `RC` as engineering shorthand for rotation because `RC` conventionally means resistor-capacitor. Use:

```text
DC -> AC -> ROTATION
```

or, when specifically measured:

```text
DC -> AC -> RMF (rotating magnetic field)
```

A rotating-field claim requires phase-resolved measurement. A motor turning does not by itself prove the intended internal route logic or memory.

## 8. Scaling contract

The same primitive must recurse:

```text
Point -> Path -> Rotation -> Field -> Volume -> next-scale Point
```

Physical scale ladder:

```text
ONE CELL_V1 HEX
 -> identical edge-to-edge cells
 -> multi-cell path
 -> closed rotation
 -> seven-cell flower
 -> coupled flowers / field
 -> 3D volume
 -> resolved volume exposed as next-scale point
```

All seven cells in a flower use the same orientation and connect flat-edge to flat-edge.

## 9. Current layer candidates — test, do not canonize

The following are retained as explicit experiments because they may map useful control depth, but none is proven merely by numerical symmetry:

```text
NERVE candidate:
2 flowers = normal + inverted / mirrored pair

M4 candidate:
2 + 2 flowers or resolved flower-volumes
= four-layer volumetric test for Views UP / Actions DOWN separation

HIGHER-BRAIN candidate:
3 / 3 / 3 volumetric expansion
and/or 3 x 3 x 3 lower-scale units

HEMISPHERE candidate:
a resolved higher-brain volume paired with a mirror-flipped counterpart
```

For every added layer, record what new measurable function appears. If adding the layer produces no new stable function, reject the count instead of preserving it for symmetry.

## 10. Build sequence

### Rev 0 — reference and DC energy loop

Prove the low-voltage supply/reference and recovery reservoir independently.

Measure:

- supply current/voltage;
- `V0` drift under unequal load;
- reservoir voltage;
- energy sent into a controlled inductive event;
- energy recovered;
- energy deliberately reused;
- losses and heating.

### Rev A — one bidirectional stateful axis

Build only A:

```text
A+ <-> [stateful path + bidirectional connection] <-> A-
```

Prove opposite-direction traversal, write/state change, retention, read with acceptable disturbance, rewrite, and that old state changes the next standardized response.

### Rev B — repeated-path muscle-memory test

Train the same A-axis route with a fixed pulse/task sequence.

Record trial-by-trial:

```text
threshold
drive energy
latency
state readback
path conductance / magnetic / phase observable
recovered energy
error/failed traversal
```

Then compare trained vs untrained/reversed route under identical conditions.

Pass condition: repeated traversal produces a reproducible physical path bias that changes later behaviour and survives long enough to matter for the next cycles.

### Rev C — three bidirectional mirrors

Replicate the proven primitive as A, B, C without changing its rules.

Verify all three pairs and the clockwise edge layout.

### Rev D — ternary local control

Demonstrate:

```text
DOWN / HOLD / UP
```

as three distinguishable local outcomes around the reference while preserving the retained path state.

### Rev E — binary local reinjection vs escalation

Define measured strain limits. Show that ordinary events close locally through recovery/reinjection, while an out-of-limit event produces an upward View/request instead of blindly repeating the path.

### Rev F — quadratic Views UP / Actions DOWN

Reconstruct Direction / Phase / Strength / Reference from measurements, send the relation upward, apply a downward conditioning/Override, and verify that the same A/B/C mirrors carry the return direction and leave a new local state.

### Rev G — motor/actuator analogue

Attach a safe instrumented load or small actuator only after Rev D-F work with dummy loads.

Test ternary command mapping:

```text
DOWN -> one direction
HOLD -> balanced/rest state
UP   -> opposite direction
```

Measure torque/position/current/phase as appropriate and verify that trained paths can reduce supervisory intervention without bypassing safety limits.

### Rev H — two/three-cell path

Connect identical cells edge-to-edge. Measure propagation loss, delay/phase, reference disturbance, crosstalk, retained-state disturbance, and whether repeated multi-cell routes train as a path rather than only as isolated local memories.

### Rev I — closed rotation

Distinguish traveling/circulating state from simultaneous switching, ringing, or standing oscillation. Test deliberate reversal.

### Rev J — seven-cell flower

Build one center + six identical surrounding cells. Test local training, competing paths, retained history, and whole-flower route reuse.

### Rev K — two-flower normal/inverted candidate

Test whether a paired normal/mirrored flower produces a useful new nerve-level function such as faster local correction, reciprocal checking, or stable reinjection. Reject the pair if it adds only duplicate hardware.

### Rev L — paired sensor-flower / motor-flower candidate

Test two coupled seven-cell flowers with distinct current roles while preserving identical CELL_V1 primitives:

```text
SENSOR FLOWER
  Views UP
  Field / Void sensory relation
  three opposed A/B/C differential pairs
        ⇅
SHARED BUS-LATTICE COUPLING
        ⇅
MOTOR FLOWER
  Actions DOWN
  Field / Void action relation
  ternary DOWN / HOLD / UP
```

The pair must be rejected if it only duplicates hardware or if the shared coupling destroys per-axis observability, retained path state, or reference stability.

The shared bus-lattice is a candidate coupling layer, not V0 and not automatically the reinjection reservoir.

Pass conditions:

1. a known sensor-side differential produces the expected signed View relation;
2. the relation reaches the motor-side flower without erasing A/B/C direction;
3. the motor-side flower produces the commanded ternary response;
4. the resulting body/actuator change is re-sensed and closes the loop;
5. Field and Void remain relational roles on both sides rather than separate hardware species;
6. the same cell primitive can exchange role in a control experiment.

### Rev M — short-term versus long-term physical memory

Test two retention bands in the active processing path family:

```text
SHORT-TERM:
  transient phase / charge / current / magnetic / impedance state
  measurable decay toward baseline

LONG-TERM:
  hysteretic / remanent / repetition-trained path bias
  measurable retention after drive removal
```

Required measurements:

- fast-state decay constant or decay curve;
- long-retention curve;
- train / rest / probe / reverse sequence;
- whether transient state can change without destroying the trained path bias;
- whether trained path bias alters later threshold, energy, latency, or route preference;
- control condition with training absent.

Do not promote "short-term" or "long-term" memory from naming alone. Each must have a declared observable and retention interval.

### Rev N — 2+2 M4 candidate

Test four coupled flower/volume layers as a candidate fast routing layer. The specific target is whether upward Views and downward Actions can coexist with lower latency or better isolation than the paired sensor/motor build.

### Rev M — 3/3/3 higher-brain candidate

Only after smaller layers pass, test 3/3/3 and/or 3 x 3 x 3 volumetric recurrence. Require a measurable increase in relational capacity, reconstruction, conflict resolution, or control depth rather than a count-based claim.

### Rev N — mirrored hemisphere candidate

Pair a resolved volume with a mirror-flipped counterpart only after the lower volume has stable state, trained paths, upward Views, downward Actions, and measured reinjection.

## 11. Mandatory muscle-memory receipts

Every training experiment records:

```text
test_id
cell_id / axis / route
trial_number
pre-state
command / pulse
threshold
voltage / current
energy in
energy recovered
latency
phase
state readback after event
same-route next-trial response
error / strain event
higher intervention yes/no
post-state
time since previous traversal
temperature
PASS / FAIL
```

Muscle-memory claims require a training curve and a control condition. Compare at minimum:

```text
repeated trained route
vs
untrained or opposite route
```

and test whether the effect persists, saturates, decays, reverses, or causes harmful lock-in.

## 12. Failure conditions

Reject or revise a build if:

- connections move to hex corners;
- A/B/C cease to be three bidirectional mirrors;
- Views and Actions require separate physical gate species;
- memory can be removed from the active processing path with no effect;
- `V0` becomes the energy dump;
- recovered energy is claimed without an energy budget;
- repeated-path learning exists only in software bookkeeping;
- a trained path cannot be overridden when strain/error limits are crossed;
- HOLD collapses into simple power-off when the claimed function requires active balance;
- ternary motor control silently becomes a different control architecture;
- a higher layer is retained only because its count looks symmetric;
- motor motion is treated as proof of memory, rotation, or learning without the corresponding measurements.

## 13. First decisive hardware target

Do **not** start with the full flower or brain stack.

The smallest build that now tests the distinctive architecture is:

```text
ONE A+ <-> A- BIDIRECTIONAL AXIS
+
ONE ACTIVE STATEFUL PROCESSING-MEMORY PATH
+
MEASURED DC RECOVERY / REINJECTION
+
REPEATED-PATH TRAINING TEST
+
EXPLICIT STRAIN / OVERRIDE CONDITION
```

If that one axis cannot demonstrate state-dependent processing and repetition-dependent path bias, scaling it into flowers or brain layers will only multiply an unproven primitive.
