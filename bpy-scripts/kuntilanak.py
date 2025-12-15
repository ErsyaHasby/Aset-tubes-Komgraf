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
    # Dress - long white dirty gown (simpler, no subdivision for performance)
    bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=0.65, radius2=0.18, depth=2.2, location=(0, 0, 1.1))
    dress = bpy.context.active_object
    dress.rotation_euler[0] = pi
    
    # Head (slightly oval)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.20, location=(0, 0, 2.25))
    head = bpy.context.active_object
    head.scale[2] = 1.15
    
    # Long black hair covering face (thicker, longer)
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.22, depth=1.8, location=(0, 0.08, 1.9))
    hair = bpy.context.active_object
    hair.scale[0] = 1.0
    hair.scale[1] = 0.8
    
    # Hair strands (more strands, longer, more natural fall)
    hair_strands = []
    for i in range(12):
        angle = i * (pi * 2 / 12)
        x_offset = 0.16 * bpy.math.cos(angle)
        y_offset = 0.16 * bpy.math.sin(angle)
        strand_length = 1.8 + (i % 3) * 0.15  # varying lengths
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.025, depth=strand_length, location=(x_offset, y_offset, 1.6))
        strand = bpy.context.active_object
        hair_strands.append(strand)
    
    # Arms - hanging straight down (natural ghost pose)
    bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=0.05, depth=1.1, location=(-0.42, 0, 1.5))
    arm_l = bpy.context.active_object
    arm_l.rotation_euler[2] = -pi / 16  # slight angle outward
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=0.05, depth=1.1, location=(0.42, 0, 1.5))
    arm_r = bpy.context.active_object
    arm_r.rotation_euler[2] = pi / 16
    
    # Hands (thin, long fingers implied by stretched spheres)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.07, location=(-0.42, 0, 0.9))
    hand_l = bpy.context.active_object
    hand_l.scale[2] = 1.3  # elongated
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.07, location=(0.42, 0, 0.9))
    hand_r = bpy.context.active_object
    hand_r.scale[2] = 1.3
    
    # Materials
    mat_dress = make_material('DressDirty', base_color=(0.88, 0.85, 0.80, 1), emission_strength=0.1, roughness=0.75)  # Dirty white-beige
    mat_skin = make_material('GhostSkin', base_color=(0.85, 0.88, 0.86, 1), emission_strength=0.05, roughness=0.6)  # Pale greenish
    mat_hair = make_material('HairBlack', base_color=(0.02, 0.02, 0.02, 1), roughness=0.9)  # Very black
    
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
