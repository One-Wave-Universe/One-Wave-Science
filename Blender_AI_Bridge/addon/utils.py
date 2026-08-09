import contextlib
import math

import bpy


def to_radians3(xyz):
    return tuple(math.radians(v) for v in xyz)


def to_degrees3(xyz):
    return tuple(math.degrees(v) for v in xyz)


def get_object(name):
    obj = bpy.data.objects.get(name)
    if obj is None:
        raise CommandError(f"object not found: {name}")
    return obj


def get_collection(name):
    coll = bpy.data.collections.get(name)
    if coll is None:
        raise CommandError(f"collection not found: {name}")
    return coll


def get_armature(name):
    obj = get_object(name)
    if obj.type != "ARMATURE":
        raise CommandError(f"object is not an armature: {name}")
    return obj


def get_mesh_object(name):
    obj = get_object(name)
    if obj.type != "MESH":
        raise CommandError(f"object is not a mesh: {name}")
    return obj


def select_only(objs):
    bpy.ops.object.select_all(action="DESELECT")
    active = None
    for obj in objs:
        obj.select_set(True)
        active = obj
    if active is not None:
        bpy.context.view_layer.objects.active = active


@contextlib.contextmanager
def object_mode(obj, mode):
    """Switch to `mode` with `obj` active, restoring the prior mode/active object after.

    Needed because bone/mesh editing operators only act on data-blocks
    reachable through the currently active object's edit/pose mode.
    """
    prev_active = bpy.context.view_layer.objects.active
    prev_mode = prev_active.mode if prev_active else "OBJECT"
    select_only([obj])
    bpy.ops.object.mode_set(mode=mode)
    try:
        yield obj
    finally:
        bpy.ops.object.mode_set(mode="OBJECT")
        if prev_active is not None:
            bpy.context.view_layer.objects.active = prev_active
            try:
                bpy.ops.object.mode_set(mode=prev_mode)
            except RuntimeError:
                pass


class CommandError(Exception):
    """Recoverable command failure (bad params, missing object, etc)."""
