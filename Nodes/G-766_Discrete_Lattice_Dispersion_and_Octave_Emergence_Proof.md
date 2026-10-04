---
node_id: "G-766"
canonical_name: "Discrete Lattice Dispersion and Octave-Emergence Proof"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Exploratory Proof Packet / Lattice Dispersion / Scale Testing"
claim_gate_detail: "YELLOW — the discrete control dispersion and octave tests are defined; no physical lattice spacing, preferred octave law, or measured fit is established"
metadata_standard: "I-06"
---

# G-766 — Discrete Lattice Dispersion and Octave-Emergence Proof

## Meaning and boundary

This One-Wave Proof extends the exact scalar benchmark in G-746 to the
declared six-neighbor numerical lattice in G-764. It asks whether octave-like
frequency relations emerge from the lattice dynamics. It does not impose an
octave ladder as an input and does not convert the numerical spacing into a
physical length.

## Dependencies

- `Nodes/G-746_Damping_Matrix_Dispersion.md`
- `Nodes/G-745_Zone_Edge_125GeV_Lattice_Constant_Hypothesis.md`
- `Nodes/G-764_Combined_State_Lattice_Simulator_Foundation.md`
- `chapters/01_Continuous_Lattice.md`
- `chapters/05_Simulation_Engine.md`
- `sims/00_CANONICAL_INGEST_RULE.md`
- `sims/00-lattice-primitive/metadata-anchors.json`

## 1. Linear control equation

Begin with the G-764 lattice with the nonlinear, history, and EM extension
terms disabled:

\[
\ddot q_i+2\zeta\omega_0\dot q_i+\omega_0^2q_i
=c_L^2(\Delta_hq)_i+d_i(t).
\]

For an undriven plane-wave trial

\[
q_i(t)=A\exp\!\left[i(\mathbf k\cdot\mathbf x_i-\omega t)\right],
\]

the six-neighbor triangular-lattice Laplacian has symbol

\[
\Lambda_\triangle(\mathbf k)=
\frac{2}{a_{\rm num}^2}
\left[
\cos(\mathbf k\!\cdot\!\mathbf a_1)+
\cos(\mathbf k\!\cdot\!\mathbf a_2)+
\cos(\mathbf k\!\cdot\!(\mathbf a_2-\mathbf a_1))-3
\right].
\]

With \(a_{\rm num}=1\) unless explicitly swept, define

\[
\Omega_\triangle^2(\mathbf k)=
\omega_0^2-c_L^2\Lambda_\triangle(\mathbf k).
\]

The temporal roots are therefore

\[
\omega_\pm(\mathbf k)=
-i\zeta\omega_0
\pm\sqrt{\Omega_\triangle^2(\mathbf k)-\zeta^2\omega_0^2}.
\]

This must reproduce the G-746 scalar form in the long-wavelength limit,
with the effective continuum speed derived from the declared stencil rather
than silently equated to \(c\).

## 2. Dispersion measurements

For every sampled direction and wavevector, report:

- \(\operatorname{Re}\omega\) and \(\operatorname{Im}\omega\);
- phase velocity \(v_p=\operatorname{Re}\omega/|\mathbf k|\);
- group velocity \(\mathbf v_g=\nabla_{\mathbf k}\operatorname{Re}\omega\);
- attenuation time and, where meaningful, attenuation length;
- directional anisotropy across the symmetry-inequivalent paths;
- analytic-versus-measured frequency residual;
- timestep, domain, boundary, and numerical-spacing convergence.

Overdamping in the temporal problem must not be relabeled as spatial
evanescence. Zone-edge flattening must not be relabeled as mass.

## 3. Octave-emergence test

Let \(f_m\) be independently detected spectral peaks from a fixed run. For
each ordered pair define the nearest-octave residual

\[
r_{mn}=\log_2\!\left(\frac{f_m}{f_n}\right)
-\operatorname{round}\!\left[
\log_2\!\left(\frac{f_m}{f_n}\right)
\right].
\]

An octave-compatible pair has \(|r_{mn}|\leq\epsilon_{\rm oct}\), where
\(\epsilon_{\rm oct}\) is fixed before examining the hypothesis run.

The simulator must compare the observed count and residual distribution with:

1. the linear Gray lattice;
2. phase-randomized data preserving the power spectrum;
3. frequency-shuffled peaks preserving peak count and band limits;
4. reflected and rotated lattice orientations;
5. synthetic non-octave and exact-octave fixtures.

Octave structure advances only if it exceeds these controls and remains under
resolution, duration, window, threshold, and boundary sweeps. Merely drawing
the predefined sequence \(f_n=2^nf_0\) is not evidence of emergence.

## 4. Scale-transform separation

Keep these transforms separate in code and receipts:

\[
f_n=2^nf_0,
\qquad A_n=2^nA_0,
\qquad r_n=2^nr_0.
\]

A frequency ratio does not establish amplitude doubling, geometric doubling,
or a next-scale physical object. A combined state may become a next-scale
point only after G-764 projection error is reported.

## 5. Real-metadata comparison

Real measurements constrain the experiment without defining its answer:

- GWOSC supplies immutable signed time series, sample cadence, detector
  identity, and uncertainty/provenance controls.
- CERN supplies immutable collision/excitation measurements and detector
  geometry before reconstructed particle labels.
- spectroscopy and antimatter measurements may supply independently sourced
  frequency ratios with their units and uncertainties.

Every transformed series must remain linked to its raw source by provider,
record/version, units, uncertainty, retrieval date, and checksum or DOI.
Sampling rate \(1/\Delta t\) must never be stored as the measured physical
signal frequency.

For a shared parameter vector \(\theta\), compare several datasets at once:

\[
\chi^2(\theta)=
\sum_d\sum_j
\frac{\left[y_{dj}^{\rm sim}(\theta)-y_{dj}^{\rm data}\right]^2}
{\sigma_{dj}^2+\sigma_{dj,\rm model}^2}.
\]

Training and held-out windows or events must be declared before fitting. A
different retuning for every event, detector, or frequency band is not one
cross-scale explanation.

## 6. Required run order

1. zero-state hold;
2. exact single-mode synthetic fixture;
3. analytic dispersion versus measured numerical dispersion;
4. timestep, domain, boundary, orientation, and spacing refinement;
5. exact-octave and non-octave detector fixtures;
6. Gray-lattice and randomized octave controls;
7. immutable GWOSC ingest and held-out comparison;
8. only then enable G-765 EM forcing and magnetic reorganization;
9. only after the EM control passes, search for localized modes.

## 7. Pass, hold, and failure gates

**Advance** the discrete-dispersion layer if analytic and measured frequencies
agree within a predeclared tolerance, the long-wave limit matches the G-746
control, energy drift and anisotropy are reported, and convergence survives
refinement.

**Advance** an octave-emergence claim only if a predeclared statistic exceeds
all listed controls, survives analysis sweeps, and predicts held-out data with
one shared parameter set.

**Hold** if dispersion passes but metadata uncertainty, provenance, or
held-out coverage is incomplete.

**Fail or revise** if octave structure is inserted by the transform, follows
from sampling/window artifacts, disappears under refinement, or requires
event-by-event retuning.

## 7a. Anisotropic signed-axis correction

See `Nodes/G-768_Anisotropic_Signed_Axis_Spectrum_and_Rotating_Axis_Scale_Test.md`.

The explicit signed-axis operator (J_a=J_b=+J, J_c=-J) does not produce isotropic (2\times) dilation under a static axis assignment. Its M-type candidate is a stripe mode with phase pattern (\psi_{nm}=A(-1)^{n+m}). Therefore octave-like spectral evidence in this node must not be promoted to geometric doubling.

A rotating three-orientation signed-axis cycle is a viable isotropy candidate, but the scale factor remains unresolved until the composed coarse-graining map (\mathcal R_3\mathcal R_2\mathcal R_1) is calculated. Rotational averaging can establish isotropy of an effective rank-2 tensor; it does not by itself establish a factor of 2.

## Current status

The six-neighbor dispersion and octave-emergence tests are specified but have
not yet been run. G-745 remains quarantined: no physical lattice spacing is
derived here. No proton, quark, mass, or new electromagnetic law follows from
this packet alone.

## 8. G-767 observational handshake

G-766 and G-767 form a two-sided test and must not be collapsed.

- G-766: generate candidate spectral/dispersion structure from the declared numerical lattice without fitting measured peaks.
- G-767: measure scale-phase structure in real spectra without assuming the lattice.
- Handshake: compare a frozen lattice prediction with a held-out measured spectrum.

A match is meaningful only when the lattice-side mode and measurement-side statistic were specified independently enough to prevent the measured spectrum from being encoded into the simulator. Any surviving relation must report parameter count, uncertainty and competing null/control likelihood.

See `Nodes/G-767_Measured_Spectrum_Lattice_Phase_Map.md`.
