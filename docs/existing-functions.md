## Libs

```py
import re
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from colorspacious import cspace_convert
```

## Functions for sequential palette generation and colour analysis

```py
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
          # You might want to raise an exception or handle this differently

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
    """
    cam02ucs_colors = convert_list_to_cam02ucs(color_values, color_type=color_type)

    deltas = compute_adjacient_dE(cam02ucs_colors)

    if show_series:
      print("CAM02-UCS coordinates for each color:")
      for color, coords in zip(color_values, cam02ucs_colors):
          print(f"{color}:  J'={coords[0]:.3f}, a'={coords[1]:.3f}, b'={coords[2]:.3f}")

      print("\nAdjacent ΔE values in CAM02-UCS:")
      for i, dE in enumerate(deltas):
          print(f" Between {color_values[i]} and {color_values[i+1]}: ΔE={dE:.3f}")

    print(f"\nMean ΔE: {np.mean(deltas):.3f}")
    print(f"Std Dev of ΔE: {np.std(deltas):.3f}")
    print(f"Coefficient of Variation (CV): {np.std(deltas)/np.mean(deltas):.3f}")

# Find closest colour in list
def find_closest_color(target_color, color_list, color_type="rgb"):
    """
    Finds and prints the closest color in color_list to target_color using CAM02-UCS color space.

    Args:
        target_color: The color to match (in same format as color_list)
        color_list: List of colors to search through
        color_type: Format of all colors ("rgb" or "hex")
    """
    # Convert target color to CAM02-UCS and get both formats
    if color_type == "rgb":
        match = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", target_color)
        if match:
            r, g, b = map(int, match.groups())
            target_rgb = target_color
            target_hex = f"#{r:02x}{g:02x}{b:02x}"
            target_norm = (r / 255.0, g / 255.0, b / 255.0)
            target_cam = cspace_convert(target_norm, "sRGB1", "CAM02-UCS")
    else:  # hex
        target_hex = target_color
        rgb = hex_to_rgb(target_color)
        r, g, b = (int(x * 255) for x in rgb)
        target_rgb = f"rgb({r}, {g}, {b})"
        target_cam = hex_to_cam02ucs(target_color)

    # Convert color list to CAM02-UCS
    cam02ucs_colors = convert_list_to_cam02ucs(color_list, color_type=color_type)

    # Find closest color
    min_distance = float('inf')
    closest_index = -1

    for i, color_cam in enumerate(cam02ucs_colors):
        distance = np.linalg.norm(np.array(color_cam) - np.array(target_cam))
        if distance < min_distance:
            min_distance = distance
            closest_index = i

    # Get both formats for closest color
    closest_color = color_list[closest_index]
    if color_type == "rgb":
        match = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", closest_color)
        r, g, b = map(int, match.groups())
        closest_rgb = closest_color
        closest_hex = f"#{r:02x}{g:02x}{b:02x}"
    else:  # hex
        closest_hex = closest_color
        rgb = hex_to_rgb(closest_color)
        r, g, b = (int(x * 255) for x in rgb)
        closest_rgb = f"rgb({r}, {g}, {b})"

    print("\nClosest color analysis:")
    print(f"Target color (RGB): {target_rgb}")
    print(f"Closest color (RGB): {closest_rgb}")
    print(f"Target color (HEX): {target_hex}")
    print(f"Closest color (HEX): {closest_hex}")
    print(f"Index in list: {closest_index}")
    print(f"CAM02-UCS distance: {min_distance:.3f}")

# Visualise Scale
def visualize_color_scale(color_list, color_type="hex", height=1):
    """
    Visualizes colors as a continuous scale of rectangles.

    Args:
        color_list: A list of hex or RGB color values
        color_type: "hex" or "rgb", indicating the format of color_list
        height: Height of the color bar in inches
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

    plt.show()

# Visualise results
def visualize_color_components(cam02ucs_colors, show_chroma_hue=False):
    L = [color[0] for color in cam02ucs_colors]
    a = [color[1] for color in cam02ucs_colors]
    b = [color[2] for color in cam02ucs_colors]

    if show_chroma_hue:
        C = [np.sqrt(x*x + y*y) for x, y in zip(a, b)]
        H = [np.degrees(np.arctan2(y, x)) % 360 for x, y in zip(a, b)]
        fig, axes = plt.subplots(3, 1, figsize=(6, 10))
    else:
        fig, axes = plt.subplots(1, 1, figsize=(6, 3))
        axes = [axes]

    x = range(len(L))

    axes[0].plot(x, L, linestyle='-')
    axes[0].set_title("Lightness (J)")
    axes[0].set_ylim(0, 100)
    axes[0].set_xticks(x)
    axes[0].tick_params(axis='x', labelsize=4)
    axes[0].grid(axis='y', color='#cccccc', linestyle='-', linewidth=0.25)

    if show_chroma_hue:
        axes[1].plot(x, C, linestyle='-')
        axes[1].set_title("Chroma")
        axes[1].set_ylim(0, 60)
        axes[1].set_xticks(x)
        axes[1].tick_params(axis='x', labelsize=4)
        axes[1].grid(axis='y', color='#cccccc', linestyle='-', linewidth=0.25)

        axes[2].plot(x, H, linestyle='-')
        axes[2].set_title("Hue")
        axes[2].set_ylim(0, 360)
        axes[2].set_xticks(x)
        axes[2].tick_params(axis='x', labelsize=4)
        axes[2].grid(axis='y', color='#cccccc', linestyle='-', linewidth=0.25)

    plt.tight_layout()
    plt.show()

def visualize_deltas(color_values, deltas, poly_order=3):
    median_delta = np.median(deltas)
    x = range(len(deltas))
    coeffs = np.polyfit(x, deltas, poly_order)
    p = np.poly1d(coeffs)
    trend = p(x)

    # Calculate median absolute deviation of trendline
    median_deviation = np.mean(np.abs(trend - median_delta))
    normalized_deviation = median_deviation / median_delta

    plt.bar(x, deltas, alpha=0.7, zorder=2)
    plt.hlines(median_delta, -0.5, len(deltas) - 0.5, colors='r',
              label=f'Median ΔE={median_delta:.3f}', zorder=2)
    plt.plot(x, trend, 'g--',
            label=f'Trend (order={poly_order})', zorder=2)

    plt.title(f'Adjacent ΔE Values (normalised trend deviation from median={normalized_deviation:.3f})')
    plt.xlabel("Color Pair Index")
    plt.ylabel("ΔE Value")
    plt.xticks(x)
    plt.tick_params(axis='x', labelsize=4)
    plt.grid(axis='y', color='#cccccc', linestyle='-', linewidth=0.25, zorder=0)
    plt.legend()
    plt.tight_layout()
    plt.show()

def run_analysis(color_list, target_color=None, color_type="rgb", show_series=False, show_chroma_hue=False, show_deltas=False, poly_order=3):
    """
    Runs the complete color analysis pipeline.
    """
    get_delta_e(color_list, color_type=color_type, show_series=show_series)
    visualize_color_scale(color_list, color_type=color_type)
    cam02ucs_colors = convert_list_to_cam02ucs(color_list, color_type=color_type)
    deltas = compute_adjacient_dE(cam02ucs_colors)
    visualize_color_components(cam02ucs_colors, show_chroma_hue=show_chroma_hue)
    visualize_deltas(color_list, deltas, poly_order=poly_order)

    if show_deltas:
      print("Index | Color Value | Delta E")
      print("------|-------------|----------")
      for i in range(len(color_list) - 1):
        print(f"{i:<5} | {color_list[i]:<11} | {deltas[i]:.3f}")

    if target_color:
      find_closest_color(target_color, color_list, color_type=color_type)


# Colour list comparison function (for the outcomes of the interpolator tests)
def compare_rgb_colors(*color_lists, log=True, detailed=False, return_differences=True):
    """
    Compare RGB color strings at the same indices across multiple lists and log the differences.

    Args:
        *color_lists: Two or more lists of RGB color strings
        log: Whether to print the comparison results
        detailed: Whether to include detailed RGB component differences in the log
        return_differences: Whether to return the difference list

    Returns:
        List of tuples containing (index, [differing_colors]) if return_differences is True
    """
    import re

    if len(color_lists) < 2:
        raise ValueError("At least two color lists are required for comparison")

    # Determine shortest list length to avoid index errors
    min_length = min(len(lst) for lst in color_lists)
    differences = []

    # Parse RGB values from a string like "rgb(0, 33, 150)"
    def parse_rgb(rgb_str):
        match = re.search(r'rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', rgb_str)
        if match:
            return tuple(int(match.group(i)) for i in range(1, 4))
        return None

    # Compare colors at each index
    for i in range(min_length):
        # Get colors at current index from all lists
        colors_at_index = [lst[i] for lst in color_lists]

        # Parse the RGB values from each color string
        rgb_values = [parse_rgb(color) for color in colors_at_index]

        # Skip if parsing failed for any color
        if any(val is None for val in rgb_values):
            continue

        # Check if all colors are identical
        if len(set(rgb_values)) > 1:  # If there's more than one unique color
            differences.append((i, colors_at_index, rgb_values))

    # Logging section
    if log:
        if not differences:
            print("No color differences found.")
        else:
            print(f"Found {len(differences)} color difference{'s' if len(differences) > 1 else ''}:")
            print("-" * 50)

            for idx, colors, rgb_values in differences:
                print(f"Difference at index {idx}:")

                for list_idx, (color, rgb) in enumerate(zip(colors, rgb_values)):
                    print(f"  List {list_idx+1}: {color}")

                if detailed:
                    print("  Component differences:")
                    # Transpose the RGB values to compare by component
                    components = list(zip(*rgb_values))

                    for comp_idx, comp_values in enumerate(['R', 'G', 'B']):
                        if len(set(components[comp_idx])) > 1:
                            print(f"    {comp_values}: {', '.join(str(v) for v in components[comp_idx])}")

                print("-" * 50)

    if return_differences:
        # Return just the index and colors, without the parsed RGB values
        return [(idx, colors) for idx, colors, _ in differences]
    return None
```

## Diverging specific functions

```py
# Find CIECAM-UCS midpoint between two RGB strings

def parse_rgb_string(rgb_string):
    """
    Parse a CSS-like rgb() string into a tuple of integers (0–255).
    Examples:
        "rgb(0,0,0)" -> (0, 0, 0)
        "rgb( 255 , 128 , 64 )" -> (255, 128, 64)
    """
    nums = re.findall(r"\d+", rgb_string)
    if len(nums) != 3:
        raise ValueError(f"Invalid rgb string: {rgb_string}")
    return tuple(map(int, nums))


def find_midpoint(rgb1, rgb2):
    """
    Return the perceptual midpoint between two sRGB colors in CAM02-UCS (CIECAM-UCS).

    Args:
        rgb1, rgb2: Either "rgb(r,g,b)" strings or 3-element tuples/lists/arrays.

    Returns:
        A string in the form "rgb(r,g,b)" with integer values 0–255.
    """
    def to_unit(c):
        arr = np.asarray(c, dtype=float)
        return arr / 255.0 if arr.max() > 1.0 else arr

    # Allow string input
    if isinstance(rgb1, str):
        rgb1 = parse_rgb_string(rgb1)
    if isinstance(rgb2, str):
        rgb2 = parse_rgb_string(rgb2)

    c1 = to_unit(rgb1)
    c2 = to_unit(rgb2)

    jpapbp1 = cspace_convert(c1, "sRGB1", "CAM02-UCS")
    jpapbp2 = cspace_convert(c2, "sRGB1", "CAM02-UCS")

    mid_jpapbp = (jpapbp1 + jpapbp2) / 2.0

    mid_rgb = cspace_convert(mid_jpapbp, "CAM02-UCS", "sRGB1")
    mid_rgb = np.clip(mid_rgb, 0.0, 1.0)

    # Round to 8-bit integers
    r, g, b = (mid_rgb * 255).round().astype(int)

    return f"rgb({r},{g},{b})"


# Smooth out Leonardo introduced lightness kink at seam

# When Leonardo stitches together the two sequential palletes it inadvertantly
# introduces a lightness spike at the seam between the two colours.
# This script smoothes the kink by calculating and applying a
# weighted regression locally ↓

def _parse(rgb_strings):
    return np.array([list(map(int, re.findall(r'\d+', s))) for s in rgb_strings], dtype=np.uint8)

def _to_rgb_strings(arr):
    return [f"rgb({int(r)}, {int(g)}, {int(b)})" for r,g,b in arr]

def fix_mid_kink_quadratic_cam02(rgb_strings, window=12, weight_edges=3, weight_inner=2, weight_peak=1):
    """
    1) Convert to CAM02-UCS (J', a', b')
    2) Find true peak k near middle (argmax J' within ±window)
    3) Fit y(d) = a*d^2 + c on indices k-2..k+2 (d = i-k), with least squares in J'
       -> slope at k is 0 by construction (dy/dd|d=0 = 0)
       -> weights: edges>inner>peak (keep shoulders; nudge the spike)
    4) Replace J'[k-2..k+2] with the fitted values; keep all other J' untouched
    5) Rebuild sRGB holding hue angle; trim chroma only if needed
    """
    rgb8 = _parse(rgb_strings)
    srgb1 = rgb8.astype(float)/255.0
    jab = cspace_convert(srgb1, "sRGB1", "CAM02-UCS")
    J, a, b = jab.T

    n = len(J); m = n//2
    lo = max(2, m - window); hi = min(n-3, m + window)
    k = lo + int(np.argmax(J[lo:hi+1]))        # measured apex (by J′)

    # indices and squared distances d^2 in the 5-point stencil
    idx = np.array([k-2, k-1, k, k+1, k+2])
    d2  = np.array([4.0, 1.0, 0.0, 1.0, 4.0])
    w   = np.array([weight_edges, weight_inner, weight_peak, weight_inner, weight_edges], dtype=float)

    y   = J[idx].astype(float)

    # weighted least squares for y_i ≈ a*d2_i + c
    S11 = np.sum(w*d2*d2)
    S12 = np.sum(w*d2)
    S22 = np.sum(w)
    T1  = np.sum(w*d2*y)
    T2  = np.sum(w*y)
    det = S11*S22 - S12*S12
    if det == 0:   # pathological, fall back to simple neighbour averaging
        v = 0.5*(J[k-1] + J[k+1])
        yfit = np.array([J[k-2], v, v, v, J[k+2]])
    else:
        a_q = ( T1*S22 - T2*S12)/det
        c_q = (-T1*S12 + T2*S11)/det
        # force concave cap
        a_q = min(a_q, 0.0)
        yfit = a_q*d2 + c_q

        # monotone guards inside the 5-point window
        yfit[1] = max(yfit[1], yfit[0])
        yfit[2] = max(yfit[2], yfit[1])
        yfit[3] = min(yfit[3], yfit[2])
        yfit[4] = min(yfit[4], yfit[3])

        # don’t overshoot original shoulders
        yfit[0] = min(yfit[0], J[k-2])
        yfit[4] = min(yfit[4], J[k+2])
        # keep peak no higher than original (only flatten the spike)
        yfit[2] = min(yfit[2], J[k])

    # write the new J′
    J_new = J.copy()
    J_new[idx] = yfit

    # rebuild sRGB: keep hue; scale chroma only if needed to stay inside [0,1]
    C = np.hypot(a, b)
    h = np.arctan2(b, a)

    def to_rgb01(Ji, Ci, hi):
        lo, hi_s = 0.0, 1.0
        ok = None
        for _ in range(22):
            mid = (lo + hi_s) / 2
            jab_try = np.array([Ji, Ci*mid*np.cos(hi), Ci*mid*np.sin(hi)])
            rgb_try = cspace_convert(jab_try, "CAM02-UCS", "sRGB1")
            if np.all((0 <= rgb_try) & (rgb_try <= 1)):
                ok = rgb_try; lo = mid
            else:
                hi_s = mid
        return ok if ok is not None else cspace_convert(np.array([Ji, 0, 0]), "CAM02-UCS", "sRGB1")

    out01 = np.vstack([to_rgb01(J_new[i], C[i], h[i]) for i in range(n)])
    return _to_rgb_strings((out01*255 + 0.5).astype(np.uint8))
```
