# CELL_V1 Build Packet

**Purpose:** current bench-to-lattice build packet for CELL_V1.

**Current architecture authority:**

1. `Nodes/Hardware/CELL_V1/CELL_V1_ANTI_DRIFT.md`
2. `Nodes/Archive/Updated/UPDATED_63_CELL_V1_STATEFUL_MUSCLE_MEMORY_BUILD.md` — historical design receipt, not current physical authority
3. `Nodes/Archive/Updated/UPDATED_62_CELL_V1_HEX_FIRST_INTERNALS_AND_SCALING.md` — historical design receipt
4. `Nodes/Architecture/ARCHITECTURE_POINT_PATH_FIELD_SCALE_RECURSION.md`
5. `Nodes/G-778_Build_Logic_Research_and_Reference_Validation_Standard.md`

**Status:** experimental physical build. The geometry and three-bidirectional-mirror contract are locked; the stateful carrier, path-training law, reinjection efficiency, motor topology, and brain-layer counts must be earned by measurement.

## 1. The build in one picture

```text
                     CELL_V1 HEX

              A+                 B+
                \               /
                 \             /
                  \           /
                   [ STATEFUL ]
          C- <----[ PROCESS / ]----> C+
                   [ MEMORY   ]
                  /     |     \
                 /      |      \
              B-        |        A-
                        |
                        | repeated successful traversal
                        v
                  PATH TRAINING
                 / muscle memory

PHYSICAL MIRRORS:
A+ <-> A-
B+ <-> B-
C+ <-> C-

SAME MIRRORS:
Views / state / relation  UP
Actions / conditioning   DOWN

ENERGY:
DC supply -> event -> recovery reservoir -> measured reinjection -> later event
               V0 = reference only, NOT the reservoir

LOCAL COMMAND:
TERNARY = DOWN / HOLD / UP
          also candidate motor/actuator grammar

LOCAL CONTROL:
within limits -> continue/recover/reinject locally
strained      -> Views UP -> higher resolution -> Action/Override DOWN
```

All six external interfaces are on **flat hex sides**, clockwise:

```text
A+ -> B+ -> C+ -> A- -> B- -> C-
```

No corner ports.

## 2. Hard physical rules

### Three bidirectional mirrors

CELL_V1 has exactly three physical bidirectional mirror axes:

```text
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

Six directed edges do not mean six separate physical gates. Legacy six-position logic may be used for receipts, but it does not create separate Mirror and Action hardware.

### Processing is memory

The active physical path must retain the state that affects the next traversal:

```text
current path state affects flow
 -> flow changes the same path state
 -> changed state remains
 -> next traversal encounters that state
```

If a separate memory block can be removed and the active path behaves identically, that separate block is not the CELL_V1 processing-memory primitive.

### Repetition makes the path

Muscle-memory behaviour means repeated successful use changes the physical path itself:

```text
same route repeats
 -> same stateful path is modified repeatedly
 -> later traversal becomes measurably easier / faster / stronger / more likely
```

Acceptable training observables include lower threshold, lower drive energy, shorter latency, larger retained bias, stronger route preference, or fewer higher-level interventions.

A software usage counter is not sufficient.

### DC handles nerve-level recovery and reinjection

DC is not discarded once AC behaviour begins. The nerve-level energy loop is:

```text
DC supply
 -> active event
 -> controlled recovery
 -> DC-link / reinjection reservoir
 -> measured later reuse
```

The center/reference `V0` is not the energy reservoir.

### Ternary controls local motion and motors

```text
DOWN
HOLD
UP
```

is the local ternary movement relation and the candidate motor/actuator command grammar. HOLD is an active balanced state where the implementation requires balance; it is not automatically equivalent to power-off.

### Quadratic views/actions share the mirrors

Views UP include:

```text
Direction
Phase
Strength
Reference
```

Actions / conditioning / Override travel DOWN through the **same A/B/C physical mirrors**.

## 3. Candidate physical implementation categories

Do not lock a device before it passes the measurements.

The active stateful path may be tested with:

- hysteretic magnetic structures;
- memristive/resistive-memory elements;
- spintronic or magnetoresistive structures;
- phase-retaining/oscillatory structures;
- another measured stateful element that both participates in the active path and retains useful history.

Bidirectional nerve connection may use back-to-back MOSFETs or another true bidirectional switch. SiC MOSFETs are candidates for later higher-power nerve/motor domains, but any gate-drive interface must be explicit; do not assume millivolt/microvolt state directly drives a SiC power gate.

## 4. Bench frame

Initial practical frame remains low voltage and current limited.

```text
Supply: nominal 5 V protected/current-limited source
Reference: separately buffered/measured center V0
Energy reservoir: separate DC-link / reinjection capacitor or equivalent
A/B/C: measured differential paths around V0
```

Do not reopen the retired +/-12 V CELL_V1 design unless a later measured requirement explicitly forces a different supply architecture.

## 5. Rev 0 — prove reference and reinjection separately

Before claiming learning or motor control, establish clean energy accounting.

Measure:

```text
V_supply
I_supply
V0 and drift
E_event_in
V_reservoir before/after
E_recovered
E_reused in later event
losses
temperature
```

Pass: returned energy is measurably collected and deliberately reused in a later permitted event.

Fail: apparent reinjection depends on reference-node motion, hidden source current, or unexplained gain.

## 6. Rev A — one A+ <-> A- stateful bidirectional path

Build one axis only:

```text
A+ <-> [true bidirectional connection]
   <-> [active stateful processing-memory path]
   <-> A-
```

Required proof:

1. traversal works in both intended directions;
2. a controlled event changes local physical state;
3. that state persists for a measured interval;
4. a later identical probe gives a different response because of the retained state;
5. the state can be rewritten/reversed;
6. recovery/reinjection remains separately measurable.

## 7. Rev B — muscle-memory training test

This is now a mandatory build gate.

Choose one standardized A-axis route/task. Repeat it without changing the hardware settings.

For every trial record:

```text
trial number
pre-state
command
threshold
latency
voltage/current
energy in
energy recovered
stateful-path observable
post-state
strain/error flag
higher intervention yes/no
time since previous trial
temperature
```

Compare:

```text
trained repeated route
vs
untrained/opposite/control route
```

Pass: repetition creates a reproducible physical path bias that changes later behaviour and persists long enough to affect subsequent cycles.

Also test:

- saturation;
- decay when unused;
- reversal/retraining;
- whether a failed/strained route is incorrectly reinforced;
- whether higher Override can redirect the trained path.

## 8. Rev C — duplicate the proven primitive into B and C

Only after A passes, reproduce the same mechanism for:

```text
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

Do not hide a weak B or C axis behind a good A result.

Required test points should expose reference, each axis electrical state, each axis stateful-memory observable, and the reinjection reservoir.

## 9. Rev D — ternary local decision and motor grammar

Demonstrate three distinguishable outcomes:

```text
DOWN
HOLD
UP
```

Then map the same relation to a safe dummy load or instrumented actuator:

```text
DOWN = one commanded direction
HOLD = balanced/resting local state
UP   = opposite commanded direction
```

Exact winding/motor implementation remains experimental. Measure current, phase, torque/position where applicable, and thermal behaviour.

## 10. Rev E — local automatic reinjection vs higher escalation

Define real measured strain variables; do not use a vague hidden `resource` value.

Candidate inputs include:

- voltage margin;
- current;
- reservoir energy;
- temperature;
- unresolved phase/oscillation;
- route conflict;
- repeated local failure.

Target behaviour:

```text
within limits
 -> local action settles
 -> energy recovered/reinjected through DC loop
 -> trained local path continues without higher intervention

outside limits
 -> local loop does not blindly repeat
 -> Views travel UP
 -> higher level resolves
 -> Action/Override travels DOWN through same mirror path
 -> new physical state remains
```

## 11. Rev F — AC and rotation

DC is the energy/recovery layer. Switching/recurrence produces AC behaviour.

When A/B/C phases are coordinated, test for actual rotation:

```text
DC -> AC -> ROTATION
```

or, if magnetic field is what is measured:

```text
DC -> AC -> RMF
```

Do not use `RC` for rotation in engineering documents because it normally means resistor-capacitor.

Distinguish:

- simultaneous switching;
- ringdown;
- standing oscillation;
- traveling/circulating phase/state;
- controlled reversal.

## 12. Rev G — path propagation and distributed training

Connect two identical CELL_V1 modules flat-edge to flat-edge, then three.

Measure:

- amplitude loss;
- phase/delay;
- noise;
- reference disturbance;
- crosstalk;
- local retained-state disturbance;
- whether repeated traversal trains the whole route or only one local cell.

A valid scalable path uses the same cell primitive at every position.

## 13. Rev H — seven-cell flower

Build one center + six surrounding identical CELL_V1 cells.

Rules:

- same orientation;
- flat-edge connections only;
- no adapters;
- each cell remains individually measurable.

Tests:

1. outer -> center;
2. center -> outer;
3. two-edge path through center;
4. perimeter/closed routes where geometry permits;
5. competing paths;
6. route repetition/training;
7. later whole-flower response after training;
8. local Override of a trained route.

## 14. Scaling experiments after the flower

The recurrence remains:

```text
Point -> Path -> Rotation -> Field -> Volume -> next-scale Point
```

Current explicit test candidates:

```text
NERVE:
2 flowers, normal + mirrored/inverted

M4:
2 + 2 flower/volume layers
candidate four-depth structure for fast Views-UP / Actions-DOWN routing

HIGHER BRAIN:
3 / 3 / 3 volumetric expansion
and/or 3 x 3 x 3 proven lower-scale units

HEMISPHERES:
resolved higher volume <-> mirror-flipped counterpart
```

These counts are **not canonized by symmetry**. Each added layer must demonstrate a new measurable function such as correction speed, isolation, reconstruction, conflict resolution, relational capacity, or stable control depth.

If a layer adds no useful measurable function, remove it.

## 15. Required muscle-memory acceptance curve

A serious muscle-memory claim needs more than before/after anecdotes.

For a fixed route, graph or tabulate across repeated trials:

```text
trial number -> activation threshold
trial number -> latency
trial number -> drive energy
trial number -> retained-state observable
trial number -> recovered energy
trial number -> intervention count
```

Then stop training and measure decay over time. Reverse/retrain the route and measure whether the bias can move rather than merely lock permanently.

The preferred result is bounded plasticity:

```text
useful repetition -> easier local reuse
strain/error      -> no blind reinforcement
Override          -> can redirect
inactivity        -> bounded persistence or measurable decay
```

## 16. Mandatory failure rules

Stop or revise if:

- any external connection moves to a hex corner;
- the build becomes six separate physical Mirror/Action gates;
- UP and DOWN require separate hardware path species instead of the same mirrors;
- memory is separate from the active processing path;
- the training effect exists only in software;
- `V0` carries recovery current as an energy reservoir;
- the energy budget implies unexplained gain;
- one-way body-diode conduction defeats the intended bidirectional gate;
- trained paths cannot be overridden under declared strain/error conditions;
- HOLD silently becomes off when active balance is required;
- a motor turning is used as proof of path memory or rotating field without those measurements;
- 2-flower, 2+2, 3/3/3, or 3x3x3 counts are promoted without a measured function.

## 17. Bench safety

- current-limit early prototypes;
- provide intentional inductive-energy return paths before switching coils;
- prevent MOSFET shoot-through;
- monitor MOSFET/stateful-element temperature;
- use differential/isolated probing where required;
- never let an oscilloscope ground clip short a floating node or V0;
- record winding polarity and switch orientation before changing connections;
- stop on unexpected heating or unstable oscillation.

## 18. Immediate first build

Do not start with the seven-cell flower.

The first decisive build is now:

```text
ONE A+ <-> A- BIDIRECTIONAL AXIS
+
ACTIVE STATEFUL PROCESSING-MEMORY PATH
+
MEASURED DC RECOVERY / REINJECTION
+
REPEATED-PATH MUSCLE-MEMORY TEST
+
MEASURED STRAIN / OVERRIDE CONDITION
```

Only after that works reproducibly do we copy it into B and C, then add ternary motor control, path propagation, rotation, flowers, and volumetric layers.


## 19. Real engineering / research reference floor

These references establish that the **component mechanisms** are real. They do not establish the combined CELL_V1 architecture.

### Midpoint/reference
Texas Instruments TLE2426 precision rail splitter:
https://www.ti.com/product/TLE2426

Use: low-current half-supply reference.  
Do not use: motor/coil return or energy reservoir.

### Three-phase motor baseline
Microchip six-step three-phase BLDC commutation:
https://onlinedocs.microchip.com/oxy/GUID-3AFF556D-77AD-488F-9A04-CD7AAB8F7DBC-en-US-1/GUID-A1DD3CA4-D59F-45CF-AA9F-EBBCB9EF37BA.html

Use: real comparison for three-phase switching, sector sequence, driver topology, current paths, and reversal.

### Fluxgate magnetic sensing
Review of fluxgate sensor structure and applications:
https://www.mdpi.com/1424-8220/21/4/1500

Use: precedent for excitation/core/sense magnetic measurement.

### Memristive stateful path
Hardware memristive neural-network review:
https://www.nature.com/articles/s41467-024-45670-9

Dynamical memristor review:
https://www.nature.com/articles/s41578-022-00434-z

Use: evidence that stateful resistive devices can combine storage and computation-like behavior.  
Not proof: CELL_V1 muscle memory or whole-cell learning.

### Magnetic/spintronic memory
STT-MRAM status:
https://www.nature.com/articles/s44287-024-00111-z

SOT-MRAM progress:
https://www.nature.com/articles/s44306-024-00044-1

Use: precedent for real nonvolatile spin-dependent memory.  
Not proof: ordinary Hall/coil feedback is spintronics.

### Historical multi-aperture ferrite memory
Transfluxor memory proceedings:
https://www.bitsavers.org/pdf/afips/1959-03_%2315.pdf

Use: historical precedent for remanent multi-aperture ferrite storage and nondestructive readout concepts.

## 20. Claim discipline

The following are currently **One-Wave hypotheses / experimental targets**, not established by the references above:
- one physical path simultaneously implementing processing, memory, muscle-memory training, and reinjection;
- three mirrored A/B/C axes scaling into the full proposed cell architecture;
- seven-cell flower producing a new functional field unit;
- volumetric 2/2, 3/3/3, or 3x3x3 brain-layer scaling;
- shared physical views-up/actions-down path beyond ordinary bidirectional sensing/control.

Each must earn promotion through the measured revision gates already defined in this packet.
