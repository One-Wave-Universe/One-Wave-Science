# Direct research connections — canonical cross-repository graph

**Status:** ACTIVE navigation and evidence-routing contract. This file owns cross-domain *references*, not duplicate physics equations, software, or measurements.

## One continuous evidence chain

`SOURCE / PRIOR ART → SCIENCE NODE → CHAPTER / EQUATION → BUILDS MODEL → SOLVER FIXTURE → EXPERIMENT → RAW MEASUREMENT → RECEIPT → VERIFICATION GATE → NODE UPDATE`

The return edge is mandatory. A test result that cannot be traced back to the exact hypothesis and version it tested is not a scientific validation receipt.

## Live connection graph

| Science authority | Question / mathematical scope | Builds implementation or test authority | Required return evidence |
|---|---|---|---|
| [C-311](Nodes/C-311_Electric_Magnetic_Duality.md) | electric/magnetic projections | [3D circuit and field models](https://github.com/One-Wave-Universe/Builds/tree/main/Virtual_3D_Electronics) | Maxwell baseline, solver residual, independent field measurement |
| [D-401](Nodes/D-401_Flux.md) | magnetic flux and conservation | [Magnetic solver](https://github.com/One-Wave-Universe/Builds/blob/main/Virtual_Breadboard/MAGNETIC_SOLVER.md) | winding EMF, flux, sign, energy, numerical convergence |
| [C-319](Nodes/C-319_Magnetic_Lattice_Reorganization.md) | proposed reorganization R and K_L | [Triangulation protocol](https://github.com/One-Wave-Universe/Builds/blob/main/validation/TRANSFLUXOR_MULTISCALE_TRIANGULATION.md) | calibrated conventional model plus distinct holdout prediction |
| [C-320](Nodes/C-320_Magnetic_Compression_Path_Coupling.md) | proposed compression-gradient coupling | [Reality-first contract](https://github.com/One-Wave-Universe/Builds/blob/main/validation/REALITY_FIRST_CONTRACT.md) | explicit independent discriminating residual, not a transfluxor-only inference |
| [G-749](Nodes/G-749_Point_Rotation_and_Angular_Momentum_Receipt.md) | point frame, mechanical angular momentum | [Magnetic/torque triangulation](https://github.com/One-Wave-Universe/Builds/blob/main/validation/TRANSFLUXOR_MULTISCALE_TRIANGULATION.md) | measured torque, angle, inertia and energy |
| [G-769](Nodes/G-769_Path_Rotation.md) | geometric path turning distinct from spin | [Magnetic/torque triangulation](https://github.com/One-Wave-Universe/Builds/blob/main/validation/TRANSFLUXOR_MULTISCALE_TRIANGULATION.md) | path geometry and rotation receipts, separately from local m |
| [C-325](Nodes/C-325_Transfluxor_Magnetic_Solver_Triangulation.md) | cross-scale experimental gate | [3D builder](https://github.com/One-Wave-Universe/Builds/tree/main/Virtual_3D_Electronics), [breadboard](https://github.com/One-Wave-Universe/Builds/tree/main/Virtual_Breadboard), [runner](https://github.com/One-Wave-Universe/Builds/blob/main/validation/bench-3d-perf.js) | model/solver/bench status and raw-data references |
| [Chapter 09](chapters/09_Transfluxor_Magnetic_Reorganization_and_Point_Rotation.md) | integrated scientific narrative | [Builds work package](https://github.com/One-Wave-Universe/Builds/blob/main/validation/TRANSFLUXOR_MULTISCALE_TRIANGULATION.md) | revisions tied to C-325 and [V1 matrix](V1_VERIFICATION_MATRIX.md) |

## Required metadata on every new experimental receipt

```yaml
receipt_id: <stable-id>
science_node_id: <governed node id>
science_commit: <exact commit sha>
equation_or_claim_id: <specific equation/test>
builds_commit: <exact commit sha>
fixture_path: <repository path>
model_version: <version>
source_dataset: <URL, DOI or immutable data hash>
calibration_or_holdout: <declared>
parameters_and_units: <declared>
solver_and_tolerances: <declared>
uncertainty: <declared>
result: PASS | FAIL | INCONCLUSIVE | INVALID | UNMODELED
evidence_level: NUMERICAL | REFERENCE | BENCH | PHYSICAL
raw_receipt_uri: <immutable link>
```

Do not fill missing fields with guesses. Missing provenance means INVALID or INCONCLUSIVE, not PASS.

## Update protocol

1. Begin from `GENERAL_REFERENCE_RULES.md`, `AI_CANONICAL_START_HERE.md`, and the owning node's metadata.
2. Resolve the scientific claim and experiment to the authoritative node, chapter and Builds source.
3. Run controls and tests without altering expected outputs to match results.
4. Preserve original raw output and immutable code/data references.
5. Update the owning Science verification ledger with the actual result and its scope.
6. Revise the theory only through a new explicit hypothesis version; retain prior failures.
7. Update this graph only when a link or ownership boundary changes, not to duplicate technical text.

**Present status:** The graph is linked at the document/source level. No automatic bidirectional event transport or receipt ingestion has been verified. Building those pipelines is an open engineering task.

**Reality is validation through consequence.**
