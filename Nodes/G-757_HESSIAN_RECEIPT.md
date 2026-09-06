# G-757 Hessian receipt (2026-09-06)

14 coordinates: amplitudes `a_0..a_6` then phases `phi_0..phi_6`.
Finite difference `h=1e-5`. Default G-757 coefficients, `chi=0`.

## Dipole seeds (physical: dipole not zero)

`dipole_seed(0.08, well=0)` and `well=pi`, `E_M = alpha_M sin^2 theta`:

```
E = 0.01152
lambda = [
  0.000000,   # global phase zero mode
  0.127017,
  0.200000, 0.200000, 0.200000, 0.200000,
  ...
  3.600000, 7.872983, 37.658333
]
n_negative = 0
n_soft = 1
```

Both wells give the same spectrum to printed precision. Locally they are **minima** after quotienting global phase.

## Symmetric point with sin^2 theta

`C=S=0` makes `theta = atan2(S,C)` non-differentiable. Finite-difference eigenvalues explode to `O(10^9)` with five huge negatives. That is a coordinate singularity, not a physical saddle of the four-interaction hold. Do not classify the vanishing-dipole point with `sin^2 theta`.

Smooth replacement that agrees with the seeds at finite dipole: `E_M = alpha_M S^2`. At the symmetric point that form stays PSD with one zero mode (`lambda_min = 0`, `lambda_max ~ 7.87`).

## Reading

- One zero mode is required (global phase).
- No extra unstable mode at the finite-dipole wells for this coefficient set.
- Two-basin *survival* is therefore local-minima survival for this slice. A connecting path and its saddle Hessian are not computed yet.
- Not C-322. Not GeV.
