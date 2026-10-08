# Code ledger — slice c24

## /home/user/One-Wave-Science/test_algorithm_zero_phase3_pressure_tensor.py
- Purpose / node IDs cited: pytest suite (474 lines) for `solvers/algorithm_zero_phase3_pressure_tensor.PressureTensorLattice` (import L18), "Algorithm Zero Phase 3" galaxy rotation-curve pressure-tensor lattice. No node IDs (C-/G-/E-/A-) cited anywhere. Docstring target "30+ tests, all passing" (L13).
- Point rotation: not present. No spin / omega / L / attitude / inertia anywhere in the test. "Rotation" here means only galaxy tangential orbital velocity (path-type) extracted from a pressure field. No start/change mechanism, no gravity or compression-gradient effect on spin, no open/closed magnetic switch, no parent organization target rate.
- Path rotation: galaxy rotation curve `measure_rotation_velocity()` -> `radii_kpc`, `rotation_velocities_km_s` (L223, L231, L248-253, L262-265, L272-282, L291-292, L382-386, L399-403, L419-427). Derived from a 6-component pressure tensor (L41) plus mass density/gradient (L52-75), "tangential pressure (drives rotation)" (L429-441). Carries no L; no angular-momentum bookkeeping at all.
- Field: pressure tensor shape (6,32,48,16) (L41-42); `inject_pressure_wake(amplitude)` (L90, L126, ...) is a "wake" injection; `grad_rho` mass gradient (L73-75). No curl, no chi, no grad chi.
- Magnetism: not present (no B, R, K_L, kappa_R).
- Parent/child: not present.
- Hard-coded targets / refits: parameters asserted fixed gamma=0.05, beta=0.15 (L35-36; "gamma" here is a damping constant, not magnetic closed-channel gamma). Physical velocity window 20-400 km/s asserted (L264-265, L338, L426-427: v_min>20, v_max>80). The solver itself clips v_rotation to [20, 400] (solvers/algorithm_zero_phase3_pressure_tensor.py:320), so L264-265 and L426 are guaranteed by construction, not predictions. Grid dims 32/48/16 asserted (L28-30).
- Pass criterion: finiteness/stability (L80-81, L102, L111-112, L364), "pressure changes"/"curves differ" (L94, L237, L282, L386), shape/key presence (L41, L250-253, L305-319, L454-469), loose bounds (L135, L172 `max_sat < 2*max_linear`, L198-199 `<100`, L403 std>1, L441 >0.01), and clipped velocity window. Pass bit is neither point rotation nor spread; it is "runs, stays finite, produces a different-looking curve in a clipped range". No comparison to observed rotation curves.
- Violations:
  - L264-265, L426-427 (with solver :320): velocity range "physical" check is a tautology because the solver clamps output to [20,400]; an imposed observed-galaxy window reported as a result (hard-coded target / refit pattern).
  - L429-441 / L223-237: galaxy rotation driven by "tangential pressure" with no Point/Path/Field split and no L = I omega; per canonical rule 1 the node is incomplete (Path only, Point and field curl absent). Not a direct contradiction of magnetism/gravity rules since those are absent.
  - Gravity here is implicit via mass density gradient (L70-75) feeding the pressure field, not g = -alpha K_L grad chi; no chi channel, so no A-115/K_L check is possible (absence, not explicit conflict).

## Slice summary
- Canonical point rotation: none. The single file has no point-spin representation.
- Violations: test_algorithm_zero_phase3_pressure_tensor.py — rotation-curve range assertions are tautological against the solver's np.clip(20,400) (solver L320); rotation modeled as pressure-driven path velocity only (no Point L, no field curl), so the node is incomplete under the Point/Path/Field rule; no node IDs cited.
- Live vs legacy: this is a legacy/exploratory "Algorithm Zero Phase 3" galaxy test at repo root; target solver exists at solvers/algorithm_zero_phase3_pressure_tensor.py. Not part of the canonical Point/Path/Field or K_L gravity solvers. Not executed for this ledger (read-only audit).
