# Code ledger c02

## /home/user/Builds/Virtual_3D_Electronics/test/cores.test.js
- Purpose / node IDs cited: Node test script (91 lines) for magnetic-core parts: square/round bodies with 1..5 apertures, built, JSON round-tripped and rejected with receipts (line 3). Imports ../js/parts.js, world.js, ai-api.js, physics.js (lines 5-8). No One-Wave node IDs cited.
- Point rotation: not present. `rotation: {x,y,z}` (lines 21-22) is the static Euler placement of a CAD part in degrees. It checks that the outline stays a true square at any orientation (lines 24-28). Nothing spins, so there is no omega, no L and no attitude dynamics. No gravity, no compression gradient, no open/closed magnetic switch, no parent organization rate.
- Path rotation: not present.
- Field: not present. No curl, wake, chi or grad chi.
- Magnetism: only engineering ferrite geometry. `P.deriveCore` returns the IEC 60205 AL, le and Ae (lines 85-87), plus transfluxor short- and long-path lengths (lines 88-89). No B tensor, R, K_L or kappa_R, and no link from magnetism to gravity.
- Parent/child: not present.
- Hard-coded targets / refits: AL is checked against the Fair-Rite/Amidon datasheet value of 350 nH/N^2 within 3% (line 86), and le ~20.7 mm and Ae ~7.26 mm^2 are checked too (line 87). These are outside reference values used to validate a geometry-derived number. They are not fed in as inputs, so they are not refits.
- Pass criterion: `check()` booleans on geometry (square sides and diagonals, round radius), aperture count and size, an identical JSON round trip, a FAIL receipt for each bad spec matching its regex (lines 60-81), and AL/le/Ae within tolerance. No rotation or spread criterion.
- Violations: none. The file is outside the One-Wave rotation and gravity domain.

## /home/user/Builds/Virtual_3D_Electronics/test/physics.test.js
- Purpose / node IDs cited: Node test script (73 lines) checking that free builds pass or fail on physics: Ohm/Kirchhoff, part ratings, copper, pads, volume and claims (line 3). Uses ../js/physics.js, catalog.js and fixtures.js (lines 5-7). No node IDs.
- Point rotation: not present. The `rotation` on toroids (lines 58, 61) is static part orientation, used to detect volume intersection ("stood up through the other" -> FAIL).
- Path rotation: not present.
- Field: not present.
- Magnetism: linear core saturation in the comment `B = mu0*800*16.5/0.0207 = 0.8 T >> Bsat 0.29 T` (line 63). It drives 50 turns of 28 AWG at 0.33 A on an FT37-43 core and expects `cores.T1.saturated === true` (lines 64-71). B is a scalar flux density in the core, with no R tensor, no K_L, no kappa_R and no gravity coupling.
- Parent/child: not present.
- Hard-coded targets / refits: AWG resistance is checked against ASTM B258 (22 AWG = 0.05296 ohm/m, 30 AWG = 0.3386 ohm/m, lines 23-25). The divider expects 6.000 V and 3 mA (lines 32-33). These are standard reference values or analytic Ohm's-law results, not refits.
- Pass criterion: the simulator's `verdict` is PASS or FAIL, with receipt text matching regexes (lines 10-21, 37-71). It checks circuit and mechanical validity, not rotation.
- Violations: none. The file is outside the domain.

## /home/user/Builds/Virtual_Breadboard/js/ai.js
- Purpose / node IDs cited: A pluggable LLM backend that turns a plain-language circuit request into a validated parts-list JSON (lines 1-10). It builds the system prompt for breadboard, perfboard and hex-cell layouts (lines 27-187). It has provider callers for Anthropic, OpenAI, Gemini and custom endpoints, using a user-supplied API key (lines 212-299). It also has `extractJson` (lines 301-308) and a shape-only `validateSpec` (lines 343-464). No node IDs. The hex-cell prompt names CELL_V1, the A/B/C mirrors, the CENTER "lean-reference island" and V_BUS (lines 49-60).
- Point rotation: not present. `mtjsensor` (lines 114-118) describes a sensor IC whose outputs are sin/cos of a "rotating field", with `freq` = rotation rate in Hz. That is a prescribed external signal source, not a body's point rotation. No L, no inertia, no switch.
- Path rotation: not present.
- Field: not present. There is no curl, chi or gradient.
- Magnetism: these are prompt-level descriptions of parts. The toroid has mutual-inductance windings and a sense of +1 or -1 (lines 126-137). `figure8round` and `figure8square` share "one idealized aperture law", and the copper length is marked as a hypothesis, "not a measured B-H curve" (lines 57, 138-144). The memorycore keeps square-loop remanence +Br/-Br and its winding ampere-turns add (lines 157-170). There is no B⊗B tensor, R, K_L, kappa_R or gravity coupling. The validator only checks turns, apertures, sense and terminal counts (lines 353-409).
- Parent/child: not present.
- Hard-coded targets / refits: default model IDs (lines 224, 243, 256) and part-class thresholds Vth 1.5 or 2.1 V (lines 152-153, 451-452). No observed physical values are reported as predictions.
- Pass criterion: `validateSpec` returns `ok` when there are no shape or range errors (line 463). The comment says circuit correctness is left to the simulator (lines 340-342).
- Violations: none against the canonical rotation, magnetism or gravity rules. One side note on project rules, not a canonical-rule violation: the file requires a developer API key in the browser (lines 7-9, 212-221). CLAUDE.md asks for the Claude connection to use an authenticated non-API route. This is a pre-existing Builds app, not the Truth Computer.

## Slice summary
- Canonical point-rotation implementations: none. None of the three files models point rotation, path rotation, field curl, chi, K_L, R or parent/child rate transport.
- Violations: none found against the canonical rules. Every "rotation" in these files is static CAD orientation (cores.test.js:21-28, physics.test.js:58-61) or a prescribed sensor-signal frequency (ai.js:114-118). Magnetism appears only as engineering core physics: AL/le/Ae (cores.test.js:85-89), scalar B-saturation (physics.test.js:63-71) and remanence descriptions (ai.js:157-170). None of it is linked to gravity.
- Live vs dead: cores.test.js and physics.test.js are live tests for the Virtual_3D_Electronics simulator (js/parts.js, js/physics.js). ai.js is the live AI-to-parts-list front end for Virtual_Breadboard. None of the three is a One-Wave solver.
