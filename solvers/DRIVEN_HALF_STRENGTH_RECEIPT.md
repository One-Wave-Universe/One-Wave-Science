# Half-strength displacement: larger-box measurement closure

[Exact eight-case execution receipt](driven_half_strength_results.json) ·
[Original 20-case receipt](DRIVEN_BULK_RECEIPT.md) ·
[Unchanged runner](run_driven_bulk.py).

## What changed

The earlier side32/width3 half-force signal was unresolved under the combined
chart policy. A **side48/width3** repeat now resolves that signal and checks its
timestep dependence. This closes a measurement gap for this declared numerical
control; it does not alter the earlier side32 result or derive physical mass.

No equation, coefficient, normalization rule, engine, wrapper, UI or test code
changed. The original 20-case JSON remains intact.

## Source and protocol

Execution source: `One-Wave-Universe/One-Wave-Science`, merged main
`d89ebdca606b26089267b7ff5903eb5c940cf3dc`. The tested local task head was
`b6e5fbef4762a3a73b9a29a270902d5753653d9c`; the four numerical source bytes are
identical to that merge. Exact SHA-256 values are embedded in the new JSON:
`bulk_excitation.py`, `joint_boundary_response.py`, `driven_bulk.py`, and
`run_driven_bulk.py`. All four were checked again after execution.

Parameters: periodic FCC side48, spacing1, Gaussian width3, conserved norm1,
linear control (focusing=saturation=0), lowest-band projector with both FCC
aliases retained, duration T=2, x-directed periodic-potential drive, other
coefficients unchanged. Eight new runs:

- f=0,+0.005,-0.005 at dt=0.02;
- f=0,+0.005,-0.005 at dt=0.01;
- f=+0.01,-0.01 at dt=0.01.

The strong-force dt=0.02 comparator is the **side48/width3** pair already in
`driven_bulk_results.json`; do not substitute its side32 or width4.5 cases.
Increasing box size changes the sinusoidal drive wavelength. These comparisons
use the same side48 box; they are not a claim of unchanged forcing across boxes.

Measured computation time was 127.143 seconds with single-threaded BLAS/OpenMP
on the isolated execution host. Python 3.12, NumPy 2.3.5, SciPy 1.17.0. Reproduce the
numerical runs without editing source:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python - <<'PY'
import sys, json
sys.path.insert(0, 'solvers')
from run_driven_bulk import run
cases = [(f, dt) for dt in (.02, .01) for f in (0, .005, -.005)]
cases += [(.01, .01), (-.01, .01)]
print(json.dumps([run(48, 3, f, dt) for f, dt in cases], indent=2))
PY
```

## Matched displacement and temporal checks

Define D± = X±(T)−X0(T), using each run's displacement from its initial centroid.
Report the zero-run drift rather than silently removing it from the receipt.
At dt=0.01 it is about −2.131e-12 along x.

| f magnitude | Matched + displacement, dt=.01 | Matched − displacement, dt=.01 | Largest dt=.02→.01 spread |
|---|---:|---:|---:|
| .005 | +0.0026447693660 | −0.0026447693107 | 7.444e-12 |
| .01 | +0.0052894798672 | −0.0052894798118 | 1.269e-11 |

For half-force, the combined force-run-plus-zero-run chart diagnostic is about
7.321e-10. Both that diagnostic and the timestep spread are far below 10% of the
signal. All eight runs retain valid charts, and maximum relative norm drift is
2.578e-13. The half-force maximum energy/work residual reduces from about
4.704e-13 to 1.229e-13 under timestep halving; its zero-drive control is already
near roundoff. This is a numerical convergence/control result.

The chart policy uses concentration, seam norm and internal-step sampling.
L times seam norm is a conservative heuristic indicator for its chosen seam
band, **not a rigorous global error bound for arbitrary multimodal fields**.
The small transverse/baseline drift remains in the raw receipt.

## Nearly proportional is not exactly proportional

Use the odd response A(f)=(D+−D−)/2. The common zero-control term cancels in A.
At dt=0.01:

- A(.005) = 0.0026447693383357;
- A(.01) = 0.0052894798394946;
- A(.01)−2A(.005) = −5.8837177e-8;
- relative departure = −1.1123433e-5, about **−11.12 ppm (−0.001112%)**.

The propagated odd-response chart diagnostic is about 1.239e-9 (do not count
the canceled zero-control term twice), and the departure changes by only
2.196e-12 when dt halves. The small finite-force correction is therefore
resolved relative to these declared diagnostics, rather than forced to vanish
by a chosen tolerance. This is neither an exact linearity claim nor a failure
of the model's infinitesimal linear-response limit.

This control does not establish an inertia, particle mass, physical units,
nonlinear pinned-state response, stable four-interaction recurrence, or the
C-318/G-759 work-metric closure. Those remain separate questions.

## Evidence-only branch-step and review

MAIN GOAL: retain reproducible consequences of the Field/Void software and
physics-control loop. WHY: close the named half-strength measurement ambiguity
without changing the physics to make a result pass.

Reference/hard start: fresh main d89ebdca, clean task worktree, matching frozen
source hashes and completed read-only execution. Choice: add this brief and the
exact eight-case JSON, plus contextual pointers in the prior receipt and lab
README. Those four files are the entire allowed scope. All original source,
workflow/test files, prior 20-case JSON, other science work and hardware are
protected. Root and independent physics pre-review ALLOW.

Field: retained the result byte-for-byte, identified the prior comparator and
reported both the measured signal and its finite-force correction. Independent
physics post-execution review ALLOW: named measurement gap resolved at the
stated grid/width/time, with no broader physical interpretation. Attempt 1/1
for this evidence-only retention; no numerical law repair or parameter tuning.

Proof: byte comparison to the execution artifact, all four source hashes,
independent arithmetic/diagnostic review, existing numerical/API tests and
relevant CI. Publication still requires final evidence-diff review and CI.
Hard stop: any source mismatch, changed prior data, unsupported extrapolation
or failed acceptance. Look-back: the earlier ambiguity was a measurement-scale
problem, not justification for an invented mass. Next permitted scientific work
must begin with a fresh reference and a separately bounded question.
