# Math dependency and verification framework v1

This is an **additive** implementation referencing, not replacing, `MATH_BACKBONE/00_MATH_BACKBONE_LOCK.md`, `CORE_RULES_LOCK.md`, `GENERAL_REFERENCE_RULES.md`, `AI_CANONICAL_START_HERE.md`, `AI_FOREMAN_WORK_REGISTER.md`, and `Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md`.

## Purpose
Each model declares equations, units, evidence class, source references, assumptions, test functions and permitted interpretation. The runner validates schema, runs deterministic controls and prints machine-readable JSON. It cannot infer unregistered mathematics, prove new physics, or automatically classify every node in this large repo.

## Usage
```sh
python3 Math_Verification/verify.py --all
python3 Math_Verification/verify.py --model harmonic_butterfly
python3 Math_Verification/verify.py --list
```
No external Python packages. Exit 0 if all selected tests pass, nonzero otherwise. CI executes the same tests.

## Registration and review workflow
1. Read canonical source and metadata; resolve node aliases before registration.
2. Add an entry to `registry.json` with owner, source path, equations, assumptions, units, evidence class, test suite, and falsification boundary.
3. Implement reproducible baseline tests with independent known controls, not theory-specific acceptance thresholds.
4. Run tests; inspect JSON receipt. Keep `unverified` physical claims unverified even when arithmetic tests pass.
5. Add required CORE-RULES-PRE, MATH-BACKBONE, CORE-RULES-POST markers to the **initial PR body**; do not rely on editing the body and rerunning an old event.
6. Do not promote claims into canonical science or modify CELL_V1 from these tests alone.

## Roadmap
Extend registry by actual node IDs after inspecting each source; add dimensional analysis, numerical stability/convergence tests, energy accounting, coupled oscillator integration and instrument-data comparison. Model selection is explicit, not keyword inference.
