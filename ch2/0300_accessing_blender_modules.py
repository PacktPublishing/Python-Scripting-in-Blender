
# The following code imports:
#
#     - the main blender functionalities, that is, bpy.
#     - bpy.data for scene and object access, and assigns it the shortcut D
#     - bpy.context for enquiring the scene status, and assigns it the shortcut C
#
# This code is executed automatically in blender's interactive console when it starts
# 

import bpy
from bpy import data as D
from bpy import context as C


# This line queries the number of objects stored in blender. The expected result
# if it is typed in the interactive console of blender's default scene is 3.

len(bpy.data.objects)


# This line gives access to the first object created in the current session.
# The expected result if it is typed in the interactive console of blender's
# default scene is bpy.data.objects['Camera']

bpy.data.objects[0]


# The following snippet prints out the name and type of the objects currently
# stored in blender. The expected results if typed in the default scene is
#
# Camera CAMERA
# Cube MESH
# Light LIGHT

import bpy
for ob in bpy.data.objects:
    print(ob.name, ob.type)


# The following snippet prints out the index, name and type of the objects
# currently stored in blender. The expected results if typed in the default
# scene's interactive console is
#
# 0 Camera CAMERA
# 1 Cube MESH
# 2 Light LIGHT

import bpy
for i, ob in enumerate(bpy.data.objects):
    print(i, ob.name, ob.type)


# The following snippet adds the letter 'z' in front of the name of the first
# object stored in the current session. The expected result if run in the
# default scene is that "Camera" is renamed to "zCamera"

import bpy
bpy.data.objects[0].name ='z' + bpy.data.objects[0].name


# The following snippet FAILS to prepend ONE "z" in front of each object's name:
# because of how blender's API works, more than 50 "z" letters are added instead

import bpy
for ob in bpy.data.objects:
    ob.name ='z' + ob.name


# The following snippet manages to add ONE "z" in front of each object's name
# by converting bpy.data.objects to a python list

import bpy
for ob in list(bpy.data.objects):
    ob.name = 'z' + ob.name


# The following lines print each object's name using the collection's search keys
for name in bpy.data.objects.keys():
    print(name)

# The following lines print each object's name and type using the collection values

for ob in bpy.data.objects.values():
    print(ob.name, ob.type)


# The following lines print each object's name and type using the collection items

for name, ob in bpy.data.objects.items():
    print(name, ob.type)
