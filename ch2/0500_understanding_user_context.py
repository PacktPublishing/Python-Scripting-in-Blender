
# The following snippet adds a new scene to the current session
# and makes it active. The result is visible in the Viewport's header

import bpy
new_scene = bpy.data.scenes.new('Another Scene')
bpy.context.window.scene = new_scene

print('The current scene is', bpy.context.scene.name)


# The following snippet adds a new layer to the current session
# and makes it active. The result is visible in the Viewport header

import bpy
new_layer = bpy.context.scene.view_layers.new('My Layer')
print('New layer created:', new_layer.name)

bpy.context.window.view_layer = new_layer
print('Current layer:', bpy.context.view_layer.name)


# The following snippet can be run in blender's default scene and
# makes 'Camera' the active object in the current scene

import bpy
view_layer = bpy.context.view_layer
view_layer.objects.active = bpy.data.objects['Camera']


# The following snippet prints the names of selected objects and
#  wether they are the active object or not"""

# The expected result after pressing A in blender's default scene is:

"""
Cube is active, skipping
Light is selected
Camera is selected
"""

import bpy

for ob in bpy.context.selected_objects:
    if ob is bpy.context.object:
        print(ob.name, 'is active, skipping')
        continue
    print(ob.name, 'is selected')


# The following snippet deselect each selected object

import bpy
for ob in bpy.context.selected_objects:
    ob.select_set(False)


# The following snippet creates two view layers, one where mesh objects
# are selected and one where cameras are selected.

import bpy
m_layer = bpy.context.scene.view_layers.new('Sel_Mesh')
c_layer = bpy.context.scene.view_layers.new('Sel_Cam')

for ob in bpy.data.objects:
    ob.select_set(ob.type == 'MESH', view_layer=m_layer)
    ob.select_set(ob.type == 'CAMERA', view_layer=c_layer)
