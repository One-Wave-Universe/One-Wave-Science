# Brain Buddy

Local Qwen / human / OpenClaw writes a short question. Brain Buddy writes a bounded packet and runs the official Gemini CLI wrapper. Nobody pastes the repo.

Gemini credentials stay in the official CLI cache. Buddy never sees them. Do not put keys in this folder.

## Layout

```text
External_Work/brain_buddy/inbox/     drop query files here
External_Work/brain_buddy/outbox/    receipts + Gemini JSON
External_Work/brain_buddy/work/      last packet.md (gitignored contents ok)
scripts/brain_buddy.sh               entry
```

Inbox files are not required in git. The directories are kept by `.gitkeep`.

## Use on the Jetson

```bash
cd /home/Scales/One-Wave-Science
bash scripts/install_gemini_jetson.sh   # once
NO_BROWSER=true ~/.local/bin/gemini     # once, Google login

bash scripts/brain_buddy.sh ask "Does 2N+2m equal 2(N+m)? Answer only yes/no plus one line."
```

From a file (Qwen / OpenClaw writes this):

```bash
printf '%s\n' 'Review Engine/PROOFS_ALGEBRA.md Theorem 1 only.' \
  > External_Work/brain_buddy/inbox/q1.md
bash scripts/brain_buddy.sh review External_Work/brain_buddy/inbox/q1.md
```

Modes match `scripts/gemini_min.sh`: `ask` `review` `code` `deep`.
`deep` still needs `GEMINI_ALLOW_PRO=1`.
`code` still refuses `main` and a dirty tree.

## What Buddy does

1. Read the question (argv or inbox file).
2. Wrap it in `GEMINI_TASK_TEMPLATE.md` fields: goal, named files only, hard stop.
3. Write `External_Work/brain_buddy/work/packet.md`.
4. Exec `scripts/gemini_min.sh <mode> packet.md`.
5. Copy stdout to `outbox/<stamp>.json` (or `.txt` if CLI missing).

If `gemini` is not installed, Buddy still writes the packet and a HOLD receipt. That is session attachment, not a fake Gemini answer.

## Ban

No sudo. No secrets. No whole-repo dump. No merge. No T6. No calling Buddy output a bench result.
