# Direct One-Wave recurrence solve with retained compression

Reference: PR #193 at `2c72eaa7c9e83fdabb18b778a0e2f2d5c34fcbe9`.
Main reference `b897fa2cb50d5be39100b4265bf95dbf97a2ec15`; AGENTS,
General Reference Rules, canonical start and Reality Database specification
are unchanged from `a878e481c1354f6e3dc8d0a2e701808564ea8d86`.
Execution is in the isolated calculation workspace, not a Jetson simulation run.

## Exact scope and equations

The unchanged [native compression candidate](native_compression_bridge.py)
retains real excitation psi, vector displacement u and compression chi=-div(u).
All constitutive coefficients remain beta=shear=k=a_c=1, eta=2. Its numerical
kinetic normalization is not measured Mass Effect. No knot, shell, Mirror or
Boundary-Tension Weave operator is added or declared derived.

This step solves directly for a periodic state in an even-time Fourier sector:

    psi(theta) = p1 cos(theta) + p3 cos(3 theta),
    u(theta) = u0 + u2 cos(2 theta) + u4 cos(4 theta),
    theta = omega t.

The temporal second derivative plus the native energy gradient must vanish.
Projecting those equations onto the declared harmonics gives 352 field equations
on 32 native FCC sites (side 4), plus one central excitation amplitude condition and three zero-mean DC
displacement gauge conditions.
Frequency is an unknown restricted to .2 <= omega <= 5. The central condition
p1(center)+p3(center)=A excludes trivial Ground. It is a solve condition, not a
physical force or a reset during subsequent evolution. The DC displacement mean is fixed to zero: a uniform offset is an unforced
gauge and must not inflate the return-distance denominator.

The analytic Jacobian uses the same spatial L and compression C=-div as the
native implementation. If chi=C u, the instantaneous force derivatives are:

    H_pp = L + diag(chi² - 4 chi),
    H_pu = diag[(2 chi - 4) psi] C,
    H_uu = blockdiag(L,L,L) + C^T diag(1+psi²) C.

The reciprocal block H_up=H_pu^T is retained. A centered directional finite
difference checks this Jacobian at a deterministic perturbed state. A separate
exact control psi=A(-1)^x cos(sqrt(8)t), u=0 has uniform psi², no compression
drive and exact periodicity. That control is extended across the box: recurrence
alone does not qualify it as a Persistent Mode.

## Verification contract

Three Gaussian-start solve amplitudes A=.2,.5,1 use the same law and at most 80
nonlinear residual evaluations each. A success flag from the least-squares solver
is not physical success. Full unprojected equation defect is checked at 32 temporal
points, including the harmonics omitted from the fit. A preliminary screen requires
relative equation defect <1e-6, anchor error <1e-6 and >=.8 of mean excitation
activity inside radius 1 around the fixed original center. Radius 1 is a declared
small-box diagnostic, not the previous radius-2 screen or a physical boundary.

Activity is the temporal mean of psi²+v_psi², not a conserved norm or energy.
Effective active sites is (sum activity)²/sum(activity²). Direct velocity-Verlet
integration then runs ten fitted periods, using 400 steps per period; the A=.2
case is repeated with 800. There is no normalization, recentering, fitted phase
alignment or repeated relaxation. Full-state return distance includes psi,u and
both velocities, divided by the initial coordinate-state size. Energy error uses
max(1,|initial energy|) as its denominator.

## Reproduce

```sh
OPENBLAS_NUM_THREADS=1 python solvers/periodic_orbit_solve.py > solvers/periodic_orbit_results.json
```

[Executable](periodic_orbit_solve.py) · [Raw results and fitted coefficients](periodic_orbit_results.json).
NumPy/SciPy required. Exit success certifies the two implementation controls,
not a physical Persistent Mode or independent-model corroboration.

## Field/Void cycle receipt

Goal: progress from seed launch to a directly solved retained-state recurrence.
Choice: one bounded finite-harmonic solve plus direct native evolution checks.
Allowed: new solver, raw measurements, this report and laboratory chapter pointer.
Protected: native law, coefficients, previous data, node gates, hardware and dirty
Jetson checkout. Field: search nonzero recurrence. Void: check exact extended
control, Jacobian, omitted-harmonic defect, localization and direct evolution.
Same assistant performed proposal and check; no independent corroboration.
The initial report encountered a NumPy Boolean JSON serialization error after
three solves. Converting the control flags to native Boolean fixed output; the
final run repeats the solves and adds evolution evidence. No physics changed.

Finite harmonics and even-time symmetry may miss valid recurrences. The small
periodic box cannot establish large-domain localization or outgoing-radiation
cancellation. No time law, Mass Effect, Vortex Phase or Knot Lock follows from a
fit. Further scope depends on the actual measured gates below.


## Measured outcome

**Three finite-box near-periodic states found; no localized Persistent Mode qualifies.**

| Center amplitude | Solved omega | Full equation defect | Central mean activity | Effective active sites | Ten-cycle return error | Max energy error |
|---|---:|---:|---:|---:|---:|---:|
| 0.2 | 2.82703446 | 5.36e-08 | 64.55% | 8.618 | 0.00183 | 2.54e-05 |
| 0.5 | 2.81984879 | 2.04e-06 | 63.21% | 9.080 | 0.00183 | 6.15e-05 |
| 1.0 | 2.79597658 | 2.96e-05 | 58.78% | 10.548 | 0.00183 | 6.1e-05 |

Both implementation controls pass; the Jacobian directional error is
1.46e-12. The exact extended control has full defect
2.11e-16 and effective activity
on all 32 sites. All three fitted states complete direct evolution. Only A=.2
passes the <1e-6 unprojected equation-defect condition; none passes the .8 central
activity requirement. Projected residuals alone would miss the larger-amplitude
omitted-harmonic defects.

For A=.2, 800 rather than 400 steps per period lowers max energy error from
2.5366661e-05 to 6.3416653e-06; ten-cycle
return distance falls from 0.0018274166 to
0.00045685542. Both improve by about four. This supports numerical
convergence over ten cycles; it is not a perturbation-stability or lifetime proof.
The solved frequency lies inside the Ground propagation band, not above it.
Finite-box recurrence therefore does not demonstrate suppression of outgoing
channels in an unbounded lattice.

State: bounded calculation complete; physical recurrence goal remains PARTIAL.
Scale: retain these as small-box recurrence branches, not Persistent Modes,
measured Mass Effects or clocks. No node gate is promoted.
Next bounded action: continue the smallest recurrence branch to a larger FCC
domain, preserving zero-mean displacement and the nonzero anchor, and increase
the temporal harmonics. Check how localization and outgoing-channel residuals
change before selecting a branch for perturbation or translation/timing tests.
If it spreads with domain size, record the missing holding mechanism instead of
assigning the full Boundary-Tension Weave to this reduced law.
