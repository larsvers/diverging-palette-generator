"""
Quick test to verify UI dependencies work
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_ui_imports():
    """Test that all UI dependencies can be imported."""
    print("Testing UI imports...")
    
    try:
        import streamlit as st
        print("✅ streamlit imported successfully")
    except ImportError as e:
        print(f"❌ streamlit import failed: {e}")
        return False
        
    try:
        import pandas as pd
        print("✅ pandas imported successfully")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        from diverging_palette_generator import DivergingPaletteGenerator
        from analysis_functions import get_delta_e, visualize_color_components
        print("✅ Custom modules imported successfully")
    except ImportError as e:
        print(f"❌ Custom modules import failed: {e}")
        return False
        
    return True

def test_palette_generation():
    """Test palette generation works for UI."""
    print("\nTesting palette generation for UI...")
    
    try:
        from diverging_palette_generator import DivergingPaletteGenerator
        generator = DivergingPaletteGenerator()
        
        palette = generator.generate_palette(
            n=11,
            h1=255, h3=10,
            p2=0.8, p4=0.8,
            output_format="hex"
        )
        
        print(f"✅ Generated {len(palette)} colors: {palette[:3]}...{palette[-3:]}")
        return True
        
    except Exception as e:
        print(f"❌ Palette generation failed: {e}")
        return False

def test_analysis():
    """Test analysis functions work."""
    print("\nTesting analysis functions...")
    
    try:
        from analysis_functions import get_delta_e
        
        test_palette = ['#002F70', '#615488', '#9F8EA8', '#F6F6F6', '#7E99A0']
        results = get_delta_e(test_palette, color_type="hex", show_series=False)
        
        print(f"✅ Delta E analysis: Mean={results['mean_dE']:.3f}, CV={results['cv']:.3f}")
        return True
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False

if __name__ == "__main__":
    print("=== UI Readiness Test ===")
    
    imports_ok = test_ui_imports()
    if not imports_ok:
        print("\n❌ UI imports failed. Check dependencies.")
        exit(1)
    
    palette_ok = test_palette_generation()
    if not palette_ok:
        print("\n❌ Palette generation failed.")
        exit(1)
        
    analysis_ok = test_analysis()
    if not analysis_ok:
        print("\n❌ Analysis functions failed.")
        exit(1)
    
    print("\n🎉 All UI tests passed! Ready to launch Streamlit app.")
    print("\nTo start the UI:")
    print("1. source venv/bin/activate")
    print("2. streamlit run ui/palette_builder.py")
    print("3. Open the URL shown in your browser")
