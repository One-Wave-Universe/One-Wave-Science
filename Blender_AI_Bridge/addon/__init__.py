bl_info = {
    "name": "One-Wave AI Bridge",
    "author": "One-Wave Science",
    "version": (0, 1, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > AI Bridge",
    "description": (
        "Local socket bridge exposing scene inspection and editing commands "
        "for AI-driven control of the open Blender scene."
    ),
    "category": "Interface",
}

import bpy

from . import dispatcher, state  # noqa: F401 - state registers get_scene_state on import
from . import commands  # noqa: F401 - importing registers every command module
from . import server


class AIBridgePreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    host: bpy.props.StringProperty(name="Host", default=server.HOST)
    port: bpy.props.IntProperty(name="Port", default=server.DEFAULT_PORT, min=1024, max=65535)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "host")
        layout.prop(self, "port")


class AIBRIDGE_PT_panel(bpy.types.Panel):
    bl_label = "AI Bridge"
    bl_idname = "AIBRIDGE_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AI Bridge"

    def draw(self, context):
        layout = self.layout
        srv = server.get_server()
        prefs = context.preferences.addons[__package__].preferences
        layout.label(text=f"Status: {'Running' if srv.running else 'Stopped'}")
        layout.label(text=f"{prefs.host}:{prefs.port}")
        if srv.running:
            layout.operator("aibridge.stop_server", text="Stop Server")
        else:
            layout.operator("aibridge.start_server", text="Start Server")
        layout.separator()
        layout.label(text=f"{len(dispatcher.command_names())} commands registered")


CLASSES = (AIBridgePreferences, AIBRIDGE_PT_panel)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    server.register()


def unregister():
    server.unregister()
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
