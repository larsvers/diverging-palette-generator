"""
Diverging Color Palette Generator

A tool for creating ColorBrewer-style diverging palettes with precise control over
lightness and chroma curves using power transformations. Based on R's colorspace
package with additional brand color proximity testing.
"""

import numpy as np
import matplotlib.pyplot as plt
from colorspacious import cspace_convert
from typing import List, Tuple, Dict, Optional, Union
import warnings

try:
    from colorspace import divergingx_hcl, diverging_hcl
    COLORSPACE_AVAILABLE = True
except ImportError:
    COLORSPACE_AVAILABLE = False
    warnings.warn(
        "colorspace package not available. Install with: pip install colorspace\n"
        "Some functions will not work without this dependency."
    )


class DivergingPaletteGenerator:
    """
    Generate diverging color palettes with precise control over lightness and chroma curves.
    
    This class provides ColorBrewer-style diverging palettes using the colorspace package
    with additional features for brand color proximity testing and curve analysis.
    """
    
    def __init__(self):
        if not COLORSPACE_AVAILABLE:
            raise ImportError("colorspace package is required. Install with: pip install colorspace")
    
    def generate_palette(
        self,
        n: int = 199,
        h1: float = 255,  # left hue (blue)
        h3: float = 10,   # right hue (red)
        h2: Optional[float] = None,  # middle hue (None = neutral gray)
        c1: float = 50,   # left chroma
        c3: float = 50,   # right chroma
        c2: Optional[float] = None,  # middle chroma (None = 0 for neutral)
        l1: float = 20,   # left lightness
        l2: float = 97,   # middle lightness (peak)
        l3: float = 20,   # right lightness
        p1: float = 1.0,  # left arm chroma power
        p2: float = 0.8,  # left arm lightness power
        p3: float = 1.0,  # right arm chroma power
        p4: float = 0.8,  # right arm lightness power
        cmax1: float = 60,  # left chroma peak
        cmax2: float = 60,  # right chroma peak
        fixup: bool = True,  # correct out-of-gamut colors
        output_format: str = "hex",  # "hex", "rgb", or "rgb_strings"
        use_classic_diverging: bool = True  # Use diverging_hcl instead of divergingx_hcl
    ) -> List[str]:
        """
        Generate a diverging color palette with power transformation controls.
        
        Args:
            n: Number of colors in the palette (odd numbers recommended for clear midpoint)
            h1, h3: Hue values for left and right arms (0-360)
            h2: Middle hue (None for neutral gray midpoint)
            c1, c3: Chroma values for left and right ends
            c2: Middle chroma (None defaults to 0 for neutral)
            l1, l2, l3: Lightness values (left, middle, right)
            p1: Power transformation for left arm chroma (< 1 = slower start, > 1 = faster start)
            p2: Power transformation for left arm lightness (< 1 = narrower hat)
            p3: Power transformation for right arm chroma
            p4: Power transformation for right arm lightness
            cmax1, cmax2: Maximum chroma values for smoother peaks
            fixup: Whether to correct out-of-gamut colors
            output_format: Output format ("hex", "rgb", "rgb_strings")
            use_classic_diverging: Use classic diverging_hcl (True) or flexible divergingx_hcl (False)
            
        Returns:
            List of color values in specified format
        """
        
        if use_classic_diverging and h2 is None:
            # Use classic diverging_hcl for HCL Wizard-style palettes
            # This maintains constant hues on each arm with neutral center
            palette = diverging_hcl(
                h=[h1, h3],  # Just the two end hues
                c=max(cmax1, cmax2),  # Use maximum chroma value (this is the peak chroma)
                l=[l1, l2],  # End lightness and peak lightness
                power=p2,    # Use lightness power transformation
                fixup=fixup
            )
        else:
            # Use flexible divergingx_hcl for multi-hue palettes
            # For neutral midpoint, use a middle hue that's between the two ends
            if h2 is None:
                # Calculate a neutral hue between h1 and h3
                h2 = (h1 + h3) / 2.0 if abs(h1 - h3) < 180 else ((h1 + h3 + 360) / 2.0) % 360
            
            if c2 is None:
                c2 = 0  # Neutral center has zero chroma
                
            h_vals = [h1, h2, h3]
            c_vals = [c1, c2, c3]
            l_vals = [l1, l2, l3]
            power_vals = [p1, p2, p3, p4]
            
            # Create palette object
            palette = divergingx_hcl(
                h=h_vals,
                c=c_vals, 
                l=l_vals,
                power=power_vals,
                cmax=max(cmax1, cmax2),  # Python version uses single cmax
                fixup=fixup
            )
        
        # Get colors
        colors = palette.colors(n)
        
        if output_format == "hex":
            return colors
        elif output_format == "rgb":
            # Convert hex to RGB tuples (0-1 range)
            rgb_list = []
            for color in colors:
                hex_color = color.lstrip('#')
                r = int(hex_color[0:2], 16) / 255.0
                g = int(hex_color[2:4], 16) / 255.0
                b = int(hex_color[4:6], 16) / 255.0
                rgb_list.append((r, g, b))
            return rgb_list
        elif output_format == "rgb_strings":
            # Convert hex to CSS-style rgb() strings
            rgb_strings = []
            for color in colors:
                hex_color = color.lstrip('#')
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                rgb_strings.append(f"rgb({r}, {g}, {b})")
            return rgb_strings
        else:
            raise ValueError("output_format must be 'hex', 'rgb', or 'rgb_strings'")
    
    def generate_simple_palette(
        self,
        n: int = 199,
        palette_name: str = "Blue-Red 3",
        output_format: str = "hex"
    ) -> List[str]:
        """
        Generate a simple diverging palette using built-in presets.
        
        Args:
            n: Number of colors
            palette_name: Name of preset palette (e.g., "Blue-Red 3", "Green-Brown", etc.)
            output_format: Output format ("hex", "rgb", "rgb_strings")
            
        Returns:
            List of color values in specified format
        """
        palette = diverging_hcl(palette=palette_name)
        colors = palette.colors(n)
        
        if output_format == "hex":
            return colors
        elif output_format == "rgb":
            # Convert hex to RGB tuples (0-1 range)
            rgb_list = []
            for color in colors:
                hex_color = color.lstrip('#')
                r = int(hex_color[0:2], 16) / 255.0
                g = int(hex_color[2:4], 16) / 255.0
                b = int(hex_color[4:6], 16) / 255.0
                rgb_list.append((r, g, b))
            return rgb_list
        elif output_format == "rgb_strings":
            # Convert hex to CSS-style rgb() strings
            rgb_strings = []
            for color in colors:
                hex_color = color.lstrip('#')
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                rgb_strings.append(f"rgb({r}, {g}, {b})")
            return rgb_strings
        else:
            raise ValueError("output_format must be 'hex', 'rgb', or 'rgb_strings'")


class BrandColorProximityTester:
    """
    Test proximity of palette colors to brand colors in CAM02-UCS space.
    """
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[float, float, float]:
        """Convert hex string to RGB tuple in [0..1] range."""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return (r / 255.0, g / 255.0, b / 255.0)
    
    @staticmethod
    def hex_to_cam02ucs(hex_color: str) -> np.ndarray:
        """Convert hex string to CAM02-UCS coordinates."""
        rgb = BrandColorProximityTester.hex_to_rgb(hex_color)
        return cspace_convert(rgb, "sRGB1", "CAM02-UCS")
    
    def test_brand_proximity(
        self,
        palette: List[str],
        brand_colors: List[str],
        palette_format: str = "hex",
        threshold: float = 10.0
    ) -> Dict:
        """
        Test proximity of palette colors to brand colors.
        
        Args:
            palette: List of palette colors
            brand_colors: List of brand colors in hex format
            palette_format: Format of palette colors ("hex" or "rgb_strings")
            threshold: ΔE threshold for proximity warning
            
        Returns:
            Dictionary with proximity analysis results
        """
        # Convert brand colors to CAM02-UCS
        brand_cam02ucs = []
        for brand_color in brand_colors:
            brand_cam02ucs.append(self.hex_to_cam02ucs(brand_color))
        
        # Convert palette colors to CAM02-UCS
        palette_cam02ucs = []
        if palette_format == "hex":
            for color in palette:
                palette_cam02ucs.append(self.hex_to_cam02ucs(color))
        elif palette_format == "rgb_strings":
            import re
            for color in palette:
                match = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", color)
                if match:
                    r, g, b = map(int, match.groups())
                    rgb = (r / 255.0, g / 255.0, b / 255.0)
                    cam02ucs = cspace_convert(rgb, "sRGB1", "CAM02-UCS")
                    palette_cam02ucs.append(cam02ucs)
        
        # Find closest palette color to each brand color
        results = {
            "brand_colors": brand_colors,
            "closest_matches": [],
            "min_distances": [],
            "proximity_warnings": []
        }
        
        for i, (brand_color, brand_cam) in enumerate(zip(brand_colors, brand_cam02ucs)):
            min_distance = float('inf')
            closest_index = -1
            
            for j, palette_cam in enumerate(palette_cam02ucs):
                distance = np.linalg.norm(np.array(palette_cam) - np.array(brand_cam))
                if distance < min_distance:
                    min_distance = distance
                    closest_index = j
            
            results["closest_matches"].append({
                "brand_color": brand_color,
                "closest_palette_color": palette[closest_index],
                "palette_index": closest_index,
                "distance": min_distance
            })
            results["min_distances"].append(min_distance)
            
            if min_distance < threshold:
                results["proximity_warnings"].append({
                    "brand_color": brand_color,
                    "palette_color": palette[closest_index],
                    "distance": min_distance,
                    "message": f"Brand color {brand_color} is very close (ΔE={min_distance:.2f}) to palette color at index {closest_index}"
                })
        
        return results
    
    def print_proximity_report(self, proximity_results: Dict) -> None:
        """Print a formatted proximity analysis report."""
        print("Brand Color Proximity Analysis")
        print("=" * 50)
        
        for match in proximity_results["closest_matches"]:
            print(f"Brand: {match['brand_color']}")
            print(f"  Closest palette color: {match['closest_palette_color']} (index {match['palette_index']})")
            print(f"  ΔE distance: {match['distance']:.3f}")
            print()
        
        if proximity_results["proximity_warnings"]:
            print("⚠️  Proximity Warnings:")
            for warning in proximity_results["proximity_warnings"]:
                print(f"  {warning['message']}")
        else:
            print("✅ No proximity conflicts detected")


class PaletteCurveAnalyzer:
    """
    Analyze lightness and chroma curves of diverging palettes.
    """
    
    @staticmethod
    def analyze_palette_curves(
        palette: List[str],
        palette_format: str = "hex",
        show_plot: bool = True
    ) -> Dict:
        """
        Analyze lightness and chroma curves of a palette.
        
        Args:
            palette: List of palette colors
            palette_format: Format of palette colors ("hex" or "rgb_strings")
            show_plot: Whether to display plots
            
        Returns:
            Dictionary with curve analysis results
        """
        # Convert to CAM02-UCS
        cam02ucs_colors = []
        if palette_format == "hex":
            for color in palette:
                rgb = BrandColorProximityTester.hex_to_rgb(color)
                cam02ucs = cspace_convert(rgb, "sRGB1", "CAM02-UCS")
                cam02ucs_colors.append(cam02ucs)
        elif palette_format == "rgb_strings":
            import re
            for color in palette:
                match = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", color)
                if match:
                    r, g, b = map(int, match.groups())
                    rgb = (r / 255.0, g / 255.0, b / 255.0)
                    cam02ucs = cspace_convert(rgb, "sRGB1", "CAM02-UCS")
                    cam02ucs_colors.append(cam02ucs)
        
        # Extract J', a', b' components
        J = [color[0] for color in cam02ucs_colors]
        a = [color[1] for color in cam02ucs_colors]
        b = [color[2] for color in cam02ucs_colors]
        
        # Calculate chroma and hue
        C = [np.sqrt(x*x + y*y) for x, y in zip(a, b)]
        H = [np.degrees(np.arctan2(y, x)) % 360 for x, y in zip(a, b)]
        
        # Find midpoint and peak
        n = len(J)
        midpoint_idx = n // 2
        peak_J_idx = np.argmax(J)
        
        # Analyze curve properties
        results = {
            "lightness": J,
            "chroma": C,
            "hue": H,
            "midpoint_index": midpoint_idx,
            "peak_lightness_index": peak_J_idx,
            "peak_lightness_value": J[peak_J_idx],
            "lightness_range": max(J) - min(J),
            "chroma_range": max(C) - min(C),
            "left_arm_monotonic": all(J[i] <= J[i+1] for i in range(peak_J_idx)),
            "right_arm_monotonic": all(J[i] >= J[i+1] for i in range(peak_J_idx, n-1)),
            "hat_width_ratio": abs(peak_J_idx - midpoint_idx) / (n / 2)  # How far peak is from center
        }
        
        if show_plot:
            PaletteCurveAnalyzer._plot_curves(J, C, H, results)
        
        return results
    
    @staticmethod
    def _plot_curves(J: List[float], C: List[float], H: List[float], results: Dict) -> None:
        """Plot lightness, chroma, and hue curves."""
        fig, axes = plt.subplots(3, 1, figsize=(10, 8))
        x = range(len(J))
        
        # Lightness plot
        axes[0].plot(x, J, 'b-', linewidth=2)
        axes[0].axvline(results["peak_lightness_index"], color='r', linestyle='--', alpha=0.7, label='Peak')
        axes[0].axvline(results["midpoint_index"], color='g', linestyle='--', alpha=0.7, label='Midpoint')
        axes[0].set_title(f"Lightness (J') - Range: {results['lightness_range']:.1f}")
        axes[0].set_ylabel("J'")
        axes[0].grid(True, alpha=0.3)
        axes[0].legend()
        
        # Chroma plot
        axes[1].plot(x, C, 'r-', linewidth=2)
        axes[1].axvline(results["midpoint_index"], color='g', linestyle='--', alpha=0.7, label='Midpoint')
        axes[1].set_title(f"Chroma - Range: {results['chroma_range']:.1f}")
        axes[1].set_ylabel("Chroma")
        axes[1].grid(True, alpha=0.3)
        axes[1].legend()
        
        # Hue plot
        axes[2].plot(x, H, 'purple', linewidth=2)
        axes[2].axvline(results["midpoint_index"], color='g', linestyle='--', alpha=0.7, label='Midpoint')
        axes[2].set_title("Hue Angle")
        axes[2].set_ylabel("Hue (°)")
        axes[2].set_xlabel("Palette Index")
        axes[2].grid(True, alpha=0.3)
        axes[2].legend()
        
        plt.tight_layout()
        plt.show()


# Convenience functions for quick usage
def generate_colorbrewer_style_palette(
    n: int = 199,
    left_hue: float = 255,  # blue
    right_hue: float = 10,  # red
    narrow_hat: bool = True,
    output_format: str = "hex",
    use_classic_diverging: bool = True
) -> List[str]:
    """
    Generate a ColorBrewer-style diverging palette with sensible defaults.
    
    Args:
        n: Number of colors (odd recommended)
        left_hue: Left arm hue (0-360)
        right_hue: Right arm hue (0-360)
        narrow_hat: Whether to use narrow hat like ColorBrewer (vs wider Leonardo-style)
        output_format: Output format ("hex", "rgb", "rgb_strings")
        use_classic_diverging: Use classic diverging method (recommended for ColorBrewer style)
    
    Returns:
        List of colors in specified format
    """
    generator = DivergingPaletteGenerator()
    
    # ColorBrewer-style parameters for narrow hat and smooth curves
    if narrow_hat:
        p2 = p4 = 0.7  # Narrower lightness hat
        cmax1 = cmax2 = 55  # Moderate chroma peaks
    else:
        p2 = p4 = 1.2  # Wider lightness hat (Leonardo-style)
        cmax1 = cmax2 = 65  # Higher chroma peaks
    
    return generator.generate_palette(
        n=n,
        h1=left_hue,
        h3=right_hue,
        p2=p2,
        p4=p4,
        cmax1=cmax1,
        cmax2=cmax2,
        output_format=output_format,
        use_classic_diverging=use_classic_diverging
    )


def test_brand_proximity_quick(
    palette: List[str],
    brand_colors: List[str],
    palette_format: str = "hex"
) -> None:
    """
    Quick brand proximity test with printed report.
    
    Args:
        palette: Palette colors
        brand_colors: Brand colors (hex format)
        palette_format: Format of palette colors
    """
    tester = BrandColorProximityTester()
    results = tester.test_brand_proximity(palette, brand_colors, palette_format)
    tester.print_proximity_report(results)


def analyze_palette_quick(
    palette: List[str],
    palette_format: str = "hex"
) -> Dict:
    """
    Quick palette curve analysis with plots.
    
    Args:
        palette: Palette colors
        palette_format: Format of palette colors
        
    Returns:
        Analysis results dictionary
    """
    return PaletteCurveAnalyzer.analyze_palette_curves(palette, palette_format, show_plot=True)
