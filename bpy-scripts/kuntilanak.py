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
    # Dress - long white flowing gown
    bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=0.7, radius2=0.15, depth=2.0, location=(0, 0, 1.0))
    dress = bpy.context.active_object
    dress.rotation_euler[0] = pi
    # Add subdivision for smooth dress
    mod_subdiv = dress.modifiers.new('Subsurf', 'SUBSURF')
    mod_subdiv.levels = 2
    
    # Head (oval-ish)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.22, location=(0, 0, 2.15))
    head = bpy.context.active_object
    head.scale[2] = 1.2  # stretch vertically
    
    # Long black hair covering face
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.25, depth=1.4, location=(0, 0.05, 2.0))
    hair = bpy.context.active_object
    hair.scale[0] = 0.9
    hair.scale[1] = 0.7
    
    # Hair strands (multiple thin cylinders)
    hair_strands = []
    for i in range(8):
        angle = i * (pi / 4)
        x_offset = 0.18 * bpy.math.cos(angle)
        y_offset = 0.18 * bpy.math.sin(angle)
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.03, depth=1.6, location=(x_offset, y_offset, 1.8))
        strand = bpy.context.active_object
        hair_strands.append(strand)
    
    # Arms - extended forward (creepy pose)
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.055, depth=0.9, location=(-0.5, -0.3, 1.7))
    arm_l = bpy.context.active_object
    arm_l.rotation_euler[1] = pi / 3
    arm_l.rotation_euler[2] = -pi / 12
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.055, depth=0.9, location=(0.5, -0.3, 1.7))
    arm_r = bpy.context.active_object
    arm_r.rotation_euler[1] = -pi / 3
    arm_r.rotation_euler[2] = pi / 12
    
    # Hands (small spheres)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.08, location=(-0.75, -0.6, 1.5))
    hand_l = bpy.context.active_object
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.08, location=(0.75, -0.6, 1.5))
    hand_r = bpy.context.active_object
    
    # Materials
    mat_dress = make_material('DressWhite', base_color=(0.95, 0.95, 0.98, 1), emission_strength=0.3, roughness=0.6)
    mat_skin = make_material('GhostSkin', base_color=(0.92, 0.92, 0.90, 1), emission_strength=0.15, roughness=0.5)
    mat_hair = make_material('HairBlack', base_color=(0.05, 0.05, 0.05, 1), roughness=0.8)
    
    assign_material(dress, mat_dress)
    assign_material(head, mat_skin)
    assign_material(hair, mat_hair)
    for strand in hair_strands:
        assign_material(strand, mat_hair)
    for o in [arm_l, arm_r, hand_l, hand_r]:
        assign_material(o, mat_skin)
    
    # Parent all to root
    root = add_empty_at('KuntilanakRoot', (0, 0, 0))
    for o in [dress, head, hair] + hair_strands + [arm_l, arm_r, hand_l, hand_r]:
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
