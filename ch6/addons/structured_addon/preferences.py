import bpy
from bpy.props import IntProperty


class StructuredPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    max_objects: IntProperty(
        name="Maximum number of displayed objects",
        default=3,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Panel Preferences")

        split = layout.split(factor=0.5)
        split.separator()
        split.label(text="Max Objects:")
        split.prop(self, 'max_objects', text="")


def register_classes():
    bpy.utils.register_class(StructuredPreferences)


def unregister_classes():
    bpy.utils.unregister_class(StructuredPreferences)
