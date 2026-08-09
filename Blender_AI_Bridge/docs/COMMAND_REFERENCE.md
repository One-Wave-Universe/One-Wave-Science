# Command Reference

Every command below is called through the MCP `execute_command(command,
params)` / `execute_commands([...])` tools. This list is also available
live via the `list_commands` MCP tool (which reflects whatever addon
version is actually running, including param names).

Rotations are in **degrees**. Locations/scale/dimensions are plain
Blender units.

## Scene / file

| Command | Params |
|---|---|
| `get_scene_state` | — |
| `list_commands` | — |
| `save_blend` | — |
| `save_blend_as` | `path` |
| `undo` / `redo` | — |
| `begin_transaction` | — |
| `commit_transaction` | `transaction_id?` |
| `rollback_transaction` | `transaction_id?` |

## Objects: create / select / delete

| Command | Params |
|---|---|
| `select_object` | `name` |
| `deselect_all` | — |
| `add_uv_sphere` | `name?, location?, radius?, segments?, ring_count?` |
| `add_cylinder` | `name?, location?, radius?, depth?, vertices?` |
| `add_cube` | `name?, location?, size?` |
| `add_plane` | `name?, location?, size?` |
| `duplicate_object` | `name, new_name?, linked?` |
| `delete_object` | `name` |

## Objects: transform / hierarchy

| Command | Params |
|---|---|
| `move_object` | `name, x, y, z` |
| `move_object_delta` | `name, dx, dy, dz` |
| `rotate_object` | `name, x, y, z` (degrees) |
| `scale_object` | `name, x, y, z` |
| `set_dimensions` | `name, x, y, z` |
| `rename_object` | `old_name, new_name` |
| `set_parent` | `child, parent, keep_transform?` |
| `create_collection` | `name` |
| `move_to_collection` | `object_name, collection_name` |

## Objects: modifiers / mesh ops

| Command | Params |
|---|---|
| `add_modifier` | `object_name, modifier_type, name?, **settings` |
| `apply_modifier` | `object_name, modifier_name` |
| `join_objects` | `object_names, target_name?` |
| `separate_object` | `object_name, mode?` (`SELECTED`/`MATERIAL`/`LOOSE`) |
| `set_origin` | `object_name, type?, center?` |
| `shade_smooth` | `object_name, use_auto_smooth?, angle?` |

## Modeling

| Command | Params |
|---|---|
| `add_mirror_modifier` | `object_name, axis?, use_clip?` |
| `create_mirrored_mesh` | `object_name, axis?, merge_threshold?` (bakes the mirror in) |
| `add_subdivision` | `object_name, levels?, render_levels?` |
| `add_solidify` | `object_name, thickness?` |
| `add_boolean` | `object_name, target_name, operation?` |
| `create_curve` | `name, curve_type?, points` |
| `convert_curve_to_mesh` | `object_name` |
| `edit_mesh_vertices` | `object_name, updates: [{index, co?, select?}]` |
| `edit_mesh_edges` | `object_name, dissolve_indices?, crease?` |
| `edit_mesh_faces` | `object_name, extrude?, inset?, delete_indices?` |

## Rigging

| Command | Params |
|---|---|
| `create_armature` | `name?, location?` |
| `add_bone` | `armature_name, bone_name, head, tail, parent_bone?, connected?, roll?` |
| `edit_bone` | `armature_name, bone_name, head?, tail?, roll?, parent_bone?, connected?` |
| `parent_mesh_to_armature` | `mesh_name, armature_name` (no weights) |
| `automatic_weights` | `mesh_name, armature_name` |
| `add_constraint` | `object_name, constraint_type, bone_name?, **settings` |
| `add_ik` | `armature_name, bone_name, target_name, chain_count?, pole_target?, pole_angle?` |
| `add_copy_rotation` | `armature_name, bone_name, target_name, target_bone?` |
| `add_limit_rotation` | `armature_name, bone_name, min_x?..max_z?, use_limit_x?..z?` |
| `pose_bone` | `armature_name, bone_name, location?, rotation_euler?, scale?` |
| `inspect_bones` | `armature_name` |
| `inspect_weights` | `mesh_name, vertex_group?` |
| `weight_paint_adjust` | `mesh_name, vertex_group, vertex_indices, weight, mode?` |

## Animation

| Command | Params |
|---|---|
| `set_frame` | `frame` |
| `insert_keyframe` | `object_name, data_path, frame?, index?, bone_name?` |
| `delete_keyframe` | `object_name, data_path, frame?, bone_name?` |
| `get_keyframes` | `object_name, bone_name?` |
| `create_action` | `name` |
| `assign_action` | `object_name, action_name` |
| `duplicate_action` | `action_name, new_name?` |
| `set_interpolation` | `object_name, interpolation?, data_path?, bone_name?` |
| `play_range` | `start, end` |
| `bake_action` | `object_name, frame_start, frame_end, only_selected_bones?, visual_keying?, clear_constraints?` |
| `inspect_animation_state` | — |

## Reference images

| Command | Params |
|---|---|
| `import_reference_image` | `path, name?, location?` |
| `list_reference_images` | — |
| `inspect_reference_image` | `name` |
| `set_reference_opacity` | `name, alpha` |
| `set_reference_transform` | `name, location?, rotation?, scale?` |
| `lock_reference` | `name, locked?` |
| `hide_reference` | `name, hide?` |

## Camera / lights / render

| Command | Params |
|---|---|
| `create_camera` | `name?, location?, rotation?` |
| `set_active_camera` | `name` |
| `position_camera` | `name, location?, rotation?, look_at?` |
| `create_light` | `name?, light_type?, location?, energy?` |
| `render_preview` | `resolution?, samples?` (returns a scratch file path; the MCP `render_preview` tool wraps this and returns the image directly) |
| `save_render_preview` | `path, resolution?, samples?` |
