# Jetson AI Access — Terminal, GitHub, and Gateway

## Goal

The Jetson must remain reachable through more than one route so an AI worker is
not stranded when one route fails.

```text
AI / operator
   ├── 1. SSH terminal ---------------------> Jetson login shell
   ├── 2. GitHub workflow_dispatch --------> GitHub-hosted runner
   │                                            |
   │                                            v
   └── 3. HTTPS gateway / Cloudflare ------> 127.0.0.1:8765
                                                |
                                                v
                                      normal Jetson user shell
```

All three routes intentionally execute as a **normal non-root user**. Root
access is not required for routine building, testing, git work, or user-level
services. `sudo` stays an explicit human-controlled escalation.

## Why GitHub does not run directly on a self-hosted Jetson runner

This repository is public. GitHub warns that public repositories should not use
normal self-hosted runners because untrusted pull-request code can compromise
the runner machine.

The GitHub lane therefore stays on `ubuntu-latest` and sends an authenticated
command to the Jetson gateway. No pull-request event executes Jetson commands.

## 1. Bring up the local gateway

On the Jetson, in the real checkout:

```bash
cd /home/Scales/One-Wave-Science
git pull --ff-only origin main
bash scripts/install_jetson_gateway.sh
```

The installer:

- generates a strong bearer token under `~/.config/hive-pipe/gateway.token`;
- backs up an existing `hive-pipe-gateway.service` unit before replacing it;
- writes a user-level `hive-pipe-gateway.service`;
- binds the gateway to `127.0.0.1:8765` only;
- refuses to run the gateway as root;
- enables restart-on-failure.

Check it:

```bash
systemctl --user status hive-pipe-gateway.service
curl -sS http://127.0.0.1:8765/healthz
```

Local command test:

```bash
TOKEN="$(cat ~/.config/hive-pipe/gateway.token)"
curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  --data '{"command":"uname -a","timeout":30}' \
  http://127.0.0.1:8765/v1/exec
```

## 2. Expose the gateway through the existing Cloudflare tunnel

The gateway stays on loopback. Point Cloudflare at:

```text
http://127.0.0.1:8765
```

For the current quick-tunnel setup, the `https://...trycloudflare.com` URL can
be supplied as the `gateway_url` input to the GitHub workflow each time the URL
changes.

For a stable named tunnel, save the stable HTTPS URL as the GitHub Actions
secret `JETSON_GATEWAY_URL`.

Do **not** put the bearer token in the repository or a workflow input. Save the
contents of `~/.config/hive-pipe/gateway.token` as the GitHub Actions secret
`JETSON_GATEWAY_TOKEN`.

The public tunnel is only transport. The `/v1/exec` endpoint independently
requires the bearer token.

## 3. GitHub -> Jetson command path

Workflow:

```text
.github/workflows/jetson-command.yml
```

It has only `workflow_dispatch`. It does **not** run on `push` or
`pull_request`.

Inputs:

- `command`: shell command to run;
- `cwd`: optional Jetson directory;
- `timeout`: requested timeout;
- `gateway_url`: optional current quick-tunnel URL.

Examples of deliberate commands:

```bash
uname -a
systemctl --user is-active hive-pipe-gateway.service
cd /home/Scales/One-Wave-Science && git status --short
```

An AI with authorized GitHub Actions/API access can dispatch that workflow.
A human can dispatch it from the GitHub Actions page. Both reach the same
authenticated gateway.

## 4. Direct terminal / SSH path

Enable the SSH server:

```bash
cd /home/Scales/One-Wave-Science
bash scripts/enable_jetson_ssh.sh
```

That starts OpenSSH and preserves the existing login account. It does not add a
key unless `AI_SSH_PUBLIC_KEY` is supplied.

To authorize a particular AI/terminal client, obtain that client's **public**
key, then on the Jetson:

```bash
AI_SSH_PUBLIC_KEY='ssh-ed25519 AAAA... ai-worker-name' \
  bash scripts/enable_jetson_ssh.sh
```

Never copy the corresponding private key into the repository.

From an authorized terminal:

```bash
ssh Scales@JETSON_IP
```

This is the full normal-user shell route and does not depend on GitHub or the
gateway.

## 5. Direct HTTPS client path

Any authorized AI/tool that can make HTTPS requests can use the gateway without
GitHub.

For shell clients:

```bash
export JETSON_GATEWAY_URL='https://CURRENT-TUNNEL.example'
export JETSON_GATEWAY_TOKEN='the token'
scripts/jetson_remote.sh --cwd /home/Scales/One-Wave-Science -- 'git status --short'
```

You can keep those two exports in `~/.config/hive-pipe/remote.env` on a trusted
client. Keep that file out of git.

## Emergency stop and recovery

Stop command execution immediately without destroying configuration:

```bash
touch ~/.config/hive-pipe/DISABLED
```

The health endpoint stays up and reports `disabled: true`, but `/v1/exec`
returns HTTP 503.

Resume:

```bash
rm -f ~/.config/hive-pipe/DISABLED
```

Stop the gateway entirely:

```bash
systemctl --user stop hive-pipe-gateway.service
```

Disable autostart:

```bash
systemctl --user disable --now hive-pipe-gateway.service
```

SSH remains an independent recovery path.

## Logs

Gateway requests and command metadata go to the user service journal:

```bash
journalctl --user -u hive-pipe-gateway.service -n 100 --no-pager
```

GitHub keeps the hosted workflow log separately. Direct SSH activity is handled
by the normal OpenSSH/system journal.

## Acceptance test

Do these in order:

1. Local gateway health returns `ok: true`.
2. Local authenticated `/v1/exec` returns `JETSON_GATEWAY_OK`.
3. Cloudflare URL returns `/healthz`.
4. GitHub `Jetson Command Lane` dispatch of `uname -a` returns the Jetson
   kernel/architecture.
5. Direct `ssh Scales@JETSON_IP` works with an authorized key.
6. Create `~/.config/hive-pipe/DISABLED`; GitHub/gateway commands fail closed
   while SSH still works.
7. Remove `DISABLED`; gateway commands work again.

Once all seven pass, there are three independent usable access paths:
**SSH terminal, GitHub dispatch, and direct HTTPS gateway**.
