# Genderuwo - Enemy Asset
# Monster berbulu besar seperti referensi
# Run inside Blender setelah common_utils.py

import bpy
from math import pi, radians

# Import helpers
try:
    from common_utils import (
        reset_scene,
        set_units_metric,
        make_material,
        assign_material,
        add_empty_at,
        export_fbx,
    )
except ModuleNotFoundError:
    if "common_utils.py" in bpy.data.texts:
        exec(bpy.data.texts["common_utils.py"].as_string(), globals())
    else:
        raise


def build_genderuwo():
    """Bangun monster Genderuwo yang bulat dan berbulu."""
    
    all_objects = []
    
    # ===== TUBUH UTAMA (BULAT BESAR) =====
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.8, location=(0, 0, 1.2))
    body = bpy.context.active_object
    body.name = "Body"
    body.scale = (1.0, 0.85, 1.1)
    bpy.ops.object.shade_smooth()
    all_objects.append(body)
    
    # ===== KEPALA (MENYATU DENGAN BADAN) =====
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.55, location=(0, 0.05, 2.05))
    head = bpy.context.active_object
    head.name = "Head"
    head.scale = (0.95, 0.9, 0.95)
    bpy.ops.object.shade_smooth()
    all_objects.append(head)
    
    # ===== MATA (BESAR MERAH BULAT) =====
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.12, location=(-0.18, 0.42, 2.12))
    eye_left = bpy.context.active_object
    eye_left.name = "Eye_Left"
    eye_left.scale = (1.0, 0.6, 1.0)
    all_objects.append(eye_left)
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.12, location=(0.18, 0.42, 2.12))
    eye_right = bpy.context.active_object
    eye_right.name = "Eye_Right"
    eye_right.scale = (1.0, 0.6, 1.0)
    all_objects.append(eye_right)
    
    # Pupil kiri
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.05, location=(-0.18, 0.47, 2.12))
    pupil_left = bpy.context.active_object
    pupil_left.name = "Pupil_Left"
    all_objects.append(pupil_left)
    
    # Pupil kanan
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, radius=0.05, location=(0.18, 0.47, 2.12))
    pupil_right = bpy.context.active_object
    pupil_right.name = "Pupil_Right"
    all_objects.append(pupil_right)
    
    # ===== MULUT (LEBAR TERBUKA) =====
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.18, depth=0.12, location=(0, 0.38, 1.82))
    mouth = bpy.context.active_object
    mouth.name = "Mouth"
    mouth.rotation_euler = (radians(90), 0, 0)
    mouth.scale = (1.0, 0.7, 1.0)
    all_objects.append(mouth)
    
    # Gigi atas
    teeth_upper = []
    for i in range(5):
        x = (i - 2) * 0.08
        bpy.ops.mesh.primitive_cube_add(size=0.06, location=(x, 0.42, 1.88))
        tooth = bpy.context.active_object
        tooth.name = f"Tooth_Upper_{i}"
        tooth.scale = (0.6, 0.4, 1.2)
        teeth_upper.append(tooth)
        all_objects.append(tooth)
    
    # Gigi bawah
    teeth_lower = []
    for i in range(5):
        x = (i - 2) * 0.08
        bpy.ops.mesh.primitive_cube_add(size=0.06, location=(x, 0.42, 1.76))
        tooth = bpy.context.active_object
        tooth.name = f"Tooth_Lower_{i}"
        tooth.scale = (0.6, 0.4, 1.2)
        teeth_lower.append(tooth)
        all_objects.append(tooth)
    
    # ===== LENGAN (PENDEK GEMUK) =====
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.16, depth=0.7, location=(-0.82, 0, 1.4))
    arm_left = bpy.context.active_object
    arm_left.name = "Arm_Left"
    arm_left.rotation_euler = (0, radians(-25), 0)
    bpy.ops.object.shade_smooth()
    all_objects.append(arm_left)
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.18, location=(-1.05, 0, 1.1))
    hand_left = bpy.context.active_object
    hand_left.name = "Hand_Left"
    hand_left.scale = (1.1, 0.9, 0.8)
    all_objects.append(hand_left)
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.16, depth=0.7, location=(0.82, 0, 1.4))
    arm_right = bpy.context.active_object
    arm_right.name = "Arm_Right"
    arm_right.rotation_euler = (0, radians(25), 0)
    bpy.ops.object.shade_smooth()
    all_objects.append(arm_right)
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.18, location=(1.05, 0, 1.1))
    hand_right = bpy.context.active_object
    hand_right.name = "Hand_Right"
    hand_right.scale = (1.1, 0.9, 0.8)
    all_objects.append(hand_right)
    
    # ===== KAKI (PENDEK TEBAL) =====
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.22, depth=0.8, location=(-0.4, 0, 0.4))
    leg_left = bpy.context.active_object
    leg_left.name = "Leg_Left"
    bpy.ops.object.shade_smooth()
    all_objects.append(leg_left)
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.24, location=(-0.4, 0.15, 0.0))
    foot_left = bpy.context.active_object
    foot_left.name = "Foot_Left"
    foot_left.scale = (1.0, 1.4, 0.6)
    all_objects.append(foot_left)
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.22, depth=0.8, location=(0.4, 0, 0.4))
    leg_right = bpy.context.active_object
    leg_right.name = "Leg_Right"
    bpy.ops.object.shade_smooth()
    all_objects.append(leg_right)
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.24, location=(0.4, 0.15, 0.0))
    foot_right = bpy.context.active_object
    foot_right.name = "Foot_Right"
    foot_right.scale = (1.0, 1.4, 0.6)
    all_objects.append(foot_right)
    
    # ===== MATERIALS =====
    mat_fur = make_material("Genderuwo_Fur", base_color=(0.2, 0.25, 0.65, 1), roughness=0.9)
    mat_eye = make_material("Genderuwo_Eye", base_color=(1.0, 0.1, 0.1, 1), emission_strength=2.0, roughness=0.3)
    mat_pupil = make_material("Genderuwo_Pupil", base_color=(0.05, 0.05, 0.05, 1), roughness=0.4)
    mat_mouth = make_material("Genderuwo_Mouth", base_color=(0.15, 0.05, 0.08, 1), roughness=0.8)
    mat_teeth = make_material("Genderuwo_Teeth", base_color=(0.95, 0.95, 0.9, 1), roughness=0.5)
    
    # Assign materials
    assign_material(body, mat_fur)
    assign_material(head, mat_fur)
    
    assign_material(eye_left, mat_eye)
    assign_material(eye_right, mat_eye)
    assign_material(pupil_left, mat_pupil)
    assign_material(pupil_right, mat_pupil)
    
    assign_material(mouth, mat_mouth)
    for tooth in teeth_upper + teeth_lower:
        assign_material(tooth, mat_teeth)
    
    assign_material(arm_left, mat_fur)
    assign_material(arm_right, mat_fur)
    assign_material(hand_left, mat_fur)
    assign_material(hand_right, mat_fur)
    
    assign_material(leg_left, mat_fur)
    assign_material(leg_right, mat_fur)
    assign_material(foot_left, mat_fur)
    assign_material(foot_right, mat_fur)
    
    # ===== PARENTING =====
    root = add_empty_at("GenderuwoRoot", (0, 0, 0))
    for obj in all_objects:
        obj.parent = root
    
    return root


def main(filepath_fbx=None):
    reset_scene()
    set_units_metric(1.0)
    build_genderuwo()
    if filepath_fbx:
        export_fbx(filepath_fbx)
    print("Genderuwo generated.")


if __name__ == "__main__":
    main(filepath_fbx=None)
