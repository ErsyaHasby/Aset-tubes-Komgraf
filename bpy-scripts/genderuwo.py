import bpy
import math

# Coba import helper; kalau gagal, jalankan dari Text datablock
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


def build_body():
    """Tubuh utama tinggi dan agak ramping seperti siluet genderuwo."""
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=20,
        radius=0.6,
        depth=2.6,
        location=(0, 0, 1.3),
    )
    body = bpy.context.active_object
    body.name = "Body"
    # Sedikit lebih lebar ke samping, tapi tetap tinggi
    body.scale = (1.2, 0.9, 1.0)
    bpy.ops.object.shade_smooth()
    return body


def build_head():
    """Kepala bulat di atas badan, tidak tenggelam."""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0.05, 3.1))
    head = bpy.context.active_object
    head.name = "Head"
    head.scale = (0.9, 0.9, 1.0)
    bpy.ops.object.shade_smooth()
    return head


def build_arms_and_legs():
    parts = []
    # Lengan: panjang, turun sampai mendekati lutut dan menempel badan
    for side in (-1, 1):
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=0.15,
            depth=2.2,
            location=(side * 0.9, 0, 2.0),
        )
        arm = bpy.context.active_object
        arm.name = f"Arm_{'L' if side < 0 else 'R'}"
        arm.rotation_euler = (math.radians(-10), 0, math.radians(4 * side))
        bpy.ops.object.shade_smooth()

        # Tidak ada bentuk tangan khusus, cukup lengan panjang saja
        parts.append(arm)

    # Kaki: lurus menopang badan tinggi
    for side in (-1, 1):
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=0.24,
            depth=1.8,
            location=(side * 0.45, 0, 0.9),
        )
        leg = bpy.context.active_object
        leg.name = f"Leg_{'L' if side < 0 else 'R'}"
        bpy.ops.object.shade_smooth()

        bpy.ops.mesh.primitive_cube_add(size=0.45, location=(side * 0.45, 0.35, 0.0))
        foot = bpy.context.active_object
        foot.name = f"Foot_{'L' if side < 0 else 'R'}"
        foot.scale = (1.2, 1.6, 0.35)

        parts.extend([leg, foot])

    return parts


def build_face_features():
    parts = []
    # Mata merah kecil di kepala
    for side in (-1, 1):
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.06,
            location=(side * 0.18, 0.4, 3.15),
        )
        eye = bpy.context.active_object
        eye.name = f"Eye_{'L' if side < 0 else 'R'}"
        parts.append(eye)

    # Mulut gelap di bawah mata
    bpy.ops.mesh.primitive_cube_add(size=0.2, location=(0, 0.35, 2.9))
    mouth = bpy.context.active_object
    mouth.name = "Mouth"
    mouth.scale = (1.2, 0.4, 0.5)
    parts.append(mouth)

    # Dua taring putih turun dari mulut
    for side in (-1, 1):
        bpy.ops.mesh.primitive_cone_add(
            radius1=0.04,
            radius2=0.01,
            depth=0.5,
            location=(side * 0.1, 0.33, 2.7),
        )
        tusk = bpy.context.active_object
        tusk.name = f"Tusk_{'L' if side < 0 else 'R'}"
        tusk.rotation_euler = (math.radians(-80), 0, 0)
        parts.append(tusk)

    return parts


def build_genderuwo():
    # Siapkan scene dan unit
    reset_scene()
    set_units_metric(1.0)

    # Buat material bulu hitam dan mata merah dengan util bawaan
    fur_mat = make_material("Genderuwo_Fur", base_color=(0.05, 0.05, 0.05, 1), roughness=0.9)
    eye_mat = make_material("Genderuwo_Eye", base_color=(1.0, 0.1, 0.1, 1), emission_strength=4.0, roughness=0.2)
    tusk_mat = make_material("Genderuwo_Tusk", base_color=(0.95, 0.95, 0.9, 1), roughness=0.4)

    body = build_body()
    head = build_head()
    limbs = build_arms_and_legs()
    face_parts = build_face_features()

    # Assign materials
    for obj in [body, head] + limbs:
        assign_material(obj, fur_mat)

    for obj in face_parts:
        if obj.name.startswith("Eye"):
            assign_material(obj, eye_mat)
        elif obj.name.startswith("Tusk"):
            assign_material(obj, tusk_mat)
        else:
            assign_material(obj, fur_mat)

    # Root empty sebagai parent untuk export ke Roblox
    root = add_empty_at("GenderuwoRoot", (0, 0, 0))
    for obj in [body, head] + limbs + face_parts:
        obj.parent = root

    return root


def main(filepath_fbx=None):
    root = build_genderuwo()
    if filepath_fbx:
        export_fbx(filepath_fbx)
    print("Genderuwo generated.")


if __name__ == "__main__":
    # Saat dijalankan dari Scripting tab, biasanya tanpa export otomatis
    main(filepath_fbx=None)
