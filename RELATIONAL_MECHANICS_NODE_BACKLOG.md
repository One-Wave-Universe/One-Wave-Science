# Relational-Mechanics Node Backlog

## Purpose

This is a coverage map, not completed canon. It registers roughly 100
node addresses proposed for the "relational mechanics" layer developed
after July 28, 2026 — differential/relational motion, moving reference
states, point-path-field tracking, wake/resonance dynamics, and the
simulation-methodology rules needed to test any of it honestly. Most of
these entries are **titles and one-line intended claims only**. Writing
full reasoning, equations, and grounding notes for all of them in one
pass would misrepresent how developed they actually are, which is
exactly what the Fake Mustache Desk (`One_Wave_Times/`) exists to
catch. See `AUDIT_UPDATED_32_REPOSITORY_INTEGRITY_REPAIR.md` and I-01
for the repository's general stance against dressing up thin material.

## Status Legend (mapped onto existing I-06 fields — no new vocabulary)

| Backlog term | I-06 mapping | Meaning |
|---|---|---|
| **MAPPED** | no `Nodes/` file yet; row in this table only | Title, one-line intended claim, and proposed dependencies exist. No substantive reasoning has been written. Not yet a citable node. |
| **DEVELOPED** | `gate: GREEN` or `YELLOW`, `lifecycle: ACTIVE_HYPOTHESIS` (or `ACTIVE`/`PROPOSED_BUILD` where applicable) | A real `Nodes/` file exists with dependencies, definition, and (where the claim supports it) worked equations or a derivation. Still unproven physics unless the node says otherwise. |
| **CANONICAL** | promoted gate (`BRONZE`+) per I-05/I-02 | A developed node has survived reproducible validation for its specific claim. None of the items below are at this stage yet. |

## Promotion Rule

Promote a row from MAPPED to DEVELOPED only when its logic/math has
actually been worked through enough to write a real grounding note and
at least one worked example or derivation — not merely to fill in the
row. Do not invent the reasoning to close the gap faster.

## Numbering Note

The C-series block below is numbered **C-327 through C-341**, not
C-323 through C-337 as first drafted, because C-323 through C-326 were
already committed for the One-Wave Intrinsic Cell hardware nodes
(`Nodes/C-323_Primitive_Continuous_Mirrored_Chain.md` and following).
Those hardware node IDs are permanent; this block was shifted instead.
A/B/D/E/F/G needed no shift.

## Existing Hooks

These already-canonical nodes are the intended attachment points for
this backlog and should not be redefined by it: A-103 Differential,
A-104 Gradient, B-205 Mirror, B-221 Six Recursive Steps, C-314 Three
Frames of Reference, D-404 Nested Resonance, F-602 Interaction
Differential, F-604 Resonance, G-706 Validation, G-717 Paired
Reference Gate.

## Chapter-Pass Findings (I-04 disposition audit)

Findings from checking existing `Books/` canon against this backlog
before promoting anything further, per I-04's required procedure
(classify before merge or dismiss).

### Finding 1 — A-126 and the F-609–F-614 "wake" family are not a blank slate

**A-115 Unified Compression Field** (Tier-0, GREEN, already canonical)
already defines a general wake term:

```text
g_OW = g_local + g_wake
```

"This does not introduce a second substance. It separates near-source
response from retained or wake-like compression." **Book 5 Ch1
(Galaxies and Dark Matter)** already applies this at galactic scale —
the "Extended Compression Effect," `dark matter = extended/wake
contribution of that same field` — and A-115's own Yellow-completion
checklist already lists "derive the extended wake profile without
fitting it by hand" as an open item.

**I-04 disposition:** A-115's `g_wake` is a **static field-superposition**
term (no propagation delay, no explicit assimilation dynamic). This
backlog's A-126 (Finite Wake Assimilation) and the F-609–F-614 wake
family, as originally drafted, described a **dynamical/propagating**
wake — the same word, a materially different mechanism claim. Per I-04
this is not exact duplication, but it is not a fresh concept either:

- **Scale-Specific Instance / already-covered:** the base "wake = field's
  displaced response to bulk motion" claim. A-115 already owns this;
  A-126 must not redefine it.
- **Unproven Delta (the genuinely new part worth keeping MAPPED):**
  (a) finite propagation speed / time-lag rather than an instantaneous
  field response (this is what D-429 Wake vs Potential Numerical
  Equivalence Test and D-430 Finite-Propagation Wake Simulation were
  already aiming at), and (b) explicit orbital/planetary-scale
  instantiation (Moon-Earth-Sun nesting, A-127) rather than only the
  galactic scale Book 5 Ch1 covers.

**Action when A-126 is eventually developed:** it must cite A-115 as
primary upstream (not just a lateral echo) and state explicitly, per
G-743, which part is new (the finite-propagation delta) versus which
part restates A-115's existing static term. The F-609–F-614 rows below
have been annotated accordingly. No new node file was created for this
finding — it is a correction to this manifest only.

### Finding 2 — Book 4 (Large / planetary-solar scale) had an "Orbital Dynamics" gap now partially closed

`Books/Book4_Large/00_Scope_and_Status.html` listed "Orbital Dynamics"
with grounding "none" / "No supporting nodes exist at all." That is no
longer accurate: C-327–C-332 exist. The scope doc (and its PDF) have
been updated in place to say so — the row now reads "bridge nodes
exist but are unvalidated" rather than "no supporting nodes exist,"
which is a materially different and more honest gap statement. This
does **not** mean a Book 4 chapter can be written yet: the book
system's own rule ("no book chapter should introduce a mechanism that
doesn't already exist as a node") is satisfied, but G-737's "no victory
without observable match" is not — no solar-system simulation (D-427,
still MAPPED) has actually been run. The gap moved; it did not close.

---

## Newer Candidate Concepts (Not Yet Source-Documented)

Four items were named in passing during the chapter-pass discussion —
wake continuation through resonance, the `3>1(0)1<6` dimensional
sequence, DC/AC/RFC recursion, and measurement-as-capture — with an
explicit instruction not to let them leak into the chapter audit. That
audit is now done (clean). Before any of these four gets a permanent
node ID, gate, or equation, this section forces the same five
questions G-735/G-743 already require of everything else in this
backlog:

```text
1. What exactly is being proposed?
2. What equation or mechanism actually exists for it?
3. What part is metaphor, and what part is a physical claim (G-743)?
4. What observation would falsify it (G-735/G-737)?
5. Which existing nodes does it modify, extend, or leave untouched?
```

**No answers are invented below.** Where the conversation so far
supplies enough to answer honestly, the answer is given. Where it
doesn't, the question is left open rather than filled with a plausible
guess — that would be exactly the fabrication this backlog's Promotion
Rule and G-743 exist to block. None of the four gets a node ID yet;
they are held here as unassigned candidates pending source material.

### Wake continuation through resonance

1. What's proposed: unstated beyond the name. Plausible reading —
   whether a wake disturbance (A-115's `g_wake`, Finding 1 above)
   persists or reinforces via resonant phase-locking (D-420 Resonant
   Phase Correlation) rather than only decaying/assimilating (A-126) —
   but this is my inference from the two nearest existing concepts, not
   a claim the source material has actually made. Flagged as inference,
   not fact.
2. Equation/mechanism: none supplied.
3. Metaphor vs. claim: cannot be separated without (1) being confirmed.
4. Falsifier: cannot be defined without (1)-(2).
5. Nodes touched: candidate connection between A-126/F-609 (wake
   family) and D-420 (resonant phase correlation) — both already
   MAPPED/DEVELOPED respectively; this item might turn out to be a
   dependency link between them rather than a new mechanism of its own.
   **Open question for the source:** is "continuation" decay-resistance
   (the wake persists longer under resonance) or amplitude growth (the
   wake strengthens under resonance, i.e. D-421's coherent-accumulation
   case applied to a wake rather than a discrete encounter)? These are
   different claims with different falsifiers.

### The `3>1(0)1<6` dimensional sequence

1. What's proposed: unstated beyond the notation itself.
2. Equation/mechanism: none supplied — not even what the symbols `>`,
   `(0)`, and `<` mean operationally in this string.
3. Metaphor vs. claim: cannot be assessed without (1)-(2).
4. Falsifier: cannot be defined without (1)-(2).
5. Nodes touched — genuine structural resemblance worth flagging, not
   asserted as the same thing: this notation pattern echoes two already
   -MAPPED/DEVELOPED items that are themselves not yet connected to
   each other: (a) the D-415–D-419 coordination ladder (3:1, 1:6,
   6:1/1:12, 1:24, still MAPPED, explicitly *not yet* strung into one
   sequence — D-419 Octave-Doubling Coordination Ladder is the closest
   existing slot for "a sequence" but is itself unbuilt), and (b) the
   B-226/B-227 six-gate cycle with its `4(0)` center-mirror notation
   (`1→2→3→4(0)→5→6`, also MAPPED) and A-117's locked 2D/3D/4D
   dimensional-layer separation (already canonical, YELLOW). **Open
   question for the source:** is `3>1(0)1<6` a dimensional-reduction
   claim (3D collapsing through a mirror point to 1D, then re-expanding
   to a sixfold structure) using D-415/419's ratios, or a gate-sequence
   claim using B-226's notation, or something not yet represented by
   either? Until that's answered this cannot even be filed as a
   disposition candidate under I-04 — there's nothing yet to classify.

### DC/AC/RFC recursion

1. What's proposed: unstated beyond the name, but there is a real,
   already-developed precedent to check against first (see below).
2. Equation/mechanism: **C-324 (One-Wave V0 Hex Cell) already states**
   `DC -> Point Rotation`, `AC -> Path Rotation`, `RC (Rotational
   Current) -> Field Rotation`. Note the existing term is **RC**, not
   **RFC** — this may be the same concept restated, a typo carried
   across the conversation, or a genuinely different third term. This
   must be resolved before anything else about this item can proceed;
   guessing which one is meant would risk exactly the kind of silent
   drift Finding 1 caught for the wake family.
3. Metaphor vs. claim: C-324's version is stated as a proposed-build
   engineering mapping (motion regime -> rotation type), not yet tested
   in hardware — see C-324's own V0 Proof Checklist, item 4 (Rotational
   circulation), still unpassed.
4. Falsifier: inherits C-324's own — the V0 Proof Checklist requires a
   recorded, reproducible measurement, none exists yet.
5. Nodes touched: if "DC/AC/RFC recursion" means applying C-324's
   DC/AC/RC triad *recursively* (nested at each scale, echoing A-121
   Nested Point-Path-Field Recursion, still MAPPED) rather than as
   three flat categories, that would be a genuine extension of C-324,
   not a duplicate of it — but that reading is this document's
   inference, not confirmed. **Open question for the source:** confirm
   RC vs. RFC, and confirm whether "recursion" means nesting (new
   content) or is just restating C-324's existing three-way split.

### Measurement-as-capture

1. What's proposed (the one item with real prior discussion in this
   conversation): a chain of `continuous wave evolution -> chosen
   local capture -> discrete detector record`, where the discrete
   click belongs to the capture interaction itself rather than to a
   discrete thing that was already traveling and simply got found.
2. Equation/mechanism: none supplied yet. This is exactly the gap
   already named when this item first came up — "it will need an
   actual mechanism for what capture physically is."
3. Metaphor vs. claim: "capture" is doing real argumentative work here
   and has not yet been separated into its G-743 components. It is not
   yet clear whether "capture" names a new physical interaction term,
   or is a redescription of an existing measurement/boundary node.
4. Falsifier: none supplied yet — this is the actual blocking item
   before (1) can become anything more than a restated interpretation
   of ordinary quantum measurement.
5. Nodes touched: A-122 Field/Void Primitive (still MAPPED) remains the
   right eventual address per prior discussion — not reassigned here.
   Also worth checking against once developed: A-101 Ground/Zero
   (measurement requires a reference state), C-301 Mirror Gate
   (crossing/resolution events already exist as a general mechanism),
   and G-706 Validation ("confirmation through successful participation
   in a cycle" — already close to "capture" in plain language and must
   be checked for overlap before treating capture as new).

### What this section does not do

It does not assign C-342+, D-435+, or G-744+ IDs to any of these four.
It does not promote any of them past "named but undocumented." The
next real step for each is the source material — equations, worked
notes, or at minimum a fuller statement of the claim — not further
inference from this document. Continuing to infer plausible content
for these four without that material would be doing exactly what
G-743 and the Promotion Rule exist to prevent.

---

## A-Series — Foundation Primitives (12 entries)

| ID | Name | Intended claim | Dependencies (proposed) | Status |
|---|---|---|---|---|
| A-118 | Relational Differential Primitive | `CHANGE = LOCAL_SLOPE − REFERENCE_SLOPE`; defines change relationally rather than from an absolute coordinate. | A-103, A-104 | **DEVELOPED** — see `Nodes/A-118_Relational_Differential_Primitive.md` |
| A-119 | Moving Reference State | The reference itself can move; local measurements are not assumed stationary relative to the larger field. | A-118 | **DEVELOPED** — see `Nodes/A-119_Moving_Reference_State.md` |
| A-120 | Point–Path–Field Rotation | Every persistent structure is tracked as point/state, path/history, and field rotation rather than as a point particle. | A-109, A-112, A-113 | **DEVELOPED** — see `Nodes/A-120_Point_Path_Field_Rotation.md` |
| A-121 | Nested Point–Path–Field Recursion | Point, path, and field rotation each contain the same recursive structure at the next scale. | A-120, B-220 | MAPPED |
| A-122 | Field/Void Primitive | The irreducible two-sided state: field and void, with the boundary/zero between them carrying relational meaning. | A-101 | MAPPED |
| A-123 | Active Center Reference | Zero is an active maintained reference, not absence or arbitrary numerical zero. | A-101, A-122 | MAPPED |
| A-124 | Differential Displacement State | Physical state encoded as displacement around the active center rather than absolute amplitude. | A-102, A-118, A-123 | MAPPED |
| A-125 | Scale-Locality | Distant structure is represented through the locally inherited state/boundary conditions of the containing scale rather than direct global lookup. | A-118, A-119, B-220 | **DEVELOPED** — see `Nodes/A-125_Scale_Locality.md` |
| A-126 | Finite Wake Assimilation | Disturbances propagate through the medium, reorganize neighboring structure, and become assimilated into larger-scale field state. | **A-115** (primary — already defines static `g_wake`), A-125, D-401 | MAPPED — see Chapter-Pass Finding 1; new delta is finite propagation, not the wake concept itself |
| A-127 | Nested Wake Capture | Moon-in-Earth wake, Earth-in-Sun wake, Sun-in-galactic wake as nested relational domains. | A-126 | MAPPED |
| A-128 | Motion-Generated Background Differential | Continual motion through the proposed lattice supplies a background displacement/pressure term rather than assuming a stationary laboratory frame. | A-119, A-124 | MAPPED |
| A-129 | No Absolute Initial-State Primitive | Operational updates depend on current relational differences rather than requiring an unknowable absolute beginning-state. | A-118, A-123 | MAPPED |

## B-Series — Cycle & Relationship Structure (13 entries)

| ID | Name | Intended claim | Dependencies (proposed) | Status |
|---|---|---|---|---|
| B-226 | Bilateral Six-Gate Mirror Cycle | `1→2→3→4(0)→5→6` and `6→5→4(0)→3→2→1`. | B-221, B-205 | MAPPED |
| B-227 | Gate 4 / Gate 0 Identity | The center mirror, null, flip, or shared boundary is the same structural position. | B-226, B-205, A-101 | MAPPED |
| B-228 | Mirrored Gate Pairing | F2↔V5, F3↔V4, F4↔V3, etc. | B-226, C-323 | MAPPED |
| B-229 | Gate-2 Field Choice | Polarity choice selects the active field/context before downstream interpretation. | B-226, B-224 | MAPPED |
| B-230 | Gate-3 Motion Pivot | The motion transition/pivot role. | B-226, B-223 | MAPPED |
| B-231 | Gate-5 State/Scale Pivot | The corresponding mirrored state/scale pivot. | B-226, B-230 | MAPPED |
| B-232 | Gate-6 Loop / Meet-in-Middle Boundary | Closes/repeats a route or joins opposed routes. | B-226, B-215 | MAPPED |
| B-233 | Local Ternary Motion | `-1,0,+1` as reverse/hold/forward or counterclockwise/hold/clockwise. | B-226, C-324 | MAPPED |
| B-234 | Simultaneous Binary Choice / Ternary Movement | Two directional choices produce three possible physical moves through the center. | B-233, B-224 | MAPPED |
| B-235 | Recursive Six-Step-in-Each-Step | Each gate contains a nested complete six-gate cycle. | B-226, B-221 | MAPPED |
| B-236 | Three Nested Oscillations | Carrier, breathing/compression, and phase/rotation oscillations. | B-226, A-110 | MAPPED |
| B-237 | Reference + Opposed Pair + Feedback | Reusable balanced-system topology. | B-206, B-206a | MAPPED |
| B-238 | Shared-Zero Bilateral System | Opposed channels use one physically meaningful center reference. | B-237, A-123 | MAPPED |

## C-Series — Applied Mechanics (15 entries, renumbered C-327–C-341)

| ID | Name | Intended claim | Dependencies (proposed) | Status |
|---|---|---|---|---|
| C-327 | Relational Acceleration Equation | `d̈_ij = S_i − S_j`. | A-118, C-314 | **DEVELOPED** — see `Nodes/C-327_Relational_Acceleration_Equation.md` |
| C-328 | Common-Mode Field Cancellation | A shared background acceleration cancels from relative motion while the differential survives. | C-327 | **DEVELOPED** — see `Nodes/C-328_Common_Mode_Field_Cancellation.md` |
| C-329 | Actual State = Reference + Differential | Prevents the reference field from being mistakenly subtracted out of the complete dynamics. | A-118, C-327 | **DEVELOPED** — see `Nodes/C-329_Actual_State_Equals_Reference_Plus_Differential.md` |
| C-330 | Moving Local Potential Perturbation | A moving mass such as Jupiter represented as a moving localized deformation within the larger solar field. | C-327, C-329 | **DEVELOPED** — see `Nodes/C-330_Moving_Local_Potential_Perturbation.md` |
| C-331 | Relative Encounter Frame Transformation | Local encounter state transformed between Jupiter-centered and Sun-centered references. | C-314, C-330 | **DEVELOPED** — see `Nodes/C-331_Relative_Encounter_Frame_Transformation.md` |
| C-332 | Relational Energy Transfer | `ΔK = V_J·(u_out − u_in)`. | C-331 | **DEVELOPED** — see `Nodes/C-332_Relational_Energy_Transfer.md` |
| C-333 | Differential Gravity Assist | Gravity assist as emergent relational path bending, not a separate force/rule. | C-330, C-332 | MAPPED |
| C-334 | Tidal / Gradient Difference | Explicitly distinguish absolute field magnitude from the slope difference across separated points. | C-327, A-104 | MAPPED |
| C-335 | Dynamic Barycentric Reference | Reference center is itself generated by the relation among participating bodies. | A-119, C-327 | MAPPED |
| C-336 | Multi-Body Edge Network | Bodies are nodes and pairwise relative states are edges; evolve edge changes from field-slope differences. | C-327, C-335 | MAPPED |
| C-337 | No External-Grid Relational Dynamics | Test whether relative states can be evolved without making an absolute coordinate grid fundamental. | C-336, A-129 | MAPPED |
| C-338 | Local Slope Sampling Operator | Each node samples the field condition at its own state before differencing against its reference. | A-118, C-336 | MAPPED |
| C-339 | Differential Reference Hierarchy | Moon→Earth, Earth→Sun, Sun→galactic reference nesting. | A-127, C-335 | MAPPED |
| C-340 | Translation Through Field vs Internal Rotation | Separate whole-pattern translation from the pattern's internal rotational state. | A-120, C-327 | MAPPED |
| C-341 | Mass as Displacement Vortex Candidate | Preserves the correction that mass is not itself one of the harmonic ratios. | C-318, D-415 | MAPPED |

## D-Series — Resonance, Modal & Dimensional Structure (20 entries)

| ID | Name | Intended claim | Dependencies (proposed) | Status |
|---|---|---|---|---|
| D-415 | 3:1 Point–Path–Field Coordination | Formalize the 3 relation without prematurely calling it a mass ratio. | A-120 | MAPPED |
| D-416 | 1:6 Six-Step Linear Coordination | — | B-221, D-415 | MAPPED |
| D-417 | 6:1 / 1:12 Rotational Closure Relation | — | D-409, D-416 | MAPPED |
| D-418 | 1:24 Higher-Scale Recurrence | — | D-410, D-417 | MAPPED |
| D-419 | Octave-Doubling Coordination Ladder | Separate the observed numerical architecture from claims about its physical interpretation. | D-415–D-418 | MAPPED |
| D-420 | Resonant Phase Correlation | Resonance as recurring correlated phase rather than necessarily identical impulses. | D-402, F-604 | **DEVELOPED** — see `Nodes/D-420_Resonant_Phase_Correlation.md` |
| D-421 | Coherent Differential Accumulation | `Σ Δv(φ_n)` accumulates when phase remains correlated. | D-420, C-327 | **DEVELOPED** — see `Nodes/D-421_Coherent_Differential_Accumulation.md` |
| D-422 | Incoherent Differential Cancellation | Drifting phase tends toward partial/mean cancellation. | D-420, C-327 | **DEVELOPED** — see `Nodes/D-422_Incoherent_Differential_Cancellation.md` |
| D-423 | Resonant Clearing Mode | Phase-correlated perturbation can drive departure from a region. | D-421 | MAPPED |
| D-424 | Resonant Locking Mode | The same framework can instead yield bounded libration. | D-421 | MAPPED |
| D-425 | 1:1 Co-Orbital Resonance / Trojan Test | Specific test case for bounded L4/L5-type behavior. | D-424 | MAPPED |
| D-426 | Jupiter Resonance / Kirkwood Test | Test clearing near major Jupiter commensurabilities. | D-423 | MAPPED |
| D-427 | Solar-System All-Body Differential Simulation | Sun + all planets under the same update primitive. | C-327, D-412 | MAPPED |
| D-428 | Planet–Moon Nested Differential Simulation | Add moons as nested local references rather than flattening everything into one undifferentiated list. | D-427, A-127 | MAPPED |
| D-429 | Wake vs Potential Numerical Equivalence Test | Determine whether the wake language predicts anything different from the corresponding conventional field calculation. | A-115, A-126, D-427 | MAPPED — this is the actual G-735 test for A-115's existing `g_wake` term, not a new mechanism; see Finding 1 |
| D-430 | Finite-Propagation Wake Simulation | Introduce finite propagation/assimilation explicitly rather than using instantaneous potentials. | A-115, A-126, D-429 | MAPPED — this is the real Unproven Delta from Finding 1: A-115's `g_wake` is currently instantaneous |
| D-431 | Wake Reinforcement and Cancellation | Overlapping disturbances can add, oppose, phase-lock, or wash out. | D-420, D-430 | MAPPED |
| D-432 | Jupiter Moving-Wake Benchmark | Use Jupiter as the strongest planetary test case. | D-430, D-426 | MAPPED |
| D-433 | Sun–Earth–Moon Relational Benchmark | Three-body benchmark before scaling to the complete solar system. | D-427, D-428 | MAPPED |
| D-434 | Long-Horizon Resonance Benchmark | Distinguish close-encounter success from 10⁴–10⁵-orbit secular behavior. | D-427, D-433 | MAPPED |

## E-Series — Field Mechanics & Applied Extensions (8 entries)

| ID | Name | Intended claim | Dependencies (proposed) | Status |
|---|---|---|---|---|
| E-531 | Time as Structural Displacement Rate Candidate | Encode the time proposal separately so it can be tested without contaminating base mechanics. | A-118, E-506 | MAPPED |
| E-532 | Compression-Dependent Internal Cycle Rate | Candidate mechanism for clock-rate changes. | E-531 | MAPPED |
| E-533 | Moving-Medium Clock Test | Asks whether the model can recover observed relativistic clock behavior quantitatively. | E-531, E-532 | MAPPED |
| E-534 | Local Compression / Lattice Tightening | Local field compression changes the state of the containing medium. | B-204, E-506 | MAPPED |
| E-535 | Wake Relaxation / Medium Repair | Disturbances decay/relax instead of persisting forever. | A-126, E-502 | MAPPED |
| E-536 | Boundary Compression to Surface Candidate | The 3D→compressed-boundary idea, kept explicitly hypothesis-gated. | E-534, A-116 | MAPPED |
| E-537 | Reflection at Nonlinear Compression Limit | Candidate reflection/reversal at a limiting boundary. | E-536, F-606 | MAPPED |
| E-538 | Jet / Ejection Boundary Release Candidate | Kept separate from the compression node so one unverified claim does not promote the others. | E-536, E-537 | MAPPED |

## F-Series — Interaction Primitives (12 entries)

| ID | Name | Intended claim | Dependencies (proposed) | Status |
|---|---|---|---|---|
| F-609 | Moving Wake | Traveling organized field disturbance left by a translating/rotating persistent mode. | A-115 (already defines the static form), A-126, F-604 | MAPPED — see Chapter-Pass Finding 1 |
| F-610 | Leading/Trailing Wake Geometry | Geometry descriptor only; does not hardcode speed-up/slow-down. | F-609 | MAPPED — see Finding 1 |
| F-611 | Wake Phase Encounter | Local response depends on encounter phase and relative trajectory. | F-609, D-420 | MAPPED — see Finding 1 |
| F-612 | Wake Superposition / Interaction | — | F-609, F-605 | MAPPED — see Finding 1 |
| F-613 | Wake Assimilation into Parent Field | — | F-609, A-126 | MAPPED — see Finding 1 |
| F-614 | Nested Wake Coupling | — | F-613, A-127 | MAPPED — see Finding 1 |
| F-615 | Phase-Coherent Repeated Interaction | — | D-420, D-421 | MAPPED |
| F-616 | Phase-Decoherent Repeated Interaction | — | D-420, D-422 | MAPPED |
| F-617 | Differential Momentum Exchange | — | F-602, C-327 | MAPPED |
| F-618 | Differential Energy Exchange | — | F-602, C-332 | MAPPED |
| F-619 | Common-Mode Rejection | Shared motion/field contribution rejected by a differential measurement. | C-328, F-602 | MAPPED |
| F-620 | Bidirectional Propagation / Reinjection | Forward and return channels as a coupled physical loop. | F-607, C-325 | MAPPED |

## G-Series — Evaluation, Modulation & Governance (20 entries)

| ID | Name | Intended claim | Dependencies (proposed) | Status |
|---|---|---|---|---|
| G-724 | One-Wave Relational Solver Rule | The minimal universal runtime: sample local slope → sample reference slope → subtract → update relation. | A-118, G-706 | MAPPED |
| G-725 | Reference Selection Rule | Defines which containing relation supplies the reference at each scale. | A-119, A-125 | MAPPED |
| G-726 | Field-Context Before Interpretation Rule | No node evaluates data outside the currently selected field. | A-122, G-701 | MAPPED |
| G-727 | Differential-Only Observation Record | Store what changed relative to reference, not pretend an absolute state was measured. | A-118, G-706 | MAPPED |
| G-728 | Point–Path–Field State Record | Every evolving entity keeps the three-part state. | A-120, A-121 | MAPPED |
| G-729 | Resonance Detector | Identifies persistent phase correlation without presupposing a resonance label. | D-420, G-706 | MAPPED |
| G-730 | Emergent-Orbit Test | Orbit is an output pattern, never a hardcoded behavior. | G-736, D-427 | MAPPED |
| G-731 | Emergent-Gravity-Assist Test | Gravity assist must emerge from the primitive. | G-730, C-333 | MAPPED |
| G-732 | Emergent-Resonance-Gap Test | Gap formation must emerge rather than being inserted. | G-730, D-426 | MAPPED |
| G-733 | Emergent-Libration Test | Stable locking/Trojan behavior must emerge. | G-730, D-425 | MAPPED |
| G-734 | Standard-Mechanics Control Run | Every One-Wave simulation runs against a control using the standard equations and identical state data. | G-706, D-412 | **DEVELOPED** — see `Nodes/G-734_Standard_Mechanics_Control_Run.md` |
| G-735 | Prediction-Difference Gate | A One-Wave mechanism does not count as new physics unless it yields a measurable departure or a simpler derivation with equal predictive accuracy. | G-734 | **DEVELOPED** — see `Nodes/G-735_Prediction_Difference_Gate.md` |
| G-736 | No Hidden Controller Rule | No orbit fixer, resonance fixer, stability target, or externally imposed steering. | G-706, D-412 | **DEVELOPED** — see `Nodes/G-736_No_Hidden_Controller_Rule.md` |
| G-737 | No Victory Without Observable Match | Simulation cannot declare success merely for staying bounded; it must hit defined quantitative observables. | G-735, G-736 | **DEVELOPED** — see `Nodes/G-737_No_Victory_Without_Observable_Match.md` |
| G-738 | Scale-Recurrence Validation | Same primitive is tested at Moon–Earth, planet–Sun, and larger nested levels. | A-127, G-737 | MAPPED |
| G-739 | Finite-Propagation Validation | Tests whether introducing finite wake propagation breaks or improves orbital agreement. | D-430, G-737 | MAPPED |
| G-740 | Relational Nonlocality Theorem Target | Formal statement of whether global-looking multi-body behavior can be generated from recursively inherited local differential relations. | A-125, C-336 | MAPPED |
| G-741 | Three-Body Silver-Bullet Benchmark | Reproduce Sun–Earth–Moon relational behavior without special-case controllers. | D-433, G-736 | MAPPED |
| G-742 | Full Solar-System Benchmark | All planets, major moons, Jupiter resonances, and long-term stability under one primitive. | D-427, D-434 | MAPPED |
| G-743 | Claim / Metaphor / Test Separation | Every new physical idea must explicitly state which part is mathematical definition, physical hypothesis, intuitive analogy, and falsification test. | G-706 | **DEVELOPED** — see `Nodes/G-743_Claim_Metaphor_Test_Separation.md` |

---

## Second Backlog Group — Not Yet Numbered: Balanced-Electronics Series

The user has flagged that the balanced-electronics work (active center
reference, opposed rails, differential LEDs, ternary `-/0/+`,
dual-reference cell, bidirectional boundaries, phase-synchronous
reinjection, hex cell, six neighbors, host+6 organelles, analog demand
bus, magnetic memory, DC→AC→RFC hierarchy) deserves its own contiguous
node series rather than being folded into C-323–C-326 or this backlog.
Most of that ground is already covered by C-323 through C-326
(Primitive Continuous Mirrored Chain, V0 Hex Cell, V0-A Engineering
Architecture, V0 Build Wiring). Anything not already covered there
(analog demand bus; explicit DC→AC→RC hierarchy as its own node) is
deferred to a future dedicated series rather than numbered
provisionally here, to avoid a second numbering collision.

## Next Steps

1. Promote MAPPED rows to DEVELOPED only as their actual reasoning is
   worked out — in dependency order, starting from whichever A-series
   and C-series primitives a given row cites.
2. Do not backfill "Definition" prose for a MAPPED row just to make
   this table look more finished.
3. Update this file's Status column in place as nodes are promoted;
   do not duplicate the tracking elsewhere.
