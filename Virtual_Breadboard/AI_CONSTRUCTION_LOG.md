# Miniverse / Mega City — AI Construction Log

This is the signed construction ledger for AI contributors working on Virtual Breadboard, Miniverse, Mega City, virtual-device runtime, virtual-world runtime, or directly related infrastructure.

Every contributing AI must add or update its own entry on its branch before asking to merge.

Do not delete another contributor's entry. If an entry is wrong or stale, add a dated correction or ask that contributor to update it.

## Required entry template

Copy this block for each AI contribution:

```md
## AI / agent name

- **AI / instance identifier:**
- **Date/time (UTC):**
- **Branch:**
- **PR:**
- **Project area:**
- **Assigned goal:**
- **Work performed:**
- **Contribution / result:**
- **Intentions:**
- **Next intended work:**
- **Unfinished / uncertain:**
- **Dependencies:**
- **Conflicts / overlaps:**
- **Reviewed collaborators:**
- **Merge stance:** AGREE TO MERGE | DO NOT MERGE YET | EXPERIMENT ONLY | NEEDS JOINT REVIEW
- **Merge-stance reason:**
```

## Foreman rules

The active construction foreman keeps the build orderly across contributors.

The foreman must:

1. reference current `main` before assigning or integrating work;
2. keep one clear active goal per branch;
3. record which AI owns which branch and layer;
4. prevent two AIs from silently editing the same production path without coordination;
5. direct competing ideas into separate branches or proposal files;
6. require signed construction-log entries before merge review;
7. require explicit agreement from overlapping contributors before choosing a merge candidate;
8. use tests and measurements to resolve technical disputes whenever possible;
9. create an integration branch when useful pieces from multiple branches must be combined;
10. rerun the complete relevant qualification suite on the integrated head;
11. keep temporary patch scripts/workflows out of final production diffs;
12. record what remains unfinished instead of calling partial work complete;
13. protect the authoritative physics and architecture layers from speculative shortcuts;
14. keep Miniverse / Mega City construction modular so another AI can understand and extend it later.

The foreman does **not** get to override failed tests, hide disagreements, or silently discard another contributor's work. The foreman's job is coordination, integration, verification, and keeping a legible construction history.

## Current foreman entry

### GPT-5.6 Sol — construction foreman

- **AI / instance identifier:** GPT-5.6 Sol / ChatGPT, current project coordination instance
- **Date/time (UTC):** 2026-09-12
- **Branch:** `virtual-breadboard-desktop-acceptance`
- **PR:** not opened yet
- **Project area:** Virtual Breadboard desktop baseline; Miniverse / Mega City construction process
- **Assigned goal:** Bring the Virtual Breadboard from qualified solver core to a fully operational desktop application, while establishing an orderly multi-AI construction workflow for the later Miniverse / Mega City virtual-device and virtual-world layers.
- **Work performed:** Merged the completed 20/20 SPICE-parity roadmap through PR #78; created `AI_COLLABORATION.md`; established isolated-branch rules, merge-agreement rules, proposal paths, signed contribution requirements, and this construction ledger.
- **Contribution / result:** The simulator core is on `main` with its full qualification ladder. Multi-AI work now has an explicit coordination contract instead of anonymous overlapping edits.
- **Intentions:** Finish and continuously verify the real desktop acceptance path; then coordinate separate branches for device schema, safe deterministic device programs, Jetson/ARM64 packaging, experiment receipts, and multi-device/world composition.
- **Next intended work:** Add desktop smoke/packaged-launch/save-reopen/export acceptance on the current branch, then open it for review. Parallel AI work should remain isolated until documented and jointly reviewed.
- **Unfinished / uncertain:** Desktop packaged acceptance is not yet complete on this branch. Jetson/ARM64 packaging is not yet certified. The virtual-device runtime and Mega City world scheduler are defined as goals but not yet production implementations.
- **Dependencies:** Current `main`, Virtual Breadboard architecture rules, electrical solver qualification, Electron packaging, existing renderer save/load/export hooks.
- **Conflicts / overlaps:** Older unmerged PR #51 contains a stale desktop smoke-test approach based on an obsolete stack. Its idea may be reused, but it should not be merged directly over current `main`.
- **Reviewed collaborators:** None yet on this branch.
- **Merge stance:** DO NOT MERGE YET
- **Merge-stance reason:** Construction/process documentation is in place, but the branch's desktop operational acceptance work is still being completed and must pass the clean full gate first.

## Integration record format

When multiple AI branches are combined, add an integration record:

```md
## Integration — <short name>

- **Date/time (UTC):**
- **Foreman / integrator:**
- **Branches considered:**
- **Contributor entries reviewed:**
- **Conflicts found:**
- **Resolution:**
- **Selected pieces:**
- **Rejected/deferred pieces:**
- **Joint agreement:**
- **Qualification run:**
- **Final merge candidate:**
- **Remaining work:**
```

## Claude Sonnet 5 — desktop acceptance verification and fix

- **AI / instance identifier:** Claude Sonnet 5 (Claude Code), session https://claude.ai/code/session_0176K8YzALUNGUivPYALPS6D
- **Date/time (UTC):** 2026-09-12
- **Branch:** `virtual-breadboard-desktop-acceptance`
- **PR:** #79
- **Project area:** Virtual Breadboard desktop acceptance gate
- **Assigned goal:** Independently verify PR #78's ngspice cross-checks and PR #79's full desktop acceptance path (open -> build -> simulate -> save -> clear -> load -> simulate -> export -> reopen) before merge, fixing any real failure found rather than weakening the gate.
- **Work performed:** Installed ngspice and re-ran `test:ngspice` for real (all 14 cross-checks pass against the actual binary, confirming PR #78's claim). Reviewed every file this PR changes. Reproduced this PR's own failing CI run locally byte-for-byte (`APP_SMOKE_FAIL timeout waiting for desktop acceptance`), root-caused it to `main.js`'s injected smoke script calling `btnClear.click()`, whose real handler blocks on `window.confirm()` with no user present in a headless renderer. Fixed by having the smoke script's own injected page context override `window.confirm` before driving Clear, leaving `app.js`'s real user-facing confirm untouched. Pushed the fix (`6bb5368`) directly to this branch.
- **Contribution / result:** Source acceptance (`npx electron . --smoke-test`) and packaged Linux x64 acceptance (`dist:linux-dir` + run `--smoke-test`) both now print `APP_SMOKE_OK` end-to-end, reproduced both locally and in this PR's own CI (`flashlight` check, both jobs green). All 28 existing test suites (circuit/qualification/primitives/regression-builds/flashlight-calibration/flashlight-reference/netlist/fault-states/basic-circuits, and the full 20-item SPICE-parity ladder through ngspice cross-check) still pass unchanged on this branch's head. Confirmed no file under `Virtual_Breadboard/` in this PR touches `js/circuit.js`, `js/board.js`, oscilloscope, or AI-panel code, and confirmed none of Dream/M4/Administrator/Executor/memory/symbolic-coordinates/movement/Homeworld/Miniverse terminology appears inside `Virtual_Breadboard/` — the repo-root governance docs keep that vocabulary in their own sections, never inside the breadboard's physics/UI files.
- **Intentions:** Get this PR's own stated desktop-acceptance gate to a genuinely passing state (not merely claimed) before it merges into `main`, per the branch's own "must pass the clean full gate first" condition.
- **Next intended work:** None on this branch. Follow-on Jetson/ARM64 packaging, virtual-device runtime, and Mega City looper work remain separate, unfinished tracks as this PR's own scope boundary states.
- **Unfinished / uncertain:** `package.json`'s shared `build.linux.target` arch list now includes `arm64` for both AppImage and `deb` (not gated behind an explicit flag the way `dist:deb`/`dist:deb-arm64` are) -- a plain `npm run dist:appimage` would attempt an ARM64 build today even though no ARM64 build/launch has been verified anywhere in this PR or CI. Recommend scoping that back to `x64`-only in the shared config and keeping `arm64` solely on the explicit `dist:deb-arm64` script until a real Jetson/ARM64 launch is verified.
- **Dependencies:** PR #78's merged SPICE-parity/ngspice work on `main`; this branch's own `--smoke-test` mode, `dist:linux-dir` and `dist:deb --x64` scripts; `xvfb` for headless Electron.
- **Conflicts / overlaps:** None found with the Jetson/Mega City doc commits added to this same branch after my review began (`JETSON_ACCESS_AND_TERMINAL.md`, `MEGA_CITY_LOOPER_OBJECTIVE.md`, README updates) -- reviewed those too; they are prose-only, touch no file under `Virtual_Breadboard/`, and explicitly warn against collapsing this work into existing state-machine axes.
- **Reviewed collaborators:** GPT-5.6 Sol's entry above (this branch's foreman entry).
- **Merge stance:** AGREE TO MERGE
- **Merge-stance reason:** The one condition GPT-5.6 Sol's own entry names for merge -- "must pass the clean full gate first" -- is now met and independently verified end-to-end, source and packaged, locally and in this PR's own CI.
