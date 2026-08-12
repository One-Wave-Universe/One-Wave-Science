---
node_id: "G-734"
canonical_name: "Standard-Mechanics Control Run"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Evaluation, Control, and Route Grammar / Simulation Governance"
claim_gate_detail: "YELLOW (procedural requirement, no physics claim of its own)"
metadata_standard: "I-06"
---

# Node G-734: Standard-Mechanics Control Run

**Dependencies**
Upstream: G-706 Validation, D-412 Lattice Simulation and State-Driven Visualization Standard
Lateral: I-02 proof lifecycle
Downstream: G-735 Prediction-Difference Gate, G-737 No Victory Without Observable Match; also the Solar-System All-Body Differential Simulation backlog item (RELATIONAL_MECHANICS_NODE_BACKLOG.md)

## Rule

Every simulation built from the relational-mechanics backlog
(`RELATIONAL_MECHANICS_NODE_BACKLOG.md`) must be run twice on the
identical initial state and identical measurement schedule:

```text
Run A: One-Wave relational update (A-118/C-327-family primitives)
Run B: standard mechanics (Newtonian gravity, ordinary numerical integrator)
```

Both runs must use the same integrator tolerance, timestep, and body
set. The control run (B) is not optional and is not permitted to be
represented only by a literature value — it must be an actual
execution against the same code path's measurement harness as run A,
so both outputs are directly comparable under D-412's standard
(`simulation state -> measured fields -> visualization`).

## Why This Is Its Own Node

G-706 Validation already requires "confirmation through successful
participation in a cycle." G-734 makes that concrete for this backlog
specifically: a relational-mechanics run's "successful participation"
is only meaningful relative to the standard-mechanics control run on
the same inputs. Without the control run, an orbit that merely stays
bounded cannot be told apart from a correct orbit, a lucky orbit, or a
numerically stable but physically wrong orbit.

## What Counts as a Valid Control

- Same body masses, positions, and velocities at `t=0`.
- Same total simulated duration and same sampling cadence for
  measurements.
- A named, reproducible standard integrator (e.g. a documented
  symplectic or RK-family integrator) rather than an unspecified
  "known good" result.

## Failure / Revision Conditions

This node fails if a relational-mechanics result is reported without a
control run on identical initial conditions, or if the control run
uses different tolerances, timesteps, or body sets than the relational
run it is meant to be compared against.
