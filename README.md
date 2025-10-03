# Diverging Color Palette Generator

A Python tool for creating ColorBrewer-style diverging palettes with precise control over lightness and chroma curves using power transformations. Includes an interactive Streamlit UI for real-time palette design and analysis.

## 📁 Project Structure

```
colour-diverging-tool/
├── src/                          # Core source code
│   ├── __init__.py
│   ├── diverging_palette_generator.py  # Main palette generation classes
│   └── analysis_functions.py           # Color analysis functions
├── ui/                           # User interface
│   └── palette_builder.py       # Streamlit web app
├── examples/                     # Example usage scripts  
│   └── example_usage.py         # Comprehensive examples
├── tests/                        # Test files
│   └── test_basic.py            # Basic functionality tests
├── docs/                         # Documentation
│   ├── existing-functions.md    # Original analysis functions
│   └── notes.md                 # Research notes
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── venv/                        # Virtual environment (created locally)
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Activate virtual environment
source venv/bin/activate

# Verify installation
python tests/test_basic.py
```

### 2. Launch Interactive UI

```bash
# Start the Streamlit app
streamlit run ui/palette_builder.py
```

This opens a web interface where you can:
- 🎛️ Adjust all parameters with sliders and inputs
- 🏷️ Input brand colors for proximity testing
- 🎨 See real-time palette generation
- 📊 View comprehensive analysis including Delta E, lightness curves, and brand proximity

### 3. Use in Code

```python
from src.diverging_palette_generator import generate_colorbrewer_style_palette

# Generate a 199-color palette
palette = generate_colorbrewer_style_palette(
    n=199,
    left_hue=255,  # blue
    right_hue=10,  # red
    narrow_hat=True,
    output_format="hex"  # or "rgb_strings" for your existing analysis functions
)
```

## 🎛️ Interactive UI Features

The Streamlit app provides a comprehensive interface with:

### Parameter Controls
- **Hue Settings**: Left, right, and middle hue controls
- **Lightness Settings**: End and peak lightness values  
- **Chroma Settings**: End chroma and peak chroma controls
- **Power Transformations**: Precise control over curve shapes
- **Brand Colors**: Input colors for proximity testing

### Analysis Outputs
1. **Palette Visualization**: 199-color continuous scale
2. **Delta E Analysis**: Adjacent color differences with statistics
3. **Curve Analysis**: Lightness, chroma, hue plots with monotonicity checks
4. **Brand Proximity**: Distance calculations to your brand colors

## 🔬 Core Features

### Power Transformation Controls
- `p2, p4` (lightness): Controls the "hat" width
  - `< 1.0`: Narrower hat (ColorBrewer-style)
  - `> 1.0`: Wider hat (Leonardo-style)
- `p1, p3` (chroma): Controls chroma buildup speed

### Brand Color Integration
- Test proximity of palette colors to brand colors
- CAM02-UCS perceptual distance calculations
- Automatic conflict detection and warnings

### Multiple Export Formats
- **Hex**: `#1E3A8A` format
- **RGB Strings**: `rgb(30, 58, 138)` format (compatible with existing analysis)
- **RGB Tuples**: `(0.118, 0.227, 0.541)` format

## 📊 Analysis Integration

The tool integrates with your existing analysis functions from `docs/existing-functions.md`:

```python
from src.analysis_functions import get_delta_e, visualize_color_components

# Generate palette
palette = generate_colorbrewer_style_palette(n=199, output_format="rgb_strings")

# Use your existing analysis
delta_results = get_delta_e(palette, color_type="rgb")
```

## 🎯 Use Cases

1. **Brand-Consistent Palettes**: Generate palettes that work with your brand colors
2. **ColorBrewer Replication**: Create palettes matching ColorBrewer's aesthetic
3. **Parameter Exploration**: Understand how power transformations affect palette appearance
4. **Colab Integration**: Export palettes for use in Jupyter/Colab notebooks

## 🔧 Technical Details

Built on:
- **colorspace**: Python port of R's colorspace package for HCL palette generation
- **colorspacious**: CAM02-UCS color space conversions
- **streamlit**: Interactive web interface
- **matplotlib**: Visualization and analysis

The tool provides the exact functionality described in your research notes:
- Power transformation controls like HCL Wizard
- 199-step continuous palette output
- Brand color proximity testing
- ColorBrewer-style narrow hats vs Leonardo-style wide hats

## 📝 Next Steps

1. **Launch the UI**: `streamlit run ui/palette_builder.py`
2. **Experiment with parameters**: Try different power values to see the effect
3. **Test brand colors**: Input your actual brand colors for proximity testing
4. **Export palettes**: Download results for use in your analysis pipeline

The interactive UI makes it easy to understand the relationship between parameters and resulting palette aesthetics!
