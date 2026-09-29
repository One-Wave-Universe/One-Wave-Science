# Jetson DeepSeek Brain Buddy

## Purpose

DeepSeek Brain Buddy is the DeepSeek counterpart to the bounded Gemini worker.

It is an external review/research lane that must use the One-Wave repository as its first authority instead of answering from memory.

The required reference chain is:

```text
GENERAL_REFERENCE_RULES.md
        ↓
AI_CANONICAL_START_HERE.md
        ↓
I-06 metadata authority
        ↓
named proof / node / task files
        ↓
DeepSeek question
        ↓
validate against metadata + receipts
        ↓
return to repository reference
```

## Runtime

Primary wrapper:

```bash
scripts/deepseek_min.sh
```

Underlying bridge:

```text
One_Wave_Bench/hive-pipe/deepseek_bridge.py
```

The bridge gives DeepSeek bounded Jetson tools through Hive Pipe. It does not grant sudo, raw-device access, credentials, or unrestricted shell.

## Authentication boundary

DeepSeek model calls require:

```text
DEEPSEEK_API_KEY
```

Keep it outside git.

Hive Pipe authentication is separate and uses the DeepSeek client token under the normal Hive Pipe token path.

A healthy Hive Pipe DeepSeek smoke test does not prove the DeepSeek model credential exists.

## First bridge smoke

```bash
cd /home/Scales/One-Wave-Science
python3 One_Wave_Bench/hive-pipe/deepseek_bridge.py --mcp-smoke
```

This should return a real Reference Goblin / Checker receipt from the Jetson.

## First model smoke

After `DEEPSEEK_API_KEY` is configured outside git:

```bash
cd /home/Scales/One-Wave-Science
bash scripts/deepseek_min.sh ask "Reply with only: DEEPSEEK BRAIN BUDDY OK"
```

## Science proof review

Create a bounded task packet:

```bash
cp DEEPSEEK_TASK_TEMPLATE.md /tmp/deepseek-task.md
```

Then:

```bash
bash scripts/deepseek_min.sh science /tmp/deepseek-task.md
```

For science work DeepSeek must:

- read `GENERAL_REFERENCE_RULES.md`;
- read `AI_CANONICAL_START_HERE.md`;
- read `Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md`;
- read only the exact proof/node files required;
- report current gate/lifecycle from YAML/front matter where present;
- separate established external physics/math from One-Wave hypotheses;
- propose falsifiable PASS / FAIL / INCONCLUSIVE criteria;
- list the exact repo paths it actually referenced.

## Brain Buddy reference loop

Use:

```text
REFERENCE GIT
    ↓
ASK / PIVOT
    ↓
REFERENCE METADATA / FLIP
    ↓
VALIDATE / PIVOT
    ↓
RETURN TO REFERENCE / UPDATE GIT
```

The “flip” always returns through reference.

DeepSeek output is advisory/review evidence. It does not become repository truth until validated and deliberately recorded in the canonical repo.

## Modes

### ask

```bash
bash scripts/deepseek_min.sh ask "question"
```

Bounded answer, no edits.

### review

```bash
bash scripts/deepseek_min.sh review TASK.md
```

Review only, named references only.

### science

```bash
bash scripts/deepseek_min.sh science TASK.md
```

Science/theory review using the full canonical metadata chain.

### deep

```bash
DEEPSEEK_ALLOW_DEEP=1 bash scripts/deepseek_min.sh deep TASK.md
```

Explicit opt-in only.

## Hard stops

DeepSeek Brain Buddy must not:

- scan the whole repo automatically;
- treat model memory as authority;
- infer node status from prose when YAML metadata exists;
- request secrets;
- commit or merge its own answer;
- create another repo clone;
- claim remote execution without a receipt;
- promote an untested One-Wave hypothesis to established physics.

## Current acceptance sequence

A complete DeepSeek Brain Buddy acceptance test is:

1. `deepseek_bridge.py --mcp-smoke` returns Jetson reference/checker receipts;
2. `DEEPSEEK_API_KEY` is present outside git;
3. `deepseek_min.sh ask` returns the exact smoke phrase;
4. a science task makes DeepSeek cite the mandatory reference chain;
5. the answer reports exact repo paths and current metadata status;
6. the answer can be compared with Gemini or another reviewer without either becoming canonical automatically.
