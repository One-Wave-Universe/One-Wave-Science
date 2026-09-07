# Layer 11 — Interface

## Canon

The UI requests actions from lower layers and displays their outputs. It does
not own the physics. If a graph is wrong but exported numbers are correct, fix
the interface. If the solver numbers are wrong, fix the physics layer — never
make the UI compensate.

## Status

| Component | File | Owns physics? | Status |
|---|---|---|---|
| Toolbox / part placement / wiring UI | `js/app.js` | No | PASSING |
| Breadboard geometry / hole hit-testing | `js/board.js` | No (delegates connectivity facts to `02_CONNECTIONS`) | PASSING |
| Part rendering/visuals | `js/components.js` | No | PASSING |
| Oscilloscope (live trace, differential mode, triggering, cursors, coupling, CSV export) | `js/app.js` (scope rendering) | No — reads solved samples via `05_MEASUREMENT`'s snapshot/trace pattern, never recomputes them | PASSING |
| Inspector / context menu / per-type controls | `js/app.js` | No | PASSING |
| AI build-spec executor | `js/ai.js` + `js/app.js` | No — validates and translates a spec into parts, does not compute circuit behavior itself | PASSING |
| `index.html` / `style.css` | presentation only | No | PASSING |

## Where the boundary is blurrier than the canon wants

`js/app.js` also contains a long list of preset/build-definition functions
(`presetCalAParts` through `presetStage1TernaryParts`, the Cal F/G/H boards,
etc.) — these are genuinely *builds* per Rule 8 (a specific circuit someone
wants to test), not interface code, even though they're currently defined in
the same file as the UI event handlers that display them. See `../BUILDS/MAP.md`
for the full accounting of every build-shaped thing in this repo and its
current location relative to where the canon says it should live.

This is recorded as a real gap, not fixed today: moving ~15 preset functions
out of `js/app.js` and into a `BUILDS/`-style location is real, valuable,
scoped work for whoever owns Layer 11 next — but it is a refactor of working,
UI-wired code with no failing test behind it, which is exactly the kind of
change `../00_RULES/architecture.md`'s No-Rebuild Protection says needs its own
dedicated pass, not one bundled into an architecture-documentation change.

## Known-good boundary discipline already in place

`test/qualification.test.js`, `test/primitives.test.js`, and
`test/regression-builds/*.js` all deliberately bypass the interface entirely
and talk to `js/circuit.js`/`simulate.js` directly — each file's own header
says so explicitly. This is the canon's own point in miniature: what's being
proven is real component/primitive *behavior*, and the interface has nothing
to add to that proof.
