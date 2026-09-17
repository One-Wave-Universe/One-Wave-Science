# ChatGPT terminal bridge repair acceptance

The bridge bootstrap is considered repaired when all of the following are true:

1. The user's active `~/One-Wave-Science` checkout may be diverged from `origin/main`.
2. Running the fetch-only bootstrap does not merge, reset, rebase, or switch that checkout.
3. Bridge code runs from `~/.local/share/one-wave-chatgpt-terminal-runtime` at `origin/main`.
4. `one-wave-chatgpt-terminal-pull.service` is active as a user service.
5. The queued `printer-diagnostic-001` request on `chatgpt-terminal` produces `.chatgpt-terminal/result.json`.
6. Subsequent ChatGPT requests can be sent by updating `.chatgpt-terminal/request.json` without local terminal work.
