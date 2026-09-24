# One Wave Bridges

Canonical home for AI, Jetson, terminal, Hive Pipe, local relay, external-work, Gemini, and open-data bridge infrastructure.

## Layout

- docs/ — operator instructions and bridge/reference guides.
- hive-pipe/ — canonical Hive Pipe gateway, parser, pull bridge, DeepSeek adapters, tests, and doctor.
- scripts/ — Jetson/Gemini/install/remote bridge utilities.
- local/ — local-machine bridge and repo-sync tooling.
- integrations/ — bridge adapters embedded in other project surfaces.
- external-work/ — inbox/outbox relay workspace.
- open-data/ — external scientific-data ingestion and wave-transform helpers.

GitHub Actions remain under .github/workflows/ because GitHub only discovers workflows there. Those workflows point into this canonical bridge tree.
