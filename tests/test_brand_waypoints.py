"""
Test and develop better brand waypoint approach
"""

import sys
import os
sys.path.append('src')

from diverging_palette_generator import DivergingPaletteGenerator
import numpy as np

def test_hue_path_issue():
    """Investigate the hue interpolation issue"""
    generator = DivergingPaletteGenerator()
    
    # Blue and red brand colors
    blue = "#1E3A8A"
    red = "#DC2626"
    
    h_blue, c_blue, l_blue = generator.hex_to_hcl(blue)
    h_red, c_red, l_red = generator.hex_to_hcl(red)
    
    print(f"Blue {blue}: H={h_blue:.1f}°, C={c_blue:.1f}, L={l_blue:.1f}")
    print(f"Red {red}: H={h_red:.1f}°, C={c_red:.1f}, L={l_red:.1f}")
    print()
    
    # Calculate hue difference both ways around the circle
    diff_direct = abs(h_red - h_blue)
    diff_around = 360 - diff_direct
    
    print(f"Hue difference (direct): {diff_direct:.1f}°")
    print(f"Hue difference (around): {diff_around:.1f}°")
    print()
    
    # Test what happens if we manually adjust the red hue to be "closer"
    # Red at 35° is close to Red at 35°+360° = 395° in terms of color appearance
    # But 292° to 395° might interpolate differently
    
    print("Testing different approaches:")
    
    # Approach 1: Direct (current - wrong)
    palette1 = generator.generate_palette(
        n=7, h1=h_blue, h3=h_red, l1=l_blue, l3=l_red,
        use_classic_diverging=True, output_format='hex'
    )
    print(f"Direct: {palette1}")
    
    # Approach 2: Flip to shorter path
    h_red_adjusted = h_red + 360 if h_red < h_blue else h_red
    print(f"Adjusted red hue: {h_red_adjusted:.1f}°")
    
    palette2 = generator.generate_palette(
        n=7, h1=h_blue, h3=h_red_adjusted, l1=l_blue, l3=l_red,
        use_classic_diverging=False, output_format='hex'  # Try divergingx for manual hue
    )
    print(f"Adjusted: {palette2}")

if __name__ == "__main__":
    test_hue_path_issue()
