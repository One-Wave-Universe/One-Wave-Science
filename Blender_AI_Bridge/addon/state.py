import math

import bpy

from . import dispatcher


def _v3(v):
    return [round(v[0], 6), round(v[1], 6), round(v[2], 6)]


def serialize_modifier(mod):
    return {"name": mod.name, "type": mod.type, "show_viewport": mod.show_viewport}


def _in_view_layer(obj):
    return obj.name in bpy.context.view_layer.objects


def _visible(obj):
    return obj.visible_get() if _in_view_layer(obj) else not obj.hide_viewport


def _selected(obj):
    return obj.select_get() if _in_view_layer(obj) else False


def serialize_object(obj):
    armature_name = None
    if obj.type == "ARMATURE":
        armature_name = obj.name
    else:
        for mod in obj.modifiers:
            if mod.type == "ARMATURE" and mod.object is not None:
                armature_name = mod.object.name
                break
        if armature_name is None and obj.parent is not None and obj.parent.type == "ARMATURE":
            armature_name = obj.parent.name

    return {
        "name": obj.name,
        "type": obj.type,
        "location": _v3(obj.location),
        "rotation_euler_deg": [round(math.degrees(a), 3) for a in obj.rotation_euler],
        "scale": _v3(obj.scale),
        "dimensions": _v3(obj.dimensions),
        "parent": obj.parent.name if obj.parent else None,
        "collections": [c.name for c in obj.users_collection],
        "visible": _visible(obj),
        "selected": _selected(obj),
        "modifiers": [serialize_modifier(m) for m in obj.modifiers],
        "material_names": [s.material.name for s in obj.material_slots if s.material],
        "armature": armature_name,
    }


def serialize_camera(obj):
    cam = obj.data
    return {
        "name": obj.name,
        "location": _v3(obj.location),
        "rotation_euler_deg": [round(math.degrees(a), 3) for a in obj.rotation_euler],
        "lens_mm": cam.lens,
        "is_active": bpy.context.scene.camera == obj,
    }


def serialize_light(obj):
    light = obj.data
    return {
        "name": obj.name,
        "type": light.type,
        "location": _v3(obj.location),
        "energy": light.energy,
        "color": [round(c, 4) for c in light.color],
    }


def get_scene_state():
    scene = bpy.context.scene
    objects = [o for o in scene.objects]

    return {
        "file_path": bpy.data.filepath or None,
        "scene_name": scene.name,
        "frame_current": scene.frame_current,
        "frame_start": scene.frame_start,
        "frame_end": scene.frame_end,
        "objects": [serialize_object(o) for o in objects],
        "active_object": bpy.context.view_layer.objects.active.name
        if bpy.context.view_layer.objects.active
        else None,
        "selected_objects": [o.name for o in objects if _selected(o)],
        "collections": [c.name for c in bpy.data.collections],
        "cameras": [serialize_camera(o) for o in objects if o.type == "CAMERA"],
        "lights": [serialize_light(o) for o in objects if o.type == "LIGHT"],
    }


dispatcher.register("get_scene_state")(get_scene_state)
