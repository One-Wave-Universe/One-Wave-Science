# One-Wave Lens App

Experimental runtime. Canonical authority remains the repository.

## Forced runtime

```
question
  -> fresh canonical repo read
  -> FIELD model
  -> reference check
  -> same canonical repo read/packet
  -> VOID model
  -> reference check
  -> same canonical repo read/packet
  -> CENTER recombination
  -> reference check
  -> PASS or REJECTED_REFERENCE_BYPASS receipt
```

The app always begins with `GENERAL_REFERENCE_RULES.md` and
`AI_CANONICAL_START_HERE.md`, then retrieves task-relevant canonical files.
It records the exact repository SHA and paths in every receipt.

External metadata, CERN/GWOSC data, web research, calculators and simulators are
tools, not mandatory stages and not project authority.

Default roles are Gemini=Field, DeepSeek=Void, Gemini=Center. Providers are
transport adapters; changing providers does not change the lens.

## Run

```bash
python3 scripts/one_wave_lens_gateway.py ask "your question"
```

Persistent local service:

```bash
python3 scripts/one_wave_lens_gateway.py serve --bind 127.0.0.1 --port 3030
curl -s http://127.0.0.1:3030/ask -H 'Content-Type: application/json' \
  -d '{"question":"your question"}'
```

Provider endpoints may be changed without changing the lens:

```bash
export OWL_GEMINI_URL=http://192.168.55.100:3001
export OWL_DEEPSEEK_URL=http://192.168.55.100:3000
```

Use `packet` to inspect exactly what reference a question receives before any
model is called:

```bash
python3 scripts/one_wave_lens_gateway.py packet "your question"
```
