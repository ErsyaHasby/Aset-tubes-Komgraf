import bpy
import bmesh
from mathutils import Vector, Euler
import math

# ============================================
# INISIALISASI - Bersihkan scene
# ============================================
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)
    for texture in bpy.data.textures:
        bpy.data.textures.remove(texture)

clear_scene()

# ============================================
# FUNGSI HELPER
# ============================================
def create_material(name):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    return mat

# ============================================
# MODELING - Kepala dengan Facial Features Detail
# ============================================
def create_head():
    # Buat kepala oval yang lebih realistis
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=0.5, location=(0, 0, 1.65))
    head = bpy.context.active_object
    head.name = "Head"
    head.scale = (0.88, 1.0, 1.15)
    
    bpy.ops.object.shade_smooth()
    subsurf = head.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 3
    subsurf.render_levels = 4
    
    return head

def create_facial_features():
    # MATA BESAR dengan detail
    for side in [-1, 1]:
        # Eye socket (area gelap di sekitar mata)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, 
                                            radius=0.12, 
                                            location=(side * 0.15, 0.42, 1.72))
        eye_socket = bpy.context.active_object
        eye_socket.name = f"EyeSocket_{['L', 'R'][side > 0]}"
        eye_socket.scale = (1.2, 0.7, 1.0)
        bpy.ops.object.shade_smooth()
        
        # Bola mata putih (sclera) - BESAR
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, 
                                            radius=0.09, 
                                            location=(side * 0.15, 0.48, 1.72))
        eyeball = bpy.context.active_object
        eyeball.name = f"Eyeball_{['L', 'R'][side > 0]}"
        bpy.ops.object.shade_smooth()
        
        # Iris hitam BESAR (seperti di gambar - sangat menonjol)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, 
                                            radius=0.06, 
                                            location=(side * 0.15, 0.52, 1.72))
        iris = bpy.context.active_object
        iris.name = f"Iris_{['L', 'R'][side > 0]}"
        iris.scale = (1.0, 0.4, 1.0)
        bpy.ops.object.shade_smooth()
        
        # Pupil hitam pekat
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, 
                                            radius=0.025, 
                                            location=(side * 0.15, 0.54, 1.72))
        pupil = bpy.context.active_object
        pupil.name = f"Pupil_{['L', 'R'][side > 0]}"
        pupil.scale = (1.0, 0.3, 1.0)
    
    # HIDUNG kecil dan mancung
    bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=0.055, radius2=0.025, 
                                   depth=0.18, location=(0, 0.48, 1.58))
    nose = bpy.context.active_object
    nose.name = "Nose"
    nose.rotation_euler = (math.radians(95), 0, 0)
    bpy.ops.object.shade_smooth()
    
    # MULUT - tersenyum menyeramkan dengan gigi terlihat
    bpy.ops.mesh.primitive_torus_add(major_radius=0.15, minor_radius=0.04, 
                                    location=(0, 0.46, 1.44))
    mouth = bpy.context.active_object
    mouth.name = "Mouth"
    mouth.scale = (1.3, 0.5, 0.6)
    mouth.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.shade_smooth()
    
    # GIGI - Deretan gigi atas
    teeth_count = 10
    for i in range(teeth_count):
        angle = (i - teeth_count/2) * 0.055
        x_pos = math.sin(angle) * 0.17
        y_pos = 0.46 + math.cos(angle) * 0.025
        z_pos = 1.455
        
        bpy.ops.mesh.primitive_cube_add(size=0.018, location=(x_pos, y_pos, z_pos))
        tooth = bpy.context.active_object
        tooth.name = f"Tooth_{i}"
        tooth.scale = (1.0, 0.6, 1.4)
        tooth.rotation_euler = (0, 0, angle * 0.5)
        bpy.ops.object.shade_smooth()

# ============================================
# MODELING - Leher
# ============================================
def create_neck():
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.2, depth=0.4, 
                                       location=(0, 0, 1.2))
    neck = bpy.context.active_object
    neck.name = "Neck"
    neck.scale = (0.95, 0.85, 1.0)
    bpy.ops.object.shade_smooth()
    
    subsurf = neck.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    
    return neck

# ============================================
# MODELING - Torso dan Bahu
# ============================================
def create_torso():
    # Torso atas (dada)
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.38, depth=0.65, 
                                       location=(0, 0, 0.7))
    torso = bpy.context.active_object
    torso.name = "Torso"
    torso.scale = (1.0, 0.65, 1.0)
    
    bpy.ops.object.shade_smooth()
    subsurf = torso.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    
    return torso

# ============================================
# MODELING - Lengan Realistis
# ============================================
def create_arms():
    arms = []
    
    for side in [-1, 1]:
        # Bahu
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, 
                                            radius=0.14, 
                                            location=(side * 0.42, 0, 0.9))
        shoulder = bpy.context.active_object
        shoulder.name = f"Shoulder_{['L', 'R'][side > 0]}"
        shoulder.scale = (1.2, 0.9, 1.0)
        bpy.ops.object.shade_smooth()
        arms.append(shoulder)
        
        # Upper arm (lengan atas)
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.095, depth=0.55, 
                                           location=(side * 0.52, 0, 0.55))
        upper_arm = bpy.context.active_object
        upper_arm.name = f"UpperArm_{['L', 'R'][side > 0]}"
        upper_arm.rotation_euler = (0, side * 0.12, 0)
        upper_arm.scale = (1.0, 1.0, 1.0)
        bpy.ops.object.shade_smooth()
        arms.append(upper_arm)
        
        # Elbow (siku)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, 
                                            radius=0.085, 
                                            location=(side * 0.58, 0, 0.25))
        elbow = bpy.context.active_object
        elbow.name = f"Elbow_{['L', 'R'][side > 0]}"
        bpy.ops.object.shade_smooth()
        arms.append(elbow)
        
        # Lower arm (lengan bawah)
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.08, depth=0.5, 
                                           location=(side * 0.64, 0, -0.05))
        lower_arm = bpy.context.active_object
        lower_arm.name = f"LowerArm_{['L', 'R'][side > 0]}"
        lower_arm.rotation_euler = (0, side * 0.08, 0)
        bpy.ops.object.shade_smooth()
        arms.append(lower_arm)
        
        # Hand (tangan)
        bpy.ops.mesh.primitive_cube_add(size=0.16, location=(side * 0.68, 0, -0.32))
        hand = bpy.context.active_object
        hand.name = f"Hand_{['L', 'R'][side > 0]}"
        hand.scale = (0.85, 0.55, 1.3)
        subsurf = hand.modifiers.new(name="Subdivision", type='SUBSURF')
        subsurf.levels = 2
        bpy.ops.object.shade_smooth()
        arms.append(hand)
    
    return arms

# ============================================
# MODELING - Gaun Panjang Detail (Sesuai Gambar)
# ============================================
def create_dress():
    # Gaun bagian atas (bodice) - fitted
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.42, depth=0.7, 
                                       location=(0, 0, 0.65))
    dress_top = bpy.context.active_object
    dress_top.name = "Dress_Top"
    dress_top.scale = (0.95, 0.7, 1.0)
    
    # Gaun bagian tengah
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.48, depth=0.8, 
                                       location=(0, 0, -0.1))
    dress_mid = bpy.context.active_object
    dress_mid.name = "Dress_Mid"
    dress_mid.scale = (1.0, 0.75, 1.0)
    
    # Gaun bagian bawah (skirt panjang menyentuh tanah)
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.5, depth=2.0, 
                                       location=(0, 0, -1.2))
    dress_bottom = bpy.context.active_object
    dress_bottom.name = "Dress_Bottom"
    
    # Edit bottom untuk flare
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bm = bmesh.from_edit_mesh(dress_bottom.data)
    
    for v in bm.verts:
        if v.co.z < -1.5:
            v.select = True
            v.co.x *= 2.2
            v.co.y *= 2.2
        elif v.co.z < -0.5:
            factor = 1.0 + ((-0.5 - v.co.z) / 1.0) * 1.2
            v.co.x *= factor
            v.co.y *= factor
    
    bmesh.update_edit_mesh(dress_bottom.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Join semua bagian gaun
    bpy.ops.object.select_all(action='DESELECT')
    dress_top.select_set(True)
    dress_mid.select_set(True)
    dress_bottom.select_set(True)
    bpy.context.view_layer.objects.active = dress_top
    bpy.ops.object.join()
    
    dress = bpy.context.active_object
    dress.name = "Dress"
    bpy.ops.object.shade_smooth()
    
    # Subdivision untuk smooth surface
    subsurf = dress.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 3
    
    # Displacement untuk lipatan kain yang natural
    displace = dress.modifiers.new(name="Displacement", type='DISPLACE')
    displace.strength = 0.05
    displace.mid_level = 0.5
    
    tex = bpy.data.textures.new("Cloth_Wrinkles", type='CLOUDS')
    tex.noise_scale = 1.5
    tex.noise_depth = 6
    displace.texture = tex
    
    # Tambahkan lengan gaun
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.11, depth=0.6, 
                                           location=(side * 0.52, 0, 0.55))
        sleeve = bpy.context.active_object
        sleeve.name = f"Sleeve_{['L', 'R'][side > 0]}"
        sleeve.rotation_euler = (0, side * 0.12, 0)
        bpy.ops.object.shade_smooth()
        
        subsurf_sleeve = sleeve.modifiers.new(name="Subdivision", type='SUBSURF')
        subsurf_sleeve.levels = 2
    
    return dress

# ============================================
# MATERIAL - Kulit Abu-abu Pucat (Fixed)
# ============================================
def create_skin_material():
    mat = create_material("Skin_Pale")
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (800, 0)
    
    # Principled BSDF (Blender 3.x+ compatible)
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (500, 0)
    bsdf.inputs['Base Color'].default_value = (0.72, 0.75, 0.73, 1.0)
    
    # Cek versi Blender untuk subsurface
    if 'Subsurface Weight' in bsdf.inputs:
        bsdf.inputs['Subsurface Weight'].default_value = 0.1
    elif 'Subsurface' in bsdf.inputs:
        bsdf.inputs['Subsurface'].default_value = 0.1
    
    bsdf.inputs['Roughness'].default_value = 0.6
    bsdf.inputs['Specular IOR Level'].default_value = 0.3
    
    # Noise untuk tekstur kulit
    coord = nodes.new(type='ShaderNodeTexCoord')
    coord.location = (-600, 0)
    
    noise = nodes.new(type='ShaderNodeTexNoise')
    noise.location = (-400, 0)
    noise.inputs['Scale'].default_value = 100.0
    noise.inputs['Detail'].default_value = 15.0
    
    # Color ramp untuk noda
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (-200, 0)
    color_ramp.color_ramp.elements[0].position = 0.35
    color_ramp.color_ramp.elements[0].color = (0.35, 0.38, 0.36, 1.0)
    color_ramp.color_ramp.elements[1].position = 0.65
    color_ramp.color_ramp.elements[1].color = (0.72, 0.75, 0.73, 1.0)
    
    # Mix
    mix = nodes.new(type='ShaderNodeMix')
    mix.location = (250, 0)
    mix.data_type = 'RGBA'
    mix.inputs[0].default_value = 0.25
    
    # Bump
    bump = nodes.new(type='ShaderNodeBump')
    bump.location = (250, -200)
    bump.inputs['Strength'].default_value = 0.1
    
    # Koneksi
    links.new(coord.outputs['Object'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], mix.inputs[6])
    links.new(mix.outputs[2], bsdf.inputs['Base Color'])
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

# ============================================
# MATERIAL - Eye Socket Gelap (Makeup)
# ============================================
def create_eye_socket_material():
    mat = create_material("Eye_Socket_Dark")
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)
    bsdf.inputs['Base Color'].default_value = (0.08, 0.08, 0.08, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.9
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

# ============================================
# MATERIAL - Mata Putih
# ============================================
def create_eye_white_material():
    mat = create_material("Eye_White")
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)
    bsdf.inputs['Base Color'].default_value = (0.98, 0.98, 0.96, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.3
    bsdf.inputs['Specular IOR Level'].default_value = 0.6
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

# ============================================
# MATERIAL - Iris Hitam Besar
# ============================================
def create_iris_material():
    mat = create_material("Iris_Black")
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)
    bsdf.inputs['Base Color'].default_value = (0.02, 0.02, 0.02, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.1
    bsdf.inputs['Specular IOR Level'].default_value = 0.9
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

# ============================================
# MATERIAL - Mulut
# ============================================
def create_mouth_material():
    mat = create_material("Mouth_Dark")
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)
    bsdf.inputs['Base Color'].default_value = (0.12, 0.08, 0.1, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.8
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

# ============================================
# MATERIAL - Gigi
# ============================================
def create_teeth_material():
    mat = create_material("Teeth_White")
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)
    bsdf.inputs['Base Color'].default_value = (0.92, 0.9, 0.85, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.3
    bsdf.inputs['Specular IOR Level'].default_value = 0.5
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

# ============================================
# MATERIAL - Gaun Putih Kotor
# ============================================
def create_dress_material():
    mat = create_material("Dress_Dirty")
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (900, 0)
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (600, 0)
    bsdf.inputs['Base Color'].default_value = (0.85, 0.88, 0.86, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.95
    bsdf.inputs['Sheen Weight'].default_value = 0.3
    
    # Coordinate
    coord = nodes.new(type='ShaderNodeTexCoord')
    coord.location = (-800, 0)
    
    # Noise untuk noda
    noise1 = nodes.new(type='ShaderNodeTexNoise')
    noise1.location = (-600, 0)
    noise1.inputs['Scale'].default_value = 8.0
    noise1.inputs['Detail'].default_value = 8.0
    
    # Musgrave untuk tekstur kain
    musgrave = nodes.new(type='ShaderNodeTexMusgrave')
    musgrave.location = (-600, -250)
    musgrave.inputs['Scale'].default_value = 25.0
    musgrave.inputs['Detail'].default_value = 12.0
    
    # Color ramp untuk noda
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.location = (-300, 0)
    color_ramp.color_ramp.elements[0].position = 0.3
    color_ramp.color_ramp.elements[0].color = (0.38, 0.42, 0.38, 1.0)
    color_ramp.color_ramp.elements[1].position = 0.7
    color_ramp.color_ramp.elements[1].color = (0.85, 0.88, 0.86, 1.0)
    
    # Mix
    mix = nodes.new(type='ShaderNodeMix')
    mix.location = (250, 0)
    mix.data_type = 'RGBA'
    mix.inputs[0].default_value = 0.4
    
    # Bump
    bump = nodes.new(type='ShaderNodeBump')
    bump.location = (250, -300)
    bump.inputs['Strength'].default_value = 0.2
    
    # Koneksi
    links.new(coord.outputs['Object'], noise1.inputs['Vector'])
    links.new(coord.outputs['Object'], musgrave.inputs['Vector'])
    links.new(noise1.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], mix.inputs[6])
    links.new(mix.outputs[2], bsdf.inputs['Base Color'])
    links.new(musgrave.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

# ============================================
# HAIR SYSTEM - Rambut Hitam Panjang Lebat
# ============================================
def create_hair_system(head):
    bpy.context.view_layer.objects.active = head
    head.select_set(True)
    
    # Buat vertex group untuk emission area (seluruh kepala)
    vg = head.vertex_groups.new(name="Hair_Emit")
    vertices = []
    for v in head.data.vertices:
        if v.co.z > 1.3:  # Area kepala
            vertices.append(v.index)
    vg.add(vertices, 1.0, 'ADD')
    
    # Tambahkan particle system
    bpy.ops.object.particle_system_add()
    psys = head.particle_systems[-1]
    settings = psys.settings
    
    settings.name = "Hair_Long_Black"
    settings.type = 'HAIR'
    settings.count = 30000  # Sangat lebat
    settings.hair_length = 3.2  # Sangat panjang
    settings.use_advanced_hair = True
    
    # Vertex group untuk emission
    psys.vertex_group_density = "Hair_Emit"
    
    # Child particles untuk volume
    settings.child_type = 'INTERPOLATED'
    settings.child_nbr = 15
    settings.rendered_child_count = 15
    
    # Clumping - rambut menggumpal natural
    settings.clump_factor = 0.5
    settings.clump_shape = -0.1
    
    # Roughness - rambut tidak terlalu rapi
    settings.roughness_1 = 0.35
    settings.roughness_2 = 0.25
    settings.roughness_1_size = 0.4
    settings.roughness_2_size = 0.3
    settings.roughness_endpoint = 0.3
    
    # Kink untuk slight wave
    settings.use_hair_bspline = True
    settings.kink = 'WAVE'
    settings.kink_amplitude = 0.06
    settings.kink_frequency = 2.0
    
    return psys

# ============================================
# MATERIAL - Hair Black
# ============================================
def create_hair_material():
    mat = create_material("Hair_Black")
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    hair_bsdf = nodes.new(type='ShaderNodeBsdfHairPrincipled')
    hair_bsdf.location = (200, 0)
    hair_bsdf.inputs['Color'].default_value = (0.015, 0.015, 0.015, 1.0)
    hair_bsdf.inputs['Melanin'].default_value = 1.0
    hair_bsdf.inputs['Melanin Redness'].default_value = 0.0
    hair_bsdf.inputs['Roughness'].default_value = 0.45
    hair_bsdf.inputs['Radial Roughness'].default_value = 0.35
    hair_bsdf.inputs['Coat'].default_value = 0.15
    hair_bsdf.inputs['IOR'].default_value = 1.55
    
    links.new(hair_bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

# ============================================
# LIGHTING - Studio Setup
# ============================================
def create_lighting():
    # Key light (main)
    bpy.ops.object.light_add(type='AREA', location=(3, 4.5, 4))
    key = bpy.context.active_object
    key.name = "Key_Light"
    key.data.energy = 400
    key.data.size = 5
    key.data.color = (1.0, 0.98, 0.96)
    key.rotation_euler = (math.radians(-35), 0, math.radians(-25))
    
    # Fill light
    bpy.ops.object.light_add(type='AREA', location=(-3.5, 3, 3))
    fill = bpy.context.active_object
    fill.name = "Fill_Light"
    fill.data.energy = 120
    fill.data.size = 4
    fill.data.color = (0.92, 0.94, 1.0)
    
    # Rim light
    bpy.ops.object.light_add(type='AREA', location=(0, -4, 3.5))
    rim = bpy.context.active_object
    rim.name = "Rim_Light"
    rim.data.energy = 180
    rim.data.size = 3.5
    rim.data.color = (0.96, 0.98, 1.0)

# ============================================
# CAMERA
# ============================================
def setup_camera():
    bpy.ops.object.camera_add(location=(0, -5.5, 1.3))
    camera = bpy.context.active_object
    camera.name = "Main_Camera"
    camera.rotation_euler = (math.radians(88), 0, 0)
    
    bpy.context.scene.camera = camera
    camera.data.lens = 70

# ============================================
# WORLD
# ============================================
def setup_world():
    world = bpy.context.scene.world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    nodes.clear()
    
    output = nodes.new(type='ShaderNodeOutputWorld')
    output.location = (400, 0)
    
    bg = nodes.new(type='ShaderNodeBackground')
    bg.location = (200, 0)
    bg.inputs['Color'].default_value = (0.96, 0.96, 0.96, 1.0)
    bg.inputs['Strength'].default_value = 0.9
    
    links.new(bg.outputs['Background'], output.inputs['Surface'])

def setup_render():
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 256
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.cycles.use_denoising = True

# ============================================
# MAIN EXECUTION
# ============================================
print("=== Membuat Model Kuntilanak (Sesuai Gambar) ===\n")

# 1. Kepala
print("1. Membuat kepala...")
head = create_head()

# 2. Facial features
print("2. Menambahkan wajah detail...")
create_facial_features()

# 3. Leher
print("3. Membuat leher...")
neck = create_neck()

# 4. Torso
print("4. Membuat torso...")
torso = create_torso()

# 5. Lengan
print("5. Membuat lengan...")
arms = create_arms()

# 6. Gaun
print("6. Membuat gaun panjang...")
dress = create_dress()

# 7. Materials
print("7. Menerapkan material...")
skin_mat = create_skin_material()
eye_socket_mat = create_eye_socket_material()
eye_white_mat = create_eye_white_material()
iris_mat = create_iris_material()
mouth_mat = create_mouth_material()
teeth_mat = create_teeth_material()
dress_mat = create_dress_material()

# Apply materials
head.data.materials.append(skin_mat)
neck.data.materials.append(skin_mat)
torso.data.materials.append(skin_mat)

for arm in arms:
    if len(arm.data.materials) == 0:
        arm.data.materials.append(skin_mat)

for obj in bpy.data.objects:
    if "EyeSocket_" in obj.name:
        obj.data.materials.append(eye_socket_mat)
    elif "Eyeball_" in obj.name:
        obj.data.materials.append(eye_white_mat)
    elif "Iris_" in obj.name or "Pupil_" in obj.name:
        obj.data.materials.append(iris_mat)
    elif obj.name == "Mouth":
        obj.data.materials.append(mouth_mat)
    elif "Tooth_" in obj.name:
        obj.data.materials.append(teeth_mat)
    elif obj.name == "Nose":
        if len(obj.data.materials) == 0:
            obj.data.materials.append(skin_mat)

dress.data.materials.append(dress_mat)

# Apply dress material to sleeves
for obj in bpy.data.objects:
    if "Sleeve_" in obj.name:
        obj.data.materials.append(dress_mat)

# 8. Hair system
print("8. Membuat sistem rambut (ini memakan waktu)...")
hair_psys = create_hair_system(head)
hair_mat = create_hair_material()

# Add hair material to head
head.data.materials.append(hair_mat)

# Set material slot untuk particle
for i, mat in enumerate(head.data.materials):
    if mat.name == "Hair_Black":
        hair_psys.settings.material = len(head.data.materials)
        hair_psys.settings.material_slot = mat.name
        break

# 9. Lighting
print("9. Setup pencahayaan...")
create_lighting()

# 10. Camera
print("10. Setup kamera...")
setup_camera()

# 11. World
print("11. Setup world...")
setup_world()

# 12. Render
print("12. Konfigurasi render...")
setup_render()
print("\n=== MODEL KUNTILANAK SELESAI ===")
print("✓ Wajah pucat dengan mata besar hitam")
print("✓ Rambut hitam panjang lebat")
print("✓ Gaun putih kotor panjang")
print("✓ Pose A-pose depan")
print("\nTekan F12 untuk render!")
print("Jika rambut tidak muncul, pastikan Particle Hair diaktifkan di Viewport Shading.")