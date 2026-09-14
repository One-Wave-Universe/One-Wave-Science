# ONE-WAVE CORE RULES — LOCKED

Status: **IMMUTABLE PROJECT CONSTITUTION**

These rules are not ordinary documentation. They are the fixed reference boundary for One-Wave work.

## Lock Rule

- Do not replace these rules.
- Do not rewrite these rules.
- Do not weaken these rules.
- Do not silently reinterpret these rules.
- Do not delete these rules.
- Do not move these rules into another file and change their meaning.
- AI agents, checkers, editors, scripts, and cleanup passes may **reference** this file but may not alter it.
- A downstream chapter, node, proof, simulation, or experiment that conflicts with a core rule is the thing that must be marked for review. The core rule is not changed to make the downstream work fit.
- This file may be finalized before initial adoption. After adoption on `main`, changes to the core are outside normal update flow and require an explicit constitutional reset rather than an ordinary content edit.

## Core Rule 1 — Reference Before Interpretation

Every scientific claim begins from the nearest accepted observation, equation, dataset, or experimentally successful reference model before a One-Wave interpretation is added.

Gray / Standard Model reference is never omitted where applicable.

One-Wave does not erase accepted measurements. It proposes a different underlying interpretation or mechanism and must be compared against the same measured target.

## Core Rule 2 — Same Target, Different Explanation

One-Wave must reproduce successful measured predictions before claiming to replace the ontology used to explain them.

A different story that does not recover the accepted numerical result is not yet a replacement theory.

## Core Rule 3 — Evidence Does Not Transfer Automatically

Evidence for the observed phenomenon is not evidence for the One-Wave explanation of that phenomenon.

Standard references establish the target. One-Wave validation requires its own derivation, reproducible calculation or simulation, experimental receipt where possible, and explicit comparison against the accepted result.

## Core Rule 4 — No Analogy As Proof

Similarity, geometry, visual resemblance, repeated patterns, or cross-scale analogy may generate a hypothesis but do not establish one.

Claims across scales require declared variables, transformation laws, measurable invariants, and controlled comparison.

## Core Rule 5 — No Reverse Fitting

A free coefficient may not be adjusted only to reproduce a known answer and then presented as a derivation.

Every free coefficient must be derived upstream, independently measured, or clearly labeled as a fitted parameter.

## Core Rule 6 — Definitions Stay Fixed During Testing

The same primitive, field, state, reference, loop, excitation, displacement, boundary, rotation, coupling, and return terms must keep the same defined meaning across chapters unless a separate explicitly named derived quantity is introduced.

A definition may not quietly change between gravity, particle, cosmology, biology, hardware, or measurement work in order to rescue a result.

## Core Rule 7 — Unknown Means Unknown

Unresolved claims remain YELLOW / OPEN.

A later chapter depending on an unresolved claim does not promote that claim to established status.

Failed calculations and failed experiments remain visible. They are not rewritten as successes.

## Core Rule 8 — Repository Reference Beats AI Memory

Before changing a scientific definition or extending a node, read the nearest authoritative repository reference.

AI memory, conversational summaries, inferred intent, and generated prose do not override the repository's locked definitions.

If memory and repository disagree, the repository is the reference and the conflict must be surfaced.

## Core Rule 9 — No Silent Drift

Definitions remain authoritative until formally superseded by an explicitly named new derived definition that does not rewrite this locked core.

Cleanup work may remove duplication or stale commentary, but it may not compress away distinctions, uncertainty, equations, dependencies, failed tests, or reference comparisons that change scientific meaning.

## Core Rule 10 — Every Serious Claim Gets a Kill Test

A mature claim must state what result would falsify or narrow it.

Where applicable, a completed claim should end with:

1. a dimensional equation set;
2. a reproducible calculation, simulation, or experiment;
3. comparison against the accepted dataset or result;
4. uncertainty or tolerance bounds;
5. an explicit pass / fail / unresolved outcome.

## Core Rule 11 — No Particle-First Assumption In One-Wave Work

Within the One-Wave hypothesis, what standard physics calls a particle is treated first as a localized, persistent, or propagating field excitation / mode to be derived and measured.

This is a One-Wave working ontology, not permission to ignore particle-physics measurements. The model must still reproduce the measurements normally described using particles.

## Core Rule 12 — Measurement Is A Physical Interaction To Be Derived

Measurement is treated as a physical coupling between an incoming field pattern and a detector / boundary response.

No collapse, observer effect, entanglement replacement, or detector rule may be declared solved until it reproduces the relevant standard measurement statistics and Bell / interference constraints where applicable.

## Core Rule 13 — Cosmology Does Not Assume Expansion By Default

Within One-Wave cosmology, expansion of space is not a starting assumption.

Redshift, distance behavior, time dilation, surface brightness, structure observations, orbital behavior, and other cosmological data must be treated as measured targets and tested against explicit One-Wave mechanisms.

"No expansion" is therefore a working hypothesis to be tested, not permission to ignore observations that standard cosmology explains with expansion.

## Core Rule 14 — One Field Means One Consistent Field

One-Wave uses one field as the primitive working object. The field may support localized modes, traveling modes, boundaries, interference, rotation, coupling, return, and persistent structures, but these behaviors must come from a consistent rule set rather than chapter-specific replacements.

## Core Rule 15 — Reference At Every Step

For every nontrivial change:

**reference -> difference -> change -> test -> compare -> drift check**

If the same approach fails three times, change angle rather than repeating the same unsupported assumption.

## Core Rule 16 — Core Rules Before And After Every Update

Every repository update must explicitly reference this locked core **before** work begins and explicitly check against this locked core **after** work ends.

The pre-update reference must identify:
- the relevant core rule numbers;
- the authoritative node / chapter / math reference being changed;
- the exact difference being addressed.

The post-update check must state:
- which core rules were rechecked;
- what definitions changed, if any;
- what equations were preserved, added, or superseded;
- what tests or comparisons were run;
- what remains YELLOW / OPEN;
- whether any drift was detected.

An update without both the pre-update reference and the post-update check is incomplete.

## Core Rule 17 — Mathematics Is The Protected Backbone

The mathematics is not a summary layer. It is the scientific backbone.

Canonical equations, definitions, assumptions, dimensions, units, boundary conditions, initial conditions, derivation steps, transformation laws, tolerances, uncertainty bounds, failed branches, and pass/fail comparisons may not be replaced by prose summaries.

Explanations may be added around mathematics. They may not substitute for it.

When a derivation is corrected:
- preserve the earlier derivation;
- add a new explicitly versioned derivation;
- state exactly why the earlier version failed or was superseded;
- preserve the dependency trail.

No AI, editor, cleanup pass, or chapter rewrite may shorten a mathematical derivation in the canonical math backbone merely because it can be summarized.

## Core Rule 18 — Missing Math Blocks Promotion

If a scientific node makes a quantitative or mechanistic claim whose required mathematics is missing, compressed away, or only described verbally, mark it:

**MATH-REBUILD-REQUIRED**

Such a node may remain exploratory / YELLOW, but it may not be promoted as mathematically established until the required derivation is restored or newly derived and placed in the protected math backbone.

---

## Enforcement

This file is the canonical core-rules reference.

The protected math backbone lives under `MATH_BACKBONE/`.

Once a canonical math file is present on `main`, normal updates are append-only:
- existing backbone math files may not be deleted;
- existing backbone math files may not be shortened;
- existing backbone math files may not be rewritten in place;
- corrections are added as new versioned files with explicit supersession notes.

Every pull request must carry:
- `CORE-RULES-PRE:` — the pre-update core reference;
- `MATH-BACKBONE:` — what math was preserved / added / rebuilt / not applicable;
- `CORE-RULES-POST:` — the post-update compliance check.

Any automation, AI agent, editor, or repository checker should fail closed when a proposed change attempts to modify this file, diminish protected mathematics, or contradict these rules without explicitly marking the downstream work as unresolved.

The correct response to a conflict is:

**protect the core rule -> expose the conflict -> protect the math -> test the downstream claim.**

Not:

**change the core rule or erase the math to preserve the downstream claim.**
