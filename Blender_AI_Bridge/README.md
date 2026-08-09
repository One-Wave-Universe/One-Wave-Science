# Blender AI Bridge

Lets an AI (Claude, ChatGPT, or anything else that speaks MCP) inspect and
control an **open** Blender scene directly through Blender's Python API —
no GUI automation, no mouse/click simulation.

You open a `.blend` file (or load a reference PNG) yourself, then tell the
AI something high-level like *"get Goblin Raccoon ready for 3D
animation"*. The AI inspects the scene, models/rigs/animates through the
bridge, renders previews to check its own work, and saves versions.

## Architecture

```
 AI client (Claude / ChatGPT / any MCP host)
        │  MCP tools: get_scene_state, execute_command, execute_commands, ...
        ▼
 mcp_server/server.py   (runs as a normal Python process, OUTSIDE Blender)
        │  newline-delimited JSON over a local TCP socket
        ▼
 addon/  (installed and running INSIDE Blender)
        │  dispatcher.execute_command(...)  — runs on Blender's main thread
        ▼
 bpy / bmesh  (the actual scene)
```

Two independent pieces:

1. **`addon/`** — a Blender addon. It starts a small TCP server
   (`127.0.0.1:9876` by default) from a modal-timer operator, so incoming
   commands are always executed on Blender's main thread — required
   because `bpy` isn't safe to call from other threads. It exposes ~70
   commands (see `docs/COMMAND_REFERENCE.md`) covering scene inspection,
   object/mesh editing, rigging, animation, reference images, and
   camera/render.

2. **`mcp_server/`** — a standalone Python process (no `bpy` needed) that
   speaks MCP to the AI client and forwards each tool call to the addon's
   socket as one JSON command. It exposes a small, stable set of MCP
   tools — `get_scene_state`, `execute_command`, `execute_commands`,
   `list_commands`, transactions, save, and `render_preview` — rather than
   one MCP tool per Blender command, so the two sides don't have to be
   kept in lockstep. The AI discovers the full command surface at runtime
   via `list_commands`.

Everything is localhost-only. There's no auth on the socket because
nothing but your own MCP server is expected to reach it — don't expose
port 9876 beyond localhost.

## Setup

### 1. Install the addon in Blender

1. Zip the `addon/` folder (or point Blender at it directly via *Edit >
   Preferences > Add-ons > Install*, selecting `addon/__init__.py` — either
   works; zipping keeps the folder name stable).
2. Enable **"One-Wave AI Bridge"** in the add-ons list.
3. Open the 3D viewport sidebar (`N`), find the **AI Bridge** tab, and
   click **Start Server**. It stays running as long as Blender is open;
   restart it if you reload the file (`bpy` state resets on file load).

Host/port are configurable in the addon's preferences panel.

### 2. Run the MCP server

```bash
cd Blender_AI_Bridge/mcp_server
pip install -r requirements.txt
python3 server.py            # connects to 127.0.0.1:9876 by default
```

Point your MCP-capable client (Claude Desktop, an MCP-enabled ChatGPT
client, etc.) at it, e.g. in Claude Desktop's `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "blender-ai-bridge": {
      "command": "python3",
      "args": ["/absolute/path/to/Blender_AI_Bridge/mcp_server/server.py"]
    }
  }
}
```

### 3. Test on a simple object first

Before pointing the AI at a real character, sanity-check the round trip:

1. In Blender, open any file (even the default cube scene) and start the
   server.
2. From the AI client, call `get_scene_state` — you should see the
   default `Cube`, `Camera`, `Light`.
3. Call `execute_command("move_object", {"name": "Cube", "x": 2, "y": 0,
   "z": 0})` and confirm the cube visibly moves in the Blender viewport.
4. Call `execute_command("add_subdivision", {"object_name": "Cube",
   "levels": 2})`, then `render_preview` and confirm you get back an image
   of a subdivided cube.
5. Only once that loop works, load your reference image
   (`import_reference_image`) and start the real modeling/rigging work.

## Transactions

Blender's undo stack isn't reliably introspectable from Python across
versions, so `begin_transaction` / `commit_transaction` /
`rollback_transaction` are implemented as a `.blend` snapshot-and-reload
rather than counting undo steps. `rollback_transaction` does **not**
silently overwrite your real file on disk — it reloads the snapshot into
memory and returns `original_path` so you can explicitly
`save_blend_as(original_path)` if you want the rollback persisted.

## Units

Rotations in every command are **degrees** (converted to radians
internally) since that's what an LLM reasons about most reliably.
Locations/scale/dimensions are plain Blender units, passed straight
through.

## Limitations

- The bridge assumes an interactive, already-open Blender window (not
  `blender --background`) — several operators it wraps
  (`parent_set`, `mode_set`, render, etc.) need a real window/screen
  context.
- Only one MCP-server connection to Blender is expected at a time.
- `play_range` only sets the scene's frame range; real-time playback
  can't be driven synchronously over a request/response bridge — step
  through frames with `set_frame` + `render_preview` instead.

## Command reference

See `docs/COMMAND_REFERENCE.md` for the full list, or call the
`list_commands` MCP tool to get it live (with parameter names) from
whatever version of the addon is actually running.

## Tests

`tests/` covers the bpy-free parts (command dispatch/registry, the wire
framing, and the MCP bridge client against a fake socket server) since
`bpy` isn't installable outside Blender itself:

```bash
pip install pytest
pytest Blender_AI_Bridge/tests/
```

The `addon/commands/*.py` modules themselves can only be exercised inside
a real Blender process — verify those by hand using the "simple object"
smoke test above.
