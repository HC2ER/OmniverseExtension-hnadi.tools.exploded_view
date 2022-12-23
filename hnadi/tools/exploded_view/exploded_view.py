from .utils import get_name_from_path, get_pure_list

import omni.usd
import omni.kit.commands
from pxr import Usd, Sdf, Gf  

# ----------------------------------------------------SELECT-------------------------------------------------------------
def select_explode_Xform(x_coord, y_coord, z_coord, x_ratio, y_ratio, z_ratio):
    global original_path
    global current_model_path
    global item_count
    global default_pivot
    global item_list0
    global translate_list0

    # Get current stage and active prim_paths
    stage = omni.usd.get_context().get_stage()
    selected_prim_path = omni.usd.get_context().get_selection().get_selected_prim_paths()

    if not selected_prim_path:
        return

    # A: If the whole group is selected
    if len(selected_prim_path) == 1:

        # Test members
        selected_prim_path = omni.usd.get_context().get_selection().get_selected_prim_paths()
        group_prim = stage.GetPrimAtPath(selected_prim_path[0])
        children_prims_list = group_prim.GetChildren()

        # If no members 
        if len(children_prims_list) <= 1:
            print("Please select a valid group or all items at once!")
            return

        else:
            original_path = selected_prim_path
            item_count = len(children_prims_list)

            omni.kit.commands.execute('CopyPrim',
                path_from= selected_prim_path[0],
                path_to='/World/Exploded_Model',
                exclusive_select=False)

            selected_prim_path = omni.usd.get_context().get_selection().get_selected_prim_paths()
            # print(selected_prim_path[-1])
            # sub_group_prim = stage.GetPrimAtPath(selected_prim_path[0])
            # sub_children_prims_list = group_prim.GetChildren()

            # original_path = selected_prim_path
            # item_count = len(selected_prim_path)        
            # for i in sub_children_prim_list:
            #     name = get_name_from_path(i)
            #     name_list.append(name)

            omni.kit.commands.execute('SelectPrims',
                old_selected_paths=selected_prim_path,
                new_selected_paths=[selected_prim_path[-1]],
                expand_in_stage=True)

    # B: If multiple prims are selected separately
    else:
        original_path = selected_prim_path
        item_count = len(selected_prim_path)

        name_list = []
        group_list = []
        for i in selected_prim_path:

            name = get_name_from_path(i)
            name_list.append(name)

            # Copy
            omni.kit.commands.execute('CopyPrim',
            path_from = i,
            path_to ='/World/item_01',
            exclusive_select=False)

            if selected_prim_path.index(i)<= 8:
                group_list.append(f'/World/item_0{selected_prim_path.index(i)+1}')
            else:
                group_list.append(f'/World/item_{selected_prim_path.index(i)+1}')

        # Group
        omni.kit.commands.execute('GroupPrims',
            prim_paths=group_list)

        # Change group name
        selected_prim_path = omni.usd.get_context().get_selection().get_selected_prim_paths()
        omni.kit.commands.execute('MovePrims',
            paths_to_move={selected_prim_path[0]: '/World/Exploded_Model'})

        # obj = stage.GetObjectAtPath(selected_prim_path[0])
        # default_pivot = obj.GetAttribute('xformOp:translate:pivot').Get()
        
        # Change members names back
        selected_prim_path = omni.usd.get_context().get_selection().get_selected_prim_paths()
        group_prim = stage.GetPrimAtPath(selected_prim_path[0])
        children_prims_list = group_prim.GetChildren()

        # Move members out of the group
        for i in children_prims_list:
            ind = children_prims_list.index(i)
            if ind <= 8:
                omni.kit.commands.execute('MovePrims',
                    paths_to_move={f"{selected_prim_path[0]}/item_0{ind+1}": f"{selected_prim_path[0]}/" + name_list[ind]})
            else:
                omni.kit.commands.execute('MovePrims',
                    paths_to_move={f"{selected_prim_path[0]}/item_{ind+1}": f"{selected_prim_path[0]}/" + name_list[ind]})



    # Choose Exploded_Model and get current path,count,pivot
    selected_prim_path = omni.usd.get_context().get_selection().get_selected_prim_paths()
    current_model_path = selected_prim_path
    obj = stage.GetObjectAtPath(selected_prim_path[0])
    default_pivot = obj.GetAttribute('xformOp:translate:pivot').Get()
    print(obj)
    print(default_pivot)

    # Get origin translate_list
    outer_group_prim = stage.GetPrimAtPath(current_model_path[0])
    children_prims_list = outer_group_prim.GetChildren()
    item_list0 = children_prims_list

    translate_list0 = []
    for i in children_prims_list:
        sub_children_prim_list = i.GetChildren()
        if len(sub_children_prim_list) <= 1:
            translate = i.GetAttribute('xformOp:translate').Get()
        else:
            translate = i.GetAttribute('xformOp:translate:pivot').Get()
        translate_list0.append(translate)

    # print("--------------------------------------------")
    # print(original_path)
    # print(current_model_path)
    # print(item_count)
    # print(default_pivot)
    # print(item_list0)
    # print(translate_list0)
    # print("--------------------------------------------")

    # Create Explosion_Centre
    omni.kit.commands.execute('CreatePrimWithDefaultXform',
        prim_type='Xform',
        attributes={})

    selected_prim_path = omni.usd.get_context().get_selection().get_selected_prim_paths()
    world_pivot_path = selected_prim_path

    omni.kit.commands.execute('ChangeProperty',
        prop_path=Sdf.Path(f"{world_pivot_path[0]}" + ".xformOp:translate"),
        value=Gf.Vec3d(default_pivot[0], default_pivot[1], default_pivot[2]),
        prev=Gf.Vec3d(0, 0, 0))

    obj1 = stage.GetObjectAtPath(selected_prim_path[0])
    default_pivot = obj1.GetAttribute('xformOp:translate').Get()

    omni.kit.commands.execute('MovePrims',
	    paths_to_move={f"{world_pivot_path[0]}": f"{current_model_path[0]}/" + "Explosion_Centre"})

    # Set_default_button_value
    x_coord.model.set_value(default_pivot[0])
    y_coord.model.set_value(default_pivot[1])
    z_coord.model.set_value(default_pivot[2])
    x_ratio.model.set_value(0)
    y_ratio.model.set_value(0)
    z_ratio.model.set_value(0)
    
    # End
    omni.kit.commands.execute('SelectPrims',
        old_selected_paths=[],
        new_selected_paths=[f'{current_model_path[0]}'],
        expand_in_stage=True)

    return

    
#------------------------------------------------------REMOVE-----------------------------------------------------------
def remove_item(x_coord, y_coord, z_coord, x_ratio, y_ratio, z_ratio):
    try:
        global original_path
        global current_model_path
        global item_count
        global default_pivot
        global item_list0
        global translate_list0

        stage = omni.usd.get_context().get_stage()
        selected_prim_path = omni.usd.get_context().get_selection().get_selected_prim_paths()

        if not selected_prim_path:
            return

        # Remove correct items
        for i in selected_prim_path:
            path = str(i)
            name = get_name_from_path(path)
            if path != f"{current_model_path[0]}/" + "Explosion_Centre":
                if path != current_model_path[0] and path.find(current_model_path[0]) != -1:

                    omni.kit.commands.execute('SelectPrims',
                        old_selected_paths=[],
                        new_selected_paths=[f'{current_model_path[0]}'],
                        expand_in_stage=True)

                    selected_prim_path = omni.usd.get_context().get_selection().get_selected_prim_paths()
                    obj0 = stage.GetObjectAtPath(selected_prim_path[0])
                    children_prims_list_z0 = obj0.GetChildren()

                    new_count = len(children_prims_list_z0)

                    if new_count == 2:
                        print("Cannot remove the only item in Exploded_Model!")
                        return

                    else:
                        # Restore values to 0 to record the postions
                        x = x_ratio.model.get_value_as_float()
                        y = y_ratio.model.get_value_as_float()
                        z = z_ratio.model.get_value_as_float()
                        # If 0，pass
                        if x == 0.0 and y== 0.0 and z == 0.0:
                            pass
                        # If not, set 0
                        else:
                            x_ratio.model.set_value(0.0)
                            y_ratio.model.set_value(0.0)
                            z_ratio.model.set_value(0.0)

                        omni.kit.commands.execute('MovePrim',
                            path_from = path,
                            path_to = "World/" + name)
                else:
                    omni.kit.commands.execute('SelectPrims',
                        old_selected_paths=[],
                        new_selected_paths=[f'{current_model_path[0]}'],
                        expand_in_stage=True)
                    print("Please select a valid item to remove!")

            else:
                omni.kit.commands.execute('SelectPrims',
                    old_selected_paths=[],
                    new_selected_paths=[f'{current_model_path[0]}'],
                    expand_in_stage=True)
                print("Cannot remove Explosion_Centre!")
        
        omni.kit.commands.execute('SelectPrims',
            old_selected_paths=[],
            new_selected_paths=[f'{current_model_path[0]}'],
            expand_in_stage=True)

        selected_prim_path = omni.usd.get_context().get_selection().get_selected_prim_paths()
        obj = stage.GetObjectAtPath(selected_prim_path[0])
        children_prims_list_z = obj.GetChildren()

        new_count2 = len(children_prims_list_z) -1

        # If any item is removed
        if new_count2 < item_count:
            # Refresh item_count
            item_count = new_count2
            obj = stage.GetObjectAtPath(selected_prim_path[0])

            # Refresh item_list0 and translate_list0
            outer_group_prim = stage.GetPrimAtPath(current_model_path[0])
            children_prims_list0 = outer_group_prim.GetChildren()
            children_prims_list = get_pure_list(children_prims_list0)

            item_list0 = children_prims_list
            translate_list0 = []
            for i in children_prims_list:
                sub_children_prim_list = i.GetChildren()
                if len(sub_children_prim_list) <= 1:
                    translate = i.GetAttribute('xformOp:translate').Get()
                else:
                    translate = i.GetAttribute('xformOp:translate:pivot').Get()
                translate_list0.append(translate)

            # Refresh pivot
            group_list = []
            name_list = []

            for i in item_list0:
                item_path = str(i.GetPath())
                name = get_name_from_path(item_path)
                name_list.append(name)
                group_list.append(item_path)

            # S1 group
            omni.kit.commands.execute('GroupPrims',
                prim_paths=group_list)

            # change group name
            selected_prim_path = omni.usd.get_context().get_selection().get_selected_prim_paths()
            omni.kit.commands.execute('MovePrims',
                paths_to_move={selected_prim_path[0]: f"{current_model_path[0]}/Sub_Exploded_Model"})

            # S2 Get new pivot by group
            omni.kit.commands.execute('SelectPrims',
                old_selected_paths=[],
                new_selected_paths=[f"{current_model_path[0]}/Sub_Exploded_Model"],
                expand_in_stage=True)

            selected_prim_path = omni.usd.get_context().get_selection().get_selected_prim_paths()
            obj = stage.GetObjectAtPath(selected_prim_path[0])
            default_pivot = obj.GetAttribute('xformOp:translate:pivot').Get()

            # S3 Move members out of the group
            group_path = selected_prim_path
            outer_group_prim = stage.GetPrimAtPath(group_path[0])
            children_prims_list = outer_group_prim.GetChildren()

            for i in children_prims_list:
                index = children_prims_list.index(i)
                name = name_list[index]
                omni.kit.commands.execute('MovePrim',
                    path_from = f"{group_path[0]}/{name_list[index]}",
                    path_to = f"{current_model_path[0]}/{name_list[index]}")

            # S4 Delete the group
            omni.kit.commands.execute('DeletePrims',
                paths=[f"{current_model_path[0]}/Sub_Exploded_Model"])

            # S5 Change pivot
            omni.kit.commands.execute('ChangeProperty',
                prop_path=Sdf.Path(f"{current_model_path[0]}/Explosion_Centre" + ".xformOp:translate"),
                value=Gf.Vec3d(default_pivot[0], default_pivot[1], default_pivot[2]),
                prev=Gf.Vec3d(0, 0, 0))
            
            # Restore_default_panel
            x_coord.model.set_value(default_pivot[0])
            y_coord.model.set_value(default_pivot[1])
            z_coord.model.set_value(default_pivot[2])
            if x == 0.0 and y== 0.0 and z == 0.0:
                pass
            else:
                x_ratio.model.set_value(x)
                y_ratio.model.set_value(y)
                z_ratio.model.set_value(z)

            # Select
            omni.kit.commands.execute('SelectPrims',
                old_selected_paths=[],
                new_selected_paths=[f'{current_model_path[0]}'],
                expand_in_stage=True)
            return
            
        # If no remove actions，return
        else:
            omni.kit.commands.execute('SelectPrims',
                old_selected_paths=[],
                new_selected_paths=[f'{current_model_path[0]}'],
                expand_in_stage=True)
            return
    except:
        print("Create a model to explode at first!")        
        return
    
#---------------------------------------------------------ADD-----------------------------------------------------------
def add_item(x_coord, y_coord, z_coord, x_ratio, y_ratio, z_ratio):
    try:
        global original_path
        global current_model_path
        global item_count
        global default_pivot
        global item_list0
        global translate_list0

        stage = omni.usd.get_context().get_stage()
        selected_prim_path = omni.usd.get_context().get_selection().get_selected_prim_paths()

        if not selected_prim_path:
            return

        # Add correct items
        for i in selected_prim_path:
            path = str(i)
            name = get_name_from_path(path)

            if path.find(current_model_path[0]) == -1:
                # Restore values to 0 to record the postions
                x =  x_ratio.model.get_value_as_float()
                y =  y_ratio.model.get_value_as_float()
                z =  z_ratio.model.get_value_as_float()
                # If 0, pass
                if x == 0.0 and y== 0.0 and z == 0.0:
                    pass
                # If not, set 0
                else:
                    x_ratio.model.set_value(0.0)
                    y_ratio.model.set_value(0.0)
                    z_ratio.model.set_value(0.0)

                omni.kit.commands.execute('MovePrim',
                    path_from = path,
                    path_to = f"{current_model_path[0]}/" + name)
            else:
                omni.kit.commands.execute('SelectPrims',
                    old_selected_paths=[],
                    new_selected_paths=[f'{current_model_path[0]}'],
                    expand_in_stage=True)
                print("The selected item already existed in the model!")

        omni.kit.commands.execute('SelectPrims',
            old_selected_paths=[],
            new_selected_paths=[f'{current_model_path[0]}'],
            expand_in_stage=True)

        selected_prim_path = omni.usd.get_context().get_selection().get_selected_prim_paths()
        obj = stage.GetObjectAtPath(selected_prim_path[0])
        children_prims_list_z = obj.GetChildren()

        new_count2 = len(children_prims_list_z) - 1
        # print(new_count2)

        # If any items is added
        if new_count2 > item_count:
            # Refresh item_count
            item_count = new_count2
            obj = stage.GetObjectAtPath(selected_prim_path[0])

            # Refresh item_list0 and translate_list0
            outer_group_prim = stage.GetPrimAtPath(current_model_path[0])
            children_prims_list0 = outer_group_prim.GetChildren()
            children_prims_list = get_pure_list(children_prims_list0)

            item_list0 = children_prims_list
            translate_list0 = []
            for i in children_prims_list:
                sub_children_prim_list = i.GetChildren()
                if len(sub_children_prim_list) <= 1:
                    translate = i.GetAttribute('xformOp:translate').Get()
                else:
                    translate = i.GetAttribute('xformOp:translate:pivot').Get()
                translate_list0.append(translate)

            # Refresh pivot
            group_list = []
            name_list = []

            for i in item_list0:
                item_path = str(i.GetPath())
                name = get_name_from_path(item_path)
                name_list.append(name)
                group_list.append(item_path)

            # S1 Group
            omni.kit.commands.execute('GroupPrims',
                prim_paths=group_list)

            # Change group name
            selected_prim_path = omni.usd.get_context().get_selection().get_selected_prim_paths()
            omni.kit.commands.execute('MovePrims',
                paths_to_move={selected_prim_path[0]: f"{current_model_path[0]}/Sub_Exploded_Model"})

            # S2 Get new pivot by group
            omni.kit.commands.execute('SelectPrims',
                old_selected_paths=[],
                new_selected_paths=[f"{current_model_path[0]}/Sub_Exploded_Model"],
                expand_in_stage=True)

            selected_prim_path = omni.usd.get_context().get_selection().get_selected_prim_paths()
            obj = stage.GetObjectAtPath(selected_prim_path[0])
            default_pivot = obj.GetAttribute('xformOp:translate:pivot').Get()
            print(default_pivot)

            # S3 Move members out of the group
            group_path = selected_prim_path
            outer_group_prim = stage.GetPrimAtPath(group_path[0])
            children_prims_list = outer_group_prim.GetChildren()

            for i in children_prims_list:
                index = children_prims_list.index(i)
                name = name_list[index]
                omni.kit.commands.execute('MovePrim',
                    path_from= f"{group_path[0]}/{name_list[index]}",
                    path_to=f"{current_model_path[0]}/{name_list[index]}")

            # S4 Delete the group
            omni.kit.commands.execute('DeletePrims',
                paths=[f"{current_model_path[0]}/Sub_Exploded_Model"])

            # S5 Change pivot
            omni.kit.commands.execute('ChangeProperty',
                prop_path=Sdf.Path(f"{current_model_path[0]}/Explosion_Centre" + ".xformOp:translate"),
                value=Gf.Vec3d(default_pivot[0], default_pivot[1], default_pivot[2]),
                prev=Gf.Vec3d(0, 0, 0))
            
            # Restore_default_panel
            x_coord.model.set_value(default_pivot[0])
            y_coord.model.set_value(default_pivot[1])
            z_coord.model.set_value(default_pivot[2])
            if x == 0.0 and y== 0.0 and z == 0.0:
                pass
            else:
                x_ratio.model.set_value(x)
                y_ratio.model.set_value(y)
                z_ratio.model.set_value(z)
            
            # Select
            omni.kit.commands.execute('SelectPrims',
                old_selected_paths=[],
                new_selected_paths=[f'{current_model_path[0]}'],
                expand_in_stage=True)
            return
            
        # If no add actions，return
        else:
            omni.kit.commands.execute('SelectPrims',
                old_selected_paths=[],
                new_selected_paths=[f'{current_model_path[0]}'],
                expand_in_stage=True)
            return

    except:
        print("Create a model to explode at first!")        
        return


#--------------------------------------------------------BIND-----------------------------------------------------------
def bind_item(x_coord, y_coord, z_coord, x_ratio, y_ratio, z_ratio):
    try:
        global original_path
        global current_model_path
        global item_count
        global default_pivot
        global item_list0
        global translate_list0

        stage = omni.usd.get_context().get_stage()
        selected_prim_path = omni.usd.get_context().get_selection().get_selected_prim_paths()

        if not selected_prim_path:
            return
        
        if len(selected_prim_path) < 2:
            omni.kit.commands.execute('SelectPrims',
                old_selected_paths=[],
                new_selected_paths=[f'{current_model_path[0]}'],
                expand_in_stage=True)
            print("Bind at least 2 items in the model!")
            return

        group_list = []
        for i in selected_prim_path:
            path = str(i)
            name = get_name_from_path(path)

            if path != f"{current_model_path[0]}/" + "Explosion_Centre":
                if path.find(current_model_path[0]) != -1:
                    group_list.append(i)
            else:
                omni.kit.commands.execute('SelectPrims',
                    old_selected_paths=[],
                    new_selected_paths=[f'{current_model_path[0]}'],
                    expand_in_stage=True)
                print("Cannot bind the Explosion_Centre!")
        
        # Restore values to 0 to bind
        x =  x_ratio.model.get_value_as_float()
        y =  y_ratio.model.get_value_as_float()
        z =  z_ratio.model.get_value_as_float()
        # If 0，pass
        if x == 0.0 and y== 0.0 and z == 0.0:
            pass
        # If not，set 0
        else:
            x_ratio.model.set_value(0.0)
            y_ratio.model.set_value(0.0)
            z_ratio.model.set_value(0.0)

        # Bind items
        omni.kit.commands.execute('GroupPrims',
            prim_paths=group_list)

        selected_prim_path = omni.usd.get_context().get_selection().get_selected_prim_paths()
        group_path = selected_prim_path[0]
        # print(group_path)
        
        omni.kit.commands.execute('SelectPrims',
            old_selected_paths=[],
            new_selected_paths=[f'{current_model_path[0]}'],
            expand_in_stage=True)

        selected_prim_path = omni.usd.get_context().get_selection().get_selected_prim_paths()
        obj = stage.GetObjectAtPath(selected_prim_path[0])
        children_prims_list_z = obj.GetChildren()

        new_count2 = len(children_prims_list_z) - 1
        # print(new_count2)

        # If bind actions
        if new_count2 < item_count:
            # Refresh item_count
            item_count = new_count2
            obj = stage.GetObjectAtPath(selected_prim_path[0])

            # Refresh item_list0 and translate_list0
            outer_group_prim = stage.GetPrimAtPath(current_model_path[0])
            children_prims_list0 = outer_group_prim.GetChildren()
            children_prims_list = get_pure_list(children_prims_list0)

            item_list0 = children_prims_list
            translate_list0 = []
            for i in children_prims_list:
                sub_children_prim_list = i.GetChildren()
                if len(sub_children_prim_list) <= 1:
                    translate = i.GetAttribute('xformOp:translate').Get()
                else:
                    translate = i.GetAttribute('xformOp:translate:pivot').Get()
                translate_list0.append(translate)
            # Refresh pivot
            default_pivot = default_pivot
            
            # Restore_default_panel
            x_coord.model.set_value(default_pivot[0])
            y_coord.model.set_value(default_pivot[1])
            z_coord.model.set_value(default_pivot[2])
            if x == 0.0 and y== 0.0 and z == 0.0:
                pass
            else:
                x_ratio.model.set_value(x)
                y_ratio.model.set_value(y)
                z_ratio.model.set_value(z)
            
            # Select
            omni.kit.commands.execute('SelectPrims',
                old_selected_paths=[],
                new_selected_paths=[f'{current_model_path[0]}'],
                expand_in_stage=True)
            return
            
        # If no bind，return
        else:
            omni.kit.commands.execute('SelectPrims',
                old_selected_paths=[],
                new_selected_paths=[f'{current_model_path[0]}'],
                expand_in_stage=True)
            return

    except:
        print("Create a model to explode at first!")        
        return

#------------------------------------------------------UNBIND-----------------------------------------------------------
def unbind_item(x_coord, y_coord, z_coord, x_ratio, y_ratio, z_ratio):
    try:
        global original_path
        global current_model_path
        global item_count
        global default_pivot
        global item_list0
        global translate_list0

        stage = omni.usd.get_context().get_stage()
        selected_prim_path = omni.usd.get_context().get_selection().get_selected_prim_paths()

        if not selected_prim_path:
            return

        # Test valid group
        for i in selected_prim_path:
            path0 = str(i)

            if path0 != current_model_path[0] and path0.find(current_model_path[0]) != -1:
                outer_group_prim = stage.GetPrimAtPath(path0)
                children_prims_list0 = outer_group_prim.GetChildren()
                if len(children_prims_list0) < 1:
                    omni.kit.commands.execute('SelectPrims',
                        old_selected_paths=[],
                        new_selected_paths=[f'{current_model_path[0]}'],
                        expand_in_stage=True)
                    print("Please select a valid group!")
                    return
                else:
                    if selected_prim_path.index(i) == 0:
                        # Restore values to 0 to unbind
                        x =  x_ratio.model.get_value_as_float()
                        y =  y_ratio.model.get_value_as_float()
                        z =  z_ratio.model.get_value_as_float()
                        # If 0，pass
                        if x == 0.0 and y== 0.0 and z == 0.0:
                            pass
                        # If not，set 0
                        else:
                            x_ratio.model.set_value(0.0)
                            y_ratio.model.set_value(0.0)
                            z_ratio.model.set_value(0.0)

                    for j in children_prims_list0:
                        path = str(j.GetPath())
                        name = get_name_from_path(path)

                        omni.kit.commands.execute('MovePrims',
                            paths_to_move={path: f"{current_model_path[0]}/{name}"})
                
                # Delete group
                omni.kit.commands.execute('DeletePrims',
                    paths=[path0])

            else:
                omni.kit.commands.execute('SelectPrims',
                    old_selected_paths=[],
                    new_selected_paths=[f'{current_model_path[0]}'],
                    expand_in_stage=True)
                print("Please unbind a valid group!")
                return
        

        omni.kit.commands.execute('SelectPrims',
            old_selected_paths=[],
            new_selected_paths=[f'{current_model_path[0]}'],
            expand_in_stage=True)

        selected_prim_path = omni.usd.get_context().get_selection().get_selected_prim_paths()
        obj = stage.GetObjectAtPath(selected_prim_path[0])
        children_prims_list_z = obj.GetChildren()

        new_count2 = len(children_prims_list_z) - 1
        # print(new_count2)

        # If unbind actions
        if new_count2 >= item_count:
            # Refresh item_count
            item_count = new_count2
            obj = stage.GetObjectAtPath(selected_prim_path[0])

            # Refresh item_list0 and translate_list0
            outer_group_prim = stage.GetPrimAtPath(current_model_path[0])
            children_prims_list0 = outer_group_prim.GetChildren()
            children_prims_list = get_pure_list(children_prims_list0)

            item_list0 = children_prims_list
            translate_list0 = []
            for i in children_prims_list:
                sub_children_prim_list = i.GetChildren()
                if len(sub_children_prim_list) <= 1:
                    translate = i.GetAttribute('xformOp:translate').Get()
                else:
                    translate = i.GetAttribute('xformOp:translate:pivot').Get()
                translate_list0.append(translate)
            # Refresh pivot
            default_pivot = default_pivot
            
            # Restore_default_panel
            x_coord.model.set_value(default_pivot[0])
            y_coord.model.set_value(default_pivot[1])
            z_coord.model.set_value(default_pivot[2])
            if x == 0.0 and y== 0.0 and z == 0.0:
                pass
            else:
                x_ratio.model.set_value(x)
                y_ratio.model.set_value(y)
                z_ratio.model.set_value(z)
            
            # Select
            omni.kit.commands.execute('SelectPrims',
                old_selected_paths=[],
                new_selected_paths=[f'{current_model_path[0]}'],
                expand_in_stage=True)
            return
            
        # If no unbind，return
        else:
            omni.kit.commands.execute('SelectPrims',
                old_selected_paths=[],
                new_selected_paths=[f'{current_model_path[0]}'],
                expand_in_stage=True)
            return

    except:
        print("Create a model to explode at first!")
        return       


#------------------------------------------------------ONCHANGE----------------------------------------------------------  
def on_pivot_change(x_coord, y_coord, z_coord, x_button, y_button, z_button, a:float):
    try:
        global original_path
        global current_model_path
        global item_count
        global default_pivot
        global item_list0
        global translate_list0

        stage = omni.usd.get_context().get_stage()

        # Select Model
        if not current_model_path:
            print("Please select items to explode at first")
            return

        omni.kit.commands.execute('SelectPrims',
            old_selected_paths=[],
            new_selected_paths=[f'{current_model_path[0]}'],
            expand_in_stage=True)

        # Get x,y,z value
        x_position = x_coord.model.get_value_as_float()
        y_position = y_coord.model.get_value_as_float()
        z_position = z_coord.model.get_value_as_float()
        # print(x_position, y_position, z_position)

        # Change pivot
        omni.kit.commands.execute('TransformPrimSRT',
            path=Sdf.Path(f"{current_model_path[0]}/" + "Explosion_Centre"),
            new_translation=Gf.Vec3d(x_position, y_position, z_position),
            old_translation=Gf.Vec3d(0, 0, 0))

        # Get new pivot
        obj2 = stage.GetObjectAtPath(f"{current_model_path[0]}/" + "Explosion_Centre")
        pivot = obj2.GetAttribute('xformOp:translate').Get()

        # Get x,y,z ratio
        x_ratio = x_button.model.get_value_as_float()
        y_ratio = y_button.model.get_value_as_float()
        z_ratio = z_button.model.get_value_as_float()

        # Calculate each item
        group_prim = stage.GetPrimAtPath(current_model_path[0])
        children_prims_list0 = group_prim.GetChildren()
        children_prims_list = get_pure_list(children_prims_list0)

        # Move each item
        for item in children_prims_list:
            sub_children_prim_list = item.GetChildren()
            index = children_prims_list.index(item)
            translate = translate_list0[index]
            # print(translate)
            item_path = item.GetPrimPath()
            # print(item_path)

            if len(sub_children_prim_list) <= 1:
                # If single item
                x_distance = (translate[0] - pivot[0]) * x_ratio
                y_distance = (translate[1] - pivot[1]) * y_ratio
                z_distance = (translate[2] - pivot[2]) * z_ratio

                omni.kit.commands.execute('TransformPrimSRT',
                    path=Sdf.Path(item_path),
                    new_translation=Gf.Vec3d(translate[0] + x_distance, translate[1] + y_distance, translate[2] + z_distance),
                    old_translation=translate)

            else:
                # If group item
                x_distance = (translate[0] - pivot[0]) * x_ratio
                y_distance = (translate[1] - pivot[1]) * y_ratio
                z_distance = (translate[2] - pivot[2]) * z_ratio

                omni.kit.commands.execute('TransformPrimSRT',
                    path=Sdf.Path(item_path),
                    new_translation=Gf.Vec3d(x_distance, y_distance, z_distance),
                    old_translation=translate)

        # End 
        omni.kit.commands.execute('SelectPrims',
            old_selected_paths=[],
            new_selected_paths=[f"{current_model_path[0]}/" + "Explosion_Centre"],
            expand_in_stage=True)

    except:
        x_coord.model.set_value(0.0)
        y_coord.model.set_value(0.0)
        z_coord.model.set_value(0.0)
        x_button.model.set_value(0.0)
        y_button.model.set_value(0.0)
        z_button.model.set_value(0.0)
        print("Create a model to explode at first!")
        return


def on_ratio_change(x_button, y_button, z_button, x_coord, y_coord, z_coord, a:float):
    try:
        global original_path
        global current_model_path
        global item_count
        global default_pivot
        global item_list0
        global translate_list0

        stage = omni.usd.get_context().get_stage()

        # Select Model
        if not current_model_path:
            print("Please select items to explode at first")
            return

        omni.kit.commands.execute('SelectPrims',
            old_selected_paths=[],
            new_selected_paths=[f'{current_model_path[0]}'],
            expand_in_stage=True)

        # Get x,y,z value
        x_position = x_coord.model.get_value_as_float()
        y_position = y_coord.model.get_value_as_float()
        z_position = z_coord.model.get_value_as_float()
        # print(x_position, y_position, z_position)

        # Change pivot
        omni.kit.commands.execute('TransformPrimSRT',
            path=Sdf.Path(f"{current_model_path[0]}/" + "Explosion_Centre"),
            new_translation=Gf.Vec3d(x_position, y_position, z_position),
            old_translation=Gf.Vec3d(0, 0, 0))

        # Get new pivot
        obj = stage.GetObjectAtPath(f"{current_model_path[0]}/" + "Explosion_Centre")
        pivot = obj.GetAttribute('xformOp:translate').Get()
        
        # Get x,y,z ratio
        x_ratio = x_button.model.get_value_as_float()
        y_ratio = y_button.model.get_value_as_float()
        z_ratio = z_button.model.get_value_as_float()

        # Calculate each item
        group_prim = stage.GetPrimAtPath(current_model_path[0])
        children_prims_list0 = group_prim.GetChildren()
        children_prims_list = get_pure_list(children_prims_list0)

        # Move each item
        for item in children_prims_list:
            sub_children_prim_list = item.GetChildren()
            index = children_prims_list.index(item)
            translate = translate_list0[index]
            item_path = item.GetPrimPath()

            if len(sub_children_prim_list) <= 1:
                # If single item
                x_distance = (translate[0] - pivot[0]) * x_ratio
                y_distance = (translate[1] - pivot[1]) * y_ratio
                z_distance = (translate[2] - pivot[2]) * z_ratio

                omni.kit.commands.execute('TransformPrimSRT',
                    path=Sdf.Path(item_path),
                    new_translation=Gf.Vec3d(translate[0] + x_distance, translate[1] + y_distance, translate[2] + z_distance),
                    old_translation=translate)

            else:
                # If group item
                x_distance = (translate[0] - pivot[0]) * x_ratio
                y_distance = (translate[1] - pivot[1]) * y_ratio
                z_distance = (translate[2] - pivot[2]) * z_ratio

                omni.kit.commands.execute('TransformPrimSRT',
                    path=Sdf.Path(item_path),
                    new_translation=Gf.Vec3d(x_distance, y_distance, z_distance),
                    old_translation=translate)
        
        # End
        omni.kit.commands.execute('SelectPrims',
            old_selected_paths=[],
            new_selected_paths=[f"{current_model_path[0]}/" + "Explosion_Centre"],
            expand_in_stage=True)

    except:
        x_coord.model.set_value(0.0)
        y_coord.model.set_value(0.0)
        z_coord.model.set_value(0.0)
        x_button.model.set_value(0.0)
        y_button.model.set_value(0.0)
        z_button.model.set_value(0.0)
        print("Create a model to explode at first!")
        return


#-------------------------------------------------SECONDARY FUNCTION------------------------------------------------------  
def hide_unhide_original_model():
    try:
        global original_path
        global item_count

        stage = omni.usd.get_context().get_stage()

        visible_count = 0
        for i in original_path:
            obj = stage.GetObjectAtPath(i)
            visual_attr = obj.GetAttribute('visibility').Get()
            # print(type(visual_attr))
            # print(visual_attr)
            if visual_attr == "inherited":
                visible_count += 1
        
        # print(original_path)
        # print(visible_count)
        # print(item_count)

        # All light
        if visible_count == 1:
            omni.kit.commands.execute('ChangeProperty',
            prop_path=Sdf.Path(f"{original_path[0]}.visibility"),
            value='invisible',
            prev=None)
            
        # All light
        elif visible_count < item_count:
            for i in original_path:
                omni.kit.commands.execute('ChangeProperty',
                prop_path=Sdf.Path(f"{i}.visibility"),
                value='inherited',
                prev=None)

        # All dark
        elif visible_count == item_count:
            for i in original_path:
                omni.kit.commands.execute('ChangeProperty',
                prop_path=Sdf.Path(f"{i}.visibility"),
                value='invisible',
                prev=None)
        return

    except:
        print("Cannot find ORIGINAL prims to hide or show!")
        return


def set_camera():
    stage = omni.usd.get_context().get_stage()

    world = stage.GetObjectAtPath('/World')
    children_refs = world.GetChildren()
    for i in children_refs:
        path = str(i)
        if path.find('/World/Axonometric_View') != -1:
            print("Axonometric camera already existed!")
            omni.kit.commands.execute('SelectPrims',
                old_selected_paths=[],
                new_selected_paths=['/World/Axonometric_View'],
                expand_in_stage=True)
            return

    omni.kit.commands.execute('DuplicateFromActiveViewportCameraCommand',
	    viewport_name='Viewport')

    omni.kit.commands.execute('CreatePrim',
        prim_path='/World/Camera',
        prim_type='Camera')
    
    selected_prim_path = omni.usd.get_context().get_selection().get_selected_prim_paths()
    camera_path = selected_prim_path

    omni.kit.commands.execute('MovePrims',
        paths_to_move={camera_path[0]: '/World/Axonometric_View'})

    omni.kit.commands.execute('MovePrim',
        path_from=camera_path[0],
        path_to='/World/Axonometric_View',
        time_code=Usd.TimeCode.Default(),
        keep_world_transform=True)
    
    omni.kit.commands.execute('ChangeProperty',
        prop_path=Sdf.Path('/World/Axonometric_View.focalLength'),
        value=500.0,
        prev=0)
    return


def reset_model(x_coord, y_coord, z_coord, x_ratio, y_ratio, z_ratio):
    try:
        global default_pivot

        x_coord.model.set_value(default_pivot[0])
        y_coord.model.set_value(default_pivot[1])
        z_coord.model.set_value(default_pivot[2])

        x = x_ratio.model.get_value_as_float()
        y = y_ratio.model.get_value_as_float()
        z = z_ratio.model.get_value_as_float()
        # If 0，pass
        if x == 0.0 and y== 0.0 and z == 0.0:
            pass
        # If not, set 0
        else:
            x_ratio.model.set_value(0.0)
            y_ratio.model.set_value(0.0)
            z_ratio.model.set_value(0.0)
        return

    except:
        print("Create a model to explode at first!")
        return


def clear(x_coord, y_coord, z_coord, x_ratio, y_ratio, z_ratio):
    try:
        global original_path
        global current_model_path
        global item_count
        global default_pivot
        global item_list0
        global translate_list0

        omni.kit.commands.execute('DeletePrims',
            paths=[current_model_path[0]])
        
        original_path = None
        current_model_path = None
        item_count = None
        default_pivot = None
        item_list0 = None
        translate_list0 = None

        x_coord.model.set_value(0.0)
        y_coord.model.set_value(0.0)
        z_coord.model.set_value(0.0)
        x_ratio.model.set_value(0.0)
        y_ratio.model.set_value(0.0)
        z_ratio.model.set_value(0.0)

        print("All data clear")
        return

    except:
        print("Create a model to explode at first!")
        return
