# Experimental Wing Test Matrix

| Module | Baseline/control | Primary metric | Failure exposed |
|---|---|---|---|
| Integrator duel | Newtonian central orbit | relative energy drift | Euler numerical drift |
| Dispersive packet | declared spectral toy | packet width/phase | parameter-driven distortion |
| Coupled modes | discrete oscillator chain | mode frequencies | missing/incorrect modes |
| RLC | linear series RLC | response magnitude | overdamping / off-resonance |
| Thermal diffusion | diffusion equation | peak + heat sum | unstable timestep/transport |
| Lensing | weak point-mass deflection | bend geometry | outside weak-field scope |
| Three-body ensemble | Newtonian figure-eight | ensemble divergence | sensitivity/chaos |
| Blackbody | Planck law | normalized peak/shape | wrong temperature scaling |
| Galaxy curves | declared comparison curves | curve residual shape | toy curve mismatch |
| Redshift | SR + exterior gravity formulas | z against normalized driver | misuse outside formula scope |
| Wake families | 1/r² reference | family departure | arbitrary cutoff behavior |
| Residual bench | synthetic 1/r² control data | relative RMSE | candidate rejection |
| Quaternion axis-angle | unit quaternion rotation | quaternion norm + rotated-vector norm | non-unit orientation state |
| Quaternion composition | SO(3) composition | angle between `qx*qy` and `qy*qx` results | false commutativity assumption |
| SLERP | quaternion great-circle interpolation | unit norm + interpolation fraction | linear interpolation distortion |
| Euler gimbal lock | ZYX Euler representation | `abs(cos(pitch))` | coordinate singularity near ±90° |
| Quaternion rate integration | `q_dot = 0.5 q omega` | normalized vs raw quaternion norm | integration drift without renormalization |
| Torque-free rigid body | Euler rigid-body equations | rotational-energy and angular-momentum drift | unstable or incorrect body dynamics |
| Frame composition | parent × child quaternion | unit norm + transformed axes | local/world frame ordering mistakes |
| Three-phase 3D rotor | classical 120° phase vectors | resultant magnitude + frame norm | incorrect phase/frame composition |
| Uniform vector field | constant analytic field | mean divergence + curl | numerical derivative bias |
| Radial source | analytic softened source | divergence map | missing source topology |
| Vortex | analytic softened vortex | curl map | missing rotational topology |
| Saddle field | `F=(x,-y)` | near-zero divergence + curl | confusing deformation with source/rotation |
| Dipole pair | source + sink superposition | signed topology / derivative map | incorrect superposition |
| Source + vortex | linear field superposition | simultaneous divergence + curl | losing one component under composition |
| Divergence theorem | linear expansion field | boundary flux - area integral of divergence | local/global inconsistency |
| Green/Stokes circulation | solid rotation field | boundary circulation - area integral of curl | rotational integral mismatch |
| Zero-integral saddle | centered saddle field | total flux + circulation residuals | false global source/rotation |
| Mixed integral field | simultaneous div/curl linear field | both theorem residuals | one identity passing while the other fails |

## Quaternion control check

The torque-free rigid-body module has a documented offline 100-time-unit RK4 check at `dt = 0.0025` with approximately `7.98e-13` relative rotational-energy drift and `3.77e-13` relative angular-momentum-magnitude drift. See `orientation-quaternion/VALIDATION.md`.

## Next validation upgrade

Replace synthetic comparisons with versioned datasets and machine-readable parameter sweeps, and continue the cross-check chain:

- quaternion orientation plus applied torque-field response;
- timestep sweeps for rigid-body and three-body controls;
- finite-reach candidates tested against the same three-body initial conditions as the control solver;
- real galaxy rotation, redshift, lensing, and stellar-spectrum datasets;
- 3D divergence/curl and surface-volume integral checks after the 2D controls are stable.
