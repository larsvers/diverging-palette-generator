## Question 1

How did Cynthia Brewer make her color brewer diverging palettes? It is said she did them manually, but it's hard to believe she did when looking at their smoothness.

I'm asking as I'm interested in making my own diverging palettes and I'm using Leonardo for it at the moment (https://leonardocolor.io/scales.html#) however, comparing the lightness arc of color brewer vs leonardo created palettes suggests that Color Brewer palettes (first image) have more linear colour arms on either side and a smaller (but still smooth) hat on the top - whereas the leonardo produced lightness arc is different in that each arm bends earlier into the peak creating a wider "hat".

Additionally (as a side) the Color Brewer chroma curve is much more pronounced in the center and beautifully round on the arm ends, whereas Leonardo produces a slightly rougher ride.

I'm trying to understand how to produce a diverging palette closer to the way ColorBrewer is doing it. Can you help research the topic and find solutions?

## Response 1

To help you create diverging color palettes similar to those from ColorBrewer, could you clarify a few details? 1. Are you looking for a specific number of colors in the palette (e.g., 7 or 11 steps)? 2. What software or environment are you generating the palettes for (e.g., Python/Matplotlib, R, web design)? 3. Do you have a specific perceptual uniformity standard or color space you’d like the palette to adhere to (e.g., CAM02-UCS, CIELAB)? 4. Would you prefer open-source tools/scripts or are you open to proprietary solutions?

Once I have this, I’ll look into how Cynthia Brewer may have designed her palettes and how you can best replicate those qualities.

## Q2

(1) It should be a continuous diverging palette. I'm currently working with 199 steps, but it can be 99 (odd number to get a clear midpoint)
(2) I'm currently using Lenoardo to build the palettes, but am using Python to analyse them
(3) I think CAM02-UCS is best but I whatever is easiest to work with
(4) open source (if there's a clear proprietary winner I'd be interested in knowing about it)

## R2

Designing Diverging Palettes à la ColorBrewer

Brewer’s Diverging Palette Methodology

Cynthia Brewer’s ColorBrewer diverging schemes were hand-crafted with perceptual principles in mind. Brewer emphasized a neutral midpoint (often light in tone) flanked by two arms extending to contrasting hue extremes ￼. Each arm is essentially a mirror-image sequential palette: colors darken outward from the pale middle to darker, saturated end-colors ￼ ￼. This symmetry ensures the two extremes are visually balanced and that the central “critical value” (e.g. zero or a mean) is highlighted by the lightest color ￼. In practice, Brewer and colleagues arrived at these palettes through an iterative, manual design process – adjusting hues, lightness, and saturation by eye, then testing for clarity and printing/color-vision robustness. (In fact, Brewer’s palettes were evaluated for colorblind safety and photocopying; ColorBrewer will even filter out schemes that fail these tests ￼ ￼.) The resulting discrete schemes are not mathematically uniform in color difference, but each step is chosen to be clearly distinguishable and perceptually ordered ￼. The diverging sets thus appear smooth and balanced, with no single color drawing undue attention except the intentional highlight at the neutral center.

Lightness and Chroma: The Key to Smooth, Balanced Transitions

A hallmark of ColorBrewer’s aesthetic is a linear lightness “arc”: lightness (perceptual luminance) increases from each dark end toward the middle in a nearly linear fashion, peaking with the pale center color ￼. In other words, each half of a diverging palette forms a monotonic lightness ramp (one ascending, one descending), meeting at the high‑lightness midpoint ￼. This ensures the data values are ordered by lightness – a critical perceptual cue – in each direction away from the center. Achieving this typically involves plotting lightness vs. position and adjusting colors so that both arms trace symmetrical, straight(ish) lines. Brewer’s palettes were designed so that the midpoint is the brightest, most neutral color, and moving outward, each step gets progressively darker ￼ ￼. This prevents any “speed bumps” in value: a smoothly varying light/dark progression yields perceptual smoothness.

Chroma (color intensity) is the other crucial dimension. Brewer’s diverging schemes generally start at low chroma near the neutral center (often literally gray or off-white, which has zero chroma) and increase in saturation toward the mid-range of each side. At the far extremes (very dark colors), chroma may taper off again because extremely dark colors can’t appear very saturated. The result is a gentle, rounded chroma trajectory rather than a jagged jump. Often a diverging palette’s maximum colorfulness occurs around the midtones – providing vivid but not garish hues – and then chroma might slightly decrease for the darkest shades to avoid muddying into black. In practice, one can model this as a triangular chroma curve: starting at C=0 at the center, rising to a moderate peak, then perhaps falling off at the extreme ￼ ￼. Using a power curve instead of a straight line can “round out” the chroma transition, avoiding any abrupt saturation changes ￼ ￼. The goal is to keep saturation changes as smooth as lightness changes, so the palette has no sudden jumps in intensity or dull spots.

Notably, Brewer’s original palettes were created in an era before today’s advanced perceptual-uniform color tools. She often relied on experience and guidelines (e.g. Munsell value/chroma charts and empirical tweaking). The smooth appearance of ColorBrewer schemes validates this approach: even without strict equal-spacing of colors, their lightness and chroma gradients are steady enough to appear seamless. Modern analyses confirm that a well-designed diverging palette is essentially two sequential palettes joined at a neutral point, with balanced lightness/chroma on each side and a smooth hue rotation between the two hues ￼ ￼.

Replicating ColorBrewer’s Perceptual Qualities

To emulate ColorBrewer’s diverging palettes, focus on controlling lightness and chroma in a perceptually uniform color space. A common strategy is: choose your two endpoint hues (for example, a deep blue and a deep red) and a neutral middle (white or gray), then interpolate between them in CIELAB or CAM02-UCS space rather than RGB. Interpolating in a perceptual space ensures the intermediate colors change in a more uniform way aligned with human vision ￼ ￼. Specifically, you should enforce the “triangular” lightness profile – highest L (or J) at the center, decreasing roughly linearly to the ends ￼. At the same time, manage the chroma curve so that it starts near 0 at the center and increases outward. If you want a very smooth transition, allow chroma to peak gently (and optionally drop off for the darkest end) rather than simply ramping up and then stopping. Many tools let you add a slight easing to the interpolation curve (“smoothing”) so that the hue and saturation transitions are gradual ￼ ￼. Also decide how the hue should transition: if your midpoint is true neutral, the two halves can be treated independently (each going from neutral to a hue). If the midpoint is itself colored (like yellow in RdYlGn), you are effectively blending through that hue – you’ll need to ensure one hue rotates into the middle and then into the other hue without a clash. In practice this means picking a midpoint color that lies on a logical hue path between the end hues. (For example, red → yellow → green naturally traverses the spectrum, whereas using white/gray as midpoint lets each side simply fade to neutral.)

An open-source approach in Python is to leverage the CIECAM02 color model (or CIELAB) for interpolation. The colorspacious library is very useful here – it converts between sRGB and perceptual spaces like CIELAB or CAM02-UCS with ease ￼. For instance, you can convert your endpoint colors from sRGB into CAM02-UCS JCh coordinates (J = lightness, C = chroma, h = hue) ￼. Once in JCh, you could specify a target lightness curve – say J values 30 → 90 → 30 for a dark–light–dark diverging scheme. You can similarly set the chroma values (maybe 0 at the center, rising to e.g. 50 at midpoints, and perhaps down to 40 at the very ends if needed). With a series of J, C, h values defined (or by interpolating these parameters linearly or with a slight curve), you then convert back to sRGB. The result will be a continuous diverging colormap with as many steps as you like (e.g. 99 or 199). The key is that by working in a perceptual space, equal increments in J and moderate changes in C translate to smooth perceptual differences in the final palette. In fact, using CAM02-UCS, Euclidean distances correspond more closely to perceived color differences, so linearly interpolating there tends to yield a smoother palette than interpolating in RGB ￼. (If coding this from scratch, ensure you clamp values to the sRGB gamut, as some interpolated colors can stray out-of-gamut. Tools below handle this for you or warn of it.)

If coding directly isn’t desired, note that R’s colorspace package provides a convenient way to generate such palettes by name or parameters. The function diverging_hcl(n, h=c(h1,h2), c=c1, l=c(l1,l2)) constructs a diverging palette with n steps by defining end hues h1,h2, a chroma and luminance trajectory (it uses a balanced triangular lightness by default) ￼. Under the hood, it ensures the two arms have balanced luminance and chroma and a neutral center (chroma → 0 at midpoint) ￼. This can produce a continuous extension of Brewer-like palettes (in fact, some diverging_hcl presets are inspired by ColorBrewer originals ￼). You can request, say, diverging_hcl(201, palette="Blue-Red 3") to get a 201-step smooth scale modeled on a blue–red Brewer scheme. The advantage is that the heavy lifting of maintaining perceptual balance is done by the algorithm (using either linear or gently curved trajectories in HCL space with optional power transformations for smoothing ￼ ￼).

Tools for Palette Creation in Perceptual Color Spaces

1. Leonardo (Adobe Open Source): Leonardo is a modern tool specifically built for designing accessible color systems and data visualization palettes. It features dedicated modes for sequential, diverging, and qualitative scales ￼ ￼. Leonardo allows you to define key colors (endpoints and midpoint for a diverging scale) and then interpolate in various perceptual spaces – including CIELAB, LCH, CIECAM02 (listed as “CAM02”), Oklab, etc. ￼. You can toggle the interpolation space to see how it affects the smoothness and hue path. Leonardo also offers a “smoothing” option when more than two anchor colors are used, which applies a curve to the interpolation path to eliminate any sharp changes in hue or saturation ￼. This is very useful for achieving the “round” chroma transitions and avoiding any abrupt perceptual shifts. Furthermore, Leonardo provides visual analysis: it plots lightness and chroma profiles and even a 3D view of the color path in your chosen color space ￼ ￼. This helps confirm that your lightness is monotonic and your hue/chroma changes are well-behaved. Being open-source, Leonardo can be run as a web app and the underlying code (on GitHub) can potentially be integrated into workflows. It also supports outputting a large number of interpolated colors (“binned” scales up to an arbitrary count) – you can directly export, for example, a 255-color gradient for use in code ￼ ￼. In short, Leonardo is a powerful interactive solution to craft ColorBrewer-like palettes with fine control in CAM02-UCS, LCH, etc., no programming required.

2. Chroma.js (JavaScript library): Chroma.js is a popular JS library for color manipulations and scaling. It natively supports interpolation in Lab or LCH color space, which is the same principle we need for perceptual smoothness. For example, using Chroma.js one can do chroma.scale([color1, color2]).mode('lch').colors(199) to get a 199-step diverging scale between two specified endpoint colors in LCH space. Under the hood, chroma.js ensures lightness and hue interpolate smoothly, often yielding results similar to ColorBrewer’s continuous versions. Gregor Aisch (the author) and others have also built tools on top of chroma.js for palette picking. For instance, Tristen Brown’s HCL color picker uses chroma.js to let you interactively adjust hues, lightness, and chroma and see the resulting ramp ￼. Chroma.js is not Python, but its methodology can be mirrored in Python (e.g. via the colorspacious or colormath libraries). Its existence is worth noting because many web vis frameworks (like D3.js) use it or similar logic to generate smooth colormaps. In short, chroma.js demonstrates how open-source code can produce continuous Brewer-style gradients by interpolating in perceptual color models. If you are comfortable in JavaScript or just want to prototype, it’s an excellent tool. (There are also CLI and Node implementations, and one can always precompute a palette in JS and use the values in Python visualization.)

3. Colorspacious (Python library): As mentioned, Colorspacious is a Python toolkit for color space conversions and manipulation. It doesn’t automatically generate palettes, but it gives you the building blocks to do so. You can convert colors to CAM02-UCS JCh (or CIELAB Lab\*) ￼, perform interpolation or adjustments, then convert back. For example, you could take Brewer’s five or seven defined colors from a diverging palette, map them into JCh, and fit a smooth spline or linear interpolation through those points to yield a continuous gradient. Or simply take the two end colors and white as center and interpolate through CAM02-UCS linearly. Colorspacious ensures that what you get is in the perceptually uniform CAM02-UCS system where Euclidean distances correspond to perceptual differences, making linear interpolation meaningful. The library’s tutorial even shows how to manipulate image colors by adjusting J (lightness) and C (chroma) independently ￼ ￼ – the same concept can be applied to a palette: one could, say, enforce a certain lightness curve by adjusting the J channel array. Using Colorspacious requires writing a bit of code, but it’s Python-based and integrates well with numpy, so you can script the generation of a 199-length colormap precisely. This is ideal for integration into a Python data science workflow where you might want to programmatically create many palettes or fine-tune one.

4. viscm (Matplotlib’s vis-colormap tool): viscm is a GUI tool originally created to design sequential colormaps (it was used to develop matplotlib’s “viridis” palette). It works by letting you adjust a spline in CAM02 space and visualizing the result. While viscm was geared toward one-way ramps, it has been extended by the community to handle diverging map design as well ￼. With viscm, you can impose monotonic lightness and specify two endpoint hues, then tweak the curve that connects them in the hue-chroma plane. For instance, Kristen Thyng’s cmocean colormaps (oceanography-focused palettes) were created with viscm and include smooth diverging maps designed to be perceptually uniform ￼ ￼. Using viscm requires installing the tool (and PyQt for the GUI), but it provides a nice interactive way to experiment with CAM02-UCS-based curves. You get real-time feedback: a plot of lightness vs. index to ensure linearity, and simulated images to check for artifacts. Once satisfied, viscm can output a Python colormap definition. This is a more specialized option, but it’s open-source and has been proven in creating high-quality palettes.

5. R “colorspace” and HCL Wizard: We touched on the R colorspace package for programmatic generation. In addition, the team behind it provides an HCL Wizard (a web-based or Shiny app) for interactive palette design in HCL space ￼ ￼. This is very much in the spirit of Brewer’s work, since HCL (hue-chroma-luminance) is basically CIELUV in polar form – a perceptual color model. The HCL Wizard lets you choose palette type (diverging, etc.), then sliders for the trajectory of L and C and hues. It ensures palettes are perceptually balanced. Many preset palettes in the HCL Wizard/colorspace (like “Blue-Red 3”, “Green-Brown”, etc.) are actually balanced versions of ColorBrewer palettes that Zeileis et al. derived ￼. Thus, this tool/package is an academically-vetted way to recreate and modify Brewer-like schemes. You can output palettes of any length and even assess them under colorblind simulations. For those comfortable in R or using the web UI, it’s a robust solution.

6. Other Notables: NASA Ames Color Tool is a legacy but noteworthy application. It was originally developed for aviation charts and allows one to input CIE LCh values and get RGB ￼. Many cartographers (including presumably Brewer) have used it to manually pick palette colors by exploring the L–C–h space. Its interface quantizes lightness to 10-point steps and chroma to 10-point steps ￼, so it’s not as fine-grained as modern tools, but it educates on the concept of moving “diagonally” through the color volume (changing hue, lightness, chroma together) ￼. Adobe Photoshop (proprietary) also has features like Gradient Maps that can blend between specified colors smoothly ￼. In fact, the NASA Earth Observatory team described using Photoshop to convert a 9-color Brewer palette into a 256-color continuous ramp ￼. The process was manual (entering each color in an indexed palette or gradient editor), but it demonstrates that any software allowing Lab or smooth RGB interpolation can do the job. Among specialized commercial tools, Tableau and ArcGIS incorporate ColorBrewer palettes and allow custom diverging ramps, but they don’t necessarily improve on the core perceptual design – they mainly make Brewer’s schemes readily available. Another interesting resource is Kenneth Moreland’s work: Moreland (2009) presented an algorithm for generating smooth diverging colormaps, including an Excel-based tool and code implementations in multiple languages ￼ ￼. His “Cool-warm” diverging palette (blue-white-red) is now widely used in scientific visualization. Moreland’s approach is essentially what we’ve discussed – define the lightness/chroma trajectory and interpolate in LAB or a similar space – and he made reference implementations (Python class, MATLAB function, VTK integration, etc.) openly available ￼ ￼. These can be great starting points if one prefers not to reinvent the wheel in code. For instance, his Python class (linked from his page) can produce a diverging map given end colors and a midpoint.

In summary, open-source tools now make it quite straightforward to produce ColorBrewer-like diverging palettes. The fundamental recipe is: work in a perceptual color space (CIELAB, CAM02-UCS, HCL), enforce a smooth, symmetric lightness curve and gradual chroma and hue transitions, and sample as many intermediate colors as needed. Whether you do this by hand (using a GUI like Leonardo or HCL Wizard) or by code (using Colorspacious, chroma.js, or Moreland’s scripts), the outcome can closely match the admired qualities of Brewer’s originals: perceptually smooth gradients, balanced on both sides, with a highlighted neutral center. By leveraging these modern tools and methods, one can replicate and even extend ColorBrewer’s diverging palettes – for example, creating a 201-color version of “RdBu” or designing new hue pairs – all while maintaining the perceptual principles that make them effective. The Python ecosystem in particular has the building blocks to do this in a reproducible way, so you can generate ColorBrewer-style palettes on the fly for your visualization needs. ￼ ￼

## Q3

Thanks! So I've been working with Leonardo heavily as it gives me the additional benefit of adding my own colours which is very valuable as I am creating these palettes around our brand colours, so I can control proximity to our colours. I tried vicsm as well as chroma.js which seem quite opinionated (as is Leonardo) about the actual curve of the hat. Will they give me control over the power power transformations that control how quickly/slowly chroma and/or luminance are changed through the palette?

I just looked at hclwizard which seems the only tool that lets me control the power of the lightness curve as well as the chroma curve! CIE LUV seems less perceptional uniform than CAM02-UCS, however, as long as I can test results in CAM02-UCS (which I have functions for) I think this might be a good way forward.

Note, that I can work with R but can also work with Python and Javascript.

Q1) Are you aware of other tools exposing power transformations for lightness and chroma?
Q2) Could I use colorspace or another lib in another language to build a tool that also let's pick colours to be included in the palette? Alternatively I could have a tool as described above where I can play with colours and a series of functions would show me what hclwizard shows test proximity to a set of colours

Ultimately I want hclwizard (see image) with additional functions

1. testing colour proximity and
2. an output of ~199 colours sampled from the palette
3. and ideally a way to smoothen the chroma peaks

Do you think that would be possible?

## R3

Short answer: yes—what you want is totally doable.

⸻

Q1) Tools that expose power transforms for lightness/chroma
• R colorspace (and its HCL Wizard UI)
• diverging_hcl() lets you set power (or p1, p2) to control non-linear behavior of chroma and luminance (triangular “hat” for L); cmax controls peak chroma. ￼
• divergingx_hcl() is the flexible variant: separate p1..p4 to control chroma/luminance power independently on each arm, plus cmax1/2 for chroma peaks; also allows a colored (non-gray) midpoint. ￼
• The HCL Wizard is just a GUI over these; those “Power 1/Power 2” sliders are the exponent controls. ￼
• Python colorspace (the port of R colorspace)
• Provides the same diverging_hcl / divergingx_hcl APIs (with power parameters) and can emit Matplotlib colormaps. Installable from PyPI or GitHub. ￼
• chroma.js (JS)
• Doesn’t give separate L/C exponents, but it does expose .gamma() to shift the scale’s center (i.e., a power transform on the ramp) and .mode('lab'|'lch') with .correctLightness() to even the lightness gradient. Useful, but less surgical than colorspace. ￼
• viscm (Python GUI)
• Lets you shape the path with splines in CAM02; no explicit “power” knobs, but you can impose the same effect by moving control points on L/C curves. It’s great for inspection, less so for parametric control.

If you want knobs exactly like HCL Wizard (separate exponents per arm for L and C), colorspace (R or Python) is the only one that exposes them cleanly out of the box. ￼

⸻

Q2) Building your own tool with brand-color constraints, tests, and 199-step export

Option A — Stay in R (quickest path)
• Use colorspace::divergingx_hcl() under a small Shiny app (the HCL Wizard code is open). Add: 1. a brand-color proximity panel that converts your palette + brand colors to CAM02-UCS and reports ΔE (Euclidean in J’a’b’); 2. an export button that writes 199 samples; 3. a chroma smoothing control that maps to cmax1/2 + p1..p4.
• divergingx_hcl() gives you the exact sliders you want (H1/H2, L1/L2, C1/Cmax, p1..p4). ￼

Option B — Python (works great with your current analysis)

Use the Python port of colorspace for palette generation + colorspacious for CAM02-UCS checks:

# pip install colorspace colorspacious

import numpy as np
from colorspace import divergingx_hcl
from colorspacious import cspace_convert

# 1) build palette with explicit power exponents (per arm for C and L)

pal = divergingx_hcl(
n = 199,
h1=255, h2=np.nan, h3=10, # left hue, (mid unused for gray), right hue
c1=50, c2=np.nan, c3=50, # chroma on each side; mid=0 by default
l1=20, l2=97, l3=20, # luminance ends + bright midpoint (the “hat”)
p1=1.0, p2=0.8, # left arm: p1=chroma power, p2=luminance power
p3=1.0, p4=0.8, # right arm: p3=chroma power, p4=luminance power
cmax1=60, cmax2=60 # optional soft, rounded chroma peak
).hex()

# 2) proximity test in CAM02-UCS

rgb = np.array([[int(h[i:i+2],16) for i in (1,3,5)] for h in pal])/255.0
jab = cspace_convert(rgb, "sRGB1", "CAM02-UCS") # J' a' b'

brand_rgb = np.array([[0.06,0.43,0.86]]) # your brand blue, for example
brand_jab = cspace_convert(brand_rgb, "sRGB1", "CAM02-UCS")

dist = np.sqrt(((jab - brand_jab)\*\*2).sum(axis=1)) # ΔE_CAM02-UCS to brand color
closest_index = np.argmin(dist)

    •	The “hat width”: use luminance powers (p2 and p4).
    •	p < 1 → faster drop from the center → narrower hat (closer to ColorBrewer).
    •	p > 1 → slower drop → wider hat (what you observed from some Leonardo results).
    •	The rounded chroma: control with cmax1/2 + chroma powers (p1, p3). Higher p grows chroma slowly near the center and more rapidly later; you can balance that against cmax to get the “pronounced mid, gentle ends” look.  ￼

Why CAM02-UCS? With colorspacious you can both verify monotonic lightness and compute ΔE reliably; conversion is a one-liner. ￼

Option C — JavaScript (fits Svelte)
• Use chroma.js for LCH/Lab interpolation and .gamma() to nudge the center, then add your own exponents by remapping the position parameter t → t^pL (for luminance) and controlling chroma by scaling the LCH vector length with t^pC. You’ll miss per-arm built-ins, but it’s straightforward to implement with a couple of functions. ￼

⸻

Practical tuning tips (to match the ColorBrewer “feel”) 1. Linear arms, smaller hat: keep L at ends ≈ 20–30, set midpoint L high (95–98), and use luminance power < 1 on both sides (e.g., 0.7–0.9). This makes the lightness drop faster near the center → visually “tighter” hat. (This is exactly what HCL Wizard’s Power sliders do.) ￼ 2. Round chroma ends: push chroma peaks toward mid-arm using moderate cmax (e.g., 55–65) and p1/p3 ≳ 1.0 so chroma ramps in gently from the center, and consider slightly reducing chroma near the very dark ends (keep c at ends a bit lower than the peak). divergingx_hcl() supports this with c1/c3 vs. cmax1/2. ￼ 3. Hue handling: with a neutral midpoint, keep each arm at a constant hue (left = H1, right = H3). If you want a colored midpoint (à la RdYlGn), divergingx_hcl() lets you route through h2 to keep a smooth rotation. ￼ 4. Gamut safety: use the fixup=TRUE/“Correct colors” option (R/py colorspace) so out-of-gamut colors are corrected to valid sRGB. ￼ 5. 199-sample export: both R and Python colorspace can emit a Matplotlib colormap or a list of hex values at any length (default 256). In Python: pal.cmap(n=199). ￼

⸻

If you’d like a template
• R (colorspace):

library(colorspace)
pal <- divergingx_hcl(
n = 199,
h1 = 255, h2 = NA, h3 = 10,
c1 = 50, c2 = NA, c3 = 50, cmax1 = 60, cmax2 = 60,
l1 = 20, l2 = 97, l3 = 20,
p1 = 1.0, p2 = 0.8, # left: chroma, luminance
p3 = 1.0, p4 = 0.8 # right: chroma, luminance
)

# writeLines(hex(pal), "my_diverging_199.txt")

(Those arguments mirror the HCL Wizard sliders.) ￼
• Python (colorspace + colorspacious): see the snippet above for 199 steps + ΔE_CAM02-UCS.

⸻

Extras you asked for 1. Color proximity tests to brand colors
• Convert both palette and brand colors to CAM02-UCS and compute Euclidean distance; report the closest swatch and ΔE. That’s exactly what colorspacious is for. ￼ 2. 199-color output
• Built in: divergingx_hcl(n=199, ...) (R or Python), or .cmap(n=199) for a Matplotlib colormap. ￼ 3. “Smoothen chroma peaks” control
• In colorspace, prefer cmax1/2 + p1..p4 (that’s exactly what the HCL Wizard uses behind the scenes). For even softer roll-offs you can map the distance-from-center |t| through a gentle easing before applying chroma, e.g. replace |t| by smoothstep(0,1,|t|) or use a raised-cosine:
C(|t|) = C_end + (C_peak - C_end) \* sin(π|t|)^q (choose q≈1–2). Implementing this is trivial if you’re doing your own JCH path.

⸻

TL;DR
• Use divergingx_hcl() (R or the Python port) to get explicit power controls for both arms and both channels—that’s the lever you need to make the hat narrower and the chroma curve rounder (ColorBrewer-style). ￼
• Use colorspacious to verify smoothness and check ΔE_CAM02-UCS proximity to brand colors. ￼
• If you’d rather stay in JS, chroma.js + your own t^p reparameterization gets you close; .gamma() can also nudge the center weighting. ￼

If you want, I can sketch a tiny Svelte or Streamlit UI that mirrors HCL Wizard’s sliders (p1..p4, cmax1/2, L/H settings), adds a brand-color proximity table, and exports 199 samples.
