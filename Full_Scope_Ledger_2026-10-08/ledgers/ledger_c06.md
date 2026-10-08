# Code ledger, slice c06 (Builds/Virtual_Breadboard)

All three files are electronics code: a breadboard UI, a three-resistor demo and the circuit-engine test suite. None of them models Point, Path or Field rotation, gravity, chi or the lattice. Their magnetism is real ferrite and square-loop core physics, meaning ampere-turns against Hc, phiSat and Faraday-induced voltage. None of them uses a B-tensor or K_L construction.

## /home/user/Builds/Virtual_Breadboard/js/components.js
- Purpose / node IDs cited: This file is the component palette, holding electrical defaults and canvas draw functions for every breadboard part (lines 1-10, 114-187). It cites no node IDs. The only One-Wave vocabulary is in comments: "CELL_V1 figure-8 nucleus" (line 82); "Extra windings ARE the group-memory / toward-away-neighbor mechanism -- just more real ampere-turns summed onto the same shared flux" (lines 169-171); and "Distinct nuclei" round figure-8 (sensor) and square figure-8 (motor) (lines 177-179).
- Point rotation: Not present. The only angle state is the potentiometer knob angle (lines 474-491), which is UI. The MTJ sensor needle angle is `2*pi*freq*animT + phase` (line 813), a display of a driven rotating field. Nothing represents L, inertia or attitude, and nothing starts or changes a spin.
- Path rotation: Not present.
- Field: Not present. There is no curl, wake, chi or grad chi.
- Magnetism: The core tables are TOROID_CORES, with A_L in H/turn² and mean turn length (lines 50-54), and TOROID_SPACING_COUPLING k = 0.97/0.9/0.75 (line 58). MEMORY_CORES holds hcAmpTurns, phiSat and switchTau (lines 72-76). TRANSFLUXOR_CORES holds phiLeg, hcLarge, hcSmall and switchTau (lines 89-92). transfluxorElement() builds windings as N, sense, R = N·meanTurnLen·ohms/m and an aperture (lines 96-110). The solved remanence B in [-1, 1] is only drawn as a colour, and the comments say this function never decides it (lines 960-966, 975-1008, 1010-1075). Nothing builds R from B, there is no K_L and no kappa_R, and B is never linked to gravity.
- Parent/child: Not present.
- Hard-coded targets / refits: None of the physics kind. Part parameters are datasheet-class constants: copper ohms per metre (line 45), MOSFET classes Vth 1.5 and 2.1 (lines 31-34) and core parameters (lines 50-92). Lines 87-88 say the transfluxor core is "a model to build and test against, not a measured part".
- Pass criterion: None, because the file has no tests.
- Violations: None.

## /home/user/Builds/Virtual_Breadboard/js/triad3d.js
- Purpose / node IDs cited: This is a "differential triad" demo with three resistor branches (Ru, Rl, Rc) sharing reference node g, fed by two equal batteries. It is solved on the real circuit engine (lines 1-33). It cites no node IDs, and line 113 labels it "Not a measured core."
- Point rotation: Not present. `yaw += 0.01` every 50 ms (line 152) is a camera spin used by the 3D projection (lines 47-55). It is purely visual, has no physics meaning and carries no L.
- Path rotation: Not present.
- Field: Not present.
- Magnetism: Not present. The file has no MOSFET, no gate and no core (line 10).
- Parent/child: Not present.
- Hard-coded targets / refits: None. The defaults are 5 V, 2200/1000/100 Ω (line 60), and the readout reports solver convergence plus Vt and the branch currents (lines 106-114).
- Pass criterion: None in this file. It is exercised by test/triad3d.test.js, which is outside this slice.
- Violations: None.

## /home/user/Builds/Virtual_Breadboard/test/circuit.test.js
- Purpose / node IDs cited: These are the circuit-engine regression tests, run by `npm test` (package.json line 11). They include Ohm's law, LED, RC/LR transients, AC, MTJ quadrature, toroid transformer, MOSFET, memory core, transfluxor-adjacent group/toward-away cores, comparator window, simulate.js tooling, thermal, battery and LED output. There are no node IDs. One-Wave-flavoured labels appear only as circuit-state names: Left/Right/Hold trits (lines 775-822); group memory (lines 824-861); toward/away neighbours (lines 863-908); and "Void/Field" and "Field/Field" conflict in resolvedOutputFrom (lines 1424-1449).
- Point rotation: Not present. Test 14 (lines 310-338) checks that sin²+cos² = amplitude² for an MTJ sensor driven by a prescribed rotating field. That rotation is an input frequency, not a body spin.
- Path rotation: Not present.
- Field: Not present.
- Magnetism: Toroid coupling and turns ratio are tested in Test 15 (lines 340-395). Test 25 (lines 655-703) checks square-loop lock and flip to ±Br past hcAmpTurns, with an induced sense spike. Test 26 (lines 705-730) checks that a sub-Hc pulse leaves remanence unchanged. Test 29 (lines 824-861) checks ampere-turn superposition, where the last write wins. Test 30 (lines 863-908) checks winding polarity (toward/away). Test 45 (lines 1504-1525) checks Hc thermal drift. Nothing builds an R or K_L tensor or sets kappa_R, and there is no gravity link.
- Parent/child: Not present.
- Hard-coded targets / refits: None in the observed-value-as-prediction sense. Expected values are analytic and computed from the inputs, for example 5/221 (line 22), (5-1.8)/233 (line 43), L/R and RC exponentials (lines 270-274, 582-583), 20 mV·e^-1 (line 639) and the 2.52 V divider (line 414). The assertions on BATTERY_MAX_CURRENT and the NMOS_PARTS rdsOn are engine constants used consistently (lines 77, 462-465, 1543).
- Pass criterion: Each test passes when its electrical quantities match an analytic answer within a tolerance, or when a core state reaches ±1 or 0 or stays unchanged. No test uses point rotation or spread as its pass bit.
- Violations: None. One terminology note, which is not a rule violation: "Void/Field" (lines 1424-1449) and "Left/Right/Hold" are used as labels for circuit voltage and core states. They do not assert any Point/Path/Field physics.

## Slice summary
- **Canonical point rotation:** No file in this slice implements point rotation (L = I·omega, open/closed dL/dt, transport from parent to child). Point, Path and Field are absent throughout.
- **Violations:** None against the canonical rules. Nothing makes gravity start a spin, turns magnetism into gravity, uses a hard-coded kappa_R or adds parent and child rates without transport. Observed values are not refit as predictions.
- **Magnetism in this slice:** It is ordinary circuit magnetics: inductance A_L·N², coupling k, square-loop Hc/phiSat remanence and a transfluxor with two apertures. It is unrelated to the canonical B → R → K_L chain.
- **Live solvers vs display code:** components.js is live. Its palette and draw functions are used by app.js, and transfluxorElement() is used by simulate.js:284 and app.js:233. triad3d.js is a live UI demo, loaded by index.html and tested by test/triad3d.test.js; its yaw spin is visual only. circuit.test.js is the live default `npm test` suite for js/circuit.js and simulate.js. The physics solver itself, js/circuit.js, is not in this slice.
