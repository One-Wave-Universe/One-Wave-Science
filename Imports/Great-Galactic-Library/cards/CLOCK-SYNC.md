# CARD: CLOCK-SYNC

- **id:** GGL-009
- **repo:** https://github.com/One-Wave-Universe/HEX-SPLIT (SYNC.md, clock_sync.py)
- **layer:** pipeline
- **one sentence:** one-wave-clock/1 — stamp propose/commit/hold/quit; followers lock, hold, snap, or quit; no chromatic slew.
- **may touch:** HEX-SPLIT clock.json, BUCKET bars, MOSFET write, GRAV hallway freeze
- **may not touch:** GPU/Field packets as commit, advancing phase on hold, Gate-7 as a noun
- **falsifier:** phase moves when polarity is 0, or a follower catches up by walking +1
- **gate:** YELLOW
- **last kick:** 2026-09-12
