# Update Rules — how a change actually gets made

These are the process rules a worker (human or AI) follows when touching the
breadboard. `architecture.md` says what the layers are; this file says how you're
allowed to move between them while fixing something.

## Work division

Work must be divided by layer. A worker gets:

```
TARGET LAYER:
SPECIFIC FAILURE:
ALLOWED FILES:
DEPENDENCY TESTS:
PASS CONDITION:
STOP CONDITION:
```

Example assignment:

```
TARGET:        01_PARTS / MOSFET
PROBLEM:       low-side MOSFET current incorrect at specified Vgs
ALLOWED:       MOSFET model, MOSFET tests
DEPENDENCY TEST: basic DC solver
PASS:          measured current matches model tolerance
DO NOT TOUCH:  UI, battery, magnetics, reinjection, other primitives, build definitions
```

This prevents scope creep.

## Bug triage — classify before touching anything

Every failure must first be classified into exactly one type, and the fix goes to
that type's owning layer.

| Type | Problem class | Example | Fix in |
|---|---|---|---|
| A | Rule problem | Pass/fail definition is ambiguous | `00_RULES` |
| B | Part problem | Capacitor ESR is wrong | `01_PARTS` |
| C | Connectivity problem | Breadboard rows that should connect are treated as separate | `02_CONNECTIONS` |
| D | Solver problem | Parallel resistance gives wrong current | `03_ELECTRICAL_CORE` |
| E | Time problem | RC decay timing is wrong | `04_TIME_AND_DYNAMICS` |
| F | Measurement problem | Circuit calculation is correct but the differential meter gives an incorrect value | `05_MEASUREMENT` |
| G | Primitive problem | The hysteresis arrangement is wired incorrectly | `06_PRIMITIVES` |
| H | Magnetic problem | Mutual coupling is wrong | `07_MAGNETICS` |
| I | Power problem | Battery voltage does not sag under load | `08_POWER` |
| J | Test problem | Expected value in a regression is itself incorrect | `09_TESTS` (do not change working physics to satisfy a wrong test) |
| K | Interface problem | Oscilloscope draws the wrong scale but the underlying samples are correct | `11_INTERFACE` |

## Cross-layer change rule

Sometimes the actual problem genuinely crosses an interface. That does not permit
a general rebuild.

Example — allowed: a newly improved capacitor model requires the transient engine
to accept one new state value → touch `01_PARTS/capacitor` and
`04_TIME_AND_DYNAMICS/interface`.

Not allowed in the same change: rewrite the electrical solver, rewrite
measurement, rewrite the UI, rewrite primitives.

Every additional layer touched must have a stated reason.

## Change budget

Before editing, write:

```
PRIMARY LAYER:
SECONDARY LAYER IF REQUIRED:
WHY:
FILES EXPECTED TO CHANGE:
TESTS TO RUN:
```

If implementation suddenly needs five unrelated layers, **stop**. That usually
means the task has drifted or the architecture boundary itself is wrong — raise
it as a Type A (rule) problem rather than pushing the change through.

## Worker ownership handoff

When one worker finds a problem owned by another layer, they do not fix it
casually. They write a failure receipt (see `10_RECEIPTS/`) naming the layer,
expected value, actual value, and a reproduction, and hand it off. The owning
layer's work then follows this same cycle from step 1.
