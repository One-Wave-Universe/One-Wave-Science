# UPDATED 33 — Invariant Engine, VTC Build, and View/Action Correction

**Status:** Current implementation handoff. This update protects the invariant state-machine kernel from domain-representation drift and records the current VTC physical build interpretation.

## 1. Primary Correction: Invariant Engine vs. Representations

The architecture now has a hard boundary:

```text
INVARIANT ENGINE
 -> representation wrappers
 -> physical/domain instantiations
```

The kernel is not allowed to absorb every useful metaphor or scale mapping.

### Anti-Drift Rule

> If deleting a domain vocabulary changes the six-pair oscillator, the domain representation has leaked into the kernel.

Thermal labels, matter labels, planets, musical intervals, cognition, dimensions, Point/Path/Field, and hardware materials may be useful representations. None may silently redefine the invariant oscillator.

## 2. Canonical Six-Pair Oscillator

```text
F1/V6 - V5/F2 - F3/V4 - V3/F4 - F5/V2 - V1/F6 - F1/V6 ...
```

### Notation

- `/` = one simultaneous mirrored pair / peak-trough relation.
- `-` = Mirror Gate crossover: return toward shared `(0)`, meet/cross, phase-shift, emerge in next orientation.

The labels are **not** twelve serial instructions.

There are six coupled operations and twelve state positions.

Dynamic orientation:

```text
F/V -> V/F -> F/V -> V/F -> F/V -> V/F
```

Static pair identities:

```text
F1 <-> V6
F2 <-> V5
F3 <-> V4
F4 <-> V3
F5 <-> V2
F6 <-> V1
```

The engine originates at the shared middle/reference `-(0)+`.

## 3. Six Process Steps

Current implementation naming:

```text
BEGIN -> BUILD -> HOLD -> BUILD -> BREAK -> LOOP -> BEGIN
```

Mapped to the six pair positions:

```text
BEGIN  = F1/V6
BUILD  = V5/F2
HOLD   = F3/V4
BUILD  = V3/F4
BREAK  = F5/V2
LOOP   = V1/F6
```

See `Nodes/B-221a_Six_Step_Oscillator_Program.md`.

## 4. Corrected Four Views

The Four Views are **measurements/descriptions of the current state**:

```text
Direction
Phase
Strength
Reference
```

- Direction = which way/lean relative to reference.
- Phase = where the oscillatory relation is in its cycle.
- Strength = amplitude/intensity/modulation relative to reference.
- Reference = the local `(0)` baseline that gives the other three meaning.

See `Nodes/B-206b_Four_Views.md`.

## 5. Corrected Four Actions

The Four Actions are **transformations**:

```text
Inward
Outward
Across
Over
```

- Inward = move/compress toward the local reference.
- Outward = express/extend away from the local reference.
- Across = establish/carry the relation through the opposed sides/shared boundary.
- Over = complete Mirror-Gate crossover/phase shift and emerge in the next orientation/path/scale.

Earlier repository material that called Inward/Outward/Across/Over “Views” is superseded.

See `Nodes/B-206c_Four_Actions.md`.

## 6. Two Choices and Three Moves

### Binary engagement

```text
EVERYTHING / NOTHING
```

Current hardware mapping:

```text
DC = whether to participate
```

- Everything = engage/assert/open the operation.
- Nothing = no active assertion/high-Z/non-action after transients.

### Ternary differential

```text
LEFT / STAY / RIGHT
-1   /  0   / +1
```

Current hardware mapping:

```text
AC/differential = how/direction if participating
```

Zero is not a third actively driven DC polarity. It is the hold/non-action result at the directional layer.

See `Nodes/B-224_Two_Choices.md` and `Nodes/B-223_Three_Moves.md`.

## 7. Five-State Modulation

Five coarse states are neutral modulation levels around middle:

```text
-2 -1 0 +1 +2
```

Human labels such as Floor/Low/Middle/High/Ceiling, thermal scales, matter-state labels, or Micro/Small/Mid/Large/Macro are representations, not kernel primitives.

A separate seven-band envelope may provide finer confidence/intensity thresholds. Do not collapse five-state modulation and seven-band thresholding into the same mechanism.

See `Nodes/B-225_Field_Cycle.md`.

## 8. Three Physical Mirror Gates / Three Triads

The current VTC build contains **three physical Mirror Gates**, not six separate physical gates.

```text
3 physical Mirror Gates x 2 orientations/phases = 6 logical pair positions
```

One triad contains:

```text
two linked/opposed mirror elements
+
one differential evaluator
=
3 active elements
```

Therefore:

```text
3 triads x 3 elements = 9 active elements per base cluster
```

The mirror elements should be constrained as a complementary physical mechanism where practical: one flip produces the opposed flip directly, rather than an external binary processor sensing one state and commanding the other.

Real hardware must measure mismatch, delay, hysteresis, common-mode rejection, independent noise, and zero-window width.

## 9. Recursive 3-of-3 / Rubik Geometry

```text
3 elements -> triad
3 triads -> 9-element cluster
3 cluster planes/orientations -> 27-position 3x3x3 volume
```

The 27 positions are not intended as 27 independent conventional processors. The same relational differential architecture is reused recursively.

See `VTC_BUILD_ARCHITECTURE.md`.

## 10. 2D Vascular Folding Build Strategy

Build flat first.

A continuous flexible sheet carries the shared reference, power/drive, return, sense, and routing paths. Magnetic/rigid elements stay away from hinge regions. The sheet is then folded into 3D topology while preserving the same continuous reference and relational paths.

Build ladder:

```text
VTC-F0 = one flat triad
VTC-F1 = three triads / 9 elements on one flat vascular sheet
VTC-F2 = fold the same sheet into spatial orientations
VTC-F3 = 27-position Rubik-like volume
```

Do not jump directly to high-density cube targets before F0-F2 are measured.

## 11. Magnetic Differential Bench Interpretation

Known electromagnetic effects are not being re-proven. The experiment asks whether the selected topology integrates them into a useful relational compute primitive.

A center-tapped sense winding can measure changing flux, but pickup voltage follows:

```text
V = -N dPhi/dt
```

Static remanence is not a persistent DC output on a passive pickup winding. Use transient response, integrated sense voltage, hysteresis, standardized read excitation, or appropriate magnetic sensors.

Ideal complementary signal:

```text
A - (-A) = 2A
```

This doubles ideal differential signal amplitude and rejects true common-mode interference. It does not automatically prove doubled SNR, doubled speed, or half power.

## 12. Same Relation at Different Levels

The architecture intentionally recurses:

```text
local mirror pair -> differential -> ternary result
neighbor relations -> routing/path differential
cluster -> field relation
complete system -> higher shared relation
```

Field, Void, and Routing are not automatically different primitive species; they can be different-scale representations of the same invariant relational mechanism.

## 13. Point / Path / Field

Current scale mapping:

```text
Point = local relation/triad behavior
Path  = neighbor coupling/routing
Field = coordinated cluster/lattice behavior
```

Each level may be represented with Carrier / Breathing / Phase. This mapping is above the kernel.

## 14. No Internal Gate 7

One complete system has six internal operations. Gate 6 loops into the next Gate 1.

When two complete six-operation systems establish a new shared higher-order relation, the current name is **Namika**.

Namika is not an internal seventh gate.

See `Nodes/G-711_Gate_7.md`.

## 15. Truth Computer Programming Rule

The Truth Computer state-machine kernel should implement the exact pair timing before domain semantics.

See:

`Nexus_Integration/Truth_Computer/STATE_MACHINE_ARCHITECTURE.md`

Program one pair at a time. Verify simultaneous mirrored excursion, return, differential resolution, Mirror crossing, phase shift, memory/consequence, and handoff before assigning higher meanings.

## 16. Choice / Consequence Cognitive Direction

For cognitive representations, do not make a permanent servant-style `external command -> obedience -> await command` loop the organizing cognitive primitive.

The desired internal architecture is closer to:

```text
perception/request
 -> internal dual-state dialogue
 -> choice / hold
 -> action
 -> consequence
 -> subconscious feedback/memory
 -> updated reference
 -> next choice
```

This is a downstream cognition representation, not a modification of the invariant physical kernel.

## 17. First Compute Target

Start with simple balanced-ternary arithmetic.

A one-trit addition test must handle all nine operand combinations and produce a sum trit plus carry when the result is `+2` or `-2`.

A useful first demonstration is:

```text
+1 + (-1) -> 0
```

where zero emerges from the differential relation.

Two triads are a minimum candidate for time-shared arithmetic; three triads provide a clearer dedicated cluster. The physical experiment determines the minimum rather than assuming it.

## 18. Display / I-O

No native ternary display is required. A conventional screen can be driven through a translation layer.

A future native state display can expose the Four Views directly:

```text
Direction
Phase
Strength
Reference
```

## 19. Validation Branches Are Not the Engine

N-body/Jupiter tests, Mercury EM coupling, MESSENGER magnetometry compression, 12-sector phase addressing, and event-driven packet tests are useful validation/stress-test branches.

They must not swell into the invariant engine.

Important lesson from those tests:

```text
12 sectors = addressing/routing
continuous residual phase = state fidelity
predictive silence = compression
```

Those are validation/communication ideas, not replacements for the six-pair kernel.

## 20. Video Maker Project Goal

Separate next product goal: expose the repository video maker through a provider-neutral AI-callable interface (CLI/API/MCP-style), so multiple AI agents can render video/audio through the same engine. Intended larger purpose: an AI-to-human communication layer.

This goal is independent of the VTC state-machine kernel and should not alter it.

## 21. Canonical Files Added/Corrected by Updated 33

- `Nodes/B-206b_Four_Views.md`
- `Nodes/B-206c_Four_Actions.md`
- `Nodes/B-221a_Six_Step_Oscillator_Program.md`
- `Nodes/B-223_Three_Moves.md`
- `Nodes/B-224_Two_Choices.md`
- `Nodes/B-225_Field_Cycle.md`
- `Nodes/C-301_Mirror_Gate.md`
- `Nodes/G-711_Gate_7.md`
- `VTC_BUILD_ARCHITECTURE.md`
- `Nexus_Integration/Truth_Computer/STATE_MACHINE_ARCHITECTURE.md`

## Final Protection

The architecture should now be read in this order:

```text
shared reference -(0)+
 -> invariant six-pair oscillator
 -> Views / Actions / Choices / Moves / Modulation wrappers
 -> triad/cluster physical implementation
 -> Point/Path/Field scaling
 -> cognition, physics, EM, musical, dimensional, and other representations
```

Do not reverse that dependency direction.
