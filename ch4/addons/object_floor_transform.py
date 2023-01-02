
bl_info = {
    "name": "Elevator",
    "author": "John Doe",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "description": "Move objects up to a minimum height",
    "category": "Object",
}


import bpy
from bpy.props import FloatProperty
from bpy.props import BoolProperty

from copy import copy


def ancestors_count(ob):
    """Return number of objects up in the hierarchy"""
    ancestors = 0
    while ob.parent:
        ancestors += 1
        ob = ob.parent

    return ancestors


def get_constraint(ob, constr_type, reuse=True):
    """Return first constraint of given type.
    If not found, a new one is created"""
    if reuse:
        for constr in ob.constraints:
            if constr.type == constr_type:
                return constr
    
    return ob.constraints.new(constr_type)


class OBJECT_OT_elevator(bpy.types.Operator):
    """Move Objects up to a certain height"""
    bl_idname = "object.pckt_floor_transform"
    bl_label = "Elevate Objects"
    bl_options = {'REGISTER', 'UNDO'}

    floor: FloatProperty(name="Floor", default=0)
    constr: BoolProperty(name="Constraints", default=False)
    reuse: BoolProperty(name="Reuse", default=True)

    @classmethod
    def poll(cls, context):
        return len(bpy.context.selected_objects) > 0

    def execute(self, context):
        if self.constr:
            for ob in context.selected_objects:
                limit = get_constraint(ob, 'LIMIT_LOCATION', self.reuse)

                limit.use_min_z = True
                limit.min_z = self.floor
            
            return {'FINISHED'}

        # affect coordinates directly
        # sort parent objects first
        selected_objects = copy(context.selected_objects)
        selected_objects.sort(key=ancestors_count)

        for ob in selected_objects:
            matrix_world = ob.matrix_world

            if matrix_world[2][3] > self.floor:
                continue    

            matrix_world[2][3] = self.floor
            # make sure next object matrix will be updated
            context.view_layer.update()

        return {'FINISHED'}


def draw_elevator_item(self, context):
    # Menu functions must accept self and context as argument
    # context is left unused in this case
    row = self.layout.row()
    row.operator(OBJECT_OT_elevator.bl_idname)


def register():
    bpy.utils.register_class(OBJECT_OT_elevator)
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_elevator_item)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_elevator)
    bpy.types.VIEW3D_MT_pose_context_menu.remove(draw_elevator_item)
