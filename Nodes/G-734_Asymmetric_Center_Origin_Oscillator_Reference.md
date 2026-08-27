# G-734 — Asymmetric Center-Origin Oscillator Reference

**Status:** YELLOW dimensionless mechanics / Field derivation open  
**Dependencies:** B-208, B-216, B-222, G-729–G-733

## Reference equation

`x_ddot+c*x_dot+a*x^3-b*x-h=u(t)`, with
`V(x)=a*x^4/4-b*x^2/2-h*x` and `c=2*zeta*omega_ref`.

For `a,b>0`, the exact saddle-node bias is

`|h_fold|=2*b^(3/2)/(3*sqrt(3*a))`.

Below the fold the potential has two stable equilibria and one unstable saddle.
Above it only one stable equilibrium remains. For `a=b=1`,
`|h_fold|=0.384900179...`.

## Locked reference mechanics

- exact cubic equilibria and curvature stability;
- conservative well-to-saddle barrier energies;
- deterministic RK4 trajectory integration;
- energy/work/dissipation balance;
- center-crossing and center-dwell measurements;
- small-signal amplitude and phase lag around a stable well;
- stable-well recovery after perturbation;
- bias mirror symmetry.

At zero bias the conservative separatrix energy is the saddle potential. Each
well has barrier height `1/4` in the `a=b=1` reference system.

## Boundary on claims

This is a dimensionless gate-mechanics reference, not the fundamental
One-Wave equation and not quark physics. Its coefficients require derivation or
calibration from the selected Field model. It becomes a simulator component
only when coupled to a declared chapter mechanism and Gray control.

## Executable authority

- `One_Wave_Bench/dynamics/asymmetric_oscillator.py`
- `One_Wave_Bench/dynamics/test_asymmetric_oscillator.py`

Fourteen oscillator tests pass.
