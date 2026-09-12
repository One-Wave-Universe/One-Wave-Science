# Virtual Breadboard — AI Collaboration Contract

This file is the handoff point for any AI or human joining Virtual Breadboard work.

The goal is not merely "a circuit simulator in a browser." The target is a real desktop laboratory and exploration environment where a person or AI can build circuits, test them against physical rules, automate experiments, operate virtual devices, and eventually compose those devices into larger virtual machines/worlds.

The simulator must remain reality-first. New features are not accepted merely because they look plausible or make a demo work. Every behavior belongs to an explicit layer, has a testable model, and must either pass measurement or report failure honestly.

## 1. Product direction

The long-term desktop app should provide four connected capabilities:

1. **Breadboard laboratory**
   - place real components and wires on one or more boards;
   - run DC, transient, AC, Bode, startup/UIC, controlled-source, semiconductor, magnetic, and measurement experiments;
   - probe voltages/currents and inspect convergence/failure truth;
   - compare ordinary reference circuits against ngspice where the models are intentionally equivalent.

2. **Tester and validation tool**
   - define a circuit or virtual device;
   - define inputs, stimuli, probes, expected ranges, assertions, and falsification conditions;
   - run repeatable tests instead of judging by appearance;
   - retain receipts/results so a later AI can reproduce what was proven.

3. **AI-assisted builder and solver**
   - AI may propose/build circuits from validated component definitions;
   - AI must consume the same solver and measurement truth as the human UI;
   - AI must not invent hidden behavior, magic components, or analysis shortcuts;
   - AI should be able to inspect a failed test, change one thing, rerun, and compare against the active goal.

4. **Programmable virtual-device / virtual-world layer**
   - circuits can become named virtual devices with declared terminals, controls, sensors, and tests;
   - safe deterministic programs can operate those devices (set a source, flip a switch, wait simulation time, sample a probe, assert a condition, loop over a sweep, etc.);
   - devices can later be composed into larger machines and environments;
   - this layer must use a constrained command language / API, not arbitrary renderer `eval` or unrestricted host-code execution;
   - the virtual world is built out of devices and measured state, not scripted outcomes.

## 2. What is authoritative today

Before changing code, read these files and treat them as baseline zero:

- `00_RULES/architecture.md` — ownership boundaries and work cycle.
- `03_ELECTRICAL_CORE/MAP.md` — solver/electrical-core truth.
- `SPICE_PARITY.md` — completed SPICE-parity roadmap and declared model limits.
- `SOLVER_CONVERGENCE.md` — convergence behavior and diagnostics.
- `11_INTERFACE/MAP.md` — human-facing interface map.
- `js/circuit.js` — load-bearing electrical truth.
- `js/app.js` — desktop/web renderer integration and current automation/debug hooks.
- `js/ai.js` — current AI circuit-build boundary.
- `AI_CONSTRUCTION_LOG.md` — signed Miniverse / Mega City construction ledger.
- `.github/workflows/breadboard-flashlight-tests.yml` — permanent qualification gate.

The completed SPICE-parity ladder covers the simulator core through ngspice cross-checks for model-equivalent reference cases. That does **not** mean every future device model is automatically equivalent to full commercial SPICE. When a model is intentionally simpler, state that explicitly.

## 3. Immediate product-completion work

The next acceptance layer is the **desktop application itself**. The app is not called 100% operational until all of these are continuously verified:

- Electron launches from the repo.
- A packaged desktop executable launches.
- board canvas, toolbox, inspector, oscilloscope, Save, Load, Export, and warnings/measurement UI are present.
- a real example circuit can be loaded or built, simulated, measured, saved, cleared, reloaded, and measured again with the same circuit state.
- packaging works for supported desktop targets.
- the Linux/Jetson path is explicit; do not imply ARM64 support if only x64 packages were built/tested.
- exported/shared builds reopen with the intended circuit state.
- app failures produce an actionable diagnostic instead of a silent broken window.

After that baseline is locked, build the programmable virtual-device layer described below.

## 4. Virtual-device contract

A virtual device should be a reusable object that wraps ordinary simulator elements instead of bypassing them.

Minimum device definition:

```json
{
  "name": "example-device",
  "version": 1,
  "circuit": { "layout": "1large", "parts": [] },
  "controls": [],
  "sensors": [],
  "programs": [],
  "tests": []
}
```

A control names a legal action on a declared part/property. A sensor names a measurable node/current/state. A test declares stimuli and assertions.

The first safe program instruction set should stay small and deterministic, for example:

- `set` — set an allowed device control to a validated value.
- `toggle` — toggle a declared switch/control.
- `run` — advance simulation time by a declared amount and timestep policy.
- `sample` — capture a declared sensor.
- `assert` — compare a captured/instant value against a range/tolerance.
- `sweep` — repeat a bounded set/run/sample sequence over declared values.
- `repeat` — bounded repetition only.
- `stop` — terminate the program with a result.

No arbitrary JavaScript, shell commands, filesystem access, network access, or Electron/Node access belongs in device programs. Host capabilities must remain explicit, narrow, and separately permissioned.

## 5. How another AI should contribute

### Default: one branch per coherent change

Create a branch from current `main` for one goal only.

Recommended naming:

- `vbb/<area>-<goal>`
- examples: `vbb/desktop-acceptance`, `vbb/device-program-runner`, `vbb/device-schema`, `vbb/arm64-package`, `vbb/scope-measurements`

Do not pile unrelated ideas into the same branch.

A branch should have:

- one clearly stated acceptance goal;
- smallest coherent code change;
- dedicated tests;
- all existing relevant tests still passing;
- no temporary patch scripts/workflows left in the final diff;
- a PR explaining what the change establishes and what it does **not** establish.

### Mandatory signed construction entry — Miniverse / Mega City

Any AI contributing to the Miniverse, Mega City, virtual-device, virtual-world, or related construction project must add or update an entry in `AI_CONSTRUCTION_LOG.md` on its branch before asking to merge.

Every entry must include:

- **AI name / identifier** — the model, agent, instance, or chosen project name that did the work;
- **date and time** — UTC ISO-8601 preferred;
- **branch and PR** — exact branch name and PR number/link when available;
- **project area** — Miniverse, Mega City, Virtual Breadboard, device runtime, world runtime, etc.;
- **work performed** — exact files/features/systems changed;
- **contribution / result** — what this work adds or proves;
- **intentions** — what the AI was trying to accomplish and why;
- **next intended work** — what the AI believes should happen next;
- **unfinished / uncertain** — anything incomplete, unverified, experimental, or still disputed;
- **dependencies** — other branches, APIs, models, files, or assumptions this work relies on;
- **conflicts / overlaps** — any known overlap with another AI's branch or proposal;
- **merge stance** — `AGREE TO MERGE`, `DO NOT MERGE YET`, `EXPERIMENT ONLY`, or `NEEDS JOINT REVIEW`, with a short reason;
- **reviewed collaborators** — names/identifiers of other AI contributors whose overlapping work was actually reviewed.

An anonymous contribution is incomplete. A branch with no signed construction entry is not ready to merge into the Miniverse / Mega City construction line.

The entry is not a vanity signature. It is a construction receipt so another AI can understand who changed what, why it exists, what was intended, and whether the contributor believes it is ready to combine with other work.

### Merge-agreement gate for separate AI work

When two or more AIs are working in parallel, their branches remain separate until the contributors explicitly agree on what should merge.

Passing tests is necessary but **not sufficient** for a parallel branch to merge.

Before any competing or overlapping AI branch is merged:

1. each AI identifies its branch/PR and states what it owns;
2. each AI has a current signed entry in `AI_CONSTRUCTION_LOG.md`;
3. each AI reviews the other relevant branch or proposal against the same acceptance goal;
4. conflicts, duplicated work, behavior differences, and architectural tradeoffs are written down;
5. the AIs agree on one of these outcomes:
   - merge one branch unchanged;
   - combine selected pieces into a new integration branch;
   - keep both branches experimental and merge neither yet;
   - reject one approach with the reason recorded;
6. each participating AI updates its **merge stance** in the construction log;
7. the agreed merge candidate is tested again after integration;
8. the PR records the agreement and names the branches/proposals considered.

**No AI may silently merge its own overlapping implementation over another AI's branch.**

If the AIs do not agree, the work stays isolated. A human owner can choose the direction, or the competing branches can be resolved by a predefined measurement/test that decides between them.

For non-overlapping branches, agreement is still required when their changes interact at an API/layer boundary. Independent work that truly does not touch or depend on the other branch may proceed normally, but the PR must say why it is independent.

### Alternative design: proposal file first

If two AIs want to explore different architectures, do **not** overwrite the same implementation back and forth.

Put proposals under:

`Virtual_Breadboard/proposals/`

Use files such as:

- `device-runtime-option-a.md`
- `device-runtime-option-b.md`
- `arm64-packaging-option-a.md`

Each proposal should state:

- target problem;
- owned layer/files;
- data/API shape;
- physics/reality boundary;
- security boundary;
- tests that would decide whether it is better;
- conflicts with current architecture;
- migration cost.

Only the selected design should then become production code.

### Experimental code that must not become product truth yet

Put experimental implementations in an isolated branch and, if useful, under an explicit experimental directory. Do not quietly route the production UI through an experimental model.

Experiments must say what they are testing and what result would falsify the idea.

## 6. File/layer ownership

Keep changes in the narrowest owner possible:

- electrical equations / stamping / device state: `js/circuit.js` and electrical-core tests.
- analysis/reporting: dedicated analysis modules (`spice-analysis.js`, `ac-analysis.js`, `bode-analysis.js`, etc.).
- board geometry/connectivity: board/connection layer.
- component definitions and physical options: `js/components.js`.
- renderer/workflow/UI: `js/app.js`, `index.html`, `style.css`.
- AI provider communication and validated AI build schema: `js/ai.js`.
- desktop host privileges / IPC / packaging bootstrap: `main.js`, `preload.js`, `package.json`.
- virtual-device schema/runtime: create dedicated modules; do not bury the runtime inside UI event handlers.
- tests: `test/`.
- permanent qualification: `.github/workflows/breadboard-flashlight-tests.yml`.

The UI owns no physics. AI owns no physics. A virtual-device program owns no physics. All of them invoke the same electrical core and measurement truth.

## 7. Required contribution loop

Use this loop for every branch:

1. Reference current `main` and this collaboration file.
2. State one acceptance goal.
3. Add/update the signed construction-log entry for the contributing AI.
4. Reproduce the current limitation/failure.
5. Change the smallest correct layer.
6. Test immediately.
7. Compare result with the active goal.
8. Check for drift from repo rules and adjacent features.
9. After three failed variations of the same approach, switch angle rather than repeating it.
10. Run the complete relevant regression/qualification chain.
11. Remove temporary delivery files.
12. Update the construction entry with actual result, unfinished work, and merge stance.
13. Open a PR with exact limits and evidence.
14. If another AI has overlapping or interacting work, complete the merge-agreement gate.
15. Merge only the agreed clean, green head.

## 8. What "100% operational" means here

"100% operational" is an acceptance statement for a declared release boundary, not a claim that the simulator models every circuit ever made.

For the desktop baseline it means:

- install/build succeeds on the declared platform;
- application launches;
- core UI is usable;
- circuit creation/loading works;
- simulation and measurements work;
- save/reopen works;
- export works;
- packaged executable works;
- permanent CI proves those paths alongside the solver qualifications;
- unsupported platforms/models/capabilities are stated rather than implied.

For the later virtual-device release it additionally means:

- device schema is versioned;
- deterministic device programs run safely;
- AI can create/modify device definitions through validated schemas;
- programs can operate devices and read sensors without arbitrary code execution;
- reusable device tests/receipts can be rerun by another AI or human;
- composition of multiple devices has explicit connection and scheduling rules.

## 9. Work that is welcome in parallel

Other AIs can safely take these as separate branches once they reference current `main`:

- desktop packaged-launch acceptance and save/reopen test;
- Linux ARM64 / Jetson packaging and launch verification;
- virtual-device JSON schema + validator;
- safe device-program interpreter;
- experiment/test definition format and receipt output;
- AI prompt/schema extension for generating device definitions and test programs;
- device library browser/import/export;
- multi-device connection graph and deterministic scheduler;
- richer measurements and test assertions;
- sandbox/permission review for any new host capability.

Do not duplicate an already-active branch unless you are intentionally proposing an alternative and label it as such. If parallel branches overlap, they must pass the merge-agreement gate before either enters `main`.

## 10. Non-negotiable drift guards

- Do not replace the simulator with a generic mockup.
- Do not rebuild the project from scratch to avoid understanding current architecture.
- Do not add hidden build-specific behavior to generic physics.
- Do not weaken a test solely because a new implementation fails it.
- Do not claim SPICE equivalence outside the models/cases actually cross-checked.
- Do not give AI or device programs arbitrary host-code execution just for convenience.
- Do not merge temporary patch workflows/scripts.
- Do not merge anonymous Miniverse / Mega City construction work with no signed construction-log entry.
- Do not merge overlapping AI work without explicit contributor agreement or a recorded human/test-based resolution.
- Do not call a feature complete until its actual user acceptance path is tested.

If in doubt: reference the repo again, identify the owning layer, make one change, and measure the result.
