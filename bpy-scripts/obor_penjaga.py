# Obor Penjaga procedural placeholder
# Run inside Blender
import bpy
import math
# Try to import helpers; fallback to loading from Blender Text Editor
try:
    from common_utils import reset_scene, set_units_metric, make_material, assign_material, add_empty_at, export_fbx
except ModuleNotFoundError:
    if "common_utils.py" in bpy.data.texts:
        exec(bpy.data.texts["common_utils.py"].as_string(), globals())
    else:
        raise


def build_obor():
    # Low-poly simple torch
    # Base platform (hexagon, low-poly)
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.35, depth=0.12, location=(0, 0, 0.06))
    base = bpy.context.active_object
    
    # Simple pole (octagon, low-poly)
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.06, depth=1.6, location=(0, 0, 0.9))
    pole = bpy.context.active_object
    
    # Single decorative ring (optional, low-poly)
    bpy.ops.mesh.primitive_torus_add(major_segments=8, minor_segments=6, major_radius=0.08, minor_radius=0.02, location=(0, 0, 1.6))
    ring = bpy.context.active_object
    rings = [ring]
    
    # Bowl (simple cone, low-poly)
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.25, radius2=0.08, depth=0.25, location=(0, 0, 1.82))
    bowl = bpy.context.active_object
    bowl.rotation_euler[0] = math.pi
    
    # Flame (geometric stylized - 3 cones for low-poly flame look)
    # Base flame (red-orange)
    bpy.ops.mesh.primitive_cone_add(vertices=6, radius1=0.18, radius2=0.02, depth=0.45, location=(0, 0, 2.05))
    flame_base = bpy.context.active_object
    flame_base.rotation_euler[2] = pi / 6  # slight rotation for style
    
    # Mid flame (orange-yellow)
    bpy.ops.mesh.primitive_cone_add(vertices=5, radius1=0.12, radius2=0.01, depth=0.35, location=(0.05, 0.03, 2.15))
    flame_mid = bpy.context.active_object
    flame_mid.rotation_euler[2] = -pi / 8
    
    # Top flame (yellow-white)
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.06, radius2=0.005, depth=0.22, location=(-0.03, -0.02, 2.28))
    flame_top = bpy.context.active_object
    
    # Glow sphere (smaller, low-poly)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=6, radius=0.22, location=(0, 0, 2.1))
    glow = bpy.context.active_object
    
    # Materials (low-poly style - flatter, less glossy)
    mat_stone = make_material('OborStone', base_color=(0.3, 0.28, 0.25, 1), roughness=1.0)
    mat_pole = make_material('OborWood', base_color=(0.25, 0.15, 0.08, 1), roughness=0.95)
    mat_metal = make_material('OborMetal', base_color=(0.4, 0.35, 0.25, 1), metallic=0.3, roughness=0.7)
    mat_flame_base = make_material('FlameRed', base_color=(1.0, 0.25, 0.05, 1), emission_strength=3.0, roughness=0.3)
    mat_flame_mid = make_material('FlameOrange', base_color=(1.0, 0.6, 0.1, 1), emission_strength=4.5, roughness=0.2)
    mat_flame_top = make_material('FlameYellow', base_color=(1.0, 0.95, 0.5, 1), emission_strength=6.0, roughness=0.1)
    mat_glow = make_material('FlameGlow', base_color=(1.0, 0.5, 0.15, 1), emission_strength=2.5, roughness=0.0)
    
    assign_material(base, mat_stone)
    assign_material(pole, mat_pole)
    for ring in rings:
        assign_material(ring, mat_metal)
    assign_material(bowl, mat_metal)
    assign_material(flame_base, mat_flame_base)
    assign_material(flame_mid, mat_flame_mid)
    assign_material(flame_top, mat_flame_top)
    assign_material(glow, mat_glow)
    
    root = add_empty_at('OborRoot', (0, 0, 0))
    for o in [base, pole] + rings + [bowl, flame_base, flame_mid, flame_top, glow]:
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
