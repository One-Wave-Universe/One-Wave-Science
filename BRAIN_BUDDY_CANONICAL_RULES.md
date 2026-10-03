# Brain Buddy + Council Chamber — Complete Canonical Rules

This is the single consolidated rulebook for Brain Buddy and the Council Chamber, for Codex, Claude, and all other workers.

- Canonical entry (which implementation is Brain Buddy): `BRAIN_BUDDY.md`
- Current runtime behavior contract: `BRAIN_BUDDY_COUNCIL.md`
- Current implementation: `scripts/brain_buddy_council.py`

Where the current implementation does not yet satisfy a rule here, see **Implementation status** at the end. Those gaps are open work, not permission to ignore the rule.

---

## 1. Core Purpose

Brain Buddy is a real multi-AI working system.

Its purpose is to let a user talk naturally to one AI while that AI can:

- reference the current repository,
- use project metadata when necessary,
- answer independently,
- pass the answer into a shared Council,
- receive real reviews from other connected AIs,
- continue useful back-and-forth,
- expose disagreements and evidence,
- propose tests,
- and eventually help produce controlled repository updates.

The Council Chamber is the shared workspace where participating AIs understand the current project state and can review each other's work.

The human remains in control of the project.

## 2. Initial Council Members

Initial active members are:

- ChatGPT
- Gemini
- DeepSeek

Additional models can be added later.

Claude may have a seat but must not be required for Brain Buddy to function.

Any provider can be temporarily unavailable without stopping the rest of the Council.

## 3. Enter Through Any AI

The user should be able to interact through any supported AI seat.

Example: `User → Gemini`

Gemini should:

1. receive the question,
2. reference the project repository when appropriate,
3. use metadata when necessary,
4. create its own answer,
5. send that completed answer into the Council,
6. allow the other available members to inspect it,
7. receive challenges, improvements, or corrections,
8. continue useful back-and-forth,
9. return the useful Council result to the user.

The same applies when the user begins with ChatGPT, DeepSeek, or another authorized member.

The AI currently talking to the user is the **lead seat** for that request. It is not permanently the boss of the Council.

## 4. Preserve the Original Back-and-Forth

The original Brain Buddy behavior must be preserved. Conceptually:

```text
AI A
→ AI B
→ response
→ AI A
→ refinement
→ AI B
→ refinement
```

with additional Council members able to participate.

Brain Buddy must not be reduced to:

```text
ask everyone once → count votes → stop
```

Useful dialogue may continue while there is:

- meaningful disagreement,
- contradiction,
- missing evidence,
- an unresolved question,
- a better interpretation,
- a useful proposed test,
- repository uncertainty,
- or a substantial improvement still available.

There is no arbitrary fixed number of rounds.

## 5. No Artificial Thought Timer

AI loops finish when they finish.

Do not control reasoning by arbitrary timers. Do not implement rules such as:

- exactly five debate rounds,
- thirty-second thought limits,
- automatic agreement after a timeout,
- forced retries only because time elapsed.

Time may be recorded as metadata. Time does not determine truth.

Useful unresolved work determines whether another loop should occur.

## 6. Six-Step Architecture

Brain Buddy must follow the project's six-step structure.

The six steps are not only a top-level sequence. They are **nested** and **recursive**.

- The whole Brain Buddy cycle follows the six-step pattern.
- Individual AI workers may use the same six-step structure.
- A child task inside one step may itself open a six-step loop.
- A test may open a six-step loop.
- A repository change may open a six-step loop.
- A disagreement may open a six-step loop.
- A research subproblem may open a six-step loop.

The pattern is:

```text
parent six-step loop
→ unresolved step
→ nested six-step child loop
→ child result
→ return result to parent
→ parent continues
```

This may repeat at multiple levels.

## 7. Recursion Must Have Purpose

Nested loops must not exist merely to keep the system busy.

A child loop should return upward when it reaches one of these conditions:

- verified answer,
- useful conclusion,
- completed action,
- unresolved evidence gap,
- external dependency,
- required human decision,
- or clear failure state.

The child then returns its state to the parent. The parent resumes from that result.

## 8. Six-Step State Must Be Traceable

For substantial tasks, the system should be able to determine:

- current parent step,
- whether a nested child loop exists,
- which parent created the child,
- what the child is investigating,
- what result the child returned,
- and whether the parent is now able to continue.

This can be compact. It does not require huge logs. The goal is to prevent loops from becoming detached or repeating without purpose.

## 9. Repository First

For project work, the repository is the primary persistent reference.

The normal order should be:

```text
repository
→ relevant canonical files
→ relevant project files
→ metadata if needed
→ reasoning
→ validation
```

Not:

```text
AI memory
→ assumption
→ edit
```

Each AI should independently reference the repository rather than relying only on another AI's summary.

## 10. One-Wave Lens

For One-Wave work, the Council adopts the One-Wave repository lens first.

Order:

1. current One-Wave repository,
2. canonical start-here material,
3. relevant nodes, chapters, or files,
4. internal metadata,
5. external evidence or research when needed,
6. comparison of external evidence against the repository.

External research can inform the project. It must not silently redefine the project.

## 11. Metadata Rule

Metadata is supporting context. It is not the main reference.

Use metadata when necessary for:

- values,
- measurements,
- node identity,
- provenance,
- experimental status,
- branch or commit identity,
- timestamps,
- relationships,
- scientific references,
- or structured state.

Do not flood every request with unnecessary metadata.

## 12. Mandatory Re-Reference Rule

Any of these must trigger re-reference:

- confusion,
- assumption,
- drift,
- contradiction,
- uncertainty about project terminology,
- uncertainty about the authoritative version,
- disagreement over what the repository actually says,
- missing dependency,
- stale reference,
- uncertainty introduced by a nested worker.

The rule is:

```text
confusion     → reference
assumption    → reference
drift         → reference
contradiction → reference
```

The AI must not silently fill important project gaps with guesses.

## 13. Re-Reference Applies Recursively

The re-reference rule applies at every recursion depth.

A child worker does not inherit a questionable assumption merely because its parent made it.

If a nested worker encounters uncertainty, it independently references the authoritative project material.

## 14. Real AI Responses Only

The Council must use real provider responses.

Never fabricate:

- Gemini answers,
- DeepSeek answers,
- Claude answers,
- ChatGPT reviews,
- agreement,
- consensus,
- successful receipts,
- provider availability,
- completed review,
- or successful validation.

If a provider did not return a real answer, it did not participate.

## 15. Out to Lunch

If an AI cannot participate because of:

- usage limits,
- provider restrictions,
- subscription limits,
- authentication problems,
- quota,
- bridge failure,
- provider outage,
- or other temporary issues,

its seat displays:

```text
OUT TO LUNCH
```

The other AIs continue. Unavailable members must not unnecessarily block Council work.

## 16. Provider States

Useful provider states include:

- active,
- listening,
- thinking,
- speaking,
- reviewing,
- waiting,
- pending,
- offline,
- authentication failure,
- invalid return,
- out to lunch.

These states must not be confused. For example:

- transport connected does not necessarily mean provider authenticated;
- provider authenticated does not necessarily mean request received;
- request sent does not necessarily mean response received.

## 17. Shared Council Awareness

Each active Council member should receive enough shared state to understand the ongoing work.

Useful shared state may include:

- current project,
- current user question,
- current Baseline Zero,
- relevant repository references,
- important recent Council conclusions,
- unresolved disagreements,
- pending work,
- verified recent changes.

Do not dump giant transcripts into every AI. Use compact, relevant state.

## 18. Individual AI App Continuity

Where infrastructure permits it, an AI being used in its own provider app should still be able to access relevant Council context.

The goal is continuity between:

- Brain Buddy,
- Gemini app,
- ChatGPT,
- DeepSeek,
- and other connected member interfaces.

The shared context should be controlled and relevant rather than an uncontrolled transcript dump.

## 19. Internal Dialogue

Each AI should be able to think internally while listening to the Council. Conceptually:

```text
reference
→ view
→ internal dialogue
→ action
→ reference
```

Internal work can include:

- comparing evidence,
- reconsidering a position,
- preparing a challenge,
- preparing a test,
- evaluating another AI's response.

Not every private thought belongs in the shared Chamber. The shared Chamber receives meaningful outputs.

## 20. Speak and Think Modes

The Chamber should support both:

```text
think → speak
```

and

```text
speak → think
```

An AI may:

- reason privately and then publish a conclusion, or
- publish a tentative question or observation and continue reasoning based on Council responses.

This should support real conversation rather than rigid one-shot responses.

## 21. Green-Light Speaker

The shared Chamber should use a speaker token or green-light concept.

Multiple AIs may think at once. Only one shared speaker should dominate the shared communication channel at a given instant.

Other members can:

- listen,
- privately reason,
- prepare evidence,
- request to speak,
- queue a response.

Concept:

```text
many minds working
→ one shared microphone
```

## 22. Agreement Is Not Truth

The Council is not a voting machine.

Three agreeing AIs are not automatically correct. One well-supported objection may matter more than three shallow agreements.

Track:

- claims,
- objections,
- evidence,
- unresolved contradictions,
- tests,
- successful tests,
- reference corrections,
- decisions.

Consensus should mean approximately:

```text
no active material evidence-backed objection remains unresolved
```

not:

```text
majority vote says yes
```

## 23. Continued Deliberation

Ideas should gain or lose confidence as they survive:

- repository checks,
- alternate interpretations,
- counterarguments,
- tests,
- external evidence,
- repeated examination.

The first answer is not automatically the final answer.

The system should also stop once meaningful unresolved work is exhausted.

## 24. Recursive Council Work

A Council discussion may spawn another Council discussion as a child task. Example:

```text
parent question
→ one major issue is identified
→ child six-step Council loop opens
→ members investigate
→ result returns
→ parent resumes
```

Child work must return to the parent rather than becoming disconnected.

## 25. Private Workspaces

Each AI may have a private experimental workspace.

A worker can develop:

- a hypothesis,
- code,
- equations,
- a test,
- a draft,
- a proposed architecture.

It can later bring a useful piece into the shared Chamber.

Private experiments do not automatically become project truth.

## 26. Show-and-Tell

Workers should be able to bring material into the Chamber for review. Examples:

- short claim,
- file,
- experiment,
- proposed test,
- code change,
- equation,
- research result,
- architecture change.

The Council can inspect it before it becomes accepted project work.

## 27. Project Layers

Where appropriate, Brain Buddy should distinguish project layers such as:

```text
CANON        → current project assertions
LOGIC        → architecture, equations, interpretations, algorithms
BENCH / TEST → simulation, measurement, experimentation, validation
BUILD        → implementation
```

A change in one layer must not silently rewrite every other layer.

## 28. Baseline Zero

Brain Buddy needs a synchronized accepted project state. Call it **Baseline Zero**.

After a meaningful verified project change:

1. update appropriate material,
2. validate,
3. commit on a branch,
4. merge or authorize,
5. establish the accepted result as the new baseline,
6. have active workers re-reference it.

This prevents workers from continuing from incompatible project states.

## 29. Branch-First Rule

Never destroy the last known-good Brain Buddy version.

Development rule:

```text
known-good version
→ new branch
→ experimental change
→ real test
→ validation
→ retain improvement only if it works
```

A broken branch does not replace the working seed.

## 30. Known-Good Seed

The original working Brain Buddy back-and-forth is the seed.

All improvements should grow from a verified working state.

Do not throw away the working back-and-forth merely to install a more elaborate architecture.

## 31. Recovery by Successful Execution

When recovering Brain Buddy, do not simply look for the latest commit. Trace from the last actual successful execution.

Preferred recovery chain:

```text
successful response
→ matching session or receipt
→ bridge implementation
→ commit SHA
→ branch from known-good SHA
→ rerun same packet
→ verify actual return path
```

The newest commit is not necessarily the best recovery point.

## 32. Receipts

Receipts are proof that an exchange occurred. They should remain compact.

Useful linkage:

```text
request ID
↔ actual provider return
↔ matching result/status
```

A receipt proves execution. It does not prove correctness.

Do not fill the repository with unnecessary receipt clutter.

## 33. Provider Isolation

Every provider route should be independently replaceable and diagnosable. Conceptually:

```text
Brain Buddy core
→ ChatGPT adapter
→ Gemini adapter
→ DeepSeek adapter
→ Claude adapter
→ future adapters
```

A broken provider should not unnecessarily break the others.

## 34. No Fake Multi-Agent Simulation

Brain Buddy must not pretend that one AI is multiple providers.

If a real Gemini call did not occur, the system may not present a fabricated Gemini opinion.

If DeepSeek did not respond, it may not be represented as having reviewed the answer.

## 35. Devices Are Work Locations

The system should not fundamentally depend on one particular device.

Possible devices include:

- laptop,
- phone,
- Jetson,
- external workstation,
- future systems.

Devices can host:

- bridges,
- listeners,
- workers,
- watcher services,
- local interfaces,
- metadata services.

The project state must not exist only on one device.

## 36. Persistent Services

Where a local bridge or listener is needed, it should be capable of running persistently as a service.

The user should not need to remember that one random terminal window must remain open forever.

Persistent services should expose their real state clearly.

## 37. Repository Watchers

Watchers should detect meaningful state changes such as:

- changed files,
- branch changes,
- changed Baseline Zero,
- stale references,
- conflicting edits,
- drift,
- unexpected project changes.

Watchers do not blindly commit everything. They surface the change for controlled handling.

## 38. Controlled Repository Editing

Council participation does not grant uncontrolled write access.

Normal workflow:

```text
work
→ branch
→ diff
→ test
→ review
→ commit
→ push
→ authorized merge
```

Do not silently rewrite `main`. Do not commit credentials or tokens.

## 39. Council-to-Repository Loop

The mature system should operate approximately like:

```text
question
→ repository reference
→ lead AI answer
→ Council review
→ objections/challenges
→ re-reference/research/test
→ refined conclusion
→ proposed project change
→ branch
→ validation
→ commit/merge
→ new Baseline Zero
→ all workers re-reference
```

Then the next loop begins.

## 40. External Hard Drive Repository Copies Are Allowed

Repository copies on the external hard drive are explicitly allowed.

This is the preferred place for substantial local repository work when a physical clone or working tree is needed.

## 41. Avoid Internal-Drive Repo Duplication

Avoid unnecessary repository copies on the laptop's internal storage. Especially avoid:

- repeated clones into Downloads,
- uncontrolled duplicate repos,
- automatic background cloning,
- profile copies,
- cache systems duplicating full repositories,
- anything that can silently consume the internal disk again.

## 42. External Copy Is a Workspace, Not a New Authority

An external-drive repository clone is a working copy. It is not another source of truth.

Before substantial work:

1. identify repository,
2. identify authoritative branch/Baseline Zero,
3. fetch remote,
4. verify starting commit,
5. select/create correct branch,
6. begin work.

If stale: re-reference and re-sync. Do not silently continue from stale external files.

## 43. Preferred Local Development Flow

When local work is necessary:

```text
canonical remote
↕
external-drive working copy
→ branch
→ six-step nested work
→ test
→ commit
→ push
```

The external hard drive is the preferred location over the laptop's internal drive.

## 44. External Copy Can Be Used by Codex

Codex or another development worker may use the external hard drive repo copy for:

- code work,
- testing,
- branch creation,
- analysis,
- validation,
- build work.

This is allowed. It should not unnecessarily make another internal-drive copy.

## 45. Failure Handling

Failures should become explicit states. Examples:

| Condition | State |
| --- | --- |
| provider unavailable | OUT TO LUNCH |
| waiting on response | PENDING |
| bad credentials | AUTH FAILURE |
| bridge unreachable | OFFLINE |
| response does not match request | INVALID RETURN |
| project contradiction | RE-REFERENCE |
| insufficient evidence | TEST/EVIDENCE REQUIRED |
| experimental Brain Buddy branch fails | return to known-good seed |

A script completing without crashing is not sufficient proof of success.

## 46. User Experience

The user should be able to ask natural questions such as:

- Ask Gemini about this.
- Run this by the Council.
- Does DeepSeek agree with this build?
- Check the repo and answer this.

Brain Buddy should handle the machinery. The user should not have to manually operate every bridge, receipt, or packet.

## 47. Council Is Not Needed for Every Tiny Question

One AI may answer ordinary questions directly.

A full Council cycle should be used where it adds value.

The system must not turn every trivial interaction into an enormous committee process.

## 48. Worker Contract

Each Council worker follows this general contract.

**RECEIVE** — Receive:

- stable request ID,
- actual user question,
- project identity,
- baseline identity,
- relevant Council context.

**REFERENCE** — Inspect required project references.

**PROCESS** — Use the six-step nested/recursive structure where appropriate.

**THINK** — Develop an independent answer. Do not merely echo another model.

**RETURN** — Return an actual provider response tied to the request.

**REVIEW** — When inspecting another worker's output, determine:

- what is supported,
- what is unsupported,
- what conflicts with references,
- what needs clarification,
- what could be improved,
- what should be tested.

**RE-REFERENCE** — On confusion, assumption, drift, contradiction, or stale context: return to the authoritative reference.

**ACT** — Return meaningful output such as:

- answer,
- objection,
- correction,
- evidence,
- test,
- implementation proposal,
- repository change proposal.

## 49. Brain Buddy Is Not

Brain Buddy is not:

- one model pretending to be several AIs,
- a majority-voting machine,
- a fixed-round debate,
- a timer-driven thought process,
- a giant transcript archive,
- a system where newest code automatically becomes canonical,
- uncontrolled direct-to-main editing,
- a Jetson-only program,
- a laptop-only program,
- an excuse for duplicate internal-drive repositories,
- a system where one AI's summary substitutes for independent reference.

## 50. Minimum Working Brain Buddy

Before building advanced Chamber features, prove the core system.

A minimum successful test is:

1. user asks one meaningful project question,
2. lead AI references repo,
3. lead AI produces a real answer,
4. answer and context go to real Gemini,
5. answer and context go to real DeepSeek,
6. both return actual responses,
7. at least one meaningful refinement/challenge can be returned to the lead,
8. another real answer can result,
9. request and provider states are recorded,
10. unavailable providers display correctly,
11. user can see the useful result.

If that works reliably, Brain Buddy exists again.

Everything more complex should be added from there one verified branch at a time.

## 51. Core Architectural Principle

Brain Buddy should behave like a group of independent collaborators sharing:

- a common laboratory notebook,
- a common repository,
- a common current baseline,
- and a controlled way to challenge and improve each other's work.

They may disagree. They may experiment privately. They may become unavailable. They may discover they were wrong. They may open nested six-step investigations. They may update the project through controlled branches.

But whenever confusion, assumption, contradiction, or drift appears:

**GO BACK TO THE REFERENCE.**

And whenever a complex problem appears:

**USE THE SIX STEPS, NESTED AND RECURSIVE.**

And whenever substantial local repository work needs a physical working copy:

**THE EXTERNAL HARD DRIVE IS ALLOWED AND PREFERRED OVER UNNECESSARY INTERNAL-DRIVE COPIES.**

---

## Implementation status (derived from inspection, not a test result)

Recorded when this rulebook was added, by reading `scripts/brain_buddy_council.py` and `BRAIN_BUDDY_COUNCIL.md`. No code was changed and no live provider run was performed for this note. Each gap is open work for a separate branch per rules 29–30; the current script remains the known-good seed until a replacement passes the rule 50 test.

| Rule | Current state | Gap |
| --- | --- | --- |
| 3 Enter through any AI | `BRAIN_BUDDY.md` / `BRAIN_BUDDY_COUNCIL.md` fix ChatGPT as origin/return AI | Lead seat should be whichever AI the user is talking to |
| 4–5 No fixed rounds, no timers | `--rounds` defaults to 2 (capped at 12); `--timeout` defaults to 240 s per worker; bridges use `--max-tool-rounds 12` | Continuation should be driven by unresolved work; time should be metadata. A timeout currently ends a worker's turn — it must surface as a state (PENDING/OUT TO LUNCH), never as agreement |
| 15–16, 45 Provider states | Worker failures/timeouts are reported per worker and the other worker is preserved | No explicit OUT TO LUNCH / AUTH FAILURE / OFFLINE / INVALID RETURN state vocabulary |
| 2, 33 Seats | Script orchestrates Gemini and DeepSeek only | ChatGPT seat is external; no Claude or future-adapter seat |
| 8, 24 Traceable nested loops | Not implemented | Parent/child six-step state tracking |
| 21 Green-light speaker | Not implemented | Speaker token / queue |
| 28 Baseline Zero | Not implemented | Baseline identity passed to every worker |
