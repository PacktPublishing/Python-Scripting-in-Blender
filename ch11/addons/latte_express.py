
bl_info = {
    "name": "Latte Express",
    "author": "Packt Man",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "description": "Create a Lattice on the active object",
    "category": "Learning",
}


import bpy
from mathutils import Vector


class LatteExpress(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.latte_express"
    bl_label = "Create Lattice on active object"
    bl_options = {'REGISTER', 'UNDO'}

    add_subsurf: bpy.props.BoolProperty(default=True)
    subd_levels: bpy.props.IntProperty(default=2)
    grid_levels: bpy.props.IntVectorProperty(default=(3, 3, 3), min=1, subtype='XYZ')
    add_armature: bpy.props.BoolProperty(default=True)

    @classmethod
    def poll(cls, context):
        return context.active_object

    def execute(self, context):
        ob = context.object

        if self.add_subsurf:
            subdiv = ob.modifiers.new('Subdivision', 'SUBSURF')
            subdiv.levels = self.subd_levels
            subdiv.render_levels = self.subd_levels
            subdiv.subdivision_type = 'SIMPLE'

        latt_data = bpy.data.lattices.new(f"LAT-{ob.name}")
        latt_obj = bpy.data.objects.new(name=latt_data.name, object_data=latt_data)

        latt_data.points_u = self.grid_levels[0]
        latt_data.points_v = self.grid_levels[1]
        latt_data.points_w = self.grid_levels[2]

        latt_data.use_outside = True

        context.collection.objects.link(latt_obj)
        latt_obj.scale = ob.dimensions

        btm_left = min((c for c in ob.bound_box), key=sum)
        top_right = max((c for c in ob.bound_box), key=sum)

        btm_left = Vector(btm_left)
        ob_center = btm_left.lerp(top_right, 0.5)
    
        ob_translation = ob.matrix_world.to_translation()
        ob_translation += ob_center

        if not self.add_armature:
            latt_obj.location = ob_translation
        else:
            arm_data = bpy.data.armatures.new(f"ARM-{ob.name}")
            arm_obj = bpy.data.objects.new(name=arm_data.name, object_data=arm_data)
            context.collection.objects.link(arm_obj)

            latt_obj.parent = arm_obj
            arm_obj.location = ob_translation

            half_height = ob.dimensions[2]/2
            arm_obj.location[2] -= half_height
            latt_obj.location[2] += half_height

            context.view_layer.objects.active = arm_obj
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)

            grid_levels = self.grid_levels[2]
            bone_length = ob.dimensions[2] / (grid_levels - 1)

            for i in range(grid_levels):
                eb = arm_data.edit_bones.new(f"LAT_{i:02}")

                eb.head = (0, 0, i * bone_length)
                eb.tail = (0, 0, eb.head[2] + bone_length)

                rel_height = i / (grid_levels - 1)
                rel_height -= 0.5

                vert_ids = []

                for id, p in enumerate(latt_data.points):
                    p_height = p.co[2]

                    if p_height == rel_height:
                        vert_ids.append(id)
                
                vg = latt_obj.vertex_groups.new(name=eb.name)
                vg.add(vert_ids, 1.0, 'REPLACE')

            arm_mod = latt_obj.modifiers.new("Armature", "ARMATURE")
            arm_mod.object = arm_obj

            bpy.ops.object.mode_set(mode='POSE', toggle=False)

            # Create Widget
            v_cos = [
                [-0.5, 0.0, -0.5], 
                [-0.5, 0.0, 0.5], 
                [0.5, 0.0, 0.5], 
                [0.5, 0.0, -0.5]
            ]

            edges = [
                [0, 1], [1, 2], [2, 3], [3, 0]
            ]

            mesh = bpy.data.meshes.new("WDG-square")
            mesh.from_pydata(v_cos, edges, [])
            wdg_obj = bpy.data.objects.new(mesh.name, mesh)
            context.collection.objects.link(wdg_obj)

            for pb in arm_obj.pose.bones:
                pb.custom_shape = wdg_obj
                pb.custom_shape_scale_xyz[0] = ob.dimensions[0] / bone_length
                pb.custom_shape_scale_xyz[2] = ob.dimensions[1] / bone_length
            
            wdg_obj.hide_set(True)
            latt_obj.hide_set(True)

        mod = ob.modifiers.new("Lattice", "LATTICE")
        mod.object = latt_obj
        ob.select_set(False)

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
