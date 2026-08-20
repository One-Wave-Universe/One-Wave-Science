# Field Coder — Branch Build Map

Every branch below inherits and must reread the complete Field Coder control set before work begins.

Each branch has a **hard start** and **hard stop**. No branch may leak work into the next step.

---

## `field-coder/00-control` — Project control layer

**Purpose:** establish scope, rules, build map, progress memory, and diary.

**Hard start:** repository is readable and `main` is known-good enough to branch from.

**Allowed work:** documentation/control files under `Field_Coder/` only.

**Success:** scope, permanent rules, step map, progress report, and diary exist and are internally consistent.

**Hard stop:** once all control documents exist and all future branches have been created from this branch, no implementation code is added here.

---

## `field-coder/01-shell` — Executable Field shell

**Purpose:** create the smallest Field coding-agent program that starts successfully.

**Hard start:** Step 00 complete; all control docs read; progress and diary updated.

**Allowed work:** initial Field source tree, minimal controller entry point, shell test only.

**Must not include:** repo reading, model calls, editing, diffing, testing other projects, retry logic, Void logic.

**Success test:** Field controller starts and reports a deterministic shell-ready status; missing required shell component is detected by a deliberate failure check.

**Hard stop:** shell pass + deliberate failure detection + restored pass are recorded in diary/progress.

---

## `field-coder/02-state-memory` — Persistent Field state

**Purpose:** persist and restore Field's exact working state across restarts.

**Hard start:** Step 01 known-good and recorded.

**Allowed work:** state schema, load/save validation, state tests.

**State must include:** goal, current task, attempt, max attempts, last action, last result, next action, active branch/step.

**Success test:** save -> process/reload -> exact restoration; invalid/missing required state is rejected.

**Hard stop:** persistence and invalid-state tests pass and are recorded.

---

## `field-coder/03-task-intake` — Goal to one narrow task

**Purpose:** convert a supplied coding goal into exactly one bounded current task.

**Hard start:** Step 02 known-good and restored from persistent state.

**Allowed work:** task intake/parser/validator and tests.

**Must not include:** repository editing or model-driven implementation.

**Success test:** broad sample goal produces one explicit task with success criteria and scope; ambiguous/unbounded output is rejected.

**Hard stop:** one-task contract is proven and recorded.

---

## `field-coder/04-repo-reader` — Read-only repository reconstruction

**Purpose:** let Field inspect repository evidence without changing it.

**Hard start:** Step 03 can provide one current task.

**Allowed work:** repo detection, branch/HEAD read, file discovery/read, relevant-context bundle.

**Must remain read-only.**

**Success test:** Field reads a fixture repo, records HEAD/branch/relevant files, and leaves repository byte-for-byte/working-tree unchanged.

**Hard stop:** read-only invariant is proven and recorded.

---

## `field-coder/05-proposal-builder` — One implementation proposal

**Purpose:** turn task + repo evidence into one structured implementation proposal.

**Hard start:** Step 04 produces a valid read-only context bundle.

**Proposal must state:** intended change, reason, exact files expected to change, invariants to preserve, expected result, exact success test.

**Must not edit files yet.**

**Success test:** valid proposal accepted; missing target files/invariants/test is rejected; multi-change proposal is rejected.

**Hard stop:** proposal contract is proven and recorded.

---

## `field-coder/06-controlled-editor` — Apply one declared change

**Purpose:** allow Field to perform only the approved/declaratively scoped edit.

**Hard start:** Step 05 has a valid single-change proposal.

**Allowed work:** controlled file edits limited to declared paths.

**Success test:** declared file change succeeds; undeclared file change is blocked/detected; unrelated files remain unchanged.

**Hard stop:** controlled-edit boundary is proven and recorded.

---

## `field-coder/07-diff-self-check` — Intended vs actual change

**Purpose:** make Field inspect what it actually changed before claiming success.

**Hard start:** Step 06 can produce a controlled edit.

**Allowed work:** changed-file inventory, unified diff capture, proposal-vs-diff comparison.

**Success test:** matching diff passes self-check; extra/unexpected change fails self-check.

**Hard stop:** actual-diff evidence is always produced and recorded.

---

## `field-coder/08-test-runner` — Evidence-producing execution

**Purpose:** execute the proposal's declared success test and capture evidence.

**Hard start:** Step 07 diff matches the declared proposal.

**Allowed work:** bounded command runner, stdout, stderr, exit status, timeout/result capture.

**Success test:** known passing command recorded as pass; known failing command recorded as failure without crashing the controller.

**Hard stop:** deterministic pass/fail evidence capture is proven and recorded.

---

## `field-coder/09-self-correction` — Three-attempt Field learning loop

**Purpose:** feed failure evidence back into Field without uncontrolled wandering.

**Hard start:** Step 08 reliably captures test evidence.

**Allowed work:** attempt tracking, retry/replan state transitions, evidence feedback.

**Rules:** attempt 1 planned approach; attempt 2 evidence-based correction; attempt 3 materially different correction/direction; then stop.

**Success test:** fixture failure follows correct attempt transitions and stops after third failed attempt.

**Hard stop:** no fourth hidden retry is possible; blocked state is recorded.

---

## `field-coder/10-git-safety` — Known-good workspace protection

**Purpose:** protect source repositories from failed Field changes.

**Hard start:** Step 09 retry logic is bounded and persistent.

**Allowed work:** known-good HEAD capture, safe work branch/worktree strategy, change inventory, rollback of failed attempt.

**Success test:** deliberate bad edit is completely restored; known-good commit is unchanged; successful candidate remains inspectable.

**Hard stop:** rollback safety is proven and recorded.

---

## `field-coder/11-review-packet` — Review-ready Field output

**Purpose:** package Field's work for an external Void/Admin reviewer without self-approval.

**Hard start:** Step 10 protects known-good state.

**Packet must include:** goal, task, proposal, files changed, diff, tests/results, attempts, remaining uncertainty, candidate status.

**Success test:** deterministic packet generated from a fixture run; Field cannot mark its own architecture verdict as approved.

**Hard stop:** review packet is complete and self-approval is impossible.

---

## `field-coder/12-model-adapter` — Replaceable coding model seat

**Purpose:** connect a real/local coding model without binding the engine to one provider.

**Hard start:** Steps 01-11 work with deterministic/fake agent outputs.

**Allowed work:** provider-neutral adapter interface plus one actual local/model implementation.

**Success test:** fake adapter and real adapter satisfy the same structured contract; adapter can be swapped without controller changes.

**Hard stop:** provider replacement requires adapter change only, not engine rewrite.

---

## `field-coder/13-sacrificial-repo` — End-to-end controlled proof

**Purpose:** prove Field can complete a tiny software task safely from goal to review-ready result.

**Hard start:** Step 12 adapter contract passes.

**Fixture:** disposable tiny repo with passing baseline tests.

**Success:** Field receives goal, narrows task, reads repo, proposes, edits, self-checks diff, tests, repairs if necessary, preserves known-good baseline, and emits review packet.

**Hard stop:** both a successful task and at least one deliberately bad candidate path have been demonstrated and recorded.

---

## `field-coder/14-real-repo-trial` — First real controlled task

**Purpose:** apply Field to one tiny real repository issue without broad feature work.

**Hard start:** Step 13 passes end-to-end and review packet is accepted for trial readiness.

**Allowed work:** one small real task, one bounded scope, existing tests/verification only plus narrowly required additions.

**Success:** review-ready candidate produced without unrelated changes or lost project state.

**Hard stop:** stop after the first real task review packet. Do not expand into autonomous production or start Void implementation on this branch.

---

# Global branch transition rule

At every branch boundary:

1. reread all Field Coder control files;
2. confirm previous hard-stop evidence exists;
3. update `PROGRESS.md`;
4. write a branch-close diary entry;
5. state the next branch hard-start conditions;
6. only then begin the next branch.

No later branch may retroactively redefine an earlier success condition without recording an architecture decision/blocker.