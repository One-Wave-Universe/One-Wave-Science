# Builds — separate from the breadboard

## Canon

A build uses the breadboard. A build does not become part of the breadboard.
The breadboard does not contain project intent — it knows "9V source connected
to these components in this topology with these requested measurements," never
"this is a One-Wave flashlight."

## What already respects this separation

- `experiments/brain_cell_001.json` — a real headless experiment: parts,
  topology, stages, requested measurements, pass criteria, submitted to
  `simulate.js` exactly the way the canon's Build Interaction Rule describes.
  This is the closest existing thing to a real `BUILDS/<name>/` entry.
- `test/qualification.test.js`, `test/primitives.test.js`,
  `test/regression-builds/*.js` — every circuit in these files is a generic
  proof of breadboard *capability*, not a build. None of them encode project
  intent (no file says "this is for the flashlight"); they say "this topology,
  these parts, these expected values."

## What currently blurs the line

| Thing | Current location | What it actually is | Where the canon puts it |
|---|---|---|---|
| Cal A-H preset boards | `js/app.js` (`presetCalAParts()` etc.) | Specific example circuits proving specific real-physics claims | `BUILDS/calibration/` |
| Stage 1 Real Millivolt Ternary preset | `js/app.js` (`presetStage1TernaryParts()`) | A specific hardware-bound build (has its own bench doc, see below) | `BUILDS/ternary_stage1/` |
| `STAGE1_PHYSICAL_BUILD.md` | repo root | Exact breadboard holes, IC pin orientations, BOM, jumper list, test points for the Stage 1 build above | `BUILDS/ternary_stage1/PHYSICAL_BUILD.md` |
| `experiments/brain_cell_001.json` | `experiments/` | A real, already-external-shaped build (see above) | `BUILDS/brain_cell_001/` — needs only a directory rename, not a rewrite |
| `experiments/prototype_001.json` + its cycle/destructive test scripts | `experiments/` | Two-state-machine + M4 fast/oversight/override experiment, with a 100-cycle repeated-run harness and a destructive/boundary-finding test | `BUILDS/prototype_001/` |

None of the above is a breadboard-layer bug. They are all real, working builds
that happen to be filed in a location the canon would organize differently.
Per `00_RULES/architecture.md`'s No-Rebuild Protection and `interface_rules.md`,
moving them is scoped, reversible, low-risk directory-organization work for
whoever picks up Layer 11 / Builds next — explicitly not bundled into this
architecture-adoption pass, which touched no build-definition file's location
or content.

## The flashlight, when it exists

Per the very conversation that produced this canon: the flashlight build
(balanced/reinjection vs. a conventional reference circuit) does not exist in
this repo yet. When it's built, it goes in `BUILDS/flashlight/` from day one —
parts, topology, requested measurements, pass criteria — and it is compared
against a conventional reference circuit using the breadboard's own
measurement layer (`05_MEASUREMENT`), never by asking the breadboard to know
it's a flashlight.
