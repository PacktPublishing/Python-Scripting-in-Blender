
bl_info = {
    "name": "Action to Range",
    "author": "John Packt",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "location": "Timeline > View > Action to Scene Range",
    "description": "Transfer Action Duration to Scene Range",
    "category": "Learning",
}


import bpy


class ActionToSceneRange(bpy.types.Operator):
    """Set Playback range to current action Start/End"""
    bl_idname = "anim.action_to_range"
    bl_label = "Action to Scene Range"
    bl_description = "Transfer action range to scene range"
    bl_options = {'REGISTER', 'UNDO'}

    use_preview: bpy.props.BoolProperty(default=False)

    @classmethod
    def poll(cls, context):
        obj = context.object

        if not obj:
            return False
        if not obj.animation_data:
            return False
        if not obj.animation_data.action:
            return False

        return True

    def execute(self, context):
        first, last = context.object.animation_data.action.frame_range

        scn = context.scene

        scn.use_preview_range = self.use_preview
        if self.use_preview:
            scn.frame_preview_start = int(first)
            scn.frame_preview_end = int(last)
        else:
            scn.frame_start = int(first)
            scn.frame_end = int(last)

        try:
            bpy.ops.action.view_all()
        except RuntimeError:
            # we are not in the timeline context
            for window in context.window_manager.windows:
                screen = window.screen
                for area in screen.areas:
                    if area.type != 'DOPESHEET_EDITOR':
                        continue
                    for region in area.regions:
                        if region.type == 'WINDOW':
                            with context.temp_override(window=window,
                                                        area=area,
                                                        region=region):
                                bpy.ops.action.view_all()
                            break
                    break
    
        return {'FINISHED'}


def menu_func(self, context):
    props = self.layout.operator(ActionToSceneRange.bl_idname,
                                 text=ActionToSceneRange.bl_label + " (preview)")
    props.use_preview = True

    props = self.layout.operator(ActionToSceneRange.bl_idname,
                                 text=ActionToSceneRange.bl_label)
    props.use_preview = False


def register():
    bpy.utils.register_class(ActionToSceneRange)
    bpy.types.TIME_MT_view.append(menu_func)

def unregister():
    bpy.types.TIME_MT_view.remove(menu_func)
    bpy.utils.unregister_class(ActionToSceneRange)
