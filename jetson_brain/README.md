# Algorythm-Zer0 Jetson Field/Void Brain Loop

Runnable prototype of the repository's Field/Void runtime using Algorythm-Zer0 retained-process rules.

## Runtime split

- **M4 loop** owns sequencing.
- **Field** is the expressive state machine and uses CUDA when `torch.cuda.is_available()`.
- **Void** is an independent CPU oversight state machine.
- **Recall/Rebuild Memory** is the persistent state path shared across cycles.
- **Deterministic resolver** supplies evidence from arithmetic, prior receipts, or local canonical files. No LLM or network model is used.

This is a runtime prototype, not a claim that these rules constitute a biological brain.

## Memory

Three behaviors stay separate:

1. **HOLD / live state** — current `BrainState` in RAM.
2. **RECALL** — relevant prior receipts retrieved from `memory.sqlite3`.
3. **REBUILD** — restart reconstruction from `state.json`, with the receipt log as fallback.

Every cycle stores the question, pre-reference, post-reference, evidence packet, Field packet, Void packet, result, commitment value, and salience. Receipt-log fallback reconstructs the last Field/Void route as well as the retained reference.

## Loop

```text
REBUILD retained state
  -> REFERENCE
  -> RECALL relevant history
  -> deterministic RESOLVER: arithmetic / memory / local canon
  -> FIELD: route from evidence / views up
  -> VOID: confirm / defer / deny evidence contract
  -> RESOLVE answer or explicit unknown
  -> REMEMBER receipt + snapshot
  -> result becomes next reference
  -> LOOP
```

Every receipt also exposes:

```text
BEGIN -> BUILD 1 -> HOLD -> BUILD 2 -> BREAK / RELEASE -> LOOP
```

## Run on Jetson

```bash
cd "$HOME/One-Wave-Science"
python3 jetson_brain/brain.py --memory "$HOME/.local/share/algorythm-zer0-brain" --status
python3 jetson_brain/brain.py --memory "$HOME/.local/share/algorythm-zer0-brain" --repl
```

Inside the REPL:

```text
/status
/recall motor balance
/quit
```

## Verify CPU/GPU split

```bash
python3 jetson_brain/brain.py --memory /tmp/zer0-brain-test --status
```

Expected on a CUDA-enabled Jetson PyTorch install:

```json
"field_backend": "cuda"
```

Void remains CPU by design. On the Jetson verification used for this PR, PyTorch was not installed, so the observed Field backend was `cpu-python`.

## Test

```bash
cd "$HOME/One-Wave-Science/jetson_brain"
python3 test_brain.py
```

Expected:

```text
PASS deterministic-answer/recall/rebuild
```

The focused test verifies multiple arithmetic phrasings, memory recall, local-canon lookup, snapshot restart, and forced SQLite-only rebuild.

## Current boundary

Persistence, recall, rebuild, lifecycle state, Field/Void routing, and the retained loop are implemented. The old character-hash text drive has been removed. Supported answers currently come only from bounded deterministic resolvers: arithmetic, receipt memory, and a small local canonical-file set. Unsupported questions return `DEFER` rather than fabricated answers. There is no LLM dependency or network fallback.

Void currently verifies the deterministic evidence contract (resolved status, answer, provenance, threshold); it is not a general truth prover. The six-part recursion receipt is still an exposed logical receipt, not proof that six independently measured runtime transitions occurred. CUDA remains conditional on an installed CUDA-enabled PyTorch build; CPU fallback is valid.
