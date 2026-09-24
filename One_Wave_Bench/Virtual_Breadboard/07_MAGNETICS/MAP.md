# Layer 07 — Magnetics

## Canon

Progression: single inductor → two coupled coils → transformer behavior → three
independently accessible windings → field-vector measurement. Three-winding
support must expose per-winding voltage, current, resistance, polarity,
inductance, coupling, phase. Do not assume field shape; if field simulation
exists, expose measurable Bx/By/Bz.

## Status

| Capability | Location | Status | Test |
|---|---|---|---|
| Single inductor | `01_PARTS/MAP.md` | PASSING | `qualification.test.js` Gate 4 |
| Two coupled coils / transformer turns ratio | `toroid` component, mutual inductance `k*sqrt(L_i*L_j)` (`circuit.js:1391`) | PASSING (real turns-ratio, real imperfect-coupling attenuation, real dot-convention polarity) | `qualification.test.js` #19, `regression-builds/14_transformer_turns_ratio.js` |
| Three independently accessible windings | same `toroid` component, arbitrary winding count | PASSING (independently measurable, symmetric for matched turns, explicit reversed-polarity support) | `qualification.test.js` #20 |
| Reflected load (heavy secondary load raises primary current) | same mutual-inductance stamp; needed a much larger self-inductance than the base qualification test to make the effect dominate magnetizing current | PASSING | `primitives.test.js` Primitive 8, `regression-builds/15_three_winding_nerve.js` |
| Per-winding voltage/current/resistance/polarity/inductance/coupling | all exposed via each winding's own `{a, b, N, R, L}` spec plus the shared `coupling` field and per-winding current readback `res.currents.get(tor.id + ':' + wi)` | PASSING | `qualification.test.js` #20 |
| Phase (between windings, or vs. drive) | derivable via `Sim.phaseDifferenceDeg` on two winding traces — no dedicated "phase" field on the component itself | PASSING as a measurement composition | not directly tested as a magnetics-specific phase check today — MISSING as a dedicated test, though the measurement primitive it would use is proven elsewhere (`05_MEASUREMENT`) |
| Field-vector measurement (Bx/By/Bz) | none | **MISSING** | — |
| Arbitrary magnetic core material parameterization | fixed `hcAmpTurns`/`switchTau`/`phiSat` model (`memorycore`), no general B-H curve or material library | **MISSING** — pre-existing backlog item "Magnetic core real material parameterization" | — |

## Honesty note

The canon says "do not assume field shape." This codebase's magnetics model is
explicitly a lumped mutual-inductance / square-loop-remanence approximation, not
a field solver — it never computes or assumes a field shape, it just doesn't
compute a field at all. Bx/By/Bz is recorded as MISSING rather than faked.
