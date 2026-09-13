# Established Electromagnetic and Tidal Baselines

## Electromagnetism

### Observation
Currents, moving charges, magnetic materials, time-varying electric fields, and time-varying magnetic fields produce reproducible forces, torques, induction, radiation, and energy transfer.

### Standard model
Maxwell equations provide the baseline description:

\[\nabla \cdot \mathbf{E}=\rho/\epsilon_0, \qquad \nabla \cdot \mathbf{B}=0,\]
\[\nabla\times\mathbf{E}=-\partial_t\mathbf{B}, \qquad \nabla\times\mathbf{B}=\mu_0\mathbf{J}+\mu_0\epsilon_0\partial_t\mathbf{E}.\]

The force on a charge is:

\[\mathbf{F}=q(\mathbf{E}+\mathbf{v}\times\mathbf{B}).\]

For an ideal isolated charge, the magnetic component is perpendicular to velocity and does no instantaneous work:

\[\mathbf{F}_B\cdot\mathbf{v}=0.\]

Time-varying fields, induced currents, sources, resistive loads, mechanical motion, and radiation exchange energy through the full coupled system.

### Minimum benchmarks
- Dipole field geometry and torque: \(\boldsymbol{\tau}=\mathbf{m}\times\mathbf{B}\).
- Faraday induction: \(\mathcal{E}=-d\Phi_B/dt\).
- Motional EMF, back-EMF, motor and generator power balance.
- Charged-particle cyclotron motion and drift.
- Electromagnetic wave propagation and polarization.

## Tidal locking

### Observation
Extended deformable orbiting bodies exchange angular momentum between spin and orbit. Dissipation of periodic deformation produces heat and drives spin-orbit evolution. Synchronous rotation is common, but non-1:1 resonances exist.

### Standard model
A tide-raising body produces a differential gravitational field across an extended object. A finite response time or dissipative lag offsets the deformation from the line of centers and creates torque:

\[\tau_{\rm tide}\sim-\frac{3}{2}\frac{k_2}{Q}\frac{Gm^2R^5}{a^6}\operatorname{sgn}(\Omega-n).\]

Here \(k_2\) is deformability, \(Q\) is dissipation quality factor, \(m\) is perturber mass, \(R\) is responding-body radius, \(a\) is separation, \(\Omega\) is spin rate, and \(n\) is mean orbital rate.

### Required numerical checks
- Total angular momentum remains conserved to numerical tolerance.
- Mechanical energy decreases only by modeled dissipation.
- Torque reverses sign at synchronous rotation.
- Faster-than-orbit spin transfers angular momentum outward; slower-than-orbit spin transfers it inward.
- Resonant states such as 1:1 and 3:2 emerge only under stated conditions.
