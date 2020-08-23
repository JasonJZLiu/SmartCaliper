import bpy
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper 
from bpy.types import Operator

count = 0
obj_file_path = ''

measurement = None

class Measure(bpy.types.Operator):
    bl_idname = 'measure.dist_verts'
    bl_label = 'Measure Distance'
    def execute(self, context):
        #Must set it to Object mode in order to refresh the context.active_object
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')

        selected_verts = [v for v in bpy.context.active_object.data.vertices if v.select]

        if len(selected_verts) != 2:
            self.report({'INFO'}, 'Measure Unsuccessful!  Please select 2  vertices')
        else:
            v1 = selected_verts[0].co
            v2 = selected_verts[1].co
            distance = ((v1[0]-v2[0])**2+(v1[1]-v2[1])**2+(v1[2]-v2[2])**2)**.5
            global measurement
            measurement = distance
            print(distance)
            self.report({'INFO'}, 'Measure Successful!')
        return {'FINISHED'}

class Add_Engineering_Annotation(bpy.types.Operator):
    bl_idname = "add.engineering_annotation"
    bl_label = "Add Engineering Annotation"
    bl_description = "Add Engineering Annotation"

    def execute (self, context):
        global count
        count += 1
        vertex_flag = False
        face_flag = False

        distance = None

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')

        selected_verts = [v for v in bpy.context.active_object.data.vertices if v.select]

        if len(selected_verts) != 2:
            self.report({'INFO'}, 'Measure Unsuccessful!  Please select 2  vertices')
        else:
            vertex_flag = True
            v1 = selected_verts[0].co
            v2 = selected_verts[1].co
            distance = ((v1[0]-v2[0])**2+(v1[1]-v2[1])**2+(v1[2]-v2[2])**2)**.5
            print(distance)
            self.report({'INFO'}, 'Measure Successful!')

        selected_polygons = [f for f in bpy.context.active_object.data.polygons if f.select]
        if len(selected_polygons) != 2:
            self.report({'INFO'}, 'Measure Unsuccessful!  Please select 2  faces')
        else:
            face_flag = True
            bpy.ops.object.mode_set(mode='EDIT')
            f1 = selected_polygons[0]
            f2 = selected_polygons[1]
            #vertices corresponding to the centroid of the two faces
            v1 = [0.0, 0.0, 0.0]
            v2 = [0.0, 0.0, 0.0]
            for v in f1.vertices:
                v1[0] += bpy.context.object.data.vertices[v].co[0]
                v1[1] += bpy.context.object.data.vertices[v].co[1]
                v1[2] += bpy.context.object.data.vertices[v].co[2]
            for v in f2.vertices:
                v2[0] += bpy.context.object.data.vertices[v].co[0]
                v2[1] += bpy.context.object.data.vertices[v].co[1]
                v2[2] += bpy.context.object.data.vertices[v].co[2]
                
            v1 = [c / len(f1.vertices) for c in v1] 
            v2 = [c / len(f2.vertices) for c in v2]
            distance = ((v1[0]-v2[0])**2+(v1[1]-v2[1])**2+(v1[2]-v2[2])**2)**.5
            self.report({'INFO'}, 'Measure Successful!')

        objs = [obj for obj in bpy.data.objects if obj.type in ["MESH", "CURVE"]]
        obj =objs[0]
        rna_ui = obj.get('_RNA_UI')
        if rna_ui is None:
            obj['_RNA_UI'] = {}
            rna_ui = obj['_RNA_UI']
        
        if vertex_flag:
            name = "Annotation {} for V({},{},{}) and V({},{},{})".format(count, round(v1[0],1), round(v1[1],1), round(v1[2],1),round(v2[0],1), round(v2[1],1), round(v2[2],1))
        elif face_flag: #TODO: Implement a concise naming convention so the actual faces values are saved in the name 
            name = "Annotation {} with Face Selection".format(count)
        else:
            name = "Annotation {} without Element Selection".format(count)

        #Making sure to truncate if necessary because Blender restricts it to be less than 63 characters long 
        if len(name) > 62:
            name = name[:4]+name[10:]
            if len(name) > 62:
                name = name[:63]

        obj[name] = 0
        default_value = 1

        if distance:
            rna_ui[name] = {"description":"Intended Dim: {} | ".format(round(distance,2)),
                    "default": 0,
                    "min":0,
                    "max":1000,
                    "soft_min":0,
                    "soft_max":1000}
            distance = None
        else:
            rna_ui[name] = {"description":"Missing Intended Dim | ",
                    "default": 0,
                    "min":0,
                    "max":1000,
                    "soft_min":0,
                    "soft_max":1000}

        return {'FINISHED'}



class Load_Engineering_Annotations(bpy.types.Operator):
    bl_idname = "load.engineering_annotation"
    bl_label = "Load All Engineering Annotations"
    bl_description = "Load All Engineering Annotations"

    filepath = bpy.props.StringProperty(subtype="FILE_PATH") 
    #somewhere to remember the address of the file

    filter_glob: StringProperty( 
        default='*.obj', 
        options={'HIDDEN'} 
    )
    
    def execute(self, context):
        global obj_file_path
        display = self.filepath          
        file_loc = display
        obj_file_path = display

        imported_object = bpy.ops.import_scene.obj(filepath=file_loc)
        obj_object = bpy.context.selected_objects[0]
        bpy.context.view_layer.objects.active = obj_object
        bpy.ops.object.mode_set(mode='EDIT')

        if load_annotations(obj_file_path) != -1:
            key_list, default_list, value_list, description_list = load_annotations(obj_file_path)
            global count

            if (len(key_list) == 0):
                count = 0
            else:
                count_list = [int(x.split()[1]) for x in key_list]
                count = max(count_list)


            objs = [obj for obj in bpy.data.objects if obj.type in ["MESH", "CURVE"]]
            obj = objs[0]
            rna_ui = obj.get('_RNA_UI')
            if rna_ui is None:
                obj['_RNA_UI'] = {}
                rna_ui = obj['_RNA_UI']

            for i in range(len(key_list)):
                name = key_list[i]
                obj[name] = value_list[i]
                rna_ui[name] = {"description": description_list[i],
                    "default": 0,
                    "min":0,
                    "max":1000,
                    "soft_min":0,
                    "soft_max":1000
                }

        return {'FINISHED'}

    def invoke(self, context, event): # See comments at end  [1]
        context.window_manager.fileselect_add(self) 
        #Open browser, take reference to 'self' 
        #read the path to selected file, 
        #put path in declared string type data structure self.filepath

        return {'RUNNING_MODAL'}  
        # Tells Blender to hang on for the slow user input

class Save_Engineering_Annotation(bpy.types.Operator):
    bl_idname = "save.engineering_annotation"
    bl_label = "Save All Engineering Annotations"
    bl_description = "Save All Engineering Annotations"

    def execute (self, context):
        objs = [obj for obj in bpy.data.objects if obj.type in ["MESH", "CURVE"]]

        obj = objs[0]
        rna_ui = obj.get('_RNA_UI')

        key_list = []
        description_list = []
        default_list = []
        value_list = []
        temp_count = 0
    
        for key in list(rna_ui.keys()):
            key_list.append(key)
            description_list.append(rna_ui[key]['description'])
            #not using default tab until the rounding issue is fixed by Blender
            #default_list.append(rna_ui[key]['default'])
            value_list.append(obj[key])
            temp_count += 1
        write_annotations(obj_file_path, description_list, default_list, value_list, key_list)

        return {'FINISHED'}

def write_annotations(file_name, description_list, default_list, value_list, key_list):
    obj_file = open(file_name, 'r')
    contents = obj_file.readlines()
    #count the number of lines before a non-comment line
    count = 0
    for line in contents:
        if line[0] == '#':
            count += 1
        else:
            break
    #getting rid of any previous comments
    contents = contents[count:]
    obj_file.close()
    assert(len(description_list) == len(value_list) == len(key_list))
    obj_file = open(file_name, 'w')
    obj_file.write('###SmartCapliper Comment###\n')
    for i in range(len(description_list)):
        key = key_list[i]
        '''
        v1_index = description.index('V')+1
        v2_index = description.index('V', v1_index+3)+1
        v1 = description[v1_index:description.index(')', v1_index)+1]
        v2 = description[v2_index:description.index(')', v2_index)+1]
        '''
        obj_file.write('#{}\t{}\t{}\n'.format(key, str(value_list[i]), description_list[i]))
    #adding back vertex info
    for line in contents:
        obj_file.write(line)
    obj_file.close()

def load_annotations(file_name):
    obj_file = open(file_name, 'r')
    contents = obj_file.readlines()
    if '###SmartCapliper Comment###' not in contents[0]:
        return -1
    else:
        description_list = []
        default_list = []
        value_list = []
        key_list = []
        for line in contents:
            if line[0] == '#' and line[1] != '#':
                line_str_list = line.split('\t')
                description_list.append(line_str_list[0][1:])
                #default_list.append(line_str_list[1])
                value_list.append(line_str_list[1])
                key_list.append(line_str_list[2].strip())
    obj_file.close()
    return (description_list, default_list, value_list, key_list)
