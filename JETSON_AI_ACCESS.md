# Jetson AI Access — Canonical Bidirectional Paths

## Priority

AI terminal access must have more than one usable route. The canonical terminal
engine is **Hive Pipe v3** on the Jetson. SSH remains an independent recovery
path. GitHub reaches Hive Pipe through an authenticated HTTPS tunnel, and the
Jetson reaches GitHub through normal git/gh authentication.

```text
                         GITHUB
                     /            \
        workflow_dispatch          git fetch/pull/push + PR
                 |                       ^
                 v                       |
      GitHub-hosted runner               |
                 |                       |
                 v                       |
         HTTPS / Cloudflare              |
                 |                       |
                 v                       |
         HIVE PIPE MCP :8765 <-----------+---- Jetson normal user
          /mcp terminal_run
                 ^
                 |
       direct HTTPS/MCP client

Independent recovery route:
AI/operator ---------------- SSH ----------------> Jetson normal-user shell

External work handoff:
GitHub External_Work/inbox  -->  ~/One-Wave-External-Work/inbox
GitHub External_Work/outbox <--  ~/One-Wave-External-Work/outbox
```

All routine routes run as the normal Jetson user. `sudo`, raw-disk formatting,
power commands, and shell `-c/-lc` strings are blocked by the AI terminal parser.

## One canonical gateway

Use:

```text
hive-pipe/gateway.py
hive-pipe/terminal_parser.py
hive-pipe/install_gateway.sh
```

Do **not** start `scripts/jetson_gateway.py` alongside Hive Pipe. Both use port
8765. `scripts/install_jetson_gateway.sh` is now only a compatibility entrypoint
that delegates to the Hive Pipe installer and can migrate the older gateway
bearer token into the Hive Pipe Codex token.

## 1. Install/restart Hive Pipe on the Jetson

From the real checkout:

```bash
cd "$HOME/One-Wave-Science"
git pull --ff-only origin main
bash hive-pipe/install_gateway.sh
```

The installer creates and starts:

```text
hive-pipe-agent.service
hive-pipe-gateway.service
```

It also creates per-client tokens:

```text
~/.config/hive-pipe/tokens/codex.token
~/.config/hive-pipe/tokens/claude.token
~/.config/hive-pipe/tokens/gemini.token
```

and the external-work workspace:

```text
~/One-Wave-External-Work/inbox
~/One-Wave-External-Work/work
~/One-Wave-External-Work/outbox
```

Check both services:

```bash
systemctl --user is-active hive-pipe-agent.service hive-pipe-gateway.service
```

Expected:

```text
active
active
```

## 2. Local MCP terminal test

Use one local token without pasting it into chat:

```bash
TOKEN="$(cat "$HOME/.config/hive-pipe/tokens/codex.token")"

curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"terminal_run","arguments":{"argv":["printf","AI_TERMINAL_OK"]}}}' \
  http://127.0.0.1:8765/mcp
```

The structured result must contain:

```text
AI_TERMINAL_OK
exit_code: 0
```

Available terminal tools:

```text
terminal_pwd
terminal_which
terminal_run
```

`terminal_run` returns stdout, stderr, exit code, cwd, timing, timeout state, and
output-clipping state.

## 3. Direct HTTPS / Cloudflare path

The gateway stays bound to:

```text
127.0.0.1:8765
```

Point the authenticated Cloudflare tunnel at:

```text
http://127.0.0.1:8765
```

The remote MCP URL is:

```text
https://YOUR-TUNNEL/mcp
```

The tunnel is transport only. Hive Pipe still requires its bearer token.

For a stable tunnel, configure GitHub Actions secrets:

```text
JETSON_GATEWAY_URL=https://YOUR-STABLE-TUNNEL
JETSON_GATEWAY_TOKEN=<contents of the authorized Hive Pipe token>
```

Never commit those values.

## 4. GitHub -> Jetson

Workflow:

```text
.github/workflows/jetson-command.yml
```

It runs only through `workflow_dispatch`; pull requests do not automatically
execute on the Jetson.

Preferred input is a structured argv JSON array:

```json
["git","status","--short"]
```

with cwd:

```text
/home/Scales/One-Wave-Science
```

The workflow sends an MCP `tools/call` request for `terminal_run`. It no longer
uses the obsolete `/v1/exec` endpoint.

A simple fallback `command` input is still available for manual use. It is
parsed with Python `shlex` into argv and does not provide pipes, redirection, or
shell operators.

Examples:

```json
["uname","-a"]
["git","status","--short","--branch"]
["python3","scripts/external_work_bridge.py","status"]
```

## 5. Direct remote client -> Jetson

`scripts/jetson_remote.sh` also uses Hive Pipe MCP `terminal_run`.

Example:

```bash
export JETSON_GATEWAY_URL='https://YOUR-TUNNEL'
export JETSON_GATEWAY_TOKEN='authorized-token'

scripts/jetson_remote.sh \
  --cwd /home/Scales/One-Wave-Science \
  -- git status --short --branch
```

External workspace example:

```bash
scripts/jetson_remote.sh \
  --cwd /home/Scales/One-Wave-External-Work \
  -- find . -maxdepth 2 -type f
```

## 6. SSH -> Jetson independent path

Enable SSH with:

```bash
cd "$HOME/One-Wave-Science"
bash scripts/enable_jetson_ssh.sh
```

Optionally add an authorized client's **public** key:

```bash
AI_SSH_PUBLIC_KEY='ssh-ed25519 AAAA... ai-worker-name' \
  bash scripts/enable_jetson_ssh.sh
```

Then:

```bash
ssh Scales@JETSON_IP
```

SSH does not depend on Cloudflare, GitHub Actions, or Hive Pipe and is the
independent recovery route.

## 7. Jetson -> GitHub

The Jetson checkout uses normal git authentication. Verify the remote first:

```bash
cd "$HOME/One-Wave-Science"
git remote -v
git fetch origin
```

For outbound AI work, never silently push to `main`. Use a task branch:

```bash
git switch -c ai/my-task
git status --short
git add <reviewed-paths>
git diff --cached
git commit -m 'Describe the task'
git push -u origin HEAD
```

Then open a PR with an authenticated GitHub client/`gh` when available.

Hive Pipe `terminal_run` permits normal `git fetch`, `git pull`, `git commit`,
and task-branch `git push`. Repository policy—not a hidden shell—controls when a
write should be published.

If `git fetch` works but `git push` does not, outbound GitHub authentication is
the missing piece; fix the Jetson's GitHub SSH/token/credential setup rather
than creating another terminal bridge.

## 8. GitHub <-> external Jetson work

Repo handoff paths:

```text
External_Work/inbox/
External_Work/outbox/
```

Jetson-local paths:

```text
~/One-Wave-External-Work/inbox/
~/One-Wave-External-Work/work/
~/One-Wave-External-Work/outbox/
```

### GitHub -> Jetson external work

After the repo receives files under `External_Work/inbox/`:

```bash
cd "$HOME/One-Wave-Science"
git pull --ff-only origin main
python3 scripts/external_work_bridge.py pull
```

The files appear under `~/One-Wave-External-Work/inbox/`.

### Jetson external work -> GitHub

Put reviewable results under:

```text
~/One-Wave-External-Work/outbox/
```

Then:

```bash
cd "$HOME/One-Wave-Science"
python3 scripts/external_work_bridge.py publish
git status --short External_Work/outbox
```

The bridge copies them to `External_Work/outbox/` but does not commit or push.
Publish them through a task branch/PR.

See `External_Work/README.md` for the handoff rules.

## 9. Access matrix

| Direction | Path | Depends on |
|---|---|---|
| AI/operator -> Jetson | SSH | LAN/SSH + authorized key |
| AI/client -> Jetson | HTTPS `/mcp` | tunnel + Hive Pipe token |
| GitHub -> Jetson | `Jetson Command Lane` | Actions secrets + tunnel + Hive Pipe |
| Jetson -> GitHub | git/gh | Jetson GitHub credentials |
| GitHub -> external work | `External_Work/inbox` + bridge pull | git sync + local workspace |
| external work -> GitHub | bridge publish + task branch/PR | git push credentials |

## 10. Acceptance test

Do these in order:

1. `hive-pipe-agent.service` is active.
2. `hive-pipe-gateway.service` is active.
3. Local MCP `terminal_run` returns `AI_TERMINAL_OK`.
4. Direct remote `scripts/jetson_remote.sh -- uname -a` returns Jetson output.
5. GitHub `Jetson Command Lane` with `["uname","-a"]` returns Jetson output.
6. `ssh Scales@JETSON_IP` works independently.
7. `git fetch origin` works on the Jetson.
8. A disposable task branch can be pushed from Jetson to GitHub.
9. External-work bridge `pull` moves a test file GitHub -> Jetson local inbox.
10. External-work bridge `publish` moves a test file Jetson local outbox -> repo outbox.

When all ten pass, both directions and the independent recovery paths are live.
