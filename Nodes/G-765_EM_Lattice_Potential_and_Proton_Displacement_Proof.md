---
node_id: "G-765"
canonical_name: "EM Lattice Potential and Proton-Displacement Proof"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Exploratory Proof Packet / EM-Lattice Coupling / Proton Calibration"
claim_gate_detail: "YELLOW — equations, controls, metadata targets, and failure gates defined; no proton-like solution or physical coupling coefficient established"
metadata_standard: "I-06"
---

# G-765 — EM Lattice Potential and Proton-Displacement Proof

## Meaning of proof in this packet

A **One-Wave Proof** is an exploratory, versioned building block of truth. It
must state its equations, assumptions, measurements, controls, uncertainty,
and failure conditions. It is not a theorem or verified physical law merely
because it is called a proof.

This packet defines the smallest lawful bridge from the current coupled
lattice to an electromagnetic displacement experiment and, only after that
bridge passes its controls, to a proton-like localized-mode search.

## Dependencies

- `Nodes/C-311_Electric_Magnetic_Duality.md`
- `Nodes/C-319_Magnetic_Lattice_Reorganization.md`
- `Nodes/C-320_Magnetic_Compression_Path_Coupling.md`
- `Nodes/G-764_Combined_State_Lattice_Simulator_Foundation.md`
- `Nodes/G-766_Discrete_Lattice_Dispersion_and_Octave_Emergence_Proof.md`
- `chapters/01_Continuous_Lattice.md`
- `chapters/05_Simulation_Engine.md`
- `sims/00_CANONICAL_INGEST_RULE.md`
- `sims/00-lattice-primitive/metadata-anchors.json`

## 1. State and declared layers

At numerical site `i`, extend the G-764 state without replacing it:

\[
X_i=(q_i,\dot q_i,\phi_i,\mathbf x_i,h_i,
\Phi_i,\mathbf E_i,\mathbf B_i,\mathbf R_i,\mathbf K_{L,i}).
\]

- `q_i`, `qdot_i`, `phi_i`, `x_i`, and `h_i` retain their G-764 meanings.
- `Phi_i` is a declared scalar electrical potential.
- `E_i` and `B_i` are electromagnetic fields.
- `R_i` is the C-319 magnetic reorganization state.
- `K_L,i` is the C-319 directional path-accessibility tensor.

These layers remain distinct. Potential is not displacement; magnetic
reorganization is not scalar compression; a combined-state projection is not
a particle identity.

## 2. Standard electromagnetic control

The control simulation uses Maxwell's relations:

\[
\mathbf E=-\nabla\Phi-\partial_t\mathbf A,
\qquad
\mathbf B=\nabla\times\mathbf A,
\]

with Gauss, Faraday, and Ampere-Maxwell residuals reported explicitly.

The ordinary electromagnetic force-density control is

\[
\mathbf f_{\rm EM}=\rho_e\mathbf E+\mathbf J\times\mathbf B.
\]

Any One-Wave extension must be compared against this control rather than
silently absorbing its behavior into new coefficients.

## 3. Candidate lattice coupling

The G-764 lattice equation becomes the control plus a separately switchable
EM drive:

\[
\ddot q_i+2\zeta\omega_0\dot q_i+\omega_0^2q_i+\lambda q_i^3
=c_L^2(\Delta_h q)_i+d_i(t)+g_E D_i(\mathbf E)+g_B D_i(\mathbf B,\mathbf K_L).
\]

`D_i` is a declared projection from vector/tensor fields into the simulated
degree of freedom. Every run must publish that projection. Renderer direction
or an undeclared dot product may not supply it.

Magnetic reorganization follows C-319:

\[
\tau_R\partial_t\mathbf R
=-\mathbf R+\lambda_B
\left(\mathbf B\otimes\mathbf B-\frac{|\mathbf B|^2}{3}\mathbf I\right),
\qquad
\mathbf K_L=\mathbf I+\kappa_R\mathbf R.
\]

The resulting loop under test is:

```text
potential -> potential slope / electric field -> lattice displacement
-> magnetic rotation -> path reorganization -> next lattice/EM state
```

Reorganization changes directional accessibility. It does not, by itself,
create energy, charge, scalar compression, gravity, or a proton.

## 4. Measured and derived energy ledger

Keep source measurements immutable and report a separate numerical ledger:

\[
E_{\rm num}=E_{\rm kinetic}+E_{\rm lattice}+E_{\rm EM}
+E_{\rm coupling}+E_{\rm boundary}.
\]

At minimum,

\[
E_{\rm EM}=\int
\left(\frac{\epsilon_0}{2}|\mathbf E|^2
+\frac{1}{2\mu_0}|\mathbf B|^2\right)dV.
\]

The simulator must report work entering through drives and boundaries. A
localized mode fails if its apparent stability comes from unreported energy
injection, numerical damping, clipping, or boundary reflection.

## 5. Real-metadata calibration contract

Calibration uses independent measurements as constraints, never as hidden
definitions of lattice spacing or coupling constants.

### Dynamics and ingest controls

- GWOSC strain constrains cadence, signed waveform ingest, propagation,
  coherence, and provenance tests.
- CERN detector measurements constrain collision/excitation geometry and
  deposited-signal comparisons before reconstructed object labels.
- Antimatter trap and spectroscopy measurements provide mirrored frequency,
  field, timing, and uncertainty comparisons when machine-readable values are
  available.

### Proton-like target observables

A candidate localized mode is compared against independently sourced values
for total electric charge, rest energy, charge radius and form factors,
magnetic moment, stability, and response to applied electromagnetic fields.

Every source record must retain provider, record or table identifier, version,
units, uncertainty, retrieval date, and checksum or DOI when available.

Fit parameters against several observables simultaneously:

\[
\theta^*=\arg\min_\theta
\sum_k
\frac{\left(O_k^{\rm sim}(\theta)-O_k^{\rm measured}\right)^2}
{\sigma_k^2}.
\]

A different retuning for every observable is not one explanatory mode.

## 6. Proton-displacement search boundary

The first search target is a **proton-like candidate localized mode**, not a
declared proton and not a hard-coded knot.

For displacement field `u`, report

\[
\chi=-\nabla\cdot\mathbf u
\]

for compression/expansion and

\[
\boldsymbol\omega=\nabla\times\mathbf u
\]

for circulation/rotation. Report the full radial and angular displacement,
field, current, energy, and uncertainty profiles—not only one fitted number.

The search is not permitted until the linear EM-coupled lattice passes its
control and convergence gates.

## 7. Required run order

1. zero-state and zero-field hold;
2. Maxwell-only control and residual checks;
3. linear lattice with EM forcing and `R=0`;
4. G-766 analytic/numerical dispersion and octave controls;
5. magnetic reorganization ON/OFF comparison;
6. timestep, spacing, orientation, and boundary refinement;
7. retained-history ablation;
8. localized-mode search without proton labels;
9. multi-observable proton comparison using fixed parameters;
10. held-out measurement comparison.

## 8. Pass, hold, and failure gates

**Advance** only if one fixed model preserves charge and declared energy
accounting, converges under refinement, separates ordinary EM behavior from
the proposed reorganization residual, produces a localized mode that survives
perturbation and boundary controls, and improves several independent proton
observables without per-observable retuning.

**Hold** if the mode is stable numerically but metadata, uncertainty, or
projection error is incomplete.

**Fail or revise** if the result disappears under refinement, is explained by
the Maxwell/control model, depends on renderer orientation, requires hidden
energy, or matches only one selected observable.

## Current status

This packet synchronizes the equations, metadata contract, and simulator
order. It does not establish a physical lattice spacing, a new EM law, or a
proton solution. Those remain outcomes to be tested.
