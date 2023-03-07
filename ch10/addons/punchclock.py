bl_info = {
    "name": "PunchClock Text",
    "author": "Packt Man",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "description": "Create a Hour/Minutes text object",
    "category": "Learning",
}


import bpy
import datetime


class PunchClock(bpy.types.Operator):
    """Create Hour/Minutes text"""
    bl_idname = "text.punch_clock"
    bl_label = "Create Hour/Minutes Text"
    bl_description = "Create Hour Minutes Text"
    bl_options = {'REGISTER', 'UNDO'}

    hour: bpy.props.IntProperty(default=0, min=0, max=23)
    mins: bpy.props.IntProperty(default=0, min=0, max=59)
    set_hours: bpy.props.BoolProperty(default=True)

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

    def draw(self, context):
        layout = self.layout
        
        row = layout.row(align=True)
        row.alignment = 'CENTER'

        row.prop(self, 'hour', text="")
        row.label(text=' :',)
        row.prop(self, 'mins', text="")

    def invoke(self, context, event):
        now = datetime.datetime.now()
        
        self.hour = now.hour
        self.mins = now.minute

        self.txt_crv = bpy.data.curves.new(type="FONT", name="TXT-hourmin")
        self.txt_obj = bpy.data.objects.new(name="Font Object", object_data=self.txt_crv)
        context.collection.objects.link(self.txt_obj)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    @staticmethod
    def range_loop(value, v_min, v_max):
        if value < v_min:
            return v_max

        if value > v_max:
            return v_min
        
        return value

    def modal(self, context, event):
        # https://docs.blender.org/api/3.3/bpy_types_enum_items/event_type_items.html

        if event.type == 'MOUSEMOVE':
            delta = event.mouse_x - event. mouse_prev_x
            delta /= 10
            delta = round(delta)
            
            if self.set_hours:
                self.hour += delta
            else:
                self.mins += delta

            self.txt_crv.body = f"{self.hour:02}:{self.mins:02}"
            
        elif event.type == 'RET':
            return {'FINISHED'}
        if event.type == 'TAB' and event.value == 'PRESS':
            self.set_hours = False if self.set_hours else True
        elif event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            if not self.set_hours:
                return {'FINISHED'}

            self.set_hours = False

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            bpy.data.objects.remove(self.txt_obj)
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def execute(self, context):
        txt_crv = bpy.data.curves.new(type="FONT", name="TXT-hourmin")
        txt_crv.body = f"{int(self.hour):02}:{int(self.mins):02}"
        txt_obj = bpy.data.objects.new(name="Font Object", object_data=txt_crv)
        context.collection.objects.link(txt_obj)

        return {'FINISHED'}




def menu_func(self, context):
    self.layout.separator()
    row = self.layout.row()
    row.operator_context = "INVOKE_DEFAULT"
    row.operator(PunchClock.bl_idname, icon='TIME')


def register():
    bpy.utils.register_class(PunchClock)
    bpy.types.VIEW3D_MT_add.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_add.remove(menu_func)
    bpy.utils.unregister_class(PunchClock)
