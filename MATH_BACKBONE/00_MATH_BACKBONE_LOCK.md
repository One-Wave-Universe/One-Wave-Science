# ONE-WAVE MATH BACKBONE — LOCKED PROTOCOL

Status: **PROTECTED / APPEND-ONLY AFTER ADOPTION**

The mathematics under this directory is the canonical scientific spine of One-Wave work.

## Non-Diminishment Rule

Canonical mathematics may be expanded but not diminished.

Do not:
- replace equations with prose;
- summarize away derivation steps;
- remove assumptions because they appear obvious;
- remove units, dimensions, domains, boundary conditions, initial conditions, tolerances, or uncertainty;
- erase failed derivations or failed comparisons;
- silently change symbols or definitions;
- overwrite an older derivation with a corrected one.

## Version Rule

Once a math file exists on `main`, normal repository updates may not edit or delete it.

A correction must be a new versioned file.

Example:

- `20_measurement_bell_v1.md`
- `20_measurement_bell_v2.md`

The newer file must identify:
1. the exact earlier file it supersedes;
2. the exact equation or assumption that changed;
3. why it changed;
4. downstream nodes affected;
5. whether the status remains YELLOW / OPEN or becomes stronger.

The older file stays present as an audit record.

## Required Mathematical Shape

A mature mathematical node should preserve, where applicable:

1. variables and symbol definitions;
2. units / dimensions;
3. domain and coordinate conventions;
4. starting assumptions;
5. governing equations;
6. derivation steps;
7. boundary and initial conditions;
8. free parameters and where they came from;
9. predicted observables;
10. accepted comparison target;
11. uncertainty / tolerance;
12. falsification or kill condition;
13. explicit PASS / FAIL / UNRESOLVED result;
14. dependencies upstream and downstream.

## Explanation Rule

Plain-language explanations are encouraged.

They are always additional.

They never replace canonical mathematics.

## Rebuild Rule

If a chapter or node contains a physical claim but its earlier mathematics has fallen out, mark:

**MATH-REBUILD-REQUIRED**

Recover the original derivation if available. If it cannot be recovered, derive a new explicitly versioned replacement and label it as newly reconstructed rather than pretending it is the lost original.

## Reference Rule

Before changing any scientific node:
- reference `CORE_RULES_LOCK.md`;
- reference the relevant file in this directory.

After the change:
- verify the core rules again;
- state exactly what math was preserved, added, superseded, or remains missing.

This protocol is part of the One-Wave anti-drift system.
