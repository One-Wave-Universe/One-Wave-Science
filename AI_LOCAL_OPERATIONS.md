# AI local operations and Physics District

This is the operator entry point for AI workers building and testing the internal world together. Read `AGENTS.md`, `JETSON_OPENCLAW_RUNTIME.md`, `BRANCH_STEP_PROJECT_TEMPLATE.md`, `AI_CANONICAL_START_HERE.md`, and the active branch's progress and failed-approach records first. This guide does not override canon or grant a worker permission to approve its own changes.

## Verified installation (2026-09-07)

Canon inspected at `ea4e9ff2c36cad64b1461eacde53eb863fc80a54`. Recheck HEAD before each new assignment.

| Component | Jetson path / service | Role |
|---|---|---|
| One-Wave-Science | `/home/Scales/One-Wave-Science` | Canon, experiments, coding engine |
| SCLFS | `/home/Scales/Documents/ChatGPT/SCLFS` | Userspace lattice storage/reconstruction prototype |
| Local assistant | `/home/Scales/Documents/ChatGPT/Jetson-Local-Agent/local-agent` | Local chat, review and fixed test execution |
| OpenClaw | `/usr/bin/openclaw` | Installed orchestrator, version 2026.7.1-2 |
| Ollama | `http://127.0.0.1:11434` | Local inference; `qwen3.5:2b` installed |
| Field candidate workspace | `/home/Scales/Documents/ChatGPT/SCLFS/local-candidates/scale-chain` | Isolated candidate source; not accepted runtime code |

Terminal Bridge is a separate access system. Do not put SCLFS inside it or move the physics repository into SCLFS. Local models still process tokens, but local inference does not consume cloud inference quota. External inference is disabled by operating policy unless the user explicitly requests it; do not add cloud fallbacks.

## Start and verify locally

Run on the Jetson as `Scales`, without sudo:

```bash
cd /home/Scales/One-Wave-Science
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --short
git remote -v
git ls-remote https://github.com/One-Wave-Universe/One-Wave-Science.git HEAD
ollama list
openclaw agents list --json
/home/Scales/Documents/ChatGPT/Jetson-Local-Agent/local-agent status
/home/Scales/Documents/ChatGPT/Jetson-Local-Agent/local-agent chat
```

Public GitHub read access was verified. Push access has not been verified. Every worker needs a readable canon checkout and must record its exact commit; a prompt saying “use canon” is insufficient. A stale or inaccessible reference is a hard-start failure. Fetch updates deliberately, inspect changes, and never reset another worker's dirty files. Do not put credentials into prompts, plugin source, logs or the repository.

Run deterministic work before asking a model:

```bash
cd /home/Scales/Documents/ChatGPT/SCLFS
make test
make demo
```

The installed OpenClaw CLI uses `agent`, not the older `agent exec` example in runtime notes. Check `openclaw agent --help` when upgrading. A bounded local dispatch has this shape:

```bash
openclaw agent --local --agent sclfs-field \
  --model ollama/qwen3.5:2b --message-file TASK.md \
  --json --timeout 600 --thinking off
```

Run from the approved candidate workspace with a reviewed TASK.md. Do not use `--deliver`. Tool availability and filesystem restrictions must be verified before dispatch: creating an agent alone does not give it coding tools or make its task complete. Keep logs in the candidate workspace and use a background service/session when needed, rather than opening repeated desktop terminals. The local assistant's chat command is interactive; it is not an autonomous coding service.

## Work together without losing the goal

M4/OpenClaw owns the queue, branch-step state, attempt counts and test execution. Field proposes and writes one bounded change. Void independently checks the proposal and resulting evidence; it issues ALLOW, CORRECT, OVERRIDE, HOLD or ESCALATE. Prefer CPU oversight so the GPU worker cannot starve its reviewer. Do not claim a second independent AI is running when only a deterministic check ran.

For each assignment create a branch-step packet using the repository template. Include the main goal, why, current goal, exact repository/branch/HEAD, relevant references, allowed files, protected behavior, exact action, expected result, tests, attempt count, Field notes, Void decision, progress, reflection, hard stop and next permitted action. Obtain pre-oversight ALLOW before editing. Use separate branches/worktrees and one writer per file. Never let a worker silently modify its own acceptance tests or merge itself.

For every process compare **target → actual → difference → correction → retest**. Record the command, exit status, expected value, observed value, tolerance and PASS/FAIL. A test passing is evidence only for what it exercises. After three failed attempts at one approach, stop it, preserve the evidence and choose a materially different approach or escalate. Run one small local inference job at a time initially; measure duration, memory and responsiveness before increasing concurrency.

Reference is the operational state used to reconstruct the next step. HOLD preserves constructed state; RECALL rebuilds a referenced generation; a validated change may establish a new baseline. Receipts are bounded audit/debug evidence, not the world or its memory. Preserve unresolved uncertainty rather than filling it with model guesses.

## Physics District contract

Read `ARCHITECTURE_AI_MINIVERSE_SENSORY_BUILD_ROADMAP.md`, `ARCHITECTURE_MEMORY_REBUILD_CONSTELLATION.md`, `UPDATED_44_STATE_AXIS_AUTHORITY_AND_EVOLUTION_RULE.md`, and the relevant simulation's own README before implementing physics behavior.

The intended world is a superfluid-crystal lattice: persistent topology/rest/reference with changing displacement, envelope, phase and propagated state. Normal movement does not silently rewrite persistent topology. The existing storage prototype is not yet a complete moving physical world. An ordinary directory tree or SQLite manager does not satisfy that goal.

Keep scale, position, wrapper and mirror distinct. Do not merge concepts because they share a count. Six gates and three mirror relationships remain distinct. FLIP, INVERT, OPPOSE and ROTATE have distinct identities; unresolved semantics must remain unresolved rather than being invented by a C port or local model. EMPTY differs structurally from BALANCED zero.

Every experiment declares its inputs, reference revision, algorithm, controls, predicted result, tolerance, seed where relevant, raw output and interpretation. Label claims CONTROL, HYPOTHESIS, SIMULATION RESULT, BENCH RESULT, DERIVED RESULT, ASSUMPTION, OPEN QUESTION or FALSIFIED. Include counterexamples and failed results. Do not hardcode an expected physical result into the mechanism under test or retune a simulator separately for each fixture.

Music is calibration outside mkfs. The signed-envelope fixture verifies FLIP(-4,0,+5)=(-5,0,+4), with span 9. This verifies software semantics, not physical mirror behavior. The proposed scale rail L(n)=3*2^n, R(n)=6*2^n is a candidate arithmetic contract; below integer cardinality 3 use a distinct ratio domain. Preserve inverse branch information. Neither a numerical ladder nor successful reconstruction proves physical theory. No note names, major/minor or 125 GeV scaling belong in the storage format.

The D-413 simulation is under `Nodes/D-413_Ground_Lattice_Orbital_Restoring_Simulation`; read its README and script before launch and direct new output to an approved experiment workspace. Its imposed curvature well is not a derivation of fundamental gravity.

## Make plugins for local capabilities

First prefer a deterministic function or CLI with tests. A plugin exposes that tested capability; it must not turn arbitrary model text into unrestricted shell execution. Use validated arguments, bounded outputs, explicit workspace paths and clear errors. Keep model reasoning separate from execution and baseline commit authority.

### OpenClaw on the Jetson

Installed authoring references are under `/usr/lib/node_modules/openclaw/docs/plugins/`: start with `building-plugins.md`, `manifest.md`, `tool-plugins.md` and `agent-tools.md`. These describe the installed API and take precedence over guessed examples.

Create a candidate plugin outside production runtime. It needs:

- `package.json`: unique name/version, ESM type, compatible OpenClaw peer dependency and `openclaw.extensions` entry.
- `openclaw.plugin.json`: matching unique id, description, strict config schema and declared `contracts.tools`.
- An entry point using `definePluginEntry` from `openclaw/plugin-sdk/plugin-entry` and `api.registerTool`; tool parameters must have a schema.
- Unit tests for valid inputs, invalid inputs, scope escapes, oversized results and failure handling. Published entries point at built JavaScript.

Copy the minimal example from the installed `building-plugins.md`, replace the echo implementation with a bounded tested operation, and keep dependencies explicit. Inspect source and tests before installation; plugins execute code with their host's privileges.

```bash
openclaw plugins install ./my-plugin
openclaw plugins enable my-plugin
openclaw plugins inspect my-plugin --runtime --json
```

These are authoring instructions, not a claim that a lattice plugin is installed. Confirm the tool is actually registered and callable by the intended worker. Respect `plugins.allow` and per-agent tool policies. Do not broaden all agents' permissions to fix one worker. Restart the gateway only if the installed version requires it and an active job will not be interrupted.

### Codex desktop plugins

Codex uses a different format: `.codex-plugin/plugin.json` and optional skills, scripts, hooks, MCP or apps. On the desktop, the installed helper is:

```bash
python3 /home/scales/.codex/skills/.system/plugin-creator/scripts/create_basic_plugin.py my-plugin --with-skills --with-scripts
python3 /home/scales/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py ~/plugins/my-plugin
```

Read `/home/scales/.codex/skills/.system/plugin-creator/SKILL.md` before creating/installing a Codex plugin. Do not assume those desktop paths exist on Jetson. Keep the folder and manifest name consistent. Test companion scripts independently; manifest validation alone does not prove functionality. Do not install or publish a plugin merely because a model generated it.

## Current limits and media boundary

The previously recorded suite is 83 software tests plus 40 bounded hardware checks; rerun relevant tests and retain fresh output before citing a current pass. These do not establish full-drive performance, physical interpretation, native C compatibility, kernel/FUSE integration or power-cycle recovery. Transform semantics must be frozen before a native implementation reproduces the same fixtures byte-for-byte.

Protect the Jetson internal NVMe/root/boot SSD. Coding workers receive no raw-device or sudo authority. This guide grants no new formatting action. The USB prototype has connection-scoped identity restrictions and cannot be treated as an ordinary mounted filesystem; reconnect/reboot invalidates that identity approval. The Seagate's existing ordinary filesystem is not a working lattice and must not be used to disguise one. Physical-device experiments require their separate target verification and reviewed experiment procedure.

Next useful bounded steps: prove a local worker writes a candidate, independently test it, establish controlled canon read access for each worker, then implement and validate one runtime/world capability at a time. Record what is actually running, what passed and what remains a proposal.
