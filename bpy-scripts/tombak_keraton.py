# Tombak Keraton - Tower Defense Asset
# Bentuk tombak tradisional seperti referensi
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


def build_tombak():
    """Bangun tombak tradisional seperti referensi."""
    
    all_objects = []
    
    # ===== GAGANG BAWAH (KAYU COKLAT) =====
    # Bagian bawah gagang - kayu panjang
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.04, depth=1.8, location=(0, 0, 0.9))
    shaft_lower = bpy.context.active_object
    shaft_lower.name = "Shaft_Lower"
    all_objects.append(shaft_lower)
    
    # ===== GAGANG TENGAH (PUTIH/PERAK) =====
    # Bagian tengah - lapisan putih/perak
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.045, depth=0.8, location=(0, 0, 2.2))
    shaft_middle = bpy.context.active_object
    shaft_middle.name = "Shaft_Middle"
    all_objects.append(shaft_middle)
    
    # ===== CINCIN PENGHUBUNG =====
    # Cincin bawah (antara kayu dan putih)
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.055, depth=0.08, location=(0, 0, 1.78))
    ring_lower = bpy.context.active_object
    ring_lower.name = "Ring_Lower"
    all_objects.append(ring_lower)
    
    # Cincin atas (antara putih dan kepala)
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.055, depth=0.08, location=(0, 0, 2.62))
    ring_upper = bpy.context.active_object
    ring_upper.name = "Ring_Upper"
    all_objects.append(ring_upper)
    
    # ===== KEPALA TOMBAK =====
    # Dudukan kepala (hitam/gelap)
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.06, depth=0.12, location=(0, 0, 2.72))
    head_base = bpy.context.active_object
    head_base.name = "Head_Base"
    all_objects.append(head_base)
    
    # Cincin dekoratif di dudukan
    bpy.ops.mesh.primitive_torus_add(major_segments=16, minor_segments=8, major_radius=0.07, minor_radius=0.015, location=(0, 0, 2.68))
    head_ring1 = bpy.context.active_object
    head_ring1.name = "Head_Ring1"
    all_objects.append(head_ring1)
    
    bpy.ops.mesh.primitive_torus_add(major_segments=16, minor_segments=8, major_radius=0.07, minor_radius=0.015, location=(0, 0, 2.76))
    head_ring2 = bpy.context.active_object
    head_ring2.name = "Head_Ring2"
    all_objects.append(head_ring2)
    
    # ===== SAYAP/WING TOMBAK =====
    # Sayap kiri
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.18, radius2=0.0, depth=0.25, location=(-0.12, 0, 2.88))
    wing_left = bpy.context.active_object
    wing_left.name = "Wing_Left"
    wing_left.rotation_euler = (0, radians(-90), 0)
    wing_left.scale = (1.0, 0.15, 1.0)
    all_objects.append(wing_left)
    
    # Sayap kanan
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.18, radius2=0.0, depth=0.25, location=(0.12, 0, 2.88))
    wing_right = bpy.context.active_object
    wing_right.name = "Wing_Right"
    wing_right.rotation_euler = (0, radians(90), 0)
    wing_right.scale = (1.0, 0.15, 1.0)
    all_objects.append(wing_right)
    
    # ===== MATA TOMBAK (UJUNG LANCIP) =====
    # Bagian bawah mata tombak (diamond shape)
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.1, radius2=0.02, depth=0.2, location=(0, 0, 2.88))
    blade_lower = bpy.context.active_object
    blade_lower.name = "Blade_Lower"
    blade_lower.scale = (1.0, 0.2, 1.0)
    all_objects.append(blade_lower)
    
    # Bagian atas mata tombak (ujung lancip)
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.08, radius2=0.0, depth=0.45, location=(0, 0, 3.22))
    blade_upper = bpy.context.active_object
    blade_upper.name = "Blade_Upper"
    blade_upper.scale = (1.0, 0.2, 1.0)
    all_objects.append(blade_upper)
    
    # ===== MATERIALS =====
    mat_wood = make_material("Tombak_Wood", base_color=(0.45, 0.3, 0.18, 1), roughness=0.75)
    mat_white = make_material("Tombak_White", base_color=(0.85, 0.85, 0.82, 1), roughness=0.5)
    mat_metal_dark = make_material("Tombak_MetalDark", base_color=(0.15, 0.15, 0.18, 1), metallic=0.6, roughness=0.4)
    mat_bronze = make_material("Tombak_Bronze", base_color=(0.55, 0.4, 0.3, 1), metallic=0.7, roughness=0.35)
    
    # Assign materials
    assign_material(shaft_lower, mat_wood)
    assign_material(shaft_middle, mat_white)
    
    assign_material(ring_lower, mat_metal_dark)
    assign_material(ring_upper, mat_metal_dark)
    
    assign_material(head_base, mat_metal_dark)
    assign_material(head_ring1, mat_metal_dark)
    assign_material(head_ring2, mat_metal_dark)
    
    assign_material(wing_left, mat_bronze)
    assign_material(wing_right, mat_bronze)
    assign_material(blade_lower, mat_bronze)
    assign_material(blade_upper, mat_bronze)
    
    # ===== PARENTING =====
    root = add_empty_at("TombakRoot", (0, 0, 0))
    for obj in all_objects:
        obj.parent = root
    
    return root


def main(filepath_fbx=None):
    reset_scene()
    set_units_metric(1.0)
    build_tombak()
    if filepath_fbx:
        export_fbx(filepath_fbx)
    print("Tombak Keraton generated.")


if __name__ == "__main__":
    main(filepath_fbx=None)
