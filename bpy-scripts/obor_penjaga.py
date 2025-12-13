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
    # Traditional Indonesian torch with ornate base
    # Base platform (stone)
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.5, depth=0.15, location=(0, 0, 0.075))
    base = bpy.context.active_object
    
    # Ornate pole segments
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.09, depth=1.8, location=(0, 0, 1.0))
    pole = bpy.context.active_object
    
    # Decorative rings on pole
    rings = []
    for z in [0.5, 1.0, 1.5]:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.11, minor_radius=0.025, location=(0, 0, z))
        ring = bpy.context.active_object
        rings.append(ring)
    
    # Bowl/holder (traditional metal bowl)
    bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=0.4, radius2=0.08, depth=0.35, location=(0, 0, 1.95))
    bowl = bpy.context.active_object
    bowl.rotation_euler[0] = pi
    
    # Inner bowl detail
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.32, depth=0.08, location=(0, 0, 2.08))
    bowl_inner = bpy.context.active_object
    
    # Flame (layered for realistic fire)
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=0.25, radius2=0.02, depth=0.6, location=(0, 0, 2.4))
    flame_base = bpy.context.active_object
    flame_base.scale[0] = 1.2
    flame_base.scale[1] = 0.9
    
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.18, radius2=0.01, depth=0.5, location=(0, 0, 2.5))
    flame_mid = bpy.context.active_object
    flame_mid.scale[0] = 0.8
    flame_mid.scale[1] = 1.1
    
    bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=0.1, radius2=0.005, depth=0.35, location=(0, 0, 2.6))
    flame_top = bpy.context.active_object
    
    # Glow sphere for light effect
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=0.35, location=(0, 0, 2.4))
    glow = bpy.context.active_object
    
    # Materials
    mat_stone = make_material('OborStone', base_color=(0.25, 0.22, 0.2, 1), roughness=0.9)
    mat_pole = make_material('OborWood', base_color=(0.12, 0.08, 0.05, 1), roughness=0.85)
    mat_metal = make_material('OborMetal', base_color=(0.3, 0.25, 0.15, 1), metallic=0.6, roughness=0.4)
    mat_flame_base = make_material('FlameBase', base_color=(1.0, 0.4, 0.05, 1), emission_strength=4.0, roughness=0.1)
    mat_flame_mid = make_material('FlameMid', base_color=(1.0, 0.7, 0.1, 1), emission_strength=6.0, roughness=0.1)
    mat_flame_top = make_material('FlameTop', base_color=(1.0, 0.9, 0.6, 1), emission_strength=8.0, roughness=0.05)
    mat_glow = make_material('FlameGlow', base_color=(1.0, 0.6, 0.2, 1), emission_strength=3.5, roughness=0.0)
    
    assign_material(base, mat_stone)
    assign_material(pole, mat_pole)
    for ring in rings:
        assign_material(ring, mat_metal)
    assign_material(bowl, mat_metal)
    assign_material(bowl_inner, mat_metal)
    assign_material(flame_base, mat_flame_base)
    assign_material(flame_mid, mat_flame_mid)
    assign_material(flame_top, mat_flame_top)
    assign_material(glow, mat_glow)
    
    root = add_empty_at('OborRoot', (0, 0, 0))
    for o in [base, pole] + rings + [bowl, bowl_inner, flame_base, flame_mid, flame_top, glow]:
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
