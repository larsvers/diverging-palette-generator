# Diverging Color Palette Generator

## Quick Start

```bash
# Setup (one time)
source venv/bin/activate
pip install -r requirements.txt

# Launch interactive UI
streamlit run ui/palette_builder.py

# Test installation
python test_ui.py
```

## What This Tool Does

**Creates ColorBrewer-style diverging palettes** with precise control over lightness and chroma curves using power transformations. Think "HCL Wizard but with brand color awareness."

**Key capabilities:**
- Generate 199-step continuous diverging palettes  
- Power transformation controls for curve shapes (narrow vs wide "hats")
- CIELAB chroma analysis (matches HCL Wizard measurements)
- Brand color proximity testing in CAM02-UCS space
- Export formats: hex, RGB tuples, RGB strings

## Core Workflow

1. **Launch UI**: `streamlit run ui/palette_builder.py`
2. **Set parameters**: Use sliders or number inputs for precise control
3. **Choose mode**: Classic diverging (HCL Wizard style) or flexible
4. **Generate palette**: 199-color continuous scale
5. **Analyze results**: View lightness/chroma curves and brand proximity
6. **Export**: Download as hex or RGB strings for Colab/analysis

## UI Layout

**Sidebar Controls:**
- Basic settings (number of colors)
- Hue settings (left, right, optional middle)  
- Lightness settings (ends and peak with power controls)
- Chroma settings (ends and peaks)
- Power transformations (curve shape controls)
- Brand colors (for proximity testing)

**Main Tabs:**
1. **Palette & Analysis**: Color bar + export options
2. **Curve Analysis**: Lightness/chroma/hue plots (3 charts in row)
3. **Delta E Analysis**: All adjacent ΔE values in scrollable table
4. **Brand Proximity**: Distance to brand colors with visual swatches

## Key Parameters

**Power Transformations** (most important):
- `p2, p4` (lightness): `< 1.0` = narrow hat (ColorBrewer), `> 1.0` = wide hat (Leonardo)
- `p1, p3` (chroma): Controls chroma buildup speed

**Modes:**
- **Classic diverging**: Constant hues per arm (blue stays blue, red stays red)
- **Flexible diverging**: Allows hue interpolation (can create unwanted purples)

## File Structure

```
src/                 # Core code
├── diverging_palette_generator.py  # Main generator classes
└── analysis_functions.py          # Color analysis (from existing Colab functions)

ui/                  # Interactive interface  
└── palette_builder.py            # Streamlit web app

examples/            # Usage examples
tests/              # Test files
docs/               # Research notes and original functions
```

## Integration with Existing Analysis

The tool generates RGB strings compatible with your existing Colab analysis functions:

```python
# Generate palette
palette = generator.generate_palette(n=199, output_format="rgb_strings")

# Use with existing analysis
from analysis_functions import get_delta_e, visualize_color_components
delta_results = get_delta_e(palette, color_type="rgb")
```

## Brand Color Workflow

**Current approach** (proximity testing):
1. Generate palette with appropriate hue parameters
2. Test proximity to brand colors in Brand Proximity tab
3. Iterate parameters to minimize ΔE distance to brand colors

**Future approach** (not implemented):
- Direct brand color waypoints (Leonardo-style)
- Requires solving HCL interpolation path issues

## Notes

- Uses Python `colorspace` package (port of R's colorspace)
- CIELAB chroma analysis matches HCL Wizard measurements
- sRGB gamut limitations affect achievable chroma at low lightness
- Classic diverging mode recommended for clean blue-red palettes
