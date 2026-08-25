# SM-004 — Five Field Lifecycle States

This node makes the established Field lifecycle explicit without changing it.

1. **Idle** — no committed action; stable/reference condition.
2. **Primed** — potential is loaded and conditions are ready, but action has not fired.
3. **Executing** — the selected action is actively being performed.
4. **Vectoring** — active motion/action is being steered, redirected, or oriented by feedback.
5. **Resolving** — the consequence is settling into a stable next state/reference.

Forward lifecycle:

`Idle -> Primed -> Executing -> Vectoring -> Resolving`

Step 6 evaluates Resolving:

- Hold: `Resolving -> Idle`
- Continue: `Resolving[n] -> Primed[n+1]`
- Break/Reroute: `Resolving -> shared (0) boundary -> reroute or terminate`

The lifecycle is not modulation `-2,-1,0,+1,+2`, not octave scale `Micro..Macro`, and not the six process steps.
