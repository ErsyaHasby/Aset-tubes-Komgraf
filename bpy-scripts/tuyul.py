import bpy
import bmesh
from mathutils import Vector
import math

# ========================================
# PEMBERSIHAN SCENE
# ========================================
def clear_scene():
    """Hapus semua objek, mesh, material, dan light di scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Bersihkan data yang tidak terpakai
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)
    for light in bpy.data.lights:
        bpy.data.lights.remove(light)

clear_scene()

# ========================================
# FUNGSI UTILITAS
# ========================================
def create_material(name):
    """Buat material baru dengan shader nodes"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    return mat

def add_subdivision(obj, levels=2):
    """Tambahkan subdivision surface modifier"""
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = levels
    subsurf.render_levels = levels
    return subsurf

def add_smooth(obj):
    """Aktifkan smooth shading"""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()

# ========================================
# MODELING TUBUH
# ========================================
def create_body():
    """Buat mesh tubuh tuyul - silinder sederhana dengan perut sedikit buncit"""
    bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=0.8, location=(0, 0, 0.6))
    body = bpy.context.active_object
    body.name = "Tuyul_Body"
    
    # Edit mode untuk membuat perut sedikit buncit
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    
    bm = bmesh.from_edit_mesh(body.data)
    
    # Scale sedikit untuk bentuk tubuh anak kecil
    for v in bm.verts:
        # Bagian tengah lebih besar (perut buncit)
        if -0.1 < v.co.z < 0.2:
            v.co.x *= 1.15
            v.co.y *= 1.15
    
    bmesh.update_edit_mesh(body.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Smooth
    add_subdivision(body, levels=2)
    add_smooth(body)
    
    return body

def create_head():
    """Buat kepala bulat besar khas tuyul dengan proporsi anak kecil"""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 1.5))
    head = bpy.context.active_object
    head.name = "Tuyul_Head"
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    
    bm = bmesh.from_edit_mesh(head.data)
    
    # Bentuk kepala: sedikit oval
    for v in bm.verts:
        v.co.z *= 1.1  # Sedikit memanjang vertikal
        v.co.y *= 0.95  # Sedikit pipih dari depan
    
    bmesh.update_edit_mesh(head.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Subdivision tinggi untuk smoothness
    add_subdivision(head, levels=3)
    add_smooth(head)
    
    return head

def create_eyes():
    """Buat mata besar bulat khas kartun dengan pupil hitam"""
    eyes = []
    pupils = []
    
    for side in [-1, 1]:
        # Bola mata putih
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(side * 0.15, 0.35, 1.55))
        eye = bpy.context.active_object
        eye.name = f"Tuyul_Eye_{['L', 'R'][side > 0]}"
        
        add_subdivision(eye, levels=2)
        add_smooth(eye)
        eyes.append(eye)
        
        # Pupil hitam
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06, location=(side * 0.15, 0.43, 1.55))
        pupil = bpy.context.active_object
        pupil.name = f"Tuyul_Pupil_{['L', 'R'][side > 0]}"
        
        add_subdivision(pupil, levels=2)
        add_smooth(pupil)
        pupils.append(pupil)
    
    return eyes, pupils

def create_nose():
    """Buat hidung kecil bulat"""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06, location=(0, 0.4, 1.35))
    nose = bpy.context.active_object
    nose.name = "Tuyul_Nose"
    nose.scale = (0.7, 1, 0.8)
    
    add_subdivision(nose, levels=2)
    add_smooth(nose)
    
    return nose

def create_mouth():
    """Buat mulut sederhana"""
    bpy.ops.mesh.primitive_cube_add(size=0.2, location=(0, 0.37, 1.15))
    mouth = bpy.context.active_object
    mouth.name = "Tuyul_Mouth"
    mouth.scale = (0.8, 0.5, 0.3)
    
    add_subdivision(mouth, levels=1)
    add_smooth(mouth)
    
    return mouth

def create_ears():
    """Buat telinga runcing seperti di gambar"""
    ears = []
    
    for side in [-1, 1]:
        # Telinga runcing (cone)
        bpy.ops.mesh.primitive_cone_add(
            radius1=0.1, 
            depth=0.25, 
            location=(side * 0.45, 0, 1.7)
        )
        ear = bpy.context.active_object
        ear.name = f"Tuyul_Ear_{['L', 'R'][side > 0]}"
        ear.rotation_euler = (0, math.radians(30 * side), math.radians(-30 * side))
        
        add_subdivision(ear, levels=2)
        add_smooth(ear)
        ears.append(ear)
    
    return ears

def create_arms():
    """Buat lengan sederhana dengan tangan bulat"""
    arms = []
    
    for side in [-1, 1]:
        # Lengan
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.08, 
            depth=0.6, 
            location=(side * 0.4, 0, 0.7)
        )
        arm = bpy.context.active_object
        arm.name = f"Tuyul_Arm_{['L', 'R'][side > 0]}"
        arm.rotation_euler = (0, 0, math.radians(10 * side))
        
        add_subdivision(arm, levels=2)
        add_smooth(arm)
        arms.append(arm)
        
        # Tangan
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.1, 
            location=(side * 0.45, 0, 0.35)
        )
        hand = bpy.context.active_object
        hand.name = f"Tuyul_Hand_{['L', 'R'][side > 0]}"
        hand.scale = (1, 1.2, 0.8)
        
        add_subdivision(hand, levels=2)
        add_smooth(hand)
        arms.append(hand)
    
    return arms

def create_legs():
    """Buat kaki pendek dan sederhana"""
    legs = []
    
    for side in [-1, 1]:
        # Kaki
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.1, 
            depth=0.4, 
            location=(side * 0.12, 0, 0)
        )
        leg = bpy.context.active_object
        leg.name = f"Tuyul_Leg_{['L', 'R'][side > 0]}"
        
        add_subdivision(leg, levels=2)
        add_smooth(leg)
        legs.append(leg)
    
    return legs

def create_pants():
    """Buat celana pendek sederhana"""
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, 0, 0.15))
    pants = bpy.context.active_object
    pants.name = "Tuyul_Pants"
    pants.scale = (0.7, 0.7, 0.3)
    
    add_subdivision(pants, levels=1)
    add_smooth(pants)
    
    return pants

# ========================================
# MATERIAL & SHADER
# ========================================
def create_skin_material():
    """Buat material kulit pucat dengan tekstur halus"""
    mat = create_material("Tuyul_Skin")
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Output node
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    # Principled BSDF
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)
    bsdf.inputs['Base Color'].default_value = (0.85, 0.82, 0.78, 1)  # Kulit pucat
    bsdf.inputs['Roughness'].default_value = 0.6
    bsdf.inputs['Subsurface'].default_value = 0.05
    bsdf.inputs['Subsurface Color'].default_value = (0.9, 0.7, 0.6, 1)
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_eye_white_material():
    """Buat material mata putih"""
    mat = create_material("Tuyul_Eye_White")
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (200, 0)
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = (1, 1, 1, 1)
    bsdf.inputs['Roughness'].default_value = 0.1
    bsdf.inputs['Specular'].default_value = 0.5
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_pupil_material():
    """Buat material pupil hitam mengkilap"""
    mat = create_material("Tuyul_Pupil")
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (200, 0)
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1)
    bsdf.inputs['Roughness'].default_value = 0.2
    bsdf.inputs['Specular'].default_value = 0.8
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_mouth_material():
    """Buat material mulut gelap"""
    mat = create_material("Tuyul_Mouth")
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (200, 0)
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = (0.2, 0.15, 0.15, 1)
    bsdf.inputs['Roughness'].default_value = 0.8
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_pants_material():
    """Buat material celana merah muda"""
    mat = create_material("Tuyul_Pants")
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (200, 0)
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = (0.9, 0.4, 0.45, 1)  # Pink/merah muda
    bsdf.inputs['Roughness'].default_value = 0.7
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_ear_material():
    """Buat material telinga dengan bagian dalam pink"""
    mat = create_material("Tuyul_Ear")
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (200, 0)
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = (0.95, 0.7, 0.75, 1)  # Pink muda
    bsdf.inputs['Roughness'].default_value = 0.5
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def apply_materials(body, head, eyes, pupils, nose, mouth, ears, arms, legs, pants):
    """Aplikasikan material ke semua objek"""
    skin_mat = create_skin_material()
    eye_white_mat = create_eye_white_material()
    pupil_mat = create_pupil_material()
    mouth_mat = create_mouth_material()
    pants_mat = create_pants_material()
    ear_mat = create_ear_material()
    
    # Kulit
    for obj in [head, nose] + arms + legs:
        if obj.data.materials:
            obj.data.materials[0] = skin_mat
        else:
            obj.data.materials.append(skin_mat)
    
    # Mata putih
    for eye in eyes:
        if eye.data.materials:
            eye.data.materials[0] = eye_white_mat
        else:
            eye.data.materials.append(eye_white_mat)
    
    # Pupil hitam
    for pupil in pupils:
        if pupil.data.materials:
            pupil.data.materials[0] = pupil_mat
        else:
            pupil.data.materials.append(pupil_mat)
    
    # Mulut
    if mouth.data.materials:
        mouth.data.materials[0] = mouth_mat
    else:
        mouth.data.materials.append(mouth_mat)
    
    # Celana
    if pants.data.materials:
        pants.data.materials[0] = pants_mat
    else:
        pants.data.materials.append(pants_mat)
    
    # Telinga
    for ear in ears:
        if ear.data.materials:
            ear.data.materials[0] = ear_mat
        else:
            ear.data.materials.append(ear_mat)
    
    # Tubuh (kulit juga)
    if body.data.materials:
        body.data.materials[0] = skin_mat
    else:
        body.data.materials.append(skin_mat)

# ========================================
# LIGHTING & ATMOSFER
# ========================================
def setup_lighting():
    """Setup pencahayaan studio sederhana"""
    
    # Sun Light utama
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    sun = bpy.context.active_object
    sun.name = "Sun_Light"
    sun.data.energy = 2.0
    sun.rotation_euler = (math.radians(45), 0, math.radians(45))
    
    # Fill light lembut
    bpy.ops.object.light_add(type='AREA', location=(-3, 3, 5))
    fill = bpy.context.active_object
    fill.name = "Fill_Light"
    fill.data.energy = 50
    fill.data.size = 3.0
    fill.rotation_euler = (math.radians(60), 0, math.radians(-45))

# ========================================
# CAMERA & RENDER SETTINGS
# ========================================
def setup_camera():
    """Setup kamera untuk framing optimal"""
    bpy.ops.object.camera_add(location=(0, -3.5, 1.2))
    camera = bpy.context.active_object
    camera.name = "Camera"
    camera.rotation_euler = (math.radians(90), 0, 0)
    
    # Set sebagai active camera
    bpy.context.scene.camera = camera
    
    # Camera settings
    camera.data.lens = 50
    camera.data.dof.use_dof = False

def setup_render_settings():
    """Pengaturan render untuk hasil optimal"""
    scene = bpy.context.scene
    
    # Engine
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 128
    scene.cycles.use_denoising = True
    
    # Resolution
    scene.render.resolution_x = 1024
    scene.render.resolution_y = 1024
    scene.render.resolution_percentage = 100
    
    # World settings (background abu-abu seperti gambar)
    world = bpy.context.scene.world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    
    # Set background color
    bg_node = nodes.get('Background')
    if bg_node:
        bg_node.inputs['Color'].default_value = (0.5, 0.5, 0.5, 1)  # Abu-abu
        bg_node.inputs['Strength'].default_value = 1.0

# ========================================
# MAIN EXECUTION
# ========================================
def create_tuyul():
    """Fungsi utama untuk membuat seluruh model tuyul"""
    print("Membuat model Tuyul stylized...")
    
    # Modeling
    print("- Membuat tubuh...")
    body = create_body()
    
    print("- Membuat kepala...")
    head = create_head()
    
    print("- Membuat mata...")
    eyes, pupils = create_eyes()
    
    print("- Membuat hidung...")
    nose = create_nose()
    
    print("- Membuat mulut...")
    mouth = create_mouth()
    
    print("- Membuat telinga...")
    ears = create_ears()
    
    print("- Membuat lengan...")
    arms = create_arms()
    
    print("- Membuat kaki...")
    legs = create_legs()
    
    print("- Membuat celana...")
    pants = create_pants()
    
    # Material
    print("- Menerapkan material...")
    apply_materials(body, head, eyes, pupils, nose, mouth, ears, arms, legs, pants)
    
    # Lighting
    print("- Setup lighting...")
    setup_lighting()
    
    # Camera & Render
    print("- Setup camera...")
    setup_camera()
    
    print("- Konfigurasi render settings...")
    setup_render_settings()
    
    print("Model Tuyul selesai dibuat!")
    print("Tekan F12 untuk render atau gunakan Viewport Shading (Z > Rendered)")

# Jalankan fungsi utama
create_tuyul()