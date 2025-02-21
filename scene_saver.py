import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.utils as utils
from shiboken2 import wrapInstance
import os
from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QRadioButton, QCheckBox, QComboBox, QDoubleSpinBox, QLineEdit, QTreeWidget, QTreeWidgetItem
from PySide2.QtCore import Qt, QRect

def get_maya_main_window():
    """
    Get the main Maya window as a QMainWindow instance
    """
    maya_window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(maya_window), QWidget)

class SceneSaver(QMainWindow):
    def __init__(self, parent = get_maya_main_window()):
        super(SceneSaver, self).__init__(parent)

        # Set the window title
        self.setWindowTitle("Scene Saver")
        
        # Initialize the UI
        project_type_lbl = QLabel("Project Type:")
        self.single_scene_rbtn = QRadioButton("Single Scene")
        self.single_scene_rbtn.toggled.connect(self.disable_widgets)
        self.cinematic_scene_rbtn = QRadioButton("Cinematic Scene")
        self.cinematic_scene_rbtn.toggled.connect(self.disable_widgets)
        self.episodic_scene_rbtn = QRadioButton("Episodic Scene")
        self.episodic_scene_rbtn.toggled.connect(self.disable_widgets)

        project_path_lbl = QLabel("Project Path:")
        self.project_path_le = QLineEdit()
        project_path_browse_btn = QPushButton("Browse...")
        project_path_browse_btn.clicked.connect(self.browse_project_path)

        episode_lbl = QLabel("Episode:")
        self.episode_cb = QComboBox()

        sequence_lbl = QLabel("Sequence:")
        self.sequence_cb = QComboBox()

        shot_lbl = QLabel("Shot:")
        self.shot_cb = QComboBox()

        department_lbl = QLabel("Department:")
        self.department_cb = QComboBox()
        self.department_cb.addItems(["Modeling", "Rigging", "Layout", "Animation", "Lighting", "FX"])
        self.department_cb.setCurrentIndex(0)

        tags_lbl = QLabel("Tags:")
        self.tags_cb = QComboBox()

        version_lbl = QLabel("Version:")
        self.version_dsb = QDoubleSpinBox()

        file_type_lbl = QLabel("File Type:")
        self.file_type_cb = QComboBox()
        self.file_type_cb.addItems(["*.ma", "*.mb"])
        self.file_type_cb.setCurrentIndex(0)

        bkp_prev_chkbox = QCheckBox("Backup Previous Version")

        file_name_format_lbl = QLabel("File Name Format:")
        self.file_name_format_le = QLineEdit()

        set_custom_name_format_btn = QPushButton("Set Custom")
        # set_custom_name_format_btn.clicked.connect(self.set_custom_name_format)

        file_name_lbl = QLabel("File Name:")
        self.file_name_le = QLineEdit()

        artist_name_lbl = QLabel("Artist Name:")
        self.artist_name_le = QLineEdit()

        date_lbl = QLabel("Date:")

        time_lbl = QLabel("Time:")

        foleder_structure_preview_lbl = QLabel("Folder Structure Preview:")
        self.folder_structure_preview_tw = QTreeWidget()
        self.folder_structure_preview_tw.setHeaderLabels(["Folder Structure Preview"])


        save_btn = QPushButton("Save")
        # save_btn.clicked.connect(self.save)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)

        hbox = QHBoxLayout()
        hbox.addWidget(save_btn)
        hbox.addWidget(cancel_btn)

        # Set the layout
        gbox = QGridLayout()

        gbox.addWidget(project_type_lbl, 0, 0)
        gbox.addWidget(self.single_scene_rbtn, 0, 1)
        gbox.addWidget(self.cinematic_scene_rbtn, 0, 2)
        gbox.addWidget(self.episodic_scene_rbtn, 0, 3)

        gbox.addWidget(project_path_lbl, 1, 0)
        gbox.addWidget(self.project_path_le, 2, 0, 1, 3)
        gbox.addWidget(project_path_browse_btn, 2, 3)

        gbox.addWidget(episode_lbl, 3, 0)
        gbox.addWidget(self.episode_cb, 4, 0)

        gbox.addWidget(sequence_lbl, 3, 1)
        gbox.addWidget(self.sequence_cb, 4, 1)

        gbox.addWidget(shot_lbl, 3, 2)
        gbox.addWidget(self.shot_cb, 4, 2)

        gbox.addWidget(department_lbl, 3, 3)
        gbox.addWidget(self.department_cb, 4, 3)

        gbox.addWidget(tags_lbl, 5, 0)
        gbox.addWidget(self.tags_cb, 6, 0)

        gbox.addWidget(version_lbl, 5, 1)
        gbox.addWidget(self.version_dsb, 6, 1)

        gbox.addWidget(file_type_lbl, 5, 2)
        gbox.addWidget(self.file_type_cb, 6, 2)

        gbox.addWidget(bkp_prev_chkbox, 5, 3, 2, 1)

        gbox.addWidget(file_name_format_lbl, 7, 0)
        gbox.addWidget(self.file_name_format_le, 8, 0, 1, 3)

        gbox.addWidget(set_custom_name_format_btn, 8, 3)

        gbox.addWidget(file_name_lbl, 9, 0)
        gbox.addWidget(self.file_name_le, 10, 0, 1, 3)

        gbox.addWidget(artist_name_lbl, 11, 0)
        gbox.addWidget(self.artist_name_le, 12, 0, 1, 2)

        gbox.addWidget(date_lbl, 12, 2)

        gbox.addWidget(time_lbl, 12, 3)

        vbox = QVBoxLayout()
        vbox.addWidget(foleder_structure_preview_lbl)
        vbox.addWidget(self.folder_structure_preview_tw)
        vbox.addLayout(hbox)

        hbox2 = QHBoxLayout()
        hbox2.addLayout(gbox)
        hbox2.addLayout(vbox)

        # Set the main layout
        main_layout = QWidget()
        main_layout.setLayout(hbox2)
        self.setCentralWidget(main_layout)

    def disable_widgets(self):
        """Enable/Disable widgets based on selected scene type."""
        sender = self.sender()

        if sender == self.single_scene_rbtn:
            self.episode_cb.setEnabled(False)
            self.sequence_cb.setEnabled(False)
            self.shot_cb.setEnabled(False)

        elif sender == self.cinematic_scene_rbtn:
            self.episode_cb.setEnabled(False)
            self.sequence_cb.setEnabled(True)
            self.shot_cb.setEnabled(True)
            
        elif sender == self.episodic_scene_rbtn:
            self.episode_cb.setEnabled(True)
            self.sequence_cb.setEnabled(True)
            self.shot_cb.setEnabled(True)

    def browse_project_path(self):
        """Browse project path dialog."""
        self.episode_cb.clear()

        self.ep_dict = {}
        self.sq_dict = {}
        self.sh_dict = {}


        self.project_path = cmds.fileDialog2(fileMode=3, dialogStyle=2, caption="Select Project Directory")
        if self.project_path:
            self.project_path_le.setText(self.project_path[0])
            self.populate_tree() # Populate the folder structure preview tree

    def populate_tree(self):
        """Populate the folder structure preview tree."""
        self.folder_structure_preview_tw.clear()
        root_item = QTreeWidgetItem([os.path.basename(self.project_path[0])])
        self.folder_structure_preview_tw.addTopLevelItem(root_item)
        self.add_subfolders(root_item, self.project_path[0])
        self.make_project_dict()

    def add_subfolders(self, parent_item, parent_path):
        """Add subfolders and files to the tree."""
        for item in os.listdir(parent_path):
            item_path = os.path.join(parent_path, item)

            if os.path.isdir(item_path):
                trw_item = QTreeWidgetItem([item])
                parent_item.addChild(trw_item)
                self.add_subfolders(trw_item, item_path)

    def make_project_dict(self):
        project_dict = {}
        project = os.path.basename(self.project_path[0])
        project_dict[project] = {}

        for item in os.listdir(self.project_path[0]):
            item_path = os.path.join(self.project_path[0], item)

            for ep_item in os.listdir(item_path):
                ep_item_path = os.path.join(item_path, ep_item)

                if  "ep" in ep_item.lower() and os.path.isdir(ep_item_path):
                    project_dict[project][ep_item] = {}
                    
                    for sq_item in os.listdir(ep_item_path):
                        sq_item_path = os.path.join(ep_item_path, sq_item)
                        
                        if "sq" in sq_item.lower() and os.path.isdir(sq_item_path):
                            project_dict[project][ep_item][sq_item] = {}
                        
                            for sh_item in os.listdir(sq_item_path):
                                sh_item_path = os.path.join(sq_item_path, sh_item)

                                if "sh" in sh_item.lower()and os.path.isdir(sh_item_path):
                                    project_dict[project][ep_item][sq_item][sh_item] = sh_item_path

        print(project_dict)
        return project_dict

    def update_ep_cb_list(self):
        """Update the episode combo box list"""
        

    def close(self):
        """Overriding the close method."""
        return super().close()

def scene_saver():
    global my_window
    try:
        my_window.close()
        my_window.deleteLater()
    except:
        pass

    my_window = SceneSaver()
    my_window.show()

scene_saver()