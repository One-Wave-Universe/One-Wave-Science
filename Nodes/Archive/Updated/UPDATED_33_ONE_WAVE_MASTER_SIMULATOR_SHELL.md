# Updated 33 - One-Wave Master Simulator Shell

Updated 33 adds the first unified entry point for the One-Wave physical simulation ladder.

## Added

- `OPEN_ONE_WAVE_SIMULATOR.html` at repository root;
- `One_Wave_Simulator/index.html`;
- stage navigation for the canonical D-412 physical simulation ladder;
- the existing D-413 Ground Lattice Orbital-Restoring Lab embedded as Stage 01;
- a full-screen lab launcher;
- dimensional, geometry, coordination, cluster, and gate declarations;
- explicit current-scope and next-test panels;
- visible but locked placeholders for later simulation stages.

## Design rule

The master program does not pretend that unfinished stages already run. A stage remains locked until it has declared state, an update law, measurements, raw results, controls, failure tests, and the native-dimensional declaration required by A-117 and D-412.

## Current runnable stage

Stage 01 is D-413:

```text
native-2D triangular Ground
-> derived hexagonal-neighborhood view
-> imposed curvature well
-> bounded displacement shell
-> restoring translation and calculated torque
-> synchronized state-driven views and measurements
```

D-413 remains a Yellow reduced model. The well is imposed and the shell is a collective coordinate. Updated 33 does not promote or claim gravity, quarks, protons, charge, Mirror Gate, or Mass Effect.

## Next build target

The next stage is not “quark animation.” It is the circulation-emergence laboratory:

1. seven-cell displacement and release;
2. ring-circulation input;
3. circulation and vorticity calculated from the velocity field;
4. persistence-under-loss measurement;
5. boundary-leakage and recovery measurements;
6. stable/unstable parameter map;
7. ablations and simpler control geometries.
