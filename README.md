# Diverging Color Palette Generator

**Creates ColorBrewer-style diverging palettes** with precise control over lightness and chroma curves using power transformations. Think "HCL Wizard but with brand color awareness."

## 🚀 Quick Start

```bash
# Setup (one time)
source venv/bin/activate
pip install -r requirements.txt

# Launch interactive UI
streamlit run ui/palette_builder.py

# Test installation
python tests/test_ui.py
```

## 🎯 What This Tool Does

**Key capabilities:**

- Generate 199-step continuous diverging palettes
- Power transformation controls for curve shapes (narrow vs wide "hats")
- CIELAB chroma analysis (matches HCL Wizard measurements)
- Brand color proximity testing in CAM02-UCS space
- Export formats: hex, RGB tuples, RGB strings

## 📁 Project Structure

```
colour-diverging-tool/
├── src/                          # Core source code
│   ├── diverging_palette_generator.py  # Main generator classes
│   └── analysis_functions.py           # Color analysis (from existing Colab)
├── ui/                           # Interactive interface
│   └── palette_builder.py              # Streamlit web app
├── examples/                     # Usage examples & tools
│   ├── example_usage.py                # Comprehensive examples
│   └── brand_analyzer.py              # Brand color parameter extraction
├── tests/                        # Test files
│   ├── test_ui.py                      # UI functionality tests
│   └── test_brand_waypoints.py         # Brand integration experiments
├── docs/                         # Documentation & research
│   ├── existing-functions.md           # Original analysis functions
│   └── notes.md                        # Research notes
├── requirements.txt              # Python dependencies
├── AGENTS.md                     # Quick reference for future work
└── README.md                     # This file
```

## 🎛️ Interactive UI Features

**Parameter Controls:**

- Hue settings (left, right, optional middle)
- Lightness settings (ends and peak with number inputs)
- Chroma settings (ends and peaks)
- Power transformations (curve shape controls)
- Brand colors (for proximity testing)

**Analysis Outputs:**

1. **Palette Visualization**: 199-color continuous scale
2. **Curve Analysis**: Lightness/chroma/hue plots (3 charts in row)
3. **Delta E Analysis**: All adjacent ΔE values in scrollable table
4. **Brand Proximity**: CAM02-UCS distance to brand colors

## 💡 Usage in Code

```python
from src.diverging_palette_generator import generate_colorbrewer_style_palette

# Generate palette
palette = generate_colorbrewer_style_palette(
    n=199, left_hue=255, right_hue=10,
    output_format="rgb_strings"  # Compatible with existing analysis
)

# Use with existing analysis functions
from src.analysis_functions import get_delta_e
delta_results = get_delta_e(palette, color_type="rgb")
```

## 🔬 Key Features

### Power Transformation Controls

- `p2, p4` (lightness): Controls "hat" width (< 1.0 = narrow, > 1.0 = wide)
- `p1, p3` (chroma): Controls chroma buildup speed

### Palette Modes

- **Classic diverging**: Constant hues per arm (blue stays blue, red stays red)
- **Flexible diverging**: Allows hue interpolation (can create unwanted purples)

### Brand Color Integration

- Proximity testing in CAM02-UCS space
- Parameter suggestions based on brand color analysis
- Distance calculations to optimize brand consistency

## 📝 Notes

- Uses Python `colorspace` package (port of R's colorspace)
- CIELAB chroma analysis matches HCL Wizard measurements
- sRGB gamut limitations affect achievable chroma at low lightness
- Classic diverging mode recommended for clean blue-red palettes

## Known issues

- The two-way binding of the sliders and the input fields is not really working. Using the input fields will work (but using sliders after won't in most cases)
