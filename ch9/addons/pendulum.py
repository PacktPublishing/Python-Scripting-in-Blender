
bl_info = {
    "name": "Object Pendulum",
    "author": "John Packt",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "description": "Add swing motion to active object",
    "category": "Learning",
}


import bpy


class ObjectPendulum(bpy.types.Operator):
    """Set Playback range to current action Start/End"""
    bl_idname = "object.shaker_animation"
    bl_label = "Make Pendulum"
    bl_description = "Add swinging motion to Active Object"
    bl_options = {'REGISTER', 'UNDO'}

    amplitude: bpy.props.FloatProperty(default=0.25, min=0.0)
    length: bpy.props.FloatProperty(default=5.0, min=0.0)

    @classmethod
    def poll(cls, context):
        obj = context.object

        if not obj:
            return False
        
        return True 

    def execute(self, context):
        ob = context.object

        # create pivot point
        pivot = bpy.data.objects.new(f"EMP-{ob.name}_pivot", None)
        context.collection.objects.link(pivot)

        # move pivot upwards
        pivot.matrix_world = ob.matrix_world
        pivot.matrix_world[2][3] += self.length

        # add amplitude attr
        pivot['amplitude'] = self.amplitude

        constr = ob.constraints.new('PIVOT')
        constr.target = pivot
        constr.rotation_range = 'ALWAYS_ACTIVE'

        drv_crv = ob.driver_add('rotation_euler', 0)
        driver = drv_crv.driver
        driver.type = 'SCRIPTED'
        driver.expression = 'sin(frame / fps / sqrt(length/9.8)) * amp * pi'

        # add fps var
        fps = driver.variables.new()
        fps.name = 'fps'
        fps.targets[0].id_type = 'SCENE'
        fps.targets[0].id = context.scene
        fps.targets[0].data_path = 'render.fps'

        # add length var
        len = driver.variables.new()
        len.name = 'length'
        len.type = 'LOC_DIFF'
        len.targets[0].id = pivot
        len.targets[1].id = ob
        
        # add amplitude var
        amp = driver.variables.new()
        amp.name = 'amp'
        amp.targets[0].id_type = 'OBJECT'
        amp.targets[0].id = pivot
        amp.targets[0].data_path = '["amplitude"]'

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.separator()
    self.layout.operator(ObjectPendulum.bl_idname)


def register():
    bpy.utils.register_class(ObjectPendulum)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)
    bpy.utils.unregister_class(ObjectPendulum)
