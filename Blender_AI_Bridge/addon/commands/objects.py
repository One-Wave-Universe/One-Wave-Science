import math

import bpy

from ..dispatcher import register
from ..state import serialize_object
from ..utils import CommandError, get_collection, get_mesh_object, get_object, select_only


@register("select_object")
def select_object(name):
    obj = get_object(name)
    select_only([obj])
    return serialize_object(obj)


@register("deselect_all")
def deselect_all():
    bpy.ops.object.select_all(action="DESELECT")
    return {"deselected": True}


def _finish_primitive(name):
    obj = bpy.context.active_object
    if name:
        obj.name = name
    return serialize_object(obj)


@register("add_uv_sphere")
def add_uv_sphere(name=None, location=(0, 0, 0), radius=1.0, segments=32, ring_count=16):
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=radius, location=location, segments=segments, ring_count=ring_count
    )
    return _finish_primitive(name)


@register("add_cylinder")
def add_cylinder(name=None, location=(0, 0, 0), radius=1.0, depth=2.0, vertices=32):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=depth, location=location, vertices=vertices
    )
    return _finish_primitive(name)


@register("add_cube")
def add_cube(name=None, location=(0, 0, 0), size=2.0):
    bpy.ops.mesh.primitive_cube_add(size=size, location=location)
    return _finish_primitive(name)


@register("add_plane")
def add_plane(name=None, location=(0, 0, 0), size=2.0):
    bpy.ops.mesh.primitive_plane_add(size=size, location=location)
    return _finish_primitive(name)


@register("duplicate_object")
def duplicate_object(name, new_name=None, linked=False):
    obj = get_object(name)
    select_only([obj])
    bpy.ops.object.duplicate(linked=linked)
    return _finish_primitive(new_name)


@register("delete_object")
def delete_object(name):
    obj = get_object(name)
    bpy.data.objects.remove(obj, do_unlink=True)
    return {"deleted": name}


@register("move_object")
def move_object(name, x, y, z):
    obj = get_object(name)
    obj.location = (x, y, z)
    return serialize_object(obj)


@register("move_object_delta")
def move_object_delta(name, dx, dy, dz):
    obj = get_object(name)
    obj.location.x += dx
    obj.location.y += dy
    obj.location.z += dz
    return serialize_object(obj)


@register("rotate_object")
def rotate_object(name, x, y, z):
    """x/y/z are degrees."""
    obj = get_object(name)
    obj.rotation_euler = (math.radians(x), math.radians(y), math.radians(z))
    return serialize_object(obj)


@register("scale_object")
def scale_object(name, x, y, z):
    obj = get_object(name)
    obj.scale = (x, y, z)
    return serialize_object(obj)


@register("set_dimensions")
def set_dimensions(name, x, y, z):
    obj = get_object(name)
    obj.dimensions = (x, y, z)
    return serialize_object(obj)


@register("rename_object")
def rename_object(old_name, new_name):
    obj = get_object(old_name)
    obj.name = new_name
    return {"old_name": old_name, "new_name": obj.name}


@register("set_parent")
def set_parent(child, parent, keep_transform=True):
    child_obj = get_object(child)
    parent_obj = get_object(parent)
    child_obj.parent = parent_obj
    if keep_transform:
        child_obj.matrix_parent_inverse = parent_obj.matrix_world.inverted()
    else:
        child_obj.matrix_parent_inverse.identity()
    return {"child": child_obj.name, "parent": parent_obj.name}


@register("create_collection")
def create_collection(name):
    if name in bpy.data.collections:
        raise CommandError(f"collection already exists: {name}")
    coll = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(coll)
    return {"name": coll.name}


@register("move_to_collection")
def move_to_collection(object_name, collection_name):
    obj = get_object(object_name)
    coll = get_collection(collection_name)
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    coll.objects.link(obj)
    return serialize_object(obj)


@register("add_modifier")
def add_modifier(object_name, modifier_type, name=None, **settings):
    obj = get_object(object_name)
    if not hasattr(obj, "modifiers"):
        raise CommandError(f"object type {obj.type} does not support modifiers")
    try:
        mod = obj.modifiers.new(name=name or modifier_type.title(), type=modifier_type)
    except (TypeError, RuntimeError) as exc:
        raise CommandError(f"could not add modifier {modifier_type}: {exc}") from exc
    for key, value in settings.items():
        try:
            setattr(mod, key, value)
        except AttributeError as exc:
            raise CommandError(f"modifier {modifier_type} has no setting '{key}'") from exc
    return {"object": obj.name, "modifier": mod.name, "type": mod.type}


@register("apply_modifier")
def apply_modifier(object_name, modifier_name):
    obj = get_mesh_object(object_name)
    select_only([obj])
    bpy.ops.object.modifier_apply(modifier=modifier_name)
    return serialize_object(obj)


@register("join_objects")
def join_objects(object_names, target_name=None):
    objs = [get_object(n) for n in object_names]
    target = get_object(target_name) if target_name else objs[-1]
    select_only(objs)
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.join()
    return serialize_object(target)


@register("separate_object")
def separate_object(object_name, mode="SELECTED"):
    obj = get_mesh_object(object_name)
    from ..utils import object_mode

    with object_mode(obj, "EDIT"):
        bpy.ops.mesh.separate(type=mode)
    return {
        "source": obj.name,
        "resulting_objects": [o.name for o in bpy.data.objects if o.name.startswith(obj.name)],
    }


@register("set_origin")
def set_origin(object_name, type="ORIGIN_GEOMETRY", center="MEDIAN"):
    obj = get_object(object_name)
    select_only([obj])
    bpy.ops.object.origin_set(type=type, center=center)
    return serialize_object(obj)


@register("shade_smooth")
def shade_smooth(object_name, use_auto_smooth=False, angle=30.0):
    obj = get_mesh_object(object_name)
    select_only([obj])
    bpy.ops.object.shade_smooth()
    if use_auto_smooth:
        # Blender < 4.1 exposes auto-smooth as mesh properties; 4.1+ moved it
        # to a "Smooth by Angle" geometry-nodes modifier via an operator.
        if hasattr(obj.data, "use_auto_smooth"):
            obj.data.use_auto_smooth = True
            obj.data.auto_smooth_angle = math.radians(angle)
        else:
            try:
                bpy.ops.object.shade_auto_smooth(angle=math.radians(angle))
            except TypeError:
                bpy.ops.object.shade_auto_smooth()
    return serialize_object(obj)
