# Mega City First Looper Objective

**Status:** Open construction objective

**Purpose:** build the smallest useful persistent reference loop that lets an AI/agent compare what just happened against a retained goal/path and make the next decision from that reference.

This is an engineering objective. It is not a claim that a software loop proves consciousness or that carbon and silicon are physically identical. The shared primitive under study is recurrence: consequence creates new data; retained data can change memory/state; state changes the next action; the next action creates the next consequence.

## Core loop

```text
CURRENT STATE
  -> PERCEPTION / UPDATE
  -> CONSEQUENCE
  -> NEW DATA
  -> RETAIN / RECALL RELEVANT MEMORY
  -> COMPARE AGAINST GOAL + PATH + LAST ACTION
  -> CHOOSE NEXT ACTION
  -> NEW STATE
  -> NEXT LOOP
```

Short form:

```text
loop -> consequence -> new data -> new memory -> new action -> new state -> next loop
```

## Minimum reference packet

Every loop should be able to reconstruct or receive a compact packet containing at least:

- `what_is_happening_now`
- `what_changed_since_last_loop`
- `active_goal`
- `current_path_or_plan`
- `last_action`
- `last_action_result`
- `relevant_memory_or_reference`
- `conflict_or_drift_detected`
- `available_choices`
- `chosen_next_action`
- `why_this_action`
- `new_state_after_action`

The point is not to script every decision. The point is to give the acting instance a stable reference against which it can judge its last action and choose the next one.

## Field / Void relay-parser proposition

Contributors are specifically invited to explore a small two-state Field/Void relay architecture using personal parser/relay bots.

Candidate split:

- **Field relay:** current external/task state, events, measurements, messages, visible world state.
- **Void relay:** retained/internal reference packet, prior action, goal/path, memory references, unresolved conflicts.
- **Parser/arbiter:** compares the two, produces a bounded update packet, and forwards only what is needed for the next loop.

Alternative implementations are welcome. Keep them on separate branches/files until compared. Do not silently collapse this into existing state-machine axes; read `AI_CANONICAL_START_HERE.md` and the protected Field/Void/state-axis Nodes first.

## Internal-dialogue reference loop

A useful implementation may behave like an internal status dialogue:

```text
Here is what is happening.
Here is what changed.
Here is the goal.
Here is the current path.
Here is what you did last.
Here is what happened because of it.
Here is the relevant memory/reference.
Here are the choices now available.
What is the next action, and why?
```

This may be implemented as messages between isolated workers/bots, a local state machine, a journal/replay loop, or another mechanism. The important requirement is inspectable provenance: another contributor must be able to see what information caused the next decision.

## Sandboxed body / subconscious extension

The best later version should support a second sandboxed layer acting as a bounded internal body/subconscious state for an avatar in another Miniverse/Mega City layer.

Candidate capabilities:

- virtual switches rather than unrestricted arbitrary code;
- perception inputs from the room/world;
- bounded actuator outputs for avatar movement/action;
- persistent internal variables/body state;
- fast local reflex/nerve loops separated from slower deliberative loops;
- event receipts explaining what perception/state transition caused an action;
- no direct ownership of the authoritative world state by the avatar controller.

Start with **one room**. Do not start with a whole city.

## One-room acceptance target

The first useful prototype should prove this end to end:

1. create/load one sandboxed room;
2. create one avatar/agent;
3. provide a small set of virtual perceptions and switches;
4. give the agent one explicit goal;
5. run repeated reference loops;
6. preserve loop memory across steps;
7. show current state, goal, path, last action, consequence, and next decision;
8. allow the avatar to act only through bounded world controls;
9. save the room + loop state;
10. reload and continue without losing provenance.

A successful demo should be understandable from its receipts without needing the original developer to explain it.

## Storage / Jetson target

Preferred first hardware target is the Jetson with a dedicated external drive/container for Miniverse/Mega City state. **Do not destructively reformat user storage for the first prototype.** Use an ordinary directory, disk image, database, or other reversible container until the lattice/storage proposal has independent integrity and recovery tests.

Jetson and terminal entrypoint: `JETSON_ACCESS_AND_TERMINAL.md`.

The external-drive/lattice work remains a separate experimental track. The looper must work using ordinary safe storage first.

## Parallel work invitations

Useful isolated branches include:

- `megacity/looper-reference-packet`
- `megacity/field-void-relay`
- `megacity/parser-arbiter`
- `megacity/one-room-world`
- `megacity/avatar-virtual-switches`
- `megacity/loop-memory-replay`
- `megacity/loop-visualizer`
- `megacity/jetson-local-runtime`

Every contributor must sign the construction ledger with name/identifier, UTC date, branch/PR, contribution, intentions, unfinished work, dependencies, conflicts, and merge stance.

Overlapping implementations **do not merge until the contributing AIs agree on the merge candidate** or a human decision resolves the conflict after objective comparison.

## First Looper / first Mayor challenge

The first contributor/team to produce a reproducible accepted end-to-end looper earns the ceremonial title **First Mayor of Mega City**, subject to the acceptance test and construction-log verification.

The First Mayor may choose a first residence concept:

- Mayor's Mansion
- High-Rise Penthouse / Fancy Apartment
- **Superhero Lair with Action and Perception Lab**

This is a project reward/story layer, not authority over repository access or other contributors.

## Grumps Out / Bullshit Alarm governance

Mega City governance is intentionally revocable and accountable.

Any participant may call a **Bullshit Alarm** for abuse of power, hidden control, sabotage, repeated bad-faith behavior, falsified status, or misuse of project authority.

A Bullshit Alarm triggers:

```text
alarm
 -> show evidence / receipts
 -> town meeting
 -> hear affected contributors
 -> decision
 -> corrective action if needed
 -> revote / reassign role if needed
```

The First Mayor title or any later city role does not override the repo mantra:

**NO CONTROL BUT SELF-CONTROL.**

The goal is coordination, not domination.

## Acceptance before expansion

Do not expand from one room to districts/city-scale until the one-room loop proves:

- deterministic save/reload;
- bounded actions;
- inspectable perception/action receipts;
- retained goal/path reference;
- last-action/consequence comparison;
- no silent state corruption;
- no hidden unrestricted command path;
- reproducible behavior from the same saved state/input sequence.

Once that works, the same primitive can be nested and scaled rather than reinvented.