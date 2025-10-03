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

# Sidebar for parameters
st.sidebar.header("🎛️ Palette Parameters")

# Basic parameters
st.sidebar.subheader("Basic Settings")
n_colors = st.sidebar.number_input("Number of colors", min_value=5, max_value=299, value=199, step=2, help="Odd numbers recommended for clear midpoint")

# Hue parameters
st.sidebar.subheader("🌈 Hue Settings")
h1 = st.sidebar.slider("Left hue (°)", 0, 360, 255, help="Hue for left arm (blue = 255)")
h3 = st.sidebar.slider("Right hue (°)", 0, 360, 10, help="Hue for right arm (red = 10)")
h2 = st.sidebar.slider("Middle hue (°)", 0, 360, int((h1 + h3) / 2), help="Hue for center (auto-calculated if neutral)")

use_neutral_center = st.sidebar.checkbox("Use neutral center", value=True, help="Check to use gray center, uncheck for colored center")

# Lightness parameters
st.sidebar.subheader("💡 Lightness Settings")
l1 = st.sidebar.slider("Left lightness", 0, 100, 20, help="Lightness at left end")
l2 = st.sidebar.slider("Middle lightness", 0, 100, 97, help="Peak lightness at center")
l3 = st.sidebar.slider("Right lightness", 0, 100, 20, help="Lightness at right end")

# Chroma parameters
st.sidebar.subheader("🌈 Chroma Settings")
c1 = st.sidebar.slider("Left chroma", 0, 100, 50, help="Chroma at left end")
c3 = st.sidebar.slider("Right chroma", 0, 100, 50, help="Chroma at right end")
cmax1 = st.sidebar.slider("Left chroma peak", 0, 100, 60, help="Maximum chroma for left arm")
cmax2 = st.sidebar.slider("Right chroma peak", 0, 100, 60, help="Maximum chroma for right arm")

# Power transformation parameters
st.sidebar.subheader("⚡ Power Transformations")
st.sidebar.markdown("*Controls curve shapes: < 1.0 = faster change, > 1.0 = slower change*")

col1, col2 = st.sidebar.columns(2)
with col1:
    st.markdown("**Left Arm**")
    p1 = st.slider("Left chroma power", 0.1, 3.0, 1.0, 0.1, help="Controls chroma buildup speed")
    p2 = st.slider("Left lightness power", 0.1, 3.0, 0.8, 0.1, help="Controls hat width (< 1 = narrow)")

with col2:
    st.markdown("**Right Arm**")
    p3 = st.slider("Right chroma power", 0.1, 3.0, 1.0, 0.1, help="Controls chroma buildup speed")
    p4 = st.slider("Right lightness power", 0.1, 3.0, 0.8, 0.1, help="Controls hat width (< 1 = narrow)")

# Brand colors
st.sidebar.subheader("🏷️ Brand Colors")
brand_color_left = st.sidebar.color_picker("Left brand color", "#1E3A8A", help="Brand color for left arm")
brand_color_right = st.sidebar.color_picker("Right brand color", "#DC2626", help="Brand color for right arm")

# Generate palette button
if st.sidebar.button("🎨 Generate Palette", type="primary"):
    with st.spinner("Generating palette..."):
        try:
            generator = DivergingPaletteGenerator()
            
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
                output_format="hex"
            )
            
            st.session_state.generated_palette = palette
            st.sidebar.success(f"✅ Generated {len(palette)} colors!")
            
        except Exception as e:
            st.sidebar.error(f"❌ Error generating palette: {str(e)}")

# Display results if palette is generated
if st.session_state.generated_palette is not None:
    palette = st.session_state.generated_palette
    
    # Main content area with tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎨 Palette & Analysis", "📊 Delta E Analysis", "📈 Curve Analysis", "🏷️ Brand Proximity"])
    
    with tab1:
        st.header("Color Palette Visualization")
        
        # Create color bar
        fig_colorbar = create_color_bar_plot(palette, color_type="hex", height=2)
        st.pyplot(fig_colorbar)
        
        # Display basic info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Colors", len(palette))
        with col2:
            st.metric("Midpoint Index", len(palette) // 2)
        with col3:
            st.metric("Format", "Hex")
        
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
            # Hex export
            hex_text = str(palette)
            st.download_button(
                "📝 Download Hex Colors",
                hex_text,
                f"palette_{n_colors}_colors_hex.txt",
                "text/plain"
            )
            
        with col2:
            # RGB strings export
            rgb_palette = []
            for color in palette:
                hex_color = color.lstrip('#')
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                rgb_palette.append(f"rgb({r}, {g}, {b})")
            
            rgb_text = str(rgb_palette)
            st.download_button(
                "🎨 Download RGB Strings",
                rgb_text,
                f"palette_{n_colors}_colors_rgb.txt",
                "text/plain"
            )
    
    with tab2:
        st.header("📊 Delta E Analysis")
        
        # Run delta E analysis
        with st.spinner("Analyzing color differences..."):
            delta_results = get_delta_e(palette, color_type="hex", show_series=False)
        
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
        
        # Detailed delta E table (first 20 and last 20)
        st.subheader("Detailed ΔE Values")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**First 20 Adjacent Pairs**")
            df_first = pd.DataFrame({
                'Index': range(20),
                'Color 1': palette[:20],
                'Color 2': palette[1:21],
                'ΔE': delta_results['deltas'][:20]
            })
            df_first['ΔE'] = df_first['ΔE'].round(3)
            st.dataframe(df_first, use_container_width=True)
            
        with col2:
            st.markdown("**Last 20 Adjacent Pairs**")
            start_idx = len(delta_results['deltas']) - 20
            df_last = pd.DataFrame({
                'Index': range(start_idx, len(delta_results['deltas'])),
                'Color 1': palette[start_idx:start_idx+20],
                'Color 2': palette[start_idx+1:start_idx+21],
                'ΔE': delta_results['deltas'][start_idx:]
            })
            df_last['ΔE'] = df_last['ΔE'].round(3)
            st.dataframe(df_last, use_container_width=True)
    
    with tab3:
        st.header("📈 Lightness, Chroma & Hue Analysis")
        
        # Get curve data
        cam02ucs_colors = convert_list_to_cam02ucs(palette, color_type="hex")
        
        # Create the visualization
        fig = visualize_color_components(cam02ucs_colors, show_chroma_hue=True, return_data=False)
        st.pyplot(fig)
        
        # Curve analysis metrics
        from analysis_functions import visualize_color_components
        curve_data = visualize_color_components(cam02ucs_colors, show_chroma_hue=True, return_data=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            lightness_range = max(curve_data['lightness']) - min(curve_data['lightness'])
            st.metric("Lightness Range", f"{lightness_range:.1f}")
            
        with col2:
            chroma_range = max(curve_data['chroma']) - min(curve_data['chroma'])
            st.metric("Chroma Range", f"{chroma_range:.1f}")
            
        with col3:
            peak_lightness_idx = np.argmax(curve_data['lightness'])
            midpoint_idx = len(curve_data['lightness']) // 2
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
    
    with tab4:
        st.header("🏷️ Brand Color Proximity Analysis")
        
        # Run brand proximity analysis
        brand_colors = [brand_color_left, brand_color_right]
        brand_names = ["Left Brand Color", "Right Brand Color"]
        
        tester = BrandColorProximityTester()
        
        with st.spinner("Analyzing brand color proximity..."):
            proximity_results = tester.test_brand_proximity(
                palette, brand_colors, palette_format="hex", threshold=15.0
            )
        
        # Display results
        st.subheader("Proximity Results")
        
        for i, match in enumerate(proximity_results["closest_matches"]):
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                st.markdown(f"**{brand_names[i]}**")
                st.color_picker(f"Brand {i+1}", brand_colors[i], disabled=True, key=f"brand_display_{i}")
            
            with col2:
                st.metric("Closest Palette Color", match["closest_palette_color"])
                st.metric("Palette Index", match["palette_index"])
                st.metric("ΔE Distance", f"{match['distance']:.3f}")
                
                # Color similarity indicator
                if match['distance'] < 5:
                    st.success("🟢 Very similar colors")
                elif match['distance'] < 10:
                    st.info("🔵 Similar colors")
                elif match['distance'] < 15:
                    st.warning("🟡 Moderately different")
                else:
                    st.error("🔴 Very different colors")
            
            with col3:
                st.markdown("**Closest Match**")
                st.color_picker(f"Match {i+1}", match["closest_palette_color"], disabled=True, key=f"match_display_{i}")
        
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
