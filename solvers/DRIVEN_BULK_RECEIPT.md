# Controlled periodic push: numerical receipt

[Exact 20-case output](driven_bulk_results.json) · [Runner](run_driven_bulk.py) ·
[Wrapper](driven_bulk.py) · [Control tests](test_driven_bulk.py) ·
[Source-binding test](test_driven_report.py).

## Subsequent measurement follow-up

The [eight-case side48/width3 follow-up](DRIVEN_HALF_STRENGTH_RECEIPT.md) resolves
the half-strength matched displacement and adds a direct timestep check for that
configuration. The original 20 cases and side32 limitations below remain unchanged.
It also measures a small finite-force departure from exact proportionality.

## Scope and reproducibility

This is an external-drive experiment on the existing dimensionless linear bulk
constitutive control. It is not a particle identification, fitted mass,
physical-unit calibration, or derivation of C-318/G-759. The original bulk and
joint-response equations were not edited. Source SHA-256 values are retained in
the JSON, and CI rejects a stale report.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python solvers/run_driven_bulk.py > solvers/driven_bulk_results.json
python solvers/test_driven_bulk.py
python solvers/test_driven_report.py
```

The report was generated with Python 3.12, NumPy 2.3.5 and SciPy 1.17.0. It
captures source hashes at startup and rejects source drift. One preliminary
sweep failed final serialization because a NumPy boolean escaped the receipt;
that output was discarded. An explicit bool conversion and direct JSON/HTTP
regressions precede this successful report.

## Verified consequences

- All 20 runs have valid charts under the declared conservative policy; maximum
  norm relative drift is 1.282e-13 without evolution renormalization.
- For side32/width3 and +0.01 drive, maximum total-energy-minus-source-work
  residuals are 1.228e-11, 3.069e-12 and 7.663e-13 for dt=0.04, 0.02 and 0.01.
  The factor-four reduction is the expected second-order splitting behavior.
- Independent q-zero lower-band Hessian finite differences converge from
  0.299986669 through 0.299996667 to 0.299999167 as dq halves. The analytic
  long-wavelength value for these input coefficients is 0.3 I.
- Native FCC alias partners are retained by the band projector; a parity
  leakage guard and unit test check the reconstructed field.
- Static source-potential energy, potential-gradient force, exact switch work,
  translation intervention work and zero-drive recovery have independent tests.

## Matched controls and limitations

At side32/width3, T=2, dt=0.02, the raw x displacements are +0.0047983433 for
+0.01, -0.0047926144 for -0.01, and -0.0000017235 for zero drive. Report this
nonzero baseline rather than silently discarding it. The odd component is
0.0047954788; the zero-subtracted even residual is 4.588e-6. The latter is not a
roundoff symmetry identity: the finite minimum-image chart has small seam
weight. Side48 at the same width reduces the even residual to 2.77e-11, but
also changes the periodic potential's wavelength. This is not an identical
forcing profile on a larger box.

The ±0.01 side32 matched displacement passes the combined baseline-plus-driven
chart diagnostic and its own timestep refinement. Half-force side32 runs pass
the individual geometric display policy, but the matched-zero signal (~0.00240)
is below ten times the combined diagnostic (~0.002592 required). Therefore the
half-force matched motion and a linearity claim remain **unresolved under that
policy**, not disproven and not a failed physical law.

For the wider-packet controls (side48/width4.5 and side64/width6), the finite-window
ratio of odd displacement to half T² times the initial measured force is
approximately 0.29316 and 0.29609, approaching the side32 value 0.28549 toward the
long-wavelength limit. These are descriptive trajectory ratios, not inertias
or exact targets: force varies in space/time and interband/deformation effects
can contribute. Larger-grid cases pass the geometric policy but do not have
separate timestep sweeps; their temporal convergence is not established here.

The seam quantity L times the seam norm is a declared conservative heuristic,
not a rigorous uncertainty bound for arbitrary multimodal fields. A single
interactive run cannot establish acceleration convergence. Pinning, splitting,
radiation, nonlinear recurrent states, continuum refinement, derived four-role
work metric and physical calibration remain separate scientific questions.

## Review outcome

Independent code/API review passed all controls, complete source/work receipts,
transactional rejection and bounded endpoints. Independent physics review
allowed these scoped numerical consequences and required the matched-half-force
and larger-grid limits above. Live driven desktop/mobile browser acceptance
must separately pass before merging the UI integration.
