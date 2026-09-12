# Solver convergence qualification receipt

Change: explicit nonlinear solver convergence reporting.

Acceptance checks:

- ordinary linear divider converges and reports a residual within tolerance;
- ordinary flashlight calibration and regression packs remain green;
- SPICE DC sweep qualification remains green;
- a deliberately under-iterated forward-biased diode (`maxIterations: 1`) must return `solver.converged === false`;
- the under-iterated case must emit `SOLVER FAILED:`;
- `diagnose()` must report `solverFailed: true` for that result.

GitHub Actions run 34672445791 passed all existing breadboard checks plus the new solver convergence qualification before this receipt was added. The receipt adds no runtime behavior.
