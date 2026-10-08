# Code ledger, slice c11 (17 files, all read in full)

Repo: /home/user/One-Wave-Science. No repo edits were made. No code was run. The only extra read was a grep of `Nodes/D-413_Ground_Lattice_Orbital_Restoring_Simulation/simulate_d413.py`, to see what `run_experiment.py` imports.

---

## One_Wave_Bench/engine/electrical/nerve_gate_resonance.py
- **Purpose / node IDs cited:** a PID "nerve-gated" three-phase gate controller. It holds V_0 at 2.5 V and tracks a "resonance" ω₀. No node IDs are cited. It names "Algorithm Zero" six-step phases (L25-36) and the M1–M4 levels (L86-90).
- **Point rotation:** not present. "M1 (Point)" is a node voltage V_0 (L95-97), not a spin, ω, L or attitude. `omega_gate` (L52) is a gate drive frequency, not a body rate. Nothing starts it inside the module; the `__main__` demo sets it from a sine (L387). There is no gravity or compression term. γ (L44) is a resonance damping factor that only feeds `q_factor = 1/γ` (L66). It is not a magnetic open/closed switch. There is no parent organization rate.
- **Path rotation:** "M2 (Path)" means gate voltages and frequencies (L99-101). There is no orbit or ride, and no L is carried.
- **Field:** "M3 (Field)" means resonance amplitude = |V_0 − 2.5| and energy = amplitude² (L322-326). There is no curl, wake, χ or ∇χ.
- **Magnetism:** not present. The docstring says "Gates drive rotating Maxwell field" (L13), but no B, R, K_L or κ_R exists. The "three-phase mirror" is `control*cos(offset)` (L174). V (120°) and W (240°) both get cos = −0.5 and so receive identical voltages. This is not a rotating three-phase field.
- **Parent/child:** not present.
- **Hard-coded targets / refits:** V target 2.5 V (L239). ω₀ = c_L·k·√(β/2) comes from defaults (L64). The 50 mV / 100 mV "biological" window is hard-coded (L136-144). These are circuit set-points, not physical observables reported as predictions.
- **Pass criterion:** none. The demo only prints.
- **Violations:** none against the physics rules, because the module has no physical point rotation. Labelling note: M1 "Point" = voltage, M2 "Path" = gate, M3 "Field" = resonance (L86-90). This reuses the Point/Path/Field words without the canonical meaning (Point rotation carries L = Iω). Code defects: "frequency_error" is actually a V_0 voltage error (L244), and ω₀ never enters gate control (L264-288). The V and W phases collapse into each other (L174).

## One_Wave_Bench/engine/electrical/p0_hexagon_correct.py
- **Purpose / node IDs cited:** builds a hexagon netlist of PMOS/NMOS half-bridges. Its three phases A/B/C run through a buffered "nucleus" virtual ground. No node IDs are cited.
- **Point rotation:** not present. The circuit has inductor currents only (L148-155).
- **Path rotation:** not present.
- **Field:** not present.
- **Magnetism:** not present. Windings are lumped L+R (L117-144) with no mutual coupling and no B.
- **Parent/child:** not present.
- **Hard-coded targets / refits:** none. Defaults are 5 V supply and Vth 1 V. The docstring claims a 0.5 V neutral gate (L21). That holds with Vth = 1 V and a 2.5 V nucleus.
- **Pass criterion:** none. This is a builder only.
- **Violations:** none.

## One_Wave_Bench/engine/electrical/p0_hexagon_direct.py
- **Purpose / node IDs cited:** the same hexagon, with a "star_ground" 0.50 V reference at a 1 V supply. The docstring says it is an "active ternary leaning" nucleus with A=state/DC, B="rotation/AC", C=gradient/RC (L18-24). No node IDs are cited.
- **Point rotation:** not present. "B mode (rotation/AC)" (L21) is a label only, with no code.
- **Path rotation:** not present.
- **Field:** not present. "C mode (gradient)" is a label only.
- **Magnetism:** not present.
- **Parent/child:** not present.
- **Hard-coded targets / refits:** 0.50 V "biological baseline" (L172). This is a set-point.
- **Pass criterion:** none.
- **Violations:** none. The "leaning" nucleus described in the docstring is not implemented: the reference is a passive divider plus buffer (L69-94).

## One_Wave_Bench/engine/electrical/p0_hexagon_final.py
- **Purpose / node IDs cited:** the hexagon with separate gates (`gate_X_hs`, `gate_X_ls`) for each PMOS/NMOS pair (L91-110). Nucleus at V/2. No node IDs are cited.
- **Point rotation / Path rotation / Field / Magnetism / Parent/child:** all not present. Windings are lumped L+R (L119-146).
- **Hard-coded targets / refits:** none.
- **Pass criterion:** none.
- **Violations:** none.

## One_Wave_Bench/engine/electrical/p0_hexagon_hbridge.py
- **Purpose / node IDs cited:** the hexagon with Drive, Memory and Sense windings per phase and a separate DC_LINK capacitor. It cites "UPDATED_63" (L18, L23) for the 18-terminal fixture and H-bridge layout.
- **Point rotation:** not present.
- **Path rotation:** not present.
- **Field:** not present.
- **Magnetism:** not present. The "Memory" winding is described as state retention (L188), but it is an L+R branch to VREF with no magnetic core, no hysteresis, no B and no mutual inductance (L191-215). Its external terminals `memory_X_*_ext` are left floating; no nerve ring is wired here (L190, L213).
- **Parent/child:** not present.
- **Hard-coded targets / refits:** 0.50 V baseline (L258). DC_LINK starts at 0 V in `cap_states` (L247) but at 0.50 V in the node voltages (L264), which is inconsistent.
- **Pass criterion:** none here. It is driven by `test_hbridge_ab_transfer.py`.
- **Violations:** none against the physics rules. The docstring says "full reversible H-bridge (not a half-bridge)" (L24-25), but the code builds half-bridges (L128-149, "for now").

## One_Wave_Bench/engine/electrical/p0_hexagon_hbridge_independent.py
- **Purpose / node IDs cited:** an independent HS/LS-gate hexagon with Drive, Sense and Memory windings, plus a "nerve ring" from A_sense to B_memory through 10 kΩ (L252-267). Cites the 18-terminal fixture.
- **Point rotation / Path rotation / Field / Magnetism / Parent/child:** all not present. Memory is again L+R only, with no magnetic state variable (L225-250).
- **Hard-coded targets / refits:** 0.50 V baseline. Gate levels 0.9 V and 0.2 V (L311-312).
- **Pass criterion:** none here.
- **Violations:** none against the physics rules. Code defects:
  - The `__main__` printout says "1kΩ coupling" (L329), but `r_nerve` is 10 kΩ (L255).
  - The initial-voltage keys `f"{winding_type}_{phase}_{half}_mid"` (L302) do not match the real node names (`mid_A_drive_pos`, `sense_A_pos`, `memory_A_pos_mid`). The drive midpoint nodes are therefore never initialised.

## One_Wave_Bench/engine/electrical/p0_hexagon_working.py
- **Purpose / node IDs cited:** the "working baseline" hexagon with a pre-wired 10 kΩ nerve ring from A_sense to B_memory (L220-235). The docstring claims B→C and C→A links as well (L19-21), but only A→B is wired.
- **Point rotation / Path rotation / Field / Magnetism / Parent/child:** all not present.
- **Hard-coded targets / refits:** 0.50 V baseline. The sense inductance is L/10 (L170).
- **Pass criterion:** none here. It is driven by `test_working_ab_transfer.py`.
- **Violations:** none against the physics rules. The docstring-to-code mismatch on the ring is noted above.

## One_Wave_Bench/engine/electrical/p0_hexagonal_circuit.py
- **Purpose / node IDs cited:** a flat-edge hexagon "transfluxor". The docstring labels A=state/temperature DC, B="rotation/gyro, AC", C=gradient RC (L9-11). No node IDs are cited.
- **Point rotation:** not present. "rotation/gyro" is a label only.
- **Path rotation / Field / Magnetism / Parent/child:** not present. "Transfluxor" implies a magnetic core, but none is modelled.
- **Hard-coded targets / refits:** none.
- **Pass criterion:** none.
- **Violations:** none against the physics rules. Code defect: both FETs are NMOS and share one gate (L97-116), so the high-side and low-side switches turn on together (shoot-through).

## One_Wave_Bench/engine/electrical/simulate_nerve_gated_cell.py
- **Purpose / node IDs cited:** runs the closed-loop P0TernaryCircuit together with NerveGateResonanceTuner. The docstring claims it "Displays cascading effects (point → path → field rotations)" (L9, L268). No node IDs are cited.
- **Point rotation:** not present. Nothing in the code is a rotation state. `omega_gate` is changed by `omega_gate += 0.01 * frequency_error` (L129-132). Because `frequency_error = |ω₀ − ω_gate|` is an absolute value (nerve_gate_resonance L320), ω_gate only ever increases and never tunes toward ω₀.
- **Path rotation:** not present.
- **Field:** `field_energy` = mean of the squared gate voltages (L212). `three_phase_balance` = |Σ cos(φ_i)·gate_i| (L193-196). Neither is curl, χ or ∇χ.
- **Magnetism:** not present.
- **Parent/child:** not present.
- **Hard-coded targets / refits:** V_0 target 2.5 V (L202, L244-248). Gain-50 mapping from nerve signal to gate voltage (L144).
- **Pass criterion:** "✓ STABLE" if the maximum V_0 error is below 0.01 V (L248). This is voltage regulation, not rotation or spread.
- **Violations:**
  - Physics: none, because there is no physical rotation.
  - Claims not backed by code: the "point → path → field rotations" claim (L9, L268) has no implementation. The ω tuning law diverges (L129-132).
  - Defaults are inconsistent: 0.05 in L164-166 versus 2.5 in L186-188.
  - Output is written to /tmp (L301), outside the repo.

## One_Wave_Bench/engine/electrical/test_hbridge_ab_transfer.py
- **Purpose / node IDs cited:** "First Hard Criterion" from UPDATED_63, step 4: "B retains a changed magnetic state" (L9).
- **Point rotation / Path rotation / Field:** not present.
- **Magnetism:** the "magnetic state" is read as the node voltage `memory_B_pos_ext` (L77, L127). In `p0_hexagon_hbridge` that terminal is floating and not wired to A, and there is no magnetic variable.
- **Parent/child:** not present.
- **Hard-coded targets / refits:** the drive gate level is fixed at 0.9 V (L93). The `drive_voltage` argument is never used (L37), so the "sweep" over 0.5–1.0 V (L209) runs the same test six times.
- **Pass criterion:** PASS if peak A activity > 0.01 V, B change > 0.01 V and |retention| > 0.005 V (L177).
  - `drive_current_history` is only appended inside `if len(drive_current_history) > 0` (L133-135). It therefore stays empty, `peak_drive_activity` is always 0, and the test can never PASS or even be UNCERTAIN. It always FAILs.
  - "Retention" is the last sample minus the baseline at t = 210 µs. Nothing checks that the transient has died.
- **Violations:** none against the physics rules. Test defects: the test is structurally unable to pass (L133), its sweep parameter is dead (L37), and it labels a voltage as a "magnetic state" (L9).

## One_Wave_Bench/engine/electrical/test_hbridge_independent_ab_transfer.py
- **Purpose / node IDs cited:** the same UPDATED_63 A→B criterion, using independent HS/LS gates.
- **Point rotation / Path rotation / Field:** not present.
- **Magnetism:** the "magnetic state" is again a node voltage, `memory_B_pos_in` (L66, L148). There is no B.
- **Parent/child:** not present.
- **Hard-coded targets / refits:** gate levels 0.2 V and 0.9 V (L84-87). The `deadband_us` argument is computed but never used (L39, L71), so no deadband is actually implemented, despite the docstring (L46).
- **Pass criterion:** PASS if peak A > 0.01 V, peak B > 0.01 V, |retention| > 0.005 V and no divergence (L176). Retention is the final sample minus a baseline. Decay of the transient is not checked separately.
- **Violations:** none against the physics rules. Test defects: the unused deadband (L71), the "magnetic state" label on a voltage (L9), and the 10 kΩ ring changes `memory_B_pos_in` resistively rather than by any retained magnetic state.

## One_Wave_Bench/engine/electrical/test_working_ab_transfer.py
- **Purpose / node IDs cited:** the same UPDATED_63 A→B criterion on `P0HexagonWorking`.
- **Point rotation / Path rotation / Field:** not present.
- **Magnetism:** "B retains changed magnetic state" (L10) is read from the node voltage `memory_B_pos_mid` (L56, L89). There is no magnetic variable.
- **Parent/child:** not present.
- **Hard-coded targets / refits:** the `drive_voltage` argument is unused (L34). All six sweep runs (L145-150) are identical.
- **Pass criterion:** the same thresholds (L115).
- **Violations:** none against the physics rules. Test defect: the dead sweep parameter (L34).

## One_Wave_Bench/engine/internal_dialogue.py
- **Purpose / node IDs cited:** a bounded Field-asks / Void-answers exchange routed by M4 (L3-10). No node IDs are cited. This is control-flow program state.
- **Point rotation / Path rotation / Field / Magnetism / Parent/child:** not present. "Field" here is a dialogue role, not a physical field (L21).
- **Hard-coded targets / refits:** budget defaults of 2, 2 and 6 turns (L64-66).
- **Pass criterion:** none. Outcomes are CONFIRM, DENY or DEFER.
- **Violations:** none.

## One_Wave_Bench/engine/run_experiment.py
- **Purpose / node IDs cited:**
  - Bench Stage 01. Cites D-412 (request/receipt governance) and D-413 (L3-8).
  - It imports `Nodes/D-413_Ground_Lattice_Orbital_Restoring_Simulation/simulate_d413.py` directly as the canonical engine (L21-34).
- **Point rotation:**
  - Reads `spin` (= the D-413 `q.omega`) from the imported engine and reports `max_abs_spin` and `final_spin` (L47, L62-63). This file does not compute spin itself.
  - In the imported D-413 engine (`simulate_d413.py` L31-34, read via grep only), the spin is driven by `tau += rx*sy - ry*sx`, where `sx = -gravity*grad_x` is the imposed curvature-well (gravity) force on an asymmetric shell. So dω/dt = spin_coupling·τ/N − 0.045·ω.
  - **Gravity therefore starts and changes point rotation.** The packet also starts with ω = 0.08 in `_auto_orbit_initial` (L41).
  - The decay term −0.045ω is an unconditional damping. It is not a magnetism-gated −γL.
  - There is no open/closed magnetic switch and no parent organization rate.
- **Path rotation:** `orbital_L` = dx·vy − dy·vx is reported (L47, L64-65). This assigns an angular momentum to the path (the orbit).
- **Field:** in the imported engine, the "curvature well" gradient is imposed, not derived. The file's own limitations admit this (L141). There is no curl or wake. Strain and compression are tracked (L66-67).
- **Magnetism:** not present.
- **Parent/child:** not present.
- **Hard-coded targets / refits:** the initial orbit speed is derived from well parameters (L40). No observed values are used.
- **Pass criterion:**
  - `zero_input_drift_below_1e-9` and `lattice_deforms_when_active` (L119-124). Neither is a point-rotation test.
  - The DEMO hypothesis is "Increasing shell asymmetry increases induced axial spin at fixed orbit" (L162), with the falsifier "max_abs_spin does not increase monotonically" (L170). That falsifier is not actually evaluated in `checks`.
  - Status is hard-coded "YELLOW" (L133).
  - It writes to `One_Wave_Bench/runs` by default (L179). I did not run it.
- **Violations:**
  - (1) Gravity (well-gradient torque on the shell) starts and changes point spin: run_experiment.py L162 (demo hypothesis) together with simulate_d413.py L33-34. This violates "Gravity does not start or affect point rotation" and "a thing does not start a spin on its own".
  - (2) Unconditional spin damping −0.045ω (simulate_d413.py L34), with no open/closed magnetic switch.
  - (3) `orbital_L` is reported as an angular momentum on the path (run_experiment.py L64-65; simulate_d413.py L42). The canonical Path rotation (G-769) carries no L. This is a bookkeeping label, but it conflicts with the C-306/C-307 ownership of L.
  - (4) The stated falsifier is not checked (L170 vs L119-124).

## One_Wave_Bench/hardware/circuit_designer.py
- **Purpose / node IDs cited:** a BOM and KiCad stub generator for a three-phase ternary driver. No node IDs are cited.
- **Point rotation / Path rotation / Field / Magnetism / Parent/child:** not present.
- **Hard-coded targets / refits:** part numbers. The schematic date "2026-10-06" is hard-coded (L340).
- **Pass criterion:** none.
- **Violations:** none. Code defects:
  - `connections` are never populated, so the netlist has no nets (L65-78 vs L144-233).
  - The divider is named "1kΩ" (L179).
  - The `__main__` block writes to /tmp (L400-401).

## One_Wave_Bench/logic_core/body_rate_transport.py
- **Purpose / node IDs cited:** "G-750 body-rate transport" (L1).
- **Point rotation:** body rate vectors ω, composed for a parent/child pair (L34-46). Nothing here starts or changes a spin; this is pure kinematics. There is no gravity, no magnetic switch and no organization target.
- **Path rotation / Field / Magnetism:** not present.
- **Parent/child:** canonical.
  - `compose_omega_body` = ω_c + R_cᵀ ω_p (L34-36). This is transport first, then add.
  - `compose_omega_ground` = R_p ω_p + (R_p R_c) ω_c, with R_child^ground = R_parent·R_child built explicitly (L39-46).
  - The two charts are mutually consistent: R_p R_c (ω_c + R_cᵀ ω_p) = R_p R_c ω_c + R_p ω_p.
- **Hard-coded targets / refits:** none.
- **Pass criterion:** none here. A companion test, `logic_core/test_body_rate_transport.py`, exists outside this slice.
- **Violations:** none. This is the canonical implementation of the G-750 transport rule.

## One_Wave_Bench/logic_core/commitment_map.py
- **Purpose / node IDs cited:** a five-level Schmitt commitment readout (−3, −2, 0, 2, 3) driven by a latent variable with retention (L1-5). The docstring calls it explicitly "not yet a physical One-Wave law" (L4-5). It imports `six_route_logic.LogicRoute` (L14).
- **Point rotation / Path rotation / Field / Magnetism / Parent/child:** not present. `phase_lock = ½(1+cos φ)` (L61-64) is a logic alignment weight, not a rotation.
- **Hard-coded targets / refits:** parameter defaults (L22-28).
- **Pass criterion:** none here.
- **Violations:** none.

---

## Slice summary

- **Canonical point-rotation implementation:** only `logic_core/body_rate_transport.py`, the G-750 parent/child body-rate transport. Its body form is ω_c + R_cᵀω_p and its ground form is R_pω_p + R_pR_cω_c. The two are consistent, and the code transports before adding. It does not model the spin itself (no L = Iω, no inertia axes, no magnetic open/closed law), because it is kinematics only.
- **Point-rotation violations:**
  - `engine/run_experiment.py`, through the D-413 engine it imports. Gravity (an imposed curvature-well gradient) applies torque to an asymmetric shell and starts and changes the spin. The demo hypothesis advertises this: "asymmetry increases induced axial spin" (L162).
  - Spin decays by an unconditional −0.045ω, with no magnetic switch.
  - Orbital "L" is reported on the path (L64-65).
  - The stated falsifier is never checked (L170).
- **Point/Path/Field vocabulary with no physics behind it:**
  - `nerve_gate_resonance.py` maps Point = voltage, Path = gate and Field = resonance (L86-90). Its "rotating Maxwell field" is not rotating, because V and W are identical (L174).
  - `simulate_nerve_gated_cell.py` claims "point → path → field rotations" with no implementation, and its ω tuning only ever increases (L129-132).
  - `p0_hexagonal_circuit.py` and `p0_hexagon_direct.py` label phase B as "rotation/gyro" with no code behind it.
- **Magnetism:** no file in this slice builds B, R, K_L or κ_R. The A→B "retains a changed magnetic state" tests (`test_hbridge_ab_transfer.py`, `test_hbridge_independent_ab_transfer.py`, `test_working_ab_transfer.py`) read node voltages. The circuits have no magnetic core or hysteresis.
  - `test_hbridge_ab_transfer.py` can never pass, because of a dead append guard (L133).
  - Two tests sweep a `drive_voltage` argument they never use (test_hbridge_ab L37, test_working_ab L34).
- **Live vs dead or legacy:**
  - Live solvers and runners: `run_experiment.py` (wraps D-413) and `simulate_nerve_gated_cell.py` (with `nerve_gate_resonance.py`).
  - Live utilities: `body_rate_transport.py`, `commitment_map.py` and `internal_dialogue.py`.
  - Earlier circuit iterations that only build netlists: the P0 hexagon variants `correct`, `direct`, `final`, `hexagonal_circuit`, `hbridge`, `working` and `hbridge_independent`. Each is superseded by the next, and the last three are each driven by one A→B test script.
  - Tooling with no physics: `hardware/circuit_designer.py`.
