# Floating-Assistive-touch-for-Windows-PC
## Assistive-touch-Beta-v1.0

A transparent floating text entry box to perform quick actions The application is written in python that creates a floating window that always stays on top to quickly access files and folders with a predefined nickname for each file or folders.

If a new nickname is entered that does not exist in the database then a file browser is popped up to select a file or a folder for the new nickname. 

Transparency action is also added. to highlight or de-highlight double click on the text box. To move the text box click on the text entry and drag.

Planning to add more updates to perform mathematical operations and open browser links and also record keyboard macro for play back option.

To use it in your pc
Download the Toucher.py file to you local system
Now, run the following command

```
pyinstaller --onefile --noconsole Toucher.py
```
## Assistive-touch-v2.0

### Fixed bugs:
```
1. Openning multiple windows to open / close folders.
2. Fixed Openning browser to perform searches in google.
3. Removed the option of adding button to hide/display the text window.
```

### New Features:
```
1. Added unlimited macro recordings
Type Macro: var_name to start macro recording, once recording is done press 'esc' to stop
Now type exe: var_name to play back the recorded macro
2. Added display control features
Type set: color: color_names to change the color of the text-entry.
     More features coming in v3.0
3. Added ability to perform searches in google.
4. Ability to add both files/folder to perform quick access
To add new-files type add: files: file_name
To add new-folders type add: folder: file_name
```

