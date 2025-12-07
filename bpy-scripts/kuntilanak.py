# Kuntilanak procedural placeholder model
# Run inside Blender: Scripting tab -> Run Script
import bpy
from math import pi
# Try to import helpers; fallback to loading from Blender Text Editor
try:
    from common_utils import reset_scene, set_units_metric, make_material, assign_material, add_empty_at, export_fbx
except ModuleNotFoundError:
    if "common_utils.py" in bpy.data.texts:
        exec(bpy.data.texts["common_utils.py"].as_string(), globals())
    else:
        raise


def build_body():
    # Floating dress-like cone + head sphere
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=0.6, radius2=0.05, depth=1.8, location=(0, 0, 0))
    dress = bpy.context.active_object
    dress.rotation_euler[0] = pi
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.25, location=(0, 0, 0.9))
    head = bpy.context.active_object
    # Arms (thin cylinders)
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.06, depth=0.8, location=(-0.45, 0, 0.5))
    arm_l = bpy.context.active_object
    arm_l.rotation_euler[1] = pi / 6
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.06, depth=0.8, location=(0.45, 0, 0.5))
    arm_r = bpy.context.active_object
    arm_r.rotation_euler[1] = -pi / 6
    # Materials
    mat_dress = make_material('DressMist', base_color=(0.9, 0.9, 1.0, 1), emission_strength=0.4, roughness=0.7)
    mat_skin = make_material('GhostSkin', base_color=(0.95, 0.95, 0.95, 1), emission_strength=0.2, roughness=0.6)
    for o in [dress]:
        assign_material(o, mat_dress)
    for o in [head, arm_l, arm_r]:
        assign_material(o, mat_skin)
    # Parent to an empty for export
    root = add_empty_at('KuntilanakRoot', (0, 0, 0))
    for o in [dress, head, arm_l, arm_r]:
        o.parent = root
    return root


def main(filepath_fbx=None):
    reset_scene()
    set_units_metric(1.0)
    root = build_body()
    if filepath_fbx:
        export_fbx(filepath_fbx)
    print('Kuntilanak generated.')


if __name__ == '__main__':
    # Set a path when running headless; inside Blender you can leave None and export via UI
    main(filepath_fbx=None)
