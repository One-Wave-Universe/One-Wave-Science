# Algorythm-Zer0 Jetson Field/Void Brain Loop

Runnable prototype of the repository's Field/Void runtime using Algorythm-Zer0 retained-process rules.

## Runtime split

- **M4 loop** owns sequencing.
- **Field** is the expressive state machine and uses CUDA when `torch.cuda.is_available()`.
- **Void** is an independent CPU oversight state machine.
- **Recall/Rebuild Memory** is the persistent state path shared across cycles.

This is a runtime prototype, not a claim that these rules constitute a biological brain.

## Memory

Three behaviors stay separate:

1. **HOLD / live state** — current `BrainState` in RAM.
2. **RECALL** — relevant prior receipts retrieved from `memory.sqlite3`.
3. **REBUILD** — restart reconstruction from `state.json`, with the receipt log as fallback.

Every cycle stores the question, reference, Field packet, Void packet, result, commitment value, and salience.

## Loop

```text
REBUILD retained state
  -> REFERENCE
  -> RECALL relevant history
  -> FIELD: polarity / choice / move / views up
  -> VOID: confirm / defer / deny + oversight
  -> RESOLVE
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

Void remains CPU by design.

## Test

```bash
cd "$HOME/One-Wave-Science/jetson_brain"
python3 test_brain.py
```

Expected:

```text
PASS recall/rebuild
```

## Current boundary

Persistence, recall, rebuild, lifecycle state, Field/Void routing, and the retained loop are implemented. The deterministic text-to-drive function is intentionally a placeholder evidence source. A local model adapter can later supply evidence or candidate answers without replacing the Field/Void/Recall/Rebuild contract.
