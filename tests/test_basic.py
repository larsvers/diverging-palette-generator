"""
Basic test to verify the installation works
"""

def test_imports():
    """Test that all required packages can be imported."""
    print("Testing imports...")
    
    try:
        import numpy as np
        print("✅ numpy imported successfully")
    except ImportError as e:
        print(f"❌ numpy import failed: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✅ matplotlib imported successfully")
    except ImportError as e:
        print(f"❌ matplotlib import failed: {e}")
        return False
    
    try:
        from colorspacious import cspace_convert
        print("✅ colorspacious imported successfully")
    except ImportError as e:
        print(f"❌ colorspacious import failed: {e}")
        return False
    
    try:
        from colorspace import divergingx_hcl, diverging_hcl
        print("✅ colorspace imported successfully")
    except ImportError as e:
        print(f"❌ colorspace import failed: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic colorspace functionality."""
    print("\nTesting basic colorspace functionality...")
    
    try:
        from colorspace import diverging_hcl
        
        # Generate a simple 5-color palette
        palette = diverging_hcl(palette="Blue-Red 3")
        colors = palette.colors(5)
        
        print(f"✅ Generated {len(colors)} colors: {colors}")
        return True
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def test_our_module():
    """Test our diverging palette generator."""
    print("\nTesting our diverging palette generator...")
    
    try:
        from diverging_palette_generator import generate_colorbrewer_style_palette
        
        # Generate a small test palette
        palette = generate_colorbrewer_style_palette(
            n=5,
            left_hue=255,
            right_hue=10,
            output_format="hex"
        )
        
        print(f"✅ Our module works! Generated {len(palette)} colors: {palette}")
        return True
    except Exception as e:
        print(f"❌ Our module test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Basic Installation Test ===")
    
    imports_ok = test_imports()
    if not imports_ok:
        print("\n❌ Import tests failed. Check your installation.")
        exit(1)
    
    basic_ok = test_basic_functionality()
    if not basic_ok:
        print("\n❌ Basic functionality tests failed.")
        exit(1)
    
    module_ok = test_our_module()
    if not module_ok:
        print("\n❌ Our module tests failed.")
        exit(1)
    
    print("\n🎉 All tests passed! The tool is ready to use.")
