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
    # Small sneaky tuyul child figure with bald head
    # Head - bald, larger proportion (childlike)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.22, location=(0, 0, 0.95))
    head = bpy.context.active_object
    head.scale[2] = 1.1  # slightly elongated
    
    # Eyes (big mischievous eyes)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.045, location=(-0.08, -0.18, 1.0))
    eye_l = bpy.context.active_object
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.045, location=(0.08, -0.18, 1.0))
    eye_r = bpy.context.active_object
    
    # Body - small round belly
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, radius=0.25, location=(0, 0, 0.5))
    body = bpy.context.active_object
    body.scale[2] = 1
    body.scale[0] = 1
    
    # Short pants
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.24, depth=0.3, location=(0, 0, 0.25))
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
    
    # Feet (small ovals)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.07, location=(-0.12, 0.05, -0.12))
    foot_l = bpy.context.active_object
    foot_l.scale[1] = 1.3
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.07, location=(0.12, 0.05, -0.12))
    foot_r = bpy.context.active_object
    foot_r.scale[1] = 1.3
    
    # Small bag/sack for stealing (iconic tuyul accessory)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=0.12, location=(0.32, 0.1, 0.4))
    sack = bpy.context.active_object
    sack.scale[2] = 1.4
    
    # Materials
    mat_skin = make_material('TuyulSkin', base_color=(0.85, 0.75, 0.6, 1), roughness=0.6)
    mat_pants = make_material('TuyulPants', base_color=(0.15, 0.1, 0.08, 1), roughness=0.8)
    mat_eye = make_material('TuyulEye', base_color=(0.05, 0.05, 0.05, 1), emission_strength=0.1, roughness=0.3)
    mat_sack = make_material('TuyulSack', base_color=(0.4, 0.3, 0.2, 1), roughness=0.9)
    
    for o in [head, body, arm_l, arm_r, leg_l, leg_r, foot_l, foot_r]:
        assign_material(o, mat_skin)
    assign_material(pants, mat_pants)
    for o in [eye_l, eye_r]:
        assign_material(o, mat_eye)
    assign_material(sack, mat_sack)
    
    root = add_empty_at('TuyulRoot', (0, 0, 0))
    for o in [head, eye_l, eye_r, body, pants, arm_l, arm_r, leg_l, leg_r, foot_l, foot_r, sack]:
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
