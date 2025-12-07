# Gamelan Spirit procedural placeholder
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


def build_gamelan():
    # Base stand
    bpy.ops.mesh.primitive_cube_add(size=1.6, location=(0, 0, 0.25))
    base = bpy.context.active_object
    base.scale[2] = 0.25
    # Metallophone bars
    bars = []
    mat_metal = make_material('GamelanMetal', base_color=(0.9, 0.85, 0.6, 1), metallic=0.8, roughness=0.3)
    for i in range(8):
        x = -0.7 + i * 0.2
        bpy.ops.mesh.primitive_cube_add(size=0.18, location=(x, 0, 0.5))
        bar = bpy.context.active_object
        assign_material(bar, mat_metal)
        bars.append(bar)
    # Aura ring (emissive torus)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.9, minor_radius=0.05, location=(0, 0, 0.1))
    aura = bpy.context.active_object
    mat_aura = make_material('GamelanAura', base_color=(0.6, 0.8, 1.0, 1), emission_strength=2.0, roughness=0.4)
    assign_material(base, make_material('GamelanStand', base_color=(0.2, 0.12, 0.08, 1), roughness=0.8))
    assign_material(aura, mat_aura)
    root = add_empty_at('GamelanRoot', (0, 0, 0))
    base.parent = root
    aura.parent = root
    for b in bars:
        b.parent = root
    return root


def main(filepath_fbx=None):
    reset_scene()
    set_units_metric(1.0)
    build_gamelan()
    if filepath_fbx:
        export_fbx(filepath_fbx)
    print('Gamelan Spirit generated.')


if __name__ == '__main__':
    main(filepath_fbx=None)
