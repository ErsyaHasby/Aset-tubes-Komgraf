# Obor Penjaga procedural placeholder
# Run inside Blender
import bpy
# Try to import helpers; fallback to loading from Blender Text Editor
try:
    from common_utils import reset_scene, set_units_metric, make_material, assign_material, add_empty_at, export_fbx
except ModuleNotFoundError:
    if "common_utils.py" in bpy.data.texts:
        exec(bpy.data.texts["common_utils.py"].as_string(), globals())
    else:
        raise


def build_obor():
    # Tall torch: pole + bowl + flame (emission)
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.08, depth=2.2, location=(0, 0, 1.1))
    pole = bpy.context.active_object
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=0.35, radius2=0.05, depth=0.4, location=(0, 0, 2.2))
    bowl = bpy.context.active_object
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.22, location=(0, 0, 2.35))
    flame = bpy.context.active_object
    mat_pole = make_material('TorchPole', base_color=(0.1, 0.08, 0.06, 1), roughness=0.8)
    mat_bowl = make_material('TorchBowl', base_color=(0.25, 0.2, 0.15, 1), metallic=0.2, roughness=0.6)
    mat_flame = make_material('TorchFlame', base_color=(1.0, 0.6, 0.1, 1), emission_strength=3.0, roughness=0.2)
    assign_material(pole, mat_pole)
    assign_material(bowl, mat_bowl)
    assign_material(flame, mat_flame)
    root = add_empty_at('OborRoot', (0, 0, 0))
    for o in [pole, bowl, flame]:
        o.parent = root
    return root


def main(filepath_fbx=None):
    reset_scene()
    set_units_metric(1.0)
    build_obor()
    if filepath_fbx:
        export_fbx(filepath_fbx)
    print('Obor Penjaga generated.')


if __name__ == '__main__':
    main(filepath_fbx=None)
