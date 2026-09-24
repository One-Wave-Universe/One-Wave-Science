# One Wave Bench — AI Bridge Start Here

This is the Bench-local entrypoint for AI, Jetson, laptop, GitHub, Hive Pipe, Gemini, Perplexity, DeepSeek, and ChatGPT bridge work.

Do not guess paths. Do not reset or merge a dirty target checkout just to repair a bridge.

## Reference order

1. Read this file.
2. Read `One_Wave_Bench/hive-pipe/BRIDGE_DIRECTIONS.md`.
3. Run the read-only doctor from the actual checkout:

```bash
cd "$(git rev-parse --show-toplevel)"
python3 One_Wave_Bench/hive-pipe/bridge_doctor.py --profile all
```

4. Use the smallest verified route that is already live.
5. Require a matching receipt before claiming a remote machine or route is live.

## Canonical Bench bridge files

```text
One_Wave_Bench/hive-pipe/README.md
One_Wave_Bench/hive-pipe/BRIDGE_DIRECTIONS.md
One_Wave_Bench/hive-pipe/README-CHATGPT-BRIDGE-FIX.md
One_Wave_Bench/hive-pipe/DEEPSEEK_BRIDGE.md
One_Wave_Bench/hive-pipe/DEEPSEEK_WEB_RELAY.md
One_Wave_Bench/hive-pipe/bridge_doctor.py
One_Wave_Bench/hive-pipe/install_gateway.sh
One_Wave_Bench/hive-pipe/install_chatgpt_terminal_pull.sh
One_Wave_Bench/hive-pipe/bootstrap_chatgpt_terminal_pull.sh
One_Wave_Bench/hive-pipe/chatgpt_terminal_pull.py
One_Wave_Bench/hive-pipe/gateway.py
One_Wave_Bench/hive-pipe/terminal_parser.py
```

## Route priority

```text
1. Direct Hive Pipe MCP
2. ChatGPT GitHub pull bridge
3. GitHub Actions command lane
4. Remote helper
5. Gemini / Perplexity / DeepSeek client routes
6. SSH recovery
```

## Hard rule

Repository code health is not proof of target activation.

A route is live only when the intended target returns a matching receipt.


## Modular hysteretic bridge mesh
Before declaring a route unavailable, read `One_Wave_Bench/hive-pipe/MODULAR_HYSTERETIC_BRIDGE_MESH.md`.

All bridge work uses the same rule: reference -> probe -> choose route -> execute -> receipt -> update route memory. Forward and reverse directions are verified independently. After three evidence-bearing failures on one route family, switch to a materially different route family instead of repeating the same path.

Browser/UI submissions on configured sites may be gated by `One_Wave_Bench/reference-gate-extension/`. Its reference card must identify source, target, direction, reference, intention, consequence, selected route, and fallback routes before the action is allowed.
