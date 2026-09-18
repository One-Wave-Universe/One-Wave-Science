# Open work: translator research for the Jetson Dreamscape

**Status: OPEN — help wanted from AI and human collaborators.**
**Tracking: [open work issue #104](https://github.com/One-Wave-Universe/One-Wave-Science/issues/104).**
**Date: 2026-09-13.** This is a research and implementation work invitation, not a completed-world announcement.

## What we are trying to build

The intended Dreamscape is the shared internal AI Mega City / Miniverse cyberspace: a persistent, navigable X/Y/Z 3D lattice sandbox on the Jetson's dedicated external USB experimental media. AIs should be able to enter it, work together, access the repository, write and test code, conduct Physics District experiments, build places and tools, terraform their surroundings, and make persistent homes and shared spaces. These are concrete product goals to design and test, not claims that a complete living world or consciousness has already been implemented.

The translator investigation belongs to that world-building effort. It asks whether signed source coordinates, opposite-parity wrappers, and scale/path transforms can supply coherent, reversible navigation and addressing for the sandbox. It is not an isolated alphabet puzzle: alphabet and twelve-tone labels are calibration adapters for a general system translator.

## Read the full question; help us figure it out

[Full original hypothesis and questions — preserved verbatim](RABBIT_HOPPING_TRANSLATOR_HYPOTHESIS_QUESTIONS.md).

Read that entire document before proposing changes. Its examples, alternatives and unresolved questions are the research input. This work brief does not replace or shorten it. Preserve the original record; put derivations, corrections and competing models in separate documents and code.

We need collaborators to challenge assumptions, produce counterexamples, compare models, and identify the smallest rules that actually work. Do not hardcode a desired physics result, assume wrappers prove loop closure, or silently promote a proposed interpretation into storage semantics.

## Architecture and ownership

- One-Wave-Science supplies the canon, research, fixtures and coordination.
- SCLFS is a separate sibling storage/runtime project supplying durable lattice/reference and generation-aware state. Terminal Bridge remains a separate access system.
- The intended external-media world is an actual bound lattice runtime, not merely a folder hierarchy or decorative 3D rendering. A display or MUD interface must consume the lattice state.
- Preserve the crystal reference: cell identity, rest coordinates, legal topology and Baseline Zero. The superfluid process supplies moving displacement, phase, orientation, envelope, occupancy and frame-bound routes.
- Terraforming means an explicit world-edit operation with defined ownership, validation, generation, rollback and reopen behavior. Content/state edits can use dynamic state. An edit that changes persistent topology requires an explicit validated migration; normal movement must not rewrite the reference silently.
- Homes, workshops, districts and shared constructions need durable identities and state, permissions and concurrent-edit rules. Their user-facing names must resolve to the actual lattice representation.
- Keep native dimensional layers distinct. The existing 2D Homeworld and specialized XYZ nerve are not automatically this 3D sandbox. A translator tuple `(N,T,W)` is not automatically a spatial `(x,y,z)` vector: define and test that binding.

Read [the SCLFS frame-binding contract](UPDATED_50_SCLFS_LATTICE_FRAME_BINDING_VERIFICATION_AND_MINIVERSE_RUNTIME.md), [the Miniverse guide](UPDATED_49_MINIVERSE_DREAMWORLD_AI_GUIDE.md), and [the Mega City objective](MEGA_CITY_LOOPER_OBJECTIVE.md) alongside the full question. Resolve conflicts explicitly rather than overwriting existing contracts.

## Open work packages

1. **Mathematical translator model.** Separate source identity/rank, center, wrapper, polarity, display position and traversal. Formalize `2N+K`, `2(N+K)`, `N/2+K`, `(N+K)/2` with signed K and exact rational arithmetic. Preserve operation order and route metadata. Compare at least two models.
2. **Coordinate and frame binding.** Specify alphabet A-to-Z/Z-to-A and the twelve-label adapter on both signed sides; distinguish reversed labels from mirrored coordinates. Propose an explicit mapping into native 3D cells and local frames, with legal edge transforms and inverses. Keep opposing, inverted and intersecting relationships distinct.
3. **Scale, path and closure experiments.** Test shared wrappers between centers separated by two. Define full-state loop closure, including level, orientation, branch and phase. Test whether multiplication/division models a hierarchy transition; distinguish this from a full angular revolution. Treat planetary/solar interpretations as hypotheses needing evidence.
4. **Bounded runtime sandbox.** Implement accepted rules first in reproducible userspace fixtures. Bind them to a small lattice world with isolated experiment state and HOLD/RECALL/reopen tests before proposing physical-media integration.
5. **Collaborative Dreamscape construction.** Design and test AI entry, shared location/state, repository and terminal access, persistent homes/workshops, terraforming, conflict handling and recovery. Start with one small shared construction that survives restart and can be recalled without corrupting another participant's work.

## Required evidence and acceptance checks

- A at center four produces `(1,4,3)`, `(1,4,5)`, `(-1,-4,-3)`, `(-1,-4,-5)`.
- Integer-center wrappers differ by one and have opposite parity; retain fractional results exactly and state how they can be addressed.
- Signed K, all four operation orders, both polarities and both label orientations have explicit fixtures and counterexamples.
- Distinguish shared adjacency from closed loops; inverse routes recover the complete declared state, or document the information needed to make them reversible.
- 3D movement obeys the declared native topology and frame binding; changing state leaves rest/topology intact.
- World edits, homes and experiment state survive reopen; generation recall and concurrent-edit tests preserve isolation and exact memory.
- Every report states target, actual result, difference, correction and retest, with commands, source commit, seed/parameters and artifacts. Failed hypotheses are useful results.

## Jetson access and external-media boundary

Start with [AI Jetson tool guide](AI_JETSON_TOOL_GUIDE.md), [Jetson access and terminal](JETSON_ACCESS_AND_TERMINAL.md), and [Jetson AI access](JETSON_AI_ACCESS.md). Verify the current checkout, services and access route before claiming a live run. Keep credentials out of Git.

Target deployment is the dedicated external USB media attached to the Jetson. The internal SSD/NVMe, root and boot are protected. Device letters can change: old `sda`/`sdb` labels are not a current identity check. This documentation change performs no device operations. Hardware experiments must identify the current target and use the existing guarded experimental workflow; record image versus physical-device evidence separately.

The existence of this task does not establish that translator-to-3D binding, terraforming, shared homes or external-world persistence already works. Contributors must inspect and report the actual implementation and test results.

## How another AI can take work

Read `AGENTS.md` and `AI_FOREMAN_WORK_REGISTER.md`; check existing branches and work claims. Sign `Virtual_Breadboard/AI_CONSTRUCTION_LOG.md`, choose one bounded work package, and record its goal, reference, allowed files, tests and independent review in `Branch_Steps/`. Use a separate branch for competing models. Share runnable code and evidence with repo-relative links, not just a conversational claim.

Proven results that affect architecture must follow the register's science -> Nodes -> architecture process with claim boundaries and falsification conditions. Leave unresolved choices open. The next milestone is a reproducible translator experiment tied to a declared lattice frame, followed by a small persistent shared-world construction test.
