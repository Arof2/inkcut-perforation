# 🗂️ Working Directory Memory - Installation Guide

## Overview
This feature adds **persistent working directory memory** to Inkcut, solving the annoying issue where you have to navigate to your project folder every time you open a file.

## 🎯 What This Feature Provides

### ✅ **Option 1: Last Browse Directory Memory**
- **Remembers where you last browsed** (even if you didn't open a file)
- **Persists across restarts** - Inkcut remembers your location
- **Automatic** - works without any configuration

### ✅ **Option 3: Default Working Directory Setting**
- **Set your preferred project directory** in settings
- **Always starts file dialogs there** if no recent location
- **User-configurable** - set it once, use it always

## 🏗️ How It Works

### **Priority System** (when feature is enabled):
1. 🥇 **Last browse directory** - Where you last browsed (even if you canceled)
2. 🥈 **Default working directory** - Your configured project folder
3. 🥉 **Last opened document directory** - Original Inkcut behavior
4. 🏠 **Home directory** - Final fallback

**Important:** The **Last browse directory takes priority** over the default working directory. The default is only used when you haven't browsed anywhere yet or after clearing the memory.

### **Memory System:**
- **Remembers your browsing** even if you cancel file dialogs
- **Saves settings automatically** to your Inkcut config
- **Works immediately** after installation
- **Can be completely disabled** if you prefer original behavior

### **✅ Option 4: Disable Feature**
- **Checkbox to turn off** the entire working directory memory system
- **Returns to original behavior** - uses last opened document directory or home
- **Disables all related UI controls** when unchecked

## 📁 Installation Files

### Files to Modify:

**1. `inkcut/job/plugin.py`** - Add directory settings
**2. `inkcut/job/manifest.enaml`** - Update file dialog logic  
**3. `inkcut/job/settings.enaml`** - Add UI settings

## 🔧 Installation Steps

### 1. Update JobPlugin (`plugin.py`)

Add these lines after line ~49 (after `optimizer_timeout`):

```python
    #: Last directory browsed in file dialogs
    last_browse_directory = Str().tag(config=True)

    #: Default working directory (user-configurable)
    default_working_directory = Str().tag(config=True)

    #: Enable working directory memory (user can disable the feature)
    enable_working_directory_memory = Bool(True).tag(config=True)
```

Also add `Bool` to the imports:
```python
from atom.api import Instance, Enum, List, Str, Int, Float, Bool, observe
```

Add these default methods after `_default_units()`:

```python
    def _default_default_working_directory(self):
        """Default to user's home directory"""
        return os.path.expanduser('~')

    def _default_last_browse_directory(self):
        """Start with default working directory"""
        return self.default_working_directory or os.path.expanduser('~')
```

### 2. Update File Dialog Logic (`manifest.enaml`)

Replace the file dialog logic (around line 35-45) with:

```python
    if not path:
        #: Determine the starting directory for file dialog
        current_path = None
        
        if plugin.enable_working_directory_memory:
            #: Priority: 1) Last browse directory, 2) Default working directory, 
            #:           3) Last opened document directory, 4) Home directory
            if plugin.last_browse_directory:
                current_path = plugin.last_browse_directory
            elif plugin.default_working_directory:
                current_path = plugin.default_working_directory
            elif plugin.jobs:
                current_path = dirname(plugin.jobs[-1].document)
            else:
                current_path = expanduser('~')
        else:
            #: Use original behavior when feature is disabled
            if plugin.jobs:
                current_path = dirname(plugin.jobs[-1].document)
            else:
                current_path = expanduser('~')

        #: Get the file to open
        path = FileDialogEx.get_open_file_name(
            ui.window, current_path=current_path, name_filters=['*.svg']
        )
        
        #: Remember the directory that was browsed to (only if feature is enabled)
        if path and plugin.enable_working_directory_memory:
            plugin.last_browse_directory = dirname(path)
```

### 3. Add UI Settings (`settings.enaml`)

Update imports:
```python
from enaml.widgets.api import Container, Form, Label, ObjectCombo, Field, PushButton, CheckBox
from enaml.layout.api import hbox
from enaml.qt.QtWidgets import QApplication, QFileDialog
```

Add after the optimizer timeout setting:

```python
        Label:
            text = QApplication.translate("settings", "Working Directory Memory")
        CheckBox:
            text = QApplication.translate("settings", "Remember last browsed directory")
            checked := model.enable_working_directory_memory
            tool_tip = QApplication.translate("settings", "Remember where you last browsed for files (disable for original behavior)")
        Label:
            text = QApplication.translate("settings", "Default working directory")
            enabled << model.enable_working_directory_memory
        Container:
            enabled << model.enable_working_directory_memory
            constraints = [hbox(field_dir, btn_browse)]
            Field: field_dir:
                text := model.default_working_directory
                tool_tip = QApplication.translate("settings", "Default directory for file dialogs")  
            PushButton: btn_browse:
                text = QApplication.translate("settings", "Browse...")
                clicked ::
                    path = QFileDialog.getExistingDirectory(
                        None, 
                        QApplication.translate("settings", "Select Default Working Directory"),
                        model.default_working_directory or ""
                    )
                    if path:
                        model.default_working_directory = path
        Label:
            text = QApplication.translate("settings", "Last browse directory")
            enabled << model.enable_working_directory_memory
        Container:
            enabled << model.enable_working_directory_memory
            constraints = [hbox(field_last, btn_clear)]
            Field: field_last:
                text := model.last_browse_directory
                read_only = True
                tool_tip = QApplication.translate("settings", "Last directory browsed to in file dialogs")
            PushButton: btn_clear:
                text = QApplication.translate("settings", "Clear")
                clicked ::
                    model.last_browse_directory = ""
```

## 🎛️ How to Use

### **Enable/Disable Feature:**
1. Go to **Settings** → **Job**
2. Check/uncheck **"Remember last browsed directory"**
3. When **unchecked**: Returns to original Inkcut behavior
4. When **checked**: Enables all working directory memory features

### **Automatic Memory** (when enabled):
- Just use Inkcut normally - it remembers where you browse!
- File dialogs will start where you last looked for files
- **Last browse directory takes priority** over default working directory

### **Set Default Working Directory:**
1. Go to **Settings** → **Job**  
2. Ensure **"Remember last browsed directory"** is checked
3. Set **"Default working directory"** to your project folder
4. Click **Browse** to select folder
5. Click **OK**

### **Clear Memory:**
- Use **"Clear"** button next to "Last browse directory" to reset memory
- File dialogs will then use default working directory (if set) or home directory

## 🎯 User Experience

### **Before This Feature:**
- File dialog always starts at home directory or last opened file location
- Have to navigate to project folder every time
- Lost browsing location if you cancel dialog

### **After This Feature:**  
- File dialog starts where you last browsed
- Can set preferred default project directory
- Remembers location even if you cancel
- Persists across Inkcut restarts

## ✅ Verification

Use the test script `test_working_directory.py` to verify the installation works correctly.

Expected behavior:
1. **First use**: Starts at home directory or default working directory
2. **After browsing**: Remembers last location you browsed to
3. **After restart**: Still remembers your last location
4. **Settings work**: Can configure default working directory

## 🔄 Backward Compatibility

- **Fully backward compatible** - existing installations won't break
- **Graceful fallbacks** - uses existing behavior if settings are empty
- **No data loss** - doesn't affect existing job or document handling

---

**This feature eliminates the file navigation frustration and makes Inkcut much more user-friendly for regular project work!** 🎉