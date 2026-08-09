import math

import bpy

from ..dispatcher import register
from ..state import serialize_object
from ..utils import (
    CommandError,
    get_armature,
    get_mesh_object,
    get_object,
    object_mode,
    select_only,
)


@register("create_armature")
def create_armature(name=None, location=(0, 0, 0)):
    bpy.ops.object.armature_add(location=location, enter_editmode=False)
    obj = bpy.context.active_object
    if name:
        obj.name = name
    with object_mode(obj, "EDIT"):
        for eb in list(obj.data.edit_bones):
            obj.data.edit_bones.remove(eb)
    return serialize_object(obj)


@register("add_bone")
def add_bone(armature_name, bone_name, head, tail, parent_bone=None, connected=False, roll=0.0):
    arm_obj = get_armature(armature_name)
    actual_name = None
    with object_mode(arm_obj, "EDIT"):
        eb = arm_obj.data.edit_bones.new(bone_name)
        eb.head = head
        eb.tail = tail
        eb.roll = math.radians(roll)
        if parent_bone:
            parent = arm_obj.data.edit_bones.get(parent_bone)
            if parent is None:
                raise CommandError(f"parent bone not found: {parent_bone}")
            eb.parent = parent
            eb.use_connect = connected
        actual_name = eb.name
    return {"armature": arm_obj.name, "bone": actual_name}


@register("edit_bone")
def edit_bone(
    armature_name, bone_name, head=None, tail=None, roll=None, parent_bone=None, connected=None
):
    arm_obj = get_armature(armature_name)
    with object_mode(arm_obj, "EDIT"):
        eb = arm_obj.data.edit_bones.get(bone_name)
        if eb is None:
            raise CommandError(f"bone not found: {bone_name}")
        if head is not None:
            eb.head = head
        if tail is not None:
            eb.tail = tail
        if roll is not None:
            eb.roll = math.radians(roll)
        if parent_bone is not None:
            if parent_bone == "":
                eb.parent = None
            else:
                parent = arm_obj.data.edit_bones.get(parent_bone)
                if parent is None:
                    raise CommandError(f"parent bone not found: {parent_bone}")
                eb.parent = parent
        if connected is not None:
            eb.use_connect = connected
    return {"armature": arm_obj.name, "bone": bone_name}


@register("parent_mesh_to_armature")
def parent_mesh_to_armature(mesh_name, armature_name):
    """Parent without computing weights (empty vertex groups per bone)."""
    mesh_obj = get_mesh_object(mesh_name)
    arm_obj = get_armature(armature_name)
    select_only([mesh_obj, arm_obj])
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.parent_set(type="ARMATURE_NAME", keep_transform=True)
    return serialize_object(mesh_obj)


@register("automatic_weights")
def automatic_weights(mesh_name, armature_name):
    mesh_obj = get_mesh_object(mesh_name)
    arm_obj = get_armature(armature_name)
    select_only([mesh_obj, arm_obj])
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.parent_set(type="ARMATURE_AUTO", keep_transform=True)
    return serialize_object(mesh_obj)


@register("add_constraint")
def add_constraint(object_name, constraint_type, bone_name=None, **settings):
    obj = get_object(object_name)
    if bone_name:
        if obj.type != "ARMATURE":
            raise CommandError("bone_name given but object is not an armature")
        owner = obj.pose.bones.get(bone_name)
        if owner is None:
            raise CommandError(f"pose bone not found: {bone_name}")
    else:
        owner = obj
    try:
        con = owner.constraints.new(type=constraint_type)
    except (TypeError, RuntimeError) as exc:
        raise CommandError(f"could not add constraint {constraint_type}: {exc}") from exc
    for key, value in settings.items():
        if key in ("target",):
            value = get_object(value)
        try:
            setattr(con, key, value)
        except AttributeError as exc:
            raise CommandError(f"constraint {constraint_type} has no setting '{key}'") from exc
    return {"object": obj.name, "bone": bone_name, "constraint": con.name, "type": con.type}


@register("add_ik")
def add_ik(armature_name, bone_name, target_name, chain_count=2, pole_target=None, pole_angle=0.0):
    arm_obj = get_armature(armature_name)
    pbone = arm_obj.pose.bones.get(bone_name)
    if pbone is None:
        raise CommandError(f"pose bone not found: {bone_name}")
    con = pbone.constraints.new(type="IK")
    con.target = get_object(target_name)
    con.chain_count = chain_count
    if pole_target:
        con.pole_target = get_object(pole_target)
        con.pole_angle = math.radians(pole_angle)
    return {"armature": arm_obj.name, "bone": bone_name, "constraint": con.name}


@register("add_copy_rotation")
def add_copy_rotation(armature_name, bone_name, target_name, target_bone=None):
    arm_obj = get_armature(armature_name)
    pbone = arm_obj.pose.bones.get(bone_name)
    if pbone is None:
        raise CommandError(f"pose bone not found: {bone_name}")
    con = pbone.constraints.new(type="COPY_ROTATION")
    con.target = get_object(target_name)
    if target_bone:
        con.subtarget = target_bone
    return {"armature": arm_obj.name, "bone": bone_name, "constraint": con.name}


@register("add_limit_rotation")
def add_limit_rotation(
    armature_name,
    bone_name,
    min_x=0.0,
    max_x=0.0,
    min_y=0.0,
    max_y=0.0,
    min_z=0.0,
    max_z=0.0,
    use_limit_x=True,
    use_limit_y=True,
    use_limit_z=True,
):
    arm_obj = get_armature(armature_name)
    pbone = arm_obj.pose.bones.get(bone_name)
    if pbone is None:
        raise CommandError(f"pose bone not found: {bone_name}")
    con = pbone.constraints.new(type="LIMIT_ROTATION")
    con.use_limit_x, con.use_limit_y, con.use_limit_z = use_limit_x, use_limit_y, use_limit_z
    con.min_x, con.max_x = math.radians(min_x), math.radians(max_x)
    con.min_y, con.max_y = math.radians(min_y), math.radians(max_y)
    con.min_z, con.max_z = math.radians(min_z), math.radians(max_z)
    con.owner_space = "LOCAL"
    return {"armature": arm_obj.name, "bone": bone_name, "constraint": con.name}


@register("pose_bone")
def pose_bone(armature_name, bone_name, location=None, rotation_euler=None, scale=None):
    arm_obj = get_armature(armature_name)
    pbone = arm_obj.pose.bones.get(bone_name)
    if pbone is None:
        raise CommandError(f"pose bone not found: {bone_name}")
    if location is not None:
        pbone.location = location
    if rotation_euler is not None:
        pbone.rotation_mode = "XYZ"
        pbone.rotation_euler = tuple(math.radians(a) for a in rotation_euler)
    if scale is not None:
        pbone.scale = scale
    return {
        "armature": arm_obj.name,
        "bone": bone_name,
        "location": list(pbone.location),
        "rotation_euler_deg": [round(math.degrees(a), 3) for a in pbone.rotation_euler],
        "scale": list(pbone.scale),
    }


@register("inspect_bones")
def inspect_bones(armature_name):
    arm_obj = get_armature(armature_name)
    bones = []
    for bone in arm_obj.data.bones:
        bones.append(
            {
                "name": bone.name,
                "parent": bone.parent.name if bone.parent else None,
                "head_local": list(bone.head_local),
                "tail_local": list(bone.tail_local),
                "use_connect": bone.use_connect,
            }
        )
    return {"armature": arm_obj.name, "bones": bones}


@register("inspect_weights")
def inspect_weights(mesh_name, vertex_group=None):
    obj = get_mesh_object(mesh_name)
    if vertex_group:
        target_groups = [g for g in obj.vertex_groups if g.name == vertex_group]
        if not target_groups:
            raise CommandError(f"vertex group not found: {vertex_group}")
    else:
        target_groups = list(obj.vertex_groups)

    result = {g.name: [] for g in target_groups}
    group_indices = {g.index: g.name for g in target_groups}
    for v in obj.data.vertices:
        for ve in v.groups:
            if ve.group in group_indices:
                result[group_indices[ve.group]].append(
                    {"vertex": v.index, "weight": round(ve.weight, 4)}
                )
    return {"object": obj.name, "groups": result}


@register("weight_paint_adjust")
def weight_paint_adjust(mesh_name, vertex_group, vertex_indices, weight, mode="REPLACE"):
    obj = get_mesh_object(mesh_name)
    group = obj.vertex_groups.get(vertex_group)
    if group is None:
        group = obj.vertex_groups.new(name=vertex_group)
    group.add(vertex_indices, weight, mode)
    return {"object": obj.name, "group": group.name, "vertices": vertex_indices, "weight": weight}
