# Cross-Repo Extraction Ledger

Purpose: remove non-science implementation, tooling, applications, and mythos material from One-Wave-Science without deleting anything before a verified destination copy exists.

## Migration law

For every subtree:
1. identify canonical destination;
2. copy without rewriting;
3. verify destination file count and blob/content identity where possible;
4. repair references/workflows/imports;
5. run destination tests;
6. only then delete the Science copy;
7. record source commit, destination commit, verification receipt, and deletion commit here.

No destructive step is allowed while the destination write path is unavailable.

## Destination repos

- Science: `One-Wave-Universe/One-Wave-Science`
- Builds: `One-Wave-Universe/Builds`
- Bench: `One-Wave-Universe/Bench`
- Mythos: `One-Wave-Universe/Mythos-and-Stories`

## First-pass unambiguous extraction

| Science source | Destination | Destination path | Status |
|---|---|---|---|
| `Virtual_Breadboard/` | Builds | `virtual-breadboard/` | BLOCKED: destination connector is read-only |
| `Builds/` | Builds | merge into appropriate existing build folders | BLOCKED |
| `Hardware_Packets/` | Builds | `hardware-packets/` | BLOCKED |
| `Workshop/` | Builds | `workshop/` | BLOCKED |
| `Android_Body/` | Builds | `android-body/` | BLOCKED |
| `One_Wave_Animator/` | Builds | `apps/animator/` | BLOCKED |
| `Learner_App/` | Builds | `apps/learner/` | BLOCKED |
| `Tools/` | Builds/Bench by subsystem | classify before copy | PENDING CLASSIFICATION |
| `One_Wave_Bench/` | Bench | preserve subsystem paths, with `hive-pipe/` under Bench | BLOCKED |
| bridge/root AI terminal docs | Bench | `bridge-docs/` or canonical Bench entrypoints | PENDING REFERENCE REPAIR |
| `Miniverse/` runtime/app code | Bench/Builds | runtime -> Bench; reusable app/package -> Builds | PENDING CLASSIFICATION |
| explicit mythos/story presentation under `library/` | Mythos-and-Stories | preserve logical book/story grouping | BLOCKED |
| `One_Wave_Times/` creative/editorial material | Mythos-and-Stories | `one-wave-times/` | PENDING CLASSIFICATION |

## Keep in Science

Science-facing material remains when it is theory, mathematics, experimental protocol, raw/processed scientific evidence, falsification criteria, grant/paper material, or scientific validation code directly required to reproduce a result.

Examples:
- `Nodes/` scientific canon and hypothesis/status nodes
- `Books/` scientific manuscripts
- `GRANTS/`
- scientific datasets/results and reproducibility artifacts
- science-specific validation scripts
- `V1_VERIFICATION_MATRIX.md`
- canonical claim/evidence/status governance

## Current blocker

The active GitHub integration can read Builds, Bench, and Mythos-and-Stories but returns `403 Resource not accessible by integration` for both branch creation and contents writes on all three destination repos.

Therefore no source deletions have been performed.

## Resume point

As soon as any authenticated write bridge reaches the destination repos:
1. copy `Virtual_Breadboard/` to Builds;
2. copy `One_Wave_Bench/` to Bench;
3. verify both;
4. repair workflows/references;
5. delete verified Science copies;
6. continue with the remaining classified top-level subsystems.
