# G-735 — Chapter-Driven Simulator Program

**Status:** Active implementation authority  
**Dependencies:** G-728, G-734, all current science chapters

## Correction

The deliverable is not a collection of disconnected mathematical demos. Every
motion and interaction described in the science chapters must have a declared
simulation route:

`chapter -> mechanism -> Gray control -> One-Wave extension -> engine -> receipts -> visual scene`.

## Coverage authority

`One_Wave_Bench/simulators/chapter_registry.py` registers all twenty-three
current science chapters across Book 1, Book 2, and Book 5. Book 3 and Book 4
currently contain scope/status documents rather than science chapters; their
future chapters must be registered when written.

Every registry entry declares:

- scale;
- motions;
- interactions;
- Gray/standard control;
- proposed One-Wave extension;
- numerical engine;
- honest coverage state;
- intended visual scene.

## Implementation rule

A chapter is not simulated merely because it has an animation. `COMPLETE`
requires a numerical engine, baseline comparison, conservation/error receipts,
parameter declarations, failed cases, and a visual driven by engine state.

Legacy HTML visuals remain visual prototypes until their state is produced by
validated engines. `UNBUILT` is recorded explicitly rather than hidden.

## Immediate build order

**Active freeze:** do not advance beyond Micro until the quark-vortex/proton
knot simulator has defensible equations, conserved/error-tracked evolution,
topological diagnostics, interaction tests, nested PPF receipts, and a polished
state-driven visual.

1. Micro unified Field scene: particle, quark-vortex candidate, proton knot,
   electron/EM shell, and Mass Effect.
2. Propagation scene: photon, neutrino, measurement windows, time/dispersion.
3. Cell scene: membrane, internal transport, signaling, division.
4. Planetary/solar scene: Newton/relativity baseline plus declared One-Wave terms.
5. Galactic scene: rotation, tidal environment, arms, wake hypotheses.
6. Stellar lifecycle: star, nucleosynthesis, supernova, black hole/quasar.
7. Neural/state scene: memory, M4, AI-human and human-human coupling.

The camera/visual system must eventually connect these as a Micro-to-Macro
zoom, but native units and solvers remain separate behind the visual lens.
