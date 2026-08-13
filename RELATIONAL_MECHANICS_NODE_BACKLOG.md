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

### DC/AC/RFC recursion — RESOLVED (RC -> RFC correction applied)

1. What's proposed: RFC is intentional (Rotating Field Current), not a
   typo for RC. Hierarchy: `DC -> point`, `AC -> path/oscillation`,
   `RFC -> field rotation`. "Recursion" means the Point -> Path -> Field
   structure can occur again inside, or at, the next scale — not a
   relabeling of C-324's existing three-way split.
2. Equation/mechanism: `Nodes/C-324_V0_Hex_Cell_Multicellular_Host_Architecture.md`
   has been corrected in place — its Motion section previously read "RC
   (Rotational Current)"; it now reads "RFC (Rotating Field Current)"
   with the RC->RFC correction stated explicitly in the node itself.
3. Metaphor vs. claim: C-324's version remains a proposed-build
   engineering mapping (motion regime -> rotation type), not yet tested
   in hardware — its own V0 Proof Checklist item 4 (Rotational
   circulation) is still unpassed. The recursion claim is a distinct,
   separate physical claim (the same triad recurring at nested scales),
   not yet tested at all.
4. Falsifier: inherits C-324's own V0 Proof Checklist — a recorded,
   reproducible measurement, none exists yet. The recursion claim
   specifically would need a second scale (e.g. the six-organelle host
   in C-324, or a coordinator-level cell) showing the same DC/AC/RFC
   triad measurably reappearing, not merely being asserted by analogy.
5. Nodes touched: candidate link to the backlog's Nested Point-Path-Field
   Recursion item (A-series), filed as **Scale-Specific Instance** under
   I-04 in C-324 itself — the physical/circuit-scale instantiation of
   that general recursive structure. Explicitly **not merged**: the two
   remain separately addressable until the backlog item is developed
   enough to check the mapping term-by-term (per instruction — do not
   silently merge them).

### Wake continuation through resonance

1. What's proposed, now clarified: a previously generated wake (A-115's
   `g_wake`, Finding 1 above) can be **sustained or reinforced** when
   subsequent oscillation arrives with the appropriate phase
   relationship. Two distinct sub-claims, kept separate rather than
   collapsed into one:
   - **(a) Decay suppression:** resonance reduces the wake's decay
     rate relative to its unreinforced falloff.
   - **(b) Coherent growth:** phase-matched reinjection causes net
     accumulation/growth of the wake, not merely slower decay.
   These are different physical claims and must not be treated as two
   phrasings of the same thing.
2. Equation/mechanism: none supplied yet for either sub-case. A-115's
   `g_wake` currently has no time-dependence/decay term at all (it is a
   static superposition, per Finding 1), so neither (a) nor (b) can be
   written down until a decay term is added to `g_wake` first.
3. Metaphor vs. claim: "continuation" and "reinforced" are still doing
   informal work; (a) and (b) are the two candidate literal readings,
   not yet reduced further.
4. Falsifiers, one per sub-case (not shared):
   - (a) is falsified if a resonantly-driven wake's measured decay rate
     is statistically indistinguishable from an unreinforced wake's
     decay rate under the same loss parameters.
   - (b) is falsified if phase-matched reinjection produces no
     amplitude growth beyond what continuous (non-phase-matched) input
     of the same total power would produce — i.e. it must show a
     phase-matching advantage, not just that adding energy adds energy.
5. Nodes touched, provisionally (not confirmed against source):
   `A-126`/`F-609` (wake family) for the base disturbance; `D-420`
   Resonant Phase Correlation for the phase-recurrence condition each
   sub-case requires; `D-421` Coherent Differential Accumulation is the
   closer match for sub-case (b) specifically (its `Delta_v_total`
   linear-in-N accumulation form is the same structure a coherent-growth
   wake claim would need), while sub-case (a) has no existing backlog
   analogue yet — it would need its own decay-rate-under-forcing
   treatment, not currently mapped to anything.

### The `3>1(0)1<6` dimensional sequence — partially reconciled

Clarified as relational/scaling notation, not ordinary arithmetic: two
opposed directions meeting through a shared `(0)` reference, preserving
this explicit ladder:

```text
3:1  - (0) - 1:6   -> 2D relation
6:1  - (0) - 1:12  -> 3D relation
12:1 - (0) - 1:24  -> next scale
```

with the stated rule that `1:1` alone is not a differential — the
differential exists between the opposed ratios around the shared
zero/reference.

1. What's proposed: the ladder above, read as paired opposed ratios
   around a shared center, not as a sequence of individually-scaling
   numbers.
2. Equation/mechanism, checked against existing canon: **D-411
   (Mirrored Axis Pairs and Directed Route Counts, already canonical,
   YELLOW) already writes exactly this axis form** — `-d (0) +d`, one
   mirrored axis pair with a shared reference — and its own Dimensional
   Count Ladder table already lists `3:1 axis-pair / 6:1 directed` for
   2D and `6:1 pair / 12:1 directed` for 3D. **This is a real
   convergence, not a coincidence to wave past**, but it is not an
   automatic identity either — D-411 pairs `3:1` with `6:1` (axis pairs
   vs. directed routes, a doubling relationship: `N pairs -> 2N routes`),
   while the `3>1(0)1<6` notation pairs `3:1` with `1:6` (which reads as
   a *reciprocal* ratio, not D-411's directed-route count). **These are
   not yet shown to be the same operational mapping** — one open
   question is whether `1:6` here is shorthand for D-411's `6:1`
   directed-route count (same thing, reciprocal notation) or a
   genuinely distinct reciprocal-ratio claim. Not resolved by this pass.
3. Metaphor vs. claim: the notation itself (`>`, `(0)`, `<`) is
   presentational; the operational claim, once the `3:1`/`1:6` question
   above is resolved, would be a real mathematical relation, not a
   metaphor — but it cannot be classified as either until that question
   is answered.
4. Falsifier: cannot be defined until (2)'s ambiguity is resolved.
5. Nodes touched — genuine, checked convergences:
   - **`6:1 - (0) - 1:12 -> 3D relation`** matches, almost verbatim,
     the backlog's own **D-417 "6:1 / 1:12 Rotational Closure Relation"**
     (still MAPPED) — filed independently before this clarification
     arrived. This is a real, checkable convergence between two
     independently-arrived-at statements, not asserted identity by
     naming alone; D-417 should be the first of the three rungs to
     develop, precisely because it already has two independent routes
     pointing at the same address.
   - `3:1 - (0) - 1:6 -> 2D relation` maps candidate-wise to the
     backlog's `D-415` (3:1 Point-Path-Field Coordination) and `D-416`
     (1:6 Six-Step Linear Coordination), both still MAPPED and not yet
     connected to each other.
   - `12:1 - (0) - 1:24 -> next scale` maps candidate-wise to `D-409`
     (Twelvefold 3D Close-Packed Coordination, already canonical) paired
     against `D-418` (1:24 Higher-Scale Recurrence, still MAPPED) — note
     D-410 (already canonical) uses `24:1`, not `1:24`; per instruction,
     **these are not declared identical** without the operational
     mappings actually matching, and D-410 itself already warns
     `12:1 = volumetric adjacency` is a different kind of count than
     `24:1 = recurrence/state coordination` — so a `12:1 - (0) - 1:24`
     pairing needs to state which of those two 24-somethings (D-410's
     recurrence shell, or D-418's still-undefined "higher-scale
     recurrence") it actually means, rather than assuming they match.
   - Cross-reference to B-226's six-gate cycle (`1->2->3->4(0)->5->6`,
     still MAPPED): shares the `(0)` center-mirror notation but is a
     *gate-sequence* (six ordered steps), not a *ratio-pair* structure
     like the ladder above. Per instruction, **not declared identical**
     — the two use the same symbol for what may be two different roles
     (a step index vs. a reference point) until checked term-by-term.

### Measurement-as-capture

1. What's proposed, now clarified: capture is **not** "measurement
   creates the state." The wave/field is already evolving continuously;
   measurement is a **local interaction** that captures part of that
   continuous evolution into a persistent record. The discreteness
   belongs to the capture interaction and the record it leaves, not to
   a pre-existing discrete object being found.
2. Equation/mechanism: none supplied yet — this remains the actual
   blocking item, per instruction to separate this into G-743's four
   components rather than assume novelty from vocabulary alone:
   - **(1) Mathematical definition:** none yet. What operator or
     boundary condition turns "continuous evolution" into "a record"?
     Not written down.
   - **(2) Physical hypothesis:** the local interaction (not the wave)
     is what produces discreteness; the record is a property of the
     interaction, not of a traveling object.
   - **(3) Metaphor:** "capture" itself — borrowed from ordinary
     photography/trapping language — flagged explicitly as analogy per
     instruction, carrying no argumentative weight on its own.
   - **(4) Falsification test:** none supplied yet.
3. Required check before treating this as new (per instruction, tested
   against G-706): **G-706 Validation** already defines "confirmation
   through successful participation in a cycle... validated when it
   produces a non-zero feedback signal through interaction." That is
   close in plain language to "captured into a record via interaction."
   Whether measurement-as-capture is a genuinely distinct mechanism or a
   restatement of G-706 applied to the measurement act specifically is
   **not yet resolved** — this is the first thing to check once any
   mechanism (item 1 above) is written down, not something to assume
   either way in advance.
4. Falsifier: still none — blocked on (1).
5. Nodes touched: `A-122` Field/Void Primitive (still MAPPED) remains
   the right eventual address, unchanged from prior discussion. Also to
   be checked once developed: `A-101` Ground/Zero (measurement requires
   a reference state), `C-301` Mirror Gate (crossing/resolution events
   already exist as a general mechanism), and `G-706` Validation (per
   item 3 above — the closest existing candidate for overlap, must be
   ruled in or out before this is filed as new rather than restated).

### What this section does not do

It does not assign new C-, D-, or G-series IDs to any of the three
still-open items (wake continuation, `3>1(0)1<6`, measurement-as-
capture). DC/AC/RFC's correction was applied directly to the
already-existing C-324 rather than creating a new ID, since it was a
factual correction to committed content, not a new claim.
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
| D-417 | 6:1 / 1:12 Rotational Closure Relation | — | D-409, D-416 | **RETIRED** — original counting claim already covered by D-409/D-411 (now cross-referenced directly); no node built. See D-417 Evidence Dossier below for the surviving Twelve-Neighbor Spatial Rotational Closure candidate, held separately and still unassigned. |
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

## D-417 Evidence Dossier

D-417 was picked as the next development candidate given the
independent convergence noted in the `3>1(0)1<6` reconciliation above.
Its backlog row never carried an intended-claim sentence — the column
was blank from the start. Rather than invent one, this dossier
exhausted what the repository already says about "6:1," "12:1," and
"closure," tested each hit for contradiction or duplication under
I-04, and reports the result: **D-417's original 6:1/12:1 meaning is
retired as already covered** (cross-references added to D-409, D-411,
and G-716 directly); **no node was built for that original meaning.**
One genuinely new, non-redundant question surfaced during the
exhaustion — whether D-409's twelve-neighbor shell has its own
discrete rotational symmetry — and has since been investigated
directly against the geometry (see below), independent of D-417's
retired meaning.

### What already exists

**1. D-409 (already canonical, GREEN) already states the 6:1/12:1
pairing D-417's title names.** Verbatim: "The twelve directed neighbor
positions may be organized into six opposite coordinate pairs for a
declared shell mapping. This gives a `6:1` mirrored-pair view and a
`12:1` directed-neighbor view, controlled by D-411." D-411's own
Dimensional Count Ladder table lists the identical pairing for the "3D
close-packed shell" row. **This is not a new relation to derive — it
is already derived, in two already-canonical nodes.**

**2. G-716 (already canonical, BRONZE — the highest-proven gate
anywhere in this backlog's neighborhood) already uses notation nearly
identical to the `3>1(0)1<6` string this pass has been reconciling.**
G-716's full core pattern: `24 > 1(0)1 < 12 > 1(0)1 < 6 > 1(0)1 < 3 >
1(0)1 < 1 > 1(0)1 < 24`. Read one segment in the direction opposite to
how G-716 states it (`6 > 1(0)1 < 3` reversed is `3 > 1(0)1 < 6`) and
it is the same gate G-716 already walks between its "6" and "3"
conversion layers. G-716's own ratio expression line spells out
`12:1 -> 6:1 -> 3:1 -> 1:1 -> 1:24` — essentially the full D-415–D-418
ladder, already present in a Bronze node, just never cross-referenced
to those still-MAPPED D-series IDs.

**3. G-716 places its own explicit guardrail directly on this
overlap**, under its Dimensional Boundary section: "The labels 24, 12,
6, 3, and 1 are recursive conversion layers in this grammar. They are
not automatically spatial dimensions or nearest-neighbor counts.
Physical or geometric uses must declare their mapping under A-117."
That is the same warning D-411 gives for its own ratios ("same ratio
≠ same domain"). **Any D-417 development must therefore state
explicitly whether it is extending G-716's abstract conversion-layer
sense of "6" and "12," or D-409/D-411's literal spatial-neighbor
sense — not assume they are the same because the numbers match.**

**4. "Closure" already has a real, different, already-canonical
meaning in this repository, at a different number.** C-301 Mirror
Gate and C-308 Spin-half (both GREEN, both real math) define `M^4 = I`
as "4π closure" — the Mirror operator returning to identity after four
applications, giving spin-half's defining property. This is an actual
derived rotational-closure result already in the repository — but its
closure number is **4**, not 6 or 12, and its domain is an internal
two-component `(psi_C, psi_E)` state, not D-409's spatial lattice
shell. Per I-06's Duplicate-Name Rule, if D-417 is ever built and
titled with "closure" in it, it will collide in name with C-301/C-308
without being the same mechanism, and will need a
`DUPLICATE_NAME_DISAMBIGUATION.md` entry at that time — not now, since
D-417 has no real node file yet for the registry to reference.

**5. B-221 (Six Recursive Steps, already canonical, YELLOW) already
flags an unresolved tension directly relevant to "rotational" in
D-417's title.** B-221's own dependency line names two unreconciled
candidates for its LOOP step: "A-111 Recursion (LOOP's candidate 1 for
G — additive, unreconciled with candidate 2), C-301 Mirror Gate
(LOOP's candidate 2 for G — rotational, unconfirmed, see LOOP
section)." That is an existing, open, already-flagged
additive-vs-rotational question sitting inside a canonical node — not
something D-417 would be introducing for the first time.

### The "six" ambiguity web (why this matters)

D-411 already states "same ratio ≠ same domain" as a hard rule. The
literal number 6 already carries at least four separate, non-identical
established meanings in this repository before D-417 exists:

```text
B-221    6 = abstract recursive-cycle step count (Six Recursive Steps)
D-408    6 = literal 2D lattice nearest-neighbor count (6:1 coordination)
D-411    6 = directed-route count derived from 3 axis pairs (6:1 view)
G-716    6 = a conversion-grammar layer label ("paired structural compression")
```

D-417 sits precisely at the point most likely to accidentally conflate
two or more of these. That is the specific risk this dossier exists to
flag before any equation gets written, not after.

### I-04 disposition, as far as the evidence supports it

- D-417's proposed 6:1/12:1 pairing vs. **D-409/D-411's existing
  6:1/12:1 pairing**: not yet distinguishable from **Duplicate** —
  the counting relationship these would state is already fully stated.
  If D-417 has nothing to add beyond this counting relationship, it
  does not need a new node; it needs D-409 and D-411 cross-referenced
  from wherever "Rotational Closure" was going to be cited instead.
- D-417's "Rotational Closure" vs. **C-301/C-308's 4π closure**: not
  Duplicate (different number, different domain) and not confirmed as
  **Architectural Homology** either (no operational mapping shown
  between an internal 2-component Mirror state and a 12-neighbor
  spatial shell). Filed as **Analogy Only** at most, pending an actual
  proposed mapping — and even that is this dossier's inference, not a
  claim the backlog makes on its own authority.
- D-417 vs. **G-716's conversion-layer 6 and 12**: same disposition —
  **Analogy Only** pending an explicit statement of whether D-417
  means the same "6"/"12" G-716 already uses, or a distinct spatial
  sense.

### Disposition — D-417's original meaning is RETIRED

Per explicit instruction, D-417's original 6:1/12:1 counting claim is
retired from the backlog as already covered, not developed as a new
node. The missing cross-references have been added directly to the
canonical nodes rather than left implicit:

- `Nodes/G-716_One_Wave_Conversion_Grammar.md` — added D-409 and D-411
  to its Dependencies (Lateral), and a sentence in its own Dimensional
  Boundary section stating D-409 governs the 12:1 spatial meaning and
  D-411 governs the 6:1/12:1 counting distinction, with an explicit
  "not merged" note.
- `Nodes/D-409_Twelvefold_3D_Close_Packed_Coordination.md` — added a
  reciprocal Lateral cross-reference to G-716.
- `Nodes/D-411_Mirrored_Axis_Pairs_and_Directed_Route_Counts.md` —
  added a reciprocal Lateral cross-reference to G-716.

No node ID was assigned for the retired counting claim. D-417's row in
the D-Series table above is marked retired accordingly.

### The surviving question — Twelve-Neighbor Spatial Rotational Closure (verified, still not assigned a node)

This is preserved separately from D-417's retired meaning, per
instruction, and has now actually been investigated rather than left
as inference — using D-409's own geometry directly, without borrowing
C-301's `M^4=I` result and without assuming the 6/12 counts imply
rotational periodicity.

**Method:** D-409 defines `N_12 = (a/sqrt2){(+-1,+-1,0), (+-1,0,+-1),
(0,+-1,+-1)}`, twelve explicit points. A numerical script
(`Integrity_Tools/verify_d409_rotational_closure.py`) constructs this
exact point set and searches directly for which 3D rotations map it
onto itself, rather than assuming a textbook answer.

**Operator:** not a single distinguished operator (unlike C-301's one
`M`). The full set of rotations preserving `N_12` forms a group; three
rotation-axis families exist — 3 four-fold axes (through opposite
square faces), 4 three-fold axes (through opposite triangular faces),
6 two-fold axes (through opposite edges) — matching the point set's
inherited cube/octahedron symmetry, since `N_12` is exactly the set of
cube edge-midpoints.

**State space:** `N_12`, the twelve points D-409 already defines, as a
subset of R^3.

**Order:** the full rotation group has order **24** (verified by
generating it numerically from a 4-fold and a 3-fold element and
checking closure), isomorphic to S4. Individual element orders present
are **only 1, 2, 3, and 4** — confirmed by direct search over all
z-axis rotation angles from 1 to 359 degrees, of which only 90, 180,
and 270 preserve the set. **No order-6 or order-12 rotation exists for
this shell.** The naive reading implied by D-417's original title —
that 12 neighbors suggests 12-fold rotational closure — is
numerically false for this specific geometry.

**Invariants:** the full 12-point set is invariant (as a set, not
pointwise) under all 24 group elements. Under a single 4-fold axis
rotation, the 12 points split into three orbits of 4; under a 3-fold
axis, into orbits of 3; under a 2-fold edge axis, two points lie on
the axis itself (fixed, orbit size 1) and the rest split into orbits
of 2.

**Failure / what this does NOT show:** (1) this is a property of the
idealized geometric point set only — it says nothing about whether any
actual lattice dynamics in this repository respects, uses, or is
constrained by this symmetry; (2) a physically-motivated departure
from the idealized cuboctahedral shell (anisotropic coupling, a
perturbed lattice) could reduce the symmetry group and change these
numbers; (3) this shows a rotation of order 4 *exists* among the
shell's symmetries — the same order as C-301's `M^4=I` — but this
script makes no claim that they are the same rotation, the same
mechanism, or related at all; that would require an actual proposed
mapping between the internal `(psi_C, psi_E)` Mirror state and this
spatial shell, which does not exist. C-301 itself already flags the
analogous open question for its own mechanism ("whether mirror
crossing is forced by One-Wave geometry or defined as a boundary rule
remains open").

**Whether this earns a node:** per instruction, a node is earned if
the geometry yields a defensible group action and closure derived from
the geometry itself, not chosen because 6 or 12 looks appealing. That
condition is met — the derivation above is reproducible
(`python3 Integrity_Tools/verify_d409_rotational_closure.py`) and does
not select its answer to match 6 or 12; it found 24, which contradicts
the appealing reading. Node assignment itself is left open rather than
done in this pass, consistent with how every other promotion decision
in this backlog has been handled — this is flagged as ready for that
decision, not made unilaterally here.

### B-221's rotational-vs-additive LOOP tension — flagged for later reconciliation, not resolved here

Per instruction, this is noted and left open rather than addressed in
this pass. B-221 already names A-111 (additive) and C-301 (rotational)
as its two unreconciled LOOP candidates. The rotational-closure work
above does not resolve that tension — it investigates a different
rotation (the spatial shell's symmetry group) from C-301's own
mechanism, and does not bear on which of A-111 or C-301 is the correct
grounding for B-221's LOOP step. That reconciliation remains B-221's
own open item, unchanged by this dossier.

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
