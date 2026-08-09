import os
import sys

# dispatcher.py and framing.py have no bpy dependency and no relative
# imports, so they can be loaded as standalone modules (bypassing
# addon/__init__.py, which does `import bpy` and would fail outside
# Blender) by putting the addon/ directory on sys.path directly.
_ADDON_DIR = os.path.join(os.path.dirname(__file__), "..", "addon")
sys.path.insert(0, os.path.abspath(_ADDON_DIR))

# mcp_server/ has no bpy dependency at the package level (bridge_client.py
# is pure stdlib), so it's importable as a normal package.
_ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.abspath(_ROOT_DIR))
