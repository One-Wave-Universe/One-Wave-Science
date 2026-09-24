# One-Wave Local AI — Architecture

## What is ours
The local language model is a replaceable component. The AI system is the complete One-Wave runtime around it:

- M4 simulated body/process state
- persistent hysteresis and retained memory
- Field/Void two-state cognition
- Parser / Reference / Doctor / Worker / Carrier Pigeon / Raccoon goblins
- reference receipts and no-drift rules
- novelty breaker
- token-economy shared packets
- automated evidence/quality loop
- sandboxed tool/action interface

## What the local model does
It performs bounded language transformations inside one role at a time. It does not own canonical memory, tool permissions, action authority, or final quality judgment.

```text
input/sensors
    -> Parser
    -> M4 body state
    -> Field local-model pass
    -> Void local-model pass
    -> M4 hysteretic action gate
    -> Field speech/action
    -> sandbox/tools
    -> evidence
    -> Void commit
    -> M4 reinjection + memory
    -> quality/reference gate
    -> next cycle
```

## Local endpoint
The first provider expects a local JSON chat endpoint configured with:

```text
ONE_WAVE_LOCAL_AI_URL
ONE_WAVE_LOCAL_AI_MODEL
ONE_WAVE_LOCAL_AI_TIMEOUT
ONE_WAVE_LOCAL_AI_MAX_TOKENS
```

No model credentials belong in the repository.

## Why this counts as our AI architecture
The underlying weights can be swapped without changing identity, memory, control law, state machine, evidence discipline, or behavior loop. Those project-owned layers define the agent.

## Later stages
1. Test with one local model serving both Field and Void.
2. Run two local models with different resource priorities.
3. Compare local Field + cloud Void and cloud Field + local Void.
4. Distill successful Field/Void traces into a smaller local model.
5. Only after the control architecture is stable, consider training/fine-tuning custom weights.
