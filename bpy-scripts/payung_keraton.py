# Payung Keraton procedural placeholder
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


def build_payung():
    # Pole
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.06, depth=2.2, location=(0, 0, 1.1))
    pole = bpy.context.active_object
    # Umbrella canopy (disc + ribs)
    bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=1.0, radius2=0.05, depth=0.25, location=(0, 0, 2.35))
    canopy = bpy.context.active_object
    canopy.rotation_euler[0] = pi
    ribs = []
    for i in range(8):
        angle = i * (pi / 4)
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.02, depth=0.9, location=(0.45, 0, 2.3))
        rib = bpy.context.active_object
        rib.rotation_euler[2] = angle
        ribs.append(rib)
    # Materials
    mat_pole = make_material('PayungPole', base_color=(0.15, 0.12, 0.1, 1), roughness=0.8)
    mat_canopy = make_material('PayungCanopy', base_color=(0.85, 0.1, 0.12, 1), roughness=0.5)
    assign_material(pole, mat_pole)
    assign_material(canopy, mat_canopy)
    for r in ribs:
        assign_material(r, mat_pole)
    # Root
    root = add_empty_at('PayungRoot', (0, 0, 0))
    pole.parent = root
    canopy.parent = root
    for r in ribs:
        r.parent = root
    return root


def main(filepath_fbx=None):
    reset_scene()
    set_units_metric(1.0)
    build_payung()
    if filepath_fbx:
        export_fbx(filepath_fbx)
    print('Payung Keraton generated.')


if __name__ == '__main__':
    main(filepath_fbx=None)
