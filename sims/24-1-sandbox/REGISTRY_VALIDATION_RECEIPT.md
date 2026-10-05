# Registry validation branch-step

## Reference and hard start

MAIN GOAL: improve the Field/Void construction engine through bounded,
reviewed, testable software changes. This step prevents the common scientific
module registry from presenting malformed metadata as a successful check.

Repository: https://github.com/One-Wave-Universe/One-Wave-Science

Starting HEAD: `d43414d07c19c873e74962c8676d59e27ed2814d` (main).
Execution route: isolated cloud runner, ephemeral worktree
`/workspace/shared/science-sandbox-registry`, branch
`fix/sandbox-registry-validation-20261005`. This is not a laptop or Jetson receipt.
Prior dirty worktrees were preserved. Remote main matched the starting reference.

Authorities: root `AGENTS.md`, `GENERAL_REFERENCE_RULES.md`,
`AI_CANONICAL_START_HERE.md`, `JETSON_OPENCLAW_RUNTIME.md`,
`BRANCH_STEP_PROJECT_TEMPLATE.md`, I-06 metadata authority, sandbox
`GOLD_STANDARD.md`, current manifests, README and lattice CI workflow.

## Choice / allowed scope

One change: fail-closed registry structure and reference-path validation.
Allowed: sandbox.py, test_sandbox.py, README.md, this receipt, slot-6 manifest's
existing-engine path, and lattice-kernel-tests.yml test/trigger integration.
Protected: all physical update laws, kernel/adapter bytes, scientific node
metadata/gates, external datasets, solver research and unrelated worktrees.

Expected result: malformed input, duplicate identities/slots, empty discovery
and broken/escaping paths fail with diagnostics; valid entries report only
manifest/path validity. Entry-point presence remains separate from execution.
No promotion to GOLD or numerical/browser/physical validation is implied.

## Field / Void / progress

Approach A, attempt 1. Independent pre-oversight: ALLOW for the exact contract.
Field: applied structure checks, bounded local path checks, non-execution labels,
negative tests and corrected the broken slot-6 engine path. Added CI coverage.
Attempt 1 proof: 16 registry, 27 Node kernel/adapter and 10 Python dispersion
controls passed. Independent post-oversight: CORRECT. A malformed slot skipped
path inspection but incorrectly reported entry-point absence as false.
State/Scale: PARTIAL, do not scale. Reentry preserved that finding.

Attempt 2 began from unchanged HEAD and the same six scoped working files.
Independent pre-oversight: ALLOW. Corrected uninspected presence to null,
added a negative assertion for an existing file with invalid slot, and documented
the distinction. Final proof and independent post-oversight follow below.

## Tests / success criteria

- Python unittest discovery in `sims/24-1-sandbox` with `test*.py`.
- `python sims/24-1-sandbox/sandbox.py --json`.
- Node tests for `sims/00-lattice-primitive/test_lattice_kernel.js` and slot-1
  `test_adapter.js`.
- Python unittest discovery in `sims/00-lattice-primitive` with `test*.py`.
- Diff scope and independent post-oversight; exact-head CI before merge.

## Hard stop / handoff

Stop on conflicting target changes, failed proof or missing authority. No new
physics, adapter, browser or runtime deployment belongs to this change.
The next module must start with a fresh repository reference. Slot 6 remains
manifest-only; this registry never claims to execute it.

## Final local evidence / State / Scale / Reentry

2026-10-05, isolated Linux cloud runner, Python 3.12.14 and Node v24.19.0:
all commands above exited 0. Results: 16 registry tests, 27 Node kernel/adapter
tests (14 kernel and 13 adapter), 10 Python dispersion tests passed. Actual
registry CLI: slots 1 and 6 valid, entry-point presence true/false respectively,
module execution not-run for both. `git diff --check` passed.
Independent final post-oversight: ALLOW. Reviewer reran registry tests/CLI and
verified the correction; previously reran protected numerical suites.

State: RESOLVED for this bounded validator contract. DO NOT SCALE to scientific
or visual verification. No equations, kernel/adapter sources, source datasets or
node gates changed. Known remaining gap: slot 6 has no sandbox adapter; scientific
fixtures and visual quality must be tested separately for each implementation.

Reflection: the original validator treated shallow key presence as sufficient.
Nested malformed objects, bool slots, empty discovery and broken references now
fail closed. Review also caught the distinction between absent and uninspected
entry points. Metadata success is explicitly separated from execution evidence.
This improves reliable software construction without fabricating physical proof.

Reentry at local completion: original HEAD retained, only the six allowed files
changed. Parent-authorized publication is a separate exact-head PR/CI/merge
operation; this local receipt does not claim remote CI, merge or deployment.
