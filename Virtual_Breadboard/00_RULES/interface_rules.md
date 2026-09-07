# Interface Rules

## The interface owns no physics

Layer 11 (`js/app.js`, `js/board.js`, `index.html`, `style.css`) sits on top. It
requests actions from lower layers and displays their outputs. It does not
compute electrical state itself.

- If a graph is wrong but the exported numbers are correct: fix the interface.
- If the solver numbers themselves are wrong: fix the responsible physics layer.
  Do not make the UI compensate for it.

## Rule 8, interface half

The interface is also where "is this the breadboard's fault or the build's
fault" (`failure_rules.md`) most often gets confused, because the UI is where a
user watches a build fail. A build-specific preset (a Cal board, a Stage-1
ternary cell, `experiments/brain_cell_001.json`) living in `js/app.js` or
`experiments/` is a *build*, per Rule 8 — even though today it's shipped in the
same repo as the breadboard engine, it is conceptually external, exactly like
`BUILDS/flashlight/` would be. See `../11_INTERFACE/MAP.md` and
`../BUILDS/MAP.md` for the current file-level boundary and where it's blurrier
than the canon wants.

## What already respects this boundary

- The oscilloscope (`js/app.js`'s scope rendering, `05_MEASUREMENT`'s scope/
  export capabilities in `simulate.js`) reads solved samples; it does not
  recompute or adjust them.
- `test/qualification.test.js`, `test/primitives.test.js`, and
  `test/regression-builds/` all talk to `js/circuit.js`/`simulate.js` directly,
  bypassing the board/hole-placement UI entirely — a deliberate choice recorded
  in each file's own header, precisely because what's being qualified is real
  component/primitive behavior, not routing wires through literal breadboard
  holes.

## What doesn't yet, cleanly

`js/app.js` (2400+ lines) currently mixes UI event handling with preset/build
definitions (the Cal boards, Stage 1 ternary preset) that the canon wants filed
under `BUILDS/`, not under the interface layer. This is recorded as a known gap
in `../11_INTERFACE/MAP.md`, not treated as blocking — per `architecture.md`'s
No-Rebuild Protection, splitting it out is a scoped, layer-by-layer job for
whoever owns Layer 11 next, not a reason to touch the physics layers today.
