#!/usr/bin/env python3
"""
Test working directory functionality
"""

def test_imports():
    """Test if we can import JobPlugin with new settings"""
    try:
        from inkcut.job.plugin import JobPlugin
        print("OK: JobPlugin imports successfully")
        return True
    except Exception as e:
        print(f"ERROR: Import failed: {e}")
        return False

def test_settings_exist():
    """Test if new settings exist on JobPlugin"""
    try:
        from inkcut.job.plugin import JobPlugin
        
        plugin = JobPlugin()
        
        # Check if new attributes exist
        assert hasattr(plugin, 'last_browse_directory'), "Missing last_browse_directory"
        assert hasattr(plugin, 'default_working_directory'), "Missing default_working_directory"
        assert hasattr(plugin, 'enable_working_directory_memory'), "Missing enable_working_directory_memory"
        
        print("OK: All new settings exist on JobPlugin")
        return True
    except Exception as e:
        print(f"ERROR: Settings test failed: {e}")
        return False

def test_default_values():
    """Test default values for new settings"""
    try:
        from inkcut.job.plugin import JobPlugin
        import os
        
        plugin = JobPlugin()
        
        # Check default values
        default_working_dir = plugin.default_working_directory
        last_browse_dir = plugin.last_browse_directory
        memory_enabled = plugin.enable_working_directory_memory
        
        print(f"Default working directory: {default_working_dir}")
        print(f"Last browse directory: {last_browse_dir}")
        print(f"Memory enabled: {memory_enabled}")
        
        # Should default to home directory
        home_dir = os.path.expanduser('~')
        assert default_working_dir == home_dir, f"Expected {home_dir}, got {default_working_dir}"
        assert memory_enabled == True, f"Expected memory enabled by default"
        
        print("OK: Default values are correct")
        return True
    except Exception as e:
        print(f"ERROR: Default values test failed: {e}")
        return False

def test_settings_ui():
    """Test if settings UI imports correctly"""
    try:
        # This will test if the enaml file compiles correctly
        import enaml
        with enaml.imports():
            from inkcut.job.settings import JobSettingsPage
        
        print("OK: Settings UI imports successfully")
        return True
    except Exception as e:
        print(f"ERROR: Settings UI test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing working directory feature...")
    
    success = True
    
    success &= test_imports()
    if success:
        success &= test_settings_exist()
    if success:
        success &= test_default_values()
    if success:
        success &= test_settings_ui()
    
    if success:
        print("\nOK: All tests passed! Working directory feature is ready.")
    else:
        print("\nERROR: Some tests failed.")
    
    print("Test completed.")