---
node_id: "G-737"
canonical_name: "No Victory Without Observable Match"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Evaluation, Control, and Route Grammar / Simulation Governance"
claim_gate_detail: "YELLOW (procedural requirement, no physics claim of its own)"
metadata_standard: "I-06"
---

# Node G-737: No Victory Without Observable Match

**Dependencies**
Upstream: G-735 Prediction-Difference Gate, G-736 No Hidden Controller Rule
Downstream: the Scale-Recurrence Validation, Finite-Propagation Validation, Three-Body Silver-Bullet Benchmark, and Full Solar-System Benchmark backlog items (RELATIONAL_MECHANICS_NODE_BACKLOG.md)

## Rule

A relational-mechanics simulation is not permitted to declare success
on the basis of "the orbit stayed bounded" or "nothing blew up" alone.
Success requires hitting a **defined, quantitative observable stated
before the run**:

```text
- a specific orbital element (semi-major axis, eccentricity, period)
  within a stated tolerance of an ephemeris or documented value;
- a specific resonance-gap location/width matching a documented
  Kirkwood-gap or libration-amplitude measurement;
- a specific gravity-assist energy change matching a documented
  mission flyby result (C-332);
- or an explicitly stated departure from the standard-mechanics
  control run (G-734) that itself matches an observation, per G-735.
```

The observable and its tolerance must be declared before the run, not
selected afterward from whichever quantity happened to match.

## Why This Is Necessary Given G-736

G-736 removes the possibility of a hidden controller forcing a
plausible-looking result. G-737 closes the remaining gap: even with no
hidden controller, a simulation can still "succeed" vacuously by
reporting only that it did not diverge, which is a much weaker claim
than reproducing (or meaningfully departing from, per G-735) a real
measured quantity. Bounded-but-untested is not success under this
node.

## Relation to the Benchmark Nodes

This is the acceptance criterion the backlog's benchmark items (the
Trojan test, the Kirkwood test, and the Three-Body and Full
Solar-System benchmarks, all mapped) must each satisfy individually
— each benchmark's own "what counts as passing" must be one or more
G-737-style declared observables, not a qualitative description of the
simulated trajectory.

## Failure / Revision Conditions

This node fails if a simulation report claims success without listing
the specific observable(s) matched and their tolerances, or if the
observable was chosen after seeing the run's output rather than
declared beforehand.
