import os
import sys
import maya.cmds as cmds
import maya.utils as utils

def create_custom_shelf():
    """Creates a shelf containing the tool"""
    shelf_name = "MayukhScripts"

    if cmds.shelfLayout(shelf_name, exists = True):
        cmds.deleteUI(shelf_name)

    cmds.shelfLayout(shelf_name, parent = "ShelfLayout")

    script_dir = os.path.join(cmds.internalVar(userPrefDir = True), "scripts")
    icon = os.path.join(script_dir, "scene_saver_icon.png")

    if not os.path.exists(icon):
        cmds.warning(f"Icon File not found {icon}")

    cmds.shelfButton(
        label="SceneSaver",
        command="import scene_saver; scene_saver.open_scene_saver()",
        image=icon,
        parent=shelf_name
        )
    
utils.executeDeferred(create_custom_shelf)