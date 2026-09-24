# Code by Law Browser Extension

Code by Law sits between an AI chatbot and a GitHub project.

Its job is to keep project work on target:

1. Think Before You Speak
2. Parser Goblin
3. Reference GitHub Before Every Step
4. Cumulative Project Build + Checklist
5. Bouncer Goblin
6. Act
7. Checker Goblin
8. Journal Entry + Checkpoint
9. Re-reference GitHub

## GitHub is the external source of truth

The popup stores:

- GitHub repository URL
- active branch
- project build / journal reference-file paths
- current project context
- cumulative six-level project build
- local working journal/checkpoints for the governed chat

Before a governed turn, Code by Law reads the configured GitHub branch HEAD and configured project-build/journal files directly from GitHub and injects that reference into the chatbot.

Repository changes are performed through the chatbot's authorized GitHub access. Code by Law does not require a Jetson, terminal bridge, localhost companion, or phone-to-laptop relay.

## Six cumulative project levels

- Level 1 = 1
- Level 2 = 1 + 2
- Level 3 = 1 + 2 + 3
- Level 4 = 1 + 2 + 3 + 4
- Level 5 = 1 + 2 + 3 + 4 + 5
- Level 6 = 1 + 2 + 3 + 4 + 5 + 6

Every higher checklist carries the complete verified record of every earlier level. The Bouncer blocks advancement when a prior level is not verified.

## Supported chats

- ChatGPT
- Gemini
- Claude
- DeepSeek

## Firefox

The source is a Manifest V3 Firefox WebExtension with Firefox Android support declared in the manifest.

Mozilla web-ext lint result for the current build: 0 errors, 0 notices, 0 warnings.
