# Code ledger, slice c07 (17 files, all read in full)

Verification note: one scratch-only check was run on copies of `hex_lattice_graph.py` and `discrete_hex_operators.py` (copied to scratchpad/c07chk, PYTHONDONTWRITEBYTECODE=1, nothing written to the repo). Result on disk_sites(2), center site:
- rotational field F=(-y,x): `discrete_divergence` = 1.1547, `discrete_curl_z` = 0.0
- radial field F=(x,y): `discrete_divergence` = 0.0, `discrete_curl_z` = 1.1547
So on this lattice the divergence and curl operators are SWAPPED, and both are scaled wrong: the continuum value is 2, and 1.1547 = 2/sqrt(3). Every Python file below that imports these operators inherits the swap.

---

## /home/user/Builds/Virtual_Breadboard/test/regression-builds/19_three_differential_reference_chain.js
- Purpose / node IDs cited: VBB circuit regression. It tests that three differentials (D1 = DC "BC-DC", D2 = AC "TC-AC", D3 = AC at 90 deg "QC-RC precursor") all refer to one CENTER from a vgnd (lines 3-11, 15-27). No node IDs. Line 11 says plainly: "This does NOT claim a 3D magnetic field. The VBB still lacks Bx/By/Bz."
- Point rotation: not present. The "rotating ELECTRICAL drive vector" (lines 8-9, 55, 107-111) is two quadrature AC sources, i.e. a phasor in voltage space. It carries no L, I or omega.
- Path rotation: not present. Line 21 calls D2 an "out-and-back path", but this is only a label.
- Field: not present.
- Magnetism: not present. Line 11 explicitly disclaims it.
- Parent/child: not present.
- Hard-coded targets / refits: the expected values (1.0 V, 0 V, a 90 deg phase, radius 1 V) are set by the sources themselves (lines 19, 22, 26). The checks confirm the circuit solver reproduces its inputs. This is a self-consistency test, not a prediction.
- Pass criterion: D1 average about 1 V, D2 and D3 means about 0, RMS values match, phase 90 +/- 3 deg, radius error < 0.03 V, CENTER midpoint error < 0.02 V (lines 71-119). It is about electrical reference continuity, not rotation.
- Violations: none. It claims no physics and disclaims B.

## /home/user/Builds/Virtual_Breadboard/test/regression-builds/21_full_mirrored_station_cell_v1.js
- Purpose / node IDs cited: qualifies the CELL_V1 mirror cell: 3 logical gates (G+, G0, G-) built from 12 NMOS, each station tapped to CENTER through a 10 ohm resistor (lines 3-17, 29-53). No node IDs.
- Point rotation: not present.
- Path rotation: not present.
- Field: not present.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none. The "lean" case uses 680 ohm vs 1000 ohm (line 37) to inject imbalance on purpose.
- Pass criterion: OFF leakage < 30 uA (92-95); balanced CENTER at the midpoint within 2 mV with net receipt < 50 uA (96-99); upper and lower currents match per station (104-107); the lean case produces a receipt > 0.5 mA while CENTER holds within 5 mV (113-118); no solver warnings (119-122). These are circuit-balance tests.
- Violations: none.

## /home/user/Builds/Virtual_Breadboard/test/regression-builds/22_bench_reality_guardrails.js
- Purpose / node IDs cited: guardrails that run `js/bench-reality.js` `Bench.audit` against unrealistic breadboard setups (line 4). Cases: dual-rail I0 receipt (79-102); series capacitor faking a center (104-116); dual supply mixed with vgnd (118-123); a 12 V high-side NMOS driven from 5 V GPIO (125-134); a motor driver inside the cell (136-142). No node IDs.
- Point rotation: not present.
- Path rotation: not present.
- Field: not present.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none. The thresholds are engineering limits.
- Pass criterion: audit error codes appear or do not appear as expected (`CENTER_SPINE_SERIES_CAP`, `MIXED_CENTER_TOPOLOGY`, `MOTOR_DRIVER_INSIDE_CELL`, `IMPOSSIBLE_ZERO_SOURCE_RECEIPT`). I0 sign flips with lean direction (100). Vout < 4 V for the 5 V GPIO case (132).
- Violations: none. This file guards against cosmetic passes, which is good practice.

## /home/user/One-Wave-Science/DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/characteristic_equation_solver.py
- Purpose / node IDs cited: a 6x6 "3C + 3R" dynamical matrix on a hex lattice (lines 1-18). It is cited as evidence by C-311 (Nodes/C-311:86-87), C-310 (Nodes/C-310:96) and A-115 (Nodes/A-115:341). It references "Phase 6B".
- Point rotation: not present. "R-field (rotation: magnitude, axis, handedness)" (line 7) is just three abstract matrix components. No omega_body, no L = I omega, no inertia tensor, no axis dynamics. Nothing starts or changes a spin.
- Path rotation: not present.
- Field: there is no curl, wake or chi. The structure factor is a sum over 6 neighbors (lines 69-82).
- Magnetism: R is NOT built from B. The R-R block is a copy of the C-C block: `D_RR = coupling_RR*(6 - D_nn.real)*I` (lines 85-86). The C-R coupling is a constant all-ones block `coupling_CR*0.1*ones` (lines 90-91) with no k dependence. There is no K_L or kappa_R. J_nn and J_nnn are accepted but never used (lines 37-38, 34-99). Gravity is not addressed.
- Parent/child: not present.
- Hard-coded targets / refits: the "unified mode prediction" is `omega_modes[:,0]`, the solver's own first eigenvalue (line 333). It is then compared against the same eigenvalue set (lines 335, 254-262).
- Pass criterion: `prediction_matches = max(min|omega_i - prediction|) < tol` (line 267). Because the prediction is one of the computed eigenvalues, min diff = 0 at every k. The check is TAUTOLOGICAL and always prints "Unified mode prediction VALIDATED" (line 341).
- Violations:
  - characteristic_equation_solver.py:333-341: a self-referential pass is reported as validation of the C-311/A-115 "unified mode". This breaks the evidence rule.
  - characteristic_equation_solver.py:86, 90-91: R is built from nothing physical (a copy of C plus a constant). There is no B to R link (W_B), and "rotation" carries no L. If C-311, C-310 and A-115 cite this as a rotation or magnetism derivation, the evidence does not support it.

## /home/user/One-Wave-Science/DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/discrete_hex_operators.py
- Purpose / node IDs cited: "Track B" discrete div, curl, grad and vector Laplacian on the hex lattice (lines 1-22). Every Maxwell solver imports these.
- Point rotation: not present.
- Path rotation: not present.
- Field: curl `discrete_curl_z` (158-209); divergence (105-151); gradient (216-251); vector Laplacian (258-304); no-monopole check (311-343). There is no chi or wake. BUG: `neighbor_outward_normals` (84-98) rotates each neighbor direction by 90 deg, so its "outward normal" is actually the edge tangent. Divergence then sums the tangential flux, which is circulation. Curl uses t = (n_y, -n_x), which is the radial direction, so it sums outward flux. The scratch check confirmed the two are swapped. Other errors:
  - The cell area is 3*sqrt3/2*a^2 (128, 182). That is the area of a hexagon with side a. The Voronoi cell of a triangular lattice with spacing a has area sqrt3/2*a^2.
  - The edge length used (183) is a, but the true Voronoi edge is a/sqrt3.
  - The gradient leaves out the phi_i term (244-247), so boundary sites are biased.
  - `verify_no_monopole_property` checks div(rot(grad(curl F))) (322-334). That is not div(curl F), and it is the 2D identity applied through the swapped operators.
- Magnetism: not present beyond the "no monopole" label.
- Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: `__main__` prints the div and curl of F = (-y, x) and a boolean no-monopole result (364-397). With the swap, this field reports nonzero divergence and zero curl, the opposite of the docstring claim (365).
- Violations: none against the rotation/magnetism canon directly. This is an infrastructure correctness defect (div and curl swapped, metric constants wrong) that invalidates every downstream "Faraday" figure in this slice.

## /home/user/One-Wave-Science/DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/discrete_maxwell_solver.py
- Purpose / node IDs cited: Track C v1. Steps psi with the update `psi^{n+1} = 2psi^n - psi^{n-1} - gamma(psi^n - psi^{n-1}) + beta[grad(div psi) - curl(curl psi)]` (lines 5-15, 157-160).
- Point rotation: not present.
- Path rotation: not present.
- Field: E is defined as grad(Re psi) (115-119), even though the docstring says grad(div psi). B is defined as the curl of (0, Im psi) (133-141). The update collapses the vector coupling to a scalar: `|grad div| - |grad curl|` (209), which is not the stated operator.
- Magnetism: B is a z-scalar taken from Im(psi). There is no R, K_L or kappa_R, and no link to gravity.
- Parent/child: not present.
- Hard-coded targets / refits: omega_approx = 0.236 "From Phase 6B results" is used to seed psi_1 (323-326).
- Pass criterion: Faraday max error < 0.1 (349).
- Violations: none against the rotation canon. It is dead/legacy and superseded by v2 through v6.

## /home/user/One-Wave-Science/DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/discrete_maxwell_solver_v2.py
- Purpose / node IDs cited: Track C v2, with a "Helmholtz" extraction (lines 1-14).
- Point rotation: not present.
- Path rotation: not present.
- Field: E = grad(div(Re psi, 0)) (68-74). B_z is just curl(Re psi, 0), not a curl of a curl. Lines 104-105 admit this approximation. The update is the same scalar-magnitude coupling as v1 (209-218).
- Magnetism: same as v1. There is no R or K_L.
- Parent/child: not present.
- Hard-coded targets / refits: omega_unified = 0.236039 (246) seeds psi_1 (269-271).
- Pass criterion: < 0.1 prints "approximately satisfied" and < 0.01 prints "SUCCESS" (300-315).
- Violations: none against the rotation canon. Dead/legacy.

## /home/user/One-Wave-Science/DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/discrete_maxwell_solver_v3.py
- Purpose / node IDs cited: Track C v3, with "complex-aware" extraction (lines 1-13).
- Point rotation: not present. A phase gradient rotated by 90 deg is added into E (95-96). This is a phase-vorticity heuristic, not body rotation.
- Path rotation: not present.
- Field: E = grad|psi| + |psi| * rot90(grad arg psi) (81-97). B = Laplacian|psi| + curl(grad arg psi) (104-117). The atan2 phase is not unwrapped (74), so the phase gradients are discontinuous. The update is unchanged from v2: Re-only with scalar magnitudes (201-233).
- Magnetism: B is made from amplitude and phase heuristics. There is no R or K_L.
- Parent/child: not present.
- Hard-coded targets / refits: omega_unified = 0.236039 (259).
- Pass criterion: same thresholds as v2 (313-331).
- Violations: none against the rotation canon. Dead/legacy.

## /home/user/One-Wave-Science/DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/discrete_maxwell_solver_v4.py
- Purpose / node IDs cited: Track C v4, vector psi = (psi_x, psi_y) (lines 1-15). It is cited as evidence by C-311 (Nodes/C-311:86), C-319 (Nodes/C-319:177), C-310 (Nodes/C-310:96) and A-115 (Nodes/A-115:341, "persistent modes"). `faraday_scaling_test.py` and `faraday_scaling_extended.py` import it.
- Point rotation: not present.
- Path rotation: not present.
- Field: E = grad(div psi) (103-104). B_z = -curl(grad(curl psi)) (111-121). In the continuum, the curl of a gradient is zero, so this B is zero by construction plus lattice error. With the swapped operators it becomes an unrelated second-derivative quantity. The update's coupling is `beta*(grad div - grad curl)` (256-261). The docstring says `- curl(curl psi)` (223), but the code subtracts grad(curl), which is not the solenoidal term. Lines 14 and 87 claim Faraday holds "by structure", but the code does not implement that structure.
- Magnetism: B is a scalar z-component from the wrong operator. There is no R, W_B, K_L or kappa_R. Gravity is not addressed.
- Parent/child: not present.
- Hard-coded targets / refits: omega_unified = 0.236039 (292) seeds psi_1 (316-322).
- Pass criterion: Faraday max error < 0.1 or < 0.01 (351-367). The repo's own status docs (PHASE_6B_V5_STATUS and V6 in the same directory, by name) record that this error was about 3.4 or larger (v5 line 300 says "was ~3.4 with asymmetric rule"). So v4 does not pass.
- Violations:
  - Its use as evidence: C-311:86, C-319:177, C-310:96 and A-115:341 cite v4 as validating E/B duality and magnetic reorganization. v4 contains no magnetism-to-lattice-reorganization mechanism, no R built from B, and no point-rotation channel. Its Faraday check fails by the repo's own record, and its operators are swapped.
  - discrete_maxwell_solver_v4.py:256-261 vs 223: the implemented operator differs from the stated rule.

## /home/user/One-Wave-Science/DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/discrete_maxwell_solver_v5_symmetric.py
- Purpose / node IDs cited: Track C v5. Replaces the Helmholtz coupling with the isotropic beta*Laplacian(psi) (lines 1-14, 136-184). Line 10 claims a characteristic equation `lambda^2 - (2-gamma-beta k^2)lambda + (1-gamma) = 0`.
- Point rotation: not present.
- Path rotation: not present.
- Field: the Laplacian is computed as div(grad) per component (35-63) using the swapped operators. In effect it is curl(grad), which is about 0 in the interior, so the beta coupling nearly vanishes. Extraction is the same as v4 (70-94).
- Magnetism: same as v4. There is no R or K_L.
- Parent/child: not present.
- Hard-coded targets / refits: omega_unified = 0.236039 (249) seeds psi_1 (268-276).
- Pass criterion: max error < 1.0 prints "IMPROVED ... Symmetric Laplacian is working!" (299-302). The threshold was loosened from 0.1 (v4) to 1.0. Line 13 claims "Faraday's law ... satisfied automatically", which this pass bit does not show.
- Violations: discrete_maxwell_solver_v5_symmetric.py:13 vs 299. A claim of automatic satisfaction is backed only by a loosened threshold. This is an evidence-gate issue, not a rotation canon issue.

## /home/user/One-Wave-Science/DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/discrete_maxwell_solver_v6_poisson.py
- Purpose / node IDs cited: Track C v6. Extracts Helmholtz parts with a least-squares Poisson solve: lap(phi) = div(psi), E = grad(phi); lap(A) = curl(psi), B = curl(rot A) (lines 1-13, 65-82). It imports v5's evolution (24-28). The docstring is honest: the Laplacian is singular (12), and v5's extraction is "not the Helmholtz parts" (4-6).
- Point rotation: not present.
- Path rotation: not present.
- Field: Poisson solve (52-58), Laplacian matrix built column by column (39-49), residual reported (61-62, 105). It still uses the swapped div/curl from discrete_hex_operators (23, 71, 76, 81).
- Magnetism: B is the z-curl of the solenoidal part. There is no R or K_L.
- Parent/child: not present.
- Hard-coded targets / refits: omega = 0.236039 (114) seeds psi_1.
- Pass criterion: none. It prints V5 vs V6 errors, the Laplacian rank and the Poisson residual for radius 2 and 3 (125-137). It is diagnostic only.
- Violations: none. This is the most honest file in the Track C series. It reports results and asserts no pass.

## /home/user/One-Wave-Science/DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/dispersion_2d.py
- Purpose / node IDs cited: Phase 2 prep, the 2D hex dispersion of the scalar update rule (lines 1-8, 45-91). It corresponds to D-601 (D-601_2D_Hexagonal_Dispersion.md in the same directory).
- Point rotation: not present. "Radial vs rotational" appears only as open questions (214-273).
- Path rotation: not present.
- Field: the hex structure factor S = 2[cos kx + cos(kx/2 - sqrt3 ky/2) + cos(kx/2 + sqrt3 ky/2)] (68-72). BUG: `C_k = 2 - gamma + (beta/6)*S_hex` (79). The correct form is (beta/6)(S_hex - 6). The -beta offset is missing, so at k = 0, C = 2 - gamma + beta instead of 2 - gamma. The rule in the docstring (50) also differs from the 1D form in dispersion_phase1.py.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none. gamma = 0.5 and beta = 0.8 are free (97-98).
- Pass criterion: none. It plots and prints. The final lines (275-276) print check marks unconditionally.
- Violations: none against the rotation canon. It has a math bug at line 79. It writes plots to a foreign absolute scratch path (165, 207), so the script is not reproducible as checked in.

## /home/user/One-Wave-Science/DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/dispersion_phase1.py
- Purpose / node IDs cited: Phase 1, the 1D dispersion of `psi^{n+1} = psi^n + (1-gamma)(psi^n - psi^{n-1}) + beta(<psi_j> - psi^n)` (lines 1-12). It corresponds to D-600 and is related to A-114.
- Point rotation: not present.
- Path rotation: not present.
- Field: `C(k) = 2 - gamma + beta(cos ka - 1)`; lambda^2 - C lambda + (1-gamma) = 0 (28-57). There is no curl or chi.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none. It runs a parameter scan (67-68).
- Pass criterion: it prints stability as |lambda| <= 1 (116-125). There is no claim gate.
- Violations: none. It writes to a foreign scratch path (175).

## /home/user/One-Wave-Science/DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/faraday_scaling_extended.py
- Purpose / node IDs cited: runs the v4 Faraday error for disk radii 1 to 8 and fits a power law (lines 1-7, 29-131).
- Point rotation: not present.
- Path rotation: not present.
- Field: inherits v4 (line 11, wildcard import).
- Magnetism: inherits v4. There is no R or K_L.
- Parent/child: not present.
- Hard-coded targets / refits: omega_unified = 0.236039 (23). The power-law fit uses only the last 3 points (97-114).
- Pass criterion: final max error < 1.0 prints "Faraday constraint satisfied by structure" and "Vector field formulation is theoretically and numerically correct" (140-143). Lines 150-152 print "One-Wave with vector psi describes EM propagation ... Faraday's law is satisfied exactly" UNCONDITIONALLY, whatever the result.
- Violations: faraday_scaling_extended.py:150-152 makes an unconditional claim of exact Faraday satisfaction, and 140-143 make claims of theoretical correctness off a loose threshold. This is an evidence-gate violation.

## /home/user/One-Wave-Science/DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/faraday_scaling_test.py
- Purpose / node IDs cited: the same procedure as the extended test for radii 1 to 4 (lines 1-7, 28-68). It is cited by C-311 (Nodes/C-311:87) and C-319 (Nodes/C-319:177).
- Point rotation: not present.
- Path rotation: not present.
- Field: inherits v4.
- Magnetism: inherits v4.
- Parent/child: not present.
- Hard-coded targets / refits: omega_unified = 0.236039 (23).
- Pass criterion: max error < 1.0 at radius 4 prints "error -> 0 ... satisfied by structure" (88-91). Lines 98-100 print "theoretically correct and numerically converging properly" UNCONDITIONALLY.
- Violations: faraday_scaling_test.py:98-100 makes an unconditional correctness claim. It is cited by C-319:177 as support for magnetic lattice reorganization, but it contains no magnetism-to-organization mechanism.

## /home/user/One-Wave-Science/DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/hex_lattice_graph.py
- Purpose / node IDs cited: "D1", a 2D triangular/sixfold graph on the D-408 lattice (lines 1-12). It provides neighbors, axis pairs (3:1), the seven-cell, disks, incidence matrix, graph Laplacian and a Jacobi eigen-solver (22-154). Line 10-11: "not a 3D or 4D object and it is not a Mass Effect derivation."
- Point rotation: not present.
- Path rotation: `directed_routes` (145-146) lists the 6 neighbor routes. This is graph topology only and carries no L.
- Field: graph Laplacian L = D - A (93-104). It is correct.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: none. It is a library.
- Violations: none. It is correct and honestly scoped.

## /home/user/One-Wave-Science/DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/maxwell_validation.py
- Purpose / node IDs cited: "Phase 4" Maxwell validation of E-like (longitudinal) and B-like (transverse) modes (lines 1-15). It imports `vector_field_framework` (line 228), which is outside this slice.
- Point rotation: not present.
- Path rotation: not present.
- Field: numpy finite-difference curl and div on a square grid (88-110). It does not use the hex operators.
- Magnetism: the test wave is built BY HAND: Ex = 0, Ey = cos(kx), Bx = By = 0, Bz = cos(kx)/c_eff (179-208). The tests that follow are therefore true by construction:
  - div B uses only (Bx, By) = 0, so it is exactly 0 (346-348).
  - div E of Ey(x) is exactly 0 (353-356).
  - Faraday compares curl E with a hand-written -k(omega/c_eff) sin(phase) using a correlation coefficient that ignores amplitude (372, 380-382).
  The plasma fit labels the slope "v_s^2 k^2" but fits linearly in k, not k^2 (304 vs 316). There is no R or K_L. Line 424 lists "Compute strong/weak/gravity coupling from same framework" as a next step. It is a proposal only, with no B to gravity code.
- Parent/child: not present.
- Hard-coded targets / refits: the E and B fields are constructed so that they satisfy Maxwell's equations, and the script then reports "Faraday's law satisfied" and "No magnetic monopoles" (407-415). Lines 422-425 plan to fine-tune (gamma, beta) "to match physical constants".
- Pass criterion: monopole RMS < 1e-6, correlation > 0.95, transverse v_p variation < 10% (269, 397-415). The Maxwell checks are tautological. Only the velocity and plasma checks touch the One-Wave dispersion.
- Violations:
  - maxwell_validation.py:340-415: a hand-built Maxwell-consistent wave is reported as One-Wave satisfying Faraday's law and no-monopoles. This is circular.
  - maxwell_validation.py:304: the fit form does not match the stated relation.

---

## Slice summary

Point rotation: NO file in this slice implements point rotation, canonically or otherwise. None has omega_body, L = I omega, an inertia tensor, attitude, a spin-preservation rule, an open/closed magnetic switch (dL/dt = 0 vs -gamma L), parent/child transport, a K_L or kappa_R gravity coupling, or bound-lattice locking (no Moon 1:1, no Mercury 3:2). Files 19, 21 and 22 are VBB circuit tests. The Python files are Phase-1/Phase-6B dispersion and E/B extraction experiments.

Non-canonical "rotation" and "magnetism" terms in this slice:
- characteristic_equation_solver.py: an "R-field (rotation)" is three abstract components whose block is a copy of the compression block (86), with constant cross-coupling (90-91). R is not built from B, so it has no W_B = B(x)B - |B|^2 I/3, and it carries no L.
- Track C v1 to v6: "B" is a z-scalar from lattice operators that are swapped and wrongly scaled. There is no magnetism-to-lattice (R) or gravity (K_L) path, which is consistent with the canon's "magnetism does not become gravity", but only because nothing is attempted.

Violations (evidence and citation, not rotation-law):
1. characteristic_equation_solver.py:333-341: the "unified mode prediction" is its own eigenvalue, so the pass is tautological. It is cited by C-311:86-87, C-310:96 and A-115:341.
2. discrete_hex_operators.py:84-98, 128, 182-183, 203: divergence and curl are swapped (verified numerically) and the cell area and edge length are wrong. Every Track C Faraday number and the "no monopole" check inherit this.
3. discrete_maxwell_solver_v4.py:223 vs 256-261: the stated operator `- curl(curl psi)` is implemented as `- grad(curl psi)`. B = -curl(grad(curl psi)) (111-121) is zero in the continuum. v4 is cited by C-311:86, C-319:177, C-310:96 and A-115:341 as validating E/B duality, magnetic lattice reorganization and persistent modes. It contains none of those mechanisms, and its Faraday error is about 3.4 by the repo's own record (v5:300).
4. discrete_maxwell_solver_v5_symmetric.py:13 vs 299: it claims "satisfied automatically" but passes on a loosened < 1.0 threshold. Its Laplacian is curl(grad), about 0, because of the swap.
5. faraday_scaling_test.py:98-100 and faraday_scaling_extended.py:150-152 print claims of "theoretically correct" or "satisfied exactly" UNCONDITIONALLY. faraday_scaling_test.py is cited by C-311:87 and C-319:177.
6. maxwell_validation.py:179-208, 340-415: a hand-built Maxwell wave is reported as One-Wave passing Faraday and no-monopoles. The fit form is wrong (304). Line 424 proposes gravity coupling from this framework (proposal only).
7. dispersion_2d.py:79: the -beta term is missing from C_k. This is a math bug, not a canon violation.
8. Hard-coded omega = 0.236039 "from Phase 6B" seeds psi_1 in v1 to v6 and both scaling tests. It is used as an initial condition, not reported as a prediction.

Live vs dead:
- Live VBB regression tests: 19, 21 and 22 (Builds). They are sound and claim no physics.
- Library: hex_lattice_graph.py (correct). discrete_hex_operators.py is live, imported by all Track C files, but defective.
- Cited-as-evidence (effectively "live" in the node graph): characteristic_equation_solver.py, discrete_maxwell_solver_v4.py and faraday_scaling_test.py. All three are cited by C-311, C-319, C-310 and/or A-115, and all three are defective as evidence.
- Latest diagnostic: discrete_maxwell_solver_v6_poisson.py. It is honest and makes no pass claim.
- Dead/legacy: discrete_maxwell_solver.py, v2 and v3 (superseded), dispersion_phase1.py and dispersion_2d.py (Phase-1/2 exploration with foreign output paths), faraday_scaling_extended.py and maxwell_validation.py (Phase 4; depends on vector_field_framework.py outside the slice).

Cross-references outside the slice that matter: Nodes/C-311:86-87, Nodes/C-319:177, Nodes/C-310:96 and Nodes/A-115:341 cite these files. vector_field_framework.py, the PHASE_6B_*_STATUS.md files, D-600, D-601, D-602 and solvers/maxwell_validator.py sit in or near this directory but are outside the slice.
