# Jetson DeepSeek Brain Buddy

## Purpose

DeepSeek Brain Buddy is the DeepSeek counterpart to the bounded Gemini worker.

Its **default path is the free DeepSeek web session already logged in on the Dell**. The Dell runs a small private Firefox relay over the direct USB link to the Jetson. No paid DeepSeek API key is required for this default path.

DeepSeek must use the One-Wave repository as its first authority instead of answering from memory.

## Mandatory reference chain

```text
GENERAL_REFERENCE_RULES.md
        ↓
AI_CANONICAL_START_HERE.md
        ↓
Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md
        ↓
named proof / node / task files
        ↓
DeepSeek question
        ↓
validate against metadata + real tool receipts
        ↓
return to repository reference
```

## Default free runtime

```text
Jetson scripts/deepseek_min.sh
        ↓
deepseek_web_bridge.py
        ↓ USB only
Dell 192.168.55.100:3000
        ↓
deepseek_web_relay.py
        ↓
private logged-in Firefox relay profile
        ↓
DeepSeek free web chat
        ↓ tool request
deepseek_web_bridge.py
        ↓
Hive Pipe MCP
        ↓
Jetson bounded terminal
```

The relay is transport only. It does not become a second source of One-Wave truth.

### Dell relay service

```text
one-wave-deepseek-web-relay.service
```

Canonical installer:

```bash
bash scripts/bootstrap_deepseek_web_relay.sh
```

Runtime state stays outside Git under:

```text
~/.local/state/one-wave-deepseek-web/
```

The relay binds only to the Dell USB interface:

```text
192.168.55.100:3000
```

and allowlists only:

```text
127.0.0.1
192.168.55.1
```

The Jetson USB address is `192.168.55.1`.

## Paid API fallback — optional

The API path remains available only when deliberately requested:

```bash
DEEPSEEK_USE_API=1 DEEPSEEK_API_KEY='...' \
  bash scripts/deepseek_min.sh ask "question"
```

The API key is **not required** for the normal free Brain Buddy path.

If the paid API lane is ever run from GitHub Actions, its optional secret name is:

```text
DEEPSEEK_API_KEY
```

Do not commit the value.

## First health checks

Dell relay:

```bash
python3 - <<'PY'
from urllib.request import urlopen
print(urlopen("http://192.168.55.100:3000/health", timeout=5).read().decode())
PY
```

Jetson/Hive Pipe:

```bash
python3 One_Wave_Bench/hive-pipe/deepseek_web_bridge.py --mcp-smoke
```

## Brain Buddy smoke

```bash
cd /home/Scales/One-Wave-Science
bash scripts/deepseek_min.sh ask "Reply with only: DEEPSEEK FREE BRAIN BUDDY OK"
```

## Science proof review

```bash
cp DEEPSEEK_TASK_TEMPLATE.md /tmp/deepseek-task.md
bash scripts/deepseek_min.sh science /tmp/deepseek-task.md
```

For science work DeepSeek must:

- read `GENERAL_REFERENCE_RULES.md`;
- read `AI_CANONICAL_START_HERE.md`;
- read I-06;
- read only the exact proof/node files required;
- report gate/lifecycle from YAML/front matter where present;
- separate established external physics/math from One-Wave hypotheses;
- propose falsifiable PASS / FAIL / INCONCLUSIVE criteria;
- list the exact repo paths actually referenced.

## Reference loop

```text
REFERENCE GIT
    ↓
ASK / PIVOT
    ↓
REFERENCE METADATA / FLIP
    ↓
VALIDATE / PIVOT
    ↓
RETURN TO REFERENCE
```

Every flip returns through reference.

DeepSeek output is advisory. It becomes durable One-Wave information only after validation and deliberate recording in the canonical repository.

## Modes

```bash
bash scripts/deepseek_min.sh ask "question"
bash scripts/deepseek_min.sh review TASK.md
bash scripts/deepseek_min.sh science TASK.md
DEEPSEEK_ALLOW_DEEP=1 bash scripts/deepseek_min.sh deep TASK.md
```

## Hard stops

DeepSeek Brain Buddy must not:

- scan the whole repo automatically;
- treat model memory as authority;
- infer node status from prose when YAML metadata exists;
- request or expose secrets;
- commit or merge its own answer;
- create another repo clone;
- claim remote execution without a receipt;
- promote an untested One-Wave hypothesis to established physics.

## Verified acceptance receipt

The free lane has completed a real end-to-end tool loop:

1. Jetson reached Dell relay health over USB.
2. DeepSeek free web requested `jetson_pwd`.
3. Hive Pipe returned a real Reference Goblin / Checker receipt.
4. DeepSeek requested `git rev-parse --show-toplevel` with explicit intention and consequence.
5. Hive Pipe returned exit code 0 and the canonical Jetson repo root.
6. DeepSeek consumed the tool result and returned the requested final confirmation.

This proves the free browser session can participate in the same bounded repo-reference/tool loop as the API bridge without a paid DeepSeek API key.
