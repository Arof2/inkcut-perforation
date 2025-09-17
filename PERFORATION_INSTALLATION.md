# Inkcut Perforation Feature Installation Guide

## Overview
This perforation feature adds FlexCut-style perforated cutting to Inkcut, allowing you to create cuts with alternating cut and bridge segments. This is perfect for:
- Sewing pattern cutting (patterns stay connected until removed)
- Stencil making
- Paper crafting
- Any application where you need pieces to remain connected

## What This Feature Does
- **Splits continuous paths** into alternating cut and bridge segments
- **Configurable cut length** (how long each cut segment should be)
- **Configurable bridge length** (how long each uncut gap should be)
- **Start with cut or bridge** option
- **Works with all supported plotters/cutters** (no firmware changes needed)
- **Uses standard PU/PD commands** for universal compatibility

## Installation Steps

### 1. Files to Copy
Copy these 3 files to your Inkcut installation:

**File 1: `inkcut/device/filters/perforation.py`**
- This is the main filter implementation

**File 2: Update `inkcut/device/filters/view.enaml`**  
- Add the PerforationConfigView to the end of this file

**File 3: Update `inkcut/device/filters/manifest.enaml`**
- Add the perforation factory functions and filter registration

### 2. File Contents

#### A. Create `perforation.py` 
Create `inkcut/device/filters/perforation.py` with the complete implementation.

#### B. Update `view.enaml`
Add this to the end of `inkcut/device/filters/view.enaml`:

```python
enamldef PerforationConfigView(Container):
    attr model
    padding = 0
    Form:
        Label:
            text = QApplication.translate("filters", "Cut length")
        DoubleSpinBox:
            tool_tip = QApplication.translate("filters", "Length of each cut segment")
            minimum = 0.1
            decimals = 2
            single_step = 0.5
            suffix << " "+model.units
            value << to_unit(model.cut_length, model.units)
            value ::
                model.cut_length = from_unit(change['value'], model.units)
        Label:
            text = QApplication.translate("filters", "Bridge length")
        DoubleSpinBox:
            tool_tip = QApplication.translate("filters", "Length of each uncut bridge (pen up)")
            minimum = 0.1
            decimals = 2
            single_step = 0.5
            suffix << " "+model.units
            value << to_unit(model.bridge_length, model.units)
            value ::
                model.bridge_length = from_unit(change['value'], model.units)
        Label:
            text = QApplication.translate("filters", "Start with cut")
        CheckBox:
            tool_tip = QApplication.translate("filters", "Start perforation with a cut (checked) or bridge (unchecked)")
            checked := model.start_with_cut
```

#### C. Update `manifest.enaml`
Add these functions after the existing factory functions in `inkcut/device/filters/manifest.enaml`:

```python
def perforation_factory():
    from .perforation import PerforationFilter
    return PerforationFilter()

def perforation_config_view():
    with enaml.imports():
        from .view import PerforationConfigView
    return PerforationConfigView
```

And add this DeviceFilter registration in the FiltersManifest section:

```python
        DeviceFilter:
            id = 'perforation'
            name = QApplication.translate("filters", "Perforation")
            factory = perforation_factory
            config_view = perforation_config_view
```

### 3. Restart Inkcut
After copying the files, restart Inkcut completely.

## How to Use

### 1. Access Settings
1. Open Inkcut
2. Go to **Settings** (Einstellungen in German)
3. Navigate to **Device** (Gerät)
4. Find **Filters** section

### 2. Enable Perforation
1. Look for **"Perforation"** in the filters list
2. **Check the box** to enable it
3. Configure the settings:
   - **Cut length**: e.g., 5.0 mm (how long each cut should be)
   - **Bridge length**: e.g., 2.0 mm (how long each gap should be)
   - **Start with cut**: Check to start cutting, uncheck to start with bridge

### 3. Recommended Settings
For sewing patterns:
- **Cut length**: 3-5 mm
- **Bridge length**: 1-2 mm
- **Start with cut**: Checked

For stencils:
- **Cut length**: 2-3 mm
- **Bridge length**: 0.5-1 mm
- **Start with cut**: Checked

## How It Works Technically

1. **Path Analysis**: The filter analyzes each continuous cutting path
2. **Segmentation**: Splits paths into alternating cut/bridge segments based on your settings
3. **Command Generation**: Creates standard PU (pen up) and PD (pen down) commands
4. **Universal Compatibility**: Works with any plotter/cutter that supports HPGL, G-code, etc.

## Troubleshooting

### Filter Not Appearing
- Ensure all files are copied correctly
- Check file permissions
- Restart Inkcut completely
- Check the log files in `~/.config/inkcut/logs/inkcut.txt`

### Cuts Not Perforated
- Verify the filter is **enabled** (checked) in settings
- Check that cut length and bridge length are both > 0
- Ensure your paths are long enough to be perforated
- Try with simple test shapes first

### Performance Issues
- For very complex paths, perforation may take longer
- Consider simplifying paths or increasing segment lengths
- The filter includes safety checks to prevent crashes

## Technical Details

- **Language**: Python 3.7+
- **Dependencies**: Uses existing Inkcut dependencies (Qt, Atom, etc.)
- **Performance**: Optimized with error handling and fallbacks
- **Compatibility**: Works with all Inkcut-supported devices
- **Safety**: Includes comprehensive error handling

## Support

This is a community-contributed feature. For issues:
1. Check the Inkcut logs
2. Test with simple shapes first
3. Verify your Inkcut installation is working properly
4. Report issues to the Inkcut community forums

## License
GPL v3 (same as Inkcut)