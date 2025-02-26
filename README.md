# Scene Saver for Maya

## Overview
Scene Saver is a Maya tool designed to simplify the saving workflow for episodic projects. It enables structured scene organization with episode, sequence, and shot selection, while supporting versioning, tagging, and customizable name formatting.

## Features
- Automatic folder structure detection
- Dynamic file naming based on user-defined formats
- Department-based folder management
- Backup and overwrite options
- Customizable file naming formats

## Installation
1. Clone this repository:
   ```bash
   git clone <repository-url>
   ```
2. Copy `scene_saver.py` into your Maya scripts directory. The default location is:
   - Windows: `C:\Users\<YourUser>\Documents\maya\<MayaVersion>\scripts`
   - macOS: `/Users/<YourUser>/Library/Preferences/Autodesk/maya/<MayaVersion>/scripts`
   - Linux: `/home/<YourUser>/maya/<MayaVersion>/scripts`

3. Place the `Maya.env` file in the appropriate Maya preferences directory:
   - Windows: `C:\Users\<YourUser>\Documents\maya\<MayaVersion>\`
   - macOS: `/Users/<YourUser>/Library/Preferences/Autodesk/maya/<MayaVersion>/`
   - Linux: `/home/<YourUser>/maya/<MayaVersion>/`

4. If you want to keep the script permanently accessible, add the script path to the `PYTHONPATH` variable inside your `Maya.env` file:
   ```
   PYTHONPATH=<path-to-your-scripts-directory>
   ```
   Example:
   ```
   PYTHONPATH=C:\Users\<YourUser>\Documents\maya\<MayaVersion>\scripts
   ```

5. If using `userSetup.mel`, place it inside your Maya scripts directory to ensure the tool initializes on startup.
6. Run the script in Maya using the following command:
   ```python
   import scene_saver
   scene_saver.open_scene_saver()
   ```

## Changing the Icon Path
By default, the icon is expected to be in the same directory as the script. If you want to place the icon elsewhere, update **line 567** in `scene_saver.py` to point to the correct path of the icon file. Example:
```
icon = os.path.join(os.path.dirname(__file__), "scene_saver_icon.png")
```
Modify this line accordingly if the icon is placed in a different location.

## Dependencies
Ensure you have the following installed:
- Autodesk Maya (Tested on Maya 2022+)
- PySide2 for UI components

## Folder Structure
The tool follows a structured folder hierarchy:
```
<Project Root>
│-- Episode_01
│   │-- Sequence_01
│   │   │-- Shot_001
│   │   │   │-- Animation
│   │   │   │-- Lighting
│   │   │   │-- FX
│-- Episode_02
    │-- Sequence_02
        │-- Shot_002
            │-- Rigging
            │-- Match Move
```

## Usage
1. Open the tool inside Maya.
2. Select your project directory.
3. Choose the episode, sequence, and shot.
4. Pick a department and set version/tag details.
5. (Optional) Define a custom naming format.
6. Save the scene using the structured naming convention.

## Custom Name Formatting
You can define custom name formats using placeholders:
- `{proj}` - Project Name
- `{ep}` - Episode
- `{sq}` - Sequence
- `{sh}` - Shot
- `{dept}` - Department
- `{tag}` - Tag
- `{ver}` - Version
- `{artist}` - Artist Name
- `{date}` - Date (ddmmyyyy)
- `{time}` - Time (hhmmss)
- `{ftype}` - File Type

### Adding a Custom Format
1. Click "Set Custom" in the tool.
2. Enter a format string, e.g., `{proj}_{sh}_{dept}_{ver}.{ftype}`.
3. Save it and use it from the dropdown menu.

## License
This tool is open-source and free to use. Modify as needed!
