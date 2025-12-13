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
    # Traditional gamelan set with mystical aura
    # Ornate wooden base/stand with carved details
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.15))
    base = bpy.context.active_object
    base.scale = (1.8, 0.8, 0.3)
    
    # Side supports (carved wood)
    bpy.ops.mesh.primitive_cube_add(size=0.2, location=(-0.85, 0, 0.35))
    support_l = bpy.context.active_object
    support_l.scale = (0.8, 3.5, 2.0)
    bpy.ops.mesh.primitive_cube_add(size=0.2, location=(0.85, 0, 0.35))
    support_r = bpy.context.active_object
    support_r.scale = (0.8, 3.5, 2.0)
    
    # Metal bars (bronze gamelan keys) with varying sizes
    bars = []
    bar_sizes = [0.22, 0.2, 0.19, 0.17, 0.16, 0.15, 0.14, 0.13]
    for i in range(8):
        x = -0.7 + i * 0.2
        size = bar_sizes[i]
        bpy.ops.mesh.primitive_cube_add(size=0.15, location=(x, 0, 0.52))
        bar = bpy.context.active_object
        bar.scale = (1.0, 4.0, size * 5)
        bars.append(bar)
    
    # Resonators under bars (traditional gamelan design)
    resonators = []
    for i in range(8):
        x = -0.7 + i * 0.2
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.08, depth=0.2, location=(x, 0, 0.3))
        res = bpy.context.active_object
        resonators.append(res)
    
    # Mystical aura effects (multiple rings)
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.04, location=(0, 0, 0.5))
    aura1 = bpy.context.active_object
    aura1.rotation_euler[0] = pi / 2
    
    bpy.ops.mesh.primitive_torus_add(major_radius=1.2, minor_radius=0.03, location=(0, 0, 0.5))
    aura2 = bpy.context.active_object
    aura2.rotation_euler[0] = pi / 2
    
    bpy.ops.mesh.primitive_torus_add(major_radius=0.8, minor_radius=0.05, location=(0, 0, 0.5))
    aura3 = bpy.context.active_object
    aura3.rotation_euler[0] = pi / 2
    aura3.rotation_euler[1] = pi / 4
    
    # Spirit orbs floating above
    orbs = []
    for i in range(4):
        angle = i * (pi / 2)
        x = 0.6 * bpy.math.cos(angle)
        y = 0.6 * bpy.math.sin(angle)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=0.08, location=(x, y, 0.9))
        orb = bpy.context.active_object
        orbs.append(orb)
    
    # Materials
    mat_wood = make_material('GamelanWood', base_color=(0.15, 0.1, 0.06, 1), roughness=0.85)
    mat_bronze = make_material('GamelanBronze', base_color=(0.85, 0.65, 0.3, 1), metallic=0.85, roughness=0.25)
    mat_resonator = make_material('GamelanResonator', base_color=(0.6, 0.5, 0.3, 1), metallic=0.3, roughness=0.6)
    mat_aura = make_material('GamelanAura', base_color=(0.5, 0.7, 1.0, 1), emission_strength=2.5, roughness=0.2)
    mat_orb = make_material('SpiritOrb', base_color=(0.7, 0.9, 1.0, 1), emission_strength=3.0, roughness=0.1)
    
    for o in [base, support_l, support_r]:
        assign_material(o, mat_wood)
    for bar in bars:
        assign_material(bar, mat_bronze)
    for res in resonators:
        assign_material(res, mat_resonator)
    for aura in [aura1, aura2, aura3]:
        assign_material(aura, mat_aura)
    for orb in orbs:
        assign_material(orb, mat_orb)
    
    root = add_empty_at('GamelanRoot', (0, 0, 0))
    for o in [base, support_l, support_r] + bars + resonators + [aura1, aura2, aura3] + orbs:
        o.parent = root
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
