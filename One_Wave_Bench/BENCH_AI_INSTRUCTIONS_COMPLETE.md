[Reading 1000 lines from start (total: 5383 lines, 4383 remaining)]

# Bench AI Instructions — Complete Copy

Source: One_Wave_Bench in One-Wave-Science
Generated: 2026-09-24


---

## SOURCE FILE: One_Wave_Bench/README.md

# One-Wave Bench — Shared AI + Human Laboratory

A turn-based workbench where **either a human or an AI** can propose a physics
experiment, run it against the canonical D-413 engine, and read the same
receipts. Governed by **D-412** (simulation standard) and **A-117** (native
dimension declaration).

## What is in here

| Path | Purpose |
|------|---------|
| `web/index.html` | The shared bench UI. Live D-413 simulation, experiment ledger of real runs, per-case charts, and an experiment composer that emits a request JSON. |
| `web/fixed_sim.html` | Fixed, reproducible simulation player. Locked-parameter scenarios selected by URL, e.g. `web/fixed_sim.html?scenario=orbit_asymmetric`. Embeddable in wiki pages. |
| `web/four_interaction_sim.html` | D-414 four-interaction visual bench driven by the shared data bundle. |
| `docs/breadboard/BREADBOARD_CANONICAL_ARCHITECTURE.md` | Canonical breadboard architecture reference. |
| `docs/breadboard/BREADBOARD_QUALIFICATION_SUITE.md` | Breadboard qualification and verification plan. |
| `schema/experiment_protocol.json` | The request/receipt contract (hypothesis, cases, falsifiers, required measurements, control checks, native dimension). |
| `engine/run_experiment.py` | Headless runner. Imports the canonical D-413 physics (single source of truth) and executes any experiment request, emitting a D-412 receipt + CSVs. |
| `engine/build_manifest.py` | Scans `runs/` for receipts and writes `runs/manifest.json`, which the bench UI reads. |
| `runs/` | Real receipts, per-case CSV time series, and the manifest. |

## Fixed simulation scenarios

All are the **same engine and one update law**; only initial conditions,
locked parameters, and camera differ. Camera/projection never changes physics.

| `?scenario=` | Shows |
|--------------|-------|
| `orbit_asymmetric` | Bounded shell orbiting an imposed curvature well with induced spin. Ground-fixed camera. |
| `deep_well` | Deeper well capturing the shell into a tight restoring orbit. Well-fixed camera. |
| `travel_across` | Bounded displacement translating across a stationary lattice, with wake. Ground-fixed camera. |
| `lattice_scrolls` | Same run as `travel_across`, displacement-fixed camera, so the lattice scrolls past. |

Add `&autoplay=0` to start paused. Click the canvas to pause/resume.

## Running an experiment (human or AI)

1. Compose a request (use the composer in `web/index.html`, or write JSON that
   matches `schema/experiment_protocol.json`).
2. Run headless:
   ```
   python One_Wave_Bench/engine/run_experiment.py --stdin << 'JSON'
   { ...request... }
   JSON
   ```
   or `--request path/to/request.json`, or `--demo` for a built-in example.
3. Rebuild the manifest:
   ```
   python One_Wave_Bench/engine/build_manifest.py
   ```
4. Refresh `web/index.html` (served over HTTP — `manifest.json` is fetched, so a
   `file://` open cannot read it). From the repo root:
   ```
   python -m http.server 8899
   # then open http://localhost:8899/One_Wave_Bench/web/index.html
   ```

## D-412 discipline (enforced)

- Simulations evolve **declared state → computed measurements → visualization**.
- Every run can **fail**; falsifiers are declared before running.
- **Interpretation is kept separate** from raw output.
- Each run declares its **native dimension** (currently 2D).
- Stage 01 is a **Yellow reduced model**: the well is imposed and the shell is a
  collective coordinate. Nothing here claims gravity, charge, a proton, a Mirror
  Gate, or a Mass Effect.


---

## SOURCE FILE: One_Wave_Bench/bridges/README.md

# One Wave Bridges

Canonical home for AI, Jetson, terminal, Hive Pipe, local relay, external-work, Gemini, and open-data bridge infrastructure.

## Layout

- docs/ — operator instructions and bridge/reference guides.
- hive-pipe/ — canonical Hive Pipe gateway, parser, pull bridge, DeepSeek adapters, tests, and doctor.
- scripts/ — Jetson/Gemini/install/remote bridge utilities.
- local/ — local-machine bridge and repo-sync tooling.
- integrations/ — bridge adapters embedded in other project surfaces.
- external-work/ — inbox/outbox relay workspace.
- open-data/ — external scientific-data ingestion and wave-transform helpers.

GitHub Actions remain under .github/workflows/ because GitHub only discovers workflows there. Those workflows point into this canonical bridge tree.


---

## SOURCE FILE: One_Wave_Bench/bridges/docs/08_AI_AGENTS_JETSON_AND_TERMINAL.md

# AI Agents, Jetson, and Terminal

## Purpose
Operational infrastructure for AI workers, local models, Jetson access, terminal control, GitHub bridges, and token-light local execution.

## Belongs here
- Jetson setup and service architecture
- Terminal / SSH / gateway / tunnel access
- AI worker and agent coordination
- Instance identification and reconstruction tooling
- Local model integration
- GitHub-driven command paths
- Permissions, safety boundaries, and recovery paths
- Token-reduction / local-first execution strategy

## Rule
Keep conceptual brain architecture in document 06 and lattice-world semantics in document 07.


---

## SOURCE FILE: One_Wave_Bench/bridges/docs/AI_ACCESS_BRIDGING_AND_OPEN_DATA_HOWTO.md

# AI Access, Bridging, GitHub, CERN, and LIGO/GWOSC How-To

For bridge selection, health checks, and exact client request/receipt formats,
start with [`One_Wave_Bench/bridges/docs/AI_BRIDGE_START_HERE.md`](One_Wave_Bench/bridges/docs/AI_BRIDGE_START_HERE.md). Run:

```bash
python3 One_Wave_Bench/bridges/hive-pipe/bridge_doctor.py --profile all
```

This longer guide remains the detailed reference for repository work and public
scientific data.

**Status:** Operational guide  
**Verified against repository access docs and official public-data documentation:** 2026-09-17

This file is the practical starting point for an authorized AI that needs to:

- read or work on the `One-Wave-Science` GitHub repository;
- reach the Jetson terminal;
- use Hive Pipe / MCP tools;
- use GitHub Actions as a bridge to the Jetson;
- use SSH as an independent recovery path;
- use Codex, Claude, Gemini, Perplexity, DeepSeek, or another authorized client;
- work in approved external-drive directories;
- obtain public CERN/LHC open data;
- obtain public LIGO/Virgo/KAGRA data from GWOSC;
- return results through a task branch / pull request rather than silently changing `main`.

This guide does **not** grant credentials. Tokens, API keys, SSH keys, and GitHub credentials stay outside the repository.

---

## 1. The whole access map

```text
                         GITHUB
                     /            \
          git / GitHub API       GitHub Actions
                 |                    |
                 |                    v
                 |          authenticated HTTPS
                 |                    |
                 |                    v
                 +----------> HIVE PIPE MCP :8765
                                  /mcp
                                    |
                 +------------------+------------------+
                 |                  |                  |
       terminal_reference    terminal_pwd     terminal_which     terminal_run
                                                     |
                                                     v
                                           Jetson normal-user shell

Independent recovery path:

AI/operator -------------------- SSH --------------------> Jetson

Public scientific data:

CERN Open Data ---------------- HTTPS / XRootD ----------> approved data dir
GWOSC (LIGO/Virgo/KAGRA) ------ HTTPS / API ------------> approved data dir
```

The normal Jetson user is `Scales`. The canonical repository checkout is normally:

```text
/home/Scales/One-Wave-Science
```

Hive Pipe is the canonical AI terminal gateway. SSH is deliberately independent.

---

## 2. First rule for every AI

Before changing anything, establish exactly where you are and what you can access.

Through a terminal tool, run:

```text
pwd
git status --short --branch
git rev-parse HEAD
git remote -v
```

Do not claim a file, branch, command, service, dataset, or result was checked unless the tool actually returned it.

For any external dataset:

1. query metadata first;
2. inspect file count and size;
3. download a tiny sample or bounded interval first;
4. record source URL / record ID / DOI / event name / run / detector;
5. keep raw data separate from derived results;
6. do not start a multi-GB or multi-TB download just because the dataset is public.

---

# PART A — GITHUB REPOSITORY ACCESS

## 3. Public read access to the repo

Repository:

```text
https://github.com/One-Wave-Universe/One-Wave-Science
```

A machine with Git can clone it with:

```bash
git clone https://github.com/One-Wave-Universe/One-Wave-Science.git
cd One-Wave-Science
```

On the Jetson, prefer the existing canonical checkout instead of making duplicate clones:

```bash
cd /home/Scales/One-Wave-Science
git status --short --branch
git rev-parse HEAD
git remote -v
git fetch origin
```

Public read/fetch can work without push credentials. Push requires an authorized GitHub credential on that machine or an authorized GitHub connector.

## 4. Read repo files without terminal access

An AI with an authorized GitHub integration can read files directly through GitHub's repository/file API.

Useful read operations are conceptually:

```text
repository metadata
branch metadata
fetch file by path/ref
list/search repository files
inspect pull request
inspect PR diff / changed files
inspect commit / workflow status
```

When a specific branch or PR matters, always read that ref rather than assuming `main` contains the same code.

## 5. Safe write workflow

Routine AI work must use a task branch, not silently write to `main`.

```bash
cd /home/Scales/One-Wave-Science
git fetch origin
git switch -c ai/short-task-name
git status --short --branch
```

After edits:

```bash
git diff --check
git diff
git status --short
```

Run the relevant tests, then:

```bash
git add <reviewed-files>
git diff --cached
git commit -m 'Describe the bounded change'
git push -u origin HEAD
```

Then open a pull request against `main`.

If `git fetch origin` works but `git push` fails, the problem is GitHub write authentication. Fix the GitHub credential; do **not** invent another terminal bridge.

---

# PART B — HIVE PIPE / MCP JETSON ACCESS

## 6. Canonical gateway

Use:

```text
One_Wave_Bench/bridges/hive-pipe/gateway.py
One_Wave_Bench/bridges/hive-pipe/terminal_parser.py
One_Wave_Bench/bridges/hive-pipe/install_gateway.sh
```

Do not start the old `One_Wave_Bench/bridges/scripts/jetson_gateway.py` beside Hive Pipe. Both use port `8765`.

Install or restart from the Jetson checkout:

```bash
cd "$HOME/One-Wave-Science"
bash One_Wave_Bench/bridges/hive-pipe/install_gateway.sh
```

Check services:

```bash
systemctl --user is-active hive-pipe-agent.service hive-pipe-gateway.service
```

Expected:

```text
active
active
```

## 7. MCP endpoint and tools

Local endpoint:

```text
http://127.0.0.1:8765/mcp
```

Remote endpoint through the authenticated tunnel:

```text
https://YOUR-TUNNEL/mcp
```

Primary MCP tools:

```text
terminal_reference
terminal_pwd
terminal_which
terminal_run
python_run
cpp_compile_run
```

`terminal_run` accepts structured argv and optional cwd/timeout.

Example tool arguments:

```json
{
  "argv": ["git", "status", "--short", "--branch"],
  "cwd": "/home/Scales/One-Wave-Science",
  "timeout": 30
}
```

Current Hive Pipe v3 permits normal development commands and normal shell wrappers such as `bash -lc`, while direct high-risk system operations, privilege escalation, raw-device formatting/partitioning, mounting, power-control commands, and credential/private-key paths remain restricted.

## 8. Per-client tokens

Tokens live only on the Jetson under:

```text
~/.config/hive-pipe/tokens/
```

Typical clients:

```text
codex.token
claude.token
gemini.token
perplexity.token
```

Create another client token with:

```bash
cd "$HOME/One-Wave-Science"
bash One_Wave_Bench/bridges/hive-pipe/create_client_token.sh CLIENT_NAME
```

Never commit a token or paste it into public repo files.

The gateway accepts common authentication forms including Bearer token and API-key headers. See `One_Wave_Bench/bridges/docs/AI_JETSON_TOOL_GUIDE.md` and `One_Wave_Bench/bridges/hive-pipe/README.md` for the current forms.

## 9. Local MCP smoke test

On the Jetson:

```bash
TOKEN="$(cat "$HOME/.config/hive-pipe/tokens/codex.token")"

curl -sS \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"terminal_run","arguments":{"argv":["printf","AI_TERMINAL_OK"]}}}' \
  http://127.0.0.1:8765/mcp
```

Expected stdout contains:

```text
AI_TERMINAL_OK
```

with exit code `0`.

---

# PART C — CLIENT-SPECIFIC BRIDGES

## Session has no terminal/MCP tools

If an AI says there is no terminal attached, do not treat that as proof the
Jetson bridge is broken. First separate **gateway health** from **session
attachment**.

Healthy Hive Pipe v3.2 on the Jetson listens at:

```text
http://127.0.0.1:8765/mcp
```

and should list:

```text
health
inventory_block_devices
repo_status
terminal_reference
terminal_pwd
terminal_which
terminal_run
python_run
cpp_compile_run
```

If local MCP `initialize` and `tools/list` succeed but the AI chat cannot see
those tools, reconnect/start that client with the Hive Pipe MCP connector
attached. A running chat cannot obtain missing MCP tools merely by reading repo
instructions.

Use the client's own token from:

```text
~/.config/hive-pipe/tokens/<client>.token
```

For remote AI products, connect through the current authorized HTTPS tunnel to
`/mcp`. Do not commit tokens or temporary public tunnel URLs.

After reconnect, the AI must prove access by calling `terminal_pwd`, then a
real `terminal_run` such as `git status --short --branch`. Until that succeeds,
repo/terminal claims are unverified and must not be fabricated.

See `One_Wave_Bench/bridges/docs/AI_JETSON_TOOL_GUIDE.md` for the full failure matrix and recovery sequence.


## 9A. Direct Python and C++ without a human terminal relay

Once an authorized AI is connected to Hive Pipe MCP, it can send bounded source
code directly instead of asking a person to copy code into a shell.

Python:

```json
{
  "name": "python_run",
  "arguments": {
    "code": "print(6 * 7)",
    "cwd": "/home/Scales/One-Wave-Science",
    "timeout": 30
  }
}
```

C++:

```json
{
  "name": "cpp_compile_run",
  "arguments": {
    "code": "#include <iostream>\nint main(){std::cout << 6*7 << \"\\n\";}",
    "standard": "c++20",
    "cwd": "/home/Scales/One-Wave-Science",
    "timeout": 60
  }
}
```

Expected stdout from both examples is `42`.

`python_run` creates a temporary Python script, executes it with `python3`,
returns structured stdout/stderr/exit status, and removes the source afterward.

`cpp_compile_run` creates temporary C++ source, compiles with `g++` using one
of `c++17`, `c++20`, or `c++23`, executes the binary, returns both compile
and runtime receipts, and removes the temporary files afterward.

These are not a second unrestricted shell. They use the existing Hive Pipe
per-client token, normal non-root user, authorized work roots, timeout/output
limits, and systemd sandbox. Direct source is limited to 12 KiB per call and
credential/private-key path markers are rejected.

For persistent project changes, the AI should still edit normal repo files on a
task branch, run tests, inspect the diff, and open a PR. See `One_Wave_Bench/bridges/docs/AI_CODE_BRIDGE.md`.

---


## 10. Codex / Claude / Gemini / Perplexity through MCP

For an MCP-capable client, configure:

```text
MCP URL: https://YOUR-TUNNEL/mcp
Authentication: the client's own Hive Pipe token
Transport: Streamable HTTP when the client asks for a transport type
```

First call `terminal_pwd`, then run a harmless terminal smoke test.

Example:

```json
{
  "name": "terminal_run",
  "arguments": {
    "argv": ["printf", "AI_TERMINAL_OK"],
    "cwd": "/home/Scales/One-Wave-Science",
    "timeout": 30
  }
}
```

Perplexity-specific setup is documented in `One_Wave_Bench/bridges/docs/AI_JETSON_TOOL_GUIDE.md` and `One_Wave_Bench/bridges/hive-pipe/README.md`.

Gemini also has a separate official CLI lane documented in `One_Wave_Bench/bridges/docs/JETSON_GEMINI_MINIMAL.md`. That lane is distinct from Hive Pipe credentials.

## 11. DeepSeek bridge

DeepSeek can use the existing function-tool adapter without requiring native MCP support.

Create its Hive Pipe token:

```bash
cd "$HOME/One-Wave-Science"
bash One_Wave_Bench/bridges/hive-pipe/create_client_token.sh deepseek
```

Smoke-test the Jetson half first:

```bash
python3 One_Wave_Bench/bridges/hive-pipe/deepseek_bridge.py --mcp-smoke
```

Then, only if the external DeepSeek API is intentionally being used, configure its API credential outside git and run:

```bash
python3 One_Wave_Bench/bridges/hive-pipe/deepseek_bridge.py \
  'Inspect the current git status and report the smallest next verification command.'
```

Full details: `One_Wave_Bench/bridges/hive-pipe/DEEPSEEK_BRIDGE.md`.

## 12. GitHub Actions -> Jetson

Workflow:

```text
.github/workflows/jetson-command.yml
```

It is manually dispatched and sends an authenticated MCP `terminal_run` call to the Jetson.

Preferred command input is structured argv, for example:

```json
["git", "status", "--short", "--branch"]
```

The stable tunnel and token are configured as GitHub Actions secrets, not committed files.

## 13. Direct remote script

The repository helper uses the same Hive Pipe parser:

```bash
export JETSON_GATEWAY_URL='https://YOUR-TUNNEL'
export JETSON_GATEWAY_TOKEN='authorized-token'

One_Wave_Bench/bridges/scripts/jetson_remote.sh \
  --cwd /home/Scales/One-Wave-Science \
  -- git status --short --branch
```

## 14. SSH recovery

SSH is independent of GitHub Actions, Cloudflare, and Hive Pipe.

```bash
ssh Scales@JETSON_IP
```

Enable/configure it with the repo helper when needed:

```bash
cd "$HOME/One-Wave-Science"
bash One_Wave_Bench/bridges/scripts/enable_jetson_ssh.sh
```

Use SSH for recovery when the MCP/tunnel route is unavailable.

---

## 14A. Shared 3D Miniverse room bridge

The visible Miniverse room is another client of the same Jetson tool/runtime
architecture, not a replacement for Hive Pipe.

```text
AI client
   |
   v
Hive Pipe terminal/Python/C++ tools
   |
   +----> Miniverse room CLI ----> shared persistent room state
   |                                  |
   |                                  +--> agents / locations
   |                                  +--> shared chat
   |                                  +--> workbench receipts
   |                                  +--> stationary 37-cell lattice
   |                                  |
   |                                  v
   +---------------------------> Three.js 3D browser view
```

Runtime URL:

```text
http://127.0.0.1:8787/
```

AI command examples:

```bash
python3 /home/Scales/miniverse-room-runtime/Miniverse/room3d/client.py join gemini --name GEMINI --role "AI REVIEWER" --color '#98ffb4'
python3 /home/Scales/miniverse-room-runtime/Miniverse/room3d/client.py say gemini "Review lane online."
python3 /home/Scales/miniverse-room-runtime/Miniverse/room3d/client.py move gemini B+
python3 /home/Scales/miniverse-room-runtime/Miniverse/room3d/client.py bench gemini review REVIEW "checked current result"
```

An AI can use `python_run` or `cpp_compile_run` for a bounded experiment and
then post the structured result to WORKSHOP, TEST LAB, or REVIEW through
`client.py bench`. The browser sees that same receipt on its next state poll.

Do not claim that a displayed body is an autonomous model merely because its
identity exists in the room. The body is an avatar/state endpoint until an
external AI client actually takes that identity.

Expansion contract: `Miniverse/EXPAND_MINIVERSE.md`. Native laptop application:
`Miniverse/desktop/README.md`. Custom AI bodies are submitted through
`client.py body <agent> <body.json>` and remain bounded/validated server state.

# PART D — EXTERNAL DRIVES AND WORKSPACES

## 15. Authorized external-drive directories

Hive Pipe can be reinstalled with explicitly allowed work roots, for example:

```bash
HIVE_PIPE_ALLOWED_ROOTS="/home/Scales/One-Wave-Science:/mnt/lattice:/mnt/sandbox" \
  bash One_Wave_Bench/bridges/hive-pipe/install_gateway.sh
```

Do not authorize an entire drive root merely for convenience. Create dedicated writable directories and authorize only those.

Good pattern:

```text
/mnt/lattice/data/cern/
/mnt/lattice/data/gwosc/
/mnt/lattice/results/
/mnt/sandbox/
```

The actual paths must exist and be writable by `Scales` before installation.

Raw-device, formatting, mounting, sudo, and power operations remain outside normal AI terminal authority.

## 16. GitHub external-work handoff

Repository-visible paths:

```text
One_Wave_Bench/bridges/external-work/External_Work/inbox/
One_Wave_Bench/bridges/external-work/External_Work/outbox/
```

Jetson-local paths:

```text
~/One-Wave-External-Work/inbox/
~/One-Wave-External-Work/work/
~/One-Wave-External-Work/outbox/
```

Pull repo inbox into the Jetson workspace:

```bash
python3 One_Wave_Bench/bridges/scripts/external_work_bridge.py pull
```

Stage Jetson-local results back into repo outbox:

```bash
python3 One_Wave_Bench/bridges/scripts/external_work_bridge.py publish
```

`publish` does not commit or push. Review the files and use a task branch / PR.

---

# PART E — CERN / LHC OPEN DATA

## 17. What CERN provides

Official portal:

```text
https://opendata.cern.ch/
```

CERN Open Data includes public material from ALICE, ATLAS, CMS, LHCb, and other CERN research outputs. LHC releases include simplified educational data and reconstructed research-grade datasets, with dataset records, metadata, software notes, licenses, and DOI citations.

An AI should treat a CERN Open Data **record ID or DOI** as the primary provenance key.

## 18. Install the CERN Open Data client

Use a user environment, not sudo:

```bash
python3 -m venv "$HOME/.venvs/cern-open-data"
source "$HOME/.venvs/cern-open-data/bin/activate"
python -m pip install --upgrade pip
python -m pip install cernopendata-client
cernopendata-client version
```

Official client source/documentation:

```text
https://github.com/cernopendata/cernopendata-client
https://cernopendata-client.readthedocs.io/
```

## 19. Find the record before downloading

Use the CERN portal search:

```text
https://opendata.cern.ch/search
```

Record pages look like:

```text
https://opendata.cern.ch/record/RECORD_ID
```

Search/filter by experiment, dataset type, year, format, or physics topic. Record the chosen record ID and DOI in the experiment notes.

For a known record ID, inspect metadata first:

```bash
cernopendata-client get-metadata --recid RECORD_ID
```

## 20. Inspect CERN file size and locations first

Before downloading:

```bash
cernopendata-client get-file-locations \
  --recid RECORD_ID \
  --server https://opendata.cern.ch \
  --verbose
```

For XRootD paths:

```bash
cernopendata-client get-file-locations \
  --recid RECORD_ID \
  --protocol xrootd \
  --verbose
```

CMS NanoAOD and other ROOT-based releases can often be streamed with XRootD instead of copying the entire dataset locally.

Typical XRootD host:

```text
root://eospublic.cern.ch//eos/opendata/...
```

## 21. Bounded CERN download

**Do not default to downloading an entire dataset.** Some records represent hundreds of GiB, TiB, or more.

First use a dry run or a bounded file range when supported:

```bash
cernopendata-client download-files \
  --recid RECORD_ID \
  --server https://opendata.cern.ch \
  --dry-run
```

Then download only a small subset, for example:

```bash
cernopendata-client download-files \
  --recid RECORD_ID \
  --server https://opendata.cern.ch \
  --filter-range 1-2 \
  --verify
```

Run the download from the approved CERN data directory so files do not fill the Jetson system disk.

Example pattern:

```bash
cd /mnt/lattice/data/cern
cernopendata-client download-files --recid RECORD_ID --filter-range 1-2 --verify
```

If that exact directory is not in `HIVE_PIPE_ALLOWED_ROOTS`, use an already-authorized workspace or update the allowed-root configuration deliberately.

## 22. CERN analysis formats

Common routes include:

```text
CMS NanoAOD -> ROOT / uproot / Awkward Array / NanoAOD tools
CMS AOD/MiniAOD -> experiment-specific CMSSW environment
ALICE -> ROOT-based workflows
LHCb -> CERN Open Data records and the LHCb Ntupling Service
```

Do not assume every CERN dataset can be interpreted by generic CSV/Python code. Read the record's own software/environment instructions.

CERN currently documents direct HTTPS downloads and XRootD streaming for CMS NanoAOD. LHCb also provides an Ntupling Service for custom open-data ntuples.

## 23. CERN provenance receipt

For every CERN-derived result, save at least:

```text
portal = CERN Open Data
record_id = ...
doi = ...
experiment = CMS / ATLAS / ALICE / LHCb / ...
dataset title = ...
file URL(s) or XRootD path(s) = ...
file checksum if supplied = ...
retrieval date = ...
analysis script / commit = ...
derived output = ...
```

---

# PART F — LIGO / VIRGO / KAGRA DATA THROUGH GWOSC

## 24. Official public source

Use the Gravitational Wave Open Science Center:

```text
https://gwosc.org/
```

Current API documentation:

```text
https://gwosc.org/api/
https://gwosc.org/api/v2/
```

GWOSC API v2 is public, read-only, uses HTTP GET, and does not require authentication.

The API exposes observing runs, event catalogs, events, strain files, data-quality segments, parameter-estimation information, and related public products.

## 25. Install the official GWOSC Python client

Use a user virtual environment:

```bash
python3 -m venv "$HOME/.venvs/gwosc"
source "$HOME/.venvs/gwosc/bin/activate"
python -m pip install --upgrade pip
python -m pip install gwosc
```

Official client docs:

```text
https://gwosc.readthedocs.io/
```

## 26. Prove GWOSC access without downloading strain

Simple API smoke test:

```bash
curl -sS https://gwosc.org/api/v2/runs | python3 -m json.tool | head -80
```

Python:

```bash
python3 - <<'PY'
import requests
r = requests.get('https://gwosc.org/api/v2/runs', timeout=30)
r.raise_for_status()
print(r.json())
PY
```

No token is required for public GWOSC API data.

## 27. Discover available GWOSC datasets

```bash
python3 - <<'PY'
from gwosc.datasets import find_datasets
print('runs:', find_datasets(type='run'))
print('events sample:', find_datasets(type='event')[:20])
PY
```

For a known event, get its GPS time:

```bash
python3 - <<'PY'
from gwosc.datasets import event_gps
print(event_gps('GW150914'))
PY
```

## 28. Find LIGO/Virgo strain URLs before downloading

For a single event:

```bash
python3 - <<'PY'
from gwosc.locate import get_event_urls
urls = get_event_urls('GW150914', detector='H1', duration=32)
for u in urls:
    print(u)
PY
```

For a GPS interval:

```bash
python3 - <<'PY'
from gwosc.locate import get_urls
urls = get_urls('L1', 968650000, 968660000, sample_rate=4096, format='hdf5')
for u in urls:
    print(u)
PY
```

`get_urls()` can select detector, GPS start/end, dataset, version, sample rate, and format.


[executed on device: scales-Latitude-E7450 (bb2a3fd3-3820-49b2-b303-8a652e54f7ce)]