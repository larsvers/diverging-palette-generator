"""
Color analysis functions extracted from existing-functions.md
These work with the existing analysis pipeline
"""

import re
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from colorspacious import cspace_convert


# Helper functions
def hex_to_rgb(hex_color):
    """
    Converts a hex string (e.g. '#4287f5') to an RGB tuple in [0..1].
    """
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r / 255.0, g / 255.0, b / 255.0)

def hex_to_cam02ucs(hex_color):
    """
    Converts a hex string to CAM02-UCS coordinates (J', a', b').
    """
    rgb = hex_to_rgb(hex_color)
    # Convert from sRGB (normalized to [0..1]) to CAM02-UCS
    # 'sRGB1' means sRGB with components in [0..1].
    cam02ucs = cspace_convert(rgb, "sRGB1", "CAM02-UCS")
    return cam02ucs

# Converting hex list to CAM02-UCS
def convert_list_to_cam02ucs(color_list, color_type="hex"):
  """
  Converts a list of hex or rgb colors to a list of CAM02-UCS coordinates.
  """
  cam02ucs_list = []
  if color_type == "hex":
      cam02ucs_list = [hex_to_cam02ucs(hx) for hx in color_list]
  elif color_type == "rgb":
    for rgb_str in color_list:
      # Extract RGB values using regular expression
      match = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", rgb_str)
      if match:
          r, g, b = map(int, match.groups())
          # Normalize RGB values to [0..1]
          rgb = (r / 255.0, g / 255.0, b / 255.0)
          # Convert from sRGB to CAM02-UCS
          cam02ucs = cspace_convert(rgb, "sRGB1", "CAM02-UCS")
          cam02ucs_list.append(cam02ucs)
      else:
          print(f"Warning: Invalid RGB string: {rgb_str}")  # Handle invalid strings

  return cam02ucs_list

def compute_adjacient_dE(cam02ucs_list):
    """
    Given a list of (J', a', b') coordinates in CAM02-UCS,
    compute the adjacent ΔE distances.
    """
    diffs = []
    for i in range(len(cam02ucs_list) - 1):
        c1 = np.array(cam02ucs_list[i])
        c2 = np.array(cam02ucs_list[i+1])
        dE = np.linalg.norm(c2 - c1)  # Euclidean distance in J'a'b'
        diffs.append(dE)
    return diffs

# Get the deltas
def get_delta_e(color_values, color_type="hex", show_series=False):
    """
    Calculates and prints ΔE values for a list of hex or RGB colors.
    Returns dictionary with analysis results.
    """
    cam02ucs_colors = convert_list_to_cam02ucs(color_values, color_type=color_type)

    deltas = compute_adjacient_dE(cam02ucs_colors)

    results = {
        'deltas': deltas,
        'mean_dE': np.mean(deltas),
        'std_dE': np.std(deltas),
        'cv': np.std(deltas)/np.mean(deltas),
        'cam02ucs_colors': cam02ucs_colors
    }

    if show_series:
      print("CAM02-UCS coordinates for each color:")
      for color, coords in zip(color_values, cam02ucs_colors):
          print(f"{color}:  J'={coords[0]:.3f}, a'={coords[1]:.3f}, b'={coords[2]:.3f}")

      print("\nAdjacent ΔE values in CAM02-UCS:")
      for i, dE in enumerate(deltas):
          print(f" Between {color_values[i]} and {color_values[i+1]}: ΔE={dE:.3f}")

      print(f"\nMean ΔE: {results['mean_dE']:.3f}")
      print(f"Std Dev of ΔE: {results['std_dE']:.3f}")
      print(f"Coefficient of Variation (CV): {results['cv']:.3f}")

    return results

def visualize_color_components(cam02ucs_colors, show_chroma_hue=True, return_data=False):
    """
    Visualizes or returns lightness, chroma, hue data
    """
    L = [color[0] for color in cam02ucs_colors]
    a = [color[1] for color in cam02ucs_colors]
    b = [color[2] for color in cam02ucs_colors]

    C = [np.sqrt(x*x + y*y) for x, y in zip(a, b)]
    H = [np.degrees(np.arctan2(y, x)) % 360 for x, y in zip(a, b)]
    
    if return_data:
        return {
            'lightness': L,
            'chroma': C,
            'hue': H,
            'a': a,
            'b': b
        }

    if show_chroma_hue:
        fig, axes = plt.subplots(3, 1, figsize=(6, 10))
    else:
        fig, axes = plt.subplots(1, 1, figsize=(6, 3))
        axes = [axes]

    x = range(len(L))

    axes[0].plot(x, L, linestyle='-')
    axes[0].set_title("Lightness (J)")
    axes[0].set_ylim(0, 100)
    axes[0].set_xticks(x[::20])  # Show fewer ticks for 199 colors
    axes[0].tick_params(axis='x', labelsize=8)
    axes[0].grid(axis='y', color='#cccccc', linestyle='-', linewidth=0.25)

    if show_chroma_hue:
        axes[1].plot(x, C, linestyle='-')
        axes[1].set_title("Chroma")
        axes[1].set_ylim(0, max(C) * 1.1)
        axes[1].set_xticks(x[::20])
        axes[1].tick_params(axis='x', labelsize=8)
        axes[1].grid(axis='y', color='#cccccc', linestyle='-', linewidth=0.25)

        axes[2].plot(x, H, linestyle='-')
        axes[2].set_title("Hue")
        axes[2].set_ylim(0, 360)
        axes[2].set_xticks(x[::20])
        axes[2].tick_params(axis='x', labelsize=8)
        axes[2].grid(axis='y', color='#cccccc', linestyle='-', linewidth=0.25)

    plt.tight_layout()
    return fig

def create_color_bar_plot(color_list, color_type="hex", height=1):
    """
    Creates a color bar plot and returns the figure
    """
    num_colors = len(color_list)

    # Create figure with appropriate width
    fig, ax = plt.subplots(figsize=(10, height))

    # Remove margins and axes
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set_axis_off()

    # Set the plot limits
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Convert colors to proper format
    if color_type == "rgb":
        # Parse RGB strings like 'rgb(0, 31, 63)'
        def parse_rgb(rgb_str):
            values = rgb_str.replace('rgb(', '').replace(')', '').split(',')
            r, g, b = map(int, values)
            return (r/255, g/255, b/255)  # Normalize to 0-1 range
        color_list = [parse_rgb(c) for c in color_list]

    # Create rectangles for each color
    width = 1.0 / num_colors
    for i, color in enumerate(color_list):
        rect = plt.Rectangle((i * width, 0), width, 1, facecolor=color)
        ax.add_patch(rect)

    return fig
