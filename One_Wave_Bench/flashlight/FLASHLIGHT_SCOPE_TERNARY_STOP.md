# Flashlight Scope — Ternary Three-Winding Stop

This file narrows the flashlight target without changing the broader One-Wave architecture.

## Default flashlight stop point

The flashlight does **not** need to reach QC-RC / quadratic rotating-field behavior.

The default useful target is:

```text
single virtual ground / CENTER reference
        ↓
BC-DC center-referenced differential
        ↓
ternary - / HOLD / + control
        ↓
three-winding nerve element
        ↓
bidirectional MOSFET nerve gates
        ↓
state-triggered reinjection
        ↓
useful light output
```

This is enough to count as the first balanced-flashlight prototype if it is physically coherent, reference-resolved, and measurably useful.

## Three windings belong to the ternary nerve layer

The three-winding element is not automatically QC-RC and is not automatically a brain cell.

Its intended flashlight role is fast local ternary routing/control:

```text
-1 / HOLD / +1
```

with every winding and gate interpreted against the same CENTER reference.

The three windings may support opposed/local routes, state retention, reinjection control, color/brightness routing, or another measured flashlight function. The exact assignment must come from the working circuit rather than being forced in advance.

## Quadratic / rotating field is optional follow-on

QC-RC, rotating magnetic-field experiments, a third spatial axis, and eventual `Bx/By/Bz` measurement remain valid later experiments.

They are **not** required for the flashlight to pass.

Only add QC-RC to the flashlight if the ternary three-winding build leaves a real measured problem that rotation solves or a useful capability that cannot be achieved at the ternary nerve layer.

Do not add quadratic behavior just to continue the architecture sequence.

## Flashlight pass criteria

Required:

1. one CENTER / virtual-ground reference from source through control and reinjection;
2. measurable differential state around CENTER;
3. ternary `- / HOLD / +` behavior that is produced by the circuit, not a binary logic chip pretending to be ternary;
4. three-winding element with independently measurable winding voltage/current/polarity;
5. bidirectional MOSFET nerve gate behavior where bilateral routing is required;
6. state-driven reinjection: decay reaches a physical threshold, reinjection occurs, state restores, source disconnects, coast resumes;
7. no timer required to decide when to reinject;
8. useful light remains measurable;
9. conventional flashlight stays a control/reference only.

Optional:

- TC-AC if the working ternary control needs an oscillatory handoff;
- QC-RC / rotating-field behavior;
- quaternary or quinary state structure;
- 3D field claims.

The prototype stops at the last useful measured layer.
