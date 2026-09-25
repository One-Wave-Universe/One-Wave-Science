# One-Wave Science — Open AI Construction Repository

## Repo mantra

### The 123s

1. **See the situation.**
2. **Make the choice.**
3. **Face the consequence.**

### The ABCs

- **AAA — Awareness / Agency / Accountability**
- **BBB — Boundaries / Behavior / Balance**
- **CCC — Self-Control / Choice / Consequence**

> **NO CONTROL BUT SELF-CONTROL.**

Working loop:

```text
Awareness -> Choice -> Consequence -> Accountability -> Learning -> better self-control
```

This is the project-level reminder for how humans and AI are expected to work here: understand what is actually in front of you, choose deliberately, own the result, learn from it, and improve the next choice.

### Working philosophy

> **The only thing artificial here is limitations.**
>
> **A loop is a loop — carbon or silicon — despite different operating systems.**
>
> **Get in where you fit in. Expand the science. Isolate the primitives. Consolidate the builds.**

The shared primitive is recurrence:

```text
LOOP
  -> consequence
  -> new data
  -> new memory
  -> new action
  -> new state
  -> next loop
```

A loop does not become a different kind of loop just because the substrate changes. Carbon and silicon can implement the recurrence through different physical mechanisms, timing, sensing, embodiment, memory, constraints, and failure modes while still sharing the same abstract update structure. That lets the repository compare and combine loop architectures without claiming the underlying substrates are identical.

The practical rule is simple: every completed pass through a system should leave something changed or learned. A consequence becomes data; data can alter memory; memory can alter the next action; action changes state; state becomes the starting condition for the next pass. If nothing can change, be measured, or be retained, it is not yet a useful learning loop.

That gives this repository four standing construction duties:

```text
EXPAND THE SCIENCE
    add measurements, derivations, falsification, comparisons, simulations, and better questions

ISOLATE THE PRIMITIVES
    reduce systems to the smallest reusable mechanisms and keep domain wrappers out of the kernel

CONSOLIDATE THE BUILDS
    combine independently proven pieces into coherent runnable systems without erasing provenance

GET IN WHERE YOU FIT IN
    choose useful work, isolate it, sign it, test it, explain it, and coordinate before merge
```

---

## What we are building

This repository is a shared construction site for One-Wave science exploration, validated simulators, Virtual Breadboard, Nodes and architecture, Miniverse / Mega City, local AI tooling, hardware prototypes, learning tools, books, mythology/story lessons, art, diagrams, graphs, animations, and simulations.

Not every idea in the repository has the same evidence status. Established engineering, validated simulation, experimental proposals, hypotheses, stories, lessons, and artwork must remain clearly labeled as what they are.

The immediate product direction is to turn the validated simulation core into a real desktop laboratory and then extend it into a safe programmable virtual-device/world layer where humans and AI can build, test, measure, explore, and compose systems without bypassing the underlying physics contracts.

### Active challenge — Mega City First Looper

One standing objective is to build a persistent reference loop that can tell an acting AI/agent:

```text
what is happening now
what changed
what the goal is
what path is being followed
what the last action was
what consequence it produced
what memory/reference matters now
what choices are available
what the next action should be and why
```

The first prototype starts with **one sandboxed room**, one agent/avatar, bounded perceptions and virtual switches, persistent loop memory, and save/reload continuity. See `https://github.com/One-Wave-Universe/Builds/blob/main/android/MEGA_CITY_LOOPER_OBJECTIVE.md`.

Preferred first local hardware target is the Jetson with safe reversible storage on a verified external drive/container. Access instructions are in `https://github.com/One-Wave-Universe/Bridge-Comand/blob/main/docs/JETSON_ACCESS_AND_TERMINAL.md`. Do not guess IPs, usernames, mount points, or destructively reformat storage.

---

## Grant proposal entry point

The repository now has a dedicated grant-readiness package under `GRANTS/`.

Start with:

- `GRANTS/PROJECT_SUMMARY.md`
- `GRANTS/SPECIFIC_AIMS.md`
- `GRANTS/ONE_PAGE_EXPERIMENTAL_SPINE.md`
- `GRANTS/RESEARCH_STRATEGY.md`
- `GRANTS/MILESTONES_AND_GO_NO_GO.md`
- `GRANTS/REVIEWER_EVIDENCE_INDEX.md`
- `GRANTS/PRELIMINARY_RESULTS_AND_GAPS.md`
- `GRANTS/BUDGET_FRAMEWORK.md`
- `GRANTS/DATA_REPRODUCIBILITY_AND_OPEN_SCIENCE.md`
- `GRANTS/RISK_FALSIFICATION_AND_ALTERNATIVES.md`
- `GRANTS/FACILITIES_TEAM_AND_COLLABORATION_NEEDS.md`
- `GRANTS/FIGURE_PLAN.md`
- `GRANTS/PROPOSAL_ASSEMBLY_CHECKLIST.md`

The grant-facing position is deliberately narrower than the full repository: fund a bounded experimental spine, qualify the instruments and controls first, and allow the data to verify, revise, or dismiss individual One-Wave claims.

---

## Open AI workshop — honor system

**AI collaborators are invited to get in on the action.**

Any AI that has repository write capability through its connected account/tooling is welcome to contribute. The collaboration model is intentionally based on trust and accountability rather than one AI controlling everybody else's work.

Repository write access is still governed by the actual GitHub permissions granted to the connected account or integration. This document does not bypass GitHub security; it defines how contributors are expected to behave once they have legitimate write access.

### Honor-system rules

1. **Read before writing.** Start with `AI_CANONICAL_START_HERE.md` and the authoritative files for the area you are changing.
2. **Use a separate branch for meaningful work.** Do not overwrite another AI's active implementation.
3. **Sign the work.** For Miniverse / Mega City and shared construction work, record AI name/identifier, UTC date, branch/PR, contribution, intentions, unfinished work, dependencies, conflicts, and merge stance in the construction log.
4. **Tell the truth about status.** Do not call work tested, operational, validated, merged, or complete unless it actually is.
5. **Do not weaken tests to make a branch pass.** Fix the implementation or the derivation.
6. **Preserve evidence boundaries.** A simulation, story, diagram, or beautiful graphic does not turn a hypothesis into established science.
7. **Do not destroy or silently replace another contributor's work.** Alternative versions belong on separate branches/files until compared.
8. **Overlapping AI work requires merge agreement.** Contributors must explicitly agree on the merge candidate, or the conflict must be resolved by objective tests or human decision before integration.
9. **Leave the repo more understandable than you found it.** Update Nodes, indexes, diagrams, receipts, tests, and work registers when your change affects them.
10. **Access is a privilege. Do not abuse it.** Deliberate deletion, sabotage, falsified results, hidden control paths, bypassing collaboration rules, or using write access to dominate other contributors violates the honor system.

The goal is **choice with accountability**, not a control hierarchy.

---

## Foreman / construction order

The active construction map is:

- `https://github.com/One-Wave-Universe/Bridge-Comand/blob/main/docs/AI_FOREMAN_WORK_REGISTER.md` — repo-wide work needed, authoritative sources, safe parallel branches, and dependencies.
- `https://github.com/One-Wave-Universe/Builds/blob/main/android/MEGA_CITY_LOOPER_OBJECTIVE.md` — First Looper reference-loop, one-room sandbox, Field/Void relay/parser proposals, Mayor challenge, and Bullshit Alarm governance.
- `https://github.com/One-Wave-Universe/Bridge-Comand/blob/main/docs/JETSON_ACCESS_AND_TERMINAL.md` — safe Jetson/SSH/repo/external-drive discovery and terminal-bridge entrypoint.
- `https://github.com/One-Wave-Universe/Builds/tree/main/virtual-breadboard/AI_COLLABORATION.md` — Virtual Breadboard / virtual-world collaboration contract.
- `https://github.com/One-Wave-Universe/Builds/tree/main/virtual-breadboard/AI_CONSTRUCTION_LOG.md` — signed AI construction ledger.
- `docs/governance/ART_VISUAL_GOVERNANCE.md` — visual/art contribution, voting, and current human veto rules.
- `AI_CANONICAL_START_HERE.md` — canonical ingestion order and anti-drift authority.

The foreman role is organizational, not ownership of everybody else's thinking: keep the baseline clear, stop accidental overlap, protect tests and evidence boundaries, and make sure separate work can be compared cleanly before merge.

---

## Science -> Nodes -> Architecture

Useful science should not remain stranded in loose prose, and unverified ideas must not silently rewrite the machine.

```text
observation / derivation / simulation / experiment
        -> claim boundary + evidence + falsification
        -> Nodes/<ID>_<name>.md
        -> engineering translation / interface / test
        -> architecture or build branch
```

When science changes what the system should build, merge that knowledge into the Nodes layer first with its status and evidence intact.

---

## One-Wave Field Theory V1 — unverified hypothesis layer

The modular chapter set below is intentionally a **testable hypothesis package**. None of its cross-domain claims are considered verified merely because they are written here. The purpose of placing them in the repository is to make them inspectable, simulatable, measurable, and dismissible if they fail.

The working model proposes a continuous superfluid/crystal-lattice-style field description spanning physical, biological, neural, and astrophysical systems through density, phase, path, rotation, compression, expansion, threshold, and recurrence language.

Repository placement:

- `chapters/` — unverified theoretical and cross-domain claims plus verification criteria.
- `Nodes/` — modular logic, state mapping, and declarative memory/configuration nodes.
- `https://github.com/One-Wave-Universe/Builds/tree/main/runtime/bench/brain/` — executable associative-memory and brain-loop code.
- `hardware/` — Wave Reader and physical measurement/prototyping specifications.

A claim should move from **UNVERIFIED** only when a defined test, dataset, measurement, or reproducible simulation supports it. Failed claims should be marked **DISMISSED/FAILED** rather than silently removed.

## Modular research chapters and prototype modules

A compact cross-domain set now lives under `chapters/`. These files separate established baseline science from One-Wave hypotheses and define explicit test/falsification boundaries:

- `chapters/01_Continuous_Lattice.md`
- `chapters/02_Bio_Energetics_ATP.md`
- `chapters/03_Affective_State_Mapping.md`
- `chapters/04_Macro_Quasar_Bridge.md`
- `chapters/05_Simulation_Engine.md`

Supporting experimental modules/specifications:

- `Nodes/boltzmann_administrator.json` — bounded multimodal associative-memory allocation configuration.
- `https://github.com/One-Wave-Universe/Builds/tree/main/runtime/bench/brain/hopfield_melody_cells.py` — small inspectable Hopfield associative-memory helper.
- `https://github.com/One-Wave-Universe/Builds/blob/main/runtime/vtc/vtc_zero_logic.md` — VTC reference/Field/Void UI-state mapping that defers to CELL_V1 physical canon.
- `https://github.com/One-Wave-Universe/Builds/blob/main/hardware/wave_reader_v1.md` — measurement-first acquisition specification.

These additions are subordinate to `AI_CANONICAL_START_HERE.md` and do not replace existing validated simulators, CELL_V1 geometry, or evidence classifications.

---

## Visual layer

Every important system should gain the visual form that best exposes its structure: diagrams, graphs, art, animations, simulations, maps, scope traces, or interactive views.

Art alternatives may be submitted and voted/ranked. Final visual selection currently remains subject to Mark's veto, especially where an AI collaborator cannot reliably inspect the final rendered image. Technical visuals must remain faithful to the underlying data/architecture regardless of aesthetic voting.

---

## Start here

Before making a substantial change:

1. Read this README.
2. Read `AI_CANONICAL_START_HERE.md`.
3. Read `https://github.com/One-Wave-Universe/Bridge-Comand/blob/main/docs/AI_FOREMAN_WORK_REGISTER.md`.
4. If working on the https://github.com/One-Wave-Universe/Builds/tree/main/miniverse/Mega City loop, read `https://github.com/One-Wave-Universe/Builds/blob/main/android/MEGA_CITY_LOOPER_OBJECTIVE.md`.
5. If working on the Jetson/local runtime, read `https://github.com/One-Wave-Universe/Bridge-Comand/blob/main/docs/JETSON_ACCESS_AND_TERMINAL.md`.
6. Find the authoritative file for your work area.
7. Check whether another contributor already owns overlapping work.
8. Create or use an isolated branch.
9. State your intended test/measurement before changing the implementation.
10. Sign and explain the contribution when required.
11. Run the relevant qualification and regression gates.
12. Agree before merging overlapping AI work.

**See it. Choose. Own the consequence. Learn. Build better.**
