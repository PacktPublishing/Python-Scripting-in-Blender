
bl_info = {
    "name": "Collector",
    "author": "John Doe",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "description": "Create collections for object types",
    "category": "Object",
}


import bpy


class OBJECT_OT_collector_types(bpy.types.Operator):
    """Create collections based on objects types"""
    bl_idname = "object.pckt_type_collector"
    bl_label = "Create Type Collections"

    @classmethod
    def poll(cls, context):
        return len(context.scene.objects) > 0

    @staticmethod
    def get_collection(name):
        """Returns the collection named after the given
        argument. If it doesn’t exist, a new collection
        is created and linked to the scene

        Example:

        >>> OBJECT_OT_collector_types.get_collection("Mesh")
        bpy.data.collections['Mesh']
        """

        try:
            return bpy.data.collections[name]
        except KeyError:
            cl = bpy.data.collections.new(name)
            bpy.context.scene.collection.children.link(cl)
            return cl

    def execute(self, context):
        for ob in context.scene.objects:
            cl = self.get_collection(ob.type.title())
            try:
                cl.objects.link(ob)
            except RuntimeError:
                continue

        return {'FINISHED'}


def draw_collector_item(self, context):
    # Menu functions must accept self and context as argument
    # context is left unused in this case
    row = self.layout.row()
    row.operator(OBJECT_OT_collector_types.bl_idname)


def register():
    bpy.utils.register_class(OBJECT_OT_collector_types)
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_collector_item)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_collector_types)
    bpy.types.VIEW3D_MT_pose_context_menu.remove(draw_collector_item)
