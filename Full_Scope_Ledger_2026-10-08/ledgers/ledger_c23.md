# Code ledger, slice c23 (15 files, all read in full)

Repo: /home/user/One-Wave-Science/solvers

## solvers/test_dispersion_validator.py (229 lines)
- Purpose / node IDs cited: unittest suite for `dispersion_validator.OneWaveDispersionValidator`. Cites D-600 (1D scalar dispersion, characteristic equation, L17-67) and D-602 (vector-field E/B sign flip, L70-124).
- Point rotation: not present. "omega" is mode frequency from omega = -i ln(lambda) (L54-67), not spin.
- Path rotation: not present.
- Field: no curl/chi. Longitudinal (E-like) vs transverse (B-like) dispersion, C_long = 2-gamma-beta k^2, C_trans = 2-gamma+beta k^2 (L110-124).
- Magnetism: "B" is only the transverse dispersion branch (L89-96). No B tensor, R, K_L or kappa_R.
- Parent/child: not present.
- Hard-coded targets / refits: none. gamma=0.5, beta=0.5 test settings.
- Pass criterion: algebraic identities (eigenvalue product = 1-gamma, L24-34), |lambda| <= 1 stability (L130-141), report keys present (L169-194). Several checks are weak (L96 only |omega_b|>0; L105-108 only array length; L163 "len>0").
- Violations: none against canonical rules. Note: weak assertions (L96, L107-108, L163) do not test the claim in their docstrings.

## solvers/test_driven_bulk.py (97 lines)
- Purpose / node IDs cited: unittest for `driven_bulk` (external uniform force on `bulk_excitation.BulkExcitation` packet). No node IDs.
- Point rotation: not present.
- Path rotation: centroid translation only; periodic centroid chart tracks rolled field (L64-73). Carries no L.
- Field: no curl/chi. Force is gradient of external potential (L43-52).
- Magnetism: not present. `m.R` at L82 is the bulk model's phase-lock matrix used in a Hessian eigenvalue (symbol*C/12 + phase_lock*R); not a magnetic R built from B.
- Parent/child: not present.
- Hard-coded targets: q=0 curvature target 0.3 (L86) is an analytic model value, not an observation.
- Pass criterion: work = energy change to 1e-13 (L26-41), time-reversal (L21-24), dt refinement ratios (L54-62), force validation and 64-event budget (L90-95).
- Violations: none.

## solvers/test_driven_report.py (35 lines)
- Purpose: checks retained `driven_bulk_results.json` against source sha256 hashes, 20 runs, norm error < 1e-10 and centroid valid (L13-21); balance-error convergence and force-sign direction (L23-32). L33 comment: direction and convergence do not identify physical inertia or mass.
- Point rotation / Path rotation / Field / Magnetism / Parent-child: not present.
- Hard-coded targets: none.
- Pass criterion: hash binding plus numerical ledger convergence.
- Violations: none.

## solvers/test_galaxy_validation.py (113 lines)
- Purpose: regression for `satellite_galaxy_validator_em_coherence_fixed` and `galaxy_external_validation` (Milky Way satellite / circular-speed screen). No node IDs in file.
- Point rotation: not present.
- Path rotation: circular speed is the observable; predicted_circular_speed = local_speed + 110 km/s (L77). Carries no L.
- Field: "v_wake" additive term: v_total = v_local + v_wake (L23). No chi or grad chi.
- Magnetism: "EM coherence" in module name only; no B/R/K_L here.
- Parent/child: v_total = v_local + v_wake is a raw addition of speeds, no frame transport (L23, L77). Not rotation rates, so the transport rule does not strictly apply.
- Hard-coded targets / refits: velocity_scale_factor 38.69 and 39.23 (L32, L36) are declared fixed calibrated scales; v_local = log10(M*+1e6)/10*38.69 (L35); frozen RMS 86.283139 / 81.647035 (L25). Test asserts both variants FAIL the discrepancy screen (L27, L74, L109) and that legacy output says INVALID_COMPARISON (L89-93). Honest negative result.
- Pass criterion: the test passes when the model fails the external screen (rejection is preserved), plus hash-drift rejection (L54-65).
- Violations: none in this file (it guards against overclaim). The modules it tests use a calibrated scale and a flat +110 km/s offset; out of slice.

## solvers/test_joint_boundary_response.py (111 lines)
- Purpose: unittest for `joint_boundary_response.JointResponse` (13-site 12-neighbour FCC cluster, 4-port scattering). No node IDs.
- Point rotation: not present. `boundary_inertia()` is an effective inertia from the Schur-complement derivative (L41-46); `carried_tensor` is a 3x3 energy-curvature tensor under displacement (L63-73). Translational, not spin or L.
- Path rotation: not present.
- Field: none (no curl, chi).
- Magnetism: not present. Coefficients `cross`, `phase_lock` (L76).
- Parent/child: not present.
- Hard-coded targets: none.
- Pass criterion: Laplacian zero-sum and PSD (L12-21), unitarity/reciprocity (L23-29), passivity and ledger (L31-39), energy drift < 1e-10 (L48-61), coupling-off gives diagonal S (L75-81), global energy scale does not change spectrum (L94-98).
- Violations: none.

## solvers/test_no_kappa_scaling.py (207 lines)
- Purpose: script, not a unittest, testing hadron masses without "Phase 5" kappa_T sqrt(m) scaling. Imports `hadron_knot_geometry`. sys.path is set to /home/claude/... (L12), which is not this repo.
- Point rotation / Path rotation / Field / Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: PDG masses proton 938.3, neutron 939.6, Lambda 1115.7 (L22-26) used as comparators. Hand-set binding -8 MeV (3 vortices) / -30 MeV (2) (L110-115); rank_factor +/-1 rule (L81-92); kappa_T sweep 0.25-0.40 (L157) to pick the best fit.
- Pass criterion: none. Prints % error only.
- Violations: parameter sweep against observed masses (L157, L22-26) that is labelled a "prediction" (L138). Not a rotation-rule violation.

## solvers/test_strange_hadrons.py (121 lines)
- Purpose: module-level script checking alpha_strange = -0.150 against nucleons and Lambda.
- Point rotation / Path rotation / Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: PDG masses (L14-23). alpha_strange=-0.150 and kappa_T_base=0.373 (L36-37, L85-86) were tuned on Lambda (see validate_strange_baryon_family L5, L174 "optimized for Lambda") and then scored on Lambda. On exception, falls back to the fixed value const + 1300 MeV (L77-81) with a bare `except:`.
- Pass criterion: Lambda error < 15% and nucleon mean < 10% prints "KEYSTONE UNLOCK VERIFIED" (L117-119).
- Violations: a value fitted to Lambda is reported as verifying Lambda (L84-86, L117-119). The silent fallback can make up a mass (L77-81).

## solvers/time_averaged_phase_locking.py (258 lines)
- Purpose: diagnostic script that claims time-averaged quark phase oscillation reduces kappa_T.
- Point rotation: not present. omega_i = kappa_T/m_i (L70) is a phase-oscillation frequency, not body spin and not L.
- Path rotation / Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: PDG masses (L43-47). PREDICTED_BASE (L49-53) and the error table {proton -23.9, neutron +27.7, Lambda +203.5} (L193) are hard-coded, not computed. Symmetric-pair reduction 0.6 is "Empirical" (L108). Amplitudes are computed (L81-88) but never used.
- Pass criterion: none. Narrative printout (L206-254) asserts causal explanations of the hard-coded errors.
- Violations: hard-coded error values presented as explained by the mechanism (L193, L251-253). Not a rotation-rule violation.

## solvers/time_resistance_probe.py (100 lines)
- Purpose: A-114 1D recurrence: exact root, packet group speed, moving phase rate, damping decay. Cites E-533 for the resistance hypothesis (L87).
- Point rotation: not present. Moving phase omega - k v_g (L63) is stated to be a transport observable, not proper time (L89).
- Path rotation: packet translation (L39-42, L51). No L.
- Field: none.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets: none. The Lorentz comparator is computed but is "not inserted into the evolving dynamics" (L64-65, L90).
- Pass criterion: root residual < 1e-12, carrier frequency < 1e-10, group speed / moving phase < 0.003, decay < 1e-6 (L78-82). The pass bit is numerical agreement of the recurrence with its own dispersion.
- Violations: none. The scope limits are stated (L83, L87-94). gamma is damping with no receiving field (L93); this is stated, not hidden.

## solvers/unified_phase_solver.py (555 lines)
- Purpose: "Phase 5" five-phase x five-scale classifier. Maps psi to "particles" via extrema and plaquette vortex counts, and computes gravity from "pressure". No node IDs except A-115 / Book 5 Ch1 in a docstring (L159).
- Point rotation: not present. Vortex detection counts plaquette phase circulation (L204-243). The plaquette sum (L237-240) is a telescoping sum of raw phases without wrapping, so it is identically 0 (circulation never detected). No spin, omega or L.
- Path rotation: galaxy rotation curve v = sqrt(r a) from -dP/dy (L347-378). Not carried as L.
- Field: no curl or chi. Pressure P = |psi| * 0.012 * scale_factor (L124-134); grad P (L136-148).
- Magnetism: not present. No B, R, K_L or kappa_R.
- Gravity: g = -|grad P| (scalar magnitude, sign lost) (L332-345). Docstring "G = -grad P" (L140, L308). Not g = -alpha K_L grad chi.
- Parent/child: not present.
- Hard-coded targets / refits: coupling 0.012 GeV "from hadron calibration" (L110). Thresholds P_crit=E_crit=0.5 (L65-66). E=0.0966 in demo (L543).
- Pass criterion: none. It prints "Phase 5 solver initialized and tested" unconditionally (L554). validate_against_observations compares acceleration arrays to a supplied rotation array (L479-488) and is never called with data.
- Violations:
  - unified_phase_solver.py:49, :164-175, :290 "Low-pressure region (Superfluid expansion)", "field's natural tendency to expand", "dark_energy_volume". This conflicts with the rule "No expansion, no scale factor".
  - unified_phase_solver.py:140, :308, :332-345 gravity = -grad P from |psi| amplitude, not -alpha K_L grad chi. The A-115 baseline form is absent.
  - unified_phase_solver.py:343 acceleration is a negative magnitude, so the direction is lost.
  - unified_phase_solver.py:237-240 vortex circulation is a telescoping sum (always 0). The photon/meson/baryon counts are therefore meaningless.
  - unified_phase_solver.py:43-48 maps 1-vortex=photon, 2=meson, 3=baryon. Speculation presented as identification.

## solvers/validate_strange_baryon_family.py (263 lines)
- Purpose: tests alpha_strange=-0.150 ("optimized for Lambda", L5, L174) across Sigma and Xi. Builds VortexPhase knots with 120 deg phase offsets (L47-89).
- Point rotation: not present. VortexPhase ell=0, em=0 (no angular momentum quantum) (L49-87).
- Path rotation / Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: PDG masses (L28-37). alpha_strange fitted on Lambda (L5, L167, L174). Base radius 0.85 fm hard-coded (L143, L151). Lambda is included in the "validation" set (L190).
- Pass criterion: at least 4 of 6 hyperons within 15% gives "VALIDATION SUCCESSFUL" (L234-238). Note: the knot names passed ("Lambda (uds)" etc., L190-195) do not match HADRON_MASSES keys ("Lambda", "Sigma+"), so the fallback at L209-214 also fails to find them. err stays None and L223 would format None with :>12.1f. Expected TypeError or N/A path; not run here.
- Violations: fitted parameter re-scored on its own fit target (L190 with L174). Key mismatch (L190-195 vs L28-37, L211) means no error is computed. Not a rotation-rule violation.

## solvers/vortex_phase_oscillations.py (245 lines)
- Purpose: claims vortex phase oscillation lowers confinement energy and "explains ALL residual errors".
- Point rotation: not present. phi_i(t) = phi_mean + A sin(omega t) is internal phase, with omega = kappa_T/(m_avg*100) (L87), computed and unused.
- Path rotation / Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: PREDICTED_STATIC hard-coded (L43-47). A_phase = 0.3 sqrt(kappa/(10 m)) "Empirical" (L84); energy * 100 "Empirical conversion" (L117); kappa_T 0.373 "From calibration" (L152). PDG masses (L36-40).
- Pass criterion: all |err| < 1% prints "ZERO-ERROR ACCURACY ACHIEVED" (L194-201). It returns False otherwise.
- Violations: empirical scale factors chosen to close the gap against observed masses (L84, L117) and reported as explanation (L199-200, L233-234). Not a rotation-rule violation.

## solvers/w2_gravity_emergence.py (407 lines)
- Purpose: "W2 keystone": Ricci from Laplacian of "pressure" P, Einstein tensor, a = -grad P (L6-10). Claims it unlocks dark matter, dark energy, rotation curves, "25+ mysteries" (L12-18).
- Point rotation: not present. Kerr profile adds spin only as a scalar factor (1 + a/r) on P (L286-296). No L and no omega dynamics.
- Path rotation: not present (rotation curves only claimed in prints, L403).
- Field: no curl or chi. P is prescribed analytically (1/r, binary, Gaussian) (L323, L355, L375). Ricci = laplace(P)/kappa (L59-82); "Ricci tensor" = Sobel-of-Sobel second derivatives (L98-105).
- Magnetism: not present. No B, R, K_L or kappa_R.
- Gravity: a = -grad P stated (L9), with Einstein-equation residuals G - kappa T, kappa = 8 pi G/c^4 in SI on unitless lattice P (L153-162, L238-260). T_00 = rho(1+P/c^2) with rho=0.1 default (L181-185). Lambda attributed to "vacuum pressure" (L150).
- Parent/child: not present.
- Hard-coded targets: G=6.674e-11, c=3e8 SI constants mixed with lattice units (L154-155).
- Pass criterion: none. It prints "Einstein equations approximately satisfied" unconditionally (L392-394), whatever the residual (L344, L367, L384).
- Violations:
  - w2_gravity_emergence.py:9, :332-ish docstring a = -grad P, not g = -alpha K_L grad chi. Conflicts with the K_L/chi rule and the A-115 baseline.
  - w2_gravity_emergence.py:13-14, :150 dark energy / cosmological constant from vacuum pressure. Conflicts with "No expansion, no scale factor".
  - w2_gravity_emergence.py:392-399 unconditional success claims.
  - w2_gravity_emergence.py:225 G_tt uses -R_xx as a stand-in (no time derivative).
  - w2_gravity_emergence.py:286-296 spin (Kerr a) enters gravity as an ad hoc scalar pressure modifier.

## solvers/weave_energy_breakdown.py (287 lines)
- Purpose: diagnostic of per-pair phase-locking energy for proton, neutron and Lambda. Monte Carlo over the sphere (L139-177).
- Point rotation: not present. omega = kappa_T/m (L42) is pair coherence bookkeeping only. coherence = 1/(1+ln ratio) (L72-80).
- Path rotation / Field / Magnetism / Parent-child: not present.
- Hard-coded targets: kappa_T_base 0.297 and sigma_T 0.01 "Phase 5 calibrated" (L217-219). Prints a hypothesis (L263-267) that the kappa_T scaling causes asymmetry, although this function uses the unscaled base (L131).
- Pass criterion: none (diagnostic).
- Violations: none against rotation, magnetism or gravity rules. L266 attributes the cause to scaling that is not applied in the computation (L83, L131).

## solvers/yukawa_matrix_solver.py (535 lines)
- Purpose: claims all fermion masses from (beta_crit, gamma_crit) with "0 free parameters". "Status: Framework skeleton, Gate YELLOW" (L27-28). Cites E-529 for neutrinos (L230).
- Point rotation: not present. "harmonic winding" frequency = (1-gamma) beta^(1/n) (L130-161).
- Path rotation / Field / Magnetism / Parent-child: not present. "B-like transverse" appears only in the docstring (L12).
- Hard-coded targets / refits:
  - GENERATION_HIERARCHY = [1, 207, 3477] = observed e/mu/tau ratios (L116), multiplied into the masses (L191, L195).
  - MASS_SCALE_FACTOR 0.0114 "calibrated to match lepton masses" (L115) * 511 MeV electron mass (L195).
  - down = 1.2 * up (L288).
  - The Yukawa matrices are built directly from EXPERIMENTAL_MASSES (L321-324, L338-341) and the observed |V_CKM| (L347-351).
  - Fallback beta=0.891, gamma=0.097 (L511).
  - Reads and writes /home/claude/... paths, outside this repo (L502, L522).
- Pass criterion: none. It reports average relative error and "FREE PARAMETERS REDUCED: 12 -> 0" (L530-531).
- Violations:
  - yukawa_matrix_solver.py:116, :191-195 observed lepton ratios and electron mass are inputs, then reported as predictions.
  - yukawa_matrix_solver.py:321-351 the Yukawa matrix and CKM are copied from measurement.
  - yukawa_matrix_solver.py:399-400, :426-428, :476, :531 claim of 0 free parameters is false given L115-116, L288.

## Slice summary

Point rotation (G-749, L = I omega). No file in this slice implements point rotation, canonically or otherwise. Every "omega" here is something else:
- dispersion/mode frequency: test_dispersion_validator, time_resistance_probe
- quark phase-oscillation frequency kappa/m: time_averaged_phase_locking L70, weave_energy_breakdown L42, vortex_phase_oscillations L87
- generation "winding" frequency: yukawa L130-161

The slice also has no:
- L bookkeeping
- open/closed magnetic switch
- organization target rate
- parent/child transport
- B to R construction
- K_L or kappa_R

So none of these files violates the point-rotation, parent/child or kappa_R rules, but none of them satisfies them either.

Gravity / expansion conflicts. Two files implement gravity outside the canonical form:
- unified_phase_solver.py
  - L140, L308, L332-345: g = -grad P (magnitude only), with P built from |psi|.
  - L49, L164-175, L290: "superfluid expansion" / dark energy.
- w2_gravity_emergence.py
  - L9, L59-82: a = -grad P and Ricci from Laplacian of P.
  - L150: vacuum-pressure Lambda.
  - L13-14: dark energy claim.
  - L392-394: unconditional "satisfied" claims.

Both conflict with g = -alpha K_L grad chi (A-115 baseline when R=0) and with "No expansion, no scale factor".

Spin in gravity. w2_gravity_emergence L286-296 lets the Kerr spin parameter a enter gravity as an ad hoc scalar pressure factor.

Refits reported as predictions:
- yukawa_matrix_solver L115-116, L191-195, L321-351, L399-400
- test_strange_hadrons L84-86, L117-119
- validate_strange_baryon_family L174, L190, L234-238
- vortex_phase_oscillations L84, L117, L194-200
- time_averaged_phase_locking L49-53, L193
- test_no_kappa_scaling L157

Code bugs:
- unified_phase_solver L237-240: the plaquette circulation telescopes to 0, so no vortex is ever detected.
- validate_strange_baryon_family L190-195 vs L28-37: the knot names do not match the mass-dict keys, so no error is computed.

Live vs dead/legacy:
- Live, maintained, honest controls with ledger tests:
  - test_driven_bulk.py, test_driven_report.py: driven_bulk, hash-bound
  - test_joint_boundary_response.py
  - test_galaxy_validation.py: asserts FAIL screens; guards against overclaim
  - time_resistance_probe.py: A-114, scope stated
  - test_dispersion_validator.py: D-600/D-602; some weak assertions
- Dead/legacy ("Phase 5", Claude Haiku era, sys.path to /home/claude/one-wave-science, which is outside this repo):
  - unified_phase_solver.py, w2_gravity_emergence.py, yukawa_matrix_solver.py
  - test_no_kappa_scaling.py, test_strange_hadrons.py, validate_strange_baryon_family.py
  - time_averaged_phase_locking.py, vortex_phase_oscillations.py, weave_energy_breakdown.py

Node IDs seen: D-600, D-602, A-114, A-115 (Book 5 Ch1), E-529, E-533.

Cross-references outside the slice that bear on rotation or magnetism:
- bulk_excitation.py: R matrix with phase_lock, used at test_driven_bulk L82. Worth checking whether this R is meant as the canonical magnetic R.
- joint_boundary_response.py: boundary_inertia, carried_tensor.
- satellite_galaxy_validator_em_coherence_fixed.py and galaxy_external_validation.py: "EM coherence", v_wake.
- hadron_knot_geometry.py and hadron_mass_predictor.py
- dispersion_validator.py
