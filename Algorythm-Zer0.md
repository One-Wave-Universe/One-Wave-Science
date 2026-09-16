# Algorythm-Zer0 — Full Primitive Base

**Status:** Restored full primitive base. This file owns the primitive logic, reference rules, threshold/readout rules, mirror/action recurrence, and the boundaries between axes. Domain mappings belong elsewhere.

**Authority rule:** newer executable/current corrections override older descriptive shorthand when they conflict. Matching counts never imply that two axes are the same thing.

**Important correction:** the idea that “2 contains 1, 3 contains 2 and 1, and so on” is a useful recursion/packing guide. It is **not the primitive definition** and must not replace the independent structures below.

---

# 0. FIELD / VOID / GROUND — THE REFERENCED PAIR

The base relation is:

```text
FIELD
  ↕
GROUND / REFERENCE
  ↕
VOID
```

Compact relational notation:

```text
1 > (0) < 1
```

Primitive rules:

- Field and Void are counterpart roles in one referenced process.
- Ground/reference is an active comparison baseline, not dead nothing.
- Ground is **not** a third committed binary choice.
- Field carries proposal/new relation/expression.
- Void carries checking/constraint/confirmation/override/action.
- Field and Void may differ in phase while remaining one coupled process.
- Mirror does not mean “swap YES and NO” and does not exchange Field and Void identities.
- The resulting state is retained; returning through the cycle is not an automatic reset to the prior state.

A complete primitive state must keep reference separate from commitment, movement, phase, and strength.

---

# 1. BINARY CHOICE — WHAT COUNTS AS CHOICE

Current executable authority defines exactly two committed binary choices:

```text
(1,0) = YES / AGREE
(0,1) = NO  / DISAGREE
```

Separate non-choice conditions:

```text
(0,0) = GROUND / NO COMMITTED BINARY CHOICE
(1,1) = CONFLICTING DUAL ASSERTION — invalid unless explicitly used diagnostically
```

Therefore:

```text
B2 = {(1,0),(0,1)}
```

contains exactly two committed binary choices.

A **Choice** is not just a threshold crossing or a label. For Algorythm-Zer0, Choice means:

```text
1. a current Field exposes a live alternative;
2. the alternatives are interpreted against the current Ground/reference;
3. one valid binary relation is committed: YES or NO;
4. that commitment participates in action/non-action;
5. a measurable consequence/readout can update retained state/reference;
6. the changed state participates in the next Field of choices.
```

So:

```text
FIELD OF AVAILABLE RELATIONS
→ CHOICE: YES / NO
→ ACTION / NON-ACTION
→ CONSEQUENCE
→ MEMORY / REFERENCE UPDATE
→ NEXT FIELD OF AVAILABLE RELATIONS
↺
```

Choice is meaningful only in relation to consequence and the next referenced state.

### Engagement interpretation

Older/current implementation language also uses:

```text
EVERYTHING = engage / assert / open the operation
NOTHING    = do not engage / preserve / high-Z where physically appropriate
```

This is an engagement interpretation of the binary layer. Current executable route authority uses YES/NO.

### Express / Compress boundary

`EXPRESS / COMPRESS` must not silently replace the two-choice finite address space. Express/Compress is a Field/Void relational polarity/behavior vocabulary used by higher routing/domain layers. The exact relationship between that vocabulary and YES/NO must be declared by the implementation.

---

# 2. TERNARY MOVEMENT — DIFFERENTIAL AROUND THE REFERENCE

The primitive movement result has exactly three positions:

```text
-1 = DOWN / LEFT / one orientation
 0 = HOLD / STAY
+1 = UP / RIGHT / opposite orientation
```

Left/Right, Down/Up, Compress/Expand, CCW/CW, and similar names are domain orientations. The invariant part is signed movement around an active reference with a real middle Hold.

For measured differential `Delta` and a declared zero window `epsilon`:

```text
Delta < -epsilon     -> -1
|Delta| <= epsilon   ->  0
Delta > +epsilon     -> +1
```

Primitive rules:

- `0` is a real active Hold result, not a third binary choice.
- exact `epsilon` is implementation-calibrated.
- a fast crossing through center is not automatically Hold.
- a turning point can be movement-Hold while away from center.
- signed movement is separate from the Four Action modes.

---

# 3. SIX ROUTE ADDRESSES — 2 CHOICES × 3 MOVES

The finite route space is:

```text
L6 = B2 × T3
```

with exactly six committed route addresses.

The executable dense addresses are:

```text
0 = NO / DOWN
1 = NO / HOLD
2 = NO / UP
3 = YES / DOWN
4 = YES / HOLD
5 = YES / UP
```

Equivalent unordered listing:

```text
YES/DOWN, YES/HOLD, YES/UP,
NO/DOWN,  NO/HOLD,  NO/UP
```

Rules:

- Ground `(0,0)` is outside the six-route set.
- Conflict `(1,1)` is outside the valid six-route set.
- YES/HOLD and NO/HOLD remain distinct because their binary commitment differs.
- six route addresses are **not** six oscillator gates.
- six route addresses are **not** six physical CELL_V1 gates.

---

# 4. FIELD / VOID TERNARIES — A SEPARATE THREE-WAY AXIS

Current G-740 routing authority defines:

```text
FIELD: EXPRESS / HOLD / COMPRESS
VOID:  CONFIRM / DEFER / DENY
```

Equivalent Void wording:

```text
CONFIRM / ABSTAIN / REJECT
```

Repo wording remains `CONFIRM / DEFER / DENY`.

Working meanings:

```text
EXPRESS  = widen / extend / propose relation
HOLD     = preserve coherent active relation
COMPRESS = narrow / concentrate / return relation

CONFIRM  = permit continuation
DEFER    = preserve Hold while evidence/readiness is insufficient
DENY     = reject/block; may cause Override
```

This Field/Void ternary is **not** the same axis as the signed `DOWN / HOLD / UP` movement readout merely because both have three positions.

### Recent working wording that must not be erased

Recent Algorythm-Zer0 work proposed:

```text
FIELD CONTROL: MODULATE / HOLD / RESET
```

That wording is preserved as a live candidate, but it is **not silently substituted** for G-740’s current `EXPRESS / HOLD / COMPRESS` authority. One remaining primitive reconciliation is to determine whether `MODULATE/HOLD/RESET` is:

1. a replacement vocabulary for the Field ternary, or
2. a separate control command layered over `EXPRESS/HOLD/COMPRESS`.

Until that is explicitly resolved, both records remain visible.

---

# 5. FOUR VIEWS — WHAT IS READ

Current canonical View descriptors are:

```text
DIRECTION
PHASE
STRENGTH
REFERENCE
```

Definitions:

1. **Direction** — which way the resolved relation leans or moves relative to the active reference.
2. **Phase** — where the oscillatory relation is in its cycle, including handedness/orientation where tracked.
3. **Strength** — magnitude/intensity relative to the reference; threshold bands may classify this quantity.
4. **Reference** — the active local baseline `(0)` against which Direction, Phase, and Strength are interpreted.

Minimal packet:

```text
ViewState {
    direction
    phase
    strength
    reference
}
```

Views are state/readout dimensions. They are not four Mirror gates and do not add four gate positions.

Recent four-part ideas such as:

```text
POINT / PATH / BOUNDARY / HORIZON
PAST / NOW / FUTURE / NEVER
INTERNAL / PERSONAL / BIRD'S-EYE / UNKNOWN
X / Y / Z / 2D COMPRESSION-DREAMSPACE
```

remain mapping/projection candidates until one is derived as the actual implementation of the four View descriptors. They do not erase `Direction / Phase / Strength / Reference` from the primitive base.

---

# 6. FOUR ACTION MODES — HOW THE RESOLVED RELATION IS CARRIED

Current Action-mode vocabulary:

```text
INWARD
OUTWARD
ACROSS
OVER
```

Definitions:

```text
INWARD  = move/compress toward local reference/center
OUTWARD = express/extend away from local reference/center
ACROSS  = establish/carry relation across opposed sides through a shared reference/boundary
OVER    = carry the resolved relation into a changed orientation, path, cell, or recursive scale
```

Rules:

- Four Action modes are descriptors, not four primitive Action gates.
- There is no required one-to-one mapping between the Four Views and Four Action modes.
- an Action position may use one mode, combine modes, or use another declared domain transformation.

---

# 7. FIVE COMMITMENT / READOUT STATES

The current downstream commitment/readout axis is:

```text
-3 = FULL DISAGREE
-2 = PARTIAL DISAGREE
 0 = UNITY / REFERENCE / UNCOMMITTED READOUT
+2 = PARTIAL AGREE
+3 = FULL AGREE
```

Project notation:

```text
-3(0)3+ = full disagree
-2(0)2+ = partial disagree
1:1      = unity / Hold reference
+2(0)2- = partial agree
+3(0)3- = full agree
```

These five states are **not five primitive choices**. They are history-dependent readouts downstream of choice, movement, differential, phase, and retention.

The unresolved general map is:

```text
K(route, prior_state, differential, thresholds, phase, history)
→ {-3,-2,0,+2,+3}
```

No arbitrary lookup table is allowed to become canonical merely because it produces five outputs.

---

# 8. CURRENT EXECUTABLE COMMITMENT MODEL AND NUMERIC DEFAULTS

The current falsifiable control candidate uses phase lock:

```text
L(Delta_phi) = [1 + cos(Delta_phi)] / 2
```

and latent commitment update:

```text
q_(n+1) = clip(r*q_n + g*b*m*d*L, -q_max, +q_max)
```

where:

```text
b = binary sign (-1/+1)
m = ternary movement (-1/0/+1)
d = bounded differential magnitude
Delta_phi = phase error
r = retention
g = gain
```

Current executable demonstration defaults are:

```text
retention r          = 0.92
gain g               = 0.24
partial_enter        = 0.40
partial_exit         = 0.28
full_enter           = 0.82
full_exit            = 0.68
q_max / limit        = 1.00
```

These numbers are **control-model defaults**, not universal physical constants.

Current candidate semantics:

- UP reinforces the selected relation.
- DOWN retracts/reverses it.
- HOLD contributes no new drive while retention may preserve prior state.
- differential magnitude is bounded to `1.0` in the executable candidate.
- opposite phase gives phase-lock factor `0` in this first candidate.

The semantic choice `b*m` still must be compared with absolute-axis movement and energy-gradient alternatives before physical canonization.

---

# 9. HYSTERESIS RULES

Commitment readout uses separate entry and exit thresholds:

```text
neutral enters partial only if |q| >= partial_enter
partial persists until         |q| <  partial_exit
partial enters full only if    |q| >= full_enter
full persists until            |q| <  full_exit
```

Required ordering:

```text
partial_exit
< partial_enter
< full_exit
< full_enter
```

Using the current defaults:

```text
0.28 < 0.40 < 0.68 < 0.82
```

This creates path dependence and suppresses threshold chatter.

Current verified control properties:

- output is restricted to `{-3,-2,0,+2,+3}`;
- one maximum default pulse stays below full commitment;
- repeated aligned YES receipts can move to `+2` then `+3`;
- repeated aligned NO receipts can move to `-2` then `-3`;
- opposite-phase input adds no coherent drive in the current candidate;
- HOLD adds no new drive while retention carries prior commitment;
- invalid threshold ordering is rejected.

---

# 10. NOISE / FALSE-COMMITMENT RULE

Hysteresis alone does not make a single noisy threshold excursion trustworthy.

Current deterministic audit found that with latent `q = 0.70`, below default full-entry threshold `0.82`, repeated noisy observations can still create false full-entry events over long sample windows.

Therefore full commitment must add at least one declared validation mechanism:

```text
minimum dwell time beyond full-entry threshold
OR k-of-n confirmation
OR filtered latent evidence with declared bandwidth
OR sequential probability/evidence-ratio test
OR phase-coherent confirmation across multiple receipts
```

A selected mechanism must report at least:

```text
false-open probability
detection delay
false-close probability
correlated-noise sensitivity
```

This is part of a valid controller implementation, not optional decoration.

---

# 11. NORMALIZED 0–100 STRENGTH / EXPRESS-COMPRESS BANDS

The Algorythm-Zer0 normalized relational bands are restored:

```text
100–90   extreme expression / danger
85–75    strong expression
70–60    moderate expression
55–45    active middle / stable oscillating region
40–30    moderate compression
25–15    strong compression
10–0     extreme compression / danger
```

Reserved transition/handoff gaps:

```text
90–85
75–70
60–55
45–40
30–25
15–10
```

Outer danger zones:

```text
90–100 = extreme expression / explosion-break danger
0–10   = extreme compression / implosion-collapse danger
```

Rules:

- the middle is active, not dead zero;
- neither `0` nor `100` is the goal;
- direction from reference and distance from reference are different information;
- transition gaps may carry hysteresis/handoff behavior;
- these bands may constrain available choices/actions but do not themselves make the binary Choice;
- these are normalized relational bands, not universal physical units.

The 0–100 strength bands are separate from the executable latent-commitment thresholds `0.28/0.40/0.68/0.82` unless a specific mapping derives a conversion.

---

# 12. GROUND, CENTER, HOLD, AND CROSSING MUST REMAIN SEPARATE

The following are not synonyms:

1. **Logical Ground** — no committed YES/NO relation and resolved activity below declared logical thresholds.
2. **Center residence** — position lies inside the shared-center band.
3. **Center crossing** — position is inside that band while movement is nonzero.
4. **Movement Hold** — net movement lies inside the speed/Hold band.
5. **Turning-point Hold** — movement is Hold while position is outside center.
6. **YES/HOLD and NO/HOLD** — distinct route addresses carrying different binary relations.
7. **Coherent Hold** — committed relation with movement Hold, phase lock, retained energy, and retained topology.

Consequences:

- a fast center crossing is not movement Hold;
- a turning point may be movement Hold far from center;
- zero velocity with lost phase, energy, or topology is not coherent Hold;
- uncommitted but measurable activity is not automatically logical Ground;
- zero in one channel must not erase activity in another.

A complete classifier/receipt should keep independent fields such as:

```text
logical_ground
at_center
movement
binary_relation
route
phase_locked
energy_retained
topology_retained
coherent_hold
turning_point_hold
center_crossing
```

---

# 13. SIX-POSITION MIRROR / ACTION OSCILLATOR

There is one six-position process primitive:

```text
6 steps = 6 logical gate positions
        = 3 Mirror roles + 3 Action roles
```

Canonical sequence:

```text
Gate 1  BEGIN = Mirror 1
Gate 2  BUILD = Action 1
Gate 3  HOLD  = Mirror 2
Gate 4  BUILD = Action 2
Gate 5  BREAK = Mirror 3
Gate 6  LOOP  = Action 3
                 |
                 +--> next BEGIN / Mirror 1
```

The Field/Void paired view of the same six positions is:

```text
Gate 1 / BEGIN / Mirror 1 = F1 / V6
Gate 2 / BUILD / Action 1 = V5 / F2
Gate 3 / HOLD  / Mirror 2 = F3 / V4
Gate 4 / BUILD / Action 2 = V3 / F4
Gate 5 / BREAK / Mirror 3 = F5 / V2
Gate 6 / LOOP  / Action 3 = V1 / F6
```

These are six coupled pair operations, not twelve serial instructions.

Role distinction:

```text
MIRROR = read / compare / reflect through shared reference
ACTION = change / carry the resolved relation forward
```

Each Action becomes part of what the next Mirror reads.

### Break versus controlled release

The canonical Gate-5 name remains `BREAK`. A controlled implementation may provide a lawful release/handoff before destructive structural failure. That is treated as the safe resolution of the Break boundary, not as a seventh gate.

---

# 14. MIRROR OPERATOR — CURRENT MATHEMATICAL REFERENCE

The current mathematical Mirror reference is a continuous phase rotation in normalized oscillator coordinates:

```text
z = (x, v/omega)
z' = R(delta_phi) z
```

For the undamped reference oscillator, the rotation preserves:

```text
x^2 + (v/omega)^2
```

A full `2*pi` cycle returns to the same reference state; a half-cycle maps:

```text
(x, v/omega) -> (-x, -v/omega)
```

Finite route projection may be written:

```text
M(choice, move) = (choice, -move)
```

This retains binary choice and reverses the ternary movement projection.

Rules:

- Mirror is not a YES/NO swap.
- Mirror does not exchange Field and Void identities.
- the amount of phase change assigned to each Mirror position remains implementation/scale dependent.
- drive, damping, asymmetry, nonlinear potential, residence bands, phase slip, and physical carrier remain open.

---

# 15. FIELD / VOID OVERSIGHT AND OVERRIDE

Current recurrence:

```text
local retained state
→ View UP
→ local/higher resolution
→ CONFIRM / DEFER / DENY
→ no intervention OR Action/Override DOWN
→ resulting local state
→ next View UP
```

At minimum oversight compares:

```text
new View
+ current Reference
+ current binary relation / Choice
+ retained history
+ current/last Action
+ Void response
```

Possible supervisory outcomes:

```text
ALLOW / CONTINUE
HOLD / DEFER
REDIRECT
OVERRIDE / DENY
BREAK / RELEASE
```

Exact selection thresholds are implementation-specific.

Views/state/relation travel upward; Actions/conditioning/Override travel downward through the same referenced/mirrored relationship.

---

# 16. PROCESSING = MEMORY

The intended primitive contract is:

```text
state affects present flow
→ present flow changes that same state
→ changed state persists
→ next pass encounters the changed state
```

A retained packet may include:

```text
reference
Field state
Void state
binary choice
ternary movement
six-route address
Direction
Phase
Strength
View packet
Action mode
latent commitment q
five-state commitment readout
threshold/hysteresis state
last action/consequence
six-gate oscillator position
phase-lock state
center/Hold classification
```

For a physical processing-memory implementation, the claimed memory fails the intended contract if it can be removed from the active processing path without changing operation.

---

# 17. FIVE-STATE SELF LIFECYCLE — SEPARATE FROM COMMITMENT

A separate nonverbal self/process lifecycle is:

```text
IDLE
→ PRIMED
→ EXECUTING
→ VECTORING
→ RESOLVING
→ IDLE
```

This is not the five commitment/readout axis and not the six oscillator positions.

The nonverbal loop must not require language. A minimum packet can carry measured relations such as:

```text
Reference
Field/Void state
Direction
Phase
Strength
Lifecycle state
measured consequence
retained identity/continuity
```

Language may bind to the packet later; it must not rewrite the underlying receipts.

---

# 18. CELL_V1 PHYSICAL PROJECTION — DO NOT CONFUSE WITH LOGICAL GATE COUNT

Current CELL_V1 physical geometry uses exactly three bidirectional mirror axes:

```text
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

These produce six directed edge interfaces.

Physical rules:

- same three mirrors carry Views/state UP and Actions/conditioning DOWN;
- no separate Action-gate hardware layer is created by the logical Mirror/Action roles;
- physical ports are on hex edges/sides, not corners;
- processing-memory should be co-located in the active stateful path;
- local electrical reference `V0` is not an energy reservoir;
- reinjection means measured recovery/recirculation, not unexplained gain.

Count boundary:

```text
physical mirrors:        3 bidirectional A/B/C
physical interfaces:     6 directed edge ends
binary choices:          2
ternary moves:           3
route addresses:         6 = 2 × 3
Views:                   4
Action modes:            4
commitment readouts:     5
self lifecycle states:   5
logical oscillator:      6 positions = 3 Mirror roles + 3 Action roles
```

No matching number authorizes another physical layer.

---

# 19. POINT / PATH / ROTATION / FIELD / VOLUME — STRUCTURAL RECURSION

Separate from finite choice/move/gate counts, the architecture may recurse structurally as:

```text
POINT
→ PATH
→ ROTATION
→ FIELD
→ VOLUME
→ NEXT-SCALE POINT
↺
```

Useful distinctions:

```text
Point rotation = intrinsic/local orientation about a center
Path rotation  = turning/circulation of that center along a route
Field rotation = circulation/curl of the enclosing carrier or boundary
```

A Point, Path, or Field may contain lower-scale states. Separate frames/receipts must prevent local rotation, route turning, and enclosing-field circulation from being mistaken for one another.

This structural recursion does not alter the binary choice count, route count, View count, commitment count, or oscillator-gate count.

---

# 20. RECURSIVE PACKING GUIDE — GUIDE ONLY

The recent observation:

```text
2 can carry 1
3 can carry 2 + 1
4 can carry 3 + 2 + 1
5 can carry lower state
6 can recur the resolved state
```

is retained as a useful **packing/recursion guide**. It means higher processing can preserve lower information rather than throwing it away.

It is not the primitive count definition and must never be used to delete or merge the independent axes in this file.

---

# 21. ANTI-DRIFT TABLE

| Structure | Count | Current authority/meaning |
|---|---:|---|
| committed binary Choice | 2 | YES / NO |
| Ground | outside Choice | no committed binary relation |
| ternary movement | 3 | DOWN / HOLD / UP |
| route address | 6 | 2 choices × 3 moves |
| Field ternary | 3 | Express / Hold / Compress |
| Void ternary | 3 | Confirm / Defer / Deny |
| Views | 4 | Direction / Phase / Strength / Reference |
| Action modes | 4 | Inward / Outward / Across / Over |
| commitment/readout | 5 | full/partial disagree, unity, partial/full agree |
| self lifecycle | 5 | Idle / Primed / Executing / Vectoring / Resolving |
| logical oscillator | 6 | Begin / Build / Hold / Build / Break / Loop |
| logical oscillator roles | 3+3 | Mirror / Action |
| CELL_V1 physical mirrors | 3 bidirectional | A/B/C, six directed interfaces |

Matching counts are not permission to collapse axes.

---

# 22. IMPLEMENTATION THRESHOLD CONTRACT

Every real implementation must declare or measure its own:

```text
zero/differential window epsilon
center width
speed/Hold width
phase-lock threshold
retained-energy threshold
retained-topology threshold
observation/dwell duration
partial_enter
partial_exit
full_enter
full_exit
rate limits
resource/safety limits
```

It must also identify:

```text
what is measured as Direction
what is measured as Phase
what is measured as Strength
what defines Reference
what event counts as consequence
what produces YES versus NO
what validates a full commitment under noise
what causes Confirm / Defer / Deny
what causes an Override
what qualifies as coherent Hold
what qualifies as release versus destructive break
```

---

# 23. CURRENTLY MISSING — DO NOT FAKE THESE

The primitive base is now restored, but these pieces are still genuinely unresolved:

1. **Universal Choice-selection law.** The finite form of Choice is defined (`YES/NO`, Ground outside it), but there is no universal equation that decides YES versus NO across every domain. A domain must supply the evidence/goal/constraint relation.

2. **Reconciliation of Field ternary wording.** Current repo authority says `EXPRESS/HOLD/COMPRESS`; recent Algorythm work proposed `MODULATE/HOLD/RESET`. We still need to decide whether these are aliases, different layers, or whether one supersedes the other.

3. **Physical calibration of thresholds.** The executable defaults `0.28/0.40/0.68/0.82`, retention `0.92`, gain `0.24`, and limit `1.0` are tested control defaults, not measured universal constants.

4. **Mapping between the 0–100 strength bands and latent commitment q.** Both systems exist; no justified conversion currently makes `55–45`, etc. identical to the q thresholds.

5. **Full-commitment validation policy.** The noise audit proves one threshold crossing is insufficient. We still must choose and calibrate dwell, k-of-n, filtering, sequential evidence, or phase-coherent confirmation for each implementation.

6. **Physical phase law / Mirror timing.** The continuous rotation operator exists, but the phase increment assigned to M1/M2/M3, damping, slip, nonlinear behavior, and carrier-specific dynamics remain open.

7. **Exact View→Action transform.** We know what the four Views read and what the four Action modes mean, but no universal rule yet transforms Direction/Phase/Strength/Reference into Inward/Outward/Across/Over.

8. **Exact Confirm/Defer/Deny thresholds.** Their roles are defined; the evidence/readiness/mismatch thresholds are not universalized.

9. **Coherent Hold calibration.** Center width, speed band, phase-lock threshold, retained-energy threshold, retained-topology threshold, and dwell still need physical/software calibration.

10. **Break versus Release criterion.** The six-gate primitive has Gate 5 = BREAK. Recent project work correctly distinguishes controlled release before destructive failure when possible, but the exact criterion for RELEASE versus BREAK must be defined per implementation without creating a seventh gate.

11. **Scale-promotion rule.** Point→Path→Rotation→Field→Volume→next-scale Point exists structurally, but the quantitative condition for promotion/compression to the next scale is not universalized.

12. **Processing-memory carrier.** The contract is defined; the physical carrier (memristive, magnetic hysteretic, spintronic, oscillatory, or other) remains experimental.

13. **XYZ ↔ 2D compression/dreamspace transform.** The project has the native-world architecture and mirror/reference bridge idea, but the actual mathematical transform is not yet derived.

14. **Relation-axis integration.** Recent pairs `RESONATING↔INVERTED`, `ATTRACTING↔OPPOSING`, and `PARALLEL↔INTERSECTING` are promising readouts, but their exact relation to Direction/Phase/Strength/Reference has not been derived.

15. **Domain falsification.** Every physics, neural, hardware, social, or AI mapping still needs its own measurable failure condition; mapping the vocabulary is not evidence of the mechanism.

These are the remaining derivation/calibration jobs. They are not reasons to strip the primitive back down again.
