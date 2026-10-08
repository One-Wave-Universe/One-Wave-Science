# Code ledger — slice c05

Files in slice: 1. Files read in full: 1 (`circuit.js`, all 3529 lines read in four pages: 1-900, 900-1799, 1800-2699, 2700-3529).

## /home/user/Builds/Virtual_Breadboard/js/circuit.js
- Purpose / node IDs cited: This is the Virtual Breadboard circuit engine, a SPICE-style Modified Nodal Analysis (MNA) solver (header, lines 1-62). It models resistors, capacitors (BE, trapezoidal and Gear2 companions, lines 1660-1705), inductors (2127-2171), ferrite toroids with mutual inductance (2173-2212), square-loop memory cores and latch relays (2214-2250, 2698-2762), transfluxors (2252-2271, 2605-2696), MOSFETs and BJTs, comparators, H-bridges, Schmitt triggers, AC/PWL/PULSE sources and an MTJ angle-sensor source (2290-2319). It also has thermal self-heating (443-460, 1181-1186). The file cites no One-Wave node IDs (no C-/G-/E-/A- IDs appear). Its only links to One-Wave vocabulary are:
  - the transfluxor is called "the CELL_V1 figure-8 nucleus" (line 1275);
  - latch relay `actualState` is labeled `'field'` when B >= 0 and `'void'` when B < 0 (line 3445).
- Point rotation: not present. Nothing represents spin, omega, L, attitude or inertia. The nearest analogue is the memory core's normalized flux B in [-1, 1]:
  - it starts at 0, "demagnetized" (lines 1439-1443);
  - below the coercive threshold Hc it holds its value, which is remanence (`target = bStart`, lines 2719-2725);
  - above Hc it relaxes toward +/-1 with time constant tau (lines 2726-2754).
  This is magnetic hysteresis, not rotation. No gravity or compression gradient exists in the file. There is no open/closed switch of the form dL/dt = 0 vs -gamma L. There is no parent "organization" target rate.
- Path rotation: not present. The MTJ sensor's "rotating field" (lines 24-28, 2290-2319) is two sinusoidal voltage sources 90 degrees apart, `wave(value, freq, phase, t)` (lines 881-883). The angle is set by the source, not by any dynamics, and it carries no L.
- Field: not present in the One-Wave sense. There is no curl, wake, chi or grad chi.
- Magnetism: done as circuit magnetics only.
  - Toroid: mutual inductance L_ij = k*sqrt(L_i L_j) with a winding sense sign (lines 2201-2209).
  - Memory core: Faraday V = N*phiSat*dB/dt (line 2247). B is switched by the net ampere-turns against Hc (lines 2705-2725), and Hc has a temperature coefficient (lines 460, 2718).
  - Transfluxor: two leg states b2/b3 with flux continuity (lines 1275-1279, 2605-2632).
  - Absent: B is never a vector field, and there is no R tensor, no W_B = B⊗B - |B|²I/3, no K_L and no kappa_R. Because there is no gravity channel, B cannot produce gravity when grad chi = 0.
- Parent/child: not present. There are no frames and no rate transport. Composition is MNA conductance stamps added into a linear matrix (e.g. lines 1616-2062). That is ordinary circuit superposition, not rotation rates.
- Hard-coded targets / refits: No Mercury, Moon, 125 GeV or particle-mass values. The constants are datasheet-class component parameters, labeled as approximations, for example:
  - LED Vf (line 371) and LED wall-plug efficiency (line 380);
  - MOSFET model cards (lines 640-645);
  - TLV3202 comparator (lines 794-821), DRV8833 H-bridge (lines 831-850), SN74HC14 Schmitt trigger (lines 864-873);
  - latch relay specs (lines 602-612), thermal specs (lines 451-460).
  None of them is reported back as a prediction.
- Pass criterion: numerical, not physical.
  - `solver.converged = stateStable && numericalConverged` (line 2908).
  - `stateStable` means no device on/off or core-state change in the last fixed-point iteration (line 2862).
  - `numericalConverged` means the max MNA residual is within abs + rel tolerance (lines 2899-2900).
  - `diagnose()` derives noReference / solverFailed / floating / short / overcurrent / open labels from the solved result (lines 277-369).
  - There is no point-rotation or spread pass bit.
- Violations: none against the canonical rules. The file is an electrical circuit simulator and does not claim to model Point/Path/Field, gravity, chi, L bookkeeping or the bound lattice. One vocabulary note, not a rule violation: line 3445 maps the sign of the relay's core B to the strings `'field'` and `'void'`. That is a label on a circuit remanence state, not a canonical Field/Void derivation, and it should not be cited as evidence for magnetism-opens-the-point or any gravity link.

## Slice summary
- Implements point rotation canonically: none. The slice has no rotation, spin, L or attitude model.
- Violates point rotation: none. The file never touches rotation, gravity, chi, K_L or kappa_R, so there is nothing in it to violate.
- Live vs dead/legacy: `circuit.js` is a live solver. It exports `Circuit`, `netlist`, `diagnose` and more through `module.exports` / `window.CircuitEngine` (lines 3515-3528). It pulls in `./magnetics.js` (`MagneticParts.prepareComponents`, lines 66-77), and its comments mention `simulate.js` (`monteCarlo`, line 556), `components.js` (line 490) and `00_RULES/measurement_rules.md` (line 284). All of that is circuit-domain only.
- Cross-references that matter for point rotation or magnetism: `./magnetics.js` (outside this slice) prepares the magnetic components before they are stamped. The "CELL_V1 figure-8 nucleus" transfluxor (line 1275) and the `'field'`/`'void'` relay labels (line 3445) are the only places that touch One-Wave terms. Any document that cites this breadboard as magnetism evidence should be checked against those two spots.
