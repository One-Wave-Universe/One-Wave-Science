# One-Wave Science Laboratory

**An experimental companion to the One-Wave Science books**  
Author of the One-Wave framework: **Mark Wright Adlard**  
Edition: October 4, 2026 · Editorial contribution: Codex  
Scope: executable models, measurements, controls and derivation work

This book explains how the One-Wave excitation and response questions become calculations. It starts with the working software, follows the quantities that software actually measures, and identifies the next changes that could resolve the physical gaps. It is a scientific laboratory book, separate from the Android book and from fiction.

The governing interpretation is that particles are measured signatures and classifications of field excitations. The field evolves; the detector samples or couples to it; the resulting record is what gets classified. A name does not substitute for a derived excitation or a calibrated detector response.

## Contents and reading order

1. [The Joint Response Laboratory](Ch01_The_Joint_Response_Laboratory.md): one four-coordinate operator, an exact discrete energy ledger, boundary coupling and carried-profile resistance.
2. [Localized Excitations and Measurements](Ch02_Localized_Excitations_and_Measurements.md): a nonlinear periodic-bulk candidate, persistence tests, detector outputs and the controls that constrain its interpretation.
3. [From Candidate to Canonical Derivation](Ch03_From_Candidate_to_Canonical_Derivation.md): the canonical memory recurrence, missing constitutive bridge, four-interaction necessity and concrete acceptance criteria.

Book 1's [Chapter 18](../Book1_Micro/Book1_Ch18_Excitations_Measurements_and_Solver_Evidence.md) connects this laboratory to the Micro book's particle, measurement and Mass Effect chapters.

## What owns the evidence

[General Reference Law](../../GENERAL_REFERENCE_RULES.md) applies. This book explains; canonical nodes own definitions and status; solver source owns implementation; machine-readable receipts own numerical outputs. Do not create a second maintained solver or copy raw data into a chapter.

| Subject | Canonical definition | Executable evidence |
|---|---|---|
| Persistent excitation | [A-112](../../Nodes/A-112_Persistent_Mode.md) | [Bulk derivation and commands](../../solvers/BULK_EXCITATION_DERIVATION.md) |
| Native dimension | [A-117](../../Nodes/A-117_Dimensional_Integrity_and_Projection_Declaration.md), [D-409](../../Nodes/D-409_Twelvefold_3D_Close_Packed_Coordination.md) | [Bulk run report](../../solvers/bulk_excitation_results.json) |
| Measured signal | [E-525](../../Nodes/E-525_Focal_Point_Measurement_Operator.md) | Detector windows in the bulk run report |
| Complete carried response | [C-318](../../Nodes/C-318_Mass_Mechanism_Candidate_Resolution.md) | [Joint derivation and commands](../../solvers/JOINT_RESPONSE_DERIVATION.md) |
| Mirror coupling | [C-322](../../Nodes/C-322_Mirror_Gate_Higgs_Scale_Resonance.md) | [Joint run report](../../solvers/joint_response_results.json) |

The two implemented laboratories have different laws and purposes. The linear reflecting-cavity fixture verifies response and accounting. The first-order nonlinear bulk hypothesis tests localization and sampling without an enclosing reflecting wall. They have not been derived as one canonical physical law. Neither supplies measured particle masses or a 125 GeV prediction.

## Reproduction

From the repository root:

```sh
python -m pip install numpy scipy
python solvers/test_joint_boundary_response.py
python solvers/test_mirror_gate_coupling.py
python solvers/test_bulk_excitation.py
python solvers/run_joint_response.py > solvers/joint_response_results.json
python solvers/run_bulk_excitation.py > solvers/bulk_excitation_results.json
```

Run outputs are dimensionless. Keep the published parameters and controls fixed when reproducing them. Replacing a failed comparison with target tuning invalidates a prediction claim.

## Edition and work record

This edition explains the verified repository at main `58703ad3702a3bf04d753162a46d9a6a72528309`, after PRs 188 and 189. It adds narrative chapters and discovery links, not a new solver, hardware change or live Nexus connection. The recorded suite contains 25 passing solver tests; that establishes their declared numerical checks.

Field prepared one bounded book package; independent Void allowed it with explicit evidence ownership, candidate/canonical separation, and correction of misleading README completion language. Book links, embedded legacy Python syntax and result references are checked before publication. Attempt 1/3. The hard stop is this explanatory edition; the next scientific step must establish a fresh reference and implement one acceptance test from Chapter 3. Protected state: current solver laws, raw receipts, existing chapter numbering and Android canon remain intact.

The consequence of this edition is a usable reading route from concept to implementation to failed and passed controls. Its unresolved state is physical closure, not a missing label: the next worker must inherit the coupling-off localization, spacing sensitivity and lattice-pinning evidence rather than erase or rediscover it.
