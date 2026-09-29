# Parser-2 + loop goblins

Two states only: **HOLD** and **GO**.

Dead band: no `text` or no `intention` or no `consequence` → HOLD.
That is the same Reference Goblin rule Hive Pipe uses on `terminal_run`.

## Who does what

| Goblin | When | May |
|---|---|---|
| HOLD | incomplete packet or bad role | refuse, name the missing field |
| RELAY | GO + role RELAY | write `External_Work/brain_buddy/inbox/relay.md` only |
| ACT | GO + role ACT | run a named wrapper (`Engine/prove_one_wave.py`, later `brain_buddy.sh` on Jetson) |

RELAY never shells. ACT never invents a wrapper. Gemini stays behind `brain_buddy.sh` / `gemini_min.sh` on the board.

```bash
cd /home/Scales/One-Wave-Science
python3 Engine/parser2_goblins.py
```

Jetson terminal from this Grok session: GitHub Actions `jetson-command.yml` (Hive Pipe). Direct SSH is not attached here.
