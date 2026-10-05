# D-415: nonlocal balance, what prevents lock, and what is needed

Date: 2026-10-05. Reference main: `007832743369f83b6f4e60e141e6e5e2f8f57952`.
Scope: the existing **2D periodic triangular-lattice candidate**, not the full planetary law, native 3D dynamics, Bell correlations or physical proof of instantaneous influence. D-415 remains YELLOW / ACTIVE_HYPOTHESIS.

## Result

Two missing pieces can be resolved without inventing a new force: the energy functional of the current candidate and its phase-charge transfer equation. They expose a precise obstruction: with positive damping and no supplied power, a nonzero exactly periodic persistent lock is impossible for the continuous-time version of this candidate. Changing positive coefficients or the smoothing length cannot repair that obstruction. Long transients and approximate locks are not excluded by this statement.

The strictly positive global kernel connects the numerical Field, but global connection alone neither confines three excitations nor demonstrates orbital motion. The original audit's lost measurement weight is not automatically lost physical energy; its measurement density is a different diagnostic.

## 1. Energy of the existing equation

Let u be the complex Field, interpreted here as two real components, v its time derivative, L the implemented six-neighbor Laplacian, and C convolution by the existing kernel K. Use the site-area inner product `<a,b> = A_cell Re sum(conj(a_i)b_i)`, with `A_cell=sqrt(3) dx^2/2`.

The semidiscrete equation implemented in time is

`u_tt + gamma u_t = c^2 L u - alpha u - beta |u|^2 u - kappa (I-C)u`.

Its energy is

`E = ||v||^2/2 - c^2 <u,Lu>/2 + alpha ||u||^2/2 + beta A_cell sum |u|^4/4 + kappa <u,(I-C)u>/2`.

The kernel is real, normalized and even on the periodic lattice, so C is self-adjoint. With nonnegative K,

`<u,(I-C)u> = A_cell/2 sum_ij K_(i-j) |u_i-u_j|^2 >= 0`.

The lattice gradient term is also nonnegative. Differentiating E gives the exact continuous-time identity

`dE/dt = -gamma ||v||^2`.

For a closed numerical domain the missing energy goes to the modeled damping reservoir. The existing code does not evolve that reservoir. The audit integrates its heat ledger; it does not add a physical reinjection mechanism.

Units here are the candidate's dimensionless units. Dimensional assignments and constitutive calibration remain open. No physical energy scale is inferred.

## 2. Why the present equation cannot retain an undriven periodic lock

For any exact periodic trajectory of period T, E(T)=E(0). If gamma>0, the identity above requires `integral_0^T ||v||^2 dt=0`, hence v=0. At a static solution take the inner product of the field equation with u:

`0 = c^2 <u,-Lu> + alpha ||u||^2 + beta A_cell sum|u|^4 + kappa <u,(I-C)u>`.

Every term is nonnegative under the default signs, and alpha>0, so u=0 is the only static solution. These statements hold for this finite periodic candidate with alpha>0, beta>=0, kappa>=0, c^2>=0 and an even nonnegative normalized K. They do not prove that all One-Wave architectures lack persistent structures. They also do not forbid undamped time-dependent localized lattice excitations or finite-lived structures; those require their own stability analysis.

## 3. Phase transfer already exists

Define local phase charge `q_i = Im(conj(u_i) v_i)`; this is the complex field's U(1) charge, **not automatically electrical charge, mass or spatial angular momentum**. Then

`dq_i/dt + gamma q_i = c^2 sum_j L_ij Im(conj(u_i)u_j) + kappa sum_j K_(i-j) Im(conj(u_i)u_j)`.

Each symmetric pair coefficient supplies antisymmetric transfers between i and j. Summing all sites cancels internal transfers:

`dQ/dt = -gamma Q`, where `Q=A_cell sum_i q_i`.

Writing `u_i=a_i exp(i theta_i)` exposes the existing `a_i a_j sin(theta_j-theta_i)` phase coupling. Thus the earlier statement that measured Lambda_ab does not feed back is true, but **it does not mean this field lacks phase interaction**. Adding a separate pair-lock force risks double counting. If measured locks are to change stiffness or transfer, they need a derived state-dependent energy and reservoir accounting.

The actual discrete update also has an exact identity. Set

`Q_n = A_cell Im sum conj(u_(n-1)) (u_n-u_(n-1))/dt`.

Because the force has zero total phase torque,

`Q_(n+1) = (1-gamma dt) Q_n`.

This identity is tested directly. Spatial rotation is different: the triangular periodic lattice does not have arbitrary continuous rotational symmetry, so this Q cannot be relabeled a conserved spatial angular momentum or a complete Point–Path–Field rotation ledger.

## 4. Executable evidence

From this directory:

```sh
python balance_audit.py
python -m unittest -v test_nonlocal_field_bench.py
```

The audit writes `balance_receipt.json`, includes source hashes, and exits nonzero when a check fails. Eight checks pass, and all nine existing regressions pass. Execution was in an isolated Python environment, not on the Jetson.

- Force versus finite-difference energy-gradient relative error: 5.54e-10.
- Kernel evenness error: 0; minimum `(I-C)` spectral eigenvalue: 1.11e-16.
- Equal-duration energy-plus-dissipation residuals at dt=.08/.04/.02/.01: 3.97e-4 / 2.52e-4 / 1.39e-4 / 7.29e-5.
- At dt=.01, initial E=6.43762, final E=5.77556, recorded damping transfer=0.662534.
- Maximum exact discrete charge-recurrence error across those runs: 1.23e-13.
- Damping-off relative energy error at dt=.01: 3.22e-6; charge error: 1.11e-13.

This is a mathematical/numerical audit of the supplied candidate. The continuum energy is not an exactly conserved invariant of the explicit time discretization. The dissipative residual tends toward first-order convergence, consistent with its one-sided damping. A Taylor-started prior field is used only in the audit to compare the same initial u,v; production seeding and dynamics are untouched. Tests cover this configuration and duration, not all grid sizes, amplitudes or stability regimes.

## 5. What a solution now needs

1. **A declared sustaining balance.** If nonzero periodic motion is intended, either remove damping in the explicitly closed conservative limit or supply an explicit reservoir/flux with average input `gamma <||v||^2>`. Simply choosing negative damping is not a conservative mechanism. Updated 41 does not require a stored wake relay; this audit does not add one.
2. **A stable bounded recurrence.** Derive its constitutive/boundary terms from the coupled architecture. Verify a nonzero profile, perturbation spectrum and stability at fixed conserved quantities where appropriate. A convex static restoring potential cannot supply a nonzero static well under the conditions above. Uniform phase rotation alone is not a localized three-excitation solution.
3. **Measured phase exchange before extra lock feedback.** Partition the pairwise charge transfers into the existing measurement windows, include moving-window transport, and distinguish real exchange from changing membership. Charge conservation alone is insufficient for spatial rotation.
4. **A physical kernel law and scaling.** Derive the global-reference weights, domain/boundary choice and their dependence on dx, kernel length and dimensional layer. An instantaneous FFT convolution is a mathematical coupling, not proof of a physical communication mechanism.
5. **Trustworthy geometry and identity.** The current observables use Euclidean norms of axial coordinates; a triangular-lattice distance uses `dq^2+dq*dr+dr^2`, multiplied by dx^2. Periodic pair-center unwrapping, merge/split identity and moving-window terms need their own repair before orbit/capture labels can be trusted. This audit does not change those routines.
6. **Then the three-excitation test.** With one fixed law, measure persistence, translation, rotation, lock/break/return, conservation and refinement; promote to native 3D only after the 2D scope is understood. Keep the Gray control separate.

The next useful calculation is the constrained stability of a source-supported bounded recurrence with its complete reservoir or conservative balance. A parameter search that only maximizes lock scores would bypass the obstruction rather than solve it.

## Branch-step and review record

MAIN GOAL: reliable Field/Void software construction with inspectable science receipts. Why this step: turn D-415's observed dispersal into a derived constraint and an executable balance test. Hard start: verified GitHub reference, D-415 code/audits, integration map, canonical start, general rules, AGENTS, I-06, terminology and Updated 41. The earlier three-body PR remains separate.

Route/root: GitHub connector; temporary execution staging `/workspace/scratch/33a9efee9aef/nonlocal_work`, no local repository checkout, no device dirty worktree access. Branch `science/d415-nonlocal-balance-20261005`. Allowed changes: this document, balance_audit.py, balance_receipt.json and a pointer in MATH_GAPS.md. Protected: original field law, measurement functions, physical nodes, planetary controls, all other work.

Field proposal: derive the existing candidate energy/charge identities and verify against its unchanged update. Void pre-review: ALLOW the bounded audit with exact scope. Roles are same-model review, not independent AI agreement. Attempt 1 calculated but JSON serialization rejected NumPy booleans; attempt 2 explicitly converted check values to Python bool and passed. No failed numerical threshold was relaxed.

View/Action: eight executable checks and nine original tests pass. State/Scale: RESOLVED energy/charge audit for the candidate; PARTIAL nonlocal three-excitation solution; DO NOT SCALE physical claims. Void post-review: preserve the distinction between phase charge and spatial rotation, between continuum energy and numerical error, and between an audit and a new physical law.

Reflection: current damping rules out an exact undriven periodic lock, and global coupling already transfers phase. Missing balance and confinement cannot be repaired by labels or lock scores. Hard stop: checked task branch/PR. Next reference must inherit these identities and tackle bounded-state stability without replacing the one-field architecture.
