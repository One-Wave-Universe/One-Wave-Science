# ChatGPT Jetson relay

This is an independent recovery path. It does not depend on the Jetson-side
`one-wave-chatgpt-terminal-pull.service`.

Flow:

```text
chatgpt-terminal request
        |
        v
GitHub Actions scheduled relay
        |
        v
authenticated Hive Pipe HTTPS /mcp
        |
        v
Jetson terminal_run
        |
        v
chatgpt-terminal result
```

The relay is event/dispatch driven only. There is no polling timer or scheduled wake-up. It uses
the existing `JETSON_GATEWAY_URL` and `JETSON_GATEWAY_TOKEN` repository
secrets and preserves the terminal parser's intention/consequence gate.

This is transport redundancy only. It does not replace or modify Brain Buddy.
