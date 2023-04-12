
bl_info = {
    "name": "A Very Simple Panel",
    "author": "John Doe",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "description": "Just show up a panel in the UI",
    "category": "Learning",
} 


import bpy
from bpy.utils import previews
import os
import random


# global variable for icon storage
custom_icons = None


def load_custom_icons():
    """Load icon from the add-on folder"""
    addon_path = os.path.dirname(__file__)
    img_file = os.path.join(addon_path, "icon_smile_64.png")
    global custom_icons

    custom_icons = previews.new()
    custom_icons.load("smile_face",img_file, 'IMAGE')


def clear_custom_icons():
    """Clear Icons loaded from file"""
    global custom_icons

    bpy.utils.previews.remove(custom_icons)


def add_random_location(objects, amount=1,
                        do_axis=(True, True, True)):
    """Add units to the locations of given objects"""
    for ob in objects:
        for i in range(3):
            if do_axis[i]:
                loc = ob.location
                loc[i] += random.randint(-amount, amount)


class TRANSFORM_OT_random_location(bpy.types.Operator):
    """Add units to the locations of selected objects"""
    bl_idname = "transform.add_random_location"
    bl_label = "Add random Location"

    amount: bpy.props.IntProperty(name="Amount",
                                  default=1)
    axis: bpy.props.BoolVectorProperty(
                               name="Displace Axis",
                               default=(True, True, True),
                               subtype='XYZ'
                               )

    @classmethod
    def poll(cls, context):
        return context.selected_objects

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        add_random_location(context.selected_objects,
                            self.amount,
                            self.axis)
        return {'FINISHED'}

    
class OBJECT_PT_very_simple(bpy.types.Panel):
    """Creates a Panel in the object context of the properties editor"""
    bl_label = "A Very Simple Panel"
    bl_idname = "VERYSIMPLE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'

    max_objects = 3

    def draw(self, context):
        layout = self.layout
        layout.label(text="A Very Simple Label", icon='INFO')
        layout.label(text="Isn't it great?", icon='QUESTION')
        layout.label(text="Smile", icon_value=custom_icons["smile_face"].icon_id)

        box = col.box()
        split = box.split(factor=0.33)
        left_col = split.column()
        right_col = split.column()

        for k, v in bl_info.items():
            if not v:
                # ignore empty entries
                continue

            left_col.label(text=k)
            right_col.label(text=str(v))

        col.label(text="Scene Objects:")
        grid = col.grid_flow(columns=2, row_major=True)
        for i, ob in enumerate(context.scene.objects):
            if i > self.max_objects:
                objects_left = len(context.scene.objects)
                objects_left -= self.max_objects
                grid.label(text=f"... (other {objects_left} objects)")

                break

            # layout item to set entry color
            item_layout = grid.column()
            
            item_layout.enabled = ob.select_get()
            item_layout.alert = ob == context.object
            item_layout.label(text=ob.name, icon=f'OUTLINER_OB_{ob.type}')

        num_selected = len(context.selected_objects)
        if (num_selected > 0):
            op_txt = f"Delete {num_selected} object"
            if num_selected > 1:
                op_txt += "s"  # add plural 's'
            
            props = col.operator(bpy.ops.object.delete.idname(), text=op_txt)
            props.confirm = False
        else:
            to_disable = col.column()
            to_disable.enabled = False
            to_disable.operator(bpy.ops.object.delete.idname(),
                                text="Delete Selected")
        
        col.operator(TRANSFORM_OT_random_location.bl_idname)



def register():
    load_custom_icons()
    bpy.utils.register_class(TRANSFORM_OT_random_location)
    bpy.utils.register_class(OBJECT_PT_very_simple)


def unregister():
    bpy.utils.unregister_class(OBJECT_PT_very_simple)
    bpy.utils.unregister_class(TRANSFORM_OT_random_location)
    clear_custom_icons()
