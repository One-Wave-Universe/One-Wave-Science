# Electrical (DC batch)

The smallest missing electrical subsystem needed to run real resistive-DC
regressions underneath the existing bench. This does not touch, replace, or
route through `engine/run_experiment.py`, the D-413 engine, `runs/`,
`runs/manifest.json`, `engine/build_manifest.py`, or the UI — it is a
separate, self-contained package a caller imports directly. No routing hook
was needed in `run_experiment.py`, so none was added.

```
electrical/
    components.py   DCVoltageSource, Resistor, Wire, Ground
    circuit.py       Circuit: a plain container + .solve()
    solver.py        real MNA-style Kirchhoff/Ohm nodal solver, no numpy dependency
    measurements.py  node/differential voltage, branch/source current, power
    energy.py        energy = power * duration, energy-balance check
    tests/
        test_dc_regressions.py   the batch's required regressions
        receipts/                 last run's TEST/EXPECTED/ACTUAL/TOLERANCE/
                                   PASS-FAIL text, JSON, and CSV output
```

## Scope (this batch only)

Components: `DCVoltageSource`, `Resistor`, `Wire`, `Ground`. Nothing else —
no MOSFETs, capacitors, inductors, comparators, batteries with internal
resistance, LEDs, magnetics, or any macro. See
`../../../Virtual_Breadboard/00_RULES/` for the general layered-architecture
discipline this follows: real Kirchhoff/Ohm relationships, not scripted
expected values; failure (a mismatched, unbalanced network) is valid output,
never silently corrected.

Run the regressions:

```
python3 One_Wave_Bench/engine/electrical/tests/test_dc_regressions.py
```

Every check prints TEST/EXPECTED/ACTUAL/TOLERANCE/PASS-FAIL, all checks run
even if one fails, and results land in `tests/receipts/` as text, JSON, and
CSV.

## The one behavior this batch exists to prove

A passive resistive midpoint (a real two-resistor divider's CENTER node) is
not fixed. Load it and it moves, by exactly the amount the real network's
own Thevenin equivalent predicts — `test_loaded_divider_center_moves` and
the 1%/5% mismatch tests are the load-bearing checks in this batch; every
other test exists to establish the Ohm's-law/Kirchhoff foundation those two
depend on.

## Explicitly out of scope for this batch

Anything beyond the pass-criteria checklist in the request this batch was
scoped from: MOSFETs, capacitors/inductors, AC, energy storage,
reinjection, magnetics, or any flashlight-specific circuit. Those are
future batches, chosen from what this batch's measurements show — not
started here.
