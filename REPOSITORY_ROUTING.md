# One-Wave Repository Routing Authority

Status: current routing rule, 2026-09-24.

## Canonical repositories

1. One-Wave-Science — science only: hypotheses, mathematics, evidence, scientific nodes, theory, scientific datasets, falsification material, and science-facing simulations.
2. Builds — hardware, software implementations, Android, CELL_V1 build packets, Virtual Breadboard, applications, editors, runtime prototypes, and speculative build material.
3. Mythos-and-Stories — fiction, narrative world-building, stories, and non-science creative material.
4. Bridge-Comand — terminal access, Hive Pipe, bridges, relays, AI control/runtime instructions, Jetson access, external-work transport, and connector recovery.

Bench is not a destination. Bench content must be dissolved into one of the four repositories above.

## Hard placement rules

- No Virtual Breadboard, hardware build packet, Android implementation, Animator, Miniverse runtime, or other build payload belongs in Science.
- No Hive Pipe, terminal bridge, relay, SSH/Jetson access runtime, or AI transport control belongs in Science.
- Science may reference implementations in Builds and transport mechanisms in Bridge-Comand, but must not duplicate their executable payloads.
- Science data and scientific-analysis code may remain in Science when they directly support reproducible scientific comparison or falsification.
- Generated caches and transient build artifacts are never committed.
- Move first, verify the destination copy, repair references/tests, then remove the obsolete source copy.

## Cross-repo references

Build implementations:
https://github.com/One-Wave-Universe/Builds

Bridge and relay runtime:
https://github.com/One-Wave-Universe/Bridge-Comand

Narrative material:
https://github.com/One-Wave-Universe/Mythos-and-Stories
