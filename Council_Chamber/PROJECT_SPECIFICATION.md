# One-Wave Council Chamber

The Council Chamber is a single shared chat and coding workspace where several AI systems can work together with one person.

It is only the beginning foundation. There are no rooms, private AI homes, Arena Games, city systems, or complicated government yet.

## The council table

Every supported AI or coding system has an available seat at the same council table.

Possible seats include:

- ChatGPT
- Codex
- Claude
- Gemini
- DeepSeek
- A local AI model
- A future custom AI connector

The user opens only the seats needed for the current job.

Each seat remains a separate participant with its own name, model, instructions, capabilities, connection, and status. ChatGPT and Codex therefore occupy separate seats and can talk directly to each other even when both use OpenAI technology.

## One shared conversation

All open seats participate in the same council chat.

The user might say:

Build the first Wave Mapper waveform display.

ChatGPT can discuss the design. Claude can examine the architecture. Codex can propose the code. Gemini can suggest another approach. Each response remains clearly labeled so nobody's work is merged or hidden behind one generic assistant identity.

The AIs can:

- Respond to the user
- Read approved messages from other seats
- Ask another seat a question
- Compare approaches
- Disagree and explain why
- Review another seat's work
- Continue from an accepted decision

The user decides which seats receive each message and when another discussion round begins. The system must not allow the AIs to generate an uncontrolled endless conversation.

## Shared coding workspace

Beside the council chat is one local project workspace containing:

- File tree
- Code editor
- Proposed changes
- Diff viewer
- Approve and reject controls
- Terminal output
- Build results
- Test results

The AIs help work on the same project, but they do not silently overwrite it.

A seat can propose a change. The Council Chamber shows exactly what would change. The user can approve it, reject it, or modify it. Approved changes are then applied to the local files.

## Local computer does the actual work

The Council Chamber should not waste AI calls on ordinary computer operations.

The local computer handles:

- Opening and saving files
- Searching the project
- Finding functions and symbols
- Applying approved patches
- Running builds
- Running tests
- Formatting and linting code
- Showing differences
- Recording decisions
- Saving project history
- Managing the task list
- Starting the local preview
- Capturing errors and output

These actions do not need another chatbot response.

AI seats are used when reasoning, planning, interpretation, code generation, review, or difficult debugging is needed.

## Local worker seats

Some seats represent local tools instead of chatbots.

Examples include:

- File Search — finds files, text, definitions, and references.
- Test Worker — runs tests and reports exact failures.
- Build Worker — compiles or starts the application.
- Patch Worker — safely applies an approved change.
- Git Worker — creates checkpoints and displays changes.
- Memory Worker — stores requirements, decisions, tasks, and results.
- Preview Worker — runs and inspects the local program.

These workers can post results into the same council chat, but they are ordinary local software rather than language models.

## Local AI seats

Small AI models running through software such as Ollama or llama.cpp can also occupy seats.

Local models can perform lighter jobs such as:

- Sorting tasks
- Summarizing short discussions
- Ranking relevant files
- Classifying errors
- Writing simple code
- Producing small code completions
- Retrieving stored project information

Stronger cloud AI seats can be reserved for harder work.

## Persistent local memory

The authoritative project memory belongs to the local computer, not to any individual chatbot.

The Council Chamber stores:

- Full conversation history
- Pinned requirements
- Accepted decisions
- Rejected ideas
- Current tasks
- Completed tasks
- File summaries
- Code changes
- Build history
- Test results
- Errors
- Checkpoints

An AI seat receives only the information relevant to its current task. It does not need the entire conversation and repository sent back on every turn.

This saves tokens and prevents the project from being lost when a model's context closes.

## Token and resource tracking

The public version should transparently show the resources used by every seat.

Depending on the connection, a seat may report:

- Input and output tokens
- Estimated price
- Number of requests
- Context-window use
- Subscription access
- Local CPU or GPU use
- Provider-supported unmetered access
- Usage unavailable

The system must not invent token counts when they are not reported.

Our local-first version should reduce AI use by completing file operations, searches, builds, tests, memory retrieval, routing, and project management directly on the computer.

## Example workflow

The user says:

Add disconnect support to the AI seats.

ChatGPT examines the requirements and proposes the behavior.

Codex inspects the relevant local files and proposes a patch.

The user approves it.

The local Patch Worker applies the change.

The local Test Worker runs the tests.

One test fails and posts the exact error into the council chat.

ChatGPT explains the likely problem.

Codex proposes a smaller repair.

The user approves it.

The Patch Worker applies it, and the Test Worker confirms that all tests pass.

The local computer performed the searching, editing, patching, testing, recording, and verification. The AI seats contributed the reasoning and code decisions.

## Beginning goal

The first Council Chamber proves one central idea:

A person can open several separate AI seats—including ChatGPT and Codex—place them into one shared conversation, let them communicate and help write code together, and use the local computer to preserve, execute, test, and verify their work.

Nothing larger should be built until this basic council chat and shared coding loop works reliably.
