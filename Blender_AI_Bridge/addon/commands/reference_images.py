import math

import bpy

from ..dispatcher import register
from ..utils import CommandError, get_object


def _get_reference(name):
    obj = get_object(name)
    if obj.type != "EMPTY" or obj.empty_display_type != "IMAGE":
        raise CommandError(f"object is not a reference image: {name}")
    return obj


def _serialize_reference(obj):
    return {
        "name": obj.name,
        "image_path": obj.data.filepath if obj.data else None,
        "location": list(obj.location),
        "rotation_euler_deg": [round(math.degrees(a), 3) for a in obj.rotation_euler],
        "scale": list(obj.scale),
        "opacity": obj.color[3],
        "use_alpha": obj.use_empty_image_alpha,
        "hidden": obj.hide_viewport,
        "locked": all(obj.lock_location),
    }


@register("import_reference_image")
def import_reference_image(path, name=None, location=(0, 0, 0)):
    bpy.ops.object.load_reference_image(filepath=path)
    obj = bpy.context.active_object
    if obj is None or obj.type != "EMPTY":
        raise CommandError("failed to create reference image empty")
    obj.location = location
    if name:
        obj.name = name
    return _serialize_reference(obj)


@register("list_reference_images")
def list_reference_images():
    refs = [o for o in bpy.data.objects if o.type == "EMPTY" and o.empty_display_type == "IMAGE"]
    return {"references": [_serialize_reference(o) for o in refs]}


@register("inspect_reference_image")
def inspect_reference_image(name):
    return _serialize_reference(_get_reference(name))


@register("set_reference_opacity")
def set_reference_opacity(name, alpha):
    obj = _get_reference(name)
    obj.use_empty_image_alpha = True
    obj.color[3] = alpha
    return _serialize_reference(obj)


@register("set_reference_transform")
def set_reference_transform(name, location=None, rotation=None, scale=None):
    obj = _get_reference(name)
    if location is not None:
        obj.location = location
    if rotation is not None:
        obj.rotation_euler = tuple(math.radians(a) for a in rotation)
    if scale is not None:
        obj.scale = scale if isinstance(scale, (list, tuple)) else (scale, scale, scale)
    return _serialize_reference(obj)


@register("lock_reference")
def lock_reference(name, locked=True):
    obj = _get_reference(name)
    obj.lock_location = (locked, locked, locked)
    obj.lock_rotation = (locked, locked, locked)
    obj.lock_scale = (locked, locked, locked)
    return _serialize_reference(obj)


@register("hide_reference")
def hide_reference(name, hide=True):
    obj = _get_reference(name)
    obj.hide_viewport = hide
    return _serialize_reference(obj)
