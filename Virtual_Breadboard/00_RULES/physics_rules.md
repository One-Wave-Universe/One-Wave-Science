# Physics Rules

## Rule 1 — Real behavior over desired behavior

The simulator represents the modeled physics. Never alter circuit behavior merely
because a proposed build was expected to work differently. If a build doesn't do
what its designer hoped, the question is always "is the physics right?", never
"how do I make the physics agree with the hope?"

This is the rule this session's own qualification work leaned on hardest: when the
LC/RLC ringdown test rang 3-300x too fast, the fix was to find and correct the real
bug (a `dt` floor silently clamping every reactive component's timestep), not to
adjust the test's expectation to match the wrong output.

## Rule 5 — Failure is valid output

The simulator must be able to genuinely produce, and never silently hide:

- shorts
- excessive current
- voltage sag
- center/reference movement
- unstable oscillation
- component overload
- MOSFET shoot-through
- battery depletion
- capacitor discharge
- inductive flyback
- resistive/dynamic losses
- thermal rise, where modeled

A circuit that *should* misbehave and doesn't is a bug, not a feature. Do not
silently correct bad circuits — see
`test/regression-builds/09_halfbridge_deadtime.js` for a build whose entire point
is that commanding both halves of a bridge on at once produces a real, large,
detectable shoot-through current, not a clamped or ignored one.

## Rule 6 — No unexplained magic primitives

Higher-level behavior must be constructed from lower-level physical capabilities.
A primitive (Layer 06) is a real arrangement of real parts with real wiring, not a
new hard-coded component that hands back a decision.

This codebase already enforces this the hard way: an earlier "Ternary Cell" macro
that internally hard-coded a Hold/Pos/Neg state machine was found and *removed*
(see git history, PR #15) specifically because it let the solver hand back a
decision instead of requiring the decision to be built from real comparator +
MOSFET + capacitor physics. `06_primitives`'s `ternary_resolved_state` and
`reinjection` mappings point at the real discrete-part circuits that replaced it.

## Real component behavior this simulator already models

(See `../LAYER_MAP.md` for exact file/function locations.) Real, non-ideal
behavior already present, not left as an idealization:

- Real forward voltage + dynamic on-resistance for diodes/LEDs (not a bare Vf).
- Real MOSFET Vth, RDS(on), gate capacitance (RC-limited switching, not an
  instant flip), body diode, and off-state leakage (GMIN-scale, not exactly zero).
- Real capacitor ESR + parallel leakage/self-discharge, keyed off a real
  electrolytic-vs-ceramic value threshold.
- Real inductor DC winding resistance (DCR).
- Real battery internal resistance, a hard current limit (brownout), and a
  Coulomb-counted capacity model with a flat-then-knee discharge curve (not a
  linear droop).
- Real comparator input offset voltage and propagation delay (a decision does not
  flip in zero time).
- Real per-color LED wall-plug efficiency for light output, not current-in-implies-
  brightness-out with no per-part distinction.

## What "real" does not mean here

This is an ordinary-electronics circuit simulator, not a finite-element field
solver. Where the canon asks for capability this codebase does not yet have
(temperature-dependent tempco beyond what's listed, arbitrary magnetic core
material parameterization, a field-vector Bx/By/Bz probe), that gap is recorded
as MISSING in `../LAYER_MAP.md`, not silently assumed.
