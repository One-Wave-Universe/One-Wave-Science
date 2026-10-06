# Reciprocal work balance and a reduced boundary-radius lock

**Found: a reciprocal path/circulation work core, and a conditional stable 3D
pressure–tension radius balance. Not yet found: a self-held native FCC knot.**
The two executable controls below isolate those different results rather than
claiming they have already been combined into the complete four-interaction mode.

Reference PR #193 at `a7e1f2bd10cfc7c198c6503b32b366d238a65425`.
Current main comparison `007832743369f83b6f4e60e141e6e5e2f8f57952`;
AGENTS, General Reference Rules, canonical start and Reality Database specification
are unchanged from `d89ebdca606b26089267b7ff5903eb5c940cf3dc`.
Execution is in the isolated calculation workspace, not a Jetson simulation run.

## 1. The reciprocal path/circulation candidate

The [previous closure audit](RECURRENCE_DOMAIN_CHECK.md) identified why the baseline
compression law cannot create curl from zero curl, and why a direct K_L multiplier
breaks reciprocity in its existing kinetic coordinates. This candidate changes
the constitutive law explicitly; it does not rewrite the historical baseline.

C-319 supplies a symmetric traceless reorganization R and positive accessibility
K_L=I+kappa_R R. C-317 supplies the intended twist and boundary role; its actual
coefficients remain unknown. Here R has five orthonormal tensor coordinates per
site. Let q=curl(u) be displacement circulation, not an independently proven
magnetic observable. It is not automatically the velocity circulation used in
C-317. Define W_q=q tensor q-|q|² I/3. The new energy is

    V = V_native - (1/2)<u,L u> + E_path + E_R,
    E_path = DeltaV/4 sum_undirected_edges w_ij |u_i-u_j|²,
    w_ij = 1 + (kappa_R/2) n_ij^T(R_i+R_j)n_ij,
    E_R = DeltaV sum_i [mu/2 ||R_i||² - g_R R_i:W_qi
                        + g_R²/(2mu) ||W_qi||²]
          + (d_R/2)<R,L R>.

Spacing is 1 in these runs. The bracketed local energy is exactly
mu/2 ||R-(g_R/mu)W_q||². The positive stabilizing term is retained, not omitted
from the force. K_L must remain positive definite; leaving that domain stops a
run. Positive K_L gives positive edge weights but does not prove the full native
compression/excitation potential is bounded.

All psi, u and R forces are derivatives of this same V. Their kinetic weights
are numerical unit choices, not measured Mass Effect. The new reversible R
coordinate is a conservative constitutive hypothesis, not a derivation of
C-319's first-order relaxation or hysteretic memory. Strain also drives R through
E_path; that is an explicit extension of the owner's magnetic-only source.
No unreported damping, normalization, reset or imposed spatial well is used.

The five-component R force at fixed psi,u is

    (mu I+d_R L) r - g_R projection_5(W_q) + S_path = 0,

where S_path is the derivative of the edge energy. Because mu>0 and L>=0, this
conditional balance has a unique solution. It is **conditional R balance**, not
simultaneous force equilibrium, persistence or a knot lock.

### Native controls and observed path response

Fixed candidate values: side 4, 32 native FCC sites, kappa_R=.4, g_R=.3, mu=2,
d_R=.2; the old beta=shear=k=a_c=1, eta=2 remain fixed. The three-dimensional
12-neighbor graph remains separate from 2D sixfold and 24-state recurrence views.

Six implementation controls pass:

| Check | Measured error |
|---|---:|
| Energy directional derivative | 2.77e-11 |
| Reciprocal mixed force derivative | 1.85e-10 |
| Coupling-off native force recovery | 1.11e-16 |
| Coupling-off native energy recovery | 0 |
| Conditional R force balance | 1.12e-18 |
| Zero-input force | 0 |

Six trajectories use the same candidate law: compression only; its half-timestep
repeat; seeded circulation with conditionally balanced R; that state's half-step
repeat and 1% positional perturbation; and coupling-off compression. The runs
last 20 time units, with dt=.01 or .005. Radius-1 activity is measured at the fixed
original center. The preliminary lock screen requires completion, scaled energy
error <.005, >=.8 activity throughout the final quarter and two full-state return
minima <=.1 after time 5, separated by at least 1. It is a screen, not a stability
proof. Activity is psi²+v_psi², not conserved energy.

All complete with positive accessibility. The seeded-circulation case has max
energy error 1.09348e-5, improving to 2.73368e-6 at half dt. Its minimum late
localization is only .31830 and there are no qualifying returns. The perturbed
case also fails localization/return. The initially curl-free compression case
produces a small nonzero displacement curl, about 2.04e-8, whereas the coupling-off
case stays near 1.37e-16. The half-step repeat is recorded in the raw results;
this is a small effect under illustrative coefficients, not a persistent vortex.
The new reciprocal terms permit the channel missing in the baseline, but do not
supply the missing holding boundary.

[Path executable](reciprocal_path_lock.py) · [Path measurements](reciprocal_path_lock_results.json).

## 2. The 3D pressure–tension balance and radius lock

C-317's surface energy is E_skin=4 pi sigma_T R² for a sphere. Take one declared
cavity recurrence coordinate Q with conjugate momentum P_Q and candidate
frequency Omega(R)=a_omega/R, where a_omega=c zeta is a frequency-times-radius
coefficient. This inverse-radius law is a **mode-reduction assumption**; the
spatial reflecting carrier and its boundary condition have not been derived by
the native FCC solver.

Give the boundary an actual evolving radius R and momentum P_R:

    H = P_Q²/2 + a_omega² Q²/(2R²)
        + P_R²/(2W_R) + 4 pi sigma_T R²,
    dot(Q)=P_Q,
    dot(P_Q)=-a_omega² Q/R²,
    dot(R)=P_R/W_R,
    dot(P_R)=a_omega² Q²/R³ - 8 pi sigma_T R.

This instantaneous Hamiltonian is what the executable evolves. The outward
force and the effect of radius on the recurrence are reciprocal derivatives of
one energy, not a one-way pressure drive. R is not clamped. W_R is an illustrative
boundary kinetic weight, not assigned physical Mass Effect. No force through the
boundary is modeled; the coordinate describes moving-surface pressure work.

When the radius varies slowly compared with the carrier recurrence, its
adiabatic action J=E_carrier/Omega gives the averaged potential

    U_avg(R)=J a_omega/R + 4 pi sigma_T R².

J is used to predict the balance and initialize the carrier. It is **not** held
constant or reset during the exact coupled evolution.

The competing pressures are

    DeltaP_carrier = J a_omega/(4 pi R⁴),
    DeltaP_tension = 2 sigma_T/R.

At the stationary radius they match:

    R_*³ = J a_omega/(8 pi sigma_T),
    U_avg''(R_*)=24 pi sigma_T > 0.

The positive curvature is the radial stability condition in this averaged
reduction. More generally a spherical balance requires DeltaP(R_*)=2 sigma_T/R_*
and radial stability requires DeltaP'(R_*) < -2 sigma_T/R_*². Merely matching the
pressures at one radius is insufficient. Here the wave pressure varies as R^-4,
so an outward deviation weakens it faster than the inward tension pressure;
an inward deviation strengthens it faster.

Dimensions close: [J]=energy*time, [a_omega]=length/time and
[sigma_T]=energy/length², so the right side has units length³. This is a 3D surface
result, not a 2D circumference law. It is a reduced boundary-radius lock, not a
claim of three Vortex Phase locking or an observed particle.

### Free-radius runs and ablations

Illustrative values sigma_T=.01, a_omega=1, W_R=100 and J=8 pi sigma_T give
R_*=1, both averaged pressures .02, curvature .75398224 and small radial
frequency .08683215. The latter is slow compared with the unit carrier frequency,
consistent with the averaged regime. The instantaneous equations, not an averaged
radius force, are integrated for 200 time units.

| Run | Observed radius range | Max scaled energy error | Radius screen |
|---|---:|---:|---|
| Balanced initial radius | .998849–1.001255 | 6.28e-6 | Pass |
| Half timestep | .998849–1.001255 | 1.57e-6 | Pass |
| +10% initial radius | .905531–1.100655 | 7.20e-6 | Pass |
| -10% initial radius | .900000–1.107293 | 8.59e-6 | Pass |
| No surface tension | Grows beyond radius 5 at t=83.47 | 6.24e-6 before stop | Fail |
| No carrier recurrence | Falls below radius .05 at t=30.34 | 7.88e-9 before stop | Fail |

The radius screen is declared before interpretation: complete t=200, remain
within (.8,1.2), and energy error <1e-4. All five boundary implementation/outcome
checks pass, including both perturbations and both ablations. The balanced run's
late mean wave and tension pressures are .0200152 and .0200012. These finite-window
averages are not exact instantaneous equality. Halving dt reduces energy error by
four. The conservative perturbed trajectories oscillate around the balance;
there is no dissipative attractor or claim that phase errors are erased.

[Boundary executable](boundary_balance_lock.py) · [Boundary measurements](boundary_balance_lock_results.json).

## Reproduce

```sh
OPENBLAS_NUM_THREADS=1 python solvers/reciprocal_path_lock.py > solvers/reciprocal_path_lock_results.json
python solvers/boundary_balance_lock.py > solvers/boundary_balance_lock_results.json
```

The path program needs NumPy/SciPy and the prior native/recurrence modules;
the radius program needs NumPy. Path exit success certifies six implementation
controls, not localization. Boundary exit success certifies the stated reduced
radius checks, not spatial carrier confinement or the complete knot.

## Field/Void receipt and what the lock means

User goal: find the balance and the lock, then update the repo. Choice: one bounded
reciprocal work/boundary-balance cycle with two separately scoped executable cores.
Allowed: the two candidate executables, raw results, this report, laboratory pointer
and additive C-317/C-319 receipts. Protected: existing solver laws and data, node
metadata/gates, hardware, the four-interaction architecture and dirty Jetson work.

Field supplies a reciprocal path/circulation energy and a pressure-versus-surface
radius balance. Void checks gradients, reciprocity, coupling ablation, zero input,
conditional force balance, full return/localization, timestep controls, radius
perturbations and removal of each balancing term. Same assistant proposed and
checked the candidates; this is not independent corroboration. The path run is
repeated with a half-step compression control and exact return-separation rule.
No failed path lock is relabeled as a successful full knot.

State: reciprocal work core and reduced radius lock RESOLVED within declared
models; native persistent spatial lock remains PARTIAL. Scale: retain the
pressure–tension relation as a candidate mechanism and a quantitative target,
not a physical calibration, full Knot Lock or measured Mass Effect.

Next concrete integration: let the native spatial recurrence exchange work with
an evolving closed 3D boundary, then measure whether its internal carrier actually
remains confined while meeting DeltaP=2 sigma_T/R and the negative pressure-slope
condition. Replace the assumed inverse-radius carrier law with a computed mode
response, preserving reflected/deflected/tangential channels and Mirror phase
coupling. Carry R and circulation through the same boundary energy ledger. A
stable radial coordinate alone cannot establish the knot, shell, Mirror and weave
phase lock required before translation/time measurements.
