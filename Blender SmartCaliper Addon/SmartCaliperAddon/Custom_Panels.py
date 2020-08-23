import bpy

class Eng_Anno_Panel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "SmartCaliper Annotation Tool"
    bl_idname = "Eng_Annotate"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"
    #bl_context = "object"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Load Engineering Annotations")
        row = layout.row()
        row.operator('load.engineering_annotation', text="Load All")

        layout.label(text="Add Engineering Annotation")
        row = layout.row()
        row.operator('add.engineering_annotation', text="Add")

        layout.label(text="Save All Engineering Annotations")
        row = layout.row()
        row.operator('save.engineering_annotation', text="Save")


     
        
