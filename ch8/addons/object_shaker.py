
bl_info = {
    "name": "Object Shaker",
    "author": "John Packt",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "description": "Add Shaky motion to active object",
    "category": "Learning",
}


import bpy


class ObjectShaker(bpy.types.Operator):
    """Set Playback range to current action Start/End"""
    bl_idname = "object.shaker_animation"
    bl_label = "Add Object Shake"
    bl_description = "Add Shake Motion to Active Object"
    bl_options = {'REGISTER', 'UNDO'}

    duration: bpy.props.FloatProperty(default=1.0, min=0.0)
    strenght: bpy.props.FloatProperty(default=1.0, soft_min=0.0, soft_max=1.0)

    @classmethod
    def poll(cls, context):
        obj = context.object

        if not obj:
            return False
        
        return True 

    def get_fcurve(self, context, data_path, index):
        action = context.object.animation_data.action

        try:
            crv = action.fcurves.new(data_path, index=index)
        except RuntimeError:
            crv = next((fc for fc in action.fcurves
                       if fc.data_path == data_path and fc.array_index == index),
                       None)
        
        if not crv.keyframe_points:
            crv.keyframe_points.insert(frame=context.scene.frame_current,
                                       value=getattr(context.object, data_path)[index])
        
        return crv

    def execute(self, context):
        # create animation data if there is none
        if not context.object.animation_data:
            anim_data = context.object.animation_data_create()
        else:
            anim_data = context.object.animation_data
        
        # create action if there is none
        if not anim_data.action:
            action = bpy.data.actions.new('ShakeMotion')
            anim_data.action = action
        else:
            action = anim_data.action
        
        z_loc_crv = self.get_fcurve(context, 'location', index=2)
        y_rot_crv = self.get_fcurve(context, 'rotation_euler', index=1)
        x_rot_crv = self.get_fcurve(context, 'rotation_euler', index=0)

        for crv in z_loc_crv, y_rot_crv, x_rot_crv:
            noise = crv.modifiers.new('NOISE')
            noise.use_restricted_range = True

            # NOTE: duration_frames and current could be moved before the for loop
            duration_frames = self.duration * context.scene.render.fps / 2
            current = context.scene.frame_current

            noise.frame_start =  current - duration_frames
            noise.frame_end = current + duration_frames

            noise.strength = self.strenght

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.separator()
    self.layout.operator(ObjectShaker.bl_idname)


def register():
    bpy.utils.register_class(ObjectShaker)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)
    bpy.utils.unregister_class(ObjectShaker)
