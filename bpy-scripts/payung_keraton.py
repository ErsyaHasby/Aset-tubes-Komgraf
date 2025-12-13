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
    # Traditional royal Javanese ceremonial umbrella (payung agung)
    # Ornate base platform
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.4, depth=0.12, location=(0, 0, 0.06))
    base = bpy.context.active_object
    
    # Decorative pole with segments
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.07, depth=1.9, location=(0, 0, 1.0))
    pole = bpy.context.active_object
    
    # Gold decorative rings on pole
    rings = []
    for z in [0.4, 0.9, 1.4]:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.09, minor_radius=0.02, location=(0, 0, z))
        ring = bpy.context.active_object
        rings.append(ring)
    
    # Top ornament (traditional finial)
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=0.12, radius2=0.02, depth=0.25, location=(0, 0, 2.05))
    finial = bpy.context.active_object
    
    # Multi-tiered canopy (traditional royal umbrella has tiers)
    # Top tier
    bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=0.7, radius2=0.1, depth=0.3, location=(0, 0, 2.25))
    canopy_top = bpy.context.active_object
    canopy_top.rotation_euler[0] = pi
    
    # Middle tier
    bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=0.95, radius2=0.12, depth=0.28, location=(0, 0, 2.05))
    canopy_mid = bpy.context.active_object
    canopy_mid.rotation_euler[0] = pi
    
    # Bottom tier (main)
    bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=1.15, radius2=0.15, depth=0.32, location=(0, 0, 1.82))
    canopy_bot = bpy.context.active_object
    canopy_bot.rotation_euler[0] = pi
    
    # Decorative ribs/frame
    ribs = []
    for i in range(12):
        angle = i * (pi / 6)
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.018, depth=1.05, location=(0.57, 0, 1.9))
        rib = bpy.context.active_object
        rib.rotation_euler[2] = angle
        rib.rotation_euler[1] = -pi / 6
        ribs.append(rib)
    
    # Hanging tassels (traditional decoration)
    tassels = []
    for i in range(8):
        angle = i * (pi / 4)
        x = 1.0 * bpy.math.cos(angle)
        y = 1.0 * bpy.math.sin(angle)
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.03, depth=0.35, location=(x, y, 1.5))
        tassel = bpy.context.active_object
        tassels.append(tassel)
    
    # Protective aura/shield effect
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1.4, location=(0, 0, 1.3))
    shield_aura = bpy.context.active_object
    shield_aura.scale[2] = 0.6
    
    # Materials
    mat_wood = make_material('PayungWood', base_color=(0.12, 0.08, 0.05, 1), roughness=0.85)
    mat_gold = make_material('PayungGold', base_color=(0.9, 0.7, 0.2, 1), metallic=0.9, roughness=0.2)
    mat_red_silk = make_material('PayungRedSilk', base_color=(0.8, 0.05, 0.08, 1), roughness=0.4)
    mat_yellow_silk = make_material('PayungYellowSilk', base_color=(0.95, 0.8, 0.15, 1), roughness=0.4)
    mat_white_silk = make_material('PayungWhiteSilk', base_color=(0.95, 0.92, 0.85, 1), roughness=0.45)
    mat_tassel = make_material('PayungTassel', base_color=(0.9, 0.75, 0.2, 1), roughness=0.7)
    mat_shield = make_material('PayungShield', base_color=(0.9, 0.85, 0.5, 0.3), emission_strength=0.8, roughness=0.1)
    
    assign_material(base, mat_wood)
    assign_material(pole, mat_wood)
    for ring in rings:
        assign_material(ring, mat_gold)
    assign_material(finial, mat_gold)
    assign_material(canopy_top, mat_yellow_silk)
    assign_material(canopy_mid, mat_white_silk)
    assign_material(canopy_bot, mat_red_silk)
    for rib in ribs:
        assign_material(rib, mat_gold)
    for tassel in tassels:
        assign_material(tassel, mat_tassel)
    assign_material(shield_aura, mat_shield)
    
    root = add_empty_at('PayungRoot', (0, 0, 0))
    for o in [base, pole] + rings + [finial, canopy_top, canopy_mid, canopy_bot] + ribs + tassels + [shield_aura]:
        o.parent = root
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
