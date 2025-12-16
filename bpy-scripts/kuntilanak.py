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
    # Dress - long white dirty gown (detailed with subdivision)
    bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=0.75, radius2=0.22, depth=2.4, location=(0, 0, 1.2))
    dress = bpy.context.active_object
    dress.rotation_euler[0] = pi
    # Add subdivision for cloth detail
    mod_subsurf = dress.modifiers.new(name='Subsurf', type='SUBSURF')
    mod_subsurf.levels = 1
    mod_subsurf.render_levels = 2
    
    # Head (bigger, slightly oval, more visible)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.28, location=(0, 0, 2.55))
    head = bpy.context.active_object
    head.scale[2] = 1.2
    
    # Eyes (creepy red glow)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.04, location=(-0.08, 0.24, 2.6))
    eye_l = bpy.context.active_object
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.04, location=(0.08, 0.24, 2.6))
    eye_r = bpy.context.active_object
    
    # Long black hair covering face (thicker, longer, more prominent)
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.30, depth=2.2, location=(0, 0.05, 2.0))
    hair = bpy.context.active_object
    hair.scale[0] = 1.1
    hair.scale[1] = 0.9
    
    # Hair strands (more strands, longer, messy natural fall)
    hair_strands = []
    for i in range(16):
        angle = i * (pi * 2 / 16)
        x_offset = 0.22 * bpy.math.cos(angle)
        y_offset = 0.22 * bpy.math.sin(angle)
        strand_length = 2.0 + (i % 4) * 0.2  # varying lengths
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.03, depth=strand_length, location=(x_offset, y_offset, 1.8))
        strand = bpy.context.active_object
        # Random slight tilt for natural messy look
        strand.rotation_euler[0] = (i % 5) * 0.05
        strand.rotation_euler[1] = (i % 3) * 0.08
        hair_strands.append(strand)
    
    # Arms - hanging straight down (more visible, longer)
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.055, depth=1.3, location=(-0.55, 0, 1.6))
    arm_l = bpy.context.active_object
    arm_l.rotation_euler[2] = -pi / 14
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.055, depth=1.3, location=(0.55, 0, 1.6))
    arm_r = bpy.context.active_object
    arm_r.rotation_euler[2] = pi / 14
    
    # Hands (thin, long creepy fingers)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=10, radius=0.08, location=(-0.55, 0, 0.95))
    hand_l = bpy.context.active_object
    hand_l.scale[2] = 1.5  # elongated creepy
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=10, radius=0.08, location=(0.55, 0, 0.95))
    hand_r = bpy.context.active_object
    hand_r.scale[2] = 1.5
    
    # Materials
    mat_dress = make_material('DressDirty', base_color=(0.90, 0.88, 0.85, 1), emission_strength=0.08, roughness=0.8)  # Dirty white
    mat_skin = make_material('GhostSkin', base_color=(0.82, 0.88, 0.84, 1), emission_strength=0.04, roughness=0.65)  # Pale ghost
    mat_hair = make_material('HairBlack', base_color=(0.01, 0.01, 0.01, 1), roughness=0.95)  # Very black
    mat_eyes = make_material('EyesRed', base_color=(0.8, 0.05, 0.0, 1), emission_strength=3.5, roughness=0.3)  # Glowing red
    
    assign_material(dress, mat_dress)
    assign_material(head, mat_skin)
    assign_material(hair, mat_hair)
    assign_material(eye_l, mat_eyes)
    assign_material(eye_r, mat_eyes)
    for strand in hair_strands:
        assign_material(strand, mat_hair)
    for o in [arm_l, arm_r, hand_l, hand_r]:
        assign_material(o, mat_skin)
    
    # Parent all to root
    root = add_empty_at('KuntilanakRoot', (0, 0, 0))
    for o in [dress, head, hair, eye_l, eye_r] + hair_strands + [arm_l, arm_r, hand_l, hand_r]:
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
