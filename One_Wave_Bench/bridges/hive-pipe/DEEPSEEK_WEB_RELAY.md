# DeepSeek Free Web Login -> Hive Pipe -> Jetson

This is an **optional, isolated, no-DeepSeek-API-key path** for a DeepSeek web
account.

It does not replace or modify the working Codex, Claude, Gemini, Perplexity,
SSH, Cloudflare, GitHub Actions, or Hive Pipe access paths.

```text
normal DeepSeek web account
        |
        v
local Playwright relay on Jetson :3000 (loopback only)
        |
        v
One_Wave_Bench/bridges/hive-pipe/deepseek_web_bridge.py
        |
        v
existing Hive Pipe /mcp
        |
        v
terminal_pwd / terminal_which / terminal_run
        |
        v
Jetson normal-user process
```

## Status and trust boundary

The browser relay is third-party software, not an official DeepSeek API or MCP
client. It automates `chat.deepseek.com` with Playwright. Web UI changes,
anti-bot changes, account challenges, or policy changes can break it.

For that reason this route is deliberately kept outside the canonical access
infrastructure:

- the third-party checkout lives under `~/One-Wave-Tools/`;
- its HTTP listener is patched to `127.0.0.1` only;
- it is not put behind the Hive Pipe/Cloudflare tunnel;
- it receives no Hive Pipe token;
- `deepseek_web_bridge.py` is the only component that can cross from the local
  browser relay into the existing Hive Pipe terminal tools;
- the normal Hive Pipe parser and systemd sandbox remain authoritative.

## Pinned relay source

The bootstrap pins:

```text
https://github.com/maresin/deepseek-automation-api.git
cd952329bf5525d4e8a5591d951a9bb5610aebe0
```

That project exposes an OpenAI-compatible local endpoint and returns function
`tool_calls`, but does not execute those tools itself. The One-Wave bridge
executes only the three already-supported Hive Pipe terminal tools.

The pinned upstream currently declares a missing `postinstall` helper in its
`package.json`; the bootstrap therefore installs dependencies with lifecycle
scripts disabled and installs Chromium explicitly through `playwright-core`.

## First-time bootstrap

On the Jetson, from the One-Wave checkout:

```bash
bash One_Wave_Bench/bridges/scripts/bootstrap_deepseek_web_relay.sh
```

The script:

1. clones the pinned relay outside the repo;
2. installs/builds it without touching the canonical Hive Pipe services;
3. installs the matching Chromium runtime;
4. patches the local relay to listen on `127.0.0.1` only;
5. starts it locally;
6. if no browser session exists, prompts in the terminal for the DeepSeek
   account email and password;
7. sends those credentials only to the local registration process;
8. unsets the password immediately after registration;
9. stores only the resulting browser session state and the relay's generated
   **local** API key;
10. runs both relay-health and Hive Pipe `terminal_pwd` smoke checks.

Do not paste the DeepSeek password into chat or commit it to the repository.

The local relay key is **not** a DeepSeek API key. It only authenticates calls
to the browser automation process running on the Jetson.

## Give the logged-in DeepSeek session a Jetson task

After bootstrap:

```bash
bash One_Wave_Bench/bridges/scripts/deepseek_web_worker.sh \
  'Inspect the current repo status, choose one useful unfinished task, make the smallest change, test it, and report the result.'
```

The worker starts the local relay if needed, then runs:

```text
DeepSeek web -> tool call -> deepseek_web_bridge.py -> Hive Pipe -> Jetson
```

No human should have to carry `git`, `grep`, or test output between DeepSeek and
the terminal.

## What the bridge exposes

Exactly the same three functions as the official-API bridge:

```text
jetson_pwd   -> terminal_pwd
jetson_which -> terminal_which
jetson_run   -> terminal_run
```

`jetson_run` still goes through the existing structured-argv parser. This route
does not create an unrestricted shell or bypass the server-side block list.

## Smoke checks

Relay only:

```bash
python3 One_Wave_Bench/bridges/hive-pipe/deepseek_web_bridge.py --relay-health
```

Hive Pipe only:

```bash
python3 One_Wave_Bench/bridges/hive-pipe/deepseek_web_bridge.py --mcp-smoke
```

Both:

```bash
python3 One_Wave_Bench/bridges/hive-pipe/deepseek_web_bridge.py --relay-health --mcp-smoke
```

## Login failures

The automatic login path works only when the DeepSeek account accepts ordinary
email/password login without an interactive challenge. If DeepSeek requires a
CAPTCHA, external identity-provider login, or another browser interaction, the
bootstrap should fail rather than storing credentials or bypassing the
challenge.

In that case the remaining safe option for this web-relay lane is a one-time
manual browser login on the Jetson desktop, after which the saved browser state
can be reused. Do not weaken the existing Hive Pipe access controls to solve a
DeepSeek web-login problem.

## Failure classification

Treat failures separately:

- relay `/health` failure -> local browser-relay process/install problem;
- login/session failure -> DeepSeek web authentication or UI change;
- tool-call parse failure -> browser-relay compatibility problem;
- Hive Pipe MCP failure -> existing Jetson terminal path;
- command rejection -> existing `terminal_parser.py` policy boundary.

A browser-relay failure does **not** mean the Jetson access path is broken.

## Tests

Offline adapter tests:

```text
One_Wave_Bench/bridges/hive-pipe/test_deepseek_web_bridge.py
```

They verify:

- local relay URL normalization and key loading;
- DeepSeek web tool calls map to the existing Hive Pipe tools;
- tool output is returned to the model;
- malformed tool arguments become explicit bridge errors;
- the bridge does not require or inject a DeepSeek API key.
