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

The next upgrade should replace synthetic comparisons with versioned datasets and machine-readable parameter sweeps.
