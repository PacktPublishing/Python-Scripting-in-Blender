import bpy
from bpy import data as D
from bpy import context as C
from mathutils import *
from math import *

#~ PYTHON INTERACTIVE CONSOLE 3.9.7 (default, Oct 11 2021, 19:31:28) [MSC v.1916 64 bit (AMD64)]
#~ 
#~ Builtin Modules:       bpy, bpy.data, bpy.ops, bpy.props, bpy.types, bpy.context, bpy.utils, bgl, blf, mathutils
#~ Convenience Imports:   from mathutils import *; from math import *
#~ Convenience Variables: C = bpy.context, D = bpy.data
#~ 
bpy.ops.object.delete(use_global=False)
#~ {'FINISHED'}
#~ 

bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
#~ {'FINISHED'}
#~ 

bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 2), scale=(1, 1, 1))
#~ {'FINISHED'}
#~ 
