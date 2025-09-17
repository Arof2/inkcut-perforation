#!/usr/bin/env python3
"""
Simple test to see if our perforation filter causes issues
"""

def test_imports():
    """Test if we can import our perforation filter"""
    try:
        from inkcut.device.filters.perforation import PerforationFilter, PerforationConfig
        print("OK: Perforation filter imports successfully")
        return True
    except Exception as e:
        print(f"ERROR: Import failed: {e}")
        return False

def test_instantiation():
    """Test if we can create instances"""
    try:
        from inkcut.device.filters.perforation import PerforationFilter, PerforationConfig
        
        config = PerforationConfig()
        filter_instance = PerforationFilter()
        print("OK: Perforation filter instantiates successfully")
        return True
    except Exception as e:
        print(f"ERROR: Instantiation failed: {e}")
        return False

def test_basic_functionality():
    """Test basic filter functionality"""
    try:
        from inkcut.device.filters.perforation import PerforationFilter, PerforationConfig
        
        config = PerforationConfig()
        config.cut_length = 5.0
        config.bridge_length = 2.0
        
        filter_instance = PerforationFilter()
        filter_instance.config = config
        
        # Test with empty polypath
        result = filter_instance.apply_to_polypath([])
        print("OK: Basic functionality works")
        return True
    except Exception as e:
        print(f"ERROR: Basic functionality failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing perforation filter...")
    
    if test_imports():
        if test_instantiation():
            test_basic_functionality()
    
    print("Test completed.")