# Primitive One-Wave Differential Simulator

This is the smallest runnable One-Wave simulator in the science repo.

It contains only:

- a live center reference
- signed expression/compression state
- restoring motion around center
- retained directional hysteresis
- the locked seven named bands
- the six unnamed transition gaps
- octave scaling as an explicit derived view

It does **not** assume particles, gravity, or a pre-existing field ontology.

## State

q in [-1,+1]

Mapped to the locked 0–100 One-Wave scale:

W = 50 + 50q

## Dynamics

The current primitive update is:

a = drive - k*q - damping*v + memory*held

This is a minimal test equation, not a claim of fundamental physics.

## Purpose

This simulator is the bottom testbed for:

reference -> differential -> point -> path -> field

Later stages may replace the primitive update rule, but they should preserve the same transparent state and measurement conventions.
