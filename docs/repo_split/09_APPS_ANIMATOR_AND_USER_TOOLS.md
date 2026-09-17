# Apps, Animator, and User Tools

## Purpose
Keep runnable end-user applications and their UX/product requirements separate from the underlying theory and infrastructure.

## Belongs here
- Animator desktop editor requirements and acceptance path
- Scene, layer, playback, save/reopen, and export behavior
- User-facing control panels and prototype-builder interfaces
- Installers, launchers, packaging, and desktop shortcuts
- App-specific UI/UX requirements
- Motion libraries, assets, and editing workflows
- Universal AI access to the Animator through the same canonical project state used by the GUI
- Provider-neutral machine interfaces, command contracts, MCP/terminal adapters, and AI-access acceptance tests

## Animator hard gate
The Animator must remain usable by a human through the GUI and by any authorized AI through a deterministic machine interface.

The AI path must operate the same reel/project state and transaction/history model as the GUI. It may be reached through Jetson/Hive Pipe, terminal, MCP, HTTP/JSON-RPC, or provider adapters, but provider-specific private animation state, screen scraping, blind file rewriting, or approximate mouse automation do not satisfy the canonical access requirement.

See `Tools/Chats-Animator/AI_ACCESS_CONTRACT.md`.

## Rule
Infrastructure shared across apps belongs in document 08; simulator internals belong in document 05.
