# One Wave Hybrid Physics Architecture

## One state, three accountable channels

The simulator advances one barycentric state. It does not run three competing
universes. The acceleration used by the integrator is

```text
a_total = a_Newton + a_1PN + a_OneWave_closed + a_boundary
```

- `a_Newton` is the Gray bulk N-body control.
- `a_1PN` is the leading solar relativistic correction. A future precision
  build should replace it with SPICE/Horizons initial states and a full
  Einstein-Infeld-Hoffmann implementation.
- `a_OneWave_closed` is the candidate internal displacement, rotation, wake,
  EM, or phase-lock channel after conservation closure.
- `a_boundary` is reserved for an explicitly declared external Field boundary.
  It may not be hidden inside an internal interaction.

Every timestep emits the norm, force balance, and torque balance of the
channels. A visual element may read this state; it may not invent another
position clock.

## Conservation gate

The current closure removes the mass-weighted uniform acceleration and rigid
rotation components of a candidate internal acceleration. Therefore the
candidate can redistribute motion without creating net linear or angular
momentum. This is a numerical gate, not the final One Wave derivation.

## What still needs physics

The One Wave channel is deliberately zero by default. To become nonzero it
requires all of the following:

1. a dimensionally complete Field state and evolution equation;
2. a map from extended Field measurements to body-scale acceleration;
3. an energy functional or flux ledger matching the momentum/torque closure;
4. a moving-wake transport law;
5. a phase-lock transfer rule with build, hold, break, and hysteresis;
6. a prediction that differs from the Gray+relativity control;
7. refinement and ephemeris comparison showing the result is not numerical
   error or parameter fitting.

## Scale transition

The planetary solver and subatomic Field solver do not share arbitrary display
units. Each scale must declare characteristic length, time, energy, and Field
amplitude before a cross-scale coupling is allowed. Camera zoom is presentation;
it is not a physical scale-transfer equation.
