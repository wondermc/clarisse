#encoding=utf-8
#!/usr/bin/env python

import ix

#####################################################
# Usage :
#----------------------------------------------------
# 1. Select Objects
# 2. Run
#####################################################

#----------------------------------------------------
# Create Context
#----------------------------------------------------
def createContext( path ):
    context_name = path.split('/')[-1]

    try:
        result = ix.get_item( path )
        if result.is_user_locked():
            result.set_user_locked(False)
    except:
        result = ix.cmds.CreateContext( context_name, ix.get_current_context() )

#----------------------------------------------------
# Copy Trasform
#----------------------------------------------------
def copyMatrix(source, target):
    source_tree = source.get_module()
    source_mx = source_tree.get_global_matrix().get_copy()
    final_matrix = ix.api.GMathMatrix4x4d()
    final_matrix.copy_from(source_mx)
    target.get_module().set_matrix(final_matrix, ix.api.ModuleSceneItem.SPACE_LOCAL)

#----------------------------------------------------
# Set Parent
#----------------------------------------------------
def setParent(source, target):
    ix.cmds.SetParent(['%s.parent' % target], ['%s' % source], [0])



#----------------------------------------------------
# RUN
#----------------------------------------------------
ix.begin_command_batch('copyMatrixSetParent')

folderName  = 'loc_lgt'
folderPath  = '%s/%s' % (ix.get_current_context(), folderName)

createContext( folderPath )

selectObj = ix.selection
selectObjNum = ix.selection.get_count()
obj = []

for i in range(selectObjNum):
    obj.append(selectObj[i])

for i in obj:
    if i.get_class().is_kindof("SceneItem"):
        new_obj_name = '%s_%s' % ( 'lgt', i.get_name() )
        new_obj_type = "LightPhysicalSphere"
        new_obj = ix.cmds.CreateObject(new_obj_name, new_obj_type, "Global", folderPath)
        copyMatrix( i, new_obj )
        setParent( i, new_obj )

ix.end_command_batch()
