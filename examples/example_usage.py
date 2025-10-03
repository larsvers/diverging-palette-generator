"""
Example usage of the Diverging Palette Generator

This file demonstrates how to use the diverging palette generator to create
ColorBrewer-style palettes with power transformation controls and brand color
proximity testing.
"""

from diverging_palette_generator import (
    DivergingPaletteGenerator,
    BrandColorProximityTester,
    PaletteCurveAnalyzer,
    generate_colorbrewer_style_palette,
    test_brand_proximity_quick,
    analyze_palette_quick
)

# Example brand colors (replace with your actual brand colors)
EXAMPLE_BRAND_COLORS = [
    "#1E3A8A",  # Brand blue
    "#DC2626",  # Brand red
    "#059669",  # Brand green
    "#7C3AED",  # Brand purple
]

def example_basic_usage():
    """Basic palette generation with default ColorBrewer-style settings."""
    print("=== Basic ColorBrewer-style Palette ===")
    
    # Generate a basic blue-red diverging palette
    palette = generate_colorbrewer_style_palette(
        n=11,  # Start with small palette for demo
        left_hue=255,  # Blue
        right_hue=10,  # Red
        narrow_hat=True,  # ColorBrewer-style narrow hat
        output_format="hex"
    )
    
    print(f"Generated {len(palette)} colors:")
    for i, color in enumerate(palette):
        print(f"  {i:2d}: {color}")
    
    return palette

def example_advanced_palette():
    """Advanced palette generation with custom power transformations."""
    print("\n=== Advanced Palette with Custom Parameters ===")
    
    generator = DivergingPaletteGenerator()
    
    palette = generator.generate_palette(
        n=199,  # Full 199-color palette
        h1=255,  # Left hue (blue)
        h3=10,   # Right hue (red)
        l1=25,   # Darker ends
        l2=95,   # Bright middle
        l3=25,   # Darker ends
        p1=1.2,  # Slower chroma buildup on left
        p2=0.6,  # Very narrow lightness hat
        p3=1.2,  # Slower chroma buildup on right
        p4=0.6,  # Very narrow lightness hat
        cmax1=50,  # Moderate left chroma peak
        cmax2=50,  # Moderate right chroma peak
        output_format="hex"
    )
    
    print(f"Generated {len(palette)} colors")
    print(f"First 5: {palette[:5]}")
    print(f"Middle 5: {palette[97:102]}")  # Around index 99 (middle of 199)
    print(f"Last 5: {palette[-5:]}")
    
    return palette

def example_brand_proximity_test():
    """Demonstrate brand color proximity testing."""
    print("\n=== Brand Color Proximity Testing ===")
    
    # Generate a palette
    palette = generate_colorbrewer_style_palette(n=99, output_format="hex")
    
    # Test proximity to brand colors
    test_brand_proximity_quick(palette, EXAMPLE_BRAND_COLORS, "hex")

def example_curve_analysis():
    """Demonstrate palette curve analysis."""
    print("\n=== Palette Curve Analysis ===")
    
    # Generate two palettes for comparison
    narrow_hat_palette = generate_colorbrewer_style_palette(
        n=51, narrow_hat=True, output_format="hex"
    )
    
    wide_hat_palette = generate_colorbrewer_style_palette(
        n=51, narrow_hat=False, output_format="hex"
    )
    
    print("Analyzing narrow hat palette (ColorBrewer-style):")
    narrow_results = analyze_palette_quick(narrow_hat_palette, "hex")
    
    print(f"  Peak lightness at index: {narrow_results['peak_lightness_index']} (midpoint: {narrow_results['midpoint_index']})")
    print(f"  Hat width ratio: {narrow_results['hat_width_ratio']:.3f}")
    print(f"  Left arm monotonic: {narrow_results['left_arm_monotonic']}")
    print(f"  Right arm monotonic: {narrow_results['right_arm_monotonic']}")
    
    print("\nAnalyzing wide hat palette (Leonardo-style):")
    wide_results = analyze_palette_quick(wide_hat_palette, "hex")
    
    print(f"  Peak lightness at index: {wide_results['peak_lightness_index']} (midpoint: {wide_results['midpoint_index']})")
    print(f"  Hat width ratio: {wide_results['hat_width_ratio']:.3f}")
    print(f"  Left arm monotonic: {wide_results['left_arm_monotonic']}")
    print(f"  Right arm monotonic: {wide_results['right_arm_monotonic']}")

def example_parameter_exploration():
    """Explore different parameter combinations."""
    print("\n=== Parameter Exploration ===")
    
    generator = DivergingPaletteGenerator()
    
    # Test different power transformations
    power_combinations = [
        (0.5, "Very narrow hat"),
        (0.8, "Narrow hat (ColorBrewer-like)"),
        (1.0, "Linear"),
        (1.5, "Wide hat (Leonardo-like)"),
        (2.0, "Very wide hat")
    ]
    
    for power, description in power_combinations:
        palette = generator.generate_palette(
            n=21,  # Small palette for quick demo
            p2=power,  # Left lightness power
            p4=power,  # Right lightness power
            output_format="hex"
        )
        
        # Quick analysis without plots
        analyzer = PaletteCurveAnalyzer()
        results = analyzer.analyze_palette_curves(palette, "hex", show_plot=False)
        
        print(f"Power {power:3.1f} ({description}):")
        print(f"  Hat width ratio: {results['hat_width_ratio']:.3f}")
        print(f"  Peak at index: {results['peak_lightness_index']} (center: {results['midpoint_index']})")

def example_export_for_colab():
    """Generate and export a palette for use in Colab."""
    print("\n=== Export for Colab ===")
    
    # Generate a full 199-color palette
    palette_hex = generate_colorbrewer_style_palette(
        n=199,
        left_hue=220,  # Different blue
        right_hue=350,  # Pink-red
        narrow_hat=True,
        output_format="hex"
    )
    
    # Also get as RGB strings for compatibility with existing functions
    generator = DivergingPaletteGenerator()
    palette_rgb_strings = generator.generate_palette(
        n=199,
        h1=220,
        h3=350,
        p2=0.7,
        p4=0.7,
        output_format="rgb_strings"
    )
    
    print("Generated palettes for Colab import:")
    print(f"Hex format: {len(palette_hex)} colors")
    print(f"RGB strings format: {len(palette_rgb_strings)} colors")
    
    # Show how to save to file
    with open("/Users/lars/devlocal/flourish/colour-diverging-tool/palette_export.txt", "w") as f:
        f.write("# Hex colors\n")
        f.write(str(palette_hex))
        f.write("\n\n# RGB strings\n")
        f.write(str(palette_rgb_strings))
    
    print("Saved to palette_export.txt")
    
    return palette_hex, palette_rgb_strings

if __name__ == "__main__":
    # Run all examples
    basic_palette = example_basic_usage()
    advanced_palette = example_advanced_palette()
    example_brand_proximity_test()
    example_curve_analysis()
    example_parameter_exploration()
    example_export_for_colab()
    
    print("\n=== Summary ===")
    print("All examples completed successfully!")
    print("You can now import these functions into your Colab notebook.")
