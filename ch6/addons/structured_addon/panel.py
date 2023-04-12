import bpy
from . import img_loader
from . import operators


class OBJECT_PT_structured(bpy.types.Panel):
    """Creates a Panel in the object context of the properties editor"""
    bl_label = "A Modular Panel"
    bl_idname = "MODULAR_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'


    def draw(self, context):
        layout = self.layout
        icons = img_loader.get_icons_collection()

        row = layout.row(align=True)
        row.label(text="Scene Objects", icon_value=icons['pack_64'].icon_id)
        row.label(text="", icon_value=icons["smile_64"].icon_id)

        grid = layout.grid_flow(columns=2, row_major=True)        
        add_on = context.preferences.addons[__package__]
        preferences = add_on.preferences

        for i, ob in enumerate(context.scene.objects):
            if i >= preferences.max_objects:
                grid.label(text="...")
                break

            grid.label(text=ob.name, icon=f'OUTLINER_OB_{ob.type}')
        
        layout.operator(operators.TRANSFORM_OT_random_location.bl_idname)



def register_classes():
    bpy.utils.register_class(OBJECT_PT_structured)


def unregister_classes():
    bpy.utils.unregister_class(OBJECT_PT_structured)
