"""MCP server that forwards tool calls to the Blender-side AI Bridge addon
over a local TCP socket. Run this outside Blender; it needs Blender open
with the addon's server started (View3D > Sidebar > AI Bridge > Start Server).
"""

import argparse
import os
from typing import Any, Dict, List, Optional

from mcp.server.mcpserver import Image, MCPServer

try:
    from .bridge_client import BridgeClient
except ImportError:
    # Allows `python3 server.py` (no parent package) in addition to
    # `python3 -m mcp_server.server`.
    from bridge_client import BridgeClient

mcp = MCPServer("blender-ai-bridge")
_client = BridgeClient()


def _call(command, **params):
    result = _client.execute_command(command, params)
    if not result.get("ok", False):
        raise RuntimeError(result.get("error") or f"{command} failed")
    return result["result"]


@mcp.tool()
def get_scene_state() -> dict:
    """Full JSON snapshot of the open Blender scene: every object with its
    transform, dimensions, parent, collections, modifiers, materials and
    armature link; active/selected objects; cameras; lights; collections;
    frame range; and the current .blend file path. Call this first, and
    again after any edit whose exact result you need to confirm."""
    return _call("get_scene_state")


@mcp.tool()
def list_commands() -> dict:
    """List every low-level command execute_command can run, with its
    parameters. Call this once at the start of a session to see the full
    surface (primitives, transforms, modifiers, bmesh edits, armature/bone/
    constraint/weight commands, keyframe/action commands, reference-image
    commands, camera/light/render commands, undo/redo/save/transactions)."""
    return _call("list_commands")


@mcp.tool()
def execute_command(command: str, params: Optional[Dict[str, Any]] = None) -> dict:
    """Run one named Blender command (see list_commands for the full list
    and its parameters) against the open scene. Returns
    {"ok", "command", "result", "error"}."""
    return _client.execute_command(command, params or {})


@mcp.tool()
def execute_commands(
    commands: List[Dict[str, Any]], stop_on_error: bool = False
) -> dict:
    """Run a batch of {"command": str, "params": dict} entries in one round
    trip instead of one call per step - use this for multi-step edits like
    building out a character's mesh or rig. Returns {"ok", "results": [...]}
    with one result per entry, in order."""
    return _client.execute_commands(commands, stop_on_error=stop_on_error)


@mcp.tool()
def begin_transaction() -> dict:
    """Snapshot the current scene before a risky multi-step edit. Follow up
    with commit_transaction to keep the result, or rollback_transaction to
    undo everything back to this point."""
    return _call("begin_transaction")


@mcp.tool()
def commit_transaction(transaction_id: Optional[str] = None) -> dict:
    """Discard the begin_transaction snapshot, keeping the current state."""
    return _call("commit_transaction", transaction_id=transaction_id)


@mcp.tool()
def rollback_transaction(transaction_id: Optional[str] = None) -> dict:
    """Restore the scene to how it was when begin_transaction was called.
    Does not overwrite the real .blend file on disk - call save_blend_as
    with the returned original_path afterward if you want that persisted."""
    return _call("rollback_transaction", transaction_id=transaction_id)


@mcp.tool()
def save_blend() -> dict:
    """Save the current .blend file in place. Fails if it has never been
    saved - use save_blend_as first."""
    return _call("save_blend")


@mcp.tool()
def save_blend_as(path: str) -> dict:
    """Save the current scene as a new/versioned .blend file at `path` (use
    this to check in progress versions, e.g. goblin_raccoon_v2.blend)."""
    return _call("save_blend_as", path=path)


@mcp.tool()
def render_preview(width: int = 640, height: int = 480, samples: Optional[int] = None) -> Image:
    """Render the current active camera view and return it as an image, so
    you can visually check whether the model, rig, or pose looks correct
    against the reference."""
    result = _call("render_preview", resolution=[width, height], samples=samples)
    with open(result["path"], "rb") as f:
        data = f.read()
    return Image(data=data, format="png")


def main():
    parser = argparse.ArgumentParser(description="One-Wave AI Bridge MCP server")
    parser.add_argument("--host", default=os.environ.get("AI_BRIDGE_HOST", "127.0.0.1"))
    parser.add_argument(
        "--port", type=int, default=int(os.environ.get("AI_BRIDGE_PORT", "9876"))
    )
    args = parser.parse_args()
    _client.host = args.host
    _client.port = args.port
    mcp.run()


if __name__ == "__main__":
    main()
