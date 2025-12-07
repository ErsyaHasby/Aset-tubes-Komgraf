# Tuyul procedural placeholder model
# Run inside Blender
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
    # Small fast-looking figure: head + body capsule
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.18, location=(0, 0, 0.9))
    head = bpy.context.active_object
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.22, depth=1.0, location=(0, 0, 0.4))
    body = bpy.context.active_object
    # Arms & legs tiny
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.04, depth=0.6, location=(-0.25, 0, 0.3))
    arm_l = bpy.context.active_object
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.04, depth=0.6, location=(0.25, 0, 0.3))
    arm_r = bpy.context.active_object
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.05, depth=0.6, location=(-0.12, 0.1, 0.0))
    leg_l = bpy.context.active_object
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.05, depth=0.6, location=(0.12, -0.1, 0.0))
    leg_r = bpy.context.active_object
    # Materials
    mat_skin = make_material('TuyulSkin', base_color=(0.95, 0.95, 0.85, 1), roughness=0.6)
    mat_short = make_material('TuyulShort', base_color=(0.2, 0.2, 0.2, 1), roughness=0.7)
    for o in [head, arm_l, arm_r, leg_l, leg_r]:
        assign_material(o, mat_skin)
    assign_material(body, mat_short)
    root = add_empty_at('TuyulRoot', (0, 0, 0))
    for o in [head, body, arm_l, arm_r, leg_l, leg_r]:
        o.parent = root
    return root


def main(filepath_fbx=None):
    reset_scene()
    set_units_metric(1.0)
    build_body()
    if filepath_fbx:
        export_fbx(filepath_fbx)
    print('Tuyul generated.')


if __name__ == '__main__':
    main(filepath_fbx=None)
