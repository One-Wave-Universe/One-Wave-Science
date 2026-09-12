# Solver convergence contract

The Virtual Breadboard nonlinear solver must never silently accept an unfinished fixed-point state as a valid physical answer.

Each successful `Circuit.solve()` now returns `result.solver` with:

- `converged`: true only when both nonlinear device state and the final linear system are converged.
- `stateStable`: true only when a nonlinear iteration completes without changing device/core/comparator/etc. state.
- `numericalConverged`: true only when the final MNA residual is within the declared absolute + relative tolerance.
- `iterations`: iterations actually used.
- `maxIterations`: configured ceiling, default 30.
- `maxResidual`: worst absolute equation residual from `A*x - b`.
- `residualTolerance`: `absTolerance + relTolerance * maxEquationScale`.
- `absTolerance`: default `1e-9`.
- `relTolerance`: default `1e-6`.

If the iteration ceiling is reached before device state stabilizes, or if the matrix residual is outside tolerance, the result is not converged. The solver adds a `SOLVER FAILED:` warning and `diagnose()` reports `solverFailed: true`.

The optional fourth argument to `solve(elements, dt, ambientC, solverOptions)` is backward-compatible and is used for qualification and future SPICE-style controls. Supported options are `maxIterations`, `absTolerance`, and `relTolerance`.

Qualification includes an intentionally capped one-iteration forward-biased diode. The first solve uses the old OFF state, the diode flips ON, and the missing second iteration must be reported as non-converged rather than accepted.
