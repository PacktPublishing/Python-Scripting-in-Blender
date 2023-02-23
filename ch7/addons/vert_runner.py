
bl_info = {
    "name": "Vert Runner",
    "author": "John Packt",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "location": "Object > Animation > Vert Runner",
    "description": "Run over vertices of the active object",
    "category": "Learning",
}


import bpy
from math import asin, pi


class VertRunner(bpy.types.Operator):
    """Run over the vertices of the active object"""
    bl_idname = "object.vert_runner"
    bl_label = "Vertex Runner"
    bl_description = "Animate along vertices of active object"
    bl_options = {'REGISTER', 'UNDO'}

    step: bpy.props.IntProperty(default=12)
    loop: bpy.props.BoolProperty(default=True)

    @classmethod
    def poll(cls, context):
        obj = context.object

        if not obj:
            return False

        if not obj.type == 'MESH':
            return False
        
        if not len(context.selected_objects) > 1:
            return False

        return True

    def aim_to_point(self, ob, target_co):
        direction = target_co - ob.location
        direction.normalize()

        arc = asin(direction.y)
        if direction.x < 0:
            arc = pi - arc
        
        arc += pi / 2
        arcs = (arc, arc + 2*pi, arc - 2*pi)

        diffs = [abs(ob.rotation_euler.z - a) for a in arcs]
        shortest = min(diffs)

        res = next(a for i, a in enumerate(arcs) if diffs[i] == shortest)
        ob.rotation_euler.z = res

    def execute(self, context):
        verts = list(context.object.data.vertices)
        
        if self.loop:
            verts.append(verts[0])

        for ob in context.selected_objects:
            if ob == context.active_object:
                continue      

            # move to last position to orient towards first vertex
            ob.location = context.object.data.vertices[-1].co

            frame = context.scene.frame_current
            for vert in verts:                
                # orient towards destination before moving the object
                self.aim_to_point(ob, vert.co)
                ob.keyframe_insert('rotation_euler', frame=frame, index=2)

                ob.location = vert.co
                ob.keyframe_insert('location', frame=frame)

                frame += self.step
 
        return {'FINISHED'}


def anim_menu_func(self, context):
    self.layout.separator()
    self.layout.operator(VertRunner.bl_idname,
                         text=VertRunner.bl_label)

def register():
    bpy.utils.register_class(VertRunner)
    bpy.types.VIEW3D_MT_object_animation.append(anim_menu_func)  #TODO: header button

def unregister():
    bpy.types.VIEW3D_MT_object_animation.remove(anim_menu_func)
    bpy.utils.unregister_class(VertRunner)
