# Next Grok on this repo

This chat cannot SSH the Jetson. Hive Pipe Actions secrets were empty (run 36588943688).

Jetson user: Scales. Checkout: /home/Scales/One-Wave-Science.
If `git pull --ff-only` dies with diverging branches:

```bash
cd /home/Scales/One-Wave-Science
git fetch origin
git branch backup/jetson-$(date -u +%Y%m%dT%H%M%SZ)
git reset --hard origin/main
python3 Engine/parser2_goblins.py
```

Or after this file exists on the board: `bash scripts/jetson_sync_main.sh`

Grok CLI install (laptop or Jetson), key stays out of git:

```bash
curl -fsSL https://x.ai/cli/install.sh | bash
export XAI_API_KEY=   # console.x.ai, never commit
grok -p "Reply GROK BOT OK"
```

Science open: hex hold 0/5, ω_s from field, D-413 HTML still paints the well, Mass Effect blocked, T6 denied.
Parser-2: HOLD / RELAY / ACT. Brain Buddy wraps gemini_min only.
Do not merge Local Aid letters into this loop.
