# Code ledger — slice c01

Files read in full: 10 / 10. Repo: /home/user/Builds (Miniverse room3d + Virtual_3D_Electronics). No repo edits, nothing run.

## /home/user/Builds/Miniverse/room3d/app.js
- Purpose / node IDs cited: Three.js browser view of the Miniverse "SANDBOX" room: 37-cell hex lattice tiles, workbenches, voxel avatars, chat/bench/experiment panels; polls `/api/state` every 700 ms (L140-144). No node IDs cited.
- Point rotation: not present. Avatar parts carry a static Euler `rotation` triple from the body spec (L75-83, L100) that is set once and never integrated; no spin, omega, L or attitude state. Benches use `g.lookAt(0,…,0)` (L61), which is a display orientation only.
- Path rotation: not present. Avatars move by `position.lerp` toward a target cell (L114, L167); keyboard moves along six lattice axes (L162-163). Camera `OrbitControls` (L19) is a viewer control, not physics.
- Field: not present (lattice tiles are colored by zone kind only, L63-69).
- Magnetism: not present.
- Parent/child: Three.js scene-graph nesting (part mesh in avatar group, L91-106) composes transforms by the library. These are static display transforms, not rates.
- Hard-coded targets / refits: none (experiment defaults L147 mirror server defaults).
- Pass criterion: none (UI only).
- Violations: none.

## /home/user/Builds/Miniverse/room3d/lattice_body_physics.py
- Purpose / node IDs cited: "Reduced lattice-body sandbox". Bodies put load on lattice sites. The stationary triangular lattice stores scalar displacement/compression and relaxes through neighbor coupling (docstring L2-8). It cites D-412 simulation governance and says it does "not claim physical validation of One-Wave gravity or CELL_V1" (L7-8). It is NOT imported by server.py. The only importer is test_lattice_body_physics.py (outside this slice), so it is a standalone or legacy module and not part of the live room.
- Point rotation: not present. `CellState` (L16-22) and `BodySense` (L24-33) have no spin, omega, L or attitude.
- Path rotation: not present (bodies sit on a cell; no motion is computed here).
- Field: scalar only. Per-cell `u, v` displacement integrated with neighbor-mean restoring force `stiffness*(nbr_u - u)` (L68), load force `-s.load` (L69), damping and multiplicative `retention` (L70-72). `chi = max(0, -u)` (L73), so chi is compression from negative displacement. `strain` = mean |u - u_nbr| (L75). `pressure = load + chi + stiffness*strain` (L76). No curl, no wake, no vector grad chi.
- Magnetism: not present (no B, R, K_L or kappa_R).
- Gravity analogue: `weight_signal = mass*(1 + pressure)` (L89) and `support = 1/(1+|u|+strain)` (L86). Weight comes from the local scalar pressure, which includes the body's own load, and NOT from a gradient. On a uniformly compressed patch (grad chi = 0) weight_signal is still > mass. Mass = part volume × scale³, clamped 0.1-20 (L41-51).
- Parent/child: not present.
- Hard-coded targets / refits: none. Constants stiffness 0.34, damping 0.18, retention 0.92, dt 0.2 (L36) are free tuning values.
- Pass criterion: none in the file (tests are outside the slice).
- Violations:
  - L89 (with L76): the gravity-like "weight" is built from local scalar pressure (load + chi + strain), not from a gradient as in g = -alpha K_L grad chi. It does not give g = 0 when grad chi = 0. This is mitigated by the L7-8 disclaimer (software coordination model only, not One-Wave gravity). Classify as a soft conflict if the module is ever presented as a gravity model.
  - L71-72: the `retention` multiplier is an unattributed loss of lattice displacement energy every step. It is a field-side detail, not an L violation.

## /home/user/Builds/Miniverse/room3d/server.py
- Purpose / node IDs cited: Shared Miniverse room runtime. One persistent JSON world state feeds the AI bridge and the 3D view. "The lattice is stationary. Agent bodies move through legal lattice edges" (L2-7). HTTP API covers join, ping, move, say, body, experiment create/run/result, bench (L578-631). No node IDs cited. This is the LIVE room server (it does not import lattice_body_physics.py).
- Point rotation: not present. `facing` (L237, L275) is a discrete axis label that is overwritten with the last move direction. It is a heading set by the path, not a carried spin. Body part `rotation` is a validated static Euler triple in ±6.3 rad (L158).
- Path rotation: discrete hops along manifest neighbor edges (L264-284). They carry no L or rate.
- Field: `_run_lattice_pulse` (L375-408): scalar graph diffusion `mixed = v + coupling*(mean_nbr - v)`, then `*= retention`. It is labeled "abstract_graph_signal_spread" with the claim boundary "Software graph experiment; not a physical One-Wave validation." (L407). No curl or grad chi.
- Magnetism: not present.
- Decay model: `_run_reference_recovery` (L410-428) runs `value *= retention` per step, a scalar exponential relaxation toward Baseline Zero. It is not L and not a magnetic channel. It is labeled "not a physical validation" (L427).
- Parent/child: not present.
- Hard-coded targets / refits: none. Experiment defaults L31-42. External results are stored as receipts with "source evidence must be checked separately" (L491).
- Pass criterion: no physics pass bit. Runs are marked `status: "COMPLETE"` unconditionally (L448, L488). The `settled` measurement is `|value| <= tolerance` (L417).
- Violations: none.

## /home/user/Builds/Miniverse/room3d/test_room_server.py
- Purpose / node IDs cited: unittest for server.WorldStore. It checks the 37-cell / 7-zone manifest, baseline "0,0" and six axes (L17-21), edge moves and boundary rejection (L22-29), persistence (L30-57), invalid shape rejection (L59-72), the lattice_pulse run (L74-92), reference_recovery settling (L94-105), external receipts (L107-120), parameter validation (L122-129) and HTTP health (L131-140).
- Point rotation: not present.
- Path rotation: only lattice-edge moves (L22-29).
- Field: lattice_pulse spread > 1 active cell (L88).
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none. Test values are self-chosen software parameters.
- Pass criterion: software behavior: persistence, validation, settling under tolerance (L103-105), active cells > 1. No physics claim.
- Violations: none.

## /home/user/Builds/Virtual_3D_Electronics/js/catalog.js
- Purpose / node IDs cited: Real-part data catalog: ferrite and permalloy materials (L43-54), square-loop hysteresis shape constants (L59-60), diodes (L66-70), MOSFETs (L76-87) with EKV fits (L148-155), capacitor classes (L90-95), NEMA AWG table (L101-126), design limits (L129-141), and a per-field VERIFICATION record (DATASHEET/FIT/CLASS/ASSUMPTION, L157-199). No One-Wave node IDs.
- Point rotation: not present.
- Path rotation: not present.
- Field: not present (no One-Wave field). `MU0 = 4e-7*pi` (L38).
- Magnetism: conventional material data only (mu_i, Bsat, Br, Hc, switching coefficient). No R, K_L or kappa_R. No coupling to gravity.
- Parent/child: not present.
- Hard-coded targets / refits: MOSFET `vt0, beta, n, rd` are FITTED to datasheet points (L148-155), and the tests "re-check the fit against those points" (L31-33). That is a re-check against the fitting data, not an independent prediction. It is disclosed as FIT in VERIFICATION (L178-184), so it is not presented as a prediction. Iron-powder `rolloffOe` 53 is fitted to two catalog points (L47-51, disclosed).
- Pass criterion: none here (data).
- Violations: none against the One-Wave canonical rules (out of domain).

## /home/user/Builds/Virtual_3D_Electronics/js/parts.js
- Purpose / node IDs cited: General part geometry: core normalisation, validation, wall/web checks and derived magnetic path lengths. It uses IEC 60205 toroid effective parameters (L405-441), winding leg selection with aperture threading (L474-517), and world/local transforms (L248-277). No node IDs.
- Point rotation: not present. `rotate`/`unrotate` (L248-268) apply a fixed Euler XYZ (degrees) placement of a part. It is static orientation, not a rate.
- Path rotation: not present.
- Field: not present (no One-Wave field). The magnetic path length `le`, `Ae` and `AL = mu0*mui*Ae/le` (L434) are classical magnetic-circuit quantities.
- Magnetism: only classical magnetic-circuit geometry. No R tensor, K_L or kappa_R. No gravity.
- Parent/child: `toWorld` = R·local + position (L269-273) is a single-level static transform. No rate transport is needed or present.
- Hard-coded targets / refits: none.
- Pass criterion: `validateCore` PASS when shape, outer size, thickness, material, apertures, outer walls and webs all meet `minWallMm` (L359-402).
- Violations: none.

## /home/user/Builds/Virtual_3D_Electronics/js/physics.js
- Purpose / node IDs cited: "Reality judge for any assembly" (L1-26). It runs strict field checks, core/pad/lead/winding/fill/intersection checks (L102-245), then DC Newton or transient circuit solves through circuit.js and magnetics.js (outside this slice; L30-33, L329-462). It applies ratings (L466-507), runs the static Ampere check per path (L510-566) and checks expect[] claims (L569-611). Status: "MODELED (nominal datasheet values, not bench)" (L613). No One-Wave node IDs.
- Point rotation: not present. Part rotation is static placement only (via parts.js).
- Path rotation: not present.
- Field: not present (no One-Wave field). Classical `H = N*I / l` (L519, L536). Linear `B = min(mu0*mui*|H|, Bsat)` (L531, L555). Square-loop switching when `|H| >= Hc` (L522, L539).
- Magnetism: classical EM only. B is built from H via the material model. No R = W_B construction, no K_L, no kappa_R. Magnetism is never routed into gravity. Core remanence is carried between runs via `coreState` (L367-383, L460), "a real core remembers". This is a memory of state, not L.
- Energy bookkeeping: transient run FAILs if the source EMF energy differs from absorbed energy by >1% (L428-438). The core energy from windings must equal ∫H dB within 2% (L439-444). This is conservative bookkeeping, consistent in spirit with the "no exception to bookkeeping" rule.
- Parent/child: not present.
- Hard-coded targets / refits: none in the solver. `expect[]` values are user claims checked against computed results, and a wrong claim FAILs (L605-610). The MOSFET body diode `is: 1e-12, n: 1.2` is hard-coded (L307) and recorded as ASSUMPTION in the catalog (L197).
- Pass criterion: `ok` stays true only if no FAIL receipt is recorded: structural, rating, convergence, energy-closure or claim failures each set FAIL (L105, L612-614). This is an electrical/magnetic engineering pass. It has nothing to do with point rotation or spread.
- Violations: none against the One-Wave canonical rules (out of domain).

## /home/user/Builds/Virtual_3D_Electronics/js/ui-form.js
- Purpose / node IDs cited: Pure mapping between the human part form and the part spec, so that form output equals AI JSON (L1-84). No node IDs.
- Point rotation: not present. `rx/ry/rz` map to the static core rotation (L52, L73-74).
- Path rotation: not present. Field: not present. Magnetism: not present. Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: none (tested in api.test.js).
- Violations: none.

## /home/user/Builds/Virtual_3D_Electronics/js/world.js
- Purpose / node IDs cited: Assembly/world state, with place, update, duplicate, remove, export and load (L1-89). `coreState` holds remanent magnetization carried between runs (L5-7, L24, L70, L80). No node IDs.
- Point rotation: not present. Static rotation defaults (L40).
- Path rotation: not present. Field: not present.
- Magnetism: only stores and carries `coreState` (remanence persistence). No B-to-gravity link.
- Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: none.
- Violations: none.

## /home/user/Builds/Virtual_3D_Electronics/test/api.test.js
- Purpose / node IDs cited: Node test that checks that human form parts equal AI JSON parts (L18-32), catalog surface (L10-16), place/duplicate/update/load/export and analysis persistence (L34-50). It depends on `_check.js` and `ai-api.js`, both outside this slice.
- Point rotation: not present (only static `rotation` objects in fixtures, L20).
- Path rotation / Field / Magnetism / Parent-child: not present.
- Hard-coded targets / refits: none (fixture values only).
- Pass criterion: structural equality and API behavior checks.
- Violations: none.

## Slice summary
- Point rotation: no file in this slice represents point rotation (spin, omega, L, inertia axes) at all. Everything named "rotation" is a static Euler placement: app.js L100, server.py L158, parts.js L248-277, ui-form.js L52, world.js L40. `facing` in server.py (L237, L275) is a discrete heading set by the last path move. It is not a carried point rate. No file starts, changes or damps spin, so none violates the "does not start one on its own" or open/closed magnetic switch rules. None implements them either.
- Path: Miniverse agents hop along stationary lattice edges (server.py L264-284) with display lerp (app.js L167). No L is carried.
- Field: scalar-only lattice models. lattice_body_physics.py has chi = max(0,-u) compression (L73) and pressure (L76). server.py lattice_pulse diffusion (L375-408) and reference_recovery decay (L410-428) carry explicit "not a physical validation" boundaries. There is no curl, no wake and no vector grad chi anywhere.
- Magnetism: only classical EM in Virtual_3D_Electronics (H = NI/l, B = mu0 mui H, square-loop Hc switching, remanence persisted via coreState). No R, W_B, K_L or kappa_R anywhere. Magnetism never feeds gravity.
- Violations / conflicts:
  1. lattice_body_physics.py L89 (with L76): `weight_signal = mass*(1+pressure)` derives weight from local scalar pressure/compression, not from grad chi, so the weight is nonzero when grad chi = 0. This conflicts with g = -alpha K_L grad chi, grad chi = 0 -> g = 0. It is softened by the L7-8 disclaimer that it is a software coordination model, not One-Wave gravity.
  2. No other canonical-rule violations. The Virtual_3D_Electronics files are classical electronics, outside the One-Wave domain. Their FIT parameters (catalog.js L148-155) are disclosed as fits and are not reported as predictions.
- Live vs dead / legacy:
  - Live: server.py is the live room runtime with app.js as its front end, and test_room_server.py tests them.
  - Standalone: lattice_body_physics.py is not wired into server.py. Only test_lattice_body_physics.py imports it, and that test is outside this slice.
  - Live (separate app): physics.js, parts.js, catalog.js, world.js, ui-form.js and api.test.js are the live Virtual_3D_Electronics stack. physics.js depends on magnetics.js, circuit.js and ai-api.js, which are outside this slice.
- Cross-references outside slice: D-412 (lattice_body_physics.py L7). Also Builds/Miniverse/room3d/test_lattice_body_physics.py, room_manifest.json, Virtual_3D_Electronics/js/magnetics.js, circuit.js, ai-api.js, test/_check.js and PARTS_AUDIT.md.
