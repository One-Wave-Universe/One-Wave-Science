# Priority One — Ground-Referenced Recursive Cell Build Map

Date: 2026-09-15
Status: **authoritative build target; implementation stages require receipts**

This is the priority-one map for the physical and simulated cell. It replaces block-diagram descriptions that call themselves a build without giving an ordered construction and test path.

## 1. Locked identity

The target is a **ground-referenced, bidirectional recursive cell**. It creates or recognizes a difference, commits a direction, produces alternating motion, turns that motion into a rotating/quadratic relation, carries Views upward, receives Actions downward, and returns the completed consequence as the next starting condition.

The cell is not six independent machines. Reference, decision, movement, view/action, state, memory, rewrite, and reinjection must remain one coherent loop.

## 2. Locked physical geometry

The hexagon has **six side terminals, never corner connections**, but it has only **three whole state gates**. Each gate is one opposed `+/-` mirror pair operating together.

Clockwise terminal order:

```text
A+ -> B+ -> C+ -> A- -> B- -> C- -> A+
```

The three whole gates are the opposed mirror pairs across the center:

```text
Gate A = A+ <-> A-
Gate B = B+ <-> B-
Gate C = C+ <-> C-
```

The `+` and `-` terminals are not separate gates and are not six serial operations. In every whole gate flip, the `+` half carries the **new Field state upward** while the mirrored `-` half carries the **last Void/action state downward**. The gate resolves their live differential around virtual ground.

```text
                 ONE WHOLE STATE GATE

                    new Field UP
                         +
                         |
                 virtual ground / HOLD
                         |
                         -
                 last Void/action DOWN
```

The center is the cell's local virtual ground and HOLD reference. Neighbor-to-neighbor lattice travel crosses a side. Corners are not electrical terminals and must not appear as cell connections in drawings, netlists, board layouts, or simulations.

## 3. Virtual ground is the ternary center

```text
FIELD / UP       virtual ground / HOLD       VOID / DOWN
    +                         0                         -
```

Virtual ground is not an after-the-fact classifier and not an optional telemetry reference. It is the physical center condition that makes `UP / HOLD / DOWN` possible.

Bench law:

- prove the center under symmetric and asymmetric loading;
- measure its displacement under every transition;
- do not call a passive sagging midpoint a working virtual ground;
- do not use the center conductor as an uncontrolled high-current return;
- every state receipt is signed relative to this same local center.

## 4. Three-gate dependency order

```text
Gate A: DC whole-state flip
 -> Gate B: AC whole-state flip
 -> Gate C: RC/quadratic whole-state flip
 -> whole-cell reinjection
```

This is a three-layer dependency, not a six-step conveyor. Within every gate, the new upward Field condition and the last downward Void/action condition coexist and resolve as one whole state flip.

### Gate A — BC/DC whole-state flip

`A+` carries the new binary Field engagement upward. `A-` simultaneously carries the last binary Void disposition downward. Their differential around virtual ground resolves engagement against the last accept/override consequence.

Receipt: selected sign, voltage from virtual ground, current, direction, and unselected-side leakage.

### Gate B — TC/AC whole-state flip

`B+` carries the new ternary Field movement upward. `B-` simultaneously carries the last ternary Void regulation downward. Their mirrored relation alternates through the live center:

```text
+ -> 0 -> - -> 0 -> +
```

The ternary movement is:

```text
UP / HOLD / DOWN
```

HOLD is a live return to virtual ground, not a deleted oscillator and not a fourth state.

Receipt: phase, amplitude, center crossings, UP/HOLD/DOWN decision, and reversal timing.

### Gate C — QC/RC quadratic whole-state flip

`C+` carries the new quadratic Field View upward. `C-` simultaneously carries the last quadratic Void Action downward. Together they resolve the rotating relationship. Magnetic feedback begins here, **after** the DC and AC dependencies.

The new half of the quadratic state is upward:

```text
Direction / Phase / Strength / Reference -> Views UP
```

The last-action mirror of the same quadratic state is downward:

```text
Inward / Outward / Across / Over -> Actions DOWN
```

Receipt: rotation handedness, phase relationship, field vector, strength, reference, selected View, returned Action, and the measured differential between commanded and actual result.

## 5. Whole-cell mirror and reinjection

Reinjection is not a raw output wire and not a copy of only the C stage. The completed three-gate consequence is mirrored as a whole and returned to the same local virtual-ground comparison that begins the next cycle.

```text
Gate A = new binary Field UP    + last binary Void/action DOWN
Gate B = new ternary Field UP   + last ternary Void/action DOWN
Gate C = new quadratic View UP  + last quadratic Action DOWN
```

```text
new cue
  +
previous whole-cell consequence
  -> next DC starting condition
```

The reinjection path must preserve sign, direction, phase, strength, reference, route address, and timing. Its gain must be bounded and measurable so the loop can reinforce a valid path without uncontrolled runaway.

## 6. Muscle memory and rewrite

Muscle memory is **structural, path-specific hardware learning**. It is not biological muscle and not merely a magnetic latch retaining one state.

Each used side-to-side lattice edge must have a bidirectional, rewritable impedance state. A physical implementation may use a memristive device, characterized memristor emulator, magnetoresistive/spintronic candidate, or another measured nonvolatile adaptive element. No candidate is accepted merely because its name sounds compatible.

Required behavior:

| Event | Required local change |
|---|---|
| First novel traversal | Default impedance; complete path receipt recorded |
| Repeated same vector | Impedance progressively decreases on that exact traversed path |
| Matching cue | Reinforced path wins locally with less drive and/or latency |
| Competing vector | Competing path can be strengthened without silently erasing unrelated paths |
| Rewrite | Selected old path weakens while the replacement path strengthens |
| Release/forget | Conductance returns toward a declared baseline under a measured rule |

The reinforced route is an `L1`/taxicab-style sequence of **side crossings** through addressed hex cells. The coordinate convention and distance receipt must be declared before scaling; regardless of coordinate notation, no corner hop is permitted.

Recall is reconstruction:

```text
cue down the spine
 -> reinforced low-impedance route reopens
 -> cells rebuild their local DC/AC/RC conditions
 -> complete operational state is reconstructed
 -> local reflex can execute without step-by-step Administrator control
```

Rewrite must be physically testable. A memory device that can only strengthen, saturate, or be globally erased does not meet the cell requirement.

## 7. Memory layers that must remain distinct

```text
HOLD          current cycle remains at/around virtual ground
state memory  completed quadratic condition remains available
muscle memory repeated multi-cell route changes future conductance
rewrite       learned route is selectively changed
reinjection   completed consequence becomes next-cycle starting context
```

Combining these in one physical device is allowed only if separate tests can still distinguish all five jobs.

## 8. Priority-one construction sequence

### Build 0 — simulator capability gate

The Virtual Breadboard must demonstrate:

- stiff virtual ground with source/sink limits;
- bilateral switch behavior including body-diode paths;
- controlled DC polarity about center;
- AC center crossings and phase receipts;
- coupled windings / multidimensional field receipts;
- a bounded whole-cell feedback path;
- a stateful edge whose conductance can reinforce, hold, weaken, and rewrite.

Hard stop: do not claim a cell build from static state labels alone.

### Build 1 — Gate A, one A+/A- DC whole-state pair

Wire one opposed bidirectional pair about a loaded virtual ground. Prove positive, HOLD, negative, reversal, leakage, and center recovery.

Hard stop: no AC until the center survives unequal load and reversal without losing its reference.

### Build 2 — add Gate B, the B+/B- mirrored AC whole-state pair

Close the out-and-back path through virtual ground. Prove both starting directions, repeatable center crossings, UP/HOLD/DOWN, frequency, phase, and break-before-reverse behavior.

Hard stop: no rotating-field claim from one merely oscillating channel.

### Build 3 — add Gate C, the C+/C- RC/quadratic whole-state pair

Drive a measured orthogonal or multiphase magnetic arrangement. Reconstruct the actual resultant field from sensors; do not infer rotation from LED order or a drawing.

Hard stop: no quadratic pass until handedness, phase, strength, reference, and rotation survive measurement.

### Build 4 — prove Views UP and Actions DOWN

Send Direction/Phase/Strength/Reference upward. Return one chosen Inward/Outward/Across/Over action through the mirrored downward path. Compare commanded and actual consequence.

Hard stop: the downward command must not bypass the local ternary reflex or directly force an unsafe bridge state.

### Build 5 — close bounded whole-cell reinjection

Return the complete measured consequence to the next DC comparison. Sweep reinjection gain from zero upward while logging decay, stable recurrence, oscillation, and runaway boundaries.

Hard stop: reinjection must be switchable off and must fail safely.

### Build 6 — install one rewritable muscle-memory edge

Measure resistance/conductance and response latency before training, through repeated identical traversals, after hold, after competing training, after selective rewrite, and after release/forget.

Hard stop: reinforcement without selective rewrite is incomplete.

### Build 7 — seven-cell side-connected lattice

Connect one center cell to six neighbors through their sides. Train one multi-cell route, cue it from a partial input, and test whether the route reconstructs without corner shortcuts or central step replay.

Hard stop: demonstrate route specificity against at least one equal-length competing path.

## 9. Required receipts

Every simulated and physical run records:

```text
cell IDs and side addresses
virtual-ground voltage and source/sink current
A/B/C pair states
signed differential from virtual ground
AC phase and center crossings
rotation vector and handedness
View sent upward
Action returned downward
pre/post reinjection state
edge conductance before and after traversal
rewrite target and measured change
path sequence and path length
temperature and supply current
PASS / FAIL against a declared tolerance
```

## 10. What is locked versus still unresolved

Locked:

- side connections, not corners;
- six side terminals but only three whole state gates;
- clockwise terminals `A+ B+ C+ A- B- C-`, paired as `A+/A-`, `B+/B-`, and `C+/C-`;
- every gate flip combines new Field UP with last Void/action DOWN;
- virtual ground is ternary HOLD/zero;
- three-gate `DC -> AC -> RC` dependency;
- quadratic Views UP and mirrored last Actions DOWN are two directions of Gate C, not separate gates;
- whole-cell reinjection;
- muscle memory as path-specific impedance reinforcement;
- selective rewrite capability;
- local cue-driven reconstruction and reflex execution.

Still requires engineering selection and receipts:

- exact virtual-ground power hardware for each current scale;
- switch, comparator, driver, winding, sensor, and protection parts;
- timing and phase values;
- safe reinjection gain window;
- memristive/magnetoresistive device technology;
- learning, decay, rewrite, and saturation curves;
- coordinate/address encoding for the larger 3D lattice.

Until those are selected and tested, diagrams are topology maps—not finished breadboard wiring.
