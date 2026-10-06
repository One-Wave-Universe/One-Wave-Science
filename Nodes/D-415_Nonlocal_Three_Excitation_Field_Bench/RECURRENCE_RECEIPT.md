# D-415: three-peak rotating recurrence

**YELLOW numerical candidate.** The unchanged D-415 equation admits a numerically
resolved three-peak rotating field when damping is explicitly set to zero.
This is a stationary spatial pattern with recurring complex phase, not three
orbiting bodies, a dissipative attractor, or a general solution for initial data.
The original defaults and science gates are unchanged.

## Derivation

Write A = -c² L6 + alpha I + kappa (I-K). For gamma=0, the existing equation is
u_tt + A u + beta |u|²u = 0. Substituting u(t)=phi exp(i omega t), with real phi,
gives A phi + beta phi³ = omega² phi. The runner continues from three isolated
nonzero sites through 21 coupling values to the full existing local and nonlocal
couplings. The frequency omega=1.5 is supplied, above the n12 linear band edge
0.950394; it is not a measured particle parameter or a uniquely selected mode.
The seed sites form a triangle of side 4 in the native triangular metric.

No periodic forcing, amplitude reset, fitted attraction or new energy term is
introduced. The existing positive quartic term allows frequency to depend on
amplitude. Finite lattice spacing matters: no continuum claim follows.

For perturbations u=exp(i omega t)(phi+a+ib), the real linearized equations are

    a_tt = -Lplus a + 2 omega b_t
    b_tt = -Lminus b - 2 omega a_t
    Lplus  = A - omega² I + 3 beta diag(phi²)
    Lminus = A - omega² I + beta diag(phi²).

The full position/velocity matrix is diagonalized, including all spatial modes.
The energy functional is inherited from [the balance audit](BALANCE_DERIVATION.md).
Positive damping still excludes an exact undriven nonzero periodic orbit; this
experiment does not alter that result.

## Observed receipt

[Machine-readable results](recurrence_receipt.json) bind the runner, force source
and energy audit by SHA-256. Reproduce with NumPy and SciPy:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench/rotating_recurrence.py
python -m unittest discover -s Nodes/D-415_Nonlocal_Three_Excitation_Field_Bench -p 'test_nonlocal_field_bench.py' -v
```

- n12 stationary relative residual: 4.16e-15. Radius-one neighborhoods of the
  three supplied centers contain 99.9902% of squared field amplitude.
- Largest real part of the rotating-frame spectrum: 1.97e-15. No exponential
  growth was resolved on this grid; this is not a nonlinear stability theorem.
  Selected eigenpair residual: 2.55e-15.
- Over 12 periods (~50.27 time units), maximum relative orbit errors for
  dt .04/.02/.01 are .008402/.002099/.000525. These compare the unforced numerical
  trajectory against the continuous-time ansatz, including accumulated phase error.
- Maximum relative energy errors are 1.21e-7/7.59e-9/4.74e-10. Centered-difference
  velocities are used; no energy rescaling occurs.
- A seeded 1e-4 relative amplitude perturbation gives maximum orbit errors
  .002126/.000595 at dt .02/.01. This small perturbation and short horizon cannot
  establish long-time robustness or distinguish every neutral drift mechanism.
- n18 and n24 stationary profiles also solve to relative residual below 5e-15.
  Peak amplitudes change from 8.86535 to 8.86123 to 8.85943. Their spectra and
  time evolution were not checked. Normalizing the global kernel on each domain
  changes its weights; this is a domain sensitivity check, not a convergence proof.
- Independent central finite difference of the rotating-frame acceleration
  agrees with its analytic linearization to 3.08e-11; global-phase null residual
  is 9.36e-15. A nonzero-damping input is rejected. Original nine tests pass.

SciPy emitted a convergence-ratio RuntimeWarning at the exactly solved uncoupled
starting point. Every continuation stage returned success and passed an explicit
finite residual check. No failed solve was accepted.

## Remaining gap and next experiment

A recurrent three-peak candidate now exists in this finite 2D equation, so adding
a new attraction law is not needed to demonstrate this limited behavior. What
remains is its robustness to phase and velocity perturbations, longer evolution,
larger-domain spectra, lattice refinement, and motion of the peak centers.
The peaks here are stationary and share a supplied frequency. This does not
prove capture, lock acquisition from generic pulses, a moving three-body orbit,
the four coupled C-318 components, or a validated One-Wave physical law.
The separate 3D four-response-coordinate bulk model is not substituted here.

## Branch-step record / progress diary

- MAIN GOAL: reliable Field/Void software-construction engine, exercised through
  a reproducible bounded scientific solver step.
- WHY / CURRENT GOAL: follow the balance audit with an existence and stability
  diagnostic of recurrent three-excitation behavior in the same equation.
- HARD START / REFERENCE: GitHub One-Wave-Universe/One-Wave-Science main
  fcab0b703d117352d4896bccdf51e89960188428 after merging balance audit PR208;
  AGENTS.md, GENERAL_REFERENCE_RULES.md, D-415 source and balance audit,
  A-112, C-317, and solvers/BULK_EXCITATION_DERIVATION.md inspected.
- LOCAL ROOT / ROUTE: isolated staging at /workspace/scratch/33a9efee9aef/nonlocal_work;
  GitHub connector is the repository route. Staging is not a checkout or Jetson.
- ACTIVE BRANCH: science/d415-rotating-recurrence-20261005, based on the above SHA.
- ALLOWED FILES: rotating_recurrence.py, recurrence_receipt.json and this receipt,
  all under D-415. PROTECTED: existing solver, defaults, node gates, 3D bulk and
  all unrelated files.
- EXACT ACTION: additive continuation, full linearized spectrum, unforced
  trajectory refinement and source-bound evidence. No force-law change.
- SUCCESS CRITERIA / CHECKS: report residuals, stability limitations, refinement,
  energy and original regression tests, whether or not a stable state is found.
- FIELD NOTES: the supplied-frequency branch exists with three localized peaks;
  its 12x12 spectrum has no resolved positive growth rate.
- VOID PRE-OVERSIGHT: ALLOW this scoped candidate test; require stability and
  energy evidence, reject any general three-body-solution claim.
- VOID POST-OVERSIGHT: ALLOW scoped numerical receipt; independent derivative
  calculation and nine regressions pass. Larger-grid stability remains unverified.
  Field/Void are same-model sequential roles, not independent models or hardware.
- ATTEMPT / STRIKE COUNT: 1/3; no failed continuation stages. Warning disclosed above.
- LOOK-BACK: existing hard nonlinear response supplies a recurrent branch without
  changing the law. A prescribed recurrent pattern is a narrower result than
  spontaneously formed moving bodies. Existing behavior remains unchanged.
- STATE/SCALE: resolved for this diagnostic; partial for sustained physical lock.
  No scaling or node promotion authorized by these results.
- HARD STOP / HANDOFF: evidence recorded; next cycle tests larger-domain spectral
  behavior and independent phase/velocity perturbations before moving-center claims.
