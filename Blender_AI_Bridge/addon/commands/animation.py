import bpy

from ..dispatcher import register
from ..utils import CommandError, get_object, select_only


def _full_data_path(data_path, bone_name):
    return f'pose.bones["{bone_name}"].{data_path}' if bone_name else data_path


@register("set_frame")
def set_frame(frame):
    bpy.context.scene.frame_set(frame)
    return {"frame": bpy.context.scene.frame_current}


@register("insert_keyframe")
def insert_keyframe(object_name, data_path, frame=None, index=-1, bone_name=None):
    obj = get_object(object_name)
    if bone_name and obj.type != "ARMATURE":
        raise CommandError("bone_name given but object is not an armature")
    if frame is None:
        frame = bpy.context.scene.frame_current
    full_path = _full_data_path(data_path, bone_name)
    try:
        if index >= 0:
            obj.keyframe_insert(data_path=full_path, index=index, frame=frame)
        else:
            obj.keyframe_insert(data_path=full_path, frame=frame)
    except TypeError as exc:
        raise CommandError(f"could not insert keyframe on {full_path}: {exc}") from exc
    return {"object": obj.name, "data_path": full_path, "frame": frame}


@register("delete_keyframe")
def delete_keyframe(object_name, data_path, frame=None, bone_name=None):
    obj = get_object(object_name)
    if frame is None:
        frame = bpy.context.scene.frame_current
    full_path = _full_data_path(data_path, bone_name)
    try:
        obj.keyframe_delete(data_path=full_path, frame=frame)
    except TypeError as exc:
        raise CommandError(f"could not delete keyframe on {full_path}: {exc}") from exc
    return {"object": obj.name, "data_path": full_path, "frame": frame}


@register("get_keyframes")
def get_keyframes(object_name, bone_name=None):
    obj = get_object(object_name)
    if not obj.animation_data or not obj.animation_data.action:
        return {"object": obj.name, "action": None, "keyframes": []}
    action = obj.animation_data.action
    prefix = f'pose.bones["{bone_name}"].' if bone_name else None
    keyframes = []
    for fcurve in action.fcurves:
        if prefix and not fcurve.data_path.startswith(prefix):
            continue
        for kp in fcurve.keyframe_points:
            keyframes.append(
                {
                    "data_path": fcurve.data_path,
                    "array_index": fcurve.array_index,
                    "frame": kp.co.x,
                    "value": kp.co.y,
                    "interpolation": kp.interpolation,
                }
            )
    return {"object": obj.name, "action": action.name, "keyframes": keyframes}


@register("create_action")
def create_action(name):
    if name in bpy.data.actions:
        raise CommandError(f"action already exists: {name}")
    action = bpy.data.actions.new(name)
    return {"name": action.name}


@register("assign_action")
def assign_action(object_name, action_name):
    obj = get_object(object_name)
    action = bpy.data.actions.get(action_name)
    if action is None:
        raise CommandError(f"action not found: {action_name}")
    if obj.animation_data is None:
        obj.animation_data_create()
    obj.animation_data.action = action
    return {"object": obj.name, "action": action.name}


@register("duplicate_action")
def duplicate_action(action_name, new_name=None):
    action = bpy.data.actions.get(action_name)
    if action is None:
        raise CommandError(f"action not found: {action_name}")
    new_action = action.copy()
    if new_name:
        new_action.name = new_name
    return {"name": new_action.name}


@register("set_interpolation")
def set_interpolation(object_name, interpolation="BEZIER", data_path=None, bone_name=None):
    obj = get_object(object_name)
    if not obj.animation_data or not obj.animation_data.action:
        raise CommandError(f"object has no action: {object_name}")
    target_path = _full_data_path(data_path, bone_name) if data_path else None
    prefix = f'pose.bones["{bone_name}"].' if bone_name else None
    changed = 0
    for fcurve in obj.animation_data.action.fcurves:
        if prefix and not fcurve.data_path.startswith(prefix):
            continue
        if target_path and fcurve.data_path != target_path:
            continue
        for kp in fcurve.keyframe_points:
            kp.interpolation = interpolation
            changed += 1
    return {"object": obj.name, "keyframes_changed": changed}


@register("play_range")
def play_range(start, end):
    """Sets the scene's playback range. Real-time playback can't be driven
    synchronously over this bridge; step frames with set_frame + render_preview
    instead if you need to inspect motion."""
    scene = bpy.context.scene
    scene.frame_start = start
    scene.frame_end = end
    return {"frame_start": scene.frame_start, "frame_end": scene.frame_end}


@register("bake_action")
def bake_action(
    object_name,
    frame_start,
    frame_end,
    only_selected_bones=False,
    visual_keying=True,
    clear_constraints=False,
):
    obj = get_object(object_name)
    select_only([obj])
    bake_types = {"POSE"} if obj.type == "ARMATURE" else {"OBJECT"}
    bpy.ops.nla.bake(
        frame_start=frame_start,
        frame_end=frame_end,
        only_selected=only_selected_bones,
        visual_keying=visual_keying,
        clear_constraints=clear_constraints,
        bake_types=bake_types,
    )
    return {"object": obj.name, "frame_start": frame_start, "frame_end": frame_end}


@register("inspect_animation_state")
def inspect_animation_state():
    scene = bpy.context.scene
    obj = bpy.context.view_layer.objects.active
    action_name = None
    if obj and obj.animation_data and obj.animation_data.action:
        action_name = obj.animation_data.action.name
    return {
        "frame_current": scene.frame_current,
        "frame_start": scene.frame_start,
        "frame_end": scene.frame_end,
        "active_object": obj.name if obj else None,
        "active_action": action_name,
    }
