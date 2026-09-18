# Engineering Validation — Chapter 1
# From Interesting Build to Defensible Build

A One-Wave build is not considered correct because the diagram is symmetric or because an analogy feels right.

The required chain is:

```text
real reference or established research
-> exact mechanism borrowed
-> One-Wave change/hypothesis
-> measurable build
-> conventional/null control
-> acceptance/failure rule
-> retained receipt
```

## Five statuses

**REFERENCE-REAL** means the underlying engineering mechanism is established.

**MODEL PASS** means a model produced the expected behavior.

**BENCH-REALITY PASS** means the proposed parts, power, drive, current, return path, and measurement method could physically work.

**PHYSICAL PASS** requires actual measured hardware.

**ONE-WAVE HYPOTHESIS** marks the part unique to the project that still needs testing.

## Examples

A TLE2426 is real. Using it as a low-current midpoint reference is grounded engineering. Using it as a motor return is not.

A six-switch three-phase inverter is real. A rotating stator field from controlled commutation is real. Calling any three sequential coil pulses a conventional three-phase motor drive without measuring phase/current is too loose.

Memristive and magnetic nonvolatile memories are real. Claiming that a repeated CELL_V1 route physically learns must still be measured against an untrained control.

ngspice is a real external simulator reference. A home-built simulator becomes credible by matching selected ngspice cases, not by calling itself SPICE-compatible.

A Jetson terminal bridge is a software build. It must identify the exact Jetson hardware, OS/runtime assumptions, endpoint, smoke test, and failure recovery.

## Rule

Whenever a build has no real precedent for the novel part, that is acceptable — but it must say **experimental** and provide the test that could make it fail.
