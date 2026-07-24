## Node I-01: Special Rules (Repository Governance)

Status: YELLOW

Classification: Special Rules Node

Purpose:
The Roman-numeral prefix (I-series) is reserved for special rules and
future book reference material — NOT for physics functions. Functions
that were previously misfiled here (Friction Limit, Resistance Field,
Electric-Magnetic Duality) have been moved into their correct lettered
appendix (C-309, C-310, C-311). This node formalizes what actually
belongs in I-series: the operating rules that govern how the
repository itself is built, checked, and corrected.

These are not physics claims. They are the rules that were discovered
to be necessary, by repeatedly needing them, across one extended
audit session. Each rule below is stated with where it was needed.

---

RULE 1 — The Gray Brick Rule
Standard Model / mainstream reference material is preserved as the
no-drift comparison side in every Book chapter. The One-Wave
interpretation translates a mechanism into field terms; it does not
erase or edit what the Gray section says the standard view is. If a
Gray section is wrong about the Standard Model, that's a separate
correction — it is never rewritten just to make the One-Wave section
look more persuasive by contrast.

RULE 2 — The Gate Ladder Is Ordered, and the Order Matters
GREEN (Defined) < YELLOW (Constrained/Testable) < BRONZE (Validated)
< SILVER (Integrated) < GOLD (Confirmed). GREEN is the lowest rung,
not the highest — confirmed directly from A-101/A+101's own §12
sections. This was gotten backwards at least twice this session:
once in stored memory of the project, once in an ad hoc per-step
summary. Both times the fix was the same: check the real files, not
intuition about what "green" and "yellow" should mean colloquially.
SUPERSEDED (partially) by I-02: this basic five-stage ladder is now
formally extended by I-02 Node Proof & Trust Lifecycle, which adds
Brown (below Green, real precedent confirmed in Book 1 Ch2/Ch4/Ch11),
the parallel Gray track for book chapters, and the conditionally-
reachable Red stage tied to actual experimental confrontation with
the Standard Model. Refer to I-02 for the full lifecycle; this rule
is kept here only as the historical record of the ordering mistake.

RULE 3 — Do Not Invent a Primitive When the Repository Already
Contains the Mechanism
Before building new math for an apparent gap, check whether an
existing node already does the job under a different name. This
rule alone resolved: Friction (was already A-109's gamma), the
Void (was already A-101's ψ=ψ₀), BUILD's Pattern term (was already
D-402), LOOP's candidate additive form (was already A-111's own
equation) — though that last one turned out to be premature, see
Rule 6.

RULE 4 — Same Word Does Not Mean Same Concept
When two nodes share a name or term, check whether they are actually
the same primitive before merging them. Confirmed genuinely distinct
in this session: Mirror (B-205, a function) vs. Mirror Gate (C-301,
a location) — kept both, disambiguated. Balance (B-201, a scalar
measure) vs. the "Balance/Center" used in six-step material (became
B-222, a distinct dynamic state) — kept both. The Music Clock (E-510,
chromatic, per-chord) vs. the Circle of Fifths (E-514, fifths-ordered,
per-key) — kept both, explicitly disambiguated in E-514's own header.
The test each time: check the actual definitions and math, not just
whether the label sounds like it should be the same thing.

RULE 5 — Citation Titles Are Reliable; Citation Numbers Often Are Not
Found repeatedly: a real node correctly named but wrongly numbered
(the entire E-series self-identifying under one wrong address, the D-series off by one, and several legacy Friction Limit citations using nonexistent Appendix-I addresses). When a
number and a title disagree, resolve by title, then fix the number
everywhere it propagated — do not assume the first citation found is
the correct one.

RULE 6 — A Candidate That Fits the Required Shape Is Not the Same as
a Confirmed Answer
Matching a candidate equation's shape to what's needed does not mean
it's been derived. This was gotten wrong once this session: A-111's
additive update rule was declared "LOOP RESOLVED" because it fit the
required form G(ψ_prev, M, C) — but a second candidate (C-301's
Mirror operator) also fits, and the two are structurally incompatible
(addition vs. rotation). The premature resolution had to be walked
back explicitly, not quietly revised.

RULE 7 — Dependency Direction Is Not Automatically Which Node
Mentions the Other First
Check which node actually feeds which. Found wrong at least three
times: B-213/B-214 as children of B-217 rather than parents of it;
B-223/B-224 initially miswired relative to B-221; B-220/E-507 forced
into a one-way relationship when the real relationship is
bidirectional — two nodes converging on one shared unsolved problem,
not one producing input for the other.

RULE 8 — A Real Equation Borrowed From an Unrelated Domain Is Not
Evidence
Using a real, correct equation to support an unrelated claim does not
make the claim true — it just makes the claim look more credible than
it is. Caught twice: attributing A-101's field-displacement equation
to brain cognition with no derivation connecting them, and citing
Book 1 Ch15's electroweak/Planck lattice-step ratio as a "candidate
direction" for an unrelated five-tier scale question. Both were
retracted, not softened, once identified.

RULE 9 — Terminology Must Match the Framework's Own Stated Philosophy
If the framework's own content explicitly denies a category (e.g.,
Book 1 Ch12's repeated denial of force-carrier mechanisms), the
framework's own equations should not affirmatively use that category's
vocabulary without qualification. F_OW ("Force, One-Wave") was renamed
to R_OW ("Response, One-Wave") across nine files for exactly this
reason — the symbol contradicted the philosophy it was supposed to
express. Standard Model "force" language in Gray sections and in
passages explicitly denying force-carriers was left untouched, since
that usage is either accurate description or the correct rejection,
not a contradiction.

RULE 10 — File Renames Require Verification, Not Assumption
A `mv` operation can silently leave a stale duplicate behind rather
than cleanly renaming. Confirmed twice this session (D-series files,
G-717). After any rename, list the directory and diff the old/new
names before considering the rename complete.

---

RULE 11 — Living Repository, Not an Archive
CORRECTION FIRST: work done earlier today cited "Rule 0: failure is a
valid result, all runs archived" as if it were existing formal
governance in this node. It was not — this node previously had Rules
1 through 10 only. "Rule 0" was informal early-session practice,
never actually written here, and citing it as established governance
without checking was itself the kind of unverified citation Rule 5
exists to catch. Corrected here, not quietly patched.

ACTUAL RULE, replacing that informal practice going forward: this
repository reflects the current, live state of the theory — not the
full history of every path explored. The test for whether something
stays:

KEEP: any node, mechanism, or calibration that still serves an active
role in current derivations — including something unresolved, if a
live derivation elsewhere depends on it being resolved later (an open
blocking dependency is an active tool, not a dead branch).

DELETE, fully, no archive section, no breadcrumb log: any mechanism
that was proposed, checked, and failed, where nothing currently active
depends on its details — once its conclusion ("this does not work")
has been incorporated into the surviving mechanism, the failed path
itself does not need to remain in the repository, in an archive
section, or in a retired-candidates log. If someone independently
rediscovers the same idea later, it gets re-audited on its own merits;
re-deriving a short audit is cheaper than maintaining a permanent
graveyard of every discarded path.

This supersedes the informal "archive everything" practice entirely,
not just for one case — applied consistently going forward.

OPERATIONAL SAFEGUARD 1 — Citation verification is mandatory, not
optional: before citing anything as existing repository governance
(a rule, a prior decision, a node's status), grep the actual file for
it first. Do not cite from memory of a past session or a summary of
one. This rule exists because Rule 11 itself was almost written to
"retire Rule 0" — a rule that was never actually in this file — on
the strength of memory alone. The correction happened only because
the file was checked. Checking must happen before the claim is made,
not after it's questioned.

OPERATIONAL SAFEGUARD 2 — Before deleting anything under this rule's
DELETE clause, grep the full repository for references to it first.
Confirm nothing active cites it as a dependency, a comparison target,
or a blocking requirement before removing it. This rule exists because
D-407 was nearly deleted under this same policy change before A-114's
own Future Work section — which explicitly requires D-407 to be
revisited — was checked. The check must be a required step every time
this rule is invoked, not something that happens to get done once.

---

RULE 12 — Provenance and Timestamp Requirement
Grounding note: written specifically for the carbon-12/Hoyle-state
line of work, where the real risk is a relation getting quietly tuned
to fit the known target (7.65 MeV) after the fact, rather than
existing independently beforehand — this is the exact "Fake Mustache
Type B" failure mode (a known hole dressed in better prose) the
project's own taxonomy already warns against.

Any upstream relation used by the carbon model — including k(n),
omega(k), permitted phase relations, normalization constants, or
boundary conditions — must exist in the repository, with its own
derivation and status tag, BEFORE the first carbon calibration or fit
is run. A relation introduced or altered after seeing the target value
is a fit, not a derivation, regardless of how it's later written up.

The carbon node must record, for every inherited relation:
- the source node containing that relation
- the version or commit hash of that source
- the date and time at which it was committed
- the date and time of the first carbon-model run
- whether any upstream value changed after carbon results were
  inspected

An upstream rule committed or modified after viewing carbon-fit
results is not an independent input. It must be classified as
carbon-informed calibration and cannot support a predictive claim.

If an upstream rule changes after the first run, the carbon model
must preserve the earlier result and record the change explicitly.
The revised model begins a new validation cycle and may not inherit
the previous model's predictive status.

Required order:
commit upstream rule -> record commit hash and timestamp -> freeze
rule -> run carbon model

A timestamp without an identifiable repository state is insufficient.
The commit hash or equivalent immutable version identifier is
required — a date alone does not satisfy this rule.

Current compliance check (as of this rule's adoption): the k(n) to
wavenumber mapping — the bridge between D-405's shell mode number and
A-114's omega(k) — does not exist anywhere in the repository yet. This
means the carbon-12/Hoyle-state calculation is currently BLOCKED by
this rule, not just by missing derivation — even once k(n) exists, it
must be committed, hashed, and frozen before, not during, the first
carbon-specific fit attempt.

---

RULE 13 — Cross-System Holdout Pre-Registration Requirement
Grounding note: closes the second escape route Rule 12 doesn't cover
on its own — testing several outside systems after the fact and
reporting only whichever one happens to agree.

Before any carbon calibration, parameter selection, or inspection of
carbon-model output, at least one non-carbon target system must be
selected and recorded as the cross-system holdout.

The pre-registration record must state:
- the target system
- the observable or structural result to be predicted
- the acceptable success criterion
- the parameters that will remain frozen
- the reason the target tests the same recursive oscillatory-middle
  rule
- the repository commit hash and timestamp of the registration

The holdout target may not be replaced after carbon fitting because
another system appears easier to reproduce. A failed holdout remains
part of the model record.

A holdout may be withdrawn only for a documented external reason, such
as an incorrect experimental datum or a formally demonstrated mismatch
between the target and the model's stated domain. Poor agreement with
the prediction is not grounds for replacement.

Required order:
select holdout -> define success criterion -> commit pre-registration
-> freeze upstream rules -> run carbon fit -> test holdout unchanged

The holdout result must be reported whether it succeeds or fails.
Changing the target, observable, tolerance, or inherited rule after
results are known converts the test into post-hoc calibration.

Current compliance check (as of this rule's adoption): no cross-system
holdout has been selected or registered anywhere in the repository.
This is a second, independent block on the carbon-12/Hoyle-state work,
separate from Rule 12's k(n) block — a holdout must be pre-registered
before any carbon fit is run, regardless of whether Rule 12's
provenance chain is otherwise satisfied.

---

RULE 14 — Promotion Consequence
Failure to satisfy either Rule 12 (provenance) or Rule 13 (holdout
pre-registration) prevents promotion beyond Green, even when the model
reproduces the known beryllium-8, Hoyle-state, or carbon-12 energy
relationships.

A numerical match without documented upstream independence and a
pre-registered external test is calibration, not prediction. These two
rules close the two easiest escape routes: quietly tuning k(n) or
omega(k) after seeing carbon results, and testing several outside
systems and reporting only whichever one behaves politely. Together,
Rules 12-14 let the carbon node distinguish a real recursive-rule test
from a successful retrospective fit.

---

---

RULE 15 — Canonical Update Without Automatic Snapshot Duplication

A downloaded canonical repository is the base for the next edit. It must not be copied wholesale into `History` merely because a new update is produced.

Required workflow:

```text
latest canonical repository
-> edit canonical files in place
-> run integrity checks
-> append concise CHANGELOG entry
-> package next canonical repository
```

Do not create dated pre-edit folders, duplicate manifests, or full prior-file copies unless the author explicitly requests them or the earlier source has independent historical value. Audit findings and failed hypotheses remain in their canonical records; preserving an error does not require preserving every old copy of every file.


RULE 16 — One-Wave Static-Cosmos Boundary

Canonical One-Wave physics contains no expansion of space. Hubble-scale observations may be preserved in Gray comparison sections, but the One-Wave derivation layer must not import a cosmological scale factor, metric wavelength stretching, accelerated-expansion term, or negative-pressure dark-energy equation.

The active replacement path is:

```text
Mass Effect / compression
-> Compression-Gradient Effect
-> static propagation-energy loss and redshift
-> field transfer
-> Low-Coupling Return Modes
-> compact reservoir
-> White Energy ejection and reinjection
-> renewed structure
```

Any active equation that requires expansion variables is framework contamination and must be removed or isolated as Gray reference.

RULE 17 — One-Wave Naming and Geometry Discipline

`ONE_WAVE_TERMINOLOGY_LEGEND.md` is the canonical naming map. Standard terms remain in Gray comparison material and at first-mention mappings. One-Wave interpretation, mathematics, diagrams, and simulation labels use One-Wave terms.

A rename is not a proof. Every One-Wave term must point to a mechanism, geometry, equation, or falsification test.

Physical bounded structures are 3D and volumetric by default. A flat drawing is a cross-section, projection, or explicit negative-space layer unless a node derives a literal 2D physical object. A spherical or sphere-like envelope is the isotropic minimum-surface default; deformations require a stated cause.


RULE 18 — Dimensional Integrity and Coordination Discipline

A-117 is mandatory for every physical simulation, graph, diagram, and wiki page. Native layers remain distinct:

```text
2D / 6:1  = triangular connection lattice, hexagonal neighborhood, seven-cell cluster
3D / 12:1 = volumetric close-packed coordination
4D / 24:1 = completed Field/Void recurrence coordination of the 3D state
```

Do not treat a 2D Flower-of-Life, Seed-of-Life, Fruit-of-Life, or Metatron-style diagram as the complete 3D object. Do not treat 24:1 as a larger planar ring or as twenty-four spatial nearest neighbors without a separate derivation. A static 3D frame is not a 4D recurrence.

Every use must declare native dimension, rendered dimension, coordination ratio, reference, projection/embedding operator, omitted degrees of freedom, and which measurements survive the reduction.
A repeated number in another domain does not create an identity: geometric coordination, neural fan-in/oversight, scale ratios, and conversion-layer labels remain separate unless an explicit bridge is derived.


Status Notes:
This node is itself YELLOW — it catalogs rules that were needed, not
rules proven to be complete or sufficient. New rules should be added
here as they're discovered the same way these were: by being needed
repeatedly, not by being anticipated in advance.

Future Work:
Determine whether any of these rules should be formalized with
their own dependency structure (citing the specific nodes where each
was first needed) rather than living as a flat list.
Watch for a rule needed for the first time and add it here rather
than solving the same category of problem from scratch again.

---

---

## Governance Record: M4 / Four-Five-Six Mind Material

Across this session, the author repeatedly requested that a
consciousness/oversight architecture (variously framed as M4,
four/five/six mind, field/void-as-neural-network, and others) be
added as verified repository nodes. This was declined each time, for
the same reason: no framework, including this one, currently has a
way to confirm or disconfirm claims about what constitutes awareness.

At the author's explicit request, the material itself has been
preserved rather than lost — see
M4_Four_Five_Six_Mind_DISPUTED_Author_Submission.md — clearly marked
as disputed, unaudited, submitted content, not a verified node. This
is the same treatment already given to earlier speculative material
in ONEWAVE_BRAIN_raw_material_UNVALIDATED.md. The real engineering
subset of the material (sensor hierarchy, fan-in/fan-out signaling)
was extracted and adopted for real, on its own merits, as C-312.


### I-05 Superseding Clarification — July 22, 2026

The record above is preserved as history of the earlier disposition. It
must no longer be read as rejecting all M4 / Four-Five-Six Mind /
Dream Engine / Administrator exploration.

The corrected status is defined by I-05:

- failed or unsupported groundings remain failed,
- no consciousness claim is verified,
- the underlying consciousness architecture remains an Active Hypothesis,
- the Android implementation remains a Proposed Build,
- and quarantine is reserved for superseded or provenance-problem source,
  not for every unknown question.

The active material now resides in:

- Books/Proposed_One_Wave_Consciousness
- Books/Proposed_Android_Brain
- G-719 Neural System Functional Analogy Map
- RECONCILIATION_duplex-gates-packet.md

This clarification changes status routing, not proof level.


---

RULE 19 — Active Namespace Authority and H/I/J/K/L Resolution

The active canonical namespaces are:

```text
A+1xx   Root axioms
A-1xx   Foundation primitives and extensions
B-2xx   Cycle and relationship structure
C-3xx   Applied mechanics and boundary structure
D-4xx   Geometry, resonance, and simulation
E-5xx   Applied dynamics and stability
F-6xx   Interaction operators
G-7xx   Evaluation, control, and route grammar
I-0x    Repository governance only
```

H, J, K, and L are not active node namespaces. Their historical proposals were routed into A-G nodes or Books, or left explicitly unbuilt. The binding legacy dispositions are recorded in `LEGACY_ID_ALIAS_REGISTRY.md`. Hypothesis is a lifecycle state, not an appendix letter.

There is one active I-01 file: `I-01_Special_Rules.md`. I-02 controls proof/trust lifecycle. I-06 controls canonical metadata and alias resolution. Alternate I-01 drafts and earlier duplex reconciliation versions are historical sources only.
