# Dynamos, Magnetospheres, and Technology

## Dynamo baseline
A conducting moving fluid can maintain or modify magnetic fields. A standard induction equation is:

\[\partial_t\mathbf B=\nabla\times(\mathbf v\times\mathbf B)+\eta\nabla^2\mathbf B.\]

A One-Wave treatment must reproduce equivalent field transport, amplification, diffusion, and polarity behavior from its lattice or phase dynamics.

## Magnetosphere baseline
A planetary magnetic field interacts with charged plasma and stellar wind. Useful first models include dipole geometry, pressure-balance standoff distance, charged-particle guiding, and reconnection-oriented boundary conditions.

## Bench technology
Build conventional calibrated hardware first. The apparatus remains valuable whether or not an exotic coupling exists.

- Helmholtz coils for near-uniform known fields.
- Hall sensors or fluxgate sensors for field telemetry.
- Rotating magnet or current loop with optical phase encoder.
- Current, voltage, and power logging for coils and loads.
- Torsion balance or load cell for torque or force measurements.
- Thermistors and accelerometers for thermal and vibration controls.
- Dummy loads, polarity reversals, phase reversals, and blind data labels.

## Required power accounting
For every run record source input, field storage, mechanical output, electrical output, heat, and radiation estimate:

\[E_{\rm source}=E_{\rm stored}+E_{\rm mechanical}+E_{\rm electrical}+E_{\rm thermal}+E_{\rm radiated}+E_{\rm residual}.\]

A persistent unexplained residual is not evidence by itself; it is an instruction to improve calibration and controls.
