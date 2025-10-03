"""
Interactive Diverging Palette Builder UI

A Streamlit app for creating and analyzing diverging color palettes with 
real-time parameter adjustments and comprehensive analysis output.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from diverging_palette_generator import DivergingPaletteGenerator, BrandColorProximityTester
from analysis_functions import get_delta_e, visualize_color_components, create_color_bar_plot, convert_list_to_cam02ucs, compute_adjacient_dE
import re

# Set page config
st.set_page_config(
    page_title="Diverging Palette Builder",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎨 Diverging Palette Builder")
st.markdown("Create ColorBrewer-style diverging palettes with precise control over lightness and chroma curves")

# Initialize session state for persistence
if 'generated_palette' not in st.session_state:
    st.session_state.generated_palette = None

# Initialize parameter values in session state for two-way binding
def init_param(key, default_value):
    if key not in st.session_state:
        st.session_state[key] = default_value

init_param('h1_value', 255)
init_param('h3_value', 10)
init_param('l1_value', 20)
init_param('l2_value', 97)
init_param('l3_value', 20)
init_param('c1_value', 50)
init_param('c3_value', 50)
init_param('cmax1_value', 60)
init_param('cmax2_value', 60)

# Helper functions
def hex_to_rgb(hex_color):
    """Convert hex to RGB tuple (0-255 range)"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_tuple):
    """Convert RGB tuple to hex string"""
    return f"#{rgb_tuple[0]:02x}{rgb_tuple[1]:02x}{rgb_tuple[2]:02x}"

def parse_rgb_input(rgb_input):
    """Parse rgb(r,g,b) string to RGB tuple"""
    match = re.match(r'rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', rgb_input.strip())
    if match:
        return tuple(int(x) for x in match.groups())
    return None

# Sidebar for parameters
st.sidebar.header("🎛️ Palette Parameters")

# Basic parameters
st.sidebar.subheader("Basic Settings")
n_colors = st.sidebar.number_input("Number of colors", min_value=5, max_value=299, value=199, step=2, help="Odd numbers recommended for clear midpoint")

# Hue parameters
st.sidebar.subheader("🌈 Hue Settings")

# Left hue with slider and number input - two-way binding
col1, col2 = st.sidebar.columns([3, 1])
with col1:
    h1_slider = st.slider("Left hue (°)", 0, 360, st.session_state.h1_value, help="Hue for left arm (blue = 255)", key="h1_slider")
with col2:
    h1_input = st.number_input("", min_value=0, max_value=360, value=st.session_state.h1_value, label_visibility="collapsed", key="h1_input")

# Update session state with whichever changed
if h1_slider != st.session_state.h1_value:
    st.session_state.h1_value = h1_slider
elif h1_input != st.session_state.h1_value:
    st.session_state.h1_value = h1_input
h1 = st.session_state.h1_value

# Right hue with slider and number input - two-way binding
col1, col2 = st.sidebar.columns([3, 1])
with col1:
    h3_slider = st.slider("Right hue (°)", 0, 360, st.session_state.h3_value, help="Hue for right arm (red = 10)", key="h3_slider")
with col2:
    h3_input = st.number_input("", min_value=0, max_value=360, value=st.session_state.h3_value, label_visibility="collapsed", key="h3_input")

# Update session state with whichever changed
if h3_slider != st.session_state.h3_value:
    st.session_state.h3_value = h3_slider
elif h3_input != st.session_state.h3_value:
    st.session_state.h3_value = h3_input
h3 = st.session_state.h3_value

# Middle hue with color picker and RGB input
st.sidebar.markdown("**Middle hue/color**")
use_neutral_center = st.sidebar.checkbox("Use neutral center", value=True, help="Check to use gray center, uncheck for colored center")
use_classic_diverging = st.sidebar.checkbox("Classic diverging (HCL Wizard style)", value=True, help="Use classic diverging_hcl for constant hues per arm (like HCL Wizard)")

# Focus on parameter-based approach - waypoints feature disabled for now
use_brand_waypoints = False

if not use_neutral_center:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        middle_color_hex = st.color_picker("Middle color", "#808080", help="Color for center")
        middle_rgb = hex_to_rgb(middle_color_hex)
    
    with col2:
        rgb_input = st.text_input("RGB input", f"rgb({middle_rgb[0]}, {middle_rgb[1]}, {middle_rgb[2]})", 
                                help="Format: rgb(r,g,b)")
        parsed_rgb = parse_rgb_input(rgb_input)
        if parsed_rgb and parsed_rgb != middle_rgb:
            middle_rgb = parsed_rgb
            middle_color_hex = rgb_to_hex(middle_rgb)
    
    # Convert RGB to approximate hue for colorspace
    from colorspacious import cspace_convert
    rgb_norm = tuple(x/255.0 for x in middle_rgb)
    try:
        lab = cspace_convert(rgb_norm, "sRGB1", "CIELab")
        h2 = np.degrees(np.arctan2(lab[2], lab[1])) % 360  # Hue from a*, b*
    except:
        h2 = int((h1 + h3) / 2)  # Fallback
else:
    h2 = int((h1 + h3) / 2)
    middle_rgb = (128, 128, 128)  # Gray

# Lightness parameters with sliders and number inputs
st.sidebar.subheader("💡 Lightness Settings")

col1, col2 = st.sidebar.columns([3, 1])
with col1:
    l1_slider = st.slider("Left lightness", 0, 100, st.session_state.l1_value, help="Lightness at left end", key="l1_slider")
with col2:
    l1_input = st.number_input("", min_value=0, max_value=100, value=st.session_state.l1_value, label_visibility="collapsed", key="l1_input")
if l1_slider != st.session_state.l1_value:
    st.session_state.l1_value = l1_slider
elif l1_input != st.session_state.l1_value:
    st.session_state.l1_value = l1_input
l1 = st.session_state.l1_value

col1, col2 = st.sidebar.columns([3, 1])
with col1:
    l2_slider = st.slider("Middle lightness", 0, 100, st.session_state.l2_value, help="Peak lightness at center", key="l2_slider")
with col2:
    l2_input = st.number_input("", min_value=0, max_value=100, value=st.session_state.l2_value, label_visibility="collapsed", key="l2_input")
if l2_slider != st.session_state.l2_value:
    st.session_state.l2_value = l2_slider
elif l2_input != st.session_state.l2_value:
    st.session_state.l2_value = l2_input
l2 = st.session_state.l2_value

col1, col2 = st.sidebar.columns([3, 1])
with col1:
    l3_slider = st.slider("Right lightness", 0, 100, st.session_state.l3_value, help="Lightness at right end", key="l3_slider")
with col2:
    l3_input = st.number_input("", min_value=0, max_value=100, value=st.session_state.l3_value, label_visibility="collapsed", key="l3_input")
if l3_slider != st.session_state.l3_value:
    st.session_state.l3_value = l3_slider
elif l3_input != st.session_state.l3_value:
    st.session_state.l3_value = l3_input
l3 = st.session_state.l3_value

# Chroma parameters with sliders and number inputs
st.sidebar.subheader("🌈 Chroma Settings")

col1, col2 = st.sidebar.columns([3, 1])
with col1:
    c1_slider = st.slider("Left chroma", 0, 100, st.session_state.c1_value, help="Chroma at left end", key="c1_slider")
with col2:
    c1_input = st.number_input("", min_value=0, max_value=100, value=st.session_state.c1_value, label_visibility="collapsed", key="c1_input")
if c1_slider != st.session_state.c1_value:
    st.session_state.c1_value = c1_slider
elif c1_input != st.session_state.c1_value:
    st.session_state.c1_value = c1_input
c1 = st.session_state.c1_value

col1, col2 = st.sidebar.columns([3, 1])
with col1:
    c3_slider = st.slider("Right chroma", 0, 100, st.session_state.c3_value, help="Chroma at right end", key="c3_slider")
with col2:
    c3_input = st.number_input("", min_value=0, max_value=100, value=st.session_state.c3_value, label_visibility="collapsed", key="c3_input")
if c3_slider != st.session_state.c3_value:
    st.session_state.c3_value = c3_slider
elif c3_input != st.session_state.c3_value:
    st.session_state.c3_value = c3_input
c3 = st.session_state.c3_value

col1, col2 = st.sidebar.columns([3, 1])
with col1:
    cmax1_slider = st.slider("Left chroma peak", 0, 100, st.session_state.cmax1_value, help="Maximum chroma for left arm", key="cmax1_slider")
with col2:
    cmax1_input = st.number_input("", min_value=0, max_value=100, value=st.session_state.cmax1_value, label_visibility="collapsed", key="cmax1_input")
if cmax1_slider != st.session_state.cmax1_value:
    st.session_state.cmax1_value = cmax1_slider
elif cmax1_input != st.session_state.cmax1_value:
    st.session_state.cmax1_value = cmax1_input
cmax1 = st.session_state.cmax1_value

col1, col2 = st.sidebar.columns([3, 1])
with col1:
    cmax2_slider = st.slider("Right chroma peak", 0, 100, st.session_state.cmax2_value, help="Maximum chroma for right arm", key="cmax2_slider")
with col2:
    cmax2_input = st.number_input("", min_value=0, max_value=100, value=st.session_state.cmax2_value, label_visibility="collapsed", key="cmax2_input")
if cmax2_slider != st.session_state.cmax2_value:
    st.session_state.cmax2_value = cmax2_slider
elif cmax2_input != st.session_state.cmax2_value:
    st.session_state.cmax2_value = cmax2_input
cmax2 = st.session_state.cmax2_value

# Power transformation parameters
st.sidebar.subheader("⚡ Power Transformations")
st.sidebar.markdown("*Controls curve shapes: < 1.0 = faster change, > 1.0 = slower change*")

col1, col2 = st.sidebar.columns(2)
with col1:
    st.markdown("**Left Arm**")
    p1 = st.slider("Left chroma power", 0.1, 3.0, 1.3, 0.1, help="Controls chroma buildup speed")
    p2 = st.slider("Left lightness power", 0.1, 3.0, 1.3, 0.1, help="Controls hat width (< 1 = narrow)")

with col2:
    st.markdown("**Right Arm**")
    p3 = st.slider("Right chroma power", 0.1, 3.0, 1.3, 0.1, help="Controls chroma buildup speed")
    p4 = st.slider("Right lightness power", 0.1, 3.0, 1.3, 0.1, help="Controls hat width (< 1 = narrow)")

# Brand colors - store as RGB values
st.sidebar.subheader("🏷️ Brand Colors")
brand_color_left_hex = st.sidebar.color_picker("Left brand color", "#1E3A8A", help="Brand color for left arm")
brand_color_right_hex = st.sidebar.color_picker("Right brand color", "#DC2626", help="Brand color for right arm")

# Convert to RGB for consistency
brand_color_left_rgb = hex_to_rgb(brand_color_left_hex)
brand_color_right_rgb = hex_to_rgb(brand_color_right_hex)

# Brand color analyzer
if st.sidebar.button("🔍 Analyze Brand Colors", help="Extract optimal parameters from your brand colors"):
    generator = DivergingPaletteGenerator()
    
    h1, c1, l1 = generator.hex_to_hcl(brand_color_left_hex)
    h3, c3, l3 = generator.hex_to_hcl(brand_color_right_hex)
    
    st.sidebar.markdown("**📊 Brand Color Analysis:**")
    st.sidebar.markdown(f"Left: H={h1:.0f}°, C={c1:.0f}, L={l1:.0f}")
    st.sidebar.markdown(f"Right: H={h3:.0f}°, C={c3:.0f}, L={l3:.0f}")
    
    st.sidebar.markdown("**🎯 Suggested Settings:**")
    st.sidebar.markdown(f"• Left hue: **{h1:.0f}**")
    st.sidebar.markdown(f"• Right hue: **{h3:.0f}**")
    st.sidebar.markdown(f"• Left lightness: **{l1:.0f}**")
    st.sidebar.markdown(f"• Right lightness: **{l3:.0f}**")
    st.sidebar.markdown(f"• Chroma peak: **{max(c1, c3, 50):.0f}**")
    st.sidebar.markdown("• Use Classic diverging ✅")
    
    suggested_power = 0.8 if abs(95 - (l1 + l3)/2) > 50 else 1.2
    st.sidebar.markdown(f"• Power: **{suggested_power}**")

# Generate palette button
if st.sidebar.button("🎨 Generate Palette", type="primary"):
    with st.spinner("Generating palette..."):
        try:
            generator = DivergingPaletteGenerator()
            
            # Use parameter-based mode (waypoints disabled)
            # Adjust parameters based on neutral center setting
            h2_param = None if use_neutral_center else h2
            c2_param = None if use_neutral_center else 20  # Small chroma for colored center
            
            palette = generator.generate_palette(
                n=n_colors,
                h1=h1, h2=h2_param, h3=h3,
                c1=c1, c2=c2_param, c3=c3,
                l1=l1, l2=l2, l3=l3,
                p1=p1, p2=p2, p3=p3, p4=p4,
                cmax1=cmax1, cmax2=cmax2,
                output_format="rgb_strings",  # Work with RGB as requested
                use_classic_diverging=use_classic_diverging
            )
            
            st.session_state.generated_palette = palette
            st.sidebar.success(f"✅ Generated {len(palette)} colors!")
            
            # Check if chroma was limited by sRGB gamut
            if use_classic_diverging:
                requested_chroma = max(cmax1, cmax2)
                if requested_chroma > 60:  # Likely to hit gamut limits
                    st.sidebar.warning("⚠️ High chroma values may be limited by sRGB gamut. Try increasing lightness values for higher chroma.")
            
        except Exception as e:
            st.sidebar.error(f"❌ Error generating palette: {str(e)}")

# Display results if palette is generated
if st.session_state.generated_palette is not None:
    palette = st.session_state.generated_palette
    
    # Main content area with tabs - Curve Analysis moved to 2nd position
    tab1, tab2, tab3, tab4 = st.tabs(["🎨 Palette & Analysis", "📈 Curve Analysis", "📊 Delta E Analysis", "🏷️ Brand Proximity"])
    
    with tab1:
        st.header("Color Palette Visualization")
        
        # Create color bar
        fig_colorbar = create_color_bar_plot(palette, color_type="rgb", height=2)
        st.pyplot(fig_colorbar)
        
        # Display basic info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Colors", len(palette))
        with col2:
            st.metric("Midpoint Index", len(palette) // 2)
        with col3:
            st.metric("Format", "RGB")
        
        # Show first, middle, and last colors
        st.subheader("Sample Colors")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**First 5 colors:**")
            for i, color in enumerate(palette[:5]):
                st.markdown(f"`{i:3d}: {color}`")
                
        with col2:
            st.markdown("**Middle 5 colors:**")
            mid_idx = len(palette) // 2
            for i, color in enumerate(palette[mid_idx-2:mid_idx+3], mid_idx-2):
                st.markdown(f"`{i:3d}: {color}`")
                
        with col3:
            st.markdown("**Last 5 colors:**")
            for i, color in enumerate(palette[-5:], len(palette)-5):
                st.markdown(f"`{i:3d}: {color}`")
        
        # Export options
        st.subheader("Export Options")
        col1, col2 = st.columns(2)
        
        with col1:
            # RGB strings export (already in this format)
            rgb_text = str(palette)
            st.download_button(
                "🎨 Download RGB Strings",
                rgb_text,
                f"palette_{n_colors}_colors_rgb.txt",
                "text/plain"
            )
            
        with col2:
            # Convert to hex for export
            hex_palette = []
            for color in palette:
                match = re.match(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', color)
                if match:
                    r, g, b = map(int, match.groups())
                    hex_palette.append(f"#{r:02x}{g:02x}{b:02x}")
            
            hex_text = str(hex_palette)
            st.download_button(
                "📝 Download Hex Colors",
                hex_text,
                f"palette_{n_colors}_colors_hex.txt",
                "text/plain"
            )
    
    with tab2:
        st.header("📈 Lightness, Chroma & Hue Analysis")
        
        # Get curve data
        cam02ucs_colors = convert_list_to_cam02ucs(palette, color_type="rgb")
        
        # Create the visualization with smaller charts in one row
        from analysis_functions import visualize_color_components
        curve_data = visualize_color_components(cam02ucs_colors, show_chroma_hue=True, return_data=True, use_lab_chroma=True)
        
        # Create compact 3-chart layout
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        x = range(len(curve_data['lightness']))
        
        # Lightness plot
        axes[0].plot(x, curve_data['lightness'], 'b-', linewidth=2)
        peak_lightness_idx = np.argmax(curve_data['lightness'])
        midpoint_idx = len(curve_data['lightness']) // 2
        axes[0].axvline(peak_lightness_idx, color='r', linestyle='--', alpha=0.7, label='Peak')
        axes[0].axvline(midpoint_idx, color='g', linestyle='--', alpha=0.7, label='Midpoint')
        axes[0].set_title("Lightness (J')")
        axes[0].set_ylabel("J'")
        axes[0].grid(True, alpha=0.3)
        axes[0].legend()
        
        # Chroma plot
        axes[1].plot(x, curve_data['chroma'], 'r-', linewidth=2)
        axes[1].axvline(midpoint_idx, color='g', linestyle='--', alpha=0.7, label='Midpoint')
        axes[1].set_title("Chroma")
        axes[1].set_ylabel("Chroma")
        axes[1].grid(True, alpha=0.3)
        axes[1].legend()
        
        # Hue plot
        axes[2].plot(x, curve_data['hue'], 'purple', linewidth=2)
        axes[2].axvline(midpoint_idx, color='g', linestyle='--', alpha=0.7, label='Midpoint')
        axes[2].set_title("Hue Angle")
        axes[2].set_ylabel("Hue (°)")
        axes[2].set_xlabel("Palette Index")
        axes[2].grid(True, alpha=0.3)
        axes[2].legend()
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Curve analysis metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            lightness_range = max(curve_data['lightness']) - min(curve_data['lightness'])
            st.metric("Lightness Range", f"{lightness_range:.1f}")
            
        with col2:
            chroma_range = max(curve_data['chroma']) - min(curve_data['chroma'])
            st.metric("Chroma Range", f"{chroma_range:.1f}")
            
        with col3:
            hat_width_ratio = abs(peak_lightness_idx - midpoint_idx) / (len(curve_data['lightness']) / 2)
            st.metric("Hat Width Ratio", f"{hat_width_ratio:.3f}")
            
        with col4:
            max_lightness = max(curve_data['lightness'])
            st.metric("Peak Lightness", f"{max_lightness:.1f}")
        
        # Monotonicity check
        st.subheader("Monotonicity Analysis")
        
        peak_idx = np.argmax(curve_data['lightness'])
        left_monotonic = all(curve_data['lightness'][i] <= curve_data['lightness'][i+1] for i in range(peak_idx))
        right_monotonic = all(curve_data['lightness'][i] >= curve_data['lightness'][i+1] for i in range(peak_idx, len(curve_data['lightness'])-1))
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Left Arm Monotonic", "✅ Yes" if left_monotonic else "❌ No")
        with col2:
            st.metric("Right Arm Monotonic", "✅ Yes" if right_monotonic else "❌ No")
    
    with tab3:
        st.header("📊 Delta E Analysis")
        
        # Run delta E analysis
        with st.spinner("Analyzing color differences..."):
            delta_results = get_delta_e(palette, color_type="rgb", show_series=False)
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Mean ΔE", f"{delta_results['mean_dE']:.3f}")
        with col2:
            st.metric("Std Dev ΔE", f"{delta_results['std_dE']:.3f}")
        with col3:
            st.metric("Coefficient of Variation", f"{delta_results['cv']:.3f}")
        with col4:
            st.metric("Total Adjacent Pairs", len(delta_results['deltas']))
        
        # Delta E distribution plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Bar plot of deltas
        x = range(len(delta_results['deltas']))
        ax1.bar(x, delta_results['deltas'], alpha=0.7)
        ax1.axhline(delta_results['mean_dE'], color='r', linestyle='--', label=f'Mean = {delta_results["mean_dE"]:.3f}')
        ax1.set_title('Adjacent ΔE Values')
        ax1.set_xlabel('Color Pair Index')
        ax1.set_ylabel('ΔE Value')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Histogram of deltas
        ax2.hist(delta_results['deltas'], bins=20, alpha=0.7, edgecolor='black')
        ax2.axvline(delta_results['mean_dE'], color='r', linestyle='--', label=f'Mean = {delta_results["mean_dE"]:.3f}')
        ax2.set_title('ΔE Distribution')
        ax2.set_xlabel('ΔE Value')
        ax2.set_ylabel('Frequency')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Detailed delta E table - show ALL values as requested
        st.subheader("All ΔE Values")
        
        # Create full dataframe with all adjacent pairs
        df_all = pd.DataFrame({
            'Index': range(len(delta_results['deltas'])),
            'Color 1': palette[:-1],  # All colors except last
            'Color 2': palette[1:],   # All colors except first
            'ΔE': [round(d, 3) for d in delta_results['deltas']]
        })
        
        # Display with pagination-like scrolling
        st.dataframe(df_all, use_container_width=True, height=400)
    
    with tab4:
        st.header("🏷️ Brand Color Proximity Analysis")
        
        # Run brand proximity analysis using hex colors for consistency
        # Use the traditional brand color inputs (waypoints disabled)
        brand_colors = [brand_color_left_hex, brand_color_right_hex]
        brand_names = ["Left Brand Color", "Right Brand Color"]
        
        tester = BrandColorProximityTester()
        
        with st.spinner("Analyzing brand color proximity..."):
            proximity_results = tester.test_brand_proximity(
                palette, brand_colors, palette_format="rgb_strings", threshold=15.0
            )
        
        # Display results in compact layout
        st.subheader("Proximity Results")
        
        for i, match in enumerate(proximity_results["closest_matches"]):
            # Get RGB values for display
            brand_rgb = hex_to_rgb(brand_colors[i])
            brand_rgb_str = f"rgb({brand_rgb[0]}, {brand_rgb[1]}, {brand_rgb[2]})"
            
            # Convert match RGB string to hex for display
            match_rgb = re.match(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', match["closest_palette_color"])
            if match_rgb:
                r, g, b = map(int, match_rgb.groups())
                match_hex = f"#{r:02x}{g:02x}{b:02x}"
                match_rgb_str = match["closest_palette_color"]
            
            # Create row layout: Brand Color | Closest Match | ΔE Distance | Palette Index | Similarity
            col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 3])
            
            with col1:
                st.markdown(f"**{brand_names[i]}**")
                # Brand color swatch
                st.markdown(f'<div style="width: 80px; height: 60px; background-color: {brand_colors[i]}; border: 1px solid #ccc; border-radius: 4px; margin-bottom: 4px;"></div>', 
                           unsafe_allow_html=True)
                st.caption(brand_rgb_str)  # Show RGB value, not hex
            
            with col2:
                st.markdown("**Closest Match**")
                # Closest match swatch right next to brand color
                st.markdown(f'<div style="width: 80px; height: 60px; background-color: {match_hex}; border: 1px solid #ccc; border-radius: 4px; margin-bottom: 4px;"></div>', 
                           unsafe_allow_html=True)
                st.caption(match_rgb_str)  # Show RGB value
            
            with col3:
                st.markdown("**ΔE Distance**")
                st.markdown(f"<div style='font-size: 24px; font-weight: bold; text-align: center; padding: 20px;'>{match['distance']:.3f}</div>", 
                           unsafe_allow_html=True)
            
            with col4:
                st.markdown("**Palette Index**")
                st.markdown(f"<div style='font-size: 24px; font-weight: bold; text-align: center; padding: 20px;'>{match['palette_index']}</div>", 
                           unsafe_allow_html=True)
            
            with col5:
                st.markdown("**Similarity**")
                # Color similarity indicator
                if match['distance'] < 5:
                    st.success("🟢 Very similar")
                elif match['distance'] < 10:
                    st.info("🔵 Similar")
                elif match['distance'] < 15:
                    st.warning("🟡 Moderate")
                else:
                    st.error("🔴 Different")
            
            st.markdown("---")  # Separator between brand colors
        
        # Warnings
        if proximity_results["proximity_warnings"]:
            st.subheader("⚠️ Proximity Warnings")
            for warning in proximity_results["proximity_warnings"]:
                st.warning(warning["message"])
        else:
            st.success("✅ No proximity conflicts detected (ΔE > 15)")
        
        # Detailed proximity table
        st.subheader("All Proximity Values")
        df_proximity = pd.DataFrame({
            'Brand Color': brand_colors,
            'Brand Name': brand_names,
            'Closest Palette Color': [match["closest_palette_color"] for match in proximity_results["closest_matches"]],
            'Palette Index': [match["palette_index"] for match in proximity_results["closest_matches"]],
            'ΔE Distance': [round(match["distance"], 3) for match in proximity_results["closest_matches"]]
        })
        st.dataframe(df_proximity, use_container_width=True)

else:
    st.info("👈 Adjust parameters in the sidebar and click 'Generate Palette' to get started!")
    
    # Show some example presets
    st.subheader("💡 Quick Start Presets")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **ColorBrewer Blue-Red**
        - Left Hue: 255° (Blue)
        - Right Hue: 10° (Red)
        - Power: 0.8 (Narrow hat)
        """)
        
    with col2:
        st.markdown("""
        **Leonardo Style**
        - Left Hue: 255° (Blue)  
        - Right Hue: 10° (Red)
        - Power: 1.2 (Wide hat)
        """)
        
    with col3:
        st.markdown("""
        **Green-Purple**
        - Left Hue: 120° (Green)
        - Right Hue: 270° (Purple)  
        - Power: 0.7 (Very narrow)
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    Built with Streamlit • Powered by colorspace & colorspacious
</div>
""", unsafe_allow_html=True)
