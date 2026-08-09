import bmesh
import bpy

from ..dispatcher import register
from ..state import serialize_object
from ..utils import CommandError, get_mesh_object, get_object, select_only

_AXIS_INDEX = {"X": 0, "Y": 1, "Z": 2}


def _axis_tuple(axis):
    axis = axis.upper()
    if axis not in _AXIS_INDEX:
        raise CommandError(f"axis must be X, Y or Z, got {axis}")
    return tuple(i == _AXIS_INDEX[axis] for i in range(3))


@register("add_mirror_modifier")
def add_mirror_modifier(object_name, axis="X", use_clip=True):
    obj = get_mesh_object(object_name)
    mod = obj.modifiers.new(name="Mirror", type="MIRROR")
    mod.use_axis = _axis_tuple(axis)
    mod.use_clip = use_clip
    return {"object": obj.name, "modifier": mod.name}


@register("create_mirrored_mesh")
def create_mirrored_mesh(object_name, axis="X", merge_threshold=0.001):
    """Mirror the mesh across `axis` and bake it in (applies the modifier)."""
    obj = get_mesh_object(object_name)
    mod = obj.modifiers.new(name="AI_Mirror", type="MIRROR")
    mod.use_axis = _axis_tuple(axis)
    mod.merge_threshold = merge_threshold
    select_only([obj])
    bpy.ops.object.modifier_apply(modifier=mod.name)
    return serialize_object(obj)


@register("add_subdivision")
def add_subdivision(object_name, levels=2, render_levels=None):
    obj = get_mesh_object(object_name)
    mod = obj.modifiers.new(name="Subdivision", type="SUBSURF")
    mod.levels = levels
    mod.render_levels = render_levels if render_levels is not None else levels
    return {"object": obj.name, "modifier": mod.name}


@register("add_solidify")
def add_solidify(object_name, thickness=0.02):
    obj = get_mesh_object(object_name)
    mod = obj.modifiers.new(name="Solidify", type="SOLIDIFY")
    mod.thickness = thickness
    return {"object": obj.name, "modifier": mod.name}


@register("add_boolean")
def add_boolean(object_name, target_name, operation="DIFFERENCE"):
    obj = get_mesh_object(object_name)
    target = get_mesh_object(target_name)
    mod = obj.modifiers.new(name="Boolean", type="BOOLEAN")
    mod.object = target
    mod.operation = operation
    return {"object": obj.name, "modifier": mod.name, "operand": target.name}


@register("create_curve")
def create_curve(name, curve_type="BEZIER", points=None):
    points = points or [[0, 0, 0], [1, 0, 0]]
    if len(points) < 2:
        raise CommandError("a curve needs at least 2 points")
    curve_data = bpy.data.curves.new(name, type="CURVE")
    curve_data.dimensions = "3D"
    spline = curve_data.splines.new(curve_type)
    if curve_type == "BEZIER":
        spline.bezier_points.add(len(points) - 1)
        for i, p in enumerate(points):
            bp = spline.bezier_points[i]
            bp.co = p
            bp.handle_left_type = "AUTO"
            bp.handle_right_type = "AUTO"
    else:
        spline.points.add(len(points) - 1)
        for i, p in enumerate(points):
            spline.points[i].co = (p[0], p[1], p[2], 1.0)
    obj = bpy.data.objects.new(name, curve_data)
    bpy.context.collection.objects.link(obj)
    return serialize_object(obj)


@register("convert_curve_to_mesh")
def convert_curve_to_mesh(object_name):
    obj = get_object(object_name)
    if obj.type != "CURVE":
        raise CommandError(f"object is not a curve: {object_name}")
    select_only([obj])
    bpy.ops.object.convert(target="MESH")
    return serialize_object(obj)


@register("edit_mesh_vertices")
def edit_mesh_vertices(object_name, updates):
    """updates: [{"index": int, "co": [x,y,z], "select": bool}, ...]"""
    obj = get_mesh_object(object_name)
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.verts.ensure_lookup_table()
    changed = []
    for u in updates:
        idx = u["index"]
        if idx < 0 or idx >= len(bm.verts):
            bm.free()
            raise CommandError(f"vertex index out of range: {idx}")
        v = bm.verts[idx]
        if "co" in u:
            v.co = u["co"]
        if "select" in u:
            v.select = u["select"]
        changed.append(idx)
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    return {"object": obj.name, "updated_indices": changed}


@register("edit_mesh_edges")
def edit_mesh_edges(object_name, dissolve_indices=None, crease=None):
    """crease: [{"index": int, "value": 0..1}, ...]. Applied before dissolve."""
    obj = get_mesh_object(object_name)
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.edges.ensure_lookup_table()

    if crease:
        try:
            crease_layer = bm.edges.layers.crease.verify()
        except AttributeError as exc:
            bm.free()
            raise CommandError(
                "edge crease layer unavailable on this Blender version"
            ) from exc
        for entry in crease:
            bm.edges[entry["index"]][crease_layer] = entry["value"]

    dissolved = []
    if dissolve_indices:
        edges = [bm.edges[i] for i in dissolve_indices]
        bmesh.ops.dissolve_edges(bm, edges=edges, use_verts=True)
        dissolved = list(dissolve_indices)

    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    return {"object": obj.name, "dissolved_indices": dissolved}


@register("edit_mesh_faces")
def edit_mesh_faces(object_name, extrude=None, inset=None, delete_indices=None):
    """extrude: [{"indices":[...], "translate":[dx,dy,dz]}, ...]
    inset: [{"indices":[...], "thickness":0.1, "depth":0.0}, ...]

    Entries are applied in order: extrude, then inset, then delete. Face
    indices always refer to the mesh's current state at the start of this
    call, so an index used by an inset entry must exist independently of
    any extrude entries run earlier in the same call (extrude changes face
    indices). Call this once per logical edit if you need to chain them.
    """
    obj = get_mesh_object(object_name)
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.faces.ensure_lookup_table()

    if extrude:
        for entry in extrude:
            faces = [bm.faces[i] for i in entry["indices"]]
            result = bmesh.ops.extrude_face_region(bm, geom=faces)
            verts = [g for g in result["geom"] if isinstance(g, bmesh.types.BMVert)]
            bmesh.ops.translate(bm, vec=entry.get("translate", (0, 0, 0)), verts=verts)
            bm.faces.ensure_lookup_table()

    if inset:
        for entry in inset:
            faces = [bm.faces[i] for i in entry["indices"]]
            bmesh.ops.inset_individual(
                bm,
                faces=faces,
                thickness=entry.get("thickness", 0.1),
                depth=entry.get("depth", 0.0),
            )
            bm.faces.ensure_lookup_table()

    if delete_indices:
        faces = [bm.faces[i] for i in delete_indices]
        bmesh.ops.delete(bm, geom=faces, context="FACES")

    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    return {"object": obj.name, "face_count": len(mesh.polygons)}
