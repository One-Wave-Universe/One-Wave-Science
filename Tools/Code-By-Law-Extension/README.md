# Code by Law Browser Extension

Code by Law governs AI project work through Think Before You Speak, Parser Goblin, Reference Every Step, one Project Build Step + Checklist at a time, Bouncer Goblin enforcement, independent checking, journal entries, checkpoints, and re-reference.

## Current layer

This layer intentionally includes only:

- Code by Law browser-extension shell;
- built-in default rules;
- editable custom rules stored in browser storage;
- add/edit/disable/delete/import/export rule management;
- current project-context field;
- rule-packet injection into supported chat editors.

It does not yet connect directly to GitHub, Hive Pipe, Jetson, OpenClaw, or checkpoint storage. Those are separate future layers.

## Supported chat sites

- ChatGPT
- Gemini
- Claude
- DeepSeek

## Add rules

Open the extension options page.

Custom rules are saved separately from built-in defaults. A custom rule with the same ID as a default overrides that default. New IDs add new rules.

The next governed turn uses the updated rules without changing extension code.

## Layer 1 success condition

The extension source must parse, the manifest/default rules must be valid JSON, custom rule management must be isolated from prompt injection, and the extension must remain a thin governance layer rather than a new terminal bridge.


## Six nested project levels

Code by Law uses the same checklist recursively at six scales:

1. **Action** — smallest bounded change.
2. **Step** — contains verified actions.
3. **Layer** — contains verified steps for one editable responsibility.
4. **Build Phase** — contains verified layers for one coherent integration phase.
5. **Project State** — contains verified phases that produce a usable state or release candidate.
6. **Project Loop** — contains the verified project state and controls completion, reentry, or expansion.

Each level is cumulative, not merely parent-child:

- Level 1 = 1
- Level 2 = 1 + 2
- Level 3 = 1 + 2 + 3
- Level 4 = 1 + 2 + 3 + 4
- Level 5 = 1 + 2 + 3 + 4 + 5
- Level 6 = 1 + 2 + 3 + 4 + 5 + 6

Every higher checklist carries forward the complete verified record of all previous steps.

## Companion URL

The popup stores the Code by Law companion base URL in extension storage. Default: http://127.0.0.1:8766.

Change this field to point the same extension at an authorized localhost companion, Jetson tunnel, or later bridge without editing extension source.
