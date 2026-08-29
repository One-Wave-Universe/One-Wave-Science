# Two-State Parser Apps

Editable Python desktop programs for testing two independent agents.

- `agent_a_app.py`: Agent A = Field + Void + its own subconscious loop.
- `agent_b_app.py`: Agent B = Field + Void + its own subconscious loop.
- `checkers_arena.py`: lets the two agents play repeated checkers games against each other.
- `shared_engine.py`: shared legal checkers mechanics plus the editable two-state parser rules.

Each agent has separate memory, subconscious ticks, move reinforcement, Field proposal, Void validation, Hold behavior, and consequence feedback.

Current variants:
- Agent A (`structure`) favors captures and central structure with a stricter Void threshold.
- Agent B (`novelty`) favors unseen positions and small exploratory noise with a slightly more permissive Void threshold.

Run with Python 3 + Tkinter:

```bash
python3 agent_a_app.py
python3 agent_b_app.py
python3 checkers_arena.py
```

The checkers rules engine supplies legal moves only; it does not supply strategy. All strategy is produced by each agent's Field/Void/subconscious rules.

First smoke test before repository upload: 50 games, alternating colors: Agent A 29 wins, Agent B 19 wins, 2 draws. This is only a baseline, not evidence of general intelligence.
