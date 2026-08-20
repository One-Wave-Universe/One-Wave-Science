# FIELD CODER — MASTER PROJECT GOAL

## MASTER PROJECT GOAL

Build the Field half of the complete **Field/Void CPU-GPU state-machine coding engine** for autonomously building, modifying, testing, debugging, and improving real software, applications, and programs.

The complete system has four distinct roles:

- **Field**: expressive/generative software movement. Field creates candidate state transitions and bounded coding actions.
- **Void**: separate mirrored oversight/override. Void evaluates Field movement and may ALLOW, CORRECT, OVERRIDE, HOLD, or ESCALATE. Void logic is not implemented inside Field branches.
- **M4 / OpenClaw controller**: fast routing, timing, state selection, branch-loop control, and handoff between Field and Void.
- **Administrator / ChatGPT escalation**: higher-level architecture decision and help when Field/Void cannot safely resolve a blocked state.

These Field branches build the actual Field state-machine computation, not a generic chatbot wrapper and not a provider-specific model orchestration system.

## CANONICAL FIELD/VOID MACHINE

The engine must preserve these primitives as executable state, not metaphor:

- **6 Steps**: Begin -> Build -> Hold -> Build -> Break -> Loop.
- **5 Field states / scale bands**: Micro/Floor, Small/Low, Medium/Mid, Large/High, Macro/Extreme.
- **4 Views**: Inward, Outward, Across, Over.
- **4 Operators**: -, +, /, x.
- **3 Moves**: Compress (-1), Hold (0), Expand (+1).
- **2 Choices**: mirrored polarity choice; Field choice selects/creates the active field.
- **1 Field / Mirror / Void reference**: shared reference boundary/zero.

Gate order:

`1 -> 2 -> 3 -> 4(0) -> 5 -> 6`

and mirrored return:

`6 -> 5 -> 4(0) -> 3 -> 2 -> 1`

Gate 4 is also Gate 0: mirror/null/flip/boundary.

Canonical mirrored relations:

- F2 Choice <-> V5 Scale
- F3 Motion <-> V4 Action
- F4 View <-> V3 Interpretation
- V2 Choice <-> F5 State
- outer F1/V6 and V1/F6

Motion contains Point, Path, and Field Rotation. Each motion mode can carry Carrier, Breathing, and Phase behavior.

Field-context law: no state is interpreted outside the currently selected active field.

Recursion law: each 1-6 step may contain the full nested chain.

## FIELD BRANCH OUTPUT

The Field build must eventually provide a provider-neutral, AI-callable software interface that can:

1. receive an explicit coding goal and current program/repository state;
2. encode that state into the canonical Field machine;
3. compute deterministic Field transitions on CPU;
4. compute equivalent batched transitions on GPU where appropriate;
5. preserve reference, differential, state, scale, motion, view, gate, and history;
6. emit one bounded candidate software movement/action at a time;
7. preserve evidence and state across iterations;
8. hand the candidate and evidence to the separate Void oversight/override side;
9. accept M4 routing/control without binding the engine to one AI provider;
10. serve real coding, app-building, and program-building workloads.

## SCOPE LAW

Every Field branch is one preplanned implementation stage of this exact project.

The complete coding plan is defined before implementation. Branches are fixed work slots. A branch may implement only its assigned stage, must preserve prior verified behavior, must test every change, must record what worked and failed, and must stop at its explicit hard stop.

No branch may redefine the master project goal, replace the state-machine engine with generic agent orchestration, merge Void implementation into Field, or implement future branch work early.