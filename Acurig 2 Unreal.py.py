bl_info = {
    "name": "My Button Addon",
    "blender": (2, 80, 0),
    "category": "0 ground",
}

import bpy
from mathutils import Vector
import math



######utilities######
def get_degrees (degrees):
    radians = degrees * (math.pi / 180)
    return radians

def reset_bone_roll(armature):
    # Switch to EDIT mode
    bpy.ops.object.mode_set(mode='EDIT')

    for bone in armature.edit_bones:
        bone.roll = 0

    # Switch back to OBJECT mode
    bpy.ops.object.mode_set(mode='OBJECT')

def connect_bones(armature):
    # Switch to EDIT mode
    bpy.ops.object.mode_set(mode='EDIT')

    for bone in armature.edit_bones:
        if bone.name not in ["Hip","Eye.R","Waist","Pelvis","Thigh.R","Clavicle.R","CalfTwist01.R","ThighTwist01.R","ForearmTwist01.R","UpperarmTwist01.R","Index1.R","Thumb1.R","Middle1.R","Ring1.R","Pinky1.R"]:
            bone.use_connect = True

    # Switch back to OBJECT mode
    bpy.ops.object.mode_set(mode='OBJECT')

def snap_duo(head,tail,armature):
    upper_bone = armature.edit_bones.get(head)
    lower_bone = armature.edit_bones.get(tail)
    
    if upper_bone and lower_bone:
        upper_bone.tail = lower_bone.head

def snap_bones(armature):
    # Switch to EDIT mode
    bpy.ops.object.mode_set(mode='EDIT')

    # Snap Upperarm.R tail to Forearm.R head
    snap_duo("Upperarm.R","Forearm.R",armature)
        
    # Snap Forearm.R tail to Hand.R head
    snap_duo("Forearm.R","Hand.R",armature)
    
    # Snap Thigh.R tail to Calf.R head
    snap_duo("Thigh.R","Calf.R",armature)
    
    # Snap Calf.R tail to Foot.R head
    snap_duo("Calf.R","Foot.R",armature)
    

    # Switch back to OBJECT mode
    bpy.ops.object.mode_set(mode='OBJECT')

######utilities######


#bone collections#

groups = ["IK", "FK", "right", "left", "fingers", "middle"]

def create_bone_collection(collection_name):
    
    global groups
    try:
        if bpy.context.object.data.collections[collection_name]:
            groups.remove(collection_name)
    except KeyError:
        bpy.context.object.data.collections.new(collection_name)
        pass

def atribuir_a_grupo(grupo,sufixo,tema):
    x = bpy.context.object.data.collections[grupo]
    bpy.ops.object.mode_set(mode='POSE')
    bpy.ops.pose.select_all(action='DESELECT')
    # Iterate over each bone in the armature
    obj = bpy.context.active_object  # Assign the currently active object to `obj`
    for bone in obj.pose.bones:
        if bone.name.endswith(sufixo):
            bone.bone.select = True
            x.assign(bone)
            bpy.context.object.data.bones[bone.name].color.palette = tema
        else:
            bone.bone.select = False

    bpy.ops.pose.select_all(action='DESELECT')

def atribuir_a_grupo_dedos():
    x = bpy.context.object.data.collections["fingers"]
    bpy.ops.pose.select_all(action='DESELECT')
    # Iterate over each bone in the armature
    obj = bpy.context.active_object  # Assign the currently active object to `obj`
    for bone in obj.pose.bones:
        if "index" in bone.name.lower() or "middle" in bone.name.lower() or "ring" in bone.name.lower() or "pinky" in bone.name.lower() or "thumb" in bone.name.lower():
            bone.bone.select = True
            x.assign(bone)
            bpy.context.object.data.bones[bone.name].color.palette = "THEME09"

        else:
            bone.bone.select = False

    bpy.ops.pose.select_all(action='DESELECT')

def create_bone_to_collection(armature_var):
    """Function to a create bone collection"""
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='DESELECT')

    global groups
    groups = ["IK", "FK", "right", "left", "fingers", "middle"]

    try:
        if bpy.context.object.data.collections["Bones"]:
            bpy.ops.armature.collection_remove()
    except KeyError:
        pass
            
    for group in groups:
        create_bone_collection(group)
    
    # continuar aqui
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='SELECT')
    bpy.ops.armature.symmetrize()

    bpy.ops.object.mode_set(mode='POSE')
    atribuir_a_grupo('left','.L', 'THEME04')
    atribuir_a_grupo('right','.R', 'THEME01')
    atribuir_a_grupo('IK','IK.R', 'THEME06')
    atribuir_a_grupo('IK','IK.L', 'THEME06')
    atribuir_a_grupo('FK','FK.R', 'THEME02')
    atribuir_a_grupo('FK','FK.L', 'THEME02')

    atribuir_a_grupo_dedos()
    

#bone collections#

def delete_left_bones(armature):
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='DESELECT')
    
    for bone in armature.edit_bones:
        if bone.name.endswith(".L"):
            armature.edit_bones.remove(bone)
    
    bpy.ops.object.mode_set(mode='OBJECT')

def update_bone_tails(armature):
    # Switch to EDIT mode
    bpy.ops.object.mode_set(mode='EDIT')

    for bone in armature.edit_bones:
        if bone.children and (bone.name !="Head" and bone.name !="Pelvis" and bone.name !="RL_BoneRoot"):
            child_bone_name = bone.children[0].name
            child_head = armature.edit_bones[child_bone_name].head
            bone.tail = child_head

    # Switch back to OBJECT mode
    bpy.ops.object.mode_set(mode='OBJECT')

def rename_and_delete_bones(context):
    if context.active_object and context.active_object.type == 'ARMATURE':
        armature = context.active_object.data

        # Switch to Edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Delete specified bones
        bones_to_delete = ["CC_Base_Tongue03", 'CC_Base_Tongue02', 'CC_Base_Tongue01', 'CC_Base_Teeth02', 'CC_Base_Teeth01', 'CC_Base_UpperJaw', 'CC_Base_JawRoot', 'CC_Base_FacialBone', 'CC_Base_R_RibsTwist', 'CC_Base_L_RibsTwist', 'CC_Base_R_Breast', 'CC_Base_L_Breast', 'CC_Base_R_KneeShareBone', 'CC_Base_L_KneeShareBone', 'CC_Base_R_KneeShareBone', 'CC_Base_L_KneeShareBone', 'CC_Base_R_ToeBase', 'CC_Base_L_ToeBase', 'CC_Base_R_PinkyToe1', 'CC_Base_L_PinkyToe1', 'CC_Base_R_RingToe1', 'CC_Base_L_RingToe1', 'CC_Base_R_MidToe1', 'CC_Base_L_MidToe1', 'CC_Base_R_IndexToe1', 'CC_Base_L_IndexToe1', 'CC_Base_R_BigToe1', 'CC_Base_L_BigToe1', 'CC_Base_R_ElbowShareBone', 'CC_Base_L_ElbowShareBone']
        for bone_name in bones_to_delete:
            if bone_name in armature.edit_bones:
                armature.edit_bones.remove(armature.edit_bones[bone_name])
                bpy.context.view_layer.update()  # Update the view layer after deletion
                bpy.ops.object.mode_set(mode='EDIT')  # Make sure we're still in edit mode
                bpy.ops.armature.select_all(action='DESELECT')  # Deselect all bones

        # Switch back to Object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Iterate through all bones in the armature
        for bone in armature.bones:
            # Remove "_R_" from the bone name and append ".R" at the end
            if "_R_" in bone.name:
                if "Base_R_Mid" in bone.name:
                    new_name = bone.name.replace("CC_Base_R_Mid", "Middle") + ".R"
                else:
                    new_name = bone.name.replace("CC_Base_R_", "") + ".R"
                bone.name = new_name

            # Remove "_L_" from the bone name and append ".L" at the end
            elif "_L_" in bone.name:
                if "Base_L_Mid" in bone.name:
                    new_name = bone.name.replace("CC_Base_L_Mid", "Middle") + ".L"
                else:
                    new_name = bone.name.replace("CC_Base_L_", "") + ".L"
                bone.name = new_name

            # Remove "CC_Base" from the bone name
            elif "CC_Base" in bone.name:
                new_name = bone.name.replace("CC_Base_", "")
                bone.name = new_name
    else:
        context.report({'ERROR'}, "No active armature object")

def extrude(extrude_vector, name, new_bone_name, distance=(0, 0, 0)):
     """Create a new bone with an offset from the head of a selected bone."""
     bpy.ops.object.mode_set(mode='EDIT')
     bpy.ops.armature.select_all(action='DESELECT')    
     bone = bpy.context.object.data.edit_bones[name]
     bone.select = True
     bone.select_head = True
     bone.select_tail = True

     bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, 
     TRANSFORM_OT_translate={"value":extrude_vector, "orient_type":'GLOBAL'})
     name += ".001"
     bone=bpy.context.object.data.edit_bones[name]
     bone.name = new_bone_name
     bone.roll = 0
     bone.use_deform = False

     # if  bone.name == "Hand IK.R":
     #     bone.select = True
     #     bone.select_head = True
     #     bone.select_tail = True

     bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={}, TRANSFORM_OT_translate={"value":(0, 0, 0.1), "orient_type":'GLOBAL'})

     bpy.ops.transform.resize(value=(-1, -1, -1), orient_type='GLOBAL')



     if not new_bone_name.endswith("FK"):
        bone.use_connect = False
        
    
     else:
        bone.use_connect = True

     bpy.ops.armature.select_all(action='DESELECT')
    
     if distance != (0, 0, 0) :
        # bpy.context.active_bone.use_connect = False 
        # bpy.ops.transform.translate(value=(distance), orient_type='GLOBAL')
        bone.select = True
        bone.select_head = True
        bone.select_tail = True
        bpy.context.active_bone.use_connect = False 
        bpy.ops.transform.translate(value=(distance), orient_type='GLOBAL')
    
     bpy.ops.armature.select_all(action='DESELECT')

def reparenter(child, parent=''):
    if parent != '':
        bpy.context.active_object.data.edit_bones[child].parent = bpy.context.active_object.data.edit_bones[parent]
    else:
        bpy.context.active_object.data.edit_bones[child].parent = None

def make_controllers(): 
    # Get the active object
    armature_obj = bpy.context.active_object

    # Check if the active object is an armature
    if armature_obj and armature_obj.type == 'ARMATURE':
        # Switch to Edit Mode
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Get the selected bone object
        extrude((0,0,2), "Clavicle.R", "Arm FK.R")

        extrude((0,2,0), "Upperarm.R", "Elbow IK.R",(0,2,0))
        reparenter("Elbow IK.R", "Arm FK.R")

        extrude((-0.7,0,0), "Forearm.R","Hand IK.R")
        reparenter("Hand IK.R", 'Arm FK.R')

        make_leg_FK()

        extrude((0,-2,0), "Thigh.R", "Knee IK.R",(0,-2,0))
        reparenter("Knee IK.R", 'Leg FK.R')

        extrude((0,2,0), "Calf.R","Foot IK.R", (0,0,0))
        reparenter("Foot IK.R", 'Leg FK.R')

        make_finger_controller()

def make_finger_controller():
    bpy.ops.armature.select_all(action='DESELECT')
    name="Hand IK.R"
    bone = bpy.context.active_object.data.edit_bones[name]
    bone.select = True
    bone.select_head = True
    bone.select_tail = True

    bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={}, TRANSFORM_OT_translate={"value":(0, 0, 0.7), "orient_type":'GLOBAL'})
    #bpy.ops.transform.resize(value=(1, 1, 1), orient_type='GLOBAL')

    bone.select = False
    bone.select_head = False
    bone.select_tail = False

    name+= ".001"
    bone = bpy.context.active_object.data.edit_bones[name]
    bone.select = True
    bone.select_head = True
    bone.select_tail = True
    bone.name = "Fingers IK.R"
    reparenter("Fingers IK.R","Hand IK.R")
    fingers = ["Hand.R","Thumb3.R", "Index3.R", "Index2.R", "Index1.R", "Middle3.R", "Middle2.R", "Middle1.R", "Ring3.R", "Ring2.R", "Ring1.R", "Pinky3.R", "Pinky2.R", "Pinky1.R"]
    for finger in fingers:
        set_fingers_to_controller(finger)
    

def set_fingers_to_controller(finger_name):
    bpy.ops.object.mode_set(mode='POSE')    
    armature = bpy.context.active_object
    pose_bones = armature.pose.bones
    
    pose_bone = pose_bones[finger_name]
    
    constraint = pose_bone.constraints.new('COPY_ROTATION')
    constraint.target = armature
    if finger_name.endswith("1.R"):
        constraint.subtarget = "Fingers IK.R"
        constraint.use_x = True
        constraint.use_y = True
        constraint.use_z = True
        constraint.owner_space = 'LOCAL'
        constraint.target_space = 'LOCAL'
        constraint.mix_mode = 'ADD'
    
    elif finger_name == "Hand.R":
        constraint.subtarget = "Hand IK.R"
        constraint.use_x = True
        constraint.use_y = True
        constraint.use_z = True
        constraint.owner_space = 'WORLD'
        constraint.target_space = 'WORLD'
        constraint.mix_mode = 'REPLACE'

    else:
        constraint.subtarget = pose_bone.parent.name
        constraint.use_x = True
        constraint.use_y = False
        constraint.use_z = False
        constraint.owner_space = 'LOCAL'
        constraint.target_space = 'LOCAL'
        constraint.mix_mode = 'ADD'

def make_leg_FK():
    bpy.ops.armature.select_all(action='DESELECT')
    name="Thigh.R"
    bone = bpy.context.active_object.data.edit_bones[name]
    bone.select = True
    bone.select_head = True
    bone.select_tail = True

    bpy.ops.armature.duplicate_move(ARMATURE_OT_duplicate={}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL'})
    bpy.ops.transform.resize(value=(-1, -1, -1), orient_type='GLOBAL')
    bone.select = False
    bone.select_head = False
    bone.select_tail = False

    name+= ".001"
    bone = bpy.context.active_object.data.edit_bones[name]
    bone.select = True
    bone.select_head = True
    bone.select_tail = True

    bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":(-0.2,0,0), "orient_type":'GLOBAL'})
    bpy.context.object.data.edit_bones.remove(bone)
    name = name[:-1]
    name+="2"

    bone=bpy.context.active_object.data.edit_bones[name]
    bone.parent = bpy.context.active_object.data.edit_bones["Pelvis"]
    bone.name ="Leg FK.R"
    bone.use_deform = False
    bone.roll=0
    bpy.ops.armature.select_all(action='DESELECT')

def apply_constraints(bone_name, target, pole_target, angle):
   # Set the active object to the armature
    bpy.context.view_layer.objects.active = bpy.context.active_object
    # Switch to Pose Mode
    bpy.ops.object.mode_set(mode='POSE')
    # Deselect all bones
    bpy.ops.pose.select_all(action='DESELECT')
    # Get the armature object
    armature = bpy.context.active_object
    # Get the specific bone by name (Forearm.R)
    bone = armature.pose.bones.get(bone_name)
    # Select the bone
    bone.bone.select = True
    # Set the active bone
    armature.data.bones.active = bone.bone
    # Add IK constraint to the selected bone
    bpy.ops.pose.constraint_add(type='IK')
    # Get the IK constraint
    IK_constraint = bone.constraints[-1]  # Assuming it's the last constraint added
    # Set the IK target bone
    IK_constraint.target = armature
    IK_constraint.subtarget = target
    # Set the pole target bone
    IK_constraint.pole_target = armature
    IK_constraint.pole_subtarget = pole_target
    IK_constraint.chain_count = 2
    IK_constraint.pole_angle = get_degrees(angle)

def apply_constraints_original():
   # Set the active object to the armature
    bpy.context.view_layer.objects.active = bpy.context.active_object
    # Switch to Pose Mode
    bpy.ops.object.mode_set(mode='POSE')
    # Deselect all bones
    bpy.ops.pose.select_all(action='DESELECT')
    # Get the armature object
    armature = bpy.context.active_object
    # Get the specific bone by name (Forearm.R)
    bone = armature.pose.bones.get('Forearm.R')
    # Select the bone
    bone.bone.select = True
    # Set the active bone
    armature.data.bones.active = bone.bone
    # Add IK constraint to the selected bone
    bpy.ops.pose.constraint_add(type='IK')
    # Get the IK constraint
    IK_constraint = bone.constraints[-1]  # Assuming it's the last constraint added
    # Set the IK target bone
    IK_constraint.target = armature
    IK_constraint.subtarget = 'Hand IK.R'
    # Set the pole target bone
    IK_constraint.pole_target = armature
    IK_constraint.pole_subtarget = 'Elbow IK.R'
    IK_constraint.chain_count = 2
    IK_constraint.pole_angle = get_degrees(-30)

def button2_macro():
    armature_obj = bpy.context.active_object
    armature = armature_obj.data
    delete_left_bones(armature)
    update_bone_tails(armature)
    snap_bones(armature)
    connect_bones(armature)
    reset_bone_roll(armature)

def button3_macro(armature_obj):
        make_controllers()
        apply_constraints('Forearm.R', 'Hand IK.R', 'Elbow IK.R', -30)
        apply_constraints('Calf.R', 'Foot IK.R', 'Knee IK.R', -90)
        create_bone_to_collection(armature_obj)
        hide_twist_bones()

def hide_twist_bones():
    # Get the selected armature object
    armature_obj = bpy.context.active_object
    
    # Iterate through each bone in the armature
    for bone in armature_obj.pose.bones:
        # Check if the bone name contains "twist"
        if "twist" in bone.name.lower():
            # Hide the bone
            bone.bone.hide = True      

#####mesh#######
def remove_all_shape_keys():
    mesh_obj = bpy.context.active_object
    
    # Check if the object is a mesh
    if mesh_obj.type != 'MESH':
        print("Selected object is not a mesh.")
        return
    
    # Remove all shape keys if they exist
    if mesh_obj.data.shape_keys:
        for shape_key in mesh_obj.data.shape_keys.key_blocks:
            mesh_obj.shape_key_remove(shape_key)
        print("All shape keys removed from the selected mesh.")
    else:
        print("No shape keys found for the selected mesh.")

    # Deselect the mesh object
    mesh_obj.select_set(False)

def rename_uvmap():
    # Get the selected mesh object
    mesh_obj = bpy.context.active_object
    # Get the first UV map
    if mesh_obj.data.uv_layers:
        first_uv_map = mesh_obj.data.uv_layers[0]
        # Rename the UV map to "UVMap"
        first_uv_map.name = "UVMap"
    
#####mesh#######

class SimpleAddonPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Simple Addon Panel"
    bl_idname = "OBJECT_PT_simple_addon"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Acurig 2 Unreal'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("object.button4_operator", text="All in One")

        row = layout.row()
        row.operator("object.button5_operator", text="Mesh Stuff")

        row = layout.row()
        row.operator("object.button1_operator", text="remove & rename")

        row = layout.row()
        row.operator("object.button2_operator", text="Details")
       
        row = layout.row()
        row.operator("object.button3_operator", text="Create Control & Groups")
       
        

class Button1Operator(bpy.types.Operator):
    """Button 1 Operator"""
    bl_idname = "object.button1_operator"
    bl_label = "Button 1"

    def execute(self, context):
        rename_and_delete_bones(context)
        return {'FINISHED'}

class Button2Operator(bpy.types.Operator):
    """Button 2 Operator"""
    bl_idname = "object.button2_operator"
    bl_label = "Button 2"

    def execute(self, context):
        button2_macro()
        return {'FINISHED'}

class Button3Operator(bpy.types.Operator):
    """Button 3 Operator"""
    bl_idname = "object.button3_operator"
    bl_label = "Button 3"

    armature: bpy.props.StringProperty()

    def execute(self, context):
        button3_macro(bpy.data.objects.get(self.armature))
        return {'FINISHED'}

class Button4Operator(bpy.types.Operator):
    """Button 4 Operator"""
    bl_idname = "object.button4_operator"
    bl_label = "Button 4"

    armature: bpy.props.StringProperty()
    def execute(self, context):
     x = bpy.context.active_object
     x.show_in_front = True
     rename_and_delete_bones(context)
     button2_macro()
     button3_macro(bpy.data.objects.get(self.armature))
     
     return {'FINISHED'}
    
class Button5Operator(bpy.types.Operator):
    """Button 5 Operator"""
    bl_idname = "object.button5_operator"
    bl_label = "Button 5"

    def execute(self, context):
     rename_uvmap()
     remove_all_shape_keys()     
     return {'FINISHED'}
        

def register():
    bpy.utils.register_class(SimpleAddonPanel)
    bpy.utils.register_class(Button1Operator)
    bpy.utils.register_class(Button2Operator)
    bpy.utils.register_class(Button3Operator)
    bpy.utils.register_class(Button4Operator)
    bpy.utils.register_class(Button5Operator)

def unregister():
    bpy.utils.unregister_class(SimpleAddonPanel)
    bpy.utils.unregister_class(Button1Operator)
    bpy.utils.unregister_class(Button2Operator)
    bpy.utils.unregister_class(Button3Operator)
    bpy.utils.unregister_class(Button4Operator)
    bpy.utils.unregister_class(Button5Operator)

if __name__ == "__main__":
    register()
