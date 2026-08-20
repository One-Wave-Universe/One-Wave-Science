# Field Coder — Locked Build Scope

## Project identity

This project builds the **Field-side coding agent**.

It is not the combined Field/Void system.
It is not the Void agent.
It is not the animation/story engine itself.
It is the coding agent that will later be able to work on those programs.

## Field role

Field reconstructs the current program state, receives a coding goal, narrows it into one targeted task, inspects relevant repository evidence, proposes one implementation, performs one controlled change, compares intended versus actual diff, runs evidence-producing checks, learns from failure, and prepares a review-ready result.

Field does not approve itself as architecturally correct. External Void/Admin review comes later.

## Build objective

Produce a reliable Field coding engine that can take one narrow software task from:

`goal -> reference -> inspect -> propose -> edit -> diff -> test -> learn/retry -> review-ready result`

without wandering into unrelated work or losing project state.

## Scope lock

This scope carries forward to every Field Coder branch and step.

A step may extend implementation only inside this scope. Any proposed scope change must be recorded as a blocked architecture decision rather than silently implemented.