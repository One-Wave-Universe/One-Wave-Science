# Failure Rules

## Rule 5 — failure is valid output (full statement)

See `physics_rules.md` for the complete list of failure modes the simulator must
be able to genuinely produce. This file covers the *process* side: what to do
when you find one.

A failing test is data, not an emergency to paper over. When a check fails:

1. Do not weaken the tolerance to make it pass.
2. Do not delete or skip the check.
3. Do not "fix" it by changing an unrelated layer until it happens to pass.
4. Classify it (Type A-K, `update_rules.md`) and fix the actually-responsible
   layer, or determine the test's own expectation was wrong (Type J) and say so
   explicitly.

This session hit real examples of both: the LC/RLC ringdown test failing was a
real Type D/E problem (a `dt` floor in the electrical/dynamics stamping) and got
a real code fix; the RC filter phase-sign test failing was a Type J problem (the
test's own expected sign was backwards relative to `Sim.phaseDifferenceDeg`'s
already-established convention) and got the test corrected instead of the
physics.

## Rule 8 — build definitions remain external

A flashlight failure does not mean "change the breadboard until the flashlight
works." Determine whether:

1. the breadboard physics is wrong,
2. the build definition is wrong, or
3. the real circuit simply does not perform as expected.

Those are three different outcomes, with three different owners. Only outcome 1
is a breadboard-layer bug. Outcome 3 in particular is not a bug at all — it is
the simulator doing its job and telling you a design doesn't work, which per
Rule 1 is exactly what it should do.

## Bug triage table

See `update_rules.md` for the full Type A-K classification table used to route
every failure to its owning layer before any file gets touched.

## Never silently correct a bad circuit

If a circuit is genuinely unstable, ill-posed, or self-contradictory, the correct
outcome is that the solver fails to converge or reports the real pathological
values — not that it quietly produces a plausible-looking wrong answer. This
session's reinjection-primitive work found exactly this case: a first NMOS-based
high-side switch design created a genuine self-referencing Vgs feedback loop
(channel state affects Vgs, which affects channel state), and the fixed-point
solver correctly refused to converge on it rather than making something up. The
fix was to redesign the circuit (a PMOS with a fixed source reference), not to
force the solver to accept the unstable one.
