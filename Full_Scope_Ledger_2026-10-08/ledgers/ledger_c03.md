# Ledger c03 (2 files, both read in full)

## /home/user/Builds/Virtual_Breadboard/js/app.js
- Purpose / node IDs cited: Browser UI controller for the Virtual Breadboard circuit simulator (2605 lines, IIFE). It handles board layout presets (L4-16), part placement and hit-testing (L139-931), the Inspector and context menu (L941-1289), save/load/export (L1292-1487), example presets (L1489-1593), the AI-build settings and spec loader (L1595-1911), the run/receipt practice API (L1747-1975), the oscilloscope (L1977-2318) and the render loop (L2320-2549). Debug and automation hooks are at L2551-2598. No One-Wave node IDs (C-/G-/E-/A-) are cited anywhere. The only "Layer" reference is the comment "Layer 11: execution controls and interchange only" (L1747).
- Point rotation: not present. The only rotation-like quantities are electrical or UI ones: the `mtjsensor` "Rotation" rate in Hz (L37, L374, L970), which sets a sin/cos quadrature source frequency, plus a decoded angle `atan2(vSin, vCos)` in the readout (L1118); and the potentiometer knob angle from `atan2`, mapped to wiper position (L735-739). There is no omega, L, inertia or attitude state, and no gravity or compression gradient. There is no open/closed magnetic switch in the dL/dt sense and no parent organization rate.
- Path rotation: not present. There are current-flow animation dots along a part or a Bezier wire arc (L2496-2518), but they are cosmetic only.
- Field: not present. There is no curl, wake, chi or grad chi.
- Magnetism: only as electrical circuit elements, which are delegated to other modules. Toroid windings and inductance come from `MagneticParts.toroidWindings` (L156-158), with coupling coefficient `TOROID_SPACING_COUPLING[p.spacing] || 0.9` (L222). Memory core values are `hcAmpTurns, phiSat, switchTau` from `Components.MEMORY_CORES` (L235-240). The remanence B readout (L1172-1185) is labeled from the solver's `coreStates`, with thresholds ±0.5 used only for the label. The transfluxor/figure-8 elements come from `Components.transfluxorElement` / `MagneticParts.figure8Element` (L231-233), and their `b2/b3` leg states are displayed at L1155-1166. None of R, K_L, kappa_R or W_B is built. B never produces gravity, and gravity does not exist in this file.
- Parent/child: not present. There are no rate frames or transport.
- Hard-coded targets / refits: none in a physics-prediction sense. There are UI default component values (L28-58), the 0.9 default coupling (L222), the hex example forcing `battery.value = 1` when `?board=hex` is set (L1585-1591), and scope constants (L87-89). No observed astronomical or particle values are used.
- Pass criterion: there is no physics pass bit. The receipt status is `SOLVER_FAILED` / `MODELED` / `EDITED_PENDING` / `UNRUN`, with `physicallyValidated: false` hard-set (L1940-1941) and explicit limits (L1949). Solver non-convergence stops the run (L1764-1766). Spec validation goes through `AIBuilder.validateSpec` plus per-field checks (L1818-1878).
- Violations: none against the canonical rotation/magnetism/gravity rules, because the file does not touch that domain. A side note outside the canonical list: the AI-build path asks for and stores a provider API key in localStorage (L1600-1611, L1723-1724). The export scrubs that key (L1349-1354).

## /home/user/Builds/Virtual_Breadboard/js/bench-reality.js
- Purpose / node IDs cited: Bench-reality audit layer (131 lines). It checks whether a solved MNA circuit corresponds to an honest physical breadboard build (L3-19). The checks are: CENTER spine missing, implemented with a series capacitor, a current source or excess resistance (L61-80); a mixed dual-supply plus vgnd topology (L82-89); exceeding the per-source `benchMaxCurrent` (L91-106); an impossible zero source receipt under real load power (L108-118); and an H-bridge inside a `cellOnly` test (L120-126). It cites no node IDs.
- Point rotation: not present.
- Path rotation: not present.
- Field: not present.
- Magnetism: not present. There are no magnetic elements, and no B, R, K_L or kappa_R.
- Parent/child: not present.
- Hard-coded targets / refits: none. The tolerances default to `1e-12` (L103) and `1e-6` (L113, L115), or come from caller-supplied options.
- Pass criterion: `ok = errors.length === 0` (L128). This is an electrical bench-contract audit, not a rotation, spread or physics claim.
- Violations: none.

## Slice summary
- Canonical point rotation implemented: neither file. Neither represents point spin, L = I omega, inertia axes, the magnetic open/closed switch, parent/child rate transport, K_L, R or kappa_R, or gravity.
- Violations of the canonical rules: none. Both files are outside the Point/Path/Field physics domain. They are electrical-circuit tooling (Virtual Breadboard). The only "rotation" (MTJ sensor frequency, pot knob angle) and "magnetism" (toroid, memory core and transfluxor B-state, handled in other modules) are ordinary circuit/UI quantities. None of them is presented as a One-Wave prediction.
- Live vs dead/legacy: both are live. app.js is the active browser front end, driving `CircuitEngine.Circuit.solve` (L20, L1763). bench-reality.js is a live CommonJS audit module (`module.exports`, L131), presumably used by Node tests or the CLI. It is not called from app.js. The magnetic physics actually lives in modules outside this slice (circuit.js B-state solver, magnetic-parts, components), referenced at L156-166 and L229-240.
