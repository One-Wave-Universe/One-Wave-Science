# FIELD BRANCH 15 MEMORANDUM — FIELD STATE KERNEL

## FULL MASTER PROJECT GOAL — CARRIED FORWARD VERBATIM

Build the Field half of the complete **Field/Void CPU-GPU state-machine coding engine** for autonomously building, modifying, testing, debugging, and improving real software, applications, and programs.

The complete system has four distinct roles:

- **Field**: expressive/generative software movement. Field creates candidate state transitions and bounded coding actions.
- **Void**: separate mirrored oversight/override. Void evaluates Field movement and may ALLOW, CORRECT, OVERRIDE, HOLD, or ESCALATE. Void logic is not implemented inside Field branches.
- **M4 / OpenClaw controller**: fast routing, timing, state selection, branch-loop control, and handoff between Field and Void.
- **Administrator / ChatGPT escalation**: higher-level architecture decision and help when Field/Void cannot safely resolve a blocked state.

These Field branches build the actual Field state-machine computation, not a generic chatbot wrapper and not a provider-specific model orchestration system.

## CANONICAL FIELD/VOID MACHINE

The engine must preserve these primitives as executable state, not metaphor:

- **6 Steps**: Begin -> Build -> Hold -> Build -> Break -> Loop.
- **5 Field states / scale bands**: Micro/Floor, Small/Low, Medium/Mid, Large/High, Macro/Extreme.
- **4 Views**: Inward, Outward, Across, Over.
- **4 Operators**: -, +, /, x.
- **3 Moves**: Compress (-1), Hold (0), Expand (+1).
- **2 Choices**: mirrored polarity choice; Field choice selects/creates the active field.
- **1 Field / Mirror / Void reference**: shared reference boundary/zero.

Gate order:

`1 -> 2 -> 3 -> 4(0) -> 5 -> 6`

and mirrored return:

`6 -> 5 -> 4(0) -> 3 -> 2 -> 1`

Gate 4 is also Gate 0: mirror/null/flip/boundary.

Canonical mirrored relations:

- F2 Choice <-> V5 Scale
- F3 Motion <-> V4 Action
- F4 View <-> V3 Interpretation
- V2 Choice <-> F5 State
- outer F1/V6 and V1/F6

Motion contains Point, Path, and Field Rotation. Each motion mode can carry Carrier, Breathing, and Phase behavior.

Field-context law: no state is interpreted outside the currently selected active field.

Recursion law: each 1-6 step may contain the full nested chain.

## FIELD BRANCH OUTPUT

The Field build must eventually provide a provider-neutral, AI-callable software interface that can:

1. receive an explicit coding goal and current program/repository state;
2. encode that state into the canonical Field machine;
3. compute deterministic Field transitions on CPU;
4. compute equivalent batched transitions on GPU where appropriate;
5. preserve reference, differential, state, scale, motion, view, gate, and history;
6. emit one bounded candidate software movement/action at a time;
7. preserve evidence and state across iterations;
8. hand the candidate and evidence to the separate Void oversight/override side;
9. accept M4 routing/control without binding the engine to one AI provider;
10. serve real coding, app-building, and program-building workloads.

## SCOPE LAW

Every Field branch is one preplanned implementation stage of this exact project.

The complete coding plan is defined before implementation. Branches are fixed work slots. A branch may implement only its assigned stage, must preserve prior verified behavior, must test every change, must record what worked and failed, and must stop at its explicit hard stop.

No branch may redefine the master project goal, replace the state-machine engine with generic agent orchestration, merge Void implementation into Field, or implement future branch work early.

---

## BRANCH 15 PURPOSE

Create the first executable canonical Field state kernel. This branch turns the locked 6/5/4/3/2/1 primitives into typed program state and deterministic primitive mechanics that later CPU/GPU transition code can consume.

## HARD START

Branch 15 may begin only after:

- Steps 00-14 remain preserved as historical verified work;
- the corrected master project goal above is loaded in full;
- `LOOP_DYNAMICS.md` is loaded;
- inherited journal history is present below;
- stale generic-agent descriptions are treated as historical implementation evidence, not authority over the corrected master goal;
- workspace cleanup is checked before coding;
- the exact Branch 15 implementation and test are declared.

Hard-start status: PASS.

## EXACT BRANCH 15 IMPLEMENTATION

Allowed implementation:

- `Field_Coder/field/state_kernel.py`
- `Field_Coder/tests/test_state_kernel.py`
- Branch 15 memorandum, diary, and progress records.

The kernel must define executable representations for:

- six cycle steps;
- five scale/state bands;
- four views;
- four operators;
- three moves;
- two Field choices;
- six gates with Gate 4 carrying mirror-boundary alias 0;
- Point / Path / Field Rotation motion mode;
- Carrier / Breathing / Phase modulation;
- active field identity;
- shared reference value;
- differential value;
- history;
- deterministic forward and reverse gate advance;
- deterministic differential-to-move selection.

## FORBIDDEN ON THIS BRANCH

Do not add:

- GPU kernels or batching;
- Void evaluation/override logic;
- M4 scheduling;
- model/provider logic;
- generic agent orchestration;
- code-edit planning logic;
- future autonomous application behavior.

## EXACT SUCCESS TEST

The test must prove:

- every canonical primitive has exactly the required number of states;
- Gate 4 reports mirror-boundary alias 0;
- forward traversal is exactly 1,2,3,4,5,6;
- reverse traversal is exactly 6,5,4,3,2,1;
- positive differential selects Expand (+1);
- zero differential selects Hold (0);
- negative differential selects Compress (-1);
- Field state validation rejects invalid/empty active-field identity;
- valid state preserves reference, differential, gate, motion, modulation, and history.

## HARD STOP

Stop Branch 15 immediately when:

- the state kernel exists;
- its exact test passes;
- prior files are not modified except required branch records;
- no forbidden future subsystem appears;
- post-branch project analysis is written;
- what worked, what failed, and architecture effects are recorded;
- workspace/stale-information cleanup is checked;
- progress and diary are updated.

---

## PRE-BRANCH PROJECT ANALYSIS / NOTES TO SELF

The most important risk is semantic drift. Previous Field work proved useful software-building plumbing, but several control files described that plumbing as if it were the whole project. Branch 15 must not repeat that mistake. The state machine is now treated as executable architecture, and future code must consume these primitives rather than merely mention them in documentation.

The state kernel should be intentionally boring and deterministic. Fancy behavior here would make later CPU/GPU parity harder to prove. The useful architectural effect of this branch is to establish one canonical representation that later layers can batch, serialize, compare, and mirror without redefining meanings.

Do not allow names from old generic-agent stages to redefine the machine. Preserve those files only as historical working components until a later explicit cleanup/migration step says otherwise.

Workspace cleanup rule for this branch: inspect touched paths before and after work; remove or correct false current-authority text encountered in the active Branch 15 memorandum/progress/diary; do not delete historical test evidence merely because the architecture evolved.

Action-effect check: every new enum or field added here becomes a compatibility surface for CPU, GPU, M4, and Void. Keep the representation minimal, typed, deterministic, and directly tied to the locked project primitives.

---

## INHERITED JOURNAL HISTORY — COPIED INTO THIS MEMORANDUM

# Field Coder — Build Diary

This diary is mandatory project memory.

## Prior verified history
- Steps 00-12: PASS
- All prior hard stops: SATISFIED

## Entry 0028 — Step 13 sacrificial-repo pre-pass
- Branch: `field-coder/13-sacrificial-repo`
- Hard-start check: PASS
- Attempt: 1/3
- Intended change: compose existing components plus one disposable end-to-end proof

## Entry 0029 — Step 13 first integration execution
- Attempt: 1/3
- Result: fixture rejected before candidate creation
- Evidence: baseline Python test created untracked `__pycache__`; known-good gate correctly refused dirty source
- Decision: RETRY fixture only; workflow unchanged

## Entry 0030 — Step 13 sacrificial workflow completed
- Date/time: 2026-08-19 America/Los_Angeles
- Branch: `field-coder/13-sacrificial-repo`
- Step: 13 — End-to-end controlled proof
- Goal: prove composed Field behavior from bounded goal through repair and review-ready packet
- Hard-start check: PASS
- Known-good state: Steps 01-12 verified
- Attempt: 1/3 implementation; one evidence-based fixture correction
- Intended change: `workflow.py`, `test_sacrificial_workflow.py`
- Files actually changed: the two declared Step 13 files plus mandatory progress/diary records; second pass changed fixture setup only to commit `.gitignore`
- Command/check executed: sacrificial end-to-end test against local mirror of checked-in Step 13 contracts
- Exit status/result: PASS — exit 0 after fixture correction
- Observed behavior: clean baseline; attempt-1 bad edit and matching diff; failing declared test; evidence propagated to attempt 2; rollback; corrected edit; passing test; source unchanged; candidate inspectable; review packet pending external review
- What worked: all previously built component contracts composed successfully; three-attempt state used correctly; Git safety protected source; review packet withheld self-approval
- What failed: initial fixture ignored no Python cache files; known-good gate correctly caught it
- What was learned: repository hygiene is part of the known-good contract and must be explicit
- Decision: KEEP
- Next permitted action: transition `field-coder/14-real-repo-trial` to this completed Step 13 lineage, reread controls, select one tiny real repo task, and stop after its review-ready packet
- Hard-stop status: SATISFIED
- Blockers: none

## Entry 0031 — Step 14 real-repo trial pre-pass
- Date/time: 2026-08-19 America/Los_Angeles
- Branch: `field-coder/14-real-repo-trial`
- Step: 14 — First real controlled task
- Goal: run one tiny real animator defect through Field controls and stop at review-ready evidence
- Hard-start check: PASS — Step 13 completed; full controls and latest diary reread; real animator source/tests inspected
- Known-good state: Steps 01-13 verified
- Attempt: 1/3
- Selected task: fix `One_Wave_Animator/app/scene_model.py::_to_portable_path()` so an in-folder filename beginning with `..` is not mistaken for a parent-directory path
- Evidence: current condition was `rel_path.startswith("..")`; this also matched valid basenames such as `..hero.png`
- Files expected to change: `One_Wave_Animator/app/scene_model.py` and one narrow scene-model regression test
- Must remain unchanged: all other animator behavior/files; Field engine; no Void; no self-approval; no merge/push to main
- Exact success test: existing scene-model tests pass; in-folder `..hero.png` remains relative; true outside path remains absolute; bounded diff only; review packet pending external review
- Decision: KEEP

## Entry 0032 — Step 14 first real animator trial completed
- Date/time: 2026-08-19 America/Los_Angeles
- Branch: `field-coder/14-real-repo-trial`
- Step: 14 — First real controlled task
- Goal: correct one real animator portability defect without unrelated changes
- Hard-start check: PASS
- Known-good state: Step 13 completed and real target read from repository
- Attempt: 1/3
- Intended change: distinguish the actual parent path component `..` from legal filenames merely beginning with two dots
- Files actually changed: `One_Wave_Animator/app/scene_model.py`, `One_Wave_Animator/tests/test_scene_model.py`, plus mandatory Field progress/diary records
- Command/check executed: exact local Git slice of the checked-in real animator source; `python3 -m pytest -q tests/test_scene_model.py` before and after candidate
- Baseline result with new regression: FAIL as expected — 4 existing tests passed and `test_double_dot_prefixed_filename_inside_scene_stays_portable` failed because current code serialized an absolute path
- Candidate result: PASS — 5/5 scene-model tests passed
- Candidate source change: `rel_path.startswith("..")` -> `rel_path == os.pardir or rel_path.startswith(os.pardir + os.sep)`
- Regression coverage: legal in-folder `..hero.png` remains relative; true parent/outside asset remains absolute
- Branch diff audit from Step 13 baseline: only Field control records plus the two declared animator files; animator source change is 1 addition/1 deletion and test coverage is 27 additions
- What worked: the defect was reproduced before editing; one bounded condition corrected it; existing scene-model behavior remained passing; outside-path protection remained intact
- What failed: nothing in candidate implementation
- What was learned: prefix-string testing was too broad for filesystem component semantics; the parent marker must be matched as a complete path component
- Decision: KEEP — REVIEW_READY_CANDIDATE
- Architecture verdict: PENDING_EXTERNAL_REVIEW
- Next permitted action: none inside the Field Coder build list; Step 14 hard stop reached
- Hard-stop status: SATISFIED — stop after first real review packet; do not start another animator task or Void implementation
- Blockers: none
