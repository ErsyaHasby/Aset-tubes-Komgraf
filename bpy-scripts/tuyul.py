# Tuyul procedural placeholder model
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


def build_body():
    # Chibi-style tuyul with big head proportion
    # Head - very large, bald, round (chibi style)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.28, location=(0, 0, 0.85))
    head = bpy.context.active_object
    head.scale[2] = 0.95  # slightly squashed for cute look
    
    # Eyes (big cute eyes)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.055, location=(-0.1, -0.23, 0.9))
    eye_l = bpy.context.active_object
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.055, location=(0.1, -0.23, 0.9))
    eye_r = bpy.context.active_object
    
    # Mouth (small cute smile)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.06, minor_radius=0.015, location=(0, -0.22, 0.82))
    mouth = bpy.context.active_object
    mouth.rotation_euler[0] = pi / 2
    mouth.scale[2] = 0.5
    
    # Small horn/ears (devil-like but cute)
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.03, radius2=0.005, depth=0.08, location=(-0.18, 0, 1.05))
    horn_l = bpy.context.active_object
    horn_l.rotation_euler[1] = -pi / 6
    bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.03, radius2=0.005, depth=0.08, location=(0.18, 0, 1.05))
    horn_r = bpy.context.active_object
    horn_r.rotation_euler[1] = pi / 6
    
    # Body - small cute belly
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, radius=0.18, location=(0, 0, 0.45))
    body = bpy.context.active_object
    body.scale[2] = 0.75
    body.scale[0] = 0.85
    
    # Short pants (red/pink)
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.19, depth=0.22, location=(0, 0, 0.25))
    pants = bpy.context.active_object
    
    # Arms (thin, running pose) - positioned to attach at shoulder with origin at one end
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.045, depth=0.5, location=(-0.28, -0.05, 0.72))
    arm_l = bpy.context.active_object
    arm_l.rotation_euler[2] = -pi / 8
    arm_l.rotation_euler[1] = pi / 4
    # Move origin to top (shoulder attachment point)
    bpy.context.view_layer.objects.active = arm_l
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.transform.translate(value=(0, 0, -0.25))
    bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.045, depth=0.5, location=(0.28, -0.05, 0.72))
    arm_r = bpy.context.active_object
    arm_r.rotation_euler[2] = pi / 8
    arm_r.rotation_euler[1] = -pi / 4
    # Move origin to top (shoulder attachment point)
    bpy.context.view_layer.objects.active = arm_r
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.transform.translate(value=(0, 0, -0.25))
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Legs (short, dynamic running stance)
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.055, depth=0.4, location=(-0.12, 0, 0.05))
    leg_l = bpy.context.active_object
    leg_l.rotation_euler[0] = pi / 12
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.055, depth=0.4, location=(0.12, 0, 0.05))
    leg_r = bpy.context.active_object
    leg_r.rotation_euler[0] = -pi / 12
    
    # Feet (small cute ovals)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.06, location=(-0.09, 0.04, -0.08))
    foot_l = bpy.context.active_object
    foot_l.scale[1] = 1.2
    foot_l.scale[2] = 0.6
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.06, location=(0.09, 0.04, -0.08))
    foot_r = bpy.context.active_object
    foot_r.scale[1] = 1.2
    foot_r.scale[2] = 0.6
    
    # Materials
    mat_skin = make_material('TuyulSkin', base_color=(0.92, 0.88, 0.82, 1), roughness=0.5)
    mat_pants = make_material('TuyulPants', base_color=(0.9, 0.3, 0.4, 1), roughness=0.6)  # Pink-red shorts
    mat_eye = make_material('TuyulEye', base_color=(0.05, 0.05, 0.05, 1), emission_strength=0.1, roughness=0.2)
    mat_mouth = make_material('TuyulMouth', base_color=(0.3, 0.15, 0.15, 1), roughness=0.6)
    mat_horn = make_material('TuyulHorn', base_color=(0.95, 0.6, 0.65, 1), roughness=0.4)  # Pink horns
    
    for o in [head, body, arm_l, arm_r, leg_l, leg_r, foot_l, foot_r]:
        assign_material(o, mat_skin)
    assign_material(pants, mat_pants)
    for o in [eye_l, eye_r]:
        assign_material(o, mat_eye)
    assign_material(mouth, mat_mouth)
    for o in [horn_l, horn_r]:
        assign_material(o, mat_horn)
    
    root = add_empty_at('TuyulRoot', (0, 0, 0))
    for o in [head, eye_l, eye_r, mouth, horn_l, horn_r, body, pants, arm_l, arm_r, leg_l, leg_r, foot_l, foot_r]:
        o.parent = root
    return root


def main(filepath_fbx=None):
    reset_scene()
    set_units_metric(1.0)
    build_body()
    if filepath_fbx:
        export_fbx(filepath_fbx)
    print('Tuyul generated.')


if __name__ == '__main__':
    main(filepath_fbx=None)
