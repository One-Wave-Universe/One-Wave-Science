# Controlled periodic push: bounded experiment

MAIN GOAL: reliable Field/Void software construction with reproducible numerical evidence. User explicitly approved continuing from the 3D lab to a controlled-push experiment and energy checks, with independent review before merge.

Reference: merged main b897fa2cb50d5be39100b4265bf95dbf97a2ec15; prior PR204 numerical/browser gates passed and actual screenshots inspected. Ephemeral execution worktree `/workspace/shared/science-native-3d`, task branch `feature/driven-bulk-response-20261005`. Root pre-review ALLOW for additive wrapper, existing canonical solvers protected. Related science PRs and independent hadron-model work excluded.

Choice: expose a small explicit periodic external drive around the existing bulk step, record source/intervention work and actual norm-centroid displacement, with mathematical ambiguity guards and reproducible control tests. No new particle identification, fitted inertia, physical kg, source-calibration or stage promotion.

Allowed files: new `solvers/driven_bulk.py`, its tests/bounded runner/result receipt; native lab server/UI/tests/docs; dedicated CI paths. Existing `bulk_excitation.py`, `joint_boundary_response.py`, scientific nodes/gates, cavity model and hardware files are protected.

Hard start: current source hashes, baseline tests and independent physics review of V phase splitting, exact total energy, force gradient and work switches. Hard stop: norm/ledger failure, unresolved centroid, stale source, reviewer rejection or model-scope drift. Ambiguity is a reporting result, not permission to output a manufactured position or mass.

Field: implemented exact static-potential half phases around original Strang evolution; force switches and discrete translations have separate work entries. A lower-band projector preserves FCC Fourier alias partners. Circular moments choose a chart; ordinary weighted centroid supplies position. Every internal step updates tracking.

Void pre: ALLOW bounded wrapper. Independent physics review required exact source-work ledger, ordinary (not circular) centroid, conservative concentration/seam/sampling policy, lower-band projector, ±force controls and no exact-0.3 assertion for finite packets. Independent code review required strict numeric input and complete translation receipts. These corrections are included.

Progress: first exploratory side32/width3 linear trajectory gave roughly 0.2853 normalized short-window response versus long-wavelength 0.3. Independent spectral calculation gave approximately 0.28318 finite-packet curvature, illustrating why the limiting value is not an exact trajectory target. Source-edited exploratory sweep was discarded; the reproducible runner now captures startup hashes and rejects source drift before publishing its report.

Tests: zero-drive equality, time reversal, force/potential finite differences, exact switch/translation work, norm/energy timestep refinement, periodic centroid crossing, ambiguous fields, FCC alias projector, analytic q-zero Hessian refinement, invalid parameters/event budget, API transactionality, unchanged original suites and live browser controls/export/ledger coverage.

State at writing: implementation and numerical control tests running; full finite-packet sweep and independent final code/physics/browser review are mandatory before publication as complete. This record does not claim physical mass derivation or target-device installation.

Look-back: a force coefficient is an external protocol input; applied force and field response are measured from actual evolving state. Source work is distinguished from numerical drift. Next permitted scientific step depends on the retained matched-control/refinement evidence, not on visual motion alone.

## Final numerical review

The complete 20-case sweep now passes source binding. Independent physics ALLOW:
maximum norm drift 1.282e-13; energy residual quarters under timestep halving;
q-zero Hessian converges to 0.3; side32 ±0.01 matched motion is resolved within
the declared policy and timestep test. Matched half-force response remains
unresolved under combined chart diagnostics; larger grids have no separate
timestep sweeps. The exact retained report and scope are in
`solvers/DRIVEN_BULK_RECEIPT.md`. JSON boolean failure was repaired and tested via
actual HTTP before retaining results. Independent code review ALLOW; live driven
browser screenshots/controls remain the final integration gate.
