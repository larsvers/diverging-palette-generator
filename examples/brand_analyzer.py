"""
Brand Color Analyzer - Extract optimal parameters from brand colors
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from diverging_palette_generator import DivergingPaletteGenerator

def analyze_brand_colors(left_brand, right_brand):
    """
    Analyze brand colors and suggest optimal parameters where brand colors 
    appear in the MID-RANGE of each arm, not as endpoints.
    """
    generator = DivergingPaletteGenerator()
    
    print("=== Brand Color Analysis ===")
    print(f"Left brand color: {left_brand}")
    print(f"Right brand color: {right_brand}")
    print()
    
    # Extract HCL values
    h1_brand, c1_brand, l1_brand = generator.hex_to_hcl(left_brand)
    h3_brand, c3_brand, l3_brand = generator.hex_to_hcl(right_brand)
    
    print("HCL Analysis:")
    print(f"  Left brand:  H={h1_brand:.1f}°, C={c1_brand:.1f}, L={l1_brand:.1f}")
    print(f"  Right brand: H={h3_brand:.1f}°, C={c3_brand:.1f}, L={l3_brand:.1f}")
    print()
    
    print("🎯 KEY INSIGHT:")
    print("Brand colors should appear in the MIDDLE of each arm, not as endpoints!")
    print(f"Brand lightness values ({l1_brand:.0f}, {l3_brand:.0f}) are too high for darkest colors.")
    print()
    
    # Calculate proper endpoint parameters
    # For brand colors to appear in mid-range, endpoints should be darker
    target_dark_lightness = 20  # Darkest colors
    target_center_lightness = 95  # Light center
    
    # Use brand hues but darker endpoint lightness
    suggested_l1 = target_dark_lightness
    suggested_l3 = target_dark_lightness
    suggested_l2 = target_center_lightness
    
    # Use slightly higher chroma at endpoints to ensure brand colors are achievable
    suggested_cmax = max(c1_brand, c3_brand) * 1.2  # 20% higher than brand chroma
    
    print("=== RECOMMENDED UI SETTINGS ===")
    print("🎛️ Set these values in your UI:")
    print()
    print("Hue Settings:")
    print(f"  Left hue: {h1_brand:.0f}° (matches left brand)")
    print(f"  Right hue: {h3_brand:.0f}° (matches right brand)")
    print()
    print("Lightness Settings:")
    print(f"  Left lightness: {suggested_l1:.0f} (DARKER than brand - creates range)")
    print(f"  Middle lightness: {suggested_l2:.0f} (light center)")
    print(f"  Right lightness: {suggested_l3:.0f} (DARKER than brand - creates range)")
    print()
    print("Chroma Settings:")
    print(f"  Left chroma: {suggested_cmax:.0f} (higher than brand to ensure coverage)")
    print(f"  Right chroma: {suggested_cmax:.0f} (higher than brand to ensure coverage)")
    print(f"  Left chroma peak: {suggested_cmax:.0f}")
    print(f"  Right chroma peak: {suggested_cmax:.0f}")
    print()
    print("Power Settings:")
    print(f"  Left lightness power: 1.0 (linear for now)")
    print(f"  Right lightness power: 1.0 (linear for now)")
    print()
    print("Other Settings:")
    print("  ✅ Check 'Classic diverging (HCL Wizard style)'")
    print("  ✅ Check 'Use neutral center'")
    print()
    
    print("💡 THEORY:")
    print("With these settings, your brand colors should appear somewhere")
    print("in the middle of each arm where their lightness values naturally fall.")
    print()
    
    # Generate test palette with these settings
    test_palette = generator.generate_palette(
        n=21,  # More colors to see brand placement better
        h1=h1_brand, h3=h3_brand,
        c1=suggested_cmax, c3=suggested_cmax,
        cmax1=suggested_cmax, cmax2=suggested_cmax,
        l1=suggested_l1, l2=suggested_l2, l3=suggested_l3,
        p2=1.0, p4=1.0,  # Linear for now
        use_classic_diverging=True,
        output_format='hex'
    )
    
    print("=== TEST PALETTE ===")
    print("Generated palette with suggested settings:")
    for i, color in enumerate(test_palette):
        print(f"  {i}: {color}")
    print()
    
    # Test proximity
    from analysis_functions import hex_to_rgb
    from colorspacious import cspace_convert
    import numpy as np
    
    def color_distance(hex1, hex2):
        """Calculate CAM02-UCS distance between two hex colors"""
        rgb1 = hex_to_rgb(hex1)
        rgb2 = hex_to_rgb(hex2)
        cam1 = cspace_convert(rgb1, "sRGB1", "CAM02-UCS")
        cam2 = cspace_convert(rgb2, "sRGB1", "CAM02-UCS")
        return np.linalg.norm(np.array(cam2) - np.array(cam1))
    
    # Find closest matches
    print("=== BRAND COLOR PROXIMITY ===")
    for brand_color, brand_name in [(left_brand, "Left"), (right_brand, "Right")]:
        min_distance = float('inf')
        closest_idx = -1
        closest_color = ""
        
        for i, pal_color in enumerate(test_palette):
            distance = color_distance(brand_color, pal_color)
            if distance < min_distance:
                min_distance = distance
                closest_idx = i
                closest_color = pal_color
        
        print(f"{brand_name} brand ({brand_color}):")
        print(f"  Closest: {closest_color} at index {closest_idx}")
        print(f"  ΔE distance: {min_distance:.1f}")
        
        if min_distance < 10:
            print("  ✅ Very close match!")
        elif min_distance < 20:
            print("  ✅ Good match")
        else:
            print("  ⚠️ Could be closer - try adjusting chroma/lightness")
        print()

if __name__ == "__main__":
    # Example with common brand colors
    analyze_brand_colors("#1E3A8A", "#DC2626")  # Blue and red
    
    print("\n" + "="*50)
    print("Copy the recommended settings above into your UI!")
    print("Then generate a 199-color palette for full analysis.")
