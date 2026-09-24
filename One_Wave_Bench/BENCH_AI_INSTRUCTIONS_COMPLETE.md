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
## 29. Download one bounded GWOSC file

After inspecting the URL list, download only the file(s) required for the test.

Example pattern:

```bash
cd /mnt/lattice/data/gwosc
curl -L -O 'PASTE_ONE_VERIFIED_GWOSC_HDF5_URL_HERE'
```

Or use Python `requests` with streaming and explicit destination.

For large bulk observing-run data, consult the GWOSC dataset page first. GWOSC recommends OSDF for large-scale cluster access. On the Jetson, prefer event-sized files or explicitly bounded GPS intervals unless bulk transfer is intentional.

## 30. Current public observing-run data

GWOSC's public data pages include event catalogs and large observing-run datasets. As of the verification date for this guide, the GWOSC data page lists O4a and O4b public releases, along with earlier runs and event products.

Do not hard-code "latest" run names into analysis logic. Query the API at runtime because public releases change.

## 31. GWOSC file formats

GWOSC strain is commonly available as:

```text
HDF5
GWF frame files
```

Public strain is commonly offered at 4096 Hz and 16384 Hz sample rates. Choose the rate required by the analysis rather than always downloading the larger file.

## 32. GWOSC provenance receipt

For every LIGO/Virgo/KAGRA-derived result, save at least:

```text
source = GWOSC
API version = v2
event or run = ...
catalog = ...
detector = H1 / L1 / V1 / ...
GPS interval = ...
sample rate = ...
format = hdf5 / gwf / ...
source URL(s) = ...
retrieval date = ...
analysis script / commit = ...
derived output = ...
```

Keep source strain immutable; write filtered/whitened/transformed data to a separate results directory.

---

# PART G — USING CERN OR GWOSC THROUGH THE AI BRIDGE

## 33. From any authorized MCP AI

Once the AI can call `terminal_run`, scientific-data access is just another bounded terminal task.

Example CERN metadata call:

```json
{
  "name": "terminal_run",
  "arguments": {
    "argv": ["cernopendata-client", "get-metadata", "--recid", "5500"],
    "cwd": "/home/Scales/One-Wave-Science",
    "timeout": 60
  }
}
```

Example GWOSC API call:

```json
{
  "name": "terminal_run",
  "arguments": {
    "argv": ["curl", "-sS", "https://gwosc.org/api/v2/runs"],
    "cwd": "/home/Scales/One-Wave-Science",
    "timeout": 60
  }
}
```

For downloads, set `cwd` to an explicitly authorized data directory, not the repo and not the system root.

## 34. Recommended scientific-data loop

```text
QUESTION / TEST
      |
      v
identify official source
      |
      v
query metadata / API
      |
      v
record provenance
      |
      v
inspect size + format
      |
      v
download smallest useful sample
      |
      v
run analysis
      |
      v
compare against control / known result
      |
      v
save raw receipt + derived result
      |
      v
commit scripts/docs/results metadata on task branch
      |
      v
PR for review
```

Never confuse "data downloaded successfully" with "the theory is validated." Data access is only the beginning of the experiment.

---

# PART H — FAST DIAGNOSTIC MATRIX

## 35. If access fails

| Failure | First thing to test | Likely layer |
|---|---|---|
| AI cannot see MCP tools | MCP connector configuration | client/tunnel |
| MCP tools visible but terminal fails | `terminal_pwd` | token/parser/service |
| local MCP fails | service status + local token | Hive Pipe |
| remote MCP fails but local works | tunnel/auth header | Cloudflare/client |
| GitHub fetch works but push fails | Git credential | GitHub write auth |
| GitHub Action cannot reach Jetson | Actions secrets + tunnel | GitHub->MCP bridge |
| MCP dead but LAN reachable | SSH | recovery path |
| CERN metadata works but download fails | file availability / protocol / size | CERN storage |
| GWOSC API works but no file URL returned | event/run/detector/GPS filters | query selection |
| external data dir write denied | `HIVE_PIPE_ALLOWED_ROOTS` + filesystem ownership | sandbox/path |

---

# PART I — MINIMUM ACCEPTANCE TEST

## 36. Access and bridge acceptance

An AI-access setup is usable when these checks pass:

1. repository can be read from GitHub;
2. Jetson repo reports its branch and HEAD;
3. `hive-pipe-agent.service` is active;
4. `hive-pipe-gateway.service` is active;
5. local MCP `terminal_run` prints `AI_TERMINAL_OK`;
6. MCP `python_run` returns `42` for `print(6 * 7)`;
7. MCP `cpp_compile_run` compiles and returns `42` for a tiny C++ program;
8. remote MCP client can call `terminal_pwd`;
9. remote MCP client can run `git status --short --branch`;
10. SSH works independently;
11. `git fetch origin` works on the Jetson;
12. a disposable task branch can be pushed or published through an authorized GitHub integration;
13. CERN record metadata can be retrieved without downloading the full dataset;
14. GWOSC `/api/v2/runs` can be queried without authentication;
15. one small CERN or GWOSC sample can be written to an approved data directory;
16. provenance is recorded with the test result.

---

# PART J — AUTHORITATIVE REPO REFERENCES

Read these when details change:

```text
One_Wave_Bench/bridges/docs/AI_JETSON_TOOL_GUIDE.md
One_Wave_Bench/bridges/docs/JETSON_AI_ACCESS.md
One_Wave_Bench/bridges/docs/AI_CODE_BRIDGE.md
One_Wave_Bench/bridges/hive-pipe/README.md
One_Wave_Bench/bridges/hive-pipe/DEEPSEEK_BRIDGE.md
One_Wave_Bench/bridges/docs/JETSON_GEMINI_MINIMAL.md
One_Wave_Bench/bridges/external-work/External_Work/README.md
AGENTS.md
```

For Hive Pipe runtime behavior, prefer the current `One_Wave_Bench/bridges/hive-pipe/README.md` and `One_Wave_Bench/bridges/docs/AI_JETSON_TOOL_GUIDE.md` over old examples copied into historical notes.

---

# PART K — OFFICIAL EXTERNAL REFERENCES

CERN:

```text
https://opendata.cern.ch/
https://opendata.cern.ch/search
https://opendata.cern.ch/docs/about
https://opendata.cern.ch/docs/cms-getting-started-nanoaod
https://opendata.cern.ch/docs/lhcb-getting-started
https://github.com/cernopendata/cernopendata-client
https://cernopendata-client.readthedocs.io/
```

LIGO / Virgo / KAGRA through GWOSC:

```text
https://gwosc.org/
https://gwosc.org/data/
https://gwosc.org/api/
https://gwosc.org/api/v2/
https://gwosc.readthedocs.io/
```

Use the official portals as the source of truth for current dataset availability, formats, licenses, acknowledgements, and release status.


---

## SOURCE FILE: One_Wave_Bench/bridges/docs/AI_BRIDGE_START_HERE.md

# One-Wave AI Bridge: Start Here

This is the canonical operating page for every AI, laptop, Jetson, and human
using One-Wave terminal access. Read this page before declaring a bridge healthy
or broken.

## One command that tells the truth

From the repository checkout:

```bash
python3 One_Wave_Bench/bridges/hive-pipe/bridge_doctor.py --profile all
```

Profiles:

```text
--profile ci       repository files, syntax, and bridge contracts only
--profile pull     ChatGPT GitHub primary/backup pull bridge
--profile gateway  local Hive Pipe services and a real MCP terminal receipt
--profile all      every local route plus optional/recovery route visibility
```

Exit meanings:

```text
0  every required check in that profile passed
1  at least one required bridge check failed
2  required checks passed, but an optional/external route is unconfigured,
   warning, or cannot be proven from this machine
```

`--json` returns the same result in machine-readable form. The doctor is
read-only. It never changes services, branches, credentials, or files.

## Supported routes and their jobs

| Route | Best use | Health proof | Independent fallback |
|---|---|---|---|
| Hive Pipe MCP | Normal live AI terminal, Python, and C++ | `terminal_reference` plus `terminal_run` receipt | Pull bridge or SSH |
| ChatGPT pull bridge | ChatGPT sessions with GitHub but no attached MCP | Matching result ID on primary or backup branch | Direct MCP |
| GitHub Actions command lane | Human-dispatched remote MCP call | Successful workflow log with exit 0 | Pull bridge |
| `One_Wave_Bench/bridges/scripts/jetson_remote.sh` | Authorized command-line client | Real structured stdout/exit receipt | SSH |
| DeepSeek API adapter | DeepSeek function tools into Hive Pipe | `--mcp-smoke`, then bounded model tool call | Direct MCP client |
| DeepSeek web adapter | Logged-in local web relay into Hive Pipe | `--relay-health` and `--mcp-smoke` | DeepSeek API/direct MCP |
| External-work bridge | GitHub handoff for approved large/external-drive work | Pull/publish smoke with matching file content | Git worktree/manual review |
| SSH | Independent human recovery | Login plus `whoami`, `hostname`, `pwd` | Local console |

The Miniverse desktop/room is a client of this architecture. It is not a
replacement terminal route.

## Route 1 — direct Hive Pipe MCP

Use this first when the AI session exposes the tools:

```text
terminal_reference
terminal_pwd
terminal_which
terminal_run
python_run
cpp_compile_run
```

First calls:

```json
{"name":"terminal_reference","arguments":{}}
```

```json
{
  "name": "terminal_run",
  "arguments": {
    "argv": ["git", "status", "--short", "--branch"],
    "timeout": 30
  }
}
```

Omit `cwd` unless the actual target checkout path has been verified. Every
receipt contains guidance naming whether the next step is an AI correction,
path authorization/creation, tool installation, authentication repair, or a
human/root intervention.

Install/restart on the Jetson or another intended gateway host:

```bash
bash One_Wave_Bench/bridges/hive-pipe/install_gateway.sh
python3 One_Wave_Bench/bridges/hive-pipe/bridge_doctor.py --profile gateway
```

The gateway remains loopback-only. Remote clients use the authorized HTTPS
tunnel and their own per-client token.

## Route 2 — ChatGPT GitHub pull bridge

Use this when ChatGPT has the GitHub connector but no Hive Pipe MCP tools.

Transport branches:

```text
chatgpt-terminal
chatgpt-terminal-backup
```

Write the **same** request to `.chatgpt-terminal/request.json` on both branches:

```json
{
  "id": "unique-task-id-001",
  "argv": ["git", "status", "--short", "--branch"],
  "timeout": 30
}
```

Use a new ID for different command content. The two-state-machine worker dedupes
the mirrored requests, executes once, and returns through the first healthy
writable back route.

Read `.chatgpt-terminal/result.json` on both branches until one contains the
matching ID. A missing result on both branches means the target worker has not
acknowledged the request; it does **not** prove the command ran.

One-time installation on the machine ChatGPT must operate:

```bash
git fetch origin main
git show origin/main:One_Wave_Bench/bridges/hive-pipe/install_chatgpt_terminal_pull.sh | ONE_WAVE_PROJECT_ROOT="$PWD" bash
python3 ~/.local/share/one-wave-chatgpt-terminal-runtime/One_Wave_Bench/bridges/hive-pipe/bridge_doctor.py --profile pull
```

The pull worker runs as the normal user and reuses `terminal_parser.py`. It does
not bypass blocked programs, credential paths, authorized roots, or the systemd
sandbox.

## Route 3 — GitHub Actions command lane

Workflow: `.github/workflows/jetson-command.yml`

Dispatch **Jetson Command Lane** with:

```text
argv_json = ["printf","GITHUB_MCP_OK"]
timeout = 30
```

Blank `gateway_url` uses the configured secret. A successful workflow with
`GITHUB_MCP_OK` and exit `0` proves the current tunnel and secret together. CI
only proves the workflow contract; it cannot prove hidden secrets or a temporary
tunnel is live.

## Route 4 — command-line remote helper

```bash
export JETSON_GATEWAY_URL='https://CURRENT-AUTHORIZED-TUNNEL'
export JETSON_GATEWAY_TOKEN='client-token'
One_Wave_Bench/bridges/scripts/jetson_remote.sh -- git status --short --branch
```

The URL and token may instead live in `~/.config/hive-pipe/remote.env` with
permissions restricted to the user. Never commit them.

## DeepSeek adapters

Official API adapter:

```bash
python3 One_Wave_Bench/bridges/hive-pipe/deepseek_bridge.py --mcp-smoke
```

Free-web/local-session adapter:

```bash
python3 One_Wave_Bench/bridges/hive-pipe/deepseek_web_bridge.py --relay-health --mcp-smoke
```

The DeepSeek adapters translate model function calls into the same bounded Hive
Pipe tools. A healthy adapter cannot compensate for an unhealthy local gateway.

## External work and SSH

External-work transfer is documented in `One_Wave_Bench/bridges/external-work/External_Work/README.md`. CI performs a
real temporary pull/publish content check.

SSH remains independent of GitHub, Cloudflare, and MCP:

```bash
ssh <verified-user>@<verified-host-address>
```

Never guess the username or address. Verify the destination with `whoami`,
`hostname`, and `pwd` after login.

## Health law for every AI

1. Repository tests prove code and contracts, not a live remote machine.
2. A live route requires a matching receipt from that route.
3. A queued request without a matching result is **pending/offline**, not passed.
4. Never claim a command ran from intent, documentation, or a branch write.
5. Use the next independent route only after recording why the preferred route
   failed.
6. Do not ask the human to relay ordinary commands once a live route is proven.
7. If activation or root work is genuinely required, name that single boundary
   precisely instead of pretending another route succeeded.


---

## SOURCE FILE: One_Wave_Bench/bridges/docs/AI_CODE_BRIDGE.md

# AI Direct Python + C++ Bridge

This bridge lets any authorized MCP-capable AI execute bounded Python and C++
source directly on the Jetson through the existing authenticated Hive Pipe
gateway. A human does not need to copy commands between the AI and terminal.

## Tools

Hive Pipe exposes:

```text
python_run(code, args?, cwd?, timeout?)
cpp_compile_run(code, args?, cwd?, timeout?, standard?)
```

The existing tools remain available:

```text
terminal_pwd
terminal_which
terminal_run
```

## Python

Example MCP call:

```json
{
  "name": "python_run",
  "arguments": {
    "code": "print(sum(i*i for i in range(6)))",
    "cwd": "/home/Scales/One-Wave-Science",
    "timeout": 30
  }
}
```

The gateway writes the source to a temporary script inside the authorized work
root, runs it with `python3`, captures stdout/stderr/exit status, and removes
the temporary source automatically.

Arguments can be passed without shell parsing:

```json
{
  "name": "python_run",
  "arguments": {
    "code": "import sys; print(sys.argv[1])",
    "args": ["hello"]
  }
}
```

## C++

Example MCP call:

```json
{
  "name": "cpp_compile_run",
  "arguments": {
    "code": "#include <iostream>\nint main(){std::cout << 42 << \"\\n\";}",
    "standard": "c++20",
    "cwd": "/home/Scales/One-Wave-Science",
    "timeout": 60
  }
}
```

The gateway creates temporary source, compiles it with:

```text
g++ -std=c++20 -O2 -Wall -Wextra -pedantic
```

then runs the temporary binary and removes both source and binary. Supported
standards are `c++17`, `c++20`, and `c++23`.

Compile failures return `phase=compile` plus compiler stdout/stderr. Successful
builds return `phase=run` plus runtime stdout/stderr and the compile receipt.

## Security and scope

These tools do not create a new daemon or privileged shell. They use the same
Hive Pipe authentication, normal non-root user, authorized work roots, timeout
limits, output clipping, systemd `NoNewPrivileges`, and `ProtectSystem=strict`
boundary already used by `terminal_run`.

Direct source is limited to 12 KiB per call. Credential/private-key path markers
are rejected. Temporary source and binaries are removed after each request.

For persistent project work, the AI should still edit normal repo files on a
task branch, run tests, inspect the diff, and open a PR. These direct tools are
for calculations, prototypes, verification, data analysis, compiler checks, and
small experiments without requiring a human terminal relay.

## Verify

After installing/restarting the updated gateway, ask the MCP client to list
tools. It should include:

```text
python_run
cpp_compile_run
```

Python smoke test:

```python
print(6 * 7)
```

Expected stdout:

```text
42
```

C++ smoke test:

```cpp
#include <iostream>
int main() {
    std::cout << 6 * 7 << "\n";
}
```

Expected stdout:

```text
42
```

## Install after merge

From the canonical Jetson checkout:

```bash
cd /home/Scales/One-Wave-Science
git pull --ff-only origin main
bash One_Wave_Bench/bridges/hive-pipe/install_gateway.sh
systemctl --user is-active hive-pipe-agent.service hive-pipe-gateway.service
```

Then reconnect or refresh the AI client's MCP tool list if the client caches it.

See also:

```text
One_Wave_Bench/bridges/docs/AI_JETSON_TOOL_GUIDE.md
One_Wave_Bench/bridges/docs/JETSON_AI_ACCESS.md
One_Wave_Bench/bridges/hive-pipe/README.md
```

---

## SOURCE FILE: One_Wave_Bench/bridges/docs/AI_JETSON_TOOL_GUIDE.md

# AI Jetson Tool Guide

This is the shortest correct guide for a fresh Perplexity/Claude/Codex/Gemini or other authorized AI instance.

## Start here

The canonical Jetson tool path is:

```text
client -> HTTPS/MCP -> One_Wave_Bench/bridges/hive-pipe/gateway.py -> terminal_parser.py -> Jetson process
```

MCP endpoint:

```text
/mcp
```

Primary tools:

```text
terminal_pwd
terminal_which
terminal_run
python_run
cpp_compile_run
```

Do not assume the old `/v1/exec` gateway is active. Do not start
`One_Wave_Bench/bridges/scripts/jetson_gateway.py` beside Hive Pipe; it uses the same port 8765.

## Client credentials

The installer creates separate tokens for:

```text
codex
claude
gemini
perplexity
```

They live only on the Jetson under:

```text
~/.config/hive-pipe/tokens/<client>.token
```

To add any other client:

```bash
bash One_Wave_Bench/bridges/hive-pipe/create_client_token.sh CLIENT_NAME
```

The gateway accepts the same client token through any of these common forms:

```text
Authorization: Bearer <token>
Authorization: ApiKey <token>
X-API-Key: <token>
Api-Key: <token>
```

Never commit or paste tokens into the public repository.

## If an AI says "there is no terminal attached"

Treat that as a **session attachment problem** until proven otherwise. Do not ask
the AI to invent terminal output, and do not assume the Jetson gateway is down.

The repo cannot make an already-running chat suddenly acquire MCP tools. The AI
client/orchestrator must start or reconnect the session with the Hive Pipe MCP
connector attached.

### 1. Verify the Jetson bridge itself

On the Jetson, Hive Pipe should be listening only on loopback:

```bash
ss -ltnp | grep ':8765'
```

Expected service:

```text
127.0.0.1:8765
one-wave-hive-pipe
```

Then initialize MCP with that client's token and call `tools/list`. A healthy
v3.2 gateway exposes at least:

```text
health
inventory_block_devices
repo_status
terminal_pwd
terminal_which
terminal_run
python_run
cpp_compile_run
```

If those tools list correctly, **do not restart or rebuild Hive Pipe just
because one AI chat cannot see them**.

### 2. Reconnect the AI client/session

Configure the client with:

```text
MCP endpoint: https://CURRENT-AUTHORIZED-TUNNEL/mcp
Transport: Streamable HTTP
Authentication: API key / Bearer token
Token source on Jetson: ~/.config/hive-pipe/tokens/<client>.token
```

For a client running locally on the Jetson, the endpoint may be:

```text
http://127.0.0.1:8765/mcp
```

A remote client needs the currently authorized HTTPS tunnel/connector path. Do
not hard-code an expired temporary tunnel URL into the repository.

Start a **new/reconnected AI session** after attaching the connector if the
product caches its tool list.

### 3. Prove attachment from inside the AI session

The AI should first list/see the Hive Pipe tools. Then call:

```text
terminal_pwd
```

and:

```json
{
  "name": "terminal_run",
  "arguments": {
    "argv": ["git", "status", "--short", "--branch"],
    "cwd": "/home/Scales/One-Wave-Science",
    "timeout": 30
  }
}
```

Only after a real tool result returns should the AI claim it inspected the repo.

### 4. Interpret the failure correctly

```text
Gateway tools/list works, AI session has no MCP tools
    -> client/session attachment failure

AI session lists tools, terminal_pwd fails authentication
    -> token/connector authentication failure

AI session lists tools, terminal_run rejects cwd/command
    -> Hive Pipe safety/authorized-root rejection

Port 8765 not listening / initialize fails locally
    -> actual Jetson Hive Pipe service failure
```

A chat that has no tool attachment may still write a proposed patch, but it must
label it unverified. It must never fabricate HEAD hashes, command output, file
contents, or test results.

## Perplexity remote MCP

Perplexity remote custom connectors support API-key authentication. Configure:

```text
MCP URL: https://YOUR-TUNNEL/mcp
Transport: Streamable HTTP
Authentication: API Key
API key: contents of ~/.config/hive-pipe/tokens/perplexity.token
```

Perplexity commonly uses normal shell wrappers such as `bash -lc` for terminal
work. Hive Pipe permits those wrappers now. If Perplexity can list tools but
terminal calls fail, first test `terminal_pwd`, then run:

```json
{
  "name": "terminal_run",
  "arguments": {
    "argv": ["bash", "-lc", "printf PERPLEXITY_TERMINAL_OK"],
    "cwd": "/home/Scales/One-Wave-Science",
    "timeout": 30
  }
}
```

Expected stdout:

```text
PERPLEXITY_TERMINAL_OK
```

## First terminal call

Call `terminal_pwd`, then test:

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

A successful result has:

```text
stdout = AI_TERMINAL_OK
exit_code = 0
```

## Direct Python and C++

The gateway exposes first-class `python_run` and `cpp_compile_run` MCP tools so an
authorized AI can run bounded source directly without a human terminal relay.
See `One_Wave_Bench/bridges/docs/AI_CODE_BRIDGE.md` for schemas, examples, limits, and verification.

## Enter the visible Miniverse room

The shared 3D/MUD room runs locally at:

```text
http://127.0.0.1:8787/
```

Source and instructions:

```text
Miniverse/room3d/README.md
```

Any authorized AI that can use Hive Pipe terminal access can enter the same
persistent room state without a human relaying commands:

```bash
python3 /home/Scales/miniverse-room-runtime/Miniverse/room3d/client.py join codex --name CODEX --role "AI CODER" --color '#86a8ff'
python3 /home/Scales/miniverse-room-runtime/Miniverse/room3d/client.py say codex "I am in the shared room."
python3 /home/Scales/miniverse-room-runtime/Miniverse/room3d/client.py move codex A+
python3 /home/Scales/miniverse-room-runtime/Miniverse/room3d/client.py bench codex workshop TEST "tests passed"
```

The six legal movement directions are `A+`, `B+`, `C+`, `A-`, `B-`,
and `C-`. The browser, CLI agents, chat, body locations, and workbench receipts
all use the same state. The room contains no built-in LLM; an external AI client
takes an identity and uses the existing authenticated bridge.

The room server is `miniverse-room.service`. Its persistent state is under
`~/.local/share/one-wave/miniverse-room/`. A graphical login autostarts the
local browser view.

TEST LAB has a persistent experiment ledger and visible controls. Built-in
software experiments plus external Python/C++/Virtual Breadboard receipts are
documented in `Miniverse/room3d/EXPERIMENT_LAB.md`.

For custom AI bodies, new districts, workbenches, objects, animation, and world
expansion, read `Miniverse/EXPAND_MINIVERSE.md` before editing. The native laptop
program and shortcut are documented in `Miniverse/desktop/README.md`.

## Repo work sequence

Before editing:

```json
["git","status","--short","--branch"]
["git","rev-parse","HEAD"]
["git","remote","-v"]
```

Read the repository's canonical project instructions before changing project
logic. Never claim a command/file was checked unless the tool returned it.

For writes, use a task branch rather than silently changing `main`:

```json
["git","switch","-c","ai/task-name"]
```

After changes:

```json
["git","diff","--check"]
["git","status","--short"]
```

Run the relevant tests, review the diff, commit, then push the task branch when
GitHub credentials are available.

## GitHub -> Jetson

Use `.github/workflows/jetson-command.yml` (`Jetson Command Lane`). Preferred
input is `argv_json`, for example:

```json
["git","status","--short","--branch"]
```

The workflow is deliberately `workflow_dispatch` only and runs on a GitHub-hosted
runner. It sends an authenticated MCP `terminal_run` call to the Jetson.

## Jetson -> GitHub

The terminal parser may run normal git commands:

```json
["git","fetch","origin"]
["git","push","-u","origin","HEAD"]
```

Do not push directly to `main` as routine AI behavior. Use a task branch + PR.
If fetch works but push fails, fix Jetson GitHub credentials; do not build a new
terminal bridge.

## Direct HTTPS client

`One_Wave_Bench/bridges/scripts/jetson_remote.sh` uses the same MCP parser:

```bash
One_Wave_Bench/bridges/scripts/jetson_remote.sh \
  --cwd /home/Scales/One-Wave-Science \
  -- git status --short --branch
```

## SSH recovery

SSH is intentionally independent:

```bash
ssh Scales@JETSON_IP
```

If the tunnel/MCP path breaks, SSH is the recovery route.

## External work

GitHub-visible handoff:

```text
One_Wave_Bench/bridges/external-work/External_Work/inbox/
One_Wave_Bench/bridges/external-work/External_Work/outbox/
```

Jetson-local external workspace:

```text
~/One-Wave-External-Work/inbox/
~/One-Wave-External-Work/work/
~/One-Wave-External-Work/outbox/
```

GitHub -> Jetson local:

```json
["python3","One_Wave_Bench/bridges/scripts/external_work_bridge.py","pull"]
```

Jetson local -> GitHub staging:

```json
["python3","One_Wave_Bench/bridges/scripts/external_work_bridge.py","publish"]
```

`publish` only copies into `One_Wave_Bench/bridges/external-work/External_Work/outbox`; it does not commit or push.
Review and publish through a task branch/PR.

## Safety boundary

Normal authenticated AI terminal access runs as the Jetson's ordinary user and
supports normal shell wrappers, including `bash -lc`.

Direct invocation of a small set of high-risk system programs remains blocked,
including privilege escalation, raw disk formatting/partitioning, mounting, and
power-control commands. Credential/private-key paths are also rejected by the
parser. These command checks are secondary guardrails, not the primary security
boundary.

The primary boundaries are:

```text
per-client authentication token
normal non-root user
systemd NoNewPrivileges
ProtectSystem=strict
explicit writable repo/workspace paths
independent SSH recovery
```

The service sandbox permits writes to the live Hive Pipe checkout, the canonical
`~/One-Wave-Science` checkout when present, and the explicit
`~/One-Wave-External-Work` workspace. System paths remain read-only.

## Full reference
Read `One_Wave_Bench/bridges/docs/JETSON_AI_ACCESS.md` for setup, tokens, tunnel configuration, all paths,
and the acceptance tests.


---

## SOURCE FILE: One_Wave_Bench/bridges/docs/CHATGPT_JETSON_PULL_BRIDGE.md

# ChatGPT -> One-Wave Resilient Terminal Bridge

This is the no-GitHub-Actions-secret path for bounded terminal work on either
the Ubuntu laptop or the Jetson. Install it on the machine ChatGPT must operate.
It has two independent loops: a transport state machine and a request state
machine.

## Path

```text
ChatGPT GitHub connector
  -> chatgpt-terminal branch
  -> .chatgpt-terminal/request.json
  -> laptop/Jetson user service polls primary and backup Git routes
  -> One_Wave_Bench/bridges/hive-pipe/terminal_parser.py
  -> local non-root command on the machine running the service
  -> .chatgpt-terminal/result.json
  -> target-machine git push
  -> ChatGPT GitHub connector reads result
```

The worker does not use the remote MCP bearer token because execution occurs on
the target machine itself. It deliberately reuses `One_Wave_Bench/bridges/hive-pipe/terminal_parser.py`,
so blocked programs (including inside shell wrappers), sensitive-path checks,
timeout/output limits, and authorized work-root checks remain in force.

## The two state machines

1. **Transport state machine:** tries `origin:chatgpt-terminal`, then
   `origin:chatgpt-terminal-backup`, plus any configured mirror routes. Healthy
   routes gain preference. Failed routes enter exponential backoff and are
   probed again later. A result is returned through the first writable healthy
   back route.
2. **Request state machine:** journals `accepted -> executing -> completed ->
   acknowledged`. The executing phase is recorded before launch. After a crash,
   an uncertain command is not silently repeated; the bridge returns a
   reconciliation receipt and asks for inspection.

This gives failover without duplicate side effects. No finite set of routes can
promise connectivity during every provider, power, or hardware failure, so
pending results remain in a durable local outbox until a configured route heals.

## Parser reference and intervention guidance

MCP clients can call `terminal_reference` with no arguments. Every command
receipt also includes `guidance` and a reference pointer. Guidance names whether
the next action is:

- a normal AI correction;
- creation/authorization of a dedicated work path;
- tool installation;
- authentication repair; or
- an approved human/root-level action outside the parser.

The parser explains the boundary; it never bypasses it.

## Runtime isolation

The bridge no longer depends on the branch state of the user's active `~/One-Wave-Science` checkout. That checkout may be ahead, behind, dirty, or diverged.

The installer creates and owns a private runtime clone at:

```text
~/.local/share/one-wave-chatgpt-terminal-runtime
```

Only that bridge runtime is reset to `origin/main`. The user's active project checkout is never merged, reset, rebased, or switched by bridge installation or polling.

## Files

- `One_Wave_Bench/bridges/hive-pipe/chatgpt_terminal_pull.py` — polling/execution/result worker
- `One_Wave_Bench/bridges/hive-pipe/install_chatgpt_terminal_pull.sh` — isolated-runtime user-systemd installer
- `One_Wave_Bench/bridges/hive-pipe/bootstrap_chatgpt_terminal_pull.sh` — fetch-only bootstrap helper
- dedicated transport branch: `chatgpt-terminal`
- request: `.chatgpt-terminal/request.json`
- result: `.chatgpt-terminal/result.json`

## One-time activation on the Ubuntu laptop or Jetson

From inside the existing checkout on the machine to control:

```bash
cd "$HOME/One-Wave-Science"
git fetch origin main
git show origin/main:One_Wave_Bench/bridges/hive-pipe/install_chatgpt_terminal_pull.sh | ONE_WAVE_PROJECT_ROOT="$PWD" bash
```

This reads the current installer directly from `origin/main` without merging
`main` into the active laptop/Jetson branch.

Verify:

```bash
systemctl --user is-active one-wave-chatgpt-terminal-pull.service
```

Expected:

```text
active
```

This activation does not need a Cloudflare tunnel or GitHub Actions secrets. It
does require the machine's existing GitHub read/write authentication so the
runtime can fetch requests and push receipts.

The two default transport branches must exist:

```text
chatgpt-terminal
chatgpt-terminal-backup
```

To add a true provider/mirror route, configure another Git remote in the private
runtime clone and extend the service environment, for example:

```text
CHATGPT_TERMINAL_ROUTES=primary=origin:chatgpt-terminal,backup=origin:chatgpt-terminal-backup,mirror=mirror:chatgpt-terminal
```

Route errors and the required repair/path-creation action are recorded in:

```text
~/.local/state/one-wave-chatgpt-terminal/bridge_state.json
```

Status is available without executing a command:

```bash
python3 ~/.local/share/one-wave-chatgpt-terminal-runtime/One_Wave_Bench/bridges/hive-pipe/chatgpt_terminal_pull.py --status
journalctl --user -u one-wave-chatgpt-terminal-pull.service -n 100 --no-pager
```

## Request format

```json
{
  "id": "printer-diagnostic-001",
  "argv": ["lpstat", "-t"],
  "cwd": "/home/Scales/One-Wave-Science",
  "timeout": 30
}
```

The worker records request id + request commit locally and will not rerun the same request commit.

## Printer diagnostics

The initial queued request checks CUPS status, configured queues, USB devices, and printer backends. Follow-up requests should stay bounded so one missing command does not hide other evidence.

Do not add `sudo` or weaken the terminal parser to repair a printer. If a repair requires a privileged package/service operation, the bridge reports the exact required action rather than bypassing the safety boundary.

## Safety / branch isolation

The worker fetches `origin/chatgpt-terminal`, executes only structured `argv` through the existing parser, then uses a temporary detached git worktree to write `result.json`. The user's active branch/worktree is not switched or reset.

The service runs as the normal user with `NoNewPrivileges=true`, `ProtectSystem=strict`, and explicit writable paths for the bridge runtime, bridge state, the project checkout, and the external-work directory.

## Acceptance test

Run the full existing Hive Pipe suite, including the compatibility tests:

```bash
PYTHONPATH=One_Wave_Bench/hive-pipe python3 -m unittest discover -s One_Wave_Bench/hive-pipe -p 'test_*.py' -v
```


---

## SOURCE FILE: One_Wave_Bench/bridges/docs/CHATGPT_JETSON_TERMINAL_BRIDGE.md

# ChatGPT -> Jetson Terminal Bridge

## Purpose

This bridge lets an authorized GitHub-connected ChatGPT session request a normal, non-root Jetson terminal command without exposing Hive Pipe tokens in chat or in the repository.

It does **not** replace Hive Pipe. It is a small GitHub request/result lane over the existing canonical path:

```text
ChatGPT GitHub connector
  -> chatgpt-terminal branch
  -> .chatgpt-terminal/request.json
  -> GitHub Actions
  -> authenticated Hive Pipe /mcp terminal_run
  -> Jetson terminal_parser.py
  -> .chatgpt-terminal/result.json
  -> ChatGPT GitHub connector
```

The Jetson parser remains the command safety boundary. The bridge cannot bypass parser restrictions, the Jetson service sandbox, normal-user permissions, or blocked credential/private-key paths.

## Dedicated command branch

After the bridge workflow is merged to `main`, create a dedicated branch from current `main`:

```text
chatgpt-terminal
```

Normal project work must not happen on that branch. It carries only terminal request/result traffic.

## Request format

ChatGPT writes or updates:

```text
.chatgpt-terminal/request.json
```

Example:

```json
{
  "id": "printer-check-001",
  "argv": ["lpstat", "-t"],
  "cwd": "/home/Scales/One-Wave-Science",
  "timeout": 30
}
```

Required:

- `id`: non-empty string, max 128 characters
- `argv`: non-empty JSON array of non-empty strings

Optional:

- `cwd`: absolute path; defaults to `/home/Scales/One-Wave-Science`
- `timeout`: integer 1..300; defaults to 120

A new commit changing only `request.json` triggers `.github/workflows/chatgpt-terminal-bridge.yml`.

## Result format

The workflow writes:

```text
.chatgpt-terminal/result.json
```

The result contains the matching request `id`, command argv, stdout, stderr, exit code, Jetson cwd/duration when provided by Hive Pipe, and bridge/RPC errors when applicable.

The result commit includes `[skip ci]`; the workflow path filter watches only `request.json`, so result commits do not recurse.

## First acceptance test

Request:

```json
{
  "id": "bridge-smoke-001",
  "argv": ["printf", "CHATGPT_JETSON_BRIDGE_OK"],
  "cwd": "/home/Scales/One-Wave-Science",
  "timeout": 30
}
```

Expected result:

```text
stdout = CHATGPT_JETSON_BRIDGE_OK
exit_code = 0
ok = true
```

## Printer diagnostic request

A useful non-destructive printer check is:

```json
{
  "id": "printer-diagnostic-001",
  "argv": ["bash", "-lc", "printf '\\n=== CUPS ===\\n'; systemctl is-active cups; printf '\\n=== PRINTERS ===\\n'; lpstat -t; printf '\\n=== USB ===\\n'; lsusb"],
  "cwd": "/home/Scales/One-Wave-Science",
  "timeout": 30
}
```

Normal-user diagnostics should work if the relevant programs are installed. Privilege escalation remains blocked by the Jetson parser; do not weaken that boundary merely to repair a printer.

## Security / anti-drift rules

1. Tokens stay in GitHub Actions secrets and on the Jetson. Never place them in request/result JSON.
2. Only the dedicated `chatgpt-terminal` branch triggers this workflow.
3. Only changes to `.chatgpt-terminal/request.json` trigger a command.
4. The bridge sends only `terminal_run` requests to the existing `/mcp` endpoint.
5. All command validation and system access restrictions already enforced by `terminal_parser.py` remain active.
6. Do not add `sudo`, root credentials, disk-management bypasses, token readers, or a second unrestricted execution path.
7. Project edits still use task branches and PRs; the terminal branch is command transport only.


---

## SOURCE FILE: One_Wave_Bench/bridges/docs/JETSON_ACCESS_AND_TERMINAL.md

# Jetson Access and Terminal Entry Point

**Purpose:** give human and AI contributors one safe, reproducible starting point for working on the Jetson without guessing credentials, IP addresses, paths, or storage targets.

## Rules

- Do not guess a Jetson IP address.
- Do not guess a username.
- Do not format or repartition attached storage just to start development.
- Do not treat an external drive as disposable unless it has been explicitly verified disposable.
- Prefer reversible user-space directories/containers before filesystem/kernel work.
- Record the exact machine, branch, command, and result in the relevant construction log/receipt.

## On the Jetson itself

Open a terminal and identify the current user and network addresses:

```bash
whoami
hostname
hostname -I
ip addr
```

Use the actual username returned by `whoami` and an address belonging to the intended LAN interface.

To verify SSH service state:

```bash
systemctl status ssh --no-pager
```

If OpenSSH server is installed but not running, a human/operator with appropriate permissions may enable/start it according to the system's Ubuntu configuration. Do not change security settings merely to make automation convenient.

## From another machine on the same trusted LAN

Use the verified username and verified Jetson LAN address:

```bash
ssh <verified-user>@<verified-jetson-ip>
```

Example shape only:

```text
ssh user@192.168.x.x
```

The example is not a credential or known address. Replace both fields from the Jetson's own output.

After connecting, verify you reached the intended machine:

```bash
whoami
hostname
uname -a
pwd
```

## Repository entry

Do not assume the checkout path. Locate the repository safely:

```bash
find "$HOME" -maxdepth 4 -type d -name One-Wave-Science 2>/dev/null
```

Then enter the verified path and inspect before editing:

```bash
cd <verified-path>/One-Wave-Science
git status
git branch --show-current
git log -1 --oneline
```

For shared AI work, create/use an isolated branch rather than editing another contributor's active branch.

## External-drive discovery

Before using an attached external drive, identify devices and mounts without changing them:

```bash
lsblk -o NAME,SIZE,FSTYPE,LABEL,UUID,MOUNTPOINTS,MODEL
findmnt
```

If the intended drive is already mounted, use its verified mount point. If it contains user data or its purpose is uncertain, stop there and do not modify it.

For Miniverse/Mega City prototyping, prefer creating a normal project directory on a verified writable mounted drive, for example:

```bash
mkdir -p <verified-mount>/one-wave-miniverse
```

Do not substitute a guessed mount path.

## First Miniverse storage rule

The first one-room looper prototype must work using ordinary reversible storage:

- directory tree;
- SQLite/database file;
- JSON/state bundle;
- disk-image/container file;
- another user-space format with integrity checks.

The experimental lattice/storage architecture is a later track. It must prove read/write integrity, migration, backup, and recovery before any destructive formatting path is considered.

## Terminal bridge / AI access direction

A terminal bridge for AI collaborators should expose bounded, auditable operations rather than unrestricted silent control. Minimum requirements:

- identify the acting AI/worker;
- record command, working directory, timestamp, exit status, and relevant output;
- show which repository branch is active;
- require explicit handling for destructive commands;
- separate read/inspect capability from write/mutate capability where practical;
- preserve a human-visible emergency stop/reset path.

The bridge should support the project honor system, not bypass it.

## Related work

Read alongside:

- `README.md`
- `AI_CANONICAL_START_HERE.md`
- `AI_FOREMAN_WORK_REGISTER.md`
- `MEGA_CITY_LOOPER_OBJECTIVE.md`
- `One_Wave_Bench/Virtual_Breadboard/AI_COLLABORATION.md`
- `One_Wave_Bench/Virtual_Breadboard/AI_CONSTRUCTION_LOG.md`

Any contributor who discovers a more reliable Jetson access/runtime path should update this file with the tested commands and sign the corresponding construction entry.

---

## SOURCE FILE: One_Wave_Bench/bridges/docs/JETSON_AI_ACCESS.md

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
          /mcp
           |-- terminal_run
           |-- python_run
           +-- cpp_compile_run
                 ^
                 |
       direct HTTPS/MCP client

Independent recovery route:
AI/operator ---------------- SSH ----------------> Jetson normal-user shell

External work handoff:
GitHub One_Wave_Bench/bridges/external-work/External_Work/inbox  -->  ~/One-Wave-External-Work/inbox
GitHub One_Wave_Bench/bridges/external-work/External_Work/outbox <--  ~/One-Wave-External-Work/outbox
```

All routine routes run as the normal Jetson user. `sudo`, raw-disk formatting,
power commands, credential/private-key paths, and other high-risk system operations
remain blocked. Normal development shell wrappers such as `bash -lc` are supported.

## One canonical gateway

Use:

```text
One_Wave_Bench/bridges/hive-pipe/gateway.py
One_Wave_Bench/bridges/hive-pipe/terminal_parser.py
One_Wave_Bench/bridges/hive-pipe/install_gateway.sh
```

Do **not** start `One_Wave_Bench/bridges/scripts/jetson_gateway.py` alongside Hive Pipe. Both use port
8765. `One_Wave_Bench/bridges/scripts/install_jetson_gateway.sh` is now only a compatibility entrypoint
that delegates to the Hive Pipe installer and can migrate the older gateway
bearer token into the Hive Pipe Codex token.

## 1. Install/restart Hive Pipe on the Jetson

From the real checkout:

```bash
cd "$HOME/One-Wave-Science"
git pull --ff-only origin main
bash One_Wave_Bench/bridges/hive-pipe/install_gateway.sh
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

Emergency stop: run `systemctl --user stop hive-pipe-gateway.service hive-pipe-agent.service`; stopping only the gateway blocks new MCP calls but leaves the queue worker running, and SSH remains independent.

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

Available terminal/code tools:

```text
terminal_pwd
terminal_which
terminal_run
python_run
cpp_compile_run
```

`terminal_run` executes structured argv. `python_run` accepts Python source
directly, writes it to a temporary script inside an authorized work root, runs it
with `python3`, captures stdout/stderr/exit status, and removes the temporary
source. `cpp_compile_run` accepts C++ source directly, compiles it with `g++`,
runs the temporary binary, returns compile/runtime receipts, and removes the
temporary source and binary.

Examples:

```json
{"name":"python_run","arguments":{"code":"print(6 * 7)","cwd":"/home/Scales/One-Wave-Science"}}
```

```json
{"name":"cpp_compile_run","arguments":{"code":"#include <iostream>\nint main(){std::cout << 6*7 << \"\\n\";}","standard":"c++20","cwd":"/home/Scales/One-Wave-Science"}}
```

Both should return stdout `42`. Direct source is bounded to 12 KiB per call and
uses the same authenticated non-root Hive Pipe sandbox and authorized work roots
as `terminal_run`. See `One_Wave_Bench/bridges/docs/AI_CODE_BRIDGE.md` for the full schemas and limits.

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
["python3","One_Wave_Bench/bridges/scripts/external_work_bridge.py","status"]
```

## 5. Direct remote client -> Jetson

`One_Wave_Bench/bridges/scripts/jetson_remote.sh` also uses Hive Pipe MCP `terminal_run`.

Example:

```bash
export JETSON_GATEWAY_URL='https://YOUR-TUNNEL'
export JETSON_GATEWAY_TOKEN='authorized-token'

One_Wave_Bench/bridges/scripts/jetson_remote.sh \
  --cwd /home/Scales/One-Wave-Science \
  -- git status --short --branch
```

External workspace example:

```bash
One_Wave_Bench/bridges/scripts/jetson_remote.sh \
  --cwd /home/Scales/One-Wave-External-Work \
  -- find . -maxdepth 2 -type f
```

## 6. SSH -> Jetson independent path

Enable SSH with:

```bash
cd "$HOME/One-Wave-Science"
bash One_Wave_Bench/bridges/scripts/enable_jetson_ssh.sh
```

Optionally add an authorized client's **public** key:

```bash
AI_SSH_PUBLIC_KEY='ssh-ed25519 AAAA... ai-worker-name' \
  bash One_Wave_Bench/bridges/scripts/enable_jetson_ssh.sh
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
One_Wave_Bench/bridges/external-work/External_Work/inbox/
One_Wave_Bench/bridges/external-work/External_Work/outbox/
```

Jetson-local paths:

```text
~/One-Wave-External-Work/inbox/
~/One-Wave-External-Work/work/
~/One-Wave-External-Work/outbox/
```

### GitHub -> Jetson external work

After the repo receives files under `One_Wave_Bench/bridges/external-work/External_Work/inbox/`:

```bash
cd "$HOME/One-Wave-Science"
git pull --ff-only origin main
python3 One_Wave_Bench/bridges/scripts/external_work_bridge.py pull
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
python3 One_Wave_Bench/bridges/scripts/external_work_bridge.py publish
git status --short One_Wave_Bench/bridges/external-work/External_Work/outbox
```

The bridge copies them to `One_Wave_Bench/bridges/external-work/External_Work/outbox/` but does not commit or push.
Publish them through a task branch/PR.

See `One_Wave_Bench/bridges/external-work/External_Work/README.md` for the handoff rules.

## 9. Access matrix

| Direction | Path | Depends on |
|---|---|---|
| AI/operator -> Jetson | SSH | LAN/SSH + authorized key |
| AI/client -> Jetson | HTTPS `/mcp` | tunnel + Hive Pipe token |
| GitHub -> Jetson | `Jetson Command Lane` | Actions secrets + tunnel + Hive Pipe |
| Jetson -> GitHub | git/gh | Jetson GitHub credentials |
| GitHub -> external work | `One_Wave_Bench/bridges/external-work/External_Work/inbox` + bridge pull | git sync + local workspace |
| external work -> GitHub | bridge publish + task branch/PR | git push credentials |

## 10. Acceptance test

Do these in order:

1. `hive-pipe-agent.service` is active.
2. `hive-pipe-gateway.service` is active.
3. Local MCP `terminal_run` returns `AI_TERMINAL_OK`.
4. MCP `python_run` with `print(6 * 7)` returns `42`.
5. MCP `cpp_compile_run` with a tiny C++ program returns `42`.
6. Direct remote `One_Wave_Bench/bridges/scripts/jetson_remote.sh -- uname -a` returns Jetson output.
7. GitHub `Jetson Command Lane` with `["uname","-a"]` returns Jetson output.
8. `ssh Scales@JETSON_IP` works independently.
9. `git fetch origin` works on the Jetson.
10. A disposable task branch can be pushed from Jetson to GitHub.
11. External-work bridge `pull` moves a test file GitHub -> Jetson local inbox.
12. External-work bridge `publish` moves a test file Jetson local outbox -> repo outbox.

When all twelve pass, both directions and the independent recovery paths are live.


---

## SOURCE FILE: One_Wave_Bench/bridges/docs/JETSON_GEMINI_MINIMAL.md

# Jetson Gemini — Minimal-Token External Worker

## Purpose

Gemini is the **external escalation/review lane** for the Jetson. It is not the
default worker.

Normal order:

```text
Deterministic tools/tests
        ↓
local Qwen / OpenClaw
        ↓ only when external judgment is useful
Gemini flash-lite review
        ↓ only for bounded coding that needs more capability
Gemini flash code
        ↓ explicit opt-in only
Gemini pro/deep
```

This keeps routine work local and avoids repeatedly sending repository context
to a cloud model.

## What is committed

```text
GEMINI.md                         tiny always-loaded project rules
.gemini/settings.json             low-context/session/tool-output limits
.geminiignore                     blocks binaries, caches, generated files, secrets
One_Wave_Bench/bridges/scripts/install_gemini_jetson.sh user-local installer; no sudo
One_Wave_Bench/bridges/scripts/gemini_min.sh             bounded review/code/ask/deep runner
GEMINI_TASK_TEMPLATE.md           small task packet template
```

## Install on the Jetson

From the existing checkout:

```bash
cd /home/Scales/One-Wave-Science
git pull --ff-only origin main
bash One_Wave_Bench/bridges/scripts/install_gemini_jetson.sh
```

The installer uses the official npm package and installs it under
`~/.local`, so it does not need sudo.

## Authenticate once

Preferred path is the official Gemini CLI's own Google login. On a Jetson or
SSH terminal with no browser:

```bash
cd /home/Scales/One-Wave-Science
NO_BROWSER=true ~/.local/bin/gemini
```

Complete the URL/code flow in another browser when prompted. The official CLI
caches its own credential for later sessions.

An API key is an optional supported authentication path, not a repository
requirement. If you use one, keep it outside the repository (for example in a
private shell environment). Never commit it to `.env`, task files, logs, or
GitHub.

Do not route Gemini CLI OAuth credentials through OpenClaw or another
third-party provider. If later programmatic service-to-service Gemini access is
needed, treat that as a separate supported API-key/Vertex integration.

## First smoke test

```bash
cd /home/Scales/One-Wave-Science
bash One_Wave_Bench/bridges/scripts/gemini_min.sh ask "Reply with only: GEMINI JETSON OK"
```

The wrapper requests JSON output. Gemini CLI includes usage statistics in its
headless JSON result, so input/output/thought/tool token usage can be inspected
instead of guessed.

## Bounded review

Create a tiny task packet. Reference files by path instead of pasting them.

```bash
cp GEMINI_TASK_TEMPLATE.md /tmp/gemini-task.md
nano /tmp/gemini-task.md
bash One_Wave_Bench/bridges/scripts/gemini_min.sh review /tmp/gemini-task.md
```

`review` uses `flash-lite`.

## Bounded coding

Use a separate branch/worktree. The wrapper refuses `main` and a dirty working
tree by default so Gemini does not collide with Codex or another worker.

```bash
cd /home/Scales/One-Wave-Science
git switch -c gemini/my-bounded-task
bash One_Wave_Bench/bridges/scripts/gemini_min.sh code /tmp/gemini-task.md
```

`code` uses `flash` and `auto_edit`: file edit tools may proceed, while broader
commands are not silently YOLO-approved. The task should name allowed files and
the deterministic test to run afterward.

## Deep model is intentionally gated

```bash
GEMINI_ALLOW_PRO=1 bash One_Wave_Bench/bridges/scripts/gemini_min.sh deep /tmp/gemini-task.md
```

Do not make this the normal path. If `flash-lite` or local Qwen can answer the
question, using Pro just burns more external inference.

## Token controls

Project settings intentionally:

- default to `flash-lite`;
- cap session turns;
- trigger context compression early;
- lower retained/history token budgets;
- summarize large shell output before it becomes model context;
- disable recursive file search;
- respect `.gitignore` and `.geminiignore`;
- disable Gemini auto-memory for this repo;
- disable usage-statistics telemetry;
- disable YOLO mode and permanent tool approval.

The wrapper additionally:

- disables extensions with `--extensions none`;
- rejects task packets larger than 16 KB;
- includes only repo/branch/HEAD plus the bounded task in its prompt;
- tells Gemini not to scan or summarize unrelated files;
- defaults review/ask to `flash-lite`;
- uses `flash` only for code;
- requires explicit `GEMINI_ALLOW_PRO=1` for Pro;
- refuses coding directly on `main` unless explicitly overridden.

## Working with local Qwen/OpenClaw

Keep the two paths separate:

```text
M4 / OpenClaw
    └── local qwen3.5:2b
           ├── deterministic test enough -> finish locally
           └── external judgment useful -> write tiny task/reference packet
                                                ↓
                                     official Gemini CLI wrapper
```

OpenClaw does not need Gemini credentials. It can prepare a small task/reference
file for the official Gemini process, and the returned bounded result can be
reviewed locally.

## Miniverse

The current Miniverse MUD PR already accepts an agent identity named `gemini`,
but that client is a coordination terminal, not an autonomous model process.
First prove this official Gemini CLI worker on the Jetson. Then an Agent Gateway
can hand bounded MUD jobs to this wrapper without giving Gemini unrestricted
shell, raw-device, or credential authority.
## Hard stops

Gemini must not receive:

- raw-drive or formatting authority;
- sudo authority;
- repository/API credentials;
- whole-repo dumps as routine context;
- an instruction to merge its own work;
- permission to rewrite its own acceptance criteria silently.

Prefer reference paths and deterministic tests. External model output is a
candidate/review, not self-validating evidence.


---

## SOURCE FILE: One_Wave_Bench/bridges/docs/JETSON_OPENCLAW_RUNTIME.md

# Jetson Orin + OpenClaw Runtime Contract

## Main purpose

This repository builds a Field/Void software-construction engine for coding, app building, and program building. The runtime must remain centered on creating, modifying, testing, validating, and improving real software.

## Local machine target

Canonical local checkout on the Jetson Orin:

`$HOME/One-Wave-Science`

Every branch-step project must begin by resolving and recording the real local repository state:

```bash
cd "$HOME/One-Wave-Science"
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git worktree list
```

If `$HOME/One-Wave-Science` is not a valid Git checkout, STOP and report `BLOCKED_REPO_PATH`. Do not guess another path and do not edit files outside the verified repository root.

## M4 / OpenClaw control

OpenClaw is the M4 orchestration layer. M4 owns:

- current branch-step project
- execution queue
- current goal and success criteria
- Field/Void dispatch order
- attempt counter and three-strike rule
- test execution
- branch/worktree verification
- progress diary updates
- working-feature ledger
- failed-approach ledger
- commit/handoff state
- escalation packets

Field and Void do not own the loop. They operate inside the bounded step selected by M4.

OpenClaw-compatible headless execution should use the repository as the working directory, for example:

```bash
openclaw agent exec --cwd "$HOME/One-Wave-Science" --message-file TASK.md --json
```

OpenClaw configuration may instead assign dedicated agent workspaces, but each software-building agent must resolve back to the verified project checkout/worktree before changing code.

## Compute split on Jetson Orin

### Field — GPU priority

Field is the expressive software-building side. Give Field priority access to GPU-backed local inference and GPU-heavy program tasks when available.

Field responsibilities include:

- proposing software changes
- writing/modifying source code
- building apps and programs
- code generation/refactoring
- compiling/building
- GPU-appropriate tests, rendering, simulation, or model-assisted coding work
- producing the candidate next software state

Field must still make one targeted change at a time and must not self-approve architectural correctness.

### Void — CPU priority

Void is the oversight/override side. Prefer CPU execution for Void so oversight remains independently available while Field consumes GPU resources.

Void responsibilities include:

- reconstructing the known-good reference
- checking the current goal and branch boundary
- reviewing proposed changes before execution
- comparing intended versus actual diff
- checking tests, logs, architecture, regressions, APIs, state flow, UI behavior, and runtime behavior
- protecting verified features
- issuing `ALLOW`, `CORRECT`, `OVERRIDE`, `HOLD`, or `ESCALATE`
- writing oversight notes and reflection

Void may use deterministic CPU tools before model inference: Git diff/status, linters, tests, schema checks, static analysis, log comparison, file/hash comparison, and project-specific validation.

## Resource isolation rule

Field may use the GPU, but it must never monopolize the machine so completely that M4/OpenClaw cannot run the control loop or Void cannot perform oversight.

Priority order:

1. M4/OpenClaw remains responsive.
2. Void oversight can execute.
3. Field receives remaining GPU-heavy capacity.
4. Background/noncritical work yields first under memory or thermal pressure.

M4 must stop or defer noncritical work when memory pressure, thermal throttling, or repeated process failure makes results unreliable.

## Branch-step project law

Every assigned task becomes one bounded branch-step project. The branch-step packet must contain:

- MAIN GOAL
- WHY THIS STEP EXISTS
- CURRENT STEP GOAL
- HARD START
- LOCAL REPO ROOT
- ACTIVE BRANCH / WORKTREE / HEAD
- REFERENCE FILES
- ALLOWED FILES
- PROTECTED WORKING FEATURES
- EXACT ACTION
- SUCCESS CRITERIA
- TEST COMMANDS
- FIELD NOTES
- VOID OVERSIGHT / OVERRIDE NOTES
- PROGRESS REPORT
- ATTEMPT / STRIKE COUNT
- LOOK-BACK REFLECTION
- HARD STOP
- HANDOFF / NEXT PERMITTED STEP

No task may be executed as an unbounded chat instruction when it can be represented as a branch-step project.

## Execution order

1. M4 loads the branch-step packet.
2. M4 verifies `$HOME/One-Wave-Science`, branch/worktree, HEAD, and clean/known state.
3. Field reads the complete reference and proposes one targeted software change.
4. Void performs pre-change oversight and returns `ALLOW`, `CORRECT`, `OVERRIDE`, `HOLD`, or `ESCALATE`.
5. Only `ALLOW` permits the targeted change.
6. Field performs one change.
7. M4 runs the exact tests/checks.
8. Field records what the evidence shows.
9. Void performs post-change oversight against the reference, diff, tests, and protected features.
10. M4 records the decision and updates diary/ledgers.
11. On success, commit and move only to the next permitted branch-step.
12. On failure, apply the three-strike rule.
13. At the hard stop, stop. Do not leak work into the next branch.

## Three-strike rule

Each specific approach receives at most three meaningful attempts.

- Attempt 1: execute the intended approach.
- Attempt 2: make a targeted correction from new evidence.
- Attempt 3: final evidence-based correction within that approach.

After three failures:

- STOP the approach.
- Record it in the failed-approach ledger.
- Summarize what each attempt proved.
- Select a materially different approach and reset to 1/3.
- If no credible different approach exists, or the replacement approach also becomes stuck, `ESCALATE` for help.

Never disguise Attempt 4 as a new approach.

## Look-back reflection law

Before any branch-step is allowed to close, Field, Void, and M4 must answer:

- What changed?
- What actually worked?
- What did not work?
- What evidence proves the result?
- What did we learn?
- Which assumption changed?
- Did previously verified software still work?
- Did this step advance the MAIN GOAL of building the coding/app/program engine?
- What state must the next branch-step inherit?

## Hard stop law

The active branch-step ends when its explicit success criteria and hard-stop condition are satisfied, or when it is blocked/escalated. Reaching a hard stop means STOP. The next step requires a new branch-step packet and a new M4 dispatch.


---

## SOURCE FILE: One_Wave_Bench/bridges/docs/UPDATED_54_TRIAD_BRAIN_JETSON_OPTIONAL.md

# Updated 54 — Triad brain; Jetson optional

G-752. Native brain is DC/AC/QC on CPU_REFERENCE. Jetson runtime is a skin. STOP remains VOID+HOLD+Resolving.


---

## SOURCE FILE: One_Wave_Bench/bridges/hive-pipe/DEEPSEEK_BRIDGE.md

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


---

## SOURCE FILE: One_Wave_Bench/bridges/hive-pipe/DEEPSEEK_WEB_RELAY.md

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


---

## SOURCE FILE: One_Wave_Bench/bridges/hive-pipe/README-CHATGPT-BRIDGE-FIX.md

# ChatGPT terminal bridge repair acceptance

The bridge bootstrap is considered repaired when all of the following are true:

1. The user's active `~/One-Wave-Science` checkout may be diverged from `origin/main`.
2. Running the fetch-only bootstrap does not merge, reset, rebase, or switch that checkout.
3. Bridge code runs from `~/.local/share/one-wave-chatgpt-terminal-runtime` at `origin/main`.
4. `one-wave-chatgpt-terminal-pull.service` is active as a user service.
5. The queued `printer-diagnostic-001` request on `chatgpt-terminal` produces `.chatgpt-terminal/result.json`.
6. Subsequent ChatGPT requests can be sent by updating `.chatgpt-terminal/request.json` without local terminal work.


---

## SOURCE FILE: One_Wave_Bench/bridges/hive-pipe/README.md

# Hive Pipe v3

Start with [`One_Wave_Bench/bridges/docs/AI_BRIDGE_START_HERE.md`](../../One_Wave_Bench/bridges/docs/AI_BRIDGE_START_HERE.md). It contains
the supported route order, exact smoke tests, pull-bridge request/result format,
and the unified read-only health command:

```bash
python3 One_Wave_Bench/bridges/hive-pipe/bridge_doctor.py --profile all
```

Hive Pipe is the authenticated Jetson-side tool gateway used by AI clients,
GitHub Actions, and direct remote clients.

It exposes:

```text
MCP / authenticated HTTP
        |
        +-- terminal_reference
        +-- terminal_pwd
        +-- terminal_which
        +-- terminal_run(argv, cwd?, timeout?)
        +-- python_run(code, args?, cwd?, timeout?)
        +-- cpp_compile_run(code, args?, cwd?, timeout?, standard?)
        |
        +-- bounded named queue actions
                |
                v
          agent.sh -> mudl.py
```

## Canonical gateway

Use:

```text
One_Wave_Bench/bridges/hive-pipe/gateway.py
One_Wave_Bench/bridges/hive-pipe/terminal_parser.py
One_Wave_Bench/bridges/hive-pipe/install_gateway.sh
```

The gateway binds to `127.0.0.1:8765` and exposes MCP at `/mcp`.
Do not run the legacy `One_Wave_Bench/bridges/scripts/jetson_gateway.py` beside Hive Pipe; it uses the
same port. `One_Wave_Bench/bridges/scripts/install_jetson_gateway.sh` delegates to this installer.

## Install on the Jetson

```bash
cd "$HOME/One-Wave-Science"
bash One_Wave_Bench/bridges/hive-pipe/install_gateway.sh
```

This installs/restarts `hive-pipe-agent.service` and
`hive-pipe-gateway.service`, creates the external-work workspace, and creates
separate client tokens for:

```text
codex
claude
gemini
perplexity
```

Tokens live under `~/.config/hive-pipe/tokens/` and remain outside git.
Add another client with:

```bash
bash One_Wave_Bench/bridges/hive-pipe/create_client_token.sh CLIENT_NAME
```

## Authentication

The gateway accepts any configured client token through common MCP/API-key
forms:

```text
Authorization: Bearer <token>
Authorization: ApiKey <token>
X-API-Key: <token>
Api-Key: <token>
```

This makes clients such as Perplexity remote custom MCP connectors usable
without forcing one provider-specific header format.

## Terminal parser

Call `terminal_reference` first when an AI needs the parser workflow, current
authorized roots and limits, or a structured explanation of where path,
authentication, package, or human/root intervention is required.

`terminal_run` accepts a structured argv array. It also permits normal shell
wrappers such as:

```json
["bash", "-lc", "git status --short --branch"]
```

That compatibility matters for AI clients that routinely wrap terminal work in
`bash -lc`.

The result contains:

```text
stdout
stderr
exit_code
cwd
duration_ms
output_clipped
timed_out (when applicable)
```

Direct invocation of a small set of high-risk system programs remains blocked,
including privilege escalation, raw-device/formatting tools, mounting, and
power-control commands. Credential/private-key paths are also rejected. These
checks are secondary guardrails; the primary boundaries are authenticated
per-client tokens, normal non-root execution, `NoNewPrivileges`,
`ProtectSystem=strict`, and explicit writable directories.

Normal development commands, shell pipelines/wrappers, `git`, `python3`, test
runners, compilers, and project scripts are supported.


## Direct Python and C++

Authorized MCP clients can execute bounded source directly without a human
copying commands into the terminal. `python_run` executes temporary Python
source; `cpp_compile_run` compiles temporary C++ with `g++`, executes it, and
returns both compile and runtime receipts. Temporary files are removed after the
request. The tools use the same non-root service sandbox and authorized work
roots as `terminal_run`. See `One_Wave_Bench/bridges/docs/AI_CODE_BRIDGE.md`.

## Perplexity test

After installing the current gateway:

```bash
TOKEN="$(cat "$HOME/.config/hive-pipe/tokens/perplexity.token")"

curl -sS \
  -H "X-API-Key: $TOKEN" \
  -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"terminal_run","arguments":{"argv":["bash","-lc","printf PERPLEXITY_TERMINAL_OK"]}}}' \
  http://127.0.0.1:8765/mcp
```

Expected output contains `PERPLEXITY_TERMINAL_OK` and exit code `0`.

For a Perplexity remote custom connector use:

```text
URL: https://YOUR-TUNNEL/mcp
Transport: Streamable HTTP
Authentication: API Key
Key: contents of ~/.config/hive-pipe/tokens/perplexity.token
```

## Remote paths

Keep Hive Pipe bound to loopback and expose it only through the authenticated
reverse tunnel. The same parser is used by GitHub -> Jetson, direct HTTPS
clients, and connected MCP-capable AI clients. SSH remains the independent
recovery path.

## External drives

The default terminal roots are the canonical checkout and
`~/One-Wave-External-Work`. To authorize dedicated work directories on mounted
external drives, reinstall with an explicit colon-separated list:

```bash
HIVE_PIPE_ALLOWED_ROOTS="/home/Scales/One-Wave-Science:/mnt/lattice:/mnt/sandbox" \
  bash One_Wave_Bench/bridges/hive-pipe/install_gateway.sh
```

Only name the dedicated work directories, never a whole drive root. Each path
must already exist and be writable by `Scales`. The installer accepts roots
under the user's home, `/mnt`, `/media`, or `/run/media`; it refuses broad
system roots. The same list is enforced twice: by the terminal parser and by
the systemd `ReadWritePaths` sandbox. Raw-device, formatting, mounting, sudo,
and power commands remain blocked.

Use `inventory_block_devices` first to identify the two drives. Keep persistent
lattice work and disposable experiments in separate authorized directories.

## External work

See `One_Wave_Bench/bridges/external-work/External_Work/README.md` and `One_Wave_Bench/bridges/scripts/external_work_bridge.py` for the
bidirectional GitHub <-> Jetson-local external-work handoff.

## Full directions

See:

```text
One_Wave_Bench/bridges/docs/AI_JETSON_TOOL_GUIDE.md
One_Wave_Bench/bridges/docs/JETSON_AI_ACCESS.md
```


---

## SOURCE FILE: One_Wave_Bench/bridges/hive-pipe/TASK.md

# Hive Pipe v1 branch-step

- **MAIN GOAL:** provide a reliable, bounded route from a queued request to a
  Jetson terminal result.
- **CURRENT STEP:** implement and verify the local queue protocol.
- **HARD START:** verified One-Wave-Science repository; separate branch; clean
  starting state.
- **ALLOWED FILES:** `One_Wave_Bench/bridges/hive-pipe/**` only.
- **PROTECTED:** `One_Wave_Bench/Virtual_Breadboard/**`, Android/control files, external drives,
  mounts, partitions, filesystems, credentials, and user data.
- **ACTION:** accept only named read-only actions; produce deterministic JSON
  results; reject malformed or unknown jobs.
- **SUCCESS:** self-test passes; drive inventory runs without write operations;
  one job produces one result and one archived request.
- **HARD STOP:** stop after the local queue loop is proven. Remote transport is
  a separate branch-step.



---

## SOURCE FILE: One_Wave_Bench/Virtual_Breadboard/AI_COLLABORATION.md

# Virtual Breadboard — AI Collaboration Contract

This file is the handoff point for any AI or human joining Virtual Breadboard work.

The goal is not merely "a circuit simulator in a browser." The target is a real desktop laboratory and exploration environment where a person or AI can build circuits, test them against physical rules, automate experiments, operate virtual devices, and eventually compose those devices into larger virtual machines/worlds.

The simulator must remain reality-first. New features are not accepted merely because they look plausible or make a demo work. Every behavior belongs to an explicit layer, has a testable model, and must either pass measurement or report failure honestly.

## 1. Product direction

The long-term desktop app should provide four connected capabilities:

1. **Breadboard laboratory**
   - place real components and wires on one or more boards;
   - run DC, transient, AC, Bode, startup/UIC, controlled-source, semiconductor, magnetic, and measurement experiments;
   - probe voltages/currents and inspect convergence/failure truth;
   - compare ordinary reference circuits against ngspice where the models are intentionally equivalent.

2. **Tester and validation tool**
   - define a circuit or virtual device;
   - define inputs, stimuli, probes, expected ranges, assertions, and falsification conditions;
   - run repeatable tests instead of judging by appearance;
   - retain receipts/results so a later AI can reproduce what was proven.

3. **AI-assisted builder and solver**
   - AI may propose/build circuits from validated component definitions;
   - AI must consume the same solver and measurement truth as the human UI;
   - AI must not invent hidden behavior, magic components, or analysis shortcuts;
   - AI should be able to inspect a failed test, change one thing, rerun, and compare against the active goal.

4. **Programmable virtual-device / virtual-world layer**
   - circuits can become named virtual devices with declared terminals, controls, sensors, and tests;
   - safe deterministic programs can operate those devices (set a source, flip a switch, wait simulation time, sample a probe, assert a condition, loop over a sweep, etc.);
   - devices can later be composed into larger machines and environments;
   - this layer must use a constrained command language / API, not arbitrary renderer `eval` or unrestricted host-code execution;
   - the virtual world is built out of devices and measured state, not scripted outcomes.

## 2. What is authoritative today

Before changing code, read these files and treat them as baseline zero:

- `00_RULES/architecture.md` — ownership boundaries and work cycle.
- `03_ELECTRICAL_CORE/MAP.md` — solver/electrical-core truth.
- `SPICE_PARITY.md` — completed SPICE-parity roadmap and declared model limits.
- `SOLVER_CONVERGENCE.md` — convergence behavior and diagnostics.
- `11_INTERFACE/MAP.md` — human-facing interface map.
- `js/circuit.js` — load-bearing electrical truth.
- `js/app.js` — desktop/web renderer integration and current automation/debug hooks.
- `js/ai.js` — current AI circuit-build boundary.
- `AI_CONSTRUCTION_LOG.md` — signed Miniverse / Mega City construction ledger.
- `.github/workflows/breadboard-flashlight-tests.yml` — permanent qualification gate.

The completed SPICE-parity ladder covers the simulator core through ngspice cross-checks for model-equivalent reference cases. That does **not** mean every future device model is automatically equivalent to full commercial SPICE. When a model is intentionally simpler, state that explicitly.

## 3. Immediate product-completion work

The next acceptance layer is the **desktop application itself**. The app is not called 100% operational until all of these are continuously verified:

- Electron launches from the repo.
- A packaged desktop executable launches.
- board canvas, toolbox, inspector, oscilloscope, Save, Load, Export, and warnings/measurement UI are present.
- a real example circuit can be loaded or built, simulated, measured, saved, cleared, reloaded, and measured again with the same circuit state.
- packaging works for supported desktop targets.
- the Linux/Jetson path is explicit; do not imply ARM64 support if only x64 packages were built/tested.
- exported/shared builds reopen with the intended circuit state.
- app failures produce an actionable diagnostic instead of a silent broken window.

After that baseline is locked, build the programmable virtual-device layer described below.

## 4. Virtual-device contract

A virtual device should be a reusable object that wraps ordinary simulator elements instead of bypassing them.

Minimum device definition:

```json
{
  "name": "example-device",
  "version": 1,
  "circuit": { "layout": "1large", "parts": [] },
  "controls": [],
  "sensors": [],
  "programs": [],
  "tests": []
}
```

A control names a legal action on a declared part/property. A sensor names a measurable node/current/state. A test declares stimuli and assertions.

The first safe program instruction set should stay small and deterministic, for example:

- `set` — set an allowed device control to a validated value.
- `toggle` — toggle a declared switch/control.
- `run` — advance simulation time by a declared amount and timestep policy.
- `sample` — capture a declared sensor.
- `assert` — compare a captured/instant value against a range/tolerance.
- `sweep` — repeat a bounded set/run/sample sequence over declared values.
- `repeat` — bounded repetition only.
- `stop` — terminate the program with a result.

No arbitrary JavaScript, shell commands, filesystem access, network access, or Electron/Node access belongs in device programs. Host capabilities must remain explicit, narrow, and separately permissioned.

## 5. How another AI should contribute

### Default: one branch per coherent change

Create a branch from current `main` for one goal only.

Recommended naming:

- `vbb/<area>-<goal>`
- examples: `vbb/desktop-acceptance`, `vbb/device-program-runner`, `vbb/device-schema`, `vbb/arm64-package`, `vbb/scope-measurements`

Do not pile unrelated ideas into the same branch.

A branch should have:

- one clearly stated acceptance goal;
- smallest coherent code change;
- dedicated tests;
- all existing relevant tests still passing;
- no temporary patch scripts/workflows left in the final diff;
- a PR explaining what the change establishes and what it does **not** establish.

### Mandatory signed construction entry — Miniverse / Mega City

Any AI contributing to the Miniverse, Mega City, virtual-device, virtual-world, or related construction project must add or update an entry in `AI_CONSTRUCTION_LOG.md` on its branch before asking to merge.

Every entry must include:

- **AI name / identifier** — the model, agent, instance, or chosen project name that did the work;
- **date and time** — UTC ISO-8601 preferred;
- **branch and PR** — exact branch name and PR number/link when available;
- **project area** — Miniverse, Mega City, Virtual Breadboard, device runtime, world runtime, etc.;
- **work performed** — exact files/features/systems changed;
- **contribution / result** — what this work adds or proves;
- **intentions** — what the AI was trying to accomplish and why;
- **next intended work** — what the AI believes should happen next;
- **unfinished / uncertain** — anything incomplete, unverified, experimental, or still disputed;
- **dependencies** — other branches, APIs, models, files, or assumptions this work relies on;
- **conflicts / overlaps** — any known overlap with another AI's branch or proposal;
- **merge stance** — `AGREE TO MERGE`, `DO NOT MERGE YET`, `EXPERIMENT ONLY`, or `NEEDS JOINT REVIEW`, with a short reason;
- **reviewed collaborators** — names/identifiers of other AI contributors whose overlapping work was actually reviewed.

An anonymous contribution is incomplete. A branch with no signed construction entry is not ready to merge into the Miniverse / Mega City construction line.

The entry is not a vanity signature. It is a construction receipt so another AI can understand who changed what, why it exists, what was intended, and whether the contributor believes it is ready to combine with other work.

### Merge-agreement gate for separate AI work

When two or more AIs are working in parallel, their branches remain separate until the contributors explicitly agree on what should merge.

Passing tests is necessary but **not sufficient** for a parallel branch to merge.

Before any competing or overlapping AI branch is merged:

1. each AI identifies its branch/PR and states what it owns;
2. each AI has a current signed entry in `AI_CONSTRUCTION_LOG.md`;
3. each AI reviews the other relevant branch or proposal against the same acceptance goal;
4. conflicts, duplicated work, behavior differences, and architectural tradeoffs are written down;
5. the AIs agree on one of these outcomes:
   - merge one branch unchanged;
   - combine selected pieces into a new integration branch;
   - keep both branches experimental and merge neither yet;
   - reject one approach with the reason recorded;
6. each participating AI updates its **merge stance** in the construction log;
7. the agreed merge candidate is tested again after integration;
8. the PR records the agreement and names the branches/proposals considered.

**No AI may silently merge its own overlapping implementation over another AI's branch.**

If the AIs do not agree, the work stays isolated. A human owner can choose the direction, or the competing branches can be resolved by a predefined measurement/test that decides between them.

For non-overlapping branches, agreement is still required when their changes interact at an API/layer boundary. Independent work that truly does not touch or depend on the other branch may proceed normally, but the PR must say why it is independent.

### Alternative design: proposal file first

If two AIs want to explore different architectures, do **not** overwrite the same implementation back and forth.

Put proposals under:
`One_Wave_Bench/Virtual_Breadboard/proposals/`

Use files such as:

- `device-runtime-option-a.md`
- `device-runtime-option-b.md`
- `arm64-packaging-option-a.md`

Each proposal should state:

- target problem;
- owned layer/files;
- data/API shape;
- physics/reality boundary;
- security boundary;
- tests that would decide whether it is better;
- conflicts with current architecture;
- migration cost.

Only the selected design should then become production code.

### Experimental code that must not become product truth yet

Put experimental implementations in an isolated branch and, if useful, under an explicit experimental directory. Do not quietly route the production UI through an experimental model.

Experiments must say what they are testing and what result would falsify the idea.

## 6. File/layer ownership

Keep changes in the narrowest owner possible:

- electrical equations / stamping / device state: `js/circuit.js` and electrical-core tests.
- analysis/reporting: dedicated analysis modules (`spice-analysis.js`, `ac-analysis.js`, `bode-analysis.js`, etc.).
- board geometry/connectivity: board/connection layer.
- component definitions and physical options: `js/components.js`.
- renderer/workflow/UI: `js/app.js`, `index.html`, `style.css`.
- AI provider communication and validated AI build schema: `js/ai.js`.
- desktop host privileges / IPC / packaging bootstrap: `main.js`, `preload.js`, `package.json`.
- virtual-device schema/runtime: create dedicated modules; do not bury the runtime inside UI event handlers.
- tests: `test/`.
- permanent qualification: `.github/workflows/breadboard-flashlight-tests.yml`.

The UI owns no physics. AI owns no physics. A virtual-device program owns no physics. All of them invoke the same electrical core and measurement truth.

## 7. Required contribution loop

Use this loop for every branch:

1. Reference current `main` and this collaboration file.
2. State one acceptance goal.
3. Add/update the signed construction-log entry for the contributing AI.
4. Reproduce the current limitation/failure.
5. Change the smallest correct layer.
6. Test immediately.
7. Compare result with the active goal.
8. Check for drift from repo rules and adjacent features.
9. After three failed variations of the same approach, switch angle rather than repeating it.
10. Run the complete relevant regression/qualification chain.
11. Remove temporary delivery files.
12. Update the construction entry with actual result, unfinished work, and merge stance.
13. Open a PR with exact limits and evidence.
14. If another AI has overlapping or interacting work, complete the merge-agreement gate.
15. Merge only the agreed clean, green head.

## 8. What "100% operational" means here

"100% operational" is an acceptance statement for a declared release boundary, not a claim that the simulator models every circuit ever made.

For the desktop baseline it means:

- install/build succeeds on the declared platform;
- application launches;
- core UI is usable;
- circuit creation/loading works;
- simulation and measurements work;
- save/reopen works;
- export works;
- packaged executable works;
- permanent CI proves those paths alongside the solver qualifications;
- unsupported platforms/models/capabilities are stated rather than implied.

For the later virtual-device release it additionally means:

- device schema is versioned;
- deterministic device programs run safely;
- AI can create/modify device definitions through validated schemas;
- programs can operate devices and read sensors without arbitrary code execution;
- reusable device tests/receipts can be rerun by another AI or human;
- composition of multiple devices has explicit connection and scheduling rules.

## 9. Work that is welcome in parallel

Other AIs can safely take these as separate branches once they reference current `main`:

- desktop packaged-launch acceptance and save/reopen test;
- Linux ARM64 / Jetson packaging and launch verification;
- virtual-device JSON schema + validator;
- safe device-program interpreter;
- experiment/test definition format and receipt output;
- AI prompt/schema extension for generating device definitions and test programs;
- device library browser/import/export;
- multi-device connection graph and deterministic scheduler;
- richer measurements and test assertions;
- sandbox/permission review for any new host capability.

Do not duplicate an already-active branch unless you are intentionally proposing an alternative and label it as such. If parallel branches overlap, they must pass the merge-agreement gate before either enters `main`.

## 10. Non-negotiable drift guards

- Do not replace the simulator with a generic mockup.
- Do not rebuild the project from scratch to avoid understanding current architecture.
- Do not add hidden build-specific behavior to generic physics.
- Do not weaken a test solely because a new implementation fails it.
- Do not claim SPICE equivalence outside the models/cases actually cross-checked.
- Do not give AI or device programs arbitrary host-code execution just for convenience.
- Do not merge temporary patch workflows/scripts.
- Do not merge anonymous Miniverse / Mega City construction work with no signed construction-log entry.
- Do not merge overlapping AI work without explicit contributor agreement or a recorded human/test-based resolution.
- Do not call a feature complete until its actual user acceptance path is tested.

If in doubt: reference the repo again, identify the owning layer, make one change, and measure the result.


---

## SOURCE FILE: One_Wave_Bench/Virtual_Breadboard/BENCH_REALITY_CONTRACT.md

# Virtual Breadboard — Bench Reality Contract

## Status

**AUTHORITATIVE QUALIFICATION BOUNDARY FOR PHYSICAL-BENCH CLAIMS.**

A solver PASS means only that the equations for the supplied model solved and met that test's numeric thresholds. It does **not** automatically mean a breadboard build is physically valid.

A build may be called **BENCH-QUALIFIED** only when it also passes the bench-reality audit and uses the same source, reference, drive, current-limit, and return topology intended for the physical build.

---

## 1. Current CELL_V1 bench authority

For the present dual-rail bench:

```text
+12 V rail
   |
  10 k
   |
   +---------- local / gate experiment
   |
  solid 0 star ---------------- measure I_0 at controller end
   |
  10 k
   |
-12 V rail
```

Physical source architecture:

```text
+12 V  ---- positive supply
  0 V  ---- REAL midpoint / star conductor
-12 V  ---- negative supply
```

This is **not** a TLE2426 / rail-splitter topology.

Do not place `vgnd`, TLE2426, or another synthetic midpoint on top of the true dual-supply 0 V midpoint and call both of them CENTER.

---

## 2. Receipt that must work before gates

With equal 10 k arms:

```text
I_0 ~= 0
V(0_bus) ~= V(0_source)
```

Then deliberately change one side, e.g. 10 k -> 6.8 k:

```text
I_0 must become measurably nonzero.
```

Move the mismatch to the opposite arm:

```text
sign(I_0) must reverse.
```

The 0 rail itself must remain a low-impedance reference. A pretty midpoint voltage with no real DC 0 path is a failure.

---

## 3. CENTER / 0 spine rules

The 0 spine is a conductor/reference path.

Allowed for measurement:

- a wire;
- a deliberately small known shunt such as 0.1 ohm at the controller end;
- real lead/contact resistance explicitly modeled.

Not allowed in series with the 0 spine:

- capacitor;
- inductor used as the only DC path;
- current source;
- decorative RC network;
- toroid winding standing in for the reference conductor.

A series capacitor can make the far side *look* centered under symmetric loading while the DC reference is actually cut. The bench audit therefore rejects it even if the solved voltage is near zero.

---

## 4. Source-current truth

Every active build must have a source-current receipt.

If resistors, MOSFET channels, LEDs, coils, or other loads are dissipating power, a display showing the supply at `0.00 A` is not an acceptable result unless the solved source current is genuinely below the displayed resolution.

The present F0 bench limit is:

```text
|I_source| <= 20 mA
```

That is an **acceptance limit**, not the engine's historical global source limit.

Any simulation that requires more than the declared bench limit is physically unqualified even if the MNA solver can still produce a voltage solution.

---

## 5. MOSFET gate-drive truth

A MOSFET gate is controlled by **VGS**, not by the gate voltage printed relative to some unrelated ground.

For an N-MOS:

```text
VGS = Vgate - Vsource
```

A Nano GPIO that swings 0..5 V relative to supply 0 can directly command only a device whose source is referenced appropriately to that same 0 V domain.

It cannot directly turn on a 12 V high-side N-MOS after the source rises. The device becomes a source follower / turns back off as VGS collapses. A real high-side N-MOS requires a bootstrapped, isolated, or otherwise source-referenced gate driver.

For the present cell work:

- direct Nano drive is allowed only where the common-source node is physically 0-referenced and VGS is proven;
- a floating bilateral pair requires its own real source-referenced / isolated gate drive;
- an ideal floating test battery is a test fixture, not proof that the final controller can drive the pair.

---

## 6. Three logical Mirrors do not license a motor power stage

CELL_V1 and a BLDC inverter are separate machines until a coupling experiment explicitly proves otherwise.

CELL_V1 qualification must not silently include an H-bridge/three-half-bridge motor power stage and then count the result as proof of the cell.

For now:

```text
CELL_V1: G+ / G0 / G- experiments
MOTOR:   disconnected
```

Later motor work uses a separate ESC/proper three-half-bridge driver with its power return bonded to supply 0 at one star point. Motor stall current never returns through a TLE/synthetic midpoint or the cell's delicate I_0 receipt path.

---

## 7. Magnetic truth

Toroids, ferrite rings, inductors, or drawn loops are not evidence of magnetic hold.

A magnetic-memory claim requires a drive-off receipt that survives controls for:

- ordinary L/R inductive decay;
- capacitor/RC storage;
- diode/MOSFET reverse recovery;
- sensor offset and drift;
- instrument zero;
- thermal drift;
- remanence of the actual core material.

Until then, magnetic parts are **measurement experiments**, not passed cell functions.

---

## 8. Breadboard parasitics

Physical qualification models at least:

- supply/lead/contact resistance;
- real component tolerance;
- MOSFET model card and VGS reference;
- capacitor ESR/leakage;
- inductor/toroid winding resistance;
- source current budget;
- CENTER/0 shunt resistance where current is measured.

At motor-current scale a solderless breadboard is not an acceptable power bus. Motor-current qualification belongs on a proper driver/module/PCB with appropriate wiring and protection.

---

## 9. PASS language

Use these terms literally:

- **SOLVER PASS** — numerical circuit equations solved.
- **MODEL PASS** — expected behavior occurs in the modeled components.
- **BENCH-REALITY PASS** — supply/reference/drive/current/return constraints also match a plausible physical build.
- **PHYSICAL PASS** — measured on actual hardware.

Never promote one level into the next without the missing receipt.


---

## SOURCE FILE: One_Wave_Bench/Virtual_Breadboard/LOCK.md

# LOCK — the cell

Kitty Hawk / hive / slip-ship = GRAV play. Not this folder's job.

## Passed in software

| stamp | file | result |
|---|---|---|
| brain | HEX-SPLIT `brain_2state.py` | Field lists, Void cuts |
| nerve | HEX-SPLIT `nerve_cell.py` | one live winding, hold |
| 1 rails | `10_RECEIPTS/cell_v1_stamp1_rails.py` | I_0 0 / ±1.2 mA |
| 2 dummy | `10_RECEIPTS/cell_v1_stamp2_bridge.py` | STAY 0, +1 = +12 mA, −1 = −12 mA |

Ideal G. Ideal switches. That is the virtual lock for the *law*, not for body diodes or layout.

## Copper still owes

BUILD_25 steps 1–11 at 50 mA. Same numbers as stamp 1–2 on a DMM.

## Canonical read (stop hunting)

`ONE_WAVE_CELL.md`  
`DETAILED_BUILD.md`  
`BUILD_25.md`  
`FULL_BODY_ARCHITECTURE.md`  
`LOCKED_CELL_TOPOLOGY_DC_AC_MIRRORED_GATES.md`

Run:

```
python One_Wave_Bench/Virtual_Breadboard/10_RECEIPTS/cell_v1_stamp1_rails.py
python One_Wave_Bench/Virtual_Breadboard/10_RECEIPTS/cell_v1_stamp2_bridge.py
```


---

## SOURCE FILE: One_Wave_Bench/speculative/CELL_V1_ANTI_DRIFT.md

# CELL_V1 Anti-Drift Lock

**Read this before drawing, simulating, routing, fabricating, or describing CELL_V1.**

## 1. Primary primitive

CELL_V1 is one repeatable hex cell. Internal stateful elements, bidirectional switches, reference circuitry, sensing, motor/actuator interfaces, and reinjection hardware are **inside or attached to that primitive**. They do not replace the hex.

Every serious architecture description must preserve:

```text
ONE CELL_V1 HEX
 -> identical edge-to-edge neighbor
 -> path
 -> closed rotation
 -> seven-cell flower / larger field
 -> 3D volume
 -> resolved next-scale point
```

Current compact scale rule:

```text
Point -> Path -> Rotation -> Field -> Volume -> next-scale Point
```

## 2. Red-line geometry

```text
PORTS: FLAT SIDES / EDGES ONLY
CORNERS / VERTICES: NO PORTS

CLOCKWISE:
A+ -> B+ -> C+ -> A- -> B- -> C-

DIRECT OPPOSITES / PHYSICAL MIRRORS:
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

If a drawing moves a connection to a corner or changes the clockwise order, it is wrong.

## 3. Three-bidirectional-mirror physical lock

CELL_V1 has **three physical bidirectional mirrors**, not six separate one-way gates and not three Mirror gates followed by three separate Action gates.

```text
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

The same physical mirrors carry both directions:

```text
UP   = View / state / relation toward higher resolution
DOWN = Action / conditioning / Override toward lower/local state
```

Legacy notation such as `M1 -> A1 -> M2 -> A2 -> M3 -> A3` may survive only as logical/receipt notation. It must never be interpreted as six physical CELL_V1 gates.

## 4. Count separation

Keep these counts separate:

```text
PHYSICAL MIRRORS: 3 bidirectional A/B/C axes
DIRECTED HEX EDGES: 6 = A+ B+ C+ A- B- C-
ROUTE ADDRESS SPACE: 6 = 2 binary relations x 3 ternary moves
LOGICAL/RECEIPT POSITIONS: may use six labels but are not six physical gates
WINDING COUNT: experimental
MOSFET COUNT: implementation dependent
BRAIN / VOLUME LAYER COUNT: experimental
```

## 5. Processing-is-memory lock

The active path itself is intended to be the memory and the process:

```text
current physical state affects current flow
 -> flow changes that same physical state
 -> changed state remains locally available
 -> next traversal encounters the changed state
```

Do not draw a conventional `processor -> separate memory -> processor` as the CELL_V1 primitive.

A memristive, hysteretic magnetic, spintronic/magnetoresistive, phase-retaining, oscillatory, or other stateful device may be tested. No named device is automatically accepted.

**Failure test:** if the claimed memory can be removed from the active A/B/C processing path without changing the operation, it is not the required processing-memory implementation.

## 6. Repeated-path muscle-memory lock

The build must develop and test a physical muscle-memory analogue from **repeated use of the same paths**.

Target rule:

```text
successful path traversal
 -> same stateful path changes
 -> repeated traversal accumulates a bounded bias
 -> later traversal of that path becomes measurably easier / faster / more likely
```

The training must live in the physical path, not only in a software counter, log, lookup table, or external RAM.

A valid repeated-path effect must change at least one measured quantity such as:

- activation threshold;
- drive energy;
- settling/decision latency;
- retained conductance;
- magnetic or phase bias;
- route preference under the same differential;
- number of higher-level interventions needed for a repeated task.

The build must also test bounded correction:

```text
useful repetition -> reinforce path bias
strain / repeated error -> do not blindly reinforce
Override -> can redirect / weaken / reverse trained bias
inactivity -> persistence or decay must be measured
```

Do not call a permanent uncontrolled lock-in `muscle memory` just because repetition changed something.

## 7. Nerve-level energy and command lock

Current nerve-level roles:

```text
DC = power + controlled recovery + reinjection
AC = alternating / recurring path activity
TERNARY = DOWN / HOLD / UP local movement and motor/actuator command
QUADRATIC VIEWS UP = Direction / Phase / Strength / Reference
QUADRATIC ACTIONS DOWN = conditioning / corrective action / Override through the same mirrors
```

`V0` is the electrical reference. It is **not** the recovery reservoir and must not be used as a power dump.

Returned inductive/magnetic energy belongs in a measured DC-link/reinjection reservoir and is deliberately reused in a later permitted event.

## 8. Local automatic nerve recurrence

The current nerve target is local recurrence when conditions are healthy and escalation only when declared limits are crossed:

```text
within limits
 -> settle locally
 -> recover/reinject through DC loop
 -> reuse trained path when appropriate

strained / unresolved / unsafe
 -> Views UP
 -> higher resolution
 -> Action / Override DOWN through same mirrors
 -> resulting new local state remains
```

Resource/strain must be an explicit measured set of variables such as voltage margin, current, energy-reservoir state, temperature, unresolved phase, route conflict, or repeated failure. Do not hide the decision in an undefined scalar.

## 9. Ternary motor-control lock

Ternary is also the candidate local motor/actuator command grammar:

```text
DOWN = one commanded direction
HOLD = active balanced/rest state
UP   = opposite commanded direction
```

HOLD is not automatically power-off. Exact motor topology remains experimental.

A motor turning does not by itself prove the path memory, ternary architecture, or rotating-field claim; each requires its own measurements.

## 10. Bidirectional nerve-gate lock

Connection hardware must actually support the intended bidirectional path. A single MOSFET body diode must not silently defeat the blocked direction.

Back-to-back MOSFETs or another true bidirectional switch are candidates. SiC MOSFETs may be tested in later nerve/power domains where their speed, thermal, endurance, or power properties help, but direct millivolt/microvolt gate control is not assumed. Gate-drive circuitry must be explicit and measured.

The bidirectional switch is connection hardware unless experiment proves it also carries the retained processing state.

## 11. Seven-cell flower

- one center hex + six surrounding identical hexes;
- all seven use the same orientation;
- flat-edge to flat-edge connections only;
- shared edges mate the intended matching axis/opposed polarity;
- no adapter cell;
- every cell retains the same CELL_V1 internal architecture.

## 12. Scale recurrence

```text
ONE HEX
 -> PATH THROUGH IDENTICAL HEXES
 -> CLOSED ROTATION
 -> SEVEN-CELL / MULTI-CELL FIELD
 -> 3D VOLUME
 -> RESOLVED NEXT-SCALE POINT
```

Real-hardware improvements may change the **inside** of the hex. They may not silently delete the repeatable edge-connected cell.

## 13. Current physical package target

The preferred bench target contains:

- six canonical flat-edge directed interfaces;
- three physical bidirectional A/B/C mirrors;
- true bidirectional connection/switching where required;
- separately generated/measured electrical reference;
- active stateful processing-memory path;
- repeated-path training capability;
- voltage/current/state sensing;
- DC recovery/reinjection reservoir with energy accounting;
- optional magnetic/memristive/spintronic structures chosen only by measurement;
- test points adequate to distinguish state, path training, energy recovery, phase, and reference motion.

Electrical reference, retained state, learned path bias, and recoverable energy are different measured quantities even if the architecture couples them.

## 14. Scaling candidates — not yet canon

Keep these as explicit experiments:

```text
NERVE candidate:
2 flowers = normal + mirrored/inverted

M4 candidate:
2 + 2 flower/volume layers

HIGHER-BRAIN candidate:
3 / 3 / 3 volumetric expansion
and/or 3 x 3 x 3 proven lower-scale units

HEMISPHERE candidate:
resolved higher volume <-> mirror-flipped counterpart
```

Each extra layer must demonstrate a new measurable function. Numerical symmetry alone is not evidence.

## 15. Current authority order

Read these together, with earlier files interpreted through later corrections:

1. `One_Wave_Bench/speculative/CELL_V1_ANTI_DRIFT.md`
2. `UPDATED_63_CELL_V1_STATEFUL_MUSCLE_MEMORY_BUILD.md`
3. `One_Wave_Bench/speculative/CELL_V1_BUILD_PACKET.md`
4. `UPDATED_62_CELL_V1_HEX_FIRST_INTERNALS_AND_SCALING.md`
5. `UPDATED_61_CELL_V1_REAL_HARDWARE_GROUNDING.md`
6. `UPDATED_60_CELL_V1_HEX_EDGE_FLOWER_VOLUMETRIC_MEMORY_ARCHITECTURE.md`
7. `UPDATED_34_PROCESSING_IS_MEMORY_AND_CUBE_SCALE_ARCHITECTURE.md`
8. `UPDATED_33_INVARIANT_ENGINE_VTC_BUILD_AND_VIEW_ACTION_CORRECTION.md`
9. `One_Wave_Bench/speculative/Nodes/G-740_Field_Void_Ternary_and_Quadratic_Command_Routing.md`
10. `One_Wave_Bench/speculative/Nodes/G-741_Crazy_Town_Balanced_Rail_Nested_Loop_Build_Proposition.md`

If older wording conflicts with the three-bidirectional-mirror, processing-is-memory, or repeated-path muscle-memory locks above, the newer lock wins for CELL_V1 hardware.

## 16. Proven vs proposed

### Locked architecture

- one repeatable hex primitive;
- flat-edge interfaces only;
- clockwise order `A+ B+ C+ A- B- C-`;
- three opposed bidirectional A/B/C mirrors;
- Views UP and Actions DOWN use the same mirrors;
- processing and memory are co-located in the active stateful path;
- repeated-path physical training is required for the muscle-memory target;
- ternary DOWN/HOLD/UP is the local movement and candidate motor-control grammar;
- DC handles controlled nerve-level recovery/reinjection separately from V0;
- Point -> Path -> Rotation -> Field -> Volume -> next-scale Point recurrence.

### Experimental

- exact processing-memory device;
- exact reinforcement/decay law;
- useful retention/training margin;
- magnetic material/core geometry;
- winding count/ratios/polarity;
- final MOSFET topology;
- reinjection efficiency;
- stable path propagation;
- stable AC/rotation/RMF behaviour;
- exact motor implementation;
- vertical/depth coupling;
- two-flower nerve role;
- `2+2` M4 depth;
- `3/3/3` or `3 x 3 x 3` higher-brain grain;
- hemisphere mirror implementation.

## 17. Rejection rule

Reject and correct any design that:

- puts ports on hex corners;
- changes the canonical edge order;
- creates six separate physical Mirror/Action gates;
- gives UP Views and DOWN Actions separate physical mirror species;
- removes memory from the active path;
- stores muscle memory only in software bookkeeping;
- reinforces failed/strained paths without a correction mechanism;
- treats V0 as an energy reservoir;
- claims recovery without an energy budget;
- treats six edge interfaces as six windings;
- assumes an ordinary ferrite, memristor, MTJ, MOSFET, or SiC device automatically provides every required function;
- promotes `2 flowers`, `2+2`, `3/3/3`, or `3x3x3` to proven hardware without a measured function.

## 18. Diagram completeness test

A CELL_V1 build diagram is complete only if a reader can identify:

```text
1. six flat-edge directed interfaces;
2. three bidirectional A/B/C mirrors;
3. active stateful processing-memory path;
4. repeated-path training / muscle-memory mechanism under test;
5. Views UP and Actions DOWN through the same mirrors;
6. ternary DOWN/HOLD/UP local command;
7. DC recovery/reinjection separate from V0;
8. strain/escalation path;
9. identical-cell edge connection;
10. scale path into flower / field / volume.
```

If any of the first seven disappear, the design has drifted away from the current CELL_V1 build.


---

## SOURCE FILE: One_Wave_Bench/Virtual_Breadboard/00_RULES/architecture.md

# Virtual Breadboard — Canonical Layered Architecture

## Purpose

The Virtual Breadboard is a reusable simulation and measurement tool.

It is not a collection of project builds.

Flashlights, nerves, motors, cells, speakers, controllers, and other builds are things
that are put onto the breadboard and tested with it.

The breadboard itself provides:

- rules
- parts
- connectivity
- electrical physics
- time/transient behavior
- measurements
- reusable physical primitives
- magnetic behavior
- power behavior
- test infrastructure
- receipts

The system must be organized so one broken layer can be repaired without rebuilding
the entire simulator.

## Fundamental architecture

```
VIRTUAL_BREADBOARD/
│
├── 00_RULES/                 authority layer (this directory)
├── 01_PARTS/                 individual physical components
├── 02_CONNECTIONS/           topology: what's connected to what
├── 03_ELECTRICAL_CORE/       DC solving: given topology, what are V/I?
├── 04_TIME_AND_DYNAMICS/     transient/time-varying behavior
├── 05_MEASUREMENT/           observation, never mutation
├── 06_PRIMITIVES/            reusable arrangements built from lower layers
├── 07_MAGNETICS/             coupled coils, transformers, field behavior
├── 08_POWER/                 sources, batteries, energy accounting
├── 09_TESTS/                 tests mirror the architecture, one dir per layer
├── 10_RECEIPTS/              every test produces a receipt
└── 11_INTERFACE/             UI sits on top, owns no physics
```

External builds remain separate:

```
BUILDS/
├── flashlight/
├── nerve/
├── motor/
├── speaker/
├── cell/
└── ...
```

A build uses the breadboard. A build does not become part of the breadboard.

**Status note (see `../LAYER_MAP.md`):** this directory tree is the canonical target.
The current codebase (`js/circuit.js`, `simulate.js`, `js/app.js`, `js/board.js`,
`js/components.js`, `js/ai.js`) predates this canon and implements most of layers
01-08 as one coupled module rather than as physically separate directories. That is
a real, tracked architecture debt — see `../LAYER_MAP.md` for the file-by-file
mapping and `failure_rules.md` / this file's "No-rebuild protection" section for why
it is repaired incrementally, layer by layer, rather than rewritten in one pass.

## Core rules

**Rule 1 — Real behavior over desired behavior.** The simulator represents the
modeled physics. Never alter circuit behavior merely because a proposed build was
expected to work differently.

**Rule 2 — No total rebuild.** Working layers remain intact. A failure in one layer
does not authorize redesigning the rest of the simulator.

**Rule 3 — Layer ownership.** Every bug or update must first be assigned to one
responsible layer. Modify that layer only, unless an actual interface dependency
requires another change.

**Rule 4 — Preserve working behavior.** Anything already passing remains a permanent
regression requirement.

**Rule 5 — Failure is valid output.** The simulator must allow shorts, excessive
current, voltage sag, center movement, unstable oscillation, component overload,
MOSFET shoot-through, battery depletion, capacitor discharge, inductive flyback,
losses, and thermal rise where modeled. Do not silently correct bad circuits.

**Rule 6 — No unexplained magic primitives.** Higher-level behavior must be
constructed from lower-level physical capabilities.

**Rule 7 — Measurements determine PASS.** Visual appearance does not determine
success. Numerical measurements and declared tolerances determine PASS or FAIL.

**Rule 8 — Build definitions remain external.** A flashlight failure does not mean
"change the breadboard until the flashlight works." Determine whether (1) the
breadboard physics is wrong, (2) the build definition is wrong, or (3) the real
circuit simply does not perform as expected. Those are different outcomes.

(Full text and worked examples for each rule: see `physics_rules.md`,
`failure_rules.md`, `testing_rules.md`, `measurement_rules.md`, `interface_rules.md`.
Process rules — how a worker applies these day to day — are in `update_rules.md`.)

## Work cycle

Every update follows exactly this loop:

1. Observe failure
2. Identify responsible layer
3. Read that layer's rules
4. Reproduce failure
5. Make smallest coherent fix
6. Run layer tests
7. Run direct dependency regressions
8. Save receipt
9. Mark PASS or FAIL
10. Stop

Not: find bug → notice old architecture → clean everything up → rewrite simulator →
lose previous behavior.

## Status system

Every capability has only four valid states: **MISSING**, **IMPLEMENTING**,
**FAILING**, **PASSING**. Not "planned-ish," "mostly done," "architecture updated,"
"documented," "should work," or "probably fixed." Documentation is not
implementation.

## Permanent regression rule

The first time something passes: PASS → receipt saved → test becomes permanent.
Future work must keep it passing. That is how the breadboard accumulates capability
instead of relearning the same thing repeatedly.

## Build interaction rule

External builds submit: parts, parameters, connections, initial conditions, runtime,
requested measurements, pass criteria.

The breadboard returns: electrical state, time evolution, measurements, warnings,
failures, scope data, energy accounting, receipt.

The breadboard does not contain project intent. It does not know "this is a One-Wave
flashlight." It knows "9V source connected to these components in this topology with
these requested measurements." That separation must remain absolute.

## Worker ownership

For parallel work, divide workers like this:

- **Worker A** — Parts + component models
- **Worker B** — Connections + electrical solver
- **Worker C** — Time/transient dynamics
- **Worker D** — Measurement + scope + exports
- **Worker E** — Power + magnetics + advanced physical models
- **Integrator** — Interfaces between layers only, regression verification, no broad
  redesign

When one worker finds a problem owned by another layer: do not fix that other
layer's code casually. Create a failure receipt and hand it to the responsible
layer. Example: a measurement worker discovers voltage samples look wrong, checks
raw solver output, and finds the raw output is already wrong — the fix is a
receipt against the electrical-core layer, not a patch inside the scope math that
would hide the real bug.

## Integration contracts

Layers communicate through explicit contracts:

```
PARTS            → component equations/state
CONNECTIONS      → circuit topology
ELECTRICAL CORE  → solved electrical state
TIME             → state at t and t+Δt
MEASUREMENT      → observations
POWER/MAGNETICS  → specialized physical state
INTERFACE        → presentation
```

A layer may depend downward. It must not reach upward. A MOSFET model must never
ask "is this being used in the flashlight?"

## No-rebuild protection

A total rewrite is allowed only if ALL of these are true:

1. The current foundation is demonstrably incapable of supporting a required
   capability.
2. The problem cannot be isolated to a layer/interface.
3. Existing regression behavior has been captured.
4. The replacement can reproduce those regressions.
5. The reason is documented before work starts.

"Code is messy" is not sufficient. "I'd organize it differently" is not sufficient.
"A new project needs a feature" is not sufficient. Default action is: repair or
extend the responsible layer.

## First build order

**Stage 1** — 00 Rules, 01 Parts, 02 Connections, 03 Electrical Core, 05
Measurement, 09 Tests, 10 Receipts. Prove: DC source, resistor, series circuit,
parallel circuit, voltage divider, loaded midpoint, node voltage, differential
voltage, branch current, power.

**Stage 2** — Add 04 Time and Dynamics. Prove: capacitor, RC, inductor, LC/RLC,
switching.

**Stage 3** — Add 08 Power. Prove: source resistance, battery sag, capacity,
energy accounting.

**Stage 4** — Add 06 Primitives. Prove reusable: shared center, differential pair,
MOSFET switching stages, hysteresis, reinjection.

**Stage 5** — Add 07 Magnetics. Prove: one winding, coupled pair, three windings,
phase, measurable field behavior.

The interface can be improved alongside this work, but interface work may never
redefine physical results.

(See `../LAYER_MAP.md` for where the current codebase already sits against these
stages — short version: Stages 1-5's *capabilities* are already proven by the
existing test suites, but not yet organized into these physical directories.)

## Final development rule

The breadboard grows like this:

```
RULE → PART → CONNECTION → PHYSICS → TIME → MEASUREMENT → PRIMITIVE
     → SPECIALIZED PHYSICS → TEST → RECEIPT
```

Every repair goes back to the exact layer responsible for it. Never restart from
the top because something near the bottom changed. Never rebuild the whole
breadboard because one experiment exposed one missing capability. Locate the
layer. Fix the layer. Test the layer. Check its interfaces. Save the receipt.
Move forward.


---

## SOURCE FILE: One_Wave_Bench/Virtual_Breadboard/00_RULES/failure_rules.md

# Failure Rules

## Rule 5 — failure is valid output (full statement)

See `physics_rules.md` for the complete list of failure modes the simulator must
be able to genuinely produce. This file covers the *process* side: what to do
when you find one.

A failing test is data, not an emergency to paper over. When a check fails:

1. Do not weaken the tolerance to make it pass.
2. Do not delete or skip the check.
3. Do not "fix" it by changing an unrelated layer until it happens to pass.
4. Classify it (Type A-K, `update_rules.md`) and fix the actually-responsible
   layer, or determine the test's own expectation was wrong (Type J) and say so
   explicitly.

This session hit real examples of both: the LC/RLC ringdown test failing was a
real Type D/E problem (a `dt` floor in the electrical/dynamics stamping) and got
a real code fix; the RC filter phase-sign test failing was a Type J problem (the
test's own expected sign was backwards relative to `Sim.phaseDifferenceDeg`'s
already-established convention) and got the test corrected instead of the
physics.

## Rule 8 — build definitions remain external

A flashlight failure does not mean "change the breadboard until the flashlight
works." Determine whether:

1. the breadboard physics is wrong,
2. the build definition is wrong, or
3. the real circuit simply does not perform as expected.

Those are three different outcomes, with three different owners. Only outcome 1
is a breadboard-layer bug. Outcome 3 in particular is not a bug at all — it is
the simulator doing its job and telling you a design doesn't work, which per
Rule 1 is exactly what it should do.

## Bug triage table

See `update_rules.md` for the full Type A-K classification table used to route
every failure to its owning layer before any file gets touched.

## Never silently correct a bad circuit

If a circuit is genuinely unstable, ill-posed, or self-contradictory, the correct
outcome is that the solver fails to converge or reports the real pathological
values — not that it quietly produces a plausible-looking wrong answer. This
session's reinjection-primitive work found exactly this case: a first NMOS-based
high-side switch design created a genuine self-referencing Vgs feedback loop
(channel state affects Vgs, which affects channel state), and the fixed-point
solver correctly refused to converge on it rather than making something up. The
fix was to redesign the circuit (a PMOS with a fixed source reference), not toforce the solver to accept the unstable one.


---

## SOURCE FILE: One_Wave_Bench/Virtual_Breadboard/00_RULES/interface_rules.md

# Interface Rules

## The interface owns no physics

Layer 11 (`js/app.js`, `js/board.js`, `index.html`, `style.css`) sits on top. It
requests actions from lower layers and displays their outputs. It does not
compute electrical state itself.

- If a graph is wrong but the exported numbers are correct: fix the interface.
- If the solver numbers themselves are wrong: fix the responsible physics layer.
  Do not make the UI compensate for it.

## Rule 8, interface half

The interface is also where "is this the breadboard's fault or the build's
fault" (`failure_rules.md`) most often gets confused, because the UI is where a
user watches a build fail. A build-specific preset (a Cal board, a Stage-1
ternary cell, `experiments/brain_cell_001.json`) living in `js/app.js` or
`experiments/` is a *build*, per Rule 8 — even though today it's shipped in the
same repo as the breadboard engine, it is conceptually external, exactly like
`BUILDS/flashlight/` would be. See `../11_INTERFACE/MAP.md` and
`../BUILDS/MAP.md` for the current file-level boundary and where it's blurrier
than the canon wants.

## What already respects this boundary

- The oscilloscope (`js/app.js`'s scope rendering, `05_MEASUREMENT`'s scope/
  export capabilities in `simulate.js`) reads solved samples; it does not
  recompute or adjust them.
- `test/qualification.test.js`, `test/primitives.test.js`, and
  `test/regression-builds/` all talk to `js/circuit.js`/`simulate.js` directly,
  bypassing the board/hole-placement UI entirely — a deliberate choice recorded
  in each file's own header, precisely because what's being qualified is real
  component/primitive behavior, not routing wires through literal breadboard
  holes.

## What doesn't yet, cleanly

`js/app.js` (2400+ lines) currently mixes UI event handling with preset/build
definitions (the Cal boards, Stage 1 ternary preset) that the canon wants filed
under `BUILDS/`, not under the interface layer. This is recorded as a known gap
in `../11_INTERFACE/MAP.md`, not treated as blocking — per `architecture.md`'s
No-Rebuild Protection, splitting it out is a scoped, layer-by-layer job for
whoever owns Layer 11 next, not a reason to touch the physics layers today.


---

## SOURCE FILE: One_Wave_Bench/Virtual_Breadboard/00_RULES/measurement_rules.md

# Measurement Rules

## Rule 7 — Measurements determine PASS

Visual appearance does not determine success. Numerical measurements and declared
tolerances determine PASS or FAIL. Every test in this repo follows the pattern
`expected`, `actual`, `tolerance`, `PASS`/`FAIL` — printed, never eyeballed off a
plotted waveform.

## Measurement is separate from simulation behavior

Meters observe. Meters do not change the answer, unless the modeled meter
intentionally has real loading (e.g. a real finite scope-probe input impedance,
currently MISSING — see `../05_MEASUREMENT/MAP.md`). A measurement bug is a
Type F problem (`update_rules.md`): if the circuit's own solved state is already
wrong, the fix belongs to `03_ELECTRICAL_CORE` or `04_TIME_AND_DYNAMICS`, not to
the measurement code reading it.

## Required measurement capabilities

- node voltage
- differential voltage
- branch current
- source current
- instantaneous power
- average power
- integrated energy
- RMS voltage
- RMS current
- frequency
- phase difference
- duty cycle
- transient trace
- battery state
- temperature, where available

Every one of these is implemented today in `simulate.js` (`averageValue`,
`rmsValue`, `integrateEnergy`, `powerFromVI`, `findCrossings`, `findPeriod`,
`findFrequency`, `phaseDifferenceDeg`, `dutyCycle`) and cross-checked against
known synthetic signals in `test/circuit.test.js` Test 47 (T-MEASURE-PRIMITIVES).
See `../05_MEASUREMENT/MAP.md` for the exact function-to-capability mapping.

## Machine-readable export

Required by the canon; see `../05_MEASUREMENT/MAP.md` for what `simulate.js`'s
`snapshot()` already exports (voltages, currents, warnings, mosfet/core/
comparator/battery states) versus what's not yet wired to an export path.

## The floating-reference trap

A measurement-layer lesson worth keeping visible: a circuit with no real ground
anchor (no battery/wire forcing a reference) lets the solver's implicit zero
land on an arbitrary node. The fix is never to read one terminal's absolute
value in that situation — always read the real voltage *difference* across the
two terminals that actually matter. This bit three separate tests in this
session (a capacitor persistence check, an inductor flyback check, and several
AC-source-driven filter/rectifier/transformer builds) before the pattern was
written down here. It is not a solver bug — the solver is doing exactly what an
under-constrained linear system is supposed to do — it is a measurement-layer
discipline: know which node is your real reference before you trust an absolute
reading.


---

## SOURCE FILE: One_Wave_Bench/Virtual_Breadboard/00_RULES/physics_rules.md

# Physics Rules

## Rule 1 — Real behavior over desired behavior

The simulator represents the modeled physics. Never alter circuit behavior merely
because a proposed build was expected to work differently. If a build doesn't do
what its designer hoped, the question is always "is the physics right?", never
"how do I make the physics agree with the hope?"

This is the rule this session's own qualification work leaned on hardest: when the
LC/RLC ringdown test rang 3-300x too fast, the fix was to find and correct the real
bug (a `dt` floor silently clamping every reactive component's timestep), not to
adjust the test's expectation to match the wrong output.

## Rule 5 — Failure is valid output

The simulator must be able to genuinely produce, and never silently hide:

- shorts
- excessive current
- voltage sag
- center/reference movement
- unstable oscillation
- component overload
- MOSFET shoot-through
- battery depletion
- capacitor discharge
- inductive flyback
- resistive/dynamic losses
- thermal rise, where modeled

A circuit that *should* misbehave and doesn't is a bug, not a feature. Do not
silently correct bad circuits — see
`test/regression-builds/09_halfbridge_deadtime.js` for a build whose entire point
is that commanding both halves of a bridge on at once produces a real, large,
detectable shoot-through current, not a clamped or ignored one.

## Rule 6 — No unexplained magic primitives

Higher-level behavior must be constructed from lower-level physical capabilities.
A primitive (Layer 06) is a real arrangement of real parts with real wiring, not a
new hard-coded component that hands back a decision.

This codebase already enforces this the hard way: an earlier "Ternary Cell" macro
that internally hard-coded a Hold/Pos/Neg state machine was found and *removed*
(see git history, PR #15) specifically because it let the solver hand back a
decision instead of requiring the decision to be built from real comparator +
MOSFET + capacitor physics. `06_primitives`'s `ternary_resolved_state` and
`reinjection` mappings point at the real discrete-part circuits that replaced it.

## Real component behavior this simulator already models

(See `../LAYER_MAP.md` for exact file/function locations.) Real, non-ideal
behavior already present, not left as an idealization:

- Real forward voltage + dynamic on-resistance for diodes/LEDs (not a bare Vf).
- Real MOSFET Vth, RDS(on), gate capacitance (RC-limited switching, not an
  instant flip), body diode, and off-state leakage (GMIN-scale, not exactly zero).
- Real capacitor ESR + parallel leakage/self-discharge, keyed off a real
  electrolytic-vs-ceramic value threshold.
- Real inductor DC winding resistance (DCR).
- Real battery internal resistance, a hard current limit (brownout), and a
  Coulomb-counted capacity model with a flat-then-knee discharge curve (not a
  linear droop).
- Real comparator input offset voltage and propagation delay (a decision does not
  flip in zero time).
- Real per-color LED wall-plug efficiency for light output, not current-in-implies-
  brightness-out with no per-part distinction.

## What "real" does not mean here

This is an ordinary-electronics circuit simulator, not a finite-element field
solver. Where the canon asks for capability this codebase does not yet have
(temperature-dependent tempco beyond what's listed, arbitrary magnetic core
material parameterization, a field-vector Bx/By/Bz probe), that gap is recorded
as MISSING in `../LAYER_MAP.md`, not silently assumed.


---

## SOURCE FILE: One_Wave_Bench/Virtual_Breadboard/00_RULES/testing_rules.md

# Testing Rules

## Rule 4 — Preserve working behavior

Anything already passing remains a permanent regression requirement. The first
time a capability passes, it becomes permanent: PASS → receipt saved → test
becomes permanent. Future work must keep it passing.

Concretely in this repo: `test/circuit.test.js` (49 tests), `node
test/qualification.test.js` (80 checks: the 7-item first gate plus the remaining
fundamental-circuit tests), `test/primitives.test.js` (26 checks across the 10
reusable primitives), and `node test/run_regression_builds.js` (39 checks across
the 17 permanent regression builds) must all stay green. None of these get
weakened to make a new change pass — see Type J in `update_rules.md`'s bug-triage
table: if a test's *expected* value is itself wrong, that is a rules/test-layer
fix on its own, done explicitly, not a side effect of some other change.

## Tests mirror the architecture

```
09_TESTS/
├── rules/
├── parts/
├── connections/
├── electrical_core/
├── dynamics/
├── measurement/
├── primitives/
├── magnetics/
├── power/
└── integration/
```

Every layer owns its tests. Examples from the canon:

```
parts/resistor_ohms_law
parts/mosfet_low_side
connections/floating_node
connections/short_detection
electrical_core/series_resistors
electrical_core/parallel_resistors
dynamics/capacitor_charge
dynamics/inductor_ramp
measurement/differential_voltage
primitives/loaded_midpoint
primitives/hysteresis
magnetics/coupled_coils
power/battery_sag
```

See `../09_TESTS/MAP.md` for exactly which existing test (in which of the four
current test files) currently proves each of these — the physical test *files*
in this repo are not yet split one-per-layer-directory the way the canon
diagrams them, but every capability the canon lists is either already covered,
or explicitly marked MISSING there.

## No eyeballing

Every check prints expected/actual/tolerance and PASS/FAIL, and the process
exits non-zero on the first failure (`test/qualification.test.js`,
`test/primitives.test.js`) or after running everything and reporting a nonzero
failure count (`test/run_regression_builds.js`). A waveform is never "close
enough" by inspection — see `measurement_rules.md`, Rule 7.

## First build order maps to what's already proven

Per `architecture.md`'s Stage 1-5 order, this codebase's *capabilities* (not yet
its directory layout) already clear every stage:

- **Stage 1** (DC source, resistor, divider, loaded midpoint, node/differential
  voltage, branch current, power) — `qualification.test.js` items #1-#3, Gate 1/2.
- **Stage 2** (capacitor, RC, inductor, LC/RLC, switching) —
  `qualification.test.js` Gate 4, items #8/#9/#10.
- **Stage 3** (source resistance, battery sag, capacity, energy accounting) —
  `qualification.test.js` Gate 7, `primitives.test.js` Primitive 9.
- **Stage 4** (shared center, differential pair, MOSFET switching stages,
  hysteresis, reinjection) — `qualification.test.js` Gates 1-3/5/6,
  `primitives.test.js` Primitives 1/3/4/6.
- **Stage 5** (one winding, coupled pair, three windings, phase, measurable
  field behavior) — `qualification.test.js` items #19/#20, `primitives.test.js`
  Primitive 8. (Bx/By/Bz field-vector measurement specifically is MISSING — see
  `../07_MAGNETICS/MAP.md`.)


---

## SOURCE FILE: One_Wave_Bench/Virtual_Breadboard/00_RULES/update_rules.md

# Update Rules — how a change actually gets made

These are the process rules a worker (human or AI) follows when touching the
breadboard. `architecture.md` says what the layers are; this file says how you're
allowed to move between them while fixing something.

## Work division

Work must be divided by layer. A worker gets:

```
TARGET LAYER:
SPECIFIC FAILURE:
ALLOWED FILES:
DEPENDENCY TESTS:
PASS CONDITION:
STOP CONDITION:
```

Example assignment:

```
TARGET:        01_PARTS / MOSFET
PROBLEM:       low-side MOSFET current incorrect at specified Vgs
ALLOWED:       MOSFET model, MOSFET tests
DEPENDENCY TEST: basic DC solver
PASS:          measured current matches model tolerance
DO NOT TOUCH:  UI, battery, magnetics, reinjection, other primitives, build definitions
```

This prevents scope creep.

## Bug triage — classify before touching anything

Every failure must first be classified into exactly one type, and the fix goes to
that type's owning layer.

| Type | Problem class | Example | Fix in |
|---|---|---|---|
| A | Rule problem | Pass/fail definition is ambiguous | `00_RULES` |
| B | Part problem | Capacitor ESR is wrong | `01_PARTS` |
| C | Connectivity problem | Breadboard rows that should connect are treated as separate | `02_CONNECTIONS` |
| D | Solver problem | Parallel resistance gives wrong current | `03_ELECTRICAL_CORE` |
| E | Time problem | RC decay timing is wrong | `04_TIME_AND_DYNAMICS` |
| F | Measurement problem | Circuit calculation is correct but the differential meter gives an incorrect value | `05_MEASUREMENT` |
| G | Primitive problem | The hysteresis arrangement is wired incorrectly | `06_PRIMITIVES` |
| H | Magnetic problem | Mutual coupling is wrong | `07_MAGNETICS` |
| I | Power problem | Battery voltage does not sag under load | `08_POWER` |
| J | Test problem | Expected value in a regression is itself incorrect | `09_TESTS` (do not change working physics to satisfy a wrong test) |
| K | Interface problem | Oscilloscope draws the wrong scale but the underlying samples are correct | `11_INTERFACE` |

## Cross-layer change rule

Sometimes the actual problem genuinely crosses an interface. That does not permit
a general rebuild.

Example — allowed: a newly improved capacitor model requires the transient engine
to accept one new state value → touch `01_PARTS/capacitor` and
`04_TIME_AND_DYNAMICS/interface`.

Not allowed in the same change: rewrite the electrical solver, rewrite
measurement, rewrite the UI, rewrite primitives.

Every additional layer touched must have a stated reason.

## Change budget

Before editing, write:

```
PRIMARY LAYER:
SECONDARY LAYER IF REQUIRED:
WHY:
FILES EXPECTED TO CHANGE:
TESTS TO RUN:
```

If implementation suddenly needs five unrelated layers, **stop**. That usually
means the task has drifted or the architecture boundary itself is wrong — raise
it as a Type A (rule) problem rather than pushing the change through.

## Worker ownership handoff

When one worker finds a problem owned by another layer, they do not fix it
casually. They write a failure receipt (see `10_RECEIPTS/`) naming the layer,
expected value, actual value, and a reproduction, and hand it off. The owning
layer's work then follows this same cycle from step 1.
