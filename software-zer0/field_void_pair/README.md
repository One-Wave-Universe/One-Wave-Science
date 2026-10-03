# Field/Void Pair — two AIs, one repo lens, Algorythm-Zer0 referee

SOFTWARE ONLY. This routes, compares and rebases numbers (`software-zer0/SEPARATE.md`).
It makes no claim about the cell, the core, or physical memory.

## What it does

Two AIs work in a loop. Each one is held to the One-Wave repository:

| Role | Job (from `AGENTS.md`, `UPDATED_34` §3, `G-740`) |
|---|---|
| **Field** | expressive side: proposes one bounded step and must cite repo paths |
| **Void** | oversight/override side: returns `ALLOW · CORRECT · OVERRIDE · HOLD · ESCALATE` plus a reference score and a goal score |

Both AIs get the same **repo lens**, which is the shared reference (0):

1. **CANON**: `CLAUDE.md`, `AGENTS.md`, `GENERAL_REFERENCE_RULES.md`, `AI_CANONICAL_START_HERE.md`,
   UPDATED_34 Field/Void, G-740, `proofs/ZER0_FIRST_CYCLE.md`, the Zer0 harness, `SEPARATE.md`, and the terminology legend.
2. **MAP**: every tracked file in the repo, grouped by directory.
3. **FOCUS**: tf-idf retrieval over every tracked text file, run again each turn from the goal and Void's last note.

The lens reads a checkout when there is one. Otherwise it reads the bundled snapshot, which holds the same files.

**Algorythm-Zer0 decides each turn.** The loop imports `simulations/zer0_first_cycle.py` directly; it does not copy it.

```text
X = grounding   deterministic: share of cited paths that really exist in the repo
Y = reference   mean of Void verdict value and Void reference score
Z = goal        Void goal score
T = timing      turn / max_turns   (closure only, does not vote)

shared_event(r, X/Y/Z/T) -> two-of-three resolve -> bounded rebase of r
   +  proposal becomes the confirmed reference state
   -  Void's note goes back to Field as an override
   0  HOLD (a split vote is HOLD, not a hidden arbiter)
```

Each branch is classified against the moving zero `r`, so the bar rises after every
confirmation. To be confirmed again, the next proposal has to beat the new reference.

The loop stops on any of these (`AGENTS.md`):
- `ESCALATE` verdict
- `THREE_STRIKES`: three denials in a row
- `SETTLED`: two HOLDs in a row
- `HARD_STOP`: the turn limit is reached
- `PROVIDER_ERROR`: a model call failed. The error is reported, not hidden.

If Void's reply can't be parsed, it reads as HOLD with scores of 0, never as a pass.

## Download with a desktop icon

There's one file to download: `fvpair-installer.sh` (about 7 MB). Build it with
`./software-zer0/field_void_pair/build_installer.sh`, which writes `dist/fvpair-installer.sh`.

```bash
bash fvpair-installer.sh                       # uses the snapshot inside the installer
bash fvpair-installer.sh --repo ~/code/One-Wave-Science   # or read a checkout you already have
```

**It never clones the repo.** The installer carries a compressed text snapshot of the whole repo,
`lens_bundle.tar.xz`: every tracked text file plus the full file list, about 5 MB. The program reads
that snapshot in memory and never unpacks it. If a checkout is already on the machine, the
installer uses it instead and deletes the snapshot.

- Space needed: about 5.2 MB after install. The installer checks for 8 MB free first and stops,
  writing nothing, if there isn't enough. Delete `fvpair-installer.sh` after installing to get its 7 MB back.
- It needs `python3`, and no sudo or git.
- It puts a **Field/Void Pair** icon on the desktop and adds an app-menu entry.
- It adds the `fvpair` and `fvpair-launch` commands to `~/.local/bin`.
- It writes `~/.config/fvpair/env` (chmod 600) for your API keys, and the repo path if you used `--repo`.
  Desktop launches don't see your shell's environment, so put your keys in this file.

The snapshot is fixed at build time. Its commit is shown in the app's reference line,
labeled `bundle:`. Rebuild the installer to pick up newer repo content.

Double-click the icon to start the app in the background and open your browser.
To stop it, right-click the icon and choose **Stop Field/Void Pair**.
On GNOME, if the icon does nothing, right-click it and choose **Allow Launching**.
To remove everything except your key file, run `~/.local/share/fvpair/app/install_linux.sh --uninstall`.

If you already have the repo checked out, `./software-zer0/field_void_pair/install_linux.sh`
installs the same way straight from the checkout.

## Linux program

```bash
fvpair providers                                     # which keys are set
fvpair run "your goal" --field anthropic --void deepseek --turns 8
fvpair run "your goal" --field anthropic:claude-opus-5-5 --void gemini:gemini-2.5-flash
fvpair lens "query"                                  # print exactly what both AIs see
```

Without installing: `python3 software-zer0/field_void_pair/cli.py ...`

Each run writes a JSONL ledger with every turn, the Zer0 trits, `r`, and a
Reference Point Zero snapshot (root, branch, HEAD, dirty). The default location is
`~/.local/share/fvpair/runs/`; use `--out` to choose another.

## App version

```bash
fvpair serve            # opens http://127.0.0.1:8742/
```

The app shows Field and Void side by side, the X/Y/Z trits for each turn, the resolved
move, and a chart of the moving reference `r`. You can halt a run and download its ledger.
The app runs on the same core as the CLI; the browser only displays it.
By default the server binds to localhost only.

## Providers

| name | key (environment only) | default model |
|---|---|---|
| `offline` | none (deterministic stand-in, not an AI) | `offline-zer0` |
| `anthropic` | `ANTHROPIC_API_KEY`; needs `pip install anthropic` | `claude-opus-5-5` |
| `deepseek` | `DEEPSEEK_API_KEY` | `deepseek-chat` |
| `openai` | `OPENAI_API_KEY` | `gpt-4o-mini` |
| `ollama` | none, local server | `llama3.1` |
| `gemini` | `GEMINI_API_KEY` | `gemini-2.5-flash` |

To change an endpoint, set `FVPAIR_<NAME>_BASE_URL`. To change Claude's effort level,
set `FVPAIR_EFFORT` (default `medium`). Keys are never sent to the page, the ledger, or the logs.

## Tests

```bash
python3 -m unittest software-zer0/field_void_pair/test_field_void_pair.py
```

These tests are deterministic and need no keys. They cover the lens, the citation check,
Void parsing, the loop (confirm, three strikes, split-vote HOLD, escalate, provider error),
key hygiene, and the app server endpoints.

## Limits

- The lens is text retrieval, not understanding. A model can still cite a real file and misread it;
  Void and the X branch catch only some of that.
- Void's scores are a model's judgment. Only X is deterministic.
- Neither AI edits files or runs commands. The loop produces a confirmed proposal plus a ledger, not a commit.
- The weights (`DEAD`, `ALPHA`, verdict values) are working calibration, not measured constants.
