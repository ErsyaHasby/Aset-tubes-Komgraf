# Utility helpers for Blender (bpy) scripting
# Run inside Blender's Python environment
import bpy
from mathutils import Vector


def reset_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for m in bpy.data.meshes:
        bpy.data.meshes.remove(m)
    for c in bpy.data.collections:
        if c.name != 'Collection':
            bpy.data.collections.remove(c)
    # Set render engine (try EEVEE_NEXT first for Blender 4.x, fallback to older versions)
    try:
        bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
    except TypeError:
        try:
            bpy.context.scene.render.engine = 'BLENDER_EEVEE'
        except TypeError:
            bpy.context.scene.render.engine = 'CYCLES'


def set_units_metric(scale_length=1.0):
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = scale_length


def make_material(name, base_color=(1, 1, 1, 1), emission_strength=0.0, metallic=0.0, roughness=0.5):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    for n in list(nodes):
        nodes.remove(n)
    out = nodes.new('ShaderNodeOutputMaterial')
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.location = (-200, 0)
    principled.inputs['Base Color'].default_value = base_color
    principled.inputs['Metallic'].default_value = metallic
    principled.inputs['Roughness'].default_value = roughness
    if emission_strength > 0.0:
        emiss = nodes.new('ShaderNodeEmission')
        emiss.location = (-200, -200)
        emiss.inputs['Color'].default_value = base_color
        emiss.inputs['Strength'].default_value = emission_strength
        mix = nodes.new('ShaderNodeAddShader')
        mix.location = (-50, -100)
        links.new(principled.outputs['BSDF'], mix.inputs[0])
        links.new(emiss.outputs['Emission'], mix.inputs[1])
        links.new(mix.outputs['Shader'], out.inputs['Surface'])
    else:
        links.new(principled.outputs['BSDF'], out.inputs['Surface'])
    return mat


def assign_material(obj, mat):
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)


def add_empty_at(name, location=(0, 0, 0)):
    empty = bpy.data.objects.new(name, None)
    empty.location = Vector(location)
    bpy.context.collection.objects.link(empty)
    return empty


def export_fbx(filepath, apply_scale='FBX_SCALE_ALL', bake_space_transform=True):
    bpy.ops.export_scene.fbx(
        filepath=filepath,
        use_selection=False,
        apply_scale_options=apply_scale,
        bake_space_transform=bake_space_transform,
        object_types={'MESH', 'EMPTY'},
        use_mesh_modifiers=True,
        add_leaf_bones=False,
        path_mode='AUTOMATIC')
