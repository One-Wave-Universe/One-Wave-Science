# Orientation & Quaternion Lab Validation

## Controls implemented

1. Axis-angle to unit quaternion conversion.
2. Quaternion vector rotation via `q v q*`.
3. Noncommutative composition check: `qx qy` versus `qy qx`.
4. SLERP on the unit quaternion sphere.
5. ZYX Euler gimbal-lock comparison near pitch = ±90°.
6. Angular-velocity integration using `q_dot = 0.5 q omega` with explicit unit renormalization and a raw non-renormalized comparison track.
7. Torque-free asymmetric rigid body using Euler's rigid-body equations for angular velocity plus quaternion orientation integration.
8. Parent/child frame composition.
9. Three-phase resultant embedded in an arbitrary quaternion orientation frame.

## Offline numerical check

For the torque-free rigid-body control with normalized principal inertias `(1, 2, 3)`, initial body rate `(1.15, 0.7, 1.45)`, RK4 angular-velocity integration, and `dt = 0.0025`, an offline 100-time-unit run produced approximately:

- relative rotational-energy drift: `-7.98e-13`
- relative angular-momentum-magnitude drift: `-3.77e-13`

These numbers validate the standalone rigid-body angular-velocity control at that timestep; they do not validate any One-Wave hypothesis.

## Required failure exposure

- quaternion norm must remain near 1 on normalized tracks;
- raw first-order quaternion integration is intentionally shown drifting away from unit norm;
- Euler-angle singularity must become visible as `|cos(pitch)| -> 0`;
- composition order must show a nonzero orientation difference for generic finite rotations;
- rigid-body energy and world angular momentum should remain stable under timestep refinement;
- perturbations must not silently modify any baseline equation.

Every exported record keeps `solver_affects_hypothesis=false`.
