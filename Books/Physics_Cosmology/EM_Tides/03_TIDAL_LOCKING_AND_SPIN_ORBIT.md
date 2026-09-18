# Tidal Locking and Spin-Orbit Dynamics

## Model hierarchy
1. Point-mass orbital baseline.
2. Extended deformable body.
3. Viscoelastic phase lag.
4. Angular-momentum transfer.
5. Eccentric forcing and heating.
6. Resonance capture.
7. Optional One-Wave displacement-response extension.

## Conservation ledger
For a simplified two-body system, track:

\[L_{\rm total}=I\Omega+m\sqrt{GMa(1-e^2)}.\]

The simulation must verify:

\[dL_{\rm total}/dt\approx0,\qquad dE_{\rm mechanical}/dt=-P_{\rm diss}.\]

## Reference cases
| Case | Baseline result to reproduce |
|---|---|
| Earth-Moon-like system | Spin-down of the primary, orbital expansion of the companion, tidal heat |
| Synchronous satellite | Average torque approaches zero near \(\Omega=n\) |
| Mercury-like case | 3:2 spin-orbit resonance can be stable under suitable eccentricity and dissipation |
| Eccentric moon | Periodic deformation and internal heating |
| Three-body extension | Perturbation, resonance, and angular-momentum exchange without numerical drift |

## One-Wave discriminator
A field-displacement formulation is useful only if it produces a non-arbitrary torque law and makes an additional prediction beyond the established tidal model. Merely reproducing the same result with renamed variables is an interpretation, not a new theory.
