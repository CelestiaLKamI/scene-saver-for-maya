import maya.cmds as cmds
import maya.OpenMayaUI as omui
import maya.utils as utils
from shiboken2 import wrapInstance
import os
from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QRadioButton, QCheckBox, QComboBox, QDoubleSpinBox, QLineEdit, QTreeWidget, QTreeWidgetItem
from PySide2.QtCore import Qt, QRect, QTimer
from datetime import datetime as dt
import json

def get_maya_main_window():
    """
    Get the main Maya window as a QMainWindow instance
    """
    maya_window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(maya_window), QWidget)

class CustomNameFormat(QMainWindow):
    def __init__(self, parent = get_maya_main_window()):
        super(CustomNameFormat, self).__init__(parent)

        self.setWindowTitle("Add Custom name format")
        self.setMinimumWidth(500)

        self.file_path = os.path.join(os.path.expanduser("~"), "file_name_formats.json")

        add_format_lbl = QLabel("Add Custom File Name Format:")
        self.add_format_le = QLineEdit()

        add_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")

        add_btn.clicked.connect(self.add_format_data)
        cancel_btn.clicked.connect(self.close)
        
        layout = QVBoxLayout()
        layout.addWidget(add_format_lbl)
        layout.addWidget(self.add_format_le)
        layout.addWidget(add_btn)
        layout.addWidget(cancel_btn)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def add_format_data(self):
        name_format = self.add_format_le.text().strip()
        if name_format:
            data = self.load_existing_data()
            if name_format not in data["formats"]:
                data["formats"].append(name_format)
                self.save_data(data)
                cmds.inViewMessage(amg='Custom format saved successfully!', pos='topCenter', fade=True)
            else:
                cmds.inViewMessage(amg='Format already exists!', pos='topCenter', fade=True)
        else:
            cmds.inViewMessage(amg='Input is empty!', pos='topCenter', fade=True)
    
    def load_existing_data(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return {"formats": []}
        return {"formats": []}
    
    def save_data(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

def set_custom_name_format_window():
    global name_format_window

    if 'name_format_window' in globals() and name_format_window is not None:
        try:
            name_format_window.close()
            name_format_window.deleteLater()
        except:
            pass

    name_format_window = CustomNameFormat()
    name_format_window.show()

class SceneSaver(QMainWindow):
    def __init__(self, parent = get_maya_main_window()):
        super(SceneSaver, self).__init__(parent)

        # Set the window title
        self.setWindowTitle("Scene Saver")
        self.setMinimumWidth(900)
        
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
        self.department_cb.addItems(["Modeling", "Rigging", "Pre-Vis", "Layout", "Animation", "Lighting", "Match Move", "FX"])
        self.department_cb.setCurrentIndex(0)

        tags_lbl = QLabel("Tags:")
        self.tags_cb = QComboBox()
        self.tags_cb.addItems(["WIP", "RFR", "APP", "REV", "RFT", "RFRD", "RDC", "RFC", "RTP", "PUB", "FNL"])

        version_lbl = QLabel("Version:")
        self.version_dsb = QDoubleSpinBox()

        file_type_lbl = QLabel("File Type:")
        self.file_type_cb = QComboBox()
        self.file_type_cb.addItems(["*.ma", "*.mb"])
        self.file_type_cb.setCurrentIndex(0)

        bkp_prev_chkbox = QCheckBox("Backup Previous Version")

        file_name_format_lbl = QLabel("File Name Format:")
        self.file_name_format_cb = QComboBox()

        set_custom_name_format_btn = QPushButton("Set Custom")
        set_custom_name_format_btn.clicked.connect(self.set_custom_name_format)

        file_name_lbl = QLabel("File Name:")
        self.file_name_le = QLineEdit()

        artist_name_lbl = QLabel("Artist Name:")
        self.artist_name_le = QLineEdit()
        self.artist_name_le.setReadOnly(True)

        self.date_lbl = QLabel()
        self.date_lbl.setAlignment(Qt.AlignCenter)
        self.time_lbl = QLabel()
        self.time_lbl.setAlignment(Qt.AlignCenter)

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
        gbox.addWidget(self.file_name_format_cb, 8, 0, 1, 3)

        gbox.addWidget(set_custom_name_format_btn, 8, 3)

        gbox.addWidget(file_name_lbl, 9, 0)
        gbox.addWidget(self.file_name_le, 10, 0, 1, 3)

        gbox.addWidget(artist_name_lbl, 11, 0)
        gbox.addWidget(self.artist_name_le, 12, 0, 1, 2)

        gbox.addWidget(self.date_lbl, 12, 2)

        gbox.addWidget(self.time_lbl, 12, 3)

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

        self.update_date_time()
        self.update_file_name_format_cb()
        self.update_artist()
        self.create_file_name()

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
        self.project_dict = {}
        project = os.path.basename(self.project_path[0])
        self.project_dict[project] = {}

        for item in os.listdir(self.project_path[0]):
            item_path = os.path.join(self.project_path[0], item)

            for ep_item in os.listdir(item_path):
                ep_item_path = os.path.join(item_path, ep_item)

                if  "ep" in ep_item.lower() and os.path.isdir(ep_item_path):
                    self.project_dict[project][ep_item] = {}
                    
                    for sq_item in os.listdir(ep_item_path):
                        sq_item_path = os.path.join(ep_item_path, sq_item)
                        
                        if "sq" in sq_item.lower() and os.path.isdir(sq_item_path):
                            self.project_dict[project][ep_item][sq_item] = {}
                        
                            for sh_item in os.listdir(sq_item_path):
                                sh_item_path = os.path.join(sq_item_path, sh_item)

                                if "sh" in sh_item.lower()and os.path.isdir(sh_item_path):
                                    self.project_dict[project][ep_item][sq_item][sh_item] = sh_item_path

        print(self.project_dict)
        self.update_ep_cb_list()

    def update_ep_cb_list(self):
        """Update the episode combo box list"""
        self.episode_cb.clear()
        self.sq_dict = {}
        self.sh_dict = {}
        
        if self.project_dict:
            self.project_name = next(iter(self.project_dict))
            episodes = self.project_dict[self.project_name].keys()

            if episodes:
                self.episode_cb.addItems(episodes)
                self.episode_cb.currentIndexChanged.connect(self.update_sq_cb_list)

                self.episode_cb.setCurrentIndex(0)
                self.update_sq_cb_list()

    def update_sq_cb_list(self):
        """Update the sequence combo box list"""
        self.sequence_cb.clear()
        
        self.selected_ep = self.episode_cb.currentText()
        if self.selected_ep in self.project_dict[self.project_name]:
            sequences = self.project_dict[self.project_name][self.selected_ep].keys()

            if sequences:
                self.sequence_cb.addItems(sequences)
                self.sequence_cb.currentIndexChanged.connect(self.update_sh_cb_list)
                self.sequence_cb.setCurrentIndex(0)

                self.update_sh_cb_list()

    def update_sh_cb_list(self):
        """Update the shot combo box list"""
        self.shot_cb.clear()

        self.selected_sq = self.sequence_cb.currentText()
        if self.selected_sq in self.project_dict[self.project_name][self.selected_ep]:
            shots = self.project_dict[self.project_name][self.selected_ep][self.selected_sq].keys()
            self.shot_cb.addItems(shots)

        if self.shot_cb:
            self.shot_cb.setCurrentIndex(0)
            self.shot_cb.currentIndexChanged.connect(self.create_file_name)

    def update_file_name_format_cb(self):
        """Update the file naming format combo box list and save to JSON as a dictionary"""
        
        default_formats = [
            "{proj}_{dept}_{ver}.{ftype}",
            "{proj}_{sh}_{ver}.{ftype}",
            "{dept}_{tag}_{ver}.{ftype}",
            "{sh}_{dept}_{tag}_{ver}.{ftype}",
            "{proj}_{sh}_{dept}_bkp_{ver}.{ftype}",
            "{proj}_{sh}_{dept}_{artist}_{ver}.{ftype}",
            "{proj}_{sh}_{dept}_{date}_{ver}.{ftype}",
            "{proj}_{sq}_{sh}_render_{ver}.{ftype}",
            "{proj}_{sh}_final_render_{date}.{ftype}",
            "{proj}_{sq}_{sh}_{dept}_bkp_{date}.{ftype}",
            "{sq}_{sh}_{dept}_{artist}_{tag}_{ver}.{ftype}",
            "{proj}_{sq}_{sh}_{dept}_{tag}_{ver}.{ftype}",
            "{proj}_{ep}_{sq}_{sh}_{dept}_{ver}.{ftype}",
            "{proj}_{ep}_{sq}_{sh}_{dept}_{tag}_{ver}.{ftype}",
            "{proj}_{sq}_{sh}_{dept}_{artist}_{date}_{time}.{ftype}",
            "{proj}_{ep}_{sq}_{sh}_{tag}_{dept}_{artist}_{date}_{time}_{ver}.{ftype}"
        ]
        
        file_path = os.path.join(os.path.expanduser("~"), "file_name_formats.json")

        # Load existing formats if the file exists
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as file:
                    existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = {"formats": []}
        else:
            existing_data = {"formats": []}

        # Merge default formats with user-added formats, avoiding duplicates
        merged_formats = list(set(default_formats + existing_data.get("formats", [])))
        existing_data["formats"] = merged_formats

        # Save the merged formats back to the JSON file as a dictionary
        with open(file_path, "w") as file:
            json.dump(existing_data, file, indent=4)

        # Update the combo box
        self.file_name_format_cb.clear()
        self.file_name_format_cb.addItems(merged_formats)

        # if self.file_name_format_cb:
        #     self.file_name_format_cb.setCurrentIndex(0)
        self.file_name_format_cb.currentIndexChanged.connect(self.create_file_name)

    def backup_previous(self):
        """This will backup any files existing with same values from the widgets"""
        

    def set_custom_name_format(self):
        set_custom_name_format_window()
        QTimer.singleShot(500, self.update_file_name_format_cb)

    def update_artist(self):
        """Update the artist line edit with the artist name"""
        self.artist_name = os.environ.get("USER") or os.environ.get("USERNAME")
        self.artist_name_le.setText(self.artist_name)

    def update_date_time(self):
        """Update the date and time label at the bottom of the UI according to the PC"""
        now = dt.now()
        
        self.formatted_date = now.strftime("%d/%m/%Y")
        self.formatted_time = now.strftime("%H:%M:%S")

        self.date_lbl.setText(self.formatted_date)
        self.time_lbl.setText(self.formatted_time)

        QTimer.singleShot(1000, self.update_date_time)

    def create_file_name(self):
        """Creates the file name based on the values set on the widgets by the user"""
        self.file_name_le.clear()

        proj = os.path.basename(self.project_path_le.text()).replace(" ", "")
        ep = self.episode_cb.currentText()
        sq = self.sequence_cb.currentText()
        sh = self.shot_cb.currentText()
        tag = self.tags_cb.currentText() 
        dept = self.department_cb.currentText()
        artist = self.artist_name_le.text()
        date = self.date_lbl.text().replace("/", "")
        time = self.time_lbl.text().replace(":", "")
        ver = self.version_dsb.value()
        ftype = self.file_type_cb.currentText()

        selected_name_format = self.file_name_format_cb.currentText()
        
        file_name = selected_name_format.format(proj=proj, ep=ep, sq=sq, sh=sh, tag=tag, dept=dept,
        artist=artist, date=date, time=time, ver=ver, ftype=ftype)

        self.file_name_le.setText(file_name)

    def close(self):
        """Overriding the close method."""
        return super().close()

def scene_saver():
    global scene_saver_window

    if 'name_format_window' in globals() and scene_saver_window is not None:
        try:
            scene_saver_window.close()
            scene_saver_window.deleteLater()
        except:
            pass

    scene_saver_window = SceneSaver()
    scene_saver_window.show()

scene_saver()