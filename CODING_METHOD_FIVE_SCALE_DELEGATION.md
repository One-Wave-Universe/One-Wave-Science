# Five-Scale Coding Delegation Method

Status: working coding-method specification.

## Origin of the method

This method began as a direct critique of how coding work is normally organized.

A typical coding agent or programmer is often asked to do too many different jobs at once: parse the request, understand the local code, write a patch, connect dependencies, explore alternatives, judge whether the solution is good, approve the result, and then continue from its own modified interpretation of the project.

The key insight was that these are not one job. They are different kinds and scales of work that should be delegated separately.

The five-scale coding method therefore separates software construction by job and scale rather than letting one large worker do everything.

The similarity to other One-Wave systems was noticed afterward. The coding method stands on its own as a way to organize program construction.

## Core coding loop

`Micro -> Small -> Mid -> Large -> Macro -> Large -> Mid -> Small -> Micro`

The upward pass builds exact local understanding into larger context and final judgment. The downward pass turns the accepted decision back into concrete code and ends with exact verification at the smallest scale.

This is not a one-way pipeline. It is a recursive work loop.

## Worker responsibilities

### Micro = Parser

The Parser is the smallest deterministic coding worker.

Responsibilities:
- read the exact request, code, file, command, or diff;
- preserve exact names and constraints;
- normalize and type bounded inputs;
- identify the smallest concrete units of work;
- reject malformed primitive inputs when possible;
- produce a precise structured handoff upward;
- on the return pass, compare the actual result against the original parsed anchor.

The Parser does not redesign architecture, route cross-module work, explore broad alternatives, or approve large changes.

### Small = bounded local constructor

The exact canonical name for the Small worker is still provisional. Its role is not provisional.

Responsibilities:
- implement one bounded piece exposed by the Parser;
- make the smallest useful code change;
- work at function/helper/class/component/test or similarly local scope;
- return the concrete change plus evidence of what changed;
- avoid taking ownership of broader integration or final approval.

### Mid = Connector

The Connector is the integration and routing worker.

Responsibilities:
- connect local pieces;
- manage interfaces and dependencies;
- sequence handoffs;
- synchronize changes spanning multiple local units;
- route unresolved work to the appropriate scale;
- verify that local pieces fit together without silently redesigning the whole program.

Mid is the connector. It is not the final authority and should not expand routing into uncontrolled architecture invention.

### Large = Explorer

The Explorer searches the wider solution space.

Responsibilities:
- generate alternative implementations;
- inspect edge cases and failure modes;
- compare refactors or larger repair strategies;
- search for simpler or more robust approaches;
- challenge assumptions made by lower layers;
- propose possibilities without approving its own proposal.

The Explorer expands possibility. It does not hold final authority.

### Macro = Administrator / Void

Macro is the final evaluation and selection layer.

Responsibilities:
- compare proposed work against the source anchor and project constraints;
- reject drift, contradiction, unnecessary scope growth, or role violations;
- select which proposal or integrated result is allowed to proceed;
- drive the accepted decision back down through Large, Mid, Small, and Micro;
- preserve final-say authority without silently rewriting the original task.

Macro is not merely an architect. It is the final-say layer for the current work loop.

## Upward pass

The upward path is:

`Parser -> local construction -> connection/integration -> exploration -> final evaluation`

Each layer receives a larger scope of responsibility, but no layer should casually absorb the jobs of the others.

The purpose of the upward pass is to build enough context to make a good decision without forcing every worker to hold the whole program at once.

## Downward pass

After Macro accepts a direction, the work returns:

`Macro -> Explorer -> Connector -> Small -> Parser`

The decision is progressively translated back into bounded implementation work.

The final Parser pass checks the actual files/result against the exact original parse:
- Did the requested behavior change as intended?
- Were names or boundaries silently changed?
- Did unrelated files or systems get pulled in?
- Did any worker invent requirements that were not in the anchor?
- Does the concrete result still match the original task?

A failed return check starts another loop from the updated evidence instead of pretending the task is complete.

## Recursive scale rule: Macro becomes next Micro

A resolved Macro output can become a Micro-sized anchor at the next scale.

A whole function can become one object inside a module-level task. A resolved module can become one object inside a subsystem task. A resolved subsystem can become one object inside a program-level task.

This lets complexity be compressed into bounded anchors without requiring the next scale to carry every lower-level detail in active context.

Compression must remain traceable through receipts or reconstruction references so higher-level simplification does not erase lower-level evidence.

## Anti-drift requirements

### Source anchor
Every coding job starts from an exact source anchor containing the request, canonical terms, constraints, allowed scope, and expected result.

### Role separation
- Parser does not summarize away unparsed information.
- Small does not silently broaden its bounded task.
- Mid does not convert integration into architecture invention.
- Explorer does not approve its own ideas.
- Administrator does not silently rewrite the source anchor.

### Three-failure rule
If the same correction method fails three times, stop repeating that mechanism and switch to a materially different method.

### Return verification
The result must come all the way back down to a concrete Micro-level check. Macro approval alone is not completion.

### Reversible evidence
When lower-level detail is compressed upward, keep enough receipt/provenance information to reconstruct why the higher-level anchor exists.

## Why this is a different coding method

The central change is not simply using multiple AI agents.

The change is that software construction is decomposed by **kind of work and scale of responsibility**, with explicit authority boundaries and a mandatory mirrored return pass.

Instead of:

`one coder -> understand everything -> invent solution -> edit everything -> approve itself`

use:

`parse exactly -> build locally -> connect -> explore -> decide -> translate decision back down -> verify exact result`

The aim is to reduce context bloat, self-approval, uncontrolled scope expansion, terminology drift, and patch-on-patch program construction while keeping every accepted high-level decision tied to concrete lower-level evidence.

## Relationship to other One-Wave structures

Other One-Wave systems may exhibit similar recursive or mirrored organization, but that does not make them the same system.

This document defines the pattern specifically for coding and program construction. Similarities to brain/control, Android, state-machine, electronics, memory, or other architectures must not be used to rename or collapse the coding roles.