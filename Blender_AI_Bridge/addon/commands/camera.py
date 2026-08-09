import math
import os

import bpy
from mathutils import Vector

from ..dispatcher import register
from ..state import serialize_camera, serialize_light
from ..utils import CommandError, get_object


@register("create_camera")
def create_camera(name=None, location=(0, 0, 10), rotation=(0, 0, 0)):
    cam_data = bpy.data.cameras.new(name or "Camera")
    obj = bpy.data.objects.new(cam_data.name, cam_data)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = tuple(math.radians(a) for a in rotation)
    if name:
        obj.name = name
    return serialize_camera(obj)


@register("set_active_camera")
def set_active_camera(name):
    obj = get_object(name)
    if obj.type != "CAMERA":
        raise CommandError(f"object is not a camera: {name}")
    bpy.context.scene.camera = obj
    return serialize_camera(obj)


@register("position_camera")
def position_camera(name, location=None, rotation=None, look_at=None):
    obj = get_object(name)
    if obj.type != "CAMERA":
        raise CommandError(f"object is not a camera: {name}")
    if location is not None:
        obj.location = location
    if look_at is not None:
        direction = Vector(look_at) - obj.location
        obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    elif rotation is not None:
        obj.rotation_euler = tuple(math.radians(a) for a in rotation)
    return serialize_camera(obj)


@register("create_light")
def create_light(name=None, light_type="POINT", location=(0, 0, 5), energy=1000.0):
    light_data = bpy.data.lights.new(name or "Light", type=light_type)
    light_data.energy = energy
    obj = bpy.data.objects.new(light_data.name, light_data)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    if name:
        obj.name = name
    return serialize_light(obj)


def _do_render(resolution, samples):
    scene = bpy.context.scene
    scene.render.resolution_x, scene.render.resolution_y = resolution
    scene.render.resolution_percentage = 100
    if samples is not None and hasattr(scene, "cycles"):
        scene.cycles.samples = samples
    bpy.ops.render.render(write_still=False)
    return bpy.data.images["Render Result"]


@register("render_preview")
def render_preview(resolution=(640, 480), samples=None):
    """Renders and writes the result to a scratch PNG (render results can't
    be read back over JSON directly), returning the file path."""
    img = _do_render(resolution, samples)
    path = os.path.join(bpy.app.tempdir, "ai_bridge_render_preview.png")
    img.save_render(filepath=path)
    return {"path": path, "resolution": list(resolution)}


@register("save_render_preview")
def save_render_preview(path, resolution=(640, 480), samples=None):
    img = _do_render(resolution, samples)
    img.save_render(filepath=path)
    return {"path": path, "resolution": list(resolution)}
