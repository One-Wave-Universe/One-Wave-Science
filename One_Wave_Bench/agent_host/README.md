# One-Wave Shared Dream/Admin Coding Host MVP

This is the smallest runnable proof of the architecture:

- **one shared memory/state** owned by the host;
- **Dream** performs bounded coding work;
- **Administrator** performs compressed oversight/override;
- **M4** is deterministic routing/state/tool control, not an AI;
- **Executor/tool broker** owns real file and command access;
- the immutable root reference survives every loop;
- completed loop state is compressed and inherited by the next loop;
- local OpenAI-compatible model servers are the default workers.

The macro loop is:

```text
BEGIN -> BUILD_1 -> HOLD -> BUILD_2 -> BREAK -> LOOP
```

The shared packet also carries the current 2/3/4/5 fields:

```text
2 choice-space
3 direction
4 relation
5 dimensional view
```

## Local model requirement

Run one or two local models behind an OpenAI-compatible endpoint. Ollama and LM Studio can expose this style of API. The default URL expected by this MVP is:

```text
http://127.0.0.1:11434/v1
```

Dream and Admin may point at the same server while using different models, or at two different local servers.

## Run one complete coding loop

From the repository root:

```bash
python -m One_Wave_Bench.agent_host.local_pair \
  --workspace . \
  --reference "THE EXACT OBSERVABLE RESULT THAT MUST NOT BE REPLACED" \
  --dream-model YOUR_LOCAL_CODER_MODEL \
  --admin-model YOUR_LOCAL_ADMIN_MODEL \
  --check "python -m pytest -q"
```

The host persists shared state to:

```text
.onewave/shared_state.json
```

Running the same command again continues from that shared state. If a different root reference is supplied while state exists, the host refuses to silently replace it.

## What is enforced now

- Dream can inspect with `read` and `search` during BUILD.
- Dream gets one bounded `write` per BUILD before the macro loop advances.
- Dream cannot write during HOLD/BREAK/LOOP.
- HOLD/BREAK measurement is run by the host, not accepted from Dream as opinion.
- Admin receives a compact state/measurement packet rather than the whole repo.
- Admin override becomes inherited unresolved guidance for Dream's next BUILD.
- exact receipts and compact inherited state remain local.
- source paths are workspace-scoped; escaping the workspace is rejected.
- obviously dangerous command families such as `sudo`, `git push`, `git reset --hard`, and root deletion are denied by the MVP broker.

## Current limitation

This is intentionally an MVP. `write` currently replaces a complete text file. The next practical improvement is a small exact-replace/patch tool so local models can make surgical edits without regenerating whole files. The macro loop should remain unchanged while that tool improves.
