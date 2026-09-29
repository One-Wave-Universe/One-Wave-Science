# ChatGPT terminal bridge repair acceptance

The bridge bootstrap is considered repaired when all of the following are true:

1. The user's active `~/One-Wave-Science` checkout may be dirty or diverged from `origin/main`.
2. The bridge does not merge, reset, rebase, switch, or duplicate that checkout.
3. Git transport uses the same real checkout and its existing Git authentication.
4. Durable bridge state/results live only under `~/.local/state/one-wave-chatgpt-terminal/`.
5. Result publication may use a temporary detached worktree; it is removed after publication.
6. `one-wave-chatgpt-terminal-pull.service` is active.
7. A uniquely identified queued request produces a matching `.chatgpt-terminal/result.json`.
8. Subsequent ChatGPT requests can be sent without local terminal work.

## No permanent runtime clone

The former `~/.local/share/one-wave-chatgpt-terminal-runtime` clone is deprecated and is not used by the service. Keep it only until a matching live receipt proves the new single-checkout route; then it can be removed separately.
