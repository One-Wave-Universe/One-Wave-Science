# Appendix D — AI-Readable Canonical Node Pack

Generated from current canonical node files. YAML front matter controls gate and lifecycle.

---

## SOURCE: D-401_Flux.md

---
node_id: "D-401"
canonical_name: "Flux"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Geometry, Resonance, and Simulation"
claim_gate_detail: "YELLOW (partially derived — steady-state harmonic condition confirmed; exponential functional form remains a gap, not a sketch)"
metadata_standard: "I-06"
---

# Node D-401: Flux

Dependencies:
Upstream: A-112 Persistent Mode
Downstream: D-402 Resonant Mode

Definition:
A persistent mode creates a surrounding field.
Flux is the statement that this field threads space and couples to other modes.

Flux = field of a persistent mode threading space and coupling outward

Mathematics (partially derived — real progress from A-109's actual update rule):

Steady-state condition, derived: A-112 Persistent Mode's stability
criterion (‖ψ_{n+k} - ψ_n‖ < ε) means ψᵢⁿ⁺¹ ≈ ψᵢⁿ ≈ ψᵢⁿ⁻¹ at a
persistent mode. Substituting into A-109's real update rule
(ψᵢⁿ⁺¹ = ψᵢⁿ + (1-γ)(ψᵢⁿ-ψᵢⁿ⁻¹) + βᵢ(⟨ψⱼⁿ⟩-ψᵢⁿ)):

ψᵢ = ψᵢ + (1-γ)(ψᵢ-ψᵢ) + βᵢ(⟨ψⱼ⟩-ψᵢ)
0 = βᵢ(⟨ψⱼ⟩-ψᵢ)

For βᵢ ≠ 0, this requires ⟨ψⱼ⟩ = ψᵢ: a persistent mode satisfies a
discrete harmonic (mean-value) condition. This IS rigorously derived
from real upstream equations, not sketched.

GAP FOUND (new — the original sketch did not derive this and the gap
was not previously flagged): the harmonic condition above does NOT by
itself produce the exponential form Phi(x) ~ A*exp(-|x-x_0|/lambda)
originally sketched. A pure discrete harmonic condition satisfies a
maximum principle; away from a source, a bounded harmonic function on
an infinite lattice tends toward constant, not exponential decay.
Getting the sketched exponential profile requires an additional
"mass" or screening term — most plausibly the residual of the memory
term (1-γ)(ψᵢⁿ-ψᵢⁿ⁻¹) not being exactly zero, which was assumed away
above. This residual has not been derived or bounded. Until it is,
the exponential form remains an assumption, and the derivation above
only establishes the weaker harmonic condition, not the full sketch.

This is a sketch. The functional form of Phi and the coupling mechanism
are not derived here.

Operational Chain:
Persistent Mode => Flux => Coupling to other modes

Yellow Audit:
- Steady-state harmonic condition (⟨ψⱼ⟩ = ψᵢ) is now rigorously derived
  from A-109's real update rule and A-112's stability criterion — this
  is genuine progress, not sketch
- The exponential functional form Phi(x) ~ exp(-|x-x_0|/lambda) is NOT
  derived from the harmonic condition alone — a real gap, newly found,
  requiring a mass/screening term (candidate source: the residual
  memory term, not yet bounded)
- Coupling length lambda not specified even if the exponential form
  is eventually justified
- Whether flux is conservative, dissipative, or mixed not established
- No longer purely "bookkeeping item, does not block chapter" — the
  harmonic-vs-exponential gap is a real open mathematical question,
  though still not urgent

Future Work:
Bound the residual memory term (1-γ)(ψᵢⁿ-ψᵢⁿ⁻¹) near a persistent mode
to determine whether it can supply the missing mass/screening term.
Measure coupling length lambda via Wave Reader, once the functional
form question above is resolved (measuring lambda for an unjustified
functional form risks fitting noise to the wrong equation).
Determine whether flux form matches known field profiles.

---

## SOURCE: D-402_Resonant_Mode.md

---
node_id: "D-402"
canonical_name: "Resonant Mode"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Geometry, Resonance, and Simulation"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node D-402: Resonant Mode

Dependencies:
Upstream: A-111 Recursion, A-112 Persistent Mode, D-401 Flux
Downstream: D-403 Spherical Modes, D-404 Nested Resonance, D-405 Harmonic Shell, B-221 Six Recursive Steps (BUILD's Pattern term)

Definition:
A Resonant Mode is a persistent mode whose recursive update produces a
stable periodic pattern — a mode that returns to itself after k steps.

psi_{n+k} = psi_n  for integer k

Mathematics:
Discrete periodic condition:
psi_{n+k} = psi_n  for integer k >= 1

The smallest such k is the period of the resonant mode.

k = 1: fixed point (stationary mode)
k = 2: period-2 oscillation
k = n: period-n resonance

From A-111 update rule:
psi_i^{n+1} = psi_i^n + (1-gamma)(psi_i^n - psi_i^{n-1}) + beta_i(<psi_j^n> - psi_i^n)

A Resonant Mode satisfies this update rule with periodic boundary condition:
psi_i^{n+k} = psi_i^n

Resonant Mode condition:
||psi_{n+k} - psi_n|| < epsilon  AND  the pattern is periodic

Operational Chain:
Persistent Mode => Resonant Mode => [Spherical Modes / Nested Resonance / Harmonic Shell]

Yellow Audit:
- Stability of resonant modes under perturbation not fully derived
- Whether all periodic modes are stable or only a subset unresolved
- Real persistence under loss, compensation mechanisms, feedback stabilization
  deferred to E-508 Real Persistence Under Loss

Canonical downstream address: E-508 Real Persistence Under Loss. The legacy D-02b address is retired and resolves through the alias registry.

---

## SOURCE: D-403_Spherical_Modes.md

---
node_id: "D-403"
canonical_name: "Spherical Modes"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "HELD"
classification: "Geometry, Resonance, and Simulation"
claim_gate_detail: "YELLOW (deferred)"
metadata_standard: "I-06"
---

# Node D-403: Spherical Modes

Dependencies:
Upstream: D-402 Resonant Mode
Downstream: Books — atomic structure, electron shells, particle identity

Definition:
A spherical mode is a 3D bounded resonant mode with angular structure.
In a spherically symmetric restoring field, modes may be classified by
angular quantum numbers.

Spherical Mode = resonant mode with 3D angular structure

Mathematics (deferred):
Spherical symmetry requires the mode to satisfy:
nabla^2 psi + k^2 psi = 0  (Helmholtz equation in 3D)

Solutions in spherical coordinates:
psi(r, theta, phi) = R(r) * Y_l^m(theta, phi)

where:
R(r) = radial function
Y_l^m = spherical harmonics
l = angular quantum number
m = magnetic quantum number

Angular quantum numbers and degeneracy structure not yet derived
from One-Wave geometry alone.

Operational Chain:
Resonant Mode => Spherical Modes => Atomic Structure (Books)

Yellow Audit:
- Full derivation of spherical mode structure from update rule deferred
- Angular quantum numbers not yet derived from One-Wave geometry
- Degeneracy structure deferred
- Connection to electron shell model deferred to Books

Future Work:
Derive radial and angular mode structure from 3D update rule.
Connect to Harmonic Shell condition (D-405).
Apply to atomic structure in Book 2.

---

## SOURCE: D-404_Nested_Resonance.md

---
node_id: "D-404"
canonical_name: "Nested Resonance"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Geometry, Resonance, and Simulation"
claim_gate_detail: "YELLOW (hypothesis)"
metadata_standard: "I-06"
---

# Node D-404: Nested Resonance

Dependencies:
Upstream: D-402 Resonant Mode
Downstream: Books — proton structure, quark hypothesis

Definition:
Nested Resonance is the existence of stable sub-modes within a primary resonant mode.
The primary mode hosts internal periodic sub-structures.

Nested Resonance = stable sub-modes existing within a primary resonant mode

Mathematics:
Harmonic generation — GREEN:
A nonlinear update rule can produce sub-modes at harmonic frequencies.

Let the primary mode oscillate at frequency f_0.
A nonlinear update rule produces harmonics at:
f_1 = 2*f_0, f_2 = 3*f_0, f_3 = n*f_0

This is mathematically proved for nonlinear recursion.

Stable nested mode — HYPOTHESIS:
Whether these harmonic sub-modes form stable, persistent sub-structures
within the primary mode is not proved.

Harmonic generation: GREEN
Stable nested mode: HYPOTHESIS

Physical content (vortex substructure, quark hypothesis) deferred to Books.

Operational Chain:
Resonant Mode => [Harmonic Generation => Nested Resonance (hypothesis)]

Yellow Audit:
- Stable nested mode not proved — hypothesis status is correct and honest
- Physical content (vortex substructure, quark sub-modes) deferred to Books
- Whether nested resonance requires specific nonlinearity conditions unresolved
- Interaction between sub-modes and primary mode not yet characterized

Future Work:
Simulate nonlinear update rule. Measure harmonic content.
Determine whether harmonic sub-modes form stable persistent patterns.
Connect to proton three-vortex braided model in Book 1 Chapter 2.

---

## SOURCE: D-405_Harmonic_Shell.md

---
node_id: "D-405"
canonical_name: "Harmonic Shell"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Geometry, Resonance, and Simulation"
claim_gate_detail: "YELLOW — GEOMETRY FORMALIZED; ENERGY INTERPRETATION OPEN"
metadata_standard: "I-06"
---

# Node D-405: Harmonic Shell

Dependencies:
Upstream: D-402 Resonant Mode, A-110 Oscillation
Downstream: Books — atomic shells, electron orbital model, proton charge radius;
            D-407 calibration reanalysis; CCD-01

Definition:
A Harmonic Shell is a bounded standing-wave geometry whose closed path contains
an integer number of wavelengths.

Shell condition:

2 pi R = n lambda,  n in Z+

where:
R = shell radius,
lambda = wavelength along the closed path,
n = integer winding/shell count.

Mathematics — variable-radius, fixed-wavelength family:

R_n = n lambda/(2 pi)
DeltaR = R_(n+1)-R_n = lambda/(2 pi).

This defines equally spaced shell-center radii if lambda is held fixed.

## Critical model distinction

There are two different quantization problems that must not be mixed:

1. Variable radius, fixed lambda:
   R_n = n lambda/(2 pi).
   Here n counts how many copies of the same wavelength fit around successively
   larger closed paths.

2. Fixed boundary radius, variable wavenumber:
   k_n = n/R.
   Here n changes the allowed wavenumber and can generate a dispersion-based
   frequency/energy ladder.

The original node used Model 1 geometry but borrowed Model 2 energy intuition.
For Model 1:

k_n = n/R_n = 2 pi/lambda,

so k_n is independent of n. Therefore E_n=hbar omega(k_n) alone gives no
nonzero adjacent-shell energy spacing.

A nonzero energy ladder requires an additional derived model, for example:

- E_n = n epsilon_lambda from an action/energy per wavelength;
- radial eigenvalues k_(r,n) from a boundary-value equation;
- curvature/pressure/surface/coupling energy depending on R_n;
- nonlinear collective-mode energy.

D-405 currently quantizes geometry. It does not yet quantize energy.

## Connection to D-407

D-407 removes a false calibration fork: neutron-profile width sigma is not
shell-center spacing. Under an unproved adjacent-shell assumption, the neutron
radii select a provisional n=7,8 assignment and lambda approximately 0.6594 fm.
This is a conditional sensitivity-test value, not a measured constant.

## CCD-01 relationship

The shell condition may contribute to a minimum-action derivation only after the
energy/action assigned to one closed wavelength is derived. Geometry alone does
not establish S_min=hbar.

Operational Chain:
Resonant Mode + closed-path wavelength condition => Harmonic Shell geometry
=> [energy model still required] => quantitative atomic/nuclear structure

Yellow Audit:
- closed-path geometry and uniform center spacing are explicit;
- variable-radius versus fixed-radius quantization is now separated;
- current geometry does not create an n-dependent k spectrum;
- lambda is not independently measured;
- D-407's 0.6594 fm candidate is conditional on an unproved 7/8 adjacency;
- action/energy per shell is not derived;
- radial stability hierarchy is not established;
- relationship to the neutron two-profile model remains conditional.

Future Work:
Derive the physical boundary-value problem that decides between fixed-R
wavenumber quantization, variable-R winding shells, or radial eigenmodes.
Derive shell energy from lattice pressure, curvature, coupling, or action.
Recover the neutron-profile fit and uncertainties before treating D-407 as a
calibration.
Apply only the derived model to atomic and carbon calculations.

---

## SOURCE: D-406_Isotope_Stability_Coupling_Density.md

---
node_id: "D-406"
canonical_name: "Isotope Stability via Outer-Shell Coupling Density"
namespace: "NODE"
gate: "GREEN"
lifecycle: "BLOCKED"
classification: "Extension Node"
claim_gate_detail: "GREEN (nuclear coupling hypothesis) / BLOCKED pending an inter-nucleon bridge"
metadata_standard: "I-06"
---

# Node D-406: Isotope Stability via Outer-Shell Coupling Density

Grounding note: Book 1 Ch5 already states the actual mechanism this
node needs — a free neutron's outer shell "loses its coupling when it
has no neighbors," which is offered there as the reason free neutrons
decay while bound neutrons don't. This node does nothing more than
take that stated mechanism seriously as a function of NEIGHBOR COUNT
and RATIO, since isotopes (same Z, different neutron count) are
precisely a question of how many neighbors each outer shell has.
Nothing here is new physics — it is making an implicit dependency
explicit and asking what it predicts.

Dependencies:
Upstream: Book 1 Ch5 The Neutron (two-shell model, R+/R-, sigma),
          A-108 Local Stability, A-112 Persistent Mode
Conditional geometry input: C-321 only after an inter-nucleon coupling bridge is derived
Downstream: none yet (proposed) — needed for carbon-12 vs carbon-14
            comparison specifically

Definition:
Ch5 establishes that a neutron's outer shell (R- = 0.8409 fm) requires
COUPLING to a neighboring structure to remain in the shell-balance
state; without a neighbor, the outer shell decouples and the two-shell
structure collapses (beta decay: proton + electron + neutrino).

This node proposes: coupling is not binary (present/absent) but has a
DENSITY, set by how many other nucleons are within coupling range and
how that coupling is distributed. For a fixed proton count Z, adding
neutrons changes this coupling density in two competing ways:

1. Each added neutron is itself a potential coupling partner for
   existing neutrons' outer shells — more neutrons, more mutual
   support, tending to stabilize.
2. Each added neutron changes the number and geometry of possible inter-nucleon couplings. C-321 cannot yet supply those couplings because it is only a reduced neck model derived from the intra-proton Boundary-Tension Weave. A separate bridge must establish whether intact proton/neutron knots form comparable necks at nuclear scale.

This gives a genuine hypothesis: there should be a coupling-density
OPTIMUM at some neutron-to-proton ratio for each Z, not a simple
monotonic "more neutrons = more stable" or "fewer = more stable." This
matches the real observed pattern (light stable nuclei cluster near
N≈Z; carbon-12 is Z=6,N=6; carbon-14 with Z=6,N=8 is beta-unstable) —
but this node does NOT derive that pattern from the mechanism, it only
identifies that the mechanism as stated in Ch5 is consistent with a
non-monotonic result and names the missing derivation.

Mathematics:

Coupling density (PROPOSED FORM, not derived from first principles —
built to have the right qualitative shape given Ch5's stated
mechanism, coefficients unknown):

CouplingDensity(i) = sum over neighbors j of [coupling_strength(i,j)] / ExpectedCoupling(shell type of i)

Decay condition (direct extension of Ch5's stated trigger):
IF CouplingDensity(i) < CouplingThreshold  THEN  outer shell of
nucleon i decouples => beta-decay-like event (matching Ch5's actual
described mechanism for the free-neutron case, generalized here to
the in-nucleus case)

Stability requirement for the WHOLE nucleus (composite of A-108's real
condition, applied per-nucleon rather than globally):
Nucleus is stable IFF, for all nucleons i: CouplingDensity(i) >= CouplingThreshold

Isotope comparison (what this node is actually FOR):
For fixed Z, as neutron count (A-Z) increases from N≈Z:
- Near N≈Z: neutrons and protons mutually support coupling density —
  CONSISTENT with observed stability clustering, not yet DERIVED from
  a specific coupling_strength(i,j) form
- Beyond some N/Z ratio: excess neutrons' outer shells are increasingly
  coupled only to OTHER neutrons (weaker/different coupling than to
  protons, per Ch5's shell-type distinction) — CouplingDensity per
  excess neutron falls, predicting eventual decay, CONSISTENT with
  carbon-14's real beta-instability, but again not yet DERIVED
  quantitatively

Operational Chain:
Ch5's single-neutron decoupling proposal => derive an inter-nucleon coupling law => define CouplingDensity(i) => require CouplingDensity(i) >= threshold for every nucleon => vary neutron count at fixed Z and test the resulting stability curve

Yellow Audit:
- coupling_strength(i,j) has no derived functional form — this is
  asserted to exist and to differ by shell type (proton-proton,
  proton-neutron, neutron-neutron), following Ch5's own shell-type
  distinction, but the actual VALUES are not derived
- CouplingThreshold is not derived — it is the same category of gap
  as Ch5's own undetermined kappa+/- (equilibrium stiffness)
- This node predicts a QUALITATIVE pattern (stability optimum near
  N≈Z, falling off with excess) that happens to match real nuclear
  physics, but "predicts the right shape" is not the same as "derives
  the right shape" — this must not be overclaimed
- C-321's N=3 junction geometry does not establish an inter-nucleon force. This node is blocked until that physical bridge is derived.
- Formation and stability requirements are taken directly from C-318 and Book 1 Ch14.

Future Work:
Derive coupling_strength(i,j) for the three shell-type cases
(proton-proton, proton-neutron, neutron-neutron) from Ch5's real
R+/R-/sigma values, rather than treating it as a free function.
Derive the missing inter-nucleon coupling bridge before importing any C-321 network geometry. Then test candidate nuclear geometries against C-318/A-112 stability requirements.
Once coupling_strength has a real form, compute CouplingDensity(i)
for carbon-12 (Z=6,N=6) and carbon-14 (Z=6,N=8) explicitly and check
whether the predicted stability difference matches the real, known
difference (carbon-12 stable, carbon-14 beta-decays with ~5730 year
half-life) — this is the actual validation target for this whole node.

---

## SOURCE: D-407_Harmonic_Shell_Calibration_Attempt.md

---
node_id: "D-407"
canonical_name: "Harmonic Shell / Two-Shell Neutron Calibration Reanalysis"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Active Calibration and Model-Definition Audit"
claim_gate_detail: "YELLOW — PARTIAL RESOLUTION"
metadata_standard: "I-06"
---

# Node D-407: Harmonic Shell / Two-Shell Neutron Calibration Reanalysis

Dependencies:
Upstream: D-405 Harmonic Shell, A-114 Dispersion Relation, Book 1 Ch5 The Neutron
Downstream: quantitative carbon-12/Hoyle-state work remains blocked, but the false two-candidate fork is removed

Purpose:
Re-examine whether the neutron two-shell parameters can calibrate D-405's
nuclear wavelength. The earlier version treated two quantities as competing
measurements of the same shell spacing:

- center separation: R_minus - R_plus;
- fitted shell width: sigma.

That comparison was not valid. A profile width and a center-to-center spacing
are different geometric quantities unless a separate equation explicitly
identifies them.

## Input provenance and role

Repository parameters:

- R_plus = 0.7331 fm — center radius of the positive inner profile;
- R_minus = 0.8409 fm — center radius of the negative outer profile;
- sigma = 0.210 fm — radial width parameter attached to the profiles.

The repository repeats these as fitted parameters but does not currently
include their source fit, covariance matrix, or uncertainties. They must be
treated as internal model-fit inputs, not independent measured constants.

For a Gaussian-style shell profile,

rho_plus(r) = A_plus exp[-(r-R_plus)^2/(2 sigma_plus^2)]
rho_minus(r) = A_minus exp[-(r-R_minus)^2/(2 sigma_minus^2)]

R_plus and R_minus locate profile centers. sigma controls spread around a
center. Therefore:

DeltaR_center = R_minus - R_plus = 0.1078 fm
sigma / DeltaR_center = 1.9481

The numerical near-factor-of-two is an overlap/width statement, not a second
wavelength calibration.

## Resolution of the earlier candidate fork

### Former Candidate B — rejected as a role conflation

The earlier step

DeltaR = sigma
lambda = 2 pi sigma

is not licensed by the shell model. It equates profile width with adjacent
shell-center spacing without a derivation. Candidate B is removed from the
calibration competition.

This does not prove sigma is irrelevant. It remains necessary for overlap,
self-energy, and coupling calculations. It simply cannot be used as shell
spacing by definition.

### Adjacent-shell hypothesis — sharpened, not proved

Assume R_plus and R_minus are adjacent integer shells n and n+1 of one
wavelength lambda:

R_n = n lambda/(2 pi)
R_(n+1) = (n+1) lambda/(2 pi)

Then the radii alone imply

n_est = R_plus/(R_minus-R_plus) = 6.800557

The unique nearest adjacent integer assignment is therefore

n_plus = 7
n_minus = 8.

The two independent wavelength estimates are

lambda_plus = 2 pi R_plus/7 = 0.658029 fm
lambda_minus = 2 pi R_minus/8 = 0.660441 fm.

They differ by 0.366%.

The least-squares common wavelength for the fixed integer pair (7,8) is

lambda_star = 2 pi (7 R_plus + 8 R_minus)/(7^2+8^2)
            = 0.659395 fm.

It predicts

R_7_star = 0.734622 fm, residual R_plus-R_7_star = -0.001522 fm (0.208%)
R_8_star = 0.839568 fm, residual R_minus-R_8_star = +0.001332 fm (0.158%).

This is a substantially cleaner consistency result than the former
"8/7 is suggestive" note. Under the adjacency assumption, 7 and 8 are not
an arbitrary rational approximation; they are the nearest integer shell
labels selected by n_est.

However, this is still not a completed calibration because:

1. adjacency of the positive and negative profile centers has not been derived;
2. the parameter uncertainties and covariance are absent, so the residuals
   cannot be assigned statistical significance;
3. the radii are internal fit parameters whose source derivation is not stored;
4. higher non-adjacent integer pairs can approximate a radius ratio unless
   adjacency is physically established.

Provisional geometric result:

lambda_nuclear,candidate = 0.659395 fm, conditional on the 7/8 adjacent-shell model.

This value may be used only as a labeled sensitivity-test parameter, not as a
measured or calibrated One-Wave constant.

## Deeper shell-number / energy result

D-405 currently uses a variable-radius, fixed-wavelength family:

R_n = n lambda/(2 pi).

For an angular phase mode on a circle, the tangential wavenumber is

k_n = n/R_n.

Substitution gives

k_n = n/[n lambda/(2 pi)] = 2 pi/lambda,

which is independent of n.

Therefore A-114's dispersion relation omega(k) does not, by itself, produce
an energy ladder across D-405's current shell family. If energy is only
E_n = hbar omega(k_n), then all n share the same k and the same omega, giving
DeltaE_(n+1,n) = 0.

This resolves A-114's former generic "n to k mapping" question negatively
for the present D-405 geometry. The repository must choose and derive one of
these distinct models before predicting shell energies:

A. fixed boundary radius R with k_n=n/R;
B. variable radius with fixed lambda plus an independently derived per-wavelength
   action/energy rule E_n=n epsilon_lambda;
C. radial eigenmodes k_(r,n) from a real boundary-value equation;
D. nonlinear/coupled shell energy depending on curvature, overlap, pressure,
   or junction terms rather than omega(k) alone.

A-114 has already narrowed omega(k) to existing lattice parameters in its
small-k regime. The remaining energy blocker is not an arbitrary missing
proportionality constant; it is the absent physical map from shell geometry
to mode energy.

## Carbon/Hoyle consequence

The earlier factor-of-two calibration fork is closed as a false comparison.
The carbon calculation is still blocked by three explicit items:

1. establish whether the neutron profile centers really are adjacent n=7,8 shells;
2. recover or independently reproduce the fit and its uncertainties;
3. derive the shell-geometry-to-energy map listed above, then connect it to
   the carbon-12 collective mode rather than inserting the 7.65 MeV target.

No Hoyle-state number is produced here.

## Yellow Audit

Resolved:
- sigma is a width, not a second shell-spacing measurement;
- the factor-of-two disagreement is not evidence of two incompatible lambdas;
- the unique nearest adjacent assignment is n=7,8;
- conditional best-fit lambda is 0.659395 fm;
- D-405's current variable-radius family has k_n independent of n, so its
  energy ladder cannot come from dispersion alone.

Still open:
- physical derivation of adjacency;
- provenance and uncertainty of R_plus, R_minus, sigma;
- full radial profile and overlap-energy derivation;
- shell-geometry-to-energy rule;
- carbon-12 collective-mode mapping.

## Future Work

1. Recover the original neutron-profile fit or refit the charge distribution
   with stated uncertainties and covariance.
2. Derive whether opposite-sign shell centers must occupy consecutive radial
   indices; do not assume adjacency merely because 7/8 fits well.
3. Use sigma in the overlap/coupling integral where it belongs.
4. Select one shell-energy model A-D and derive it from existing One-Wave
   equations.
5. Only then run a held-out carbon/Hoyle calculation.

---

## SOURCE: D-408_Sixfold_2D_Triangular_Hexagonal_Lattice.md

---
node_id: "D-408"
canonical_name: "Sixfold 2D Triangular-Hexagonal Lattice"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Native 2D Geometry / Simulation Foundation"
claim_gate_detail: "YELLOW (geometry) / GREEN (physical interpretation and dynamics)"
metadata_standard: "I-06"
---

# Node D-408: Sixfold 2D Triangular-Hexagonal Lattice

**Dependencies**  
Upstream: A-101 Ground / Zero, A-102 Displacement, A-104 Gradient, A-117 Dimensional Integrity, B-206 Paired Loop  
Lateral: D-411 Mirrored Axis Pairs, D-412 Lattice Simulation Standard, E-520 Recursive Self-Modeling Levels, E-524 Kuramoto Lattice Synchronization  
Downstream: D-413 Ground-lattice orbital-restoring simulation, circulation-emergence simulation, quark-phase simulation, Wave Computer cell simulations

## Definition

The native 2D One-Wave lattice is a triangular connection lattice with a hexagonal cell or neighborhood view.

Choose basis vectors

\[
\mathbf a_1=a(1,0),
\qquad
\mathbf a_2=a\left(\frac12,\frac{\sqrt3}{2}\right).
\]

A lattice site is

\[
\mathbf r_{mn}=m\mathbf a_1+n\mathbf a_2.
\]

Every interior site has six equidistant in-plane nearest neighbors. The native coordination is therefore

\[
\boxed{6{:}1}.
\]

The triangle view records local connections. The hexagonal view records the bounded neighborhood and closed circulation routes generated by those connections. They are two views of the same 2D lattice, not separate mechanisms.

The six directed neighbor routes form three mirrored axis pairs:

\[
\boxed{3{:}1\text{ axis-pair view}\quad\leftrightarrow\quad6{:}1\text{ directed-neighbor view}}.
\]

D-411 controls this counting distinction. The `3:1` planar axis-pair count is not automatically the neural `3:1` aggregation ratio.

## Seven-Cell Cluster

The first complete local operating region is

\[
\mathcal C_7=\
\{c_0,c_1,c_2,c_3,c_4,c_5,c_6\},
\]

where \(c_0\) is the active center/reference and \(c_1\ldots c_6\) are the surrounding ring.

Thus

\[
\boxed{1\text{ center}+6\text{ surrounding}=7\text{-cell cluster}}.
\]

The outer six form the first closed loop around the center. The same site may be the center of one cluster and an outer member of another; clusters overlap throughout the lattice.

## Triangle and Hexagon Roles

### Triangular connection view

Each edge carries candidate local quantities such as:

- relative displacement,
- compression or extension,
- shear,
- relative velocity,
- phase difference,
- restoring response,
- transferred work.

For an edge \(i\leftrightarrow j\), define its strain candidate as

\[
\varepsilon_{ij}
=
\frac{|\mathbf r_j+\mathbf u_j-\mathbf r_i-\mathbf u_i|-a}{a}.
\]

### Hexagonal cell view

Each bounded cell or center-plus-six neighborhood may carry derived quantities such as:

- area change,
- local pressure,
- circulation,
- vorticity proxy,
- boundary leakage,
- recurrence phase,
- center drift.

For the six-edge ring, a discrete circulation measure is

\[
\Gamma_6
=
\sum_{k=1}^{6}
\mathbf v_k\cdot\Delta\boldsymbol\ell_k.
\]

A nonzero \(\Gamma_6\) is circulation evidence. It is not by itself a quark or stable Vortex Phase.

## Seed of Life and Flower of Life View

Place equal-radius influence circles on the triangular-lattice centers. One center plus its six surrounding centers produces the seven-circle Seed-of-Life arrangement. Repetition produces the Flower-of-Life overlap pattern.

Within simulations, these circles may visualize:

- influence radius,
- oscillation reach,
- overlap pressure,
- shared boundary range,
- phase-coupling range.

They are generated from the same lattice coordinates. They are not extra physical objects.

## Metatron Connection View

Metatron's Cube is treated as a finite higher-order connection overlay selected from centers in the same sixfold family. It may expose radial, triangular, hexagonal, mirrored, and longer-range pathways.

It does **not** authorize every visible line as an active physical coupling. Every non-nearest-neighbor connection requires a declared rule, weight, and test.

## Stationary Ground Requirement

The undisplaced state is

\[
\mathbf u_i=0,
\qquad
\mathbf v_i=0
\]

for all sites, with zero net update. Stationary means zero net motion, not a frozen lattice. Each site must remain capable of displacement, restoring response, transmission, and return.

## Required First Simulations

1. equilibrium hold with no spontaneous drift;
2. single-site and seven-cell displacement/release;
3. planar compression and recovery;
4. shear input;
5. ring-circulation input;
6. resistance sweep;
7. overlap-field visualization generated from the same state arrays.

D-413 now supplies the first runnable reduced implementation of this geometry, including Ground-fixed and displacement-fixed views, a curvature-well candidate, lattice bunching, and torque ablations.

Every run must satisfy D-412 and record:

- total numerical energy or work balance,
- maximum displacement,
- cell-area change,
- ring circulation,
- recovery time,
- residual drift,
- failure boundary.

## Dimensional Boundary

This node is natively 2D. It can test planar transfer and circulation emergence. It cannot establish a complete 3D Vortex Phase, Three-Vortex Knot, volumetric shell, or Mass Effect tensor.

Those require D-409 and the relevant physical nodes.

## Failure / Falsification

The sixfold candidate fails if another 2D coordination geometry produces better isotropy, recurrence, stability, and perturbation recovery under the same update laws, or if the seven-cell cluster cannot transmit displacement without directional artifacts that survive refinement.

---

## SOURCE: D-409_Twelvefold_3D_Close_Packed_Coordination.md

---
node_id: "D-409"
canonical_name: "Twelvefold 3D Close-Packed Coordination"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Native 3D Geometry / Volumetric Simulation Foundation"
claim_gate_detail: "YELLOW (geometry) / GREEN (canonical physical-lattice candidate)"
metadata_standard: "I-06"
---

# Node D-409: Twelvefold 3D Close-Packed Coordination

**Dependencies**  
Upstream: A-116 Three-Dimensional Spherical Default, A-117 Dimensional Integrity, D-408 Sixfold 2D Lattice, D-411 Mirrored Axis Pairs, D-412 Lattice Simulation Standard, C-317 Boundary-Tension Weave  
Downstream: bounded-excitation simulation, Vortex-Phase simulation, Three-Vortex-Knot simulation, electrical-shell simulation, Mass-Effect response simulation

## Definition

The native physical layer is three-dimensional and volumetric. The current canonical lattice candidate uses close-packed local coordination, where a center has twelve nearest neighbors:

\[
\boxed{12{:}1}.
\]

This is a distinct 3D coordination shell, not two flat six-cell rings pasted together and called a volume.

## Local Neighbor Shell

One convenient normalized twelve-neighbor shell is the cuboctahedral set

\[
\mathcal N_{12}
=
\frac{a}{\sqrt2}
\left\{
(\pm1,\pm1,0),
(\pm1,0,\pm1),
(0,\pm1,\pm1)
\right\}.
\]

The twelve directed neighbor positions may be organized into six opposite coordinate pairs for a declared shell mapping. This gives a `6:1` mirrored-pair view and a `12:1` directed-neighbor view, controlled by D-411. It does not make every six-count mechanism identical.

Each point lies at distance \(a\) from the center. The complete local cluster therefore contains

\[
1\text{ center}+12\text{ nearest neighbors}=13\text{ sites}.
\]

Face-centered cubic and hexagonal close-packed arrangements share this local coordination number while differing in their longer-range stacking. The repository must test stacking rather than quietly treating FCC and HCP as identical.

## Relationship to the 2D Sixfold Layer

A 2D slice or projection of a 3D close-packed neighborhood may expose sixfold rings, triangles, hexagons, seven-center clusters, or thirteen-center diagrams. Such a picture is a projection/indexing view.

The native 3D state includes out-of-plane neighbors and gradients that the 2D view omits.

Therefore

\[
P_{3\rightarrow2}(\mathcal N_{12})
\neq
\mathcal N_{12}
\]

as a full dynamical object, even when the projection preserves sixfold visual symmetry.

## Volumetric State Variables

A 3D lattice site or cell may carry:

\[
X_i^{(3)}
=
\left(
\mathbf u_i,
\mathbf v_i,
\phi_i,
\chi_i,
\mathbf q_i,
B_i
\right),
\]

where candidate meanings include:

- \(\mathbf u_i\): 3D displacement,
- \(\mathbf v_i\): 3D local motion,
- \(\phi_i\): recurrence phase,
- \(\chi_i\): compression state,
- \(\mathbf q_i\): rotational/circulation state,
- \(B_i\): boundary or weave state.

The exact physical update law remains to be derived and tested. These variables are a simulation interface, not proof of mechanism.

## Required 3D Behaviors

The 3D lattice must be capable of displaying and measuring:

- volumetric compression and release,
- shear in multiple planes,
- rotational flow and vorticity,
- bounded recurrence,
- internal/external shell differentiation,
- Boundary-Tension Weave strain,
- Mirror-Gate approach and crossing,
- translation by sequential displacement and reconstruction,
- front compression, side transfer, and rear recovery.

## Relation to Flower-of-Life and Metatron Views

Flower-of-Life, Fruit-of-Life, and Metatron-style diagrams may be used as 2D coordinate, overlap, or connection projections of selected centers. They are not the native 3D object.

A thirteen-center 2D diagram may index the one-plus-twelve local shell, but the mapping must specify which projected point corresponds to which 3D neighbor and which lines represent actual couplings.

## Quark and Proton Boundary

A Vortex Phase must be simulated in this 3D layer. A planar circulation in D-408 is only a precursor test.

A proton candidate requires one continuous volumetric bounded excitation containing three persistent Vortex Phases coupled by the Boundary-Tension Weave. It cannot be validated in a single 2D ring.

## Required First 3D Tests

1. equilibrium hold of the twelve-neighbor shell;
2. isotropy test under impulses in many directions;
3. compression pulse and recovery;
4. rotational perturbation and vorticity retention;
5. localized bounded-excitation formation;
6. perturbation recovery;
7. FCC versus HCP stacking comparison;
8. 2D slice/projection comparison with measured information loss.

## Failure / Falsification

The close-packed candidate fails if:

- another 3D coordination produces demonstrably better isotropy and stable recurrence under the same laws;
- twelvefold local coordination cannot preserve bounded modes without imposed hard walls;
- the claimed 2D/3D correspondence cannot be defined without losing the quantities used by the physical interpretation.

---

## SOURCE: D-410_TwentyFourfold_4D_Field_Void_Recurrence_Shell.md

---
node_id: "D-410"
canonical_name: "Twenty-Fourfold 4D Field/Void Recurrence Shell"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Native 4D Recurrence / State-Coordination Architecture"
claim_gate_detail: "BRONZE (canonical architecture) / YELLOW (physical derivation and measurement)"
metadata_standard: "I-06"
---

# Node D-410: Twenty-Fourfold 4D Field/Void Recurrence Shell

**Dependencies**  
Upstream: A-111 Recursion, A-117 Dimensional Integrity, B-205 Mirror, B-206 Paired Loop, C-301 Mirror Gate, D-409 Twelvefold 3D Coordination  
Bidirectional/Lateral: G-716 One-Wave Conversion Grammar, G-716a Conversion Simulation Rule  
Downstream: full recurrence simulations, Mirror-Gate trajectory analysis, dimensional simulation headers, Wave Computer recursive coordination

## Definition

The One-Wave 4D layer is the ordered evolution of a complete 3D state through recurrence, phase, direction, Mirror-Gate crossing, and return.

Unless a later node explicitly derives a fourth spatial coordinate, write the evolving state as

\[
X^{(4)}(n)
=
\left(X^{(3)}_n,\phi_n,g_n,d_n,h_n\right),
\]

where:

- \(X^{(3)}_n\) is the full volumetric state at update \(n\),
- \(\phi_n\) is recurrence phase,
- \(g_n\) is Mirror-Gate relation,
- \(d_n\) is directional state,
- \(h_n\) is retained history required to distinguish recurrence from a static copy.

A static 3D frame is not a 4D recurrence.

## Twenty-Four-to-One Architecture

The canonical 24:1 relation is a completed Field/Void dual-cycle coordinated around one persistent identity/reference:

\[
\boxed{24{:}1}.
\]

A useful indexing form is

\[
\mathcal R_{24}
=
\{F_1,\ldots,F_{12},V_1,\ldots,V_{12}\},
\]

with one identity/reference \(I\) whose continuity is tested across the cycle.

Here:

- the twelve \(F_k\) positions describe the expressive/Field-facing half of the completed shell;
- the twelve \(V_k\) positions describe the mirrored/compressive/reference-facing half;
- Mirror-Gate relations pair or transform positions across the two halves;
- \(I\) is not replaced at every step; its recurrence continuity is what the shell must test.

This notation is an architecture for simulation and indexing. The physical spacing, timing, and coupling of the twenty-four positions remain Yellow until derived.

## Not a Spatial Neighbor Count

D-409's 12:1 is a native 3D nearest-neighbor coordination candidate. D-410's 24:1 is not automatically twenty-four nearest neighbors in four-dimensional Euclidean space.

The distinction is

\[
12{:}1=\text{volumetric adjacency},
\]

\[
24{:}1=\text{recurrence/state coordination}.
\]

Any later proposal for a literal four-spatial-dimensional lattice must be filed separately and may not overwrite this node by implication.

## Relation to 6:1 and 12:1

The completed architecture preserves the nested relations

\[
6{:}1\quad\text{within a 2D operational neighborhood},
\]

\[
12{:}1\quad\text{within a 3D volumetric neighborhood},
\]

\[
24{:}1\quad\text{across the completed Field/Void recurrence of the 3D state}.
\]

The 24-shell contains the history and mirrored return relation needed to tell whether a 3D mode truly recurs rather than merely resembles an earlier frame.

## Mirror-Gate Position

The gate form

\[
1(0)1
\]

marks a boundary relation between paired states. Zero is an active shared reference or transition condition, not absence.

A valid gate crossing must log:

- state before crossing,
- direction of approach,
- pressure or threshold measure,
- state at the shared reference,
- state after crossing,
- inverse/return path,
- identity continuity or break.

## Required 4D Simulation Record

A simulation claiming 4D recurrence must preserve at least:

```text
complete 3D state or sufficient loss-bounded encoding
update index and physical time candidate
phase
Field/Void side
Mirror-Gate crossing log
direction and inverse direction
prior-state memory
recurrence error
identity continuity score
return-path validity
```

A rendered animation alone is insufficient. The history must be inspectable and replayable.

## Recurrence Tests

For a candidate period \(T\), define a recurrence error

\[
\epsilon_R(T)
=
\frac{\|X^{(3)}(t+T)-\mathcal M X^{(3)}(t)\|}{\|X^{(3)}(t)\|+\epsilon},
\]

where \(\mathcal M\) is the explicitly declared allowed mirror, rotation, translation, or phase-alignment operator.

A return passes only if:

1. \(\epsilon_R(T)\) is below a declared threshold;
2. the gate history is valid;
3. identity continuity is preserved;
4. the result survives perturbation;
5. no unlogged reset reconstructs the desired answer.

## Relation to G-716

G-716's ordered path

\[
24\rightarrow12\rightarrow6\rightarrow3\rightarrow1\rightarrow24
\]

is a conversion grammar across recursive layers. D-410 defines the dimensional and recurrence discipline required when that grammar is represented physically or simulated.

The numerical labels in G-716 are not automatically spatial dimensions or neighbor counts. Every use must declare which role each number has.

## Failure / Falsification

This architecture fails or must be revised if:

- a different recurrence-state count produces the complete Field/Void cycle with fewer assumptions and better predictive performance;
- the 24 positions cannot be mapped to measurable state transitions;
- identity continuity does not require the retained history this node assigns to the 4D layer;
- the 24:1 relation is physically derived as a different native structure.

---

## SOURCE: D-411_Mirrored_Axis_Pairs_and_Directed_Route_Counts.md

---
node_id: "D-411"
canonical_name: "Mirrored Axis Pairs and Directed Route Counts"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Geometry Vocabulary / Coordination Audit / Ratio-Domain Guardrail"
claim_gate_detail: "BRONZE (counting distinction) / YELLOW (cross-dimensional physical bridge)"
metadata_standard: "I-06"
---

# Node D-411: Mirrored Axis Pairs and Directed Route Counts

**Dependencies**  
Upstream: A-103 Differential, A-117 Dimensional Integrity, B-205 Mirror, D-408 Sixfold 2D Lattice, D-409 Twelvefold 3D Coordination, D-410 Twenty-Fourfold 4D Recurrence Shell  
Lateral: G-719 Neural System Functional Analogy Map, G-720 No Control But Self-Control  
Downstream: lattice simulation headers, Android movement-route declarations, ratio-domain audits

## Purpose

This node separates three counts that were being spoken about as if they were interchangeable:

1. undirected or mirrored axis pairs;
2. directed routes;
3. directed routes plus the shared center/reference.

For a local architecture with `N` mirrored axis pairs,

\[
\boxed{N\text{ axis pairs}\rightarrow 2N\text{ directed routes}\rightarrow 2N+1\text{ centered states}}
\]

The center is not another direction. It is the active hold, comparison, or shared reference around which the paired directions are defined.

## Terminology

- one **axis**;
- several **axes**;
- one **mirrored axis pair** contains two opposed directed routes;
- `+` and `-` identify opposed direction along the same axis;
- `(0)` identifies the shared reference or hold state.

Thus one local axis is

\[
-\mathbf d\;(0)\;+\mathbf d.
\]

## Dimensional Count Ladder

| Native layer | Mirrored axis pairs | Directed routes | Centered states | Local ratio views |
|---|---:|---:|---:|---|
| 1D line | 1 | 2 | 3 | `1:1` axis-pair view; `2:1` directed view |
| 2D triangular lattice | 3 | 6 | 7 | `3:1` axis-pair view; `6:1` directed view |
| 3D close-packed shell | 6 candidate opposite pairs | 12 | 13 | `6:1` pair view; `12:1` directed shell |
| 4D recurrence candidate | 12 paired route families | 24 | 25 | `12:1` pair view; `24:1` recurrence shell |

The 2D row is geometrically explicit: six nearest-neighbor directions form three opposite pairs around one center.

The 3D row is a coordinate-pair interpretation of the twelve-neighbor shell and must declare the chosen opposite-pair mapping.

The 4D row is a candidate correspondence to D-410's twenty-four recurrence positions. D-410 is not automatically a spatial kissing-number statement. A simulation or derivation must state whether the twenty-four positions are spatial routes, state routes, Field/Void phases, or another declared domain.

## Domain Declaration

Every ratio must be written with its domain:

```text
3:1 planar mirrored-axis geometry
3:1 nerve aggregation
6:1 planar directed-neighbor geometry
6:1 oversight ratio
12:1 three-dimensional neighbor shell
12:1 engineering throttle ceiling
24:1 Field/Void recurrence shell
```

Matching numbers do not merge mechanisms.

\[
\boxed{\text{same ratio}\neq\text{same domain}}
\]

## Relationship to Foundational Choice

For a selected route family `a`, foundational choice supplies

\[
c\in\{-1,0,+1\}.
\]

The local movement is

\[
\Delta q=c\,\mathbf d_a.
\]

The route family identifies the axis. Choice selects its negative direction, hold state, or positive direction. Binary oversight may permit or block the result but does not create the choice.

## Required Simulation Header

Any simulation using these counts must declare:

```text
native dimension:
axis-pair count:
directed-route count:
center/reference definition:
ratio domain:
projection dimension:
what the projection omits:
```

## Failure / Revision Conditions

This node must be revised if:

1. a proposed shell cannot be paired into the claimed opposite routes;
2. the center is counted as a direction;
3. a neural/control ratio is silently substituted for a geometric ratio;
4. a 4D recurrence count is presented as spatial geometry without a mapping;
5. direction, axis family, and hold are collapsed into one undifferentiated symbol.

---

## SOURCE: D-412_Lattice_Simulation_and_State_Driven_Visualization_Standard.md

---
node_id: "D-412"
canonical_name: "Lattice Simulation and State-Driven Visualization Standard"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Simulation Governance / Wiki Laboratory Standard / Dimensional Visualization"
claim_gate_detail: "BRONZE (simulation standard) / YELLOW (physical implementations pending)"
metadata_standard: "I-06"
---

# Node D-412: Lattice Simulation and State-Driven Visualization Standard

**Dependencies**  
Upstream: A-102 Displacement, A-103 Differential, A-105 Restoring Response, A-117 Dimensional Integrity, C-317 Boundary-Tension Weave, D-408, D-409, D-410, D-411  
Lateral: I-02 proof lifecycle, G-706 Validation  
Downstream: D-413 Ground-lattice orbital-restoring lab, circulation-emergence, Vortex-Phase, Three-Vortex-Knot, electrical-shell, Mirror-Gate, and Mass-Effect simulations

## Purpose

A moving picture is not automatically a simulation. A valid One-Wave simulation must evolve declared state variables under a reproducible update law, calculate measurements from those states, expose failure conditions, and render only quantities actually present in the run.

\[
\boxed{\text{simulation state}\rightarrow\text{measured fields}\rightarrow\text{visualization}}
\]

The prohibited reversal is

\[
\boxed{\text{desired picture}\rightarrow\text{animation pretending to be evidence}}.
\]

## Native Geometry

- native 2D tests use the D-408 triangular connection lattice and hexagonal cell/neighborhood view;
- native 3D physical tests use the D-409 volumetric twelve-neighbor candidate;
- D-410 supplies recurrence/state-history requirements and is not silently rendered as ordinary 3D space;
- every view declares whether it is native, sliced, projected, or derived.

## Stationary Ground

Stationary means zero net motion at equilibrium, not frozen nodes:

\[
\mathbf u_i=0,\qquad \mathbf v_i=0,\qquad \Delta X_i=0.
\]

Every site must remain capable of displacement, transfer, restoring response, and return.

## Minimum State Interface

A physical lattice run should declare at least:

\[
X_i(t)=\left(\mathbf u_i,\mathbf v_i,\phi_i,\chi_i,\mathbf q_i,B_i\right),
\]

where candidate meanings are:

- displacement `u`;
- local motion `v`;
- recurrence phase `phi`;
- compression state `chi`;
- circulation/rotation state `q`;
- boundary/weave state `B`.

The exact update law remains a separate derivation. The interface does not prove the physics.

## Required State-Driven Views

A serious wiki laboratory page should be able to display synchronized views of one run:

1. **deformed lattice:** actual displaced site positions and connections;
2. **triangle-edge view:** relative strain, shear, and transfer along edges;
3. **hexagonal-cell view:** area change, pressure, circulation, leakage, and center drift;
4. **velocity/vector view:** local flow and directional reconstruction;
5. **vorticity view:** circulation calculated from the velocity field;
6. **resistance/restoring view:** calculated local pushback, not generic damping color;
7. **Boundary-Tension Weave view:** strain and confinement derived from the boundary model;
8. **internal/external electrical view:** shown only if the update produces a derived differential shell response;
9. **Mirror-Gate view:** hold, approach, crossing, and return conditions calculated from the declared gate variable;
10. **graph panel:** live measurements from the same arrays.

Flower-of-Life and Metatron-style overlays may visualize overlap radius or declared connection maps. They may not add couplings absent from the update law.

## Required Measurements

At minimum, record:

- total numerical energy/work balance;
- maximum and RMS displacement;
- compression ahead and release behind a moving recurrence;
- edge strain and cell-area change;
- circulation and vorticity concentration;
- boundary leakage;
- recurrence error;
- recovery time after perturbation;
- center drift and residual wake;
- applied work, velocity-dependent drag, and acceleration-dependent response;
- parameter values, grid spacing, time step, seed, and code version.

## Required Failure Tests

Every model must be capable of failing. Required tests include:

1. zero-input drift;
2. time-step and spatial-refinement convergence;
3. energy injection from numerical error;
4. perturbation recovery versus collapse;
5. parameter sweeps that produce stable and unstable regions;
6. interaction ablations;
7. dimensional projection-loss measurement;
8. comparison against periodic, random, or simpler control models where relevant.

## Physical Simulation Ladder

The canonical dependency order is

```text
stationary responsive Ground
-> displacement and recovery
-> compression / shear / rotational input
-> bounded excitation
-> circulation emergence
-> persistent confined Vortex Phase candidate
-> three-phase coupling
-> Three-Vortex Knot / proton candidate
-> electrical-shell and Mirror-Gate response
-> controlled translation
-> four-interaction Mass-Effect measurement
```

The Mass Effect is measured after a complete stable recurrence exists. It is not inserted as an initial parameter.


## First Runnable Implementation

D-413 is the first implementation governed by this standard. It supplies a triangular Ground background, synchronized Ground-fixed and displacement-fixed cameras, an imposed curvature depression, off-axis restoring/orbital tests, torque-based axial spin, a symmetric-shell ablation, a no-well control, zero-input drift checks, CSV receipts, and batch graphs.

D-413 remains Yellow because the well is imposed and the bounded displacement shell is a reduced collective coordinate.

## Wiki Laboratory Requirement

A Silver-candidate physical wiki page requires:

- runnable code or an exact executable reference;
- declared native dimension and projection;
- parameter table;
- raw machine-readable results;
- graphs;
- stable and failed examples;
- interpretation separated from output;
- explicit falsifiers.

An illustration or artistic reconstruction is welcome only when labeled as art and grounded in a specific simulation receipt.

## Failure / Revision Conditions

This standard fails if it permits an animation to be promoted without state equations, raw results, failure cases, or reproducibility; or if it forces a renderer to display a theoretical feature that the underlying update never calculated.

---

## SOURCE: D-413_Ground_Lattice_Orbital_Restoring_Simulation.md

---
node_id: "D-413"
canonical_name: "Ground Lattice Orbital-Restoring Simulation"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Ground-Lattice Laboratory / Orbital-Restoring Candidate / State-Driven Visualization"
claim_gate_detail: "YELLOW (reduced coupled simulation; physical derivation open)"
metadata_standard: "I-06"
---

# Node D-413: Ground Lattice Orbital-Restoring Simulation

**Dependencies**  
Upstream: A-101 Ground Zero, A-102 Displacement, A-103 Differential, A-105 Restoring Response, A-109 Inertial Memory, A-117 Dimensional Integrity, C-317 Boundary-Tension Weave, D-408, D-411, D-412  
Lateral: B-202 Pressure, E-502 Flowback, E-503 Pressure, E-506 Stability  
Downstream: bounded excitation, circulation emergence, Vortex Phase, quark, proton knot, electrical shell, Mirror Gate, and Mass Effect simulations

## Purpose

D-413 is the first runnable Ground-lattice background for later physical simulations. It provides a responsive native-2D triangular connection lattice, a derived hexagonal-neighborhood view, an imposed curvature depression rendered directly through the deformed triangular surface, and a bounded displacement region that moves on and responds to that same surface.

The model is deliberately lower than a quark. It asks whether a declared lattice can visibly and measurably:

- remain stationary at zero input without being frozen;
- deform, bunch, resist, and restore;
- carry a bounded displacement region across the Ground;
- display the same physical run in Ground-fixed and displacement-fixed camera frames;
- turn an off-center fall through a curvature well into orbital motion;
- generate axial torque when unequal restoring forces act across an asymmetric bounded shell.

A camera change must never change the state equations:

\[
\boxed{\text{Ground-fixed view}\equiv\text{displacement-fixed scrolling view}}
\]

The equivalence is observational only. The physical state remains one run.

## Native Dimension and Geometry

```text
native dimension: 2D lattice coordinates with a rendered height/depression field
connection geometry: triangular, six directed nearest-neighbor routes
cell/neighborhood view: derived hexagonal rings
axis-pair count: 3 mirrored pairs
centered local count: 6 directed routes + 1 reference
projection: oblique 2D rendering of x,y,z state
omitted: full 3D twelve-neighbor coordination and 4D recurrence shell
```

The lattice is not square and does not use four-neighbor Cartesian propagation.

## Ground State

Each site has rest location

\[
\mathbf X_i^0=(x_i^0,y_i^0,0)
\]

and dynamic state

\[
\mathbf X_i=\mathbf X_i^0+\mathbf u_i,
\qquad
\dot{\mathbf u}_i=\mathbf v_i.
\]

Nearest-neighbor edges supply a provisional elastic work law:

\[
\mathbf F_{ij}
=
\left[k_s(\ell_{ij}-\ell_0)
+c_e\left((\mathbf v_j-\mathbf v_i)\cdot\hat{\mathbf e}_{ij}\right)\right]
\hat{\mathbf e}_{ij}.
\]

Each site also has local return and resistance:

\[
\mathbf F_{i,\mathrm{Ground}}
=-k_0\mathbf u_i-c_0\mathbf v_i.
\]

These are numerical candidate work laws. They do not assert that the physical One-Wave Ground is literally made of mechanical springs.

## Imposed Curvature Depression

The first gravitational-well test uses a declared Gaussian target depression:

\[
z_G(x,y)
=-D\exp\left[-\frac{(x-x_G)^2+(y-y_G)^2}{2\sigma_G^2}\right].
\]

Lattice sites are initialized on this target depression when the well is enabled, then continue evolving under lattice coupling, restoring response, resistance, and well-follow forces. The well is therefore visible from the first frame rather than existing only as an invisible force calculation.

The browser renderer triangulates the actual displaced lattice sites and shades those calculated faces. Curved contour rings sample the same interpolated height field used by the moving bounded region. A Ground-to-bottom depth marker reports the current sampled depression. Vertical exaggeration changes only the projection and never the state equations.

The bounded displacement centroid and its shell samples use the same surface interpolation for displayed height and restoring-gradient calculation:

\[
\boxed{z_{\rm display}(\mathbf q)=z_{\rm force}(\mathbf q)=\mathcal I[\{z_i\}](\mathbf q)}
\]

If the visible depression and the sampled restoring surface disagree, the renderer fails.

The curvature well is **imposed**, not derived. D-413 therefore tests the consequences of a curvature/restoring field but does not claim to derive gravity.

## Bounded Displacement Region

The moving structure is represented as a collective bounded shell, not a particle. Its reduced state is

\[
Q(t)=\left(\mathbf q,\dot{\mathbf q},\theta,\omega\right),
\]

where \(\mathbf q\) is the displacement centroid, \(\theta\) is shell orientation, and \(\omega\) is axial spin.

The shell is sampled at points \(\mathbf r_a\) around an ellipse. Each sample feels the local restoring field:

\[
\mathbf f_a=-g_R\nabla z(\mathbf q+\mathbf r_a).
\]

The translational restoring response is

\[
\mathbf F_Q=\frac{1}{N_s}\sum_a\mathbf f_a-c_Q\dot{\mathbf q}.
\]

The axial torque is

\[
\boxed{
\tau_Q
=
\frac{1}{N_s}\sum_a
\mathbf r_a\times\mathbf f_a
-c_\omega\omega
}
\]

and

\[
I_Q\dot\omega=\tau_Q.
\]

For a perfectly symmetric shell in a symmetric central well, the finite reference ablation produces approximately zero axial torque. With shell asymmetry or off-axis loading, unequal restoring forces can produce nonzero torque.

This is the precise simulation version of:

```text
displacement falls across the depression
-> restoring force is unequal across the shell
-> different shell regions correct by different amounts
-> torque appears
-> orbit and axial spin may emerge
```

Spin is not inserted as an animation command.

## Lattice Coupling

The bounded region deforms the actual lattice through a localized pressure field. The pressure is biased toward the direction of travel so the renderer can measure:

- bunching ahead;
- side strain;
- depression beneath the region;
- release and wake behind.

The lattice reaction is included only as a weak reduced feedback in this first version. A later promotion must derive a complete action-reaction work ledger.

## Camera Modes

The browser laboratory provides:

1. **Ground fixed:** the lattice remains visually fixed while the displacement crosses it;
2. **Displacement fixed:** the displacement stays centered and the lattice scrolls beneath it;
3. **Well fixed:** the curvature center remains fixed.

These are renderer transforms only:

\[
\mathbf X_i^{\mathrm{screen}}
=\mathcal P\left(\mathbf X_i-\mathbf C_{\mathrm{camera}}\right).
\]

Changing camera mode must leave every saved metric unchanged.

## Runnable Artifacts

```text
Nodes/D-413_Ground_Lattice_Orbital_Restoring_Simulation/index.html
Nodes/D-413_Ground_Lattice_Orbital_Restoring_Simulation/simulate_d413.py
Nodes/D-413_Ground_Lattice_Orbital_Restoring_Simulation/results/
```

The browser laboratory includes live controls, camera changes, top-down and curved-surface projections, adjustable view-only vertical exaggeration, shaded triangular curvature faces, sampled depth contours, a visible well-depth marker, lattice-freeze ablation, strain and velocity overlays, orbital trail, metrics, and CSV export.

The batch validator runs five finite cases:

1. off-axis drop;
2. asymmetric orbital shell;
3. symmetric-shell torque ablation;
4. no-well travel control;
5. zero-input drift.

## Current Finite Results

The reference run reports:

- zero-input drift below numerical tolerance;
- nonzero lattice strain when pressure coupling is active;
- a changed path under the well compared with the no-well control;
- nonzero axial spin for the asymmetric shell;
- approximately zero axial spin for the symmetric-shell ablation.

These results validate the declared reduced code path only. They do not validate One-Wave gravity, quark identity, proton structure, electrical-shell emergence, or Mass Effect.

## Required Next Tests

Before promotion, D-413 must add:

- time-step refinement;
- lattice-radius refinement;
- boundary-reflection and periodic-boundary comparisons;
- full work accounting for imposed well, damping, and lattice reaction;
- a field-only displacement with no collective shell coordinate;
- derived circulation and vorticity from the lattice state;
- stable-orbit windows versus capture, escape, and collapse;
- 3D D-409 translation after the 2D mechanism is understood.

## Failure / Revision Conditions

D-413 fails if:

1. camera mode changes the physical trajectory or measurements;
2. spin remains when the shell is symmetric and all torque sources are removed;
3. the zero-input lattice drifts or injects energy;
4. the renderer displays compression, curvature, orbit, or spin not calculated from state;
5. the visible well surface, contour geometry, displacement height, and restoring gradient do not come from the same lattice state;
6. the curvature well is described as derived gravity;
7. the bounded shell is mislabeled as a quark or particle;
8. a visually attractive orbit is promoted without convergence, ablation, and work-ledger tests.

---

## SOURCE: D-414_Four_Interaction_Shell_Simulation.md

---
node_id: "D-414"
canonical_name: "Four-Interaction Shell Simulation (Real Data as Wave Data)"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Reduced Simulation / Four-Interaction Visualization"
claim_gate_detail: "YELLOW (illustrative simulation of the C-318 coupled four-interaction state driven by real experimental data used as wave data; candidate geometry and couplings; does not derive gravity, charge, proton, or Mass Effect)"
metadata_standard: "I-06"
---

# Node D-414: Four-Interaction Shell Simulation

**Assets**
- `Nodes/D-414_Four_Interaction_Shell_Simulation/four_interaction_sim.html` — live interactive simulation
- `Nodes/D-414_Four_Interaction_Shell_Simulation/data/waves_bundle.json` — real datasets as wave data
- `Nodes/D-414_Four_Interaction_Shell_Simulation/graphs/*.png` — rendered data graphs (six_step_cycle, ligo_events, eeg_bands, reactor_isotopes, binding_curve, four_channels)
- `Wiki_Pages/D-414_Wiki_Page.html` — wiki page with embedded live sim + graphs

**Dependencies**
Upstream: C-318 Four-Interaction Mass-Effect Response, C-317 Boundary-Tension Weave, C-311 Electric-Magnetic Duality, C-301 Mirror Gate, C-322 (125 GeV anchor), A-115 Unified Compression Field
Downstream: One_Wave_Bench experiment ledger

## Purpose

D-414 renders the **four interactions** of the C-318 coupled state — **not** the four fundamental forces, but the four channels of **one** bounded wave — and drives each channel with a **real experimental dataset used as wave data** (the actual time series or spectrum fed in as the channel's wave function, not merely a headline constant).

The four interactions:

1. **Z_K — Three-Vortex Knot:** internal braided geometry (the proton drawn as three interwoven strands).
2. **Z_E — Electrical Shell:** pressure/voltage shell and its push-back against compression.
3. **Z_M — Mirror Gate:** compression↔expression reversal boundary (C-301 / C-322, 125 GeV anchor).
4. **Z_T — Boundary-Tension Weave:** surface + volume confinement / gluon-like surface tension (C-317).

## The Six-Step Master Cycle (B-221) — how every dataset is folded

Every real dataset is folded onto the repo's canonical six-step cycle, exactly as it already lives in the repo (`Nodes/B-221_Six_Recursive_Steps.md`):

**BEGIN → MOVE → HOLD → BUILD → BREAK → LOOP**

The fold is:
- **Nested / recursive (B-220):** the same six steps repeat inside every step, five scale layers deep — Micro ⊂ Small ⊂ Medium ⊂ Large ⊂ Macro.
- **Everything doubles + bidirectional (B-224, C-301):** the forward pass is doubled by a mirror-reversed pass; each dataset yields a 48-point bidirectional envelope, forward then mirrored through the center. Mirror M² = −I, M⁴ = I (4π closure).
- **Oscillating at the middle (B-222):** HOLD resolves back toward BEGIN through the oscillation center (A-108); every transition is Compression ← Center → Expression.

Each dataset in `waves_bundle.json` therefore carries a `fold` object: `center_pivot`, `amplitude`, the six `steps{BEGIN..LOOP}` with per-step level/energy, `hold_returns_to_begin_residual`, `break_crossing`, the `bidirectional_envelope`, `nested_scales`, and a `nested_energy_tree` (6 branches at each of 5 levels). The simulation animates the bidirectional envelope; the graphs render the folded steps.

## Real Data as Wave Data (expanded)

| Channel | Real datasets (each used as wave, folded on the six-step cycle) | Source |
|---|---|---|
| Z_M Mirror Gate | **7 LIGO/Virgo events**, 32 s @ 4096 Hz each — GW150914 (BBH, break-crossing), GW151226 (Boxing Day BBH), GW170817 (binary neutron-star, ~2.74 M☉), GW190425 (2nd BNS), GW190521 (massive BH, ~142 M☉), GW190814 (most asymmetric masses, 2.6 M☉ mass-gap secondary), GW200105 (first confident neutron-star–black-hole); **125.11 GeV Higgs** = mirror-gate boundary scale | GWOSC / LIGO-Virgo; ATLAS/CMS |
| Z_E Electric Shell | **8 real EEG records** across 5 subjects (PhysioNet eegmmidb, 160 Hz) — S001R01 eyes-open, S001R02 eyes-closed (real Berger alpha-blocking, highest alpha 0.178), S001R03 motor task, S001R04 motor imagery, S002R01/S003R01/S004R01/S005R01 additional subjects; **antimatter** = same shell with inverted voltage differential (CERN ALPHA 1S–2S) | PhysioNet / CERN ALPHA |
| Z_T Boundary-Tension Weave | **5 reactor isotopes** — point-kinetics neutron-flux transients from measured Keepin six-group delayed-neutron data: U-235 thermal (β=0.0067), Pu-239 thermal (β=0.0022), U-238 fast (β=0.0164), U-233 thermal (β=0.0026), Th-232 fast (β=0.0291, largest); plus the **nuclear binding-energy curve** (peak Ni-62/Fe-56 ~8.79 MeV) | Keepin / NEA / IAEA; Wikipedia binding curve |
| Z_K Three-Vortex Knot | **Full CODATA-2022 anchor set** — proton 938.272 MeV / 0.8409 fm (uud = three braids), neutron 939.565 MeV, electron 0.511 MeV, the complete three-generation quark ladder (up 2.16, down 4.70, strange 93.5, charm 1273, bottom 4183, top 172570 MeV), lepton ladder (muon 105.7, tau 1776.9 MeV), deuteron & alpha-particle masses, radii, g-factors, fine-structure constant; braided phase is candidate geometry | NIST CODATA 2022 / PDG 2024 |

## What the Simulation Shows

- **Proton braids / knot (Z_K):** three interwoven strands with adjustable crossing number — the Three-Vortex geometry drawn explicitly.
- **Toroidal flow (Z_T):** particles circulating around a torus, flow rate modulated by real reactor kinetics — the surface + volume confinement of C-317.
- **Electric shell + push-back (Z_E):** a pulsing shell that displaces inward and pushes back when EEG-driven data compresses it.
- **Mirror-Gate boundary (Z_M):** a crossing ring that flashes when the LIGO strain amplitude passes threshold.
- **Cross-coupling E_×:** live energy panel tracks E_K, E_E, E_M, E_T and the load-bearing cross term, per C-318.
- **Data-drive selector:** choose any single real dataset (each LIGO event, each EEG record, each reactor isotope, the binding curve, or antimatter) or the blended “all real data” mode; the selected dataset's six-step bidirectional envelope drives the live simulation.
- **Scale (micro→macro):** from a single proton-scale knot out to many shells whose retained wake is the Extended-Compression / dark-matter view. Camera/scale never changes the physics.

## Discipline & Honest Limits (D-412)

D-414 is a **YELLOW reduced model**. It separates state from measurement from visualization, declares its native dimension (a bounded field of coupled channels), and its runs can fail. The real datasets **drive** the channels as inputs; the geometry and coupling coefficients are **candidate**, not derived.

D-414 does **not** claim to prove gravity, charge, the proton, or Mass Effect, and does **not** reinterpret the source experiments — LIGO remains gravitational waves, EEG remains cortical voltage, reactor data remains neutron kinetics. They are used strictly as wave inputs to an illustrative one-wave analogy.

## Sources

- LIGO/GWOSC event portal (GW150914, GW170817, GW190521): https://gwosc.org/eventapi/
- PhysioNet EEG Motor Movement/Imagery Database: https://physionet.org/content/eegmmidb/1.0.0/
- Keepin six-group delayed-neutron data (U-235 / Pu-239 / U-238; standard nuclear tables, NEA/IAEA): https://www.sciencedirect.com/topics/engineering/delayed-neutron
- Nuclear binding-energy curve: https://en.wikipedia.org/wiki/Nuclear_binding_energy
- NIST CODATA 2022 constants: https://physics.nist.gov/cuu/Constants/
- Higgs 125.11 GeV: https://atlas.cern and https://cms-results.web.cern.ch
- Six-step cycle & nesting: `Nodes/B-221_Six_Recursive_Steps.md`, `B-220_Scale_Layer`, `B-222_Oscillation_Center`, `B-224_Two_Choices`, `C-301_Mirror`

---

