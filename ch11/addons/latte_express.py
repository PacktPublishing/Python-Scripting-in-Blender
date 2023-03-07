import bpy

bl_info = {
    "name": "Latte Express",
    "author": "Packt Man",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "description": "Create a Lattice for selected objects",
    "category": "Learning",
}



class LatteExpress(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.latte_express"
    bl_label = "Create Lattice for selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    # TODO: subdiv
    # TODO: u, v, w

    @classmethod
    def poll(cls, context):
        return context.active_object

    def execute(self, context):
        
        ob = context.object
        latt_data = bpy.data.lattices.new(f"LAT-{ob.name}")

        latt_data.points_u = 3
        latt_data.points_v = 3
        latt_data.points_w = 3

        latt_obj = bpy.data.objects.new(name=latt_data.name, object_data=latt_data)
        context.collection.objects.link(latt_obj)

        latt_obj.location = ob.matrix_world.to_translation()
        latt_obj.scale = ob.dimensions / 2

        mod = ob.modifiers.new("Lattice", 'LATTICE')
        mod.object = latt_obj

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(LatteExpress.bl_idname,
                         icon="MOD_LATTICE")


def register():
    bpy.utils.register_class(LatteExpress)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)

def unregister():
    bpy.utils.unregister_class(LatteExpress)
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)
