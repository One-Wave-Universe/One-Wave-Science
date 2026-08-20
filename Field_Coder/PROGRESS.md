# Field Coder — Progress Report

## Project

- Project: Field Coder
- Scope: Field-side coding agent only
- Current branch: `field-coder/04-repo-reader`
- Current step: 04 — Read-only repository reconstruction
- Status: IN PROGRESS
- Attempt: 1/3

## Completed steps

- Step 00 — Project control layer: COMPLETE
- Step 01 — Executable Field shell: COMPLETE
- Step 02 — Persistent Field state: COMPLETE
- Step 03 — Goal to one narrow task: COMPLETE

## Current goal

Read one task-relevant repository context without modifying the repository in any way.

## Hard-start evidence

- Step 04 moved to completed Step 03 lineage.
- Step 03 one-task contract is verified and recorded.
- Complete Field control set and active Step 04 section reread.
- Read-only invariant confirmed as mandatory.

## Known-good state

Field can start, persist validated state, and accept exactly one bounded task.

## One allowed change

Add only a read-only repository reader/context bundle and repo-reader-only tests.

## Exact success test

1. create a temporary fixture Git repository with committed files;
2. capture HEAD, branch, working-tree status, and byte hashes before read;
3. Field reads repository identity and only task-scoped relevant files into a context bundle;
4. returned context reports exact HEAD, branch, and file contents;
5. after read, HEAD, branch, status, and byte hashes are identical to before;
6. prior Step 01-03 regression tests remain passing.

## Must not add in Step 04

- file editing
- proposal generation
- model calls
- diff generation for changes
- target-project command execution
- retry/controller behavior
- Void logic

## Next allowed action

Create `Field_Coder/field/repo_reader.py` and `Field_Coder/tests/test_repo_reader.py`, then run the read-only invariant test plus prior regressions.

## Hard stop

Stop after the context bundle is correct, byte-for-byte/working-tree immutability is proven, prior tests pass, and diary/progress are updated.