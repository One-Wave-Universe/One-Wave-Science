# Magnetic / Spintronic Feedback Loop

**Status:** terminology and experiment boundary.

## Use the terms correctly

Hall sensors, search coils, encoders, ordinary motor windings, and magnetic remanence experiments are **magnetic/electromechanical feedback**.

Call a mechanism **spintronic** only when the actual device physics uses spin-dependent transport or torque, such as magnetic tunnel junction / STT-MRAM / SOT-MRAM-class devices.

References:
- STT-MRAM review: https://www.nature.com/articles/s44287-024-00111-z
- SOT-MRAM review: https://www.nature.com/articles/s44306-024-00044-1

## Current CELL_V1 feedback path

A practical first implementation may use:

```text
command DOWN:
controller -> gate/driver -> coil or stateful element

view UP:
current shunt + Hall/search coil/encoder + state readout -> controller
```

Those measurements can report:
- current;
- position;
- field magnitude/direction;
- retained state;
- phase/timing.

They are valid feedback without being called spintronics.

## If a real spintronic device is introduced

Record:
- exact part/device stack;
- write mechanism;
- read mechanism;
- switching threshold/current/voltage;
- retention;
- endurance;
- temperature dependence;
- whether the same physical element both changes state and stores the state.

Only then may the spintronic label be used for that path.

## One-Wave hypothesis boundary

The idea that views-up and actions-down form one mirrored processing-memory loop remains a hypothesis until a physical implementation demonstrates the claimed coupling.

G-778 applies.
