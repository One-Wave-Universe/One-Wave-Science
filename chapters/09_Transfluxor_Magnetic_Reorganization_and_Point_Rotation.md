# Chapter 09 — Transfluxors, Magnetic Reorganization and Point Rotation

**Status:** RESEARCH CHAPTER / UNVERIFIED CROSS-SCALE HYPOTHESES  
**Scope:** established electromagnetism, magnetic materials, multiscale solvers, and falsifiable One-Wave extensions.  
**Implementation authority:** [Builds magnetic triangulation](https://github.com/One-Wave-Universe/Builds/blob/main/validation/TRANSFLUXOR_MULTISCALE_TRIANGULATION.md). No duplicate implementation or competing calibration canon here.

## 1. The central question

Can the magnetic state of a multi-aperture core reorganize its flux paths and magnetization texture in a measurable, history-dependent way? **Yes, established magnetics predicts such behavior.** Does the same observation require an additional One-Wave substrate/path-accessibility law, and does it change *point rotation* independently of ordinary torque and magnetic damping? **Not established.** This chapter defines the tests that can distinguish those claims.

Keep distinct: (a) circuit and magnetic flux-network topology, (b) magnetic domains and their material microstructure, (c) the ordinary atomic crystal lattice, and (d) the hypothesized One-Wave underlying lattice. Observing (a) or (b) is not direct evidence for (d).

## 2. Historical and modern prior art

- J. A. Rajchman and A. W. Lo, “The Transfluxor,” 1956 Western Joint Computer Conference, primary proceedings: https://www.bitsavers.org/pdf/afips/1956-02_%2309.pdf . Multiple apertures, magnetic paths, blocked/set/read states, winding placement and retained control.
- Classical Maxwell/Faraday/Ampère magnetostatics and quasistatics provide the independent baseline, not a One-Wave fit.
- Preisach and Jiles–Atherton hysteresis models offer different macroscopic constitutive approximations; compare each with independently measured major and minor B–H loops.
- Landau–Lifshitz–Gilbert (LLG) micromagnetics models local magnetization direction, exchange, anisotropy, demagnetization and damping; it is not equivalent to a macroscopic motor shaft rotating.
- Independent circuit (ngspice), nonlinear magnetic-circuit, finite-element vector-field, and micromagnetic solvers form a **triangulation**, not a vote among models.

Reference methods and source bibliography with model limits: Builds `validation/TRANSFLUXOR_MULTISCALE_TRIANGULATION.md`.

## 3. Established physics: equations that must be recovered

Magnetic induction and flux:
\[
\nabla\cdot\mathbf B=0,\quad
\nabla\times\mathbf H=\mathbf J_{\mathrm{free}}\quad(\mathrm{magnetoquasistatic}),\quad
\mathbf B=\mu_0(\mathbf H+\mathbf M),\quad
\Phi=\int_A\mathbf B\cdot d\mathbf A.
\]
Winding/circuit:
\[
v=Ri+\frac{d\lambda}{dt},\quad
\lambda=\sum_k N_k\Phi_k,\quad
\oint\mathbf H\cdot d\mathbf l=\sum_j N_j i_j.
\]
Signs and winding dots must be declared; the simplified winding law assumes a compatible passive voltage convention. General induced EMF is \(\mathcal E=-d\lambda/dt\). Magnetic graph nodes conserve flux; coupled branches share leg reluctance. Under a linear unsaturated approximation \(L\approx\mu N^2 A/\ell\); hysteretic multi-aperture paths generally require a nonlinear state-dependent model.

Micromagnetic local direction \(\mathbf m=\mathbf M/M_s\) evolves approximately by
\[
\partial_t\mathbf m=-\gamma\mathbf m\times\mathbf B_{\rm eff}
+\alpha\mathbf m\times\partial_t\mathbf m.
\]
The effective field comes from a declared free-energy functional and boundary conditions. This equation concerns magnetic-moment precession/damping. **Rigid-body point rotation** instead requires a measured mechanical torque and inertia:
\[
\dot{\mathbf L}=\boldsymbol\tau,\qquad \mathbf L=\mathbf I\boldsymbol\omega
\]
in a declared frame, with full Euler rigid-body terms when \(\mathbf I\) is body-fixed. The magnetic torque may be computed from a valid energy derivative or Maxwell stress tensor. Do not transfer microscopic \(\gamma\) into a mechanical point-rotation rate.

## 4. Canonical One-Wave hypothesis and explicit dimensional repair

C-319 proposes a symmetric traceless reorganization tensor \(\mathbf R\) and a path-accessibility tensor \(\mathbf K_L=\mathbf I+\kappa_R\mathbf R\). Its candidate driving tensor is
\[
\mathbf W_B=\mathbf B\otimes\mathbf B-\tfrac13|\mathbf B|^2\mathbf I,
\]
with \(\tau_R\partial_t\mathbf R=-\mathbf R+\lambda_B\mathbf W_B+\lambda_\omega\mathbf W_\omega\). Because \(\mathbf W_B\) has units of tesla squared, \(\lambda_B\) must have units of inverse tesla squared if \(\mathbf R\) is dimensionless. Likewise \(\lambda_\omega\) must compensate for the declared units of \(\mathbf W_\omega\). \(\kappa_R\) is dimensionless in this convention.

This is a **proposed phenomenological law**, not a derivation of Maxwell's equations or evidence of a new material medium. Its \(\mathbf B\mapsto-\mathbf B\) symmetry cannot predict an odd-in-field response without an additional explicitly measured signed variable. Require \(\mathbf K_L\) positive definite, unmagnetized recovery \(\mathbf R\to0\), and no hidden fit of \(\lambda_B\), \(\lambda_\omega\), or \(\kappa_R\) to holdout outcomes.

C-320 proposes \(\mathbf g_{\rm OW}=-\alpha_g\mathbf K_L\nabla\chi\), with \(\chi=-\nabla\cdot\mathbf u\). This is a separate unverified coupling. The transfluxor bench does not measure gravity; it can calibrate conventional magnetic variables and test whether an extra state is needed. A fit to magnetic remanence does not establish \(\mathbf g_{\rm OW}\).

G-749 is the authority for Point rotation; G-769 for Path rotation. Do not confuse \(\mathbf m\), a magnetic moment, \(\mathbf L\), rigid-body angular momentum, and a path's turning angle.

## 5. Reality-first solver triangulation

**Analytic control:** toroid \(L\), RL time constant, Kirchhoff laws, Faraday EMF, flux continuity, energy conservation.  
**Magnetic-circuit model:** independent shared-leg graph with aperture and dot-polarity bookkeeping, nonlinear reluctance and retained state.  
**FEM:** vector-potential \(\mathbf A\), \(\mathbf B=\nabla\times\mathbf A\), real aperture geometry, air leakage, mesh refinement and magnetic stress/force when relevant.  
**LLG/micromagnetics:** only where spatial resolution and calibrated exchange/anisotropy/material parameters justify it.  
**Measured bench:** winding drive/sense, current, flux integration, major/minor B–H, Hc, Br, Bsat, crosstalk, spatial Bx/By/Bz, losses, temperature and probe uncertainty.

A single idealized breadboard transfluxor threshold card and a 3D geometry-derived threshold are *competing approximations*. Do not adjust one to agree with the other. Compare both against measured cores. Independent solver agreement is weaker evidence than independent physical data when the solvers share constitutive assumptions.

## 6. Experiments and discriminating predictions

1. **Single-aperture baseline:** verify analytical inductance, transient RL response, probe polarity and energy ledger.
2. **Multi-aperture block/set/read:** independently specify geometry and pulse history; measure retained readout and shared-leg flux redistribution.
3. **Symmetry:** reverse winding sense, mirror geometry and reverse applied field; distinguish even \(\mathbf B\otimes\mathbf B\) response from sign-sensitive hysteresis.
4. **Domain versus path:** compare measured local field maps and remanence with both FEM and magnetic-circuit models; distinguish spatial magnetic field from inferred graph flux.
5. **Mechanical point rotation:** if there is a rotor, measure angle, torque and energy separately; do not call domain-wall motion rotor rotation.
6. **One-Wave differential prediction:** predeclare a quantitative residual (observable, sign, scale, material, uncertainty) not explained by calibrated Maxwell + material physics; fit only on calibration trials, then test blind on withheld sequences. If no distinguishable prediction is offered, mark the new mechanism **INCONCLUSIVE / NOT DISCRIMINATED**, not verified.
7. **Negative controls:** demagnetized core, nonhysteretic material, altered winding polarity, thermal and probe offsets, matched magnetic loading and null fields.

## 7. Numerical truth and mathematical methods

Use dimensionless scaling, exact graph incidence/cycle matrices, implicit time stepping, Newton continuation, analytic Jacobians or checked automatic differentiation, sensitivity singular values, parameter identifiability, mesh/timestep convergence, and energy closure. Each method needs a reproducible fixture and failure receipt. A pretty field rendering or an unconverged solver is not evidence.

## 8. Interpretation and scientific boundary

If Maxwell, measured material hysteresis and ordinary torque fully predict the observations, record that as success for the instrument and no independent support for additional One-Wave coupling. If repeatable, preregistered residuals remain after calibration and controls, formulate a narrower model and seek replication. Do not infer the origin of gravity or spacetime from transfluxor flux switching.

**Reference chain:** C-311 → C-319 → C-320; D-401 flux; C-306/C-307 mechanical torque/angular momentum; G-749 point rotation; G-769 path rotation; C-325 test protocol; Chapters 01/05/07 for lattice and solver context. Existing Chapter 07's simulated Maxwell-like PASS claims do not substitute for experimental Maxwell validation.

**Reality is validation through consequence.**
