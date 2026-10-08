# Code ledger, slice c14 (13 files)

All line numbers are from each file's own numbering. All 13 files were read in full.

## scripts/tests/test_brain_buddy_council.py
- Purpose / node IDs cited: Offline contract tests for `scripts/brain_buddy_council.py` (L1, L13). They cover the multi-AI "Council" (gemini, deepseek and local ollama workers), reference snapshots, FIELD/VOID six-step loop (L228-233), child loops, budgets, drift (RE_REFERENCE), science evidence receipts (L503-528) and local reference windows (L544-556). No physics node IDs are cited. A test fixture node `TEST` is used (L190).
- Point rotation: not present.
- Path rotation: not present.
- Field: not present. "FIELD"/"VOID" are names of loop phases, not a physical field (L231).
- Magnetism: not present.
- Parent/child: There are parent and child council loops (L252-268), but this is process orchestration, not rate transport.
- Hard-coded targets / refits: none. Fixture CSV `Run,E1\n1,3.5` (L507) is test data only.
- Pass criterion: Each unittest assertion on receipt status (AGREED_RESOLUTION, HOLD, INVALID_RETURN, BUDGET_EXHAUSTED and so on). Nothing physical.
- Violations: none. The file is outside physics scope.

## sims/00-lattice-primitive/dispersion_octave_fixture.py
- Purpose / node IDs cited: G-766 triangular-lattice dispersion and octave control (L1). Gate YELLOW (L18). Self-described as "numerical control fixture, not a physical lattice derivation" (L3-5).
- Point rotation: not present. "omega" here is a temporal mode frequency, omega^2 = omega0^2 - c^2 * symbol (L34-44). It is not a body spin rate.
- Path rotation: not present.
- Field: A scalar mode on a 6-neighbour triangular Laplacian symbol (L22-31) with group velocity (L88-104). There is no curl, wake, chi or grad chi.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: The octave fixtures are (10, 20, 40) and (10, 15, 23) (L191-192). They are labelled controls, and the file states "no octave emergence or physical scale established" (L194). The flags a_num_is_physical_length=False and derived_physical_lattice_spacing=False are set at L173-174.
- Pass criterion: Leapfrog frequency converges to the analytic omega. The octave receipt all_pairs_compatible is true when every pair has |log2 residual| <= epsilon (L137-144).
- Violations: none.

## sims/00-lattice-primitive/lattice-kernel.js
- Purpose / node IDs cited: G-764 numerical control kernel (L1). States "Numerical coordinates are not physical spacing."
- Point rotation: not present. Each site has a scalar displacement x, a velocity v and an oscillator phase = atan2(v/w, x) (L72). This is oscillator phase, not body attitude. There is no L, inertia or attitude.
- Path rotation: not present.
- Field: The "circulation" observable is a discrete phase-space ring sum, sum(x_a v_b - x_b v_a) over a site ring (L45-48). It is reported as a measurement only and nothing feeds back into dynamics. There is no compression, chi or grad chi. The adapter lists "Compression, vorticity field ... unavailable" (adapter L24).
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: Values stay finite. Steps are atomic and each substep must satisfy h*sqrt(stiffness) <= SAFETY (L63-80). The receipt reports physical_lattice_spacing 'UNDEFINED' (L81).
- Violations: none. This is a numeric oscillator lattice that makes no physics claims.

## sims/00-lattice-primitive/test_dispersion_octave_fixture.py
- Purpose / node IDs cited: Unit tests for the G-766 fixture (L1-12).
- Point rotation: not present.
- Path rotation: not present.
- Field: Tests that the Laplacian symbol is zero at k=0, that it is non-positive, and that the long-wave speed is sqrt(1.5)*c (L16-27).
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: Damping roots keep the declared damping (L29-32). Leapfrog error converges quadratically (L37-42). The receipt refuses any physical spacing claim (L44-51). The exact octave fixture passes and the non-octave fixture fails (L55-63).
- Violations: none.

## sims/24-1-sandbox/modules/01-lattice-primitive/adapter.js
- Purpose / node IDs cited: Sandbox adapter for the G-764 kernel (L2, L12). Reads `Nodes/G-764_Combined_State_Lattice_Simulator_Foundation.md` and checks the `node_id: G-764` header (L89). Hashes its source files (L90) and refuses to run if a source changed after import (L111).
- Point rotation: not present. A single centre site is given an amplitude and a velocity (L61-64). These are oscillator initial conditions, not spin.
- Path rotation: not present.
- Field: A radius-3 hex graph of 37 sites (L34-43). Height is a "displacement projection, not native 3D" (L20). The limitations list states that compression, vorticity field, boundary leakage and work balance are unavailable (L24).
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none. physical_validation is 'unverified' (L122).
- Pass criterion: status 'completed' when every requested step finishes and samples are finite (L127). This is an energy drift report and not a physics pass.
- Violations: none.

## software-zer0/bench_assist.py
- Purpose / node IDs cited: Software helper for the analog CELL bench (L2-5). Scores differential voltages into trit/HOLD bands (L21, L37-65), runs a retained-state history test (L100-116) and a two-of-three triad vote (L119-139). States "Does not store magnetic state" (L5). No nodes are cited.
- Point rotation: not present.
- Path rotation: not present.
- Field: not present.
- Magnetism: Only the prose at L112, "iron may be remembering", which is a hysteresis bench interpretation. No B, R or K_L.
- Parent/child: not present.
- Hard-coded targets / refits: The HOLD band 0.45-0.55 (L21) and the band table (L39-53) are design constants, not observed targets.
- Pass criterion: The history test passes when |probe_a - probe_b| > noise (L101-102). The score test fails rails if CENTER is tied to V_BUS (L89-91).
- Violations: none against the rotation and magnetism rules. It is a bench tool outside physics scope.

## solvers/a115_galaxy_validation_derived_source.py
- Purpose / node IDs cited: Tests the "derived" A-115 hybrid source (sigma_core 0.5, sigma_tail 2.0, weight_tail 0.4) against 45 Milky Way rotation-curve points read from `solvers/data/mw_dr3plus_2023.csv` (L2-11, L26-37). Imports `source_hybrid_nd` and `solve_a115_dimensional` from `a115_dimensional_source_analysis.py` (L23). That file exists but is outside this slice.
- Point rotation: not present.
- Path rotation: The galaxy circular velocity is v_c = sqrt(|a| r) (L40-55). This is the orbit, a Path rate, and it carries no L, which is correct. The sign of a is discarded with np.abs (L49), so an outward (repulsive) acceleration would still produce a rotation speed.
- Field: The acceleration comes from the external solver, a = -alpha dchi/dr (L9, L46). It is interpolated cubically and extrapolated (L154).
- Magnetism: not present. K_L is implicitly I (scalar A-115 baseline). There is no R, so the R=0 A-115 baseline applies.
- Parent/child: not present.
- Hard-coded targets / refits:
  - The source parameters are hard-coded (L59-60, L134-139), along with predicted_ext_int_ratio 0.0391 (L222).
  - A free amplitude scale is fitted to the observed velocities by error-weighted least squares (L89-112, L163). The predictions are then scored against the same data (L168-178) and graded EXCELLENT, GOOD, MODERATE or POOR on MAPE (L190-201). This is a refit to the observed curve that is reported as validation.
  - The docstring says "No parameter fitting - only scale calibration" (L11) and "Derived ... (not fitted to galaxy data)" (L223). The parameter values come from `a115_source_amplitude_law.py`, where they are hard-coded and not derived (see below).
  - The dimensionless solver radius is treated as kpc with outer_radius=30 "to match MW data range" (L64, L133). The output units are km/s only because of the fitted scale.
- Pass criterion: MAPE thresholds of 5, 10 and 15% after the one-parameter fit (L190-201). The criterion is Path (orbit speed) agreement, not point rotation.
- Violations:
  - L89-112, L163-178: an observed rotation curve is used to fit the amplitude and then scored as a prediction.
  - L49: abs() hides the sign of g, so the check cannot tell attraction from repulsion.
  - L222-223: a "derived" label is attached to parameters that are hard-coded upstream.

## solvers/a115_noncompact_source_derivation.py
- Purpose / node IDs cited: A-115 non-compact source study (L1-12). Cites `Nodes/A-115_Unified_Compression_Field.md`, `Nodes/E-532_Bound_Unbound_Criterion_and_Finite_Wake.md` and `solvers/SOURCE_CONSTITUTIVE_DERIVATION.md` (L189-193). The reference_commit is "current", not pinned (L218).
- Point rotation: not present.
- Path rotation: not present.
- Field:
  - The solver uses (K_chi+S_u) lap chi = div J in spherical 1D (L68-104).
  - grad chi is computed at L107-109, and g = -alpha dchi/dr at L112.
  - The source is a radial vector J_r. Because of the flux form (L91), the exterior gradient equals J_r/stiffness locally, so exterior "gravity" exists only where J_r is nonzero. "Exterior" acceleration therefore means the source is non-compact by construction, not that a field reaches beyond the source.
- Magnetism: K_L=I is stated in scope (L199). There is no B or R. This is consistent with the A-115 baseline.
- Parent/child: not present.
- Hard-coded targets / refits: No observed data. The sources are chosen by hand: sigma 0.5/1.0/2.0 and weights 0.3/0.5 (L158-168).
- Pass criterion: none. The script reports exterior/interior acceleration ratios (L172-181).
- Violations and defects:
  - L6, L9, L41-42 and conclusion L231 claim that an exponential tail e^{-r/sigma}/r produces "exterior 1/r^2 gravity". With chi' = J_r/K, an exponentially decaying J_r gives an exponentially decaying g, not an inverse-square one. L42's "behaves as r^(-1)" ignores the exponential factor. This is an overclaim.
  - L132-133: max_compression_error is computed as reconstructed_chi minus compression. That is the displacement-identity check repeated, not the error against an exact solution, so the label is wrong.
  - L46: the r=0 branch returns e^0/1e-6 = 1e6, a hand-set singular value.
  - L233 says amplitude and sigma "can be specified independently without fitting". Nothing in the file derives them.

## solvers/a115_source_amplitude_law.py
- Purpose / node IDs cited: Claims to "derive" a source amplitude law A(d, layer) (L1-6). No node IDs are cited.
- Point rotation: not present.
- Path rotation: not present. Prose only mentions "observed circular velocity curves" (L96-98).
- Field: none computed. No solver is run.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits:
  - The "observed" exterior/interior ratios {2: 0.0195, 3: 0.0391, 4: 0.00357} are hard-coded literals (L12-16). The "derivation" (L37-60) only divides them by the d=2 value.
  - The galaxy law sigma_core 0.5, sigma_tail 2.0, weight_tail 0.4 and predicted ratio 0.0391 are hard-coded returns (L102-110). The file labels them "DERIVED, not fitted" (L93) and "From harmonic layer structure" (L109), but no derivation is computed.
  - "Layer-12 ... 12 musical scales" (L86) is numerology with no computation behind it.
- Pass criterion: none. The script only prints and returns a dict.
- Violations: L12-16 and L102-110 present hard-coded inputs as derived outputs. The galaxy validation script downstream consumes them as "derived".

## solvers/a115_source_scaling_derivation.py
- Purpose / node IDs cited: Sweeps hybrid source parameters in 2D, 3D and 4D at "harmonic layers" r = 6, 12, 24 (L1-14, L116). Imports from `a115_dimensional_source_analysis.py` (L26). No node IDs are cited.
- Point rotation: not present.
- Path rotation: not present.
- Field: Calls solve_a115_dimensional for exterior and interior acceleration maxima (L48-63). Exceptions are silently swallowed (L65-66).
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits:
  - The "Key finding" values 0.0195, 0.0391 and "3D is 2.00x stronger" are printed as string literals (L135-138). They are not taken from the sweep the script just ran. The report repeats "exactly 2x" as a key_constraint (L164-168).
  - The hypothesis A(d) ∝ r^(d-1) is asserted (L141, L171), not tested.
  - next_steps L180 says "Fit A(d) and sigma(d) functional forms".
  - minimize_scalar is imported and never used (L21).
- Pass criterion: none.
- Violations: L135-138 and L164-168 report hard-coded numbers as findings. L65-66 hides failures.

## solvers/a115_static_source.py
- Purpose / node IDs cited: Static spherical A-115 diagnostic with V_b=0. Dimensionless, "not a fit" (L1). Cites `Nodes/A-115_Unified_Compression_Field.md` and `Nodes/C-320_Magnetic_Compression_Path_Coupling.md` (L49-50). reference_commit is pinned to 87ad3af (L56).
- Point rotation: not present.
- Path rotation: not present.
- Field:
  - Compact source J_r = r(1-r^2)^2 for r<1 (L17-18).
  - Solves (K_chi+S_u) lap chi = div J (L19-26). grad chi at L27-29, g = -alpha grad chi at L30.
  - Exact solution chi = -(1-r^2)^3/(6K) is used for the error check (L31).
  - Displacement identity reconstruction at L33-36.
- Magnetism: Scope states K_L=I (L52). Limit L63: "Tensor path weighting cannot create acceleration where grad(chi)=0". This is consistent with C-320, grad chi = 0 → g = 0, and with magnetism not becoming gravity. R=0 gives the A-115 baseline.
- Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: The file reports errors only, including max_exterior_acceleration (expected 0) and the gradient error against the exact source (L39-45). Its conclusion is a negative result: a compact source gives zero exterior acceleration and "does not recover inverse-square gravity" (L60).
- Violations: none. This is the most canonical file in the slice.

## solvers/algorithm_zero_3d_volumetric_lattice.py
- Purpose / node IDs cited: "Algorithm Zero" 3D volumetric D-409 lattice for galaxy rotation curves (L1-15). Cites D-409, described as a twelvefold close-packed lattice (L27).
- Point rotation: not present. No body spin, L or inertia. The docstring's "Collective rotation from phase-locking to galactic wake" (L31) is not implemented.
- Path rotation:
  - The galaxy rotation velocity is built as v = 100 + phase_gradient * 50 km/s (L191). The 100 km/s offset and the 50 multiplier are hand-set, "Scaled to realistic values" (L189-191).
  - The phase is taken from np.angle(ring + 1j*roll(ring)) of a real field (L185). It does not measure a physical orbit, and no L is involved.
- Field:
  - Scalar psi with a 6-neighbour average (L128-142). np.roll wraps periodically in r and z (L131, L139), which links r=0 to r=31.
  - Damping is written as (1-gamma) momentum (L154).
  - A density source term is added as 0.05*0.1*rho every step (L146, L156), an unbounded drive.
  - There is no chi, no grad chi and no curl.
- Magnetism: not present.
- Parent/child: not present. Prose only, "cascade inheritance" (L393).
- Hard-coded targets / refits:
  - volumetric_coupling_enhancement = 8.0, justified only by "1D underpredicts by ~1000x" (L47). This is a refit knob.
  - A typical NGC 628 curve is hand-typed (L258-259), and the galaxy is then relabelled "Test_Galaxy" (L358).
  - The printed claims "Electron orbitals: 0.1% error", "Atomic spectra 0.12%" and so on are bare prints (L310-314).
  - "✓ 3D volumetric coupling successfully models galaxy rotation" and "Proves volumetric D-409 lattice is necessary" are printed unconditionally, whatever the computed error (L385-387).
- Pass criterion: none computed. The success prints do not depend on the comparison.
- Violations:
  - L191: a hand-scaled velocity is reported as emergent.
  - L47: a fudge factor is used to fix the underprediction.
  - L385-387: unconditional success claims.
  - L435: writes to a hard-coded nonexistent path `/home/claude/one-wave-science/...`, so a run would crash at the end. This marks the file as legacy or dead.
  - L131 and L139: periodic wrap in r is unphysical.

## solvers/algorithm_zero_emergence.py
- Purpose / node IDs cited: An "Emergence Encyclopedia" (L1-20). Its scale profiles are hard-coded dataclasses (L222-484). Author line L18. No node IDs are cited.
- Point rotation:
  - Electron spin "phase-locks to nuclear wake at ±ℏ/2", with origin WAKE_PHASE_LOCK and dependence on magnetic_field (L232-243). Spin is thereby caused by an external wake and field rather than carried.
  - Stellar rotation: "Galactic wake induces star's rotation" and "Star phase-locks to galactic spiral wake" (L331-342). The parent wake starts the point spin. This contradicts the rule that a thing keeps the spin it has and does not start one, and the rule that point spin is not created by a field.
  - There is no L, no I omega and no open/closed magnetic switch.
- Path rotation: The rotation curve is "Orbital velocity determined by wake resonance", with predicted_value 220e3 m/s, the observed Milky Way value (L398-409). It also depends on "magnetic_field" (L408).
- Field:
  - detect_pressure_gradient_effects: "gravity = -∇P" with P = |field| (L112-135).
  - "Spacetime curvature ~ ∇²P" (L124).
  - Vortex circulation is a 2D plaquette phase sum (L152-165). Its interpretation is labelled "electron spin ½" (L174), so it conflates Field curl with Point spin.
- Magnetism:
  - The stellar magnetic field comes from "Rotation → plasma motion → lattice reorganization" (L344-354).
  - Extended compression / g_wake depends on "magnetic_field" (L410-421). The galactic rotation curve and spiral arms also list magnetic_field as a dependency (L396, L408). This implies magnetism feeding gravity and orbits.
  - There is no B, R or K_L tensor.
- Parent/child: Phase-lock detection compares the argmax of the FFT index norm (L80-109). The coherence calculation uses parent_power where child power was intended (L105). Rates are not transported.
- Hard-coded targets / refits:
  - predicted_value fields are measured constants: spin 0.5 (L240), -13.6 eV (L252), e = 1.602e-19 (L264), 220e3 m/s (L406), 1e12 M_sun (L418), H0 = 70 km/s/Mpc (L450).
  - The harmonic ratios 0.25 and 0.111 are the hydrogen 1/n^2 ratios (L269-273).
- Pass criterion: validate_emergence_encyclopedia only checks that text fields are non-empty and that harmonic_ratios is non-empty (L490-523). There is no physical pass.
- Violations:
  - L442-453: "universe_expansion / Hubble Expansion" with H0 = 70 contradicts the no-expansion rule (redshift is E-528 path loss).
  - L331-342: a galactic wake starts stellar point rotation.
  - L232-243: spin is created by phase-locking to a nuclear wake or magnetic field.
  - L410-421 and L396-408: magnetic_field is listed as a dependency of the compression/gravity effect and of the rotation curve. This contradicts "magnetism does not become gravity".
  - L120-134: gravity = -∇|psi|, not -alpha K_L grad chi.
  - L174: vortex circulation is labelled spin, so Field curl is conflated with Point rotation.
  - L240-450: measured constants are stored as "predicted_value".
  - L105: coherence bug.
  - L424-426 put the string "harmonic ratios" into harmonic_ratios, so the `{ratio_val:.4f}` format at L576 would raise ValueError when the encyclopedia is printed under __main__.

## Slice summary
- **Canonical point rotation:** No file in this slice implements Point rotation (L = I omega, attitude, open/closed dL/dt switch, inertia axes) at all. None models parent/child rate transport.
- **Canonical on Field/gravity:**
  - `solvers/a115_static_source.py` is the only file that matches the A-115/C-320 rules. It uses K_L=I, g = -alpha grad chi, and gives zero acceleration where grad chi = 0. It honestly reports the negative inverse-square result.
  - `a115_noncompact_source_derivation.py` uses the same correct solver form, but it overclaims inverse-square gravity from an exponential tail and has a mislabelled error metric.
- **Violators:**
  - `algorithm_zero_emergence.py` violates the most rules:
    - expansion with H0 = 70
    - a wake or magnetic field starting point spin
    - magnetism listed as feeding gravity and rotation curves
    - gravity = -∇|psi|
    - curl conflated with spin
    - measured constants stored as predictions
  - `algorithm_zero_3d_volumetric_lattice.py`:
    - hand-scaled rotation velocity (L191)
    - fudge factor of 8 (L47)
    - unconditional "proves" prints (L385-387)
  - The A-115 galaxy chain is circular. `a115_source_amplitude_law.py` hard-codes the ratios and parameters and labels them "derived". `a115_source_scaling_derivation.py` prints literal findings. `a115_galaxy_validation_derived_source.py` fits an amplitude to the MW data and grades the fit as validation, with abs() on g.
- **Live versus dead:**
  - Live and runnable: the A-115 solvers (static, noncompact, scaling, galaxy validation; the last two depend on `a115_dimensional_source_analysis.py`, which is outside this slice) and the G-764/G-766 sims.
  - Legacy or dead: both algorithm_zero files. The 3D lattice writes to a nonexistent /home/claude path. The emergence printer would crash on the string ratio and is descriptive data only.
- **Out of physics scope:** the G-764/G-766 sims, the council test and bench_assist make no physics claims, and the sims explicitly disclaim them.
