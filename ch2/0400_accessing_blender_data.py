
# The following lines create a new empty object and link it to the scene

import bpy
my_empty = bpy.data.objects.new('My Empty', None)
print('New Empty created:', my_empty)

bpy.data.collections['Collection'].objects.link(my_empty)


# The following line removes the empty created in the previous snippet

bpy.data.objects.remove(my_empty)


# The following lines work with blender's default scene and remove
# the object 'Cube' from the scene, but not from bpy.data.objects

collection = bpy.data.collections['Collection']
collection.objects.unlink(bpy.data.objects['Cube'])
