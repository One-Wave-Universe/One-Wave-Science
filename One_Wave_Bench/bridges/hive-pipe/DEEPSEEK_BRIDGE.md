# DeepSeek -> Hive Pipe -> Jetson

This is the no-clipboard route for DeepSeek when using the DeepSeek API.

```text
human task
   |
   v
One_Wave_Bench/bridges/hive-pipe/deepseek_bridge.py
   |
   +--> DeepSeek API function call: jetson_pwd / jetson_which / jetson_run
   |
   v
Hive Pipe MCP /mcp
   |
   v
terminal_pwd / terminal_which / terminal_run
   |
   v
Jetson normal-user process
```

DeepSeek does not need native MCP support for this route. The local client turns
DeepSeek function-tool calls into the existing Hive Pipe MCP JSON-RPC calls and
feeds the structured results back to DeepSeek automatically.

## 1. Create a DeepSeek Hive Pipe token

On the Jetson, from the canonical checkout:

```bash
cd "$HOME/One-Wave-Science"
bash One_Wave_Bench/bridges/hive-pipe/create_client_token.sh deepseek
```

This creates:

```text
~/.config/hive-pipe/tokens/deepseek.token
```

Do not commit or paste that token into chat.

## 2. Set the DeepSeek API key

Keep the API key in the process environment or another local secret store:

```bash
export DEEPSEEK_API_KEY='your-api-key'
```

The bridge defaults to:

```text
DeepSeek base URL: https://api.deepseek.com
Model:             deepseek-v4-pro
Hive Pipe MCP:     http://127.0.0.1:8765/mcp
```

Override the model if desired:

```bash
export DEEPSEEK_MODEL='deepseek-v4-flash'
```

## 3. Prove the Jetson half first

This does not call DeepSeek. It proves the token, endpoint, and Hive Pipe MCP
shape are correct:

```bash
python3 One_Wave_Bench/bridges/hive-pipe/deepseek_bridge.py --mcp-smoke
```

Expected result contains an `ok: true` working-directory response.

If this fails, fix Hive Pipe before involving the model.

## 4. Give DeepSeek a real repo task

```bash
python3 One_Wave_Bench/bridges/hive-pipe/deepseek_bridge.py \
  'Inspect the current One-Wave-Science git status, read the canonical access docs, and report the smallest next verification command.'
```

The loop is automatic:

1. DeepSeek returns a function call.
2. The bridge validates the function name and argument shape.
3. The bridge sends a JSON-RPC `tools/call` request to Hive Pipe `/mcp`.
4. Hive Pipe runs the canonical terminal parser on the Jetson.
5. Structured stdout/stderr/exit code goes back to DeepSeek.
6. DeepSeek can call another tool or return the final answer.

No human carries `grep`, `git`, or test output between the terminal and model.

## 5. Running the client off the Jetson

Keep Hive Pipe bound to Jetson loopback. Use the existing authenticated reverse
tunnel and point the client at its `/mcp` URL:

```bash
export HIVE_PIPE_MCP_URL='https://YOUR-TUNNEL/mcp'
export HIVE_PIPE_TOKEN_FILE='/secure/path/deepseek.token'
export DEEPSEEK_API_KEY='your-api-key'
python3 One_Wave_Bench/bridges/hive-pipe/deepseek_bridge.py 'Check the repo and run the relevant tests.'
```

You may set `HIVE_PIPE_TOKEN` directly instead of `HIVE_PIPE_TOKEN_FILE`, but do
not put it in source code or shell history if avoidable.

## Exact MCP request used

The adapter sends the same current Hive Pipe MCP shape as the other clients:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "terminal_run",
    "arguments": {
      "argv": ["git", "status", "--short", "--branch"],
      "cwd": "/home/Scales/One-Wave-Science",
      "timeout": 30
    }
  }
}
```

It does **not** use the obsolete raw `{ "action": ..., "params": ... }` shape
and it does **not** use the old `~/.config/hive-pipe/gateway.token` path.

## Boundaries

The adapter does not create a new unrestricted shell. `jetson_run` forwards to
the existing `terminal_run`, so the current Hive Pipe terminal parser and the
systemd service sandbox remain authoritative.

The bridge itself also refuses unknown function-tool names and malformed
arguments before they reach Hive Pipe. Server-side enforcement still decides
what actually runs.

## DeepSeek thinking-mode compatibility

DeepSeek thinking mode requires the model's `reasoning_content` field to be
passed back on later tool-call requests. `deepseek_bridge.py` preserves that
field on every assistant tool turn. Omitting it can cause DeepSeek API `400`
errors during a multi-tool task.

The bridge deliberately uses DeepSeek function tools rather than assuming
DeepSeek's Responses API will execute a native MCP connector.

## Tests

The adapter has offline tests in:

```text
One_Wave_Bench/bridges/hive-pipe/test_deepseek_bridge.py
```

They verify:

- current JSON-RPC MCP request shape;
- bearer-token forwarding;
- exactly three exposed DeepSeek terminal functions;
- function-name mapping to Hive Pipe terminal tools;
- rejection of malformed arguments;
- preservation of `reasoning_content` across tool-call rounds.

These tests do not require a real DeepSeek API key and are picked up by the
existing Hive Pipe `test_*.py` discovery workflow.
