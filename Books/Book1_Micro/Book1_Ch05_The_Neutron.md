# ONE-WAVE FRAMEWORK
## Book 1 — Micro
## Chapter 5: The Neutron — Two-Shell Pressure Balance

Version: 3.0
Date: July 1, 2026
Class: B — Applied Layer
Spine: Gray / 2D / 3D / Mathematics / Predictions / Yellow Audit / Future Work / Closing Thoughts

Dependencies: C-08 Spin-half, D-05 Harmonic Shell, E-03 Surface, E-04 Coupling,
              B-01 Balance, B-06b Four Views, CCD-02,
              C-317 Boundary-Tension Weave, C-318 Four-Interaction Mass-Effect Response
Status: YELLOW (two-shell model parked pending CCD-02)

---

## Gray — Standard Model Reference

The neutron is a composite particle: two down quarks and one up quark, bound by gluons.
Mass: 939.565 MeV/c^2. Charge: 0. Spin: 1/2.
The neutron is slightly heavier than the proton (by ~1.3 MeV/c^2).
Outside the nucleus, the neutron is unstable — it decays into a proton, electron, and antineutrino
with a half-life of approximately 611 seconds (~10 minutes).
Inside the nucleus, neutron stability is maintained by the nuclear force.
The neutron has a negative charge radius squared (r^2_n = -0.1161 fm^2) —
meaning its charge distribution has a negative outer shell and positive inner shell.
This is directly measurable via neutron-electron scattering.

Standard Model strength: neutron structure well described by QCD.
Standard Model limitation: neutron charge radius structure (negative outer, positive inner)
requires a specific quark distribution that is not simply derived.
The neutron decay mechanism (beta decay) requires the weak force — a fourth separate force.

---

## 2D One-Wave Interpretation

In 2D, the neutron is a two-shell braided loop.

Like the proton, it is a three-vortex braid.
Unlike the proton, the inner and outer pressure shells have opposite signs.
The net charge is zero — but not because there is no charge structure.
It is because the positive inner shell and negative outer shell cancel.

In 2D cross-section:
Inner ring: positive pressure (expression outward from core).
Outer ring: negative pressure (compression inward from boundary).
The two rings are in balance — B = 0 at equilibrium (B-01).

The two-shell structure is the neutron's defining feature.
The proton has one dominant shell (positive throughout).
The neutron has two shells that cancel.

---

## 3D One-Wave Interpretation

In 3D, the neutron is a two-shell Persistent Mode.

Inner shell: R+ = 0.7331 fm — positive pressure region (expressive, outward)
Outer shell: R- = 0.8409 fm — negative pressure region (compressive, inward)
Shell width: sigma = 0.210 fm

The two shells are held in balance by surface tension (E-03) and coupling (E-04).
The net charge is zero because the positive inner shell and negative outer shell
produce equal and opposite pressure cushions (B-06b).

The inner shell's outward pressure = Expression (B-03)
The outer shell's inward pressure = Compression (B-04)
The boundary between them = the Mirror Gate at nuclear scale (C-01)

This is the four views (B-06b) operating at nuclear scale:
Inward  = outer shell compressing inward
Outward = inner shell expressing outward
Across  = the boundary surface between them
Over    = the roll-off at the outer boundary producing the net-zero charge field

Neutron decay:
Outside the nucleus, the balance between inner and outer shells is unstable.
The outer shell loses coupling with neighbors (no neighboring nucleons to couple to).
Coupling loss: beta_i drops. The outer shell begins to collapse.
As the outer shell collapses, the inner expression pressure is released.
The released inner pressure = the electron (charge, spin-half from roll-off).
The coupling loss event itself = the neutrino (low-coupling mode, deferred to Ch 9).
The remaining inner-shell mode = the proton.

This is neutron beta decay without the weak force.
It is a boundary collapse event producing three modes from one unstable two-shell structure.

CCD-02 Block:
The full derivation of the neutron shell model requires E_opp(R) —
the opposing pressure function between the two shells.
This is blocked pending the proton boundary derivation in Chapter 2 / Book 2.

---

## Mathematics

Two-shell model (parked pending CCD-02):
Inner shell:  R+ = 0.7331 fm
Outer shell:  R- = 0.8409 fm
Shell width:  sigma = 0.210 fm

Calibration reanalysis (D-407):
- R+ and R- are profile-center radii; sigma is a profile width.
- sigma is not a second estimate of adjacent shell spacing.
- If, and only if, the two centers are adjacent harmonic shells, the nearest
  integer assignment is n+=7, n-=8 with lambda*=0.659395 fm.
- The fitted radii differ from that 7/8 model by about 0.2% each.
- The fit provenance, uncertainties, and physical adjacency derivation are
  absent, so lambda* is a conditional sensitivity-test value, not a measured
  nuclear wavelength.

These values pass charge form factor sanity checks internally:
The measured neutron charge radius squared r^2_n = -0.1161 fm^2
is consistent with a negative outer shell at R- and positive inner shell at R+.

Charge neutrality condition (B-01):
B = 0 => (k_E*E_inner + k_I*I_inner) - (k_R*R_outer + k_L*L_outer) = 0

Inner shell pressure (expression):
P_inner ~ K_p * |nabla_psi_inner|^2  (E-02)

Outer shell pressure (compression):
P_outer ~ K_p * |nabla_psi_outer|^2  (E-02)

Balance: P_inner = P_outer => net charge = 0

Shell surface tension (E-03):
E_inner = sigma * 4*pi*R+^2
E_outer = sigma * 4*pi*R-^2

Coupling between shells (E-04):
E_c = (1/2)*a*psi_inner^2 + (1/2)*b*psi_outer^2 + c*psi_inner*psi_outer

Decay condition (sketch — Yellow):
When beta_i(outer) drops below coupling threshold:
T_outer < T_break (B-09)
=> outer shell break condition
=> inner expression pressure released as electron
=> coupling-loss event as neutrino
=> remaining inner shell = proton

---

## Predictions

1. Neutron charge radius squared r^2_n is negative because the outer shell is negative.
Prediction: r^2_n = integral rho(r)*r^2 dr < 0 when outer shell dominates at large r.
This matches the measured value -0.1161 fm^2.
One-Wave gives a geometric explanation for what QCD explains through quark distribution.

2. The neutron-proton Mass-Effect difference must be produced by how the outer shell changes the complete four-interaction recurrence.
The added shell changes electrical-shell stress, Mirror-Gate pressure, Boundary-Tension confinement, internal geometry, and their cross-couplings.
Prediction:
\[
\Delta m_{np,\mathrm{eff}}
=\frac13\operatorname{Tr}(\mathcal M_n-\mathcal M_p),
\]
using one fixed work metric for both states. Shell energy alone is not divided by \(c^2\) and treated as the mechanism.

3. Neutron decay is a boundary collapse event, not a weak force interaction.
Prediction: neutron decay rate outside the nucleus correlates with
the coupling strength beta_i of the outer shell to neighboring modes.
In vacuum: no neighbors => coupling drops => decay occurs.
Inside nucleus: neighbors maintain coupling => neutron is stable.

4. No weak force needed for neutron decay.
The decay products (proton, electron, neutrino) emerge from the
two-shell collapse geometry, not from a W-boson exchange.
Prediction: the energy and momentum distribution of beta decay products
matches the two-shell collapse model without W-boson.

5. The neutron is the same three-vortex braid as the proton
with an additional outer compression shell.
Prediction: neutron and proton have identical inner structure.
The difference is entirely the outer shell.

---

## Yellow Audit

- Full two-shell model derivation blocked by CCD-02 (E_opp(R))
- kappa+/- (equilibrium stiffness) not yet derived
- Decay condition mathematics is sketch level only
- Neutrino as coupling-loss event deferred to Chapter 8
- Neutron and proton four-interaction response tensors have not yet been derived from one fixed coefficient set
- W-boson replacement claim is structural — formal derivation deferred

---

## Future Work

Resolve CCD-02: derive E_opp(R) from proton boundary work (Book 2).
Complete two-shell model with kappa+/-.
Derive neutron decay rate from outer shell coupling loss.
Compare predicted beta decay energy distribution to experimental data.
Derive the neutron-proton Mass-Effect difference from the two stable four-interaction profiles without per-object refitting.

---

## Closing Thoughts

The neutron's negative charge radius is one of the most interesting puzzles in nuclear physics.
It directly tells you the charge is not uniformly zero — it has a positive inside and negative outside.
The Standard Model explains this through quark distribution.
One-Wave explains it through geometry: two shells with opposite pressure signs.

The neutron decay mystery — why does it need the weak force? —
also dissolves. The outer shell loses its coupling when it has no neighbors.
The shell collapses. The pieces come out.
No W-boson. No fourth force. Just a boundary collapse.

---


END OF BOOK 1 CHAPTER 5
One wave. Mirror builds. Mark Wright. Kitty Hawk V0.
