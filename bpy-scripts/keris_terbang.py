# Keris Terbang - Tower Defense Asset
# Bentuk keris tradisional Jawa yang melayang di atas pedestal
# Run inside Blender setelah common_utils.py

import bpy
from math import pi, radians

# Import helpers
try:
    from common_utils import reset_scene, set_units_metric, make_material, assign_material, add_empty_at, export_fbx
except ModuleNotFoundError:
    if "common_utils.py" in bpy.data.texts:
        exec(bpy.data.texts["common_utils.py"].as_string(), globals())
    else:
        raise


def build_keris():
    """Bangun keris tradisional melayang di atas pedestal batu."""
    
    all_objects = []
    
    # ===== PEDESTAL / ALAS =====
    # Tiang penyangga saja
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.08, depth=0.8, location=(0, 0, 0.4))
    pillar = bpy.context.active_object
    pillar.name = "Pillar"
    all_objects.append(pillar)
    
    # ===== KERIS - HULU (GAGANG) =====
    # Gagang utama - bentuk silinder miring ke belakang
    bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.05, depth=0.3, location=(0, -0.06, 1.0))
    hulu = bpy.context.active_object
    hulu.name = "Hulu"
    hulu.rotation_euler = (radians(20), 0, 0)
    all_objects.append(hulu)
    
    # Kepala gagang (ukiran) - bentuk bulat
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.065, location=(0, -0.12, 1.15))
    hulu_head = bpy.context.active_object
    hulu_head.name = "Hulu_Head"
    hulu_head.scale = (0.8, 1.0, 1.1)
    all_objects.append(hulu_head)
    
    # ===== KERIS - WARANGKA (SARUNG ATAS) =====
    # Warangka bentuk lebar khas keris Jawa
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.88))
    warangka = bpy.context.active_object
    warangka.name = "Warangka"
    warangka.scale = (0.35, 0.08, 0.06)
    all_objects.append(warangka)
    
    # Ujung warangka kanan (naik ke atas)
    bpy.ops.mesh.primitive_cube_add(size=0.3, location=(0.22, 0, 0.92))
    warangka_tip = bpy.context.active_object
    warangka_tip.name = "Warangka_Tip"
    warangka_tip.scale = (0.4, 0.06, 0.05)
    warangka_tip.rotation_euler = (0, 0, radians(35))
    all_objects.append(warangka_tip)
    
    # ===== KERIS - GANDAR (SARUNG BAWAH) =====
    # Sarung bawah panjang
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.5))
    gandar = bpy.context.active_object
    gandar.name = "Gandar"
    gandar.scale = (0.055, 0.035, 0.55)
    all_objects.append(gandar)
    
    # Lapisan emas di gandar
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.022, 0.5))
    gandar_gold = bpy.context.active_object
    gandar_gold.name = "Gandar_Gold"
    gandar_gold.scale = (0.015, 0.012, 0.5)
    all_objects.append(gandar_gold)
    
    # ===== KERIS - BILAH (MATA KERIS) =====
    # Bilah utama - pipih dan lurus
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.05, 1.45))
    blade = bpy.context.active_object
    blade.name = "Blade"
    blade.scale = (0.045, 0.006, 0.45)
    all_objects.append(blade)
    
    # Pamor (garis tengah bilah)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.054, 1.45))
    pamor = bpy.context.active_object
    pamor.name = "Pamor"
    pamor.scale = (0.012, 0.004, 0.4)
    all_objects.append(pamor)
    
    # Ujung bilah lancip
    bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.045, radius2=0.0, depth=0.18, location=(0, 0.05, 1.9))
    blade_tip = bpy.context.active_object
    blade_tip.name = "Blade_Tip"
    blade_tip.scale = (1.0, 0.15, 1.0)
    all_objects.append(blade_tip)
    
    # ===== MATERIALS =====
    mat_stone = make_material("Keris_Stone", base_color=(0.3, 0.28, 0.26, 1), roughness=0.95)
    mat_wood = make_material("Keris_Wood", base_color=(0.4, 0.2, 0.1, 1), roughness=0.7)
    mat_gold = make_material("Keris_Gold", base_color=(0.85, 0.65, 0.15, 1), metallic=0.9, roughness=0.3)
    mat_blade = make_material("Keris_Blade", base_color=(0.75, 0.73, 0.7, 1), metallic=0.8, roughness=0.25)
    mat_pamor = make_material("Keris_Pamor", base_color=(0.5, 0.48, 0.45, 1), metallic=0.6, roughness=0.4)
    
    # Assign materials
    assign_material(pillar, mat_stone)
    
    assign_material(hulu, mat_wood)
    assign_material(hulu_head, mat_wood)
    
    assign_material(warangka, mat_wood)
    assign_material(warangka_tip, mat_wood)
    
    assign_material(gandar, mat_wood)
    assign_material(gandar_gold, mat_gold)
    
    assign_material(blade, mat_blade)
    assign_material(pamor, mat_pamor)
    assign_material(blade_tip, mat_blade)
    
    # ===== PARENTING =====
    root = add_empty_at("KerisRoot", (0, 0, 0))
    for obj in all_objects:
        obj.parent = root
    
    return root


def main(filepath_fbx=None):
    reset_scene()
    set_units_metric(1.0)
    build_keris()
    if filepath_fbx:
        export_fbx(filepath_fbx)
    print("Keris Terbang generated.")


if __name__ == "__main__":
    main(filepath_fbx=None)
