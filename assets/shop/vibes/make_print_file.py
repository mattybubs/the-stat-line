#!/usr/bin/env python3
"""Render the VIBES R HIGH Toys R Us v3 design as a Printful-ready transparent PNG.
Canvas 3000x4000 (12x16in @ 300 DPI), design 2700px wide, sRGB, transparent.
No blur, full opacity — print needs crisp edges."""
import math, os
from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(BASE, "fonts")
OUT = os.path.join(BASE, "tsl-vibes-r-high-toys-print.png")

RED = (238, 44, 36, 255)
ORANGE = (247, 148, 29, 255)
GREEN = (0, 166, 81, 255)
BLUE = (27, 79, 156, 255)
CYCLE = [RED, ORANGE, GREEN]
TEXT = "VIBES R HIGH"
BOUNCE = [0, -0.06, 0.05, -0.04, 0.04, 0, -0.05, 0.04, -0.06, 0.05, -0.04, 0.02]
TARGET_W = 2700
CANVAS = (3000, 4000)
Y_TOP = 480

def load(size):
    return ImageFont.truetype(os.path.join(FONTS, "Baloo2-ExtraBold.ttf"), size)

def tw(d, s, f):
    return d.textbbox((0, 0), s, font=f)[2]

def star_points(cx, cy, r_out, r_in, rot=-90):
    pts = []
    for i in range(10):
        ang = math.radians(rot + i * 36)
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts

def measure(U):
    img = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fb, fr = load(U), load(int(U * 1.35))
    widths = []
    for ch in TEXT:
        if ch == " ":
            widths.append(int(0.23 * U))
        elif ch == "R":
            widths.append(int(tw(d, "R", fr) * 0.92))
        else:
            widths.append(int(tw(d, ch, fb) * 0.92))
    return sum(widths), widths

def render(U, widths):
    W, H = CANVAS
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fb, fr = load(U), load(int(U * 1.35))
    total = sum(widths)
    x = (W - total) / 2
    asc_s = fb.getmetrics()[0]
    asc_r = fr.getmetrics()[0]
    ci = 0
    for idx, (ch, cw) in enumerate(zip(TEXT, widths)):
        if ch == " ":
            x += cw
            continue
        if ch == "R":
            rw = cw
            rh = int(1.93 * U)
            r_img = Image.new("RGBA", (rw + int(0.15 * U), rh), (0, 0, 0, 0))
            rd = ImageDraw.Draw(r_img)
            rd.text((int(0.06 * U), 0), "R", font=fr, fill=BLUE)
            r_img = ImageOps.mirror(r_img)
            sd = ImageDraw.Draw(r_img)
            scx = int(rw * 0.36) + int(0.16 * U)
            scy = int(rh * 0.36) + int(0.27 * U)
            sr = int(0.20 * U)
            # fill the R's counter with blue so the star sits on solid blue (like the logo)
            import numpy as np
            from scipy.ndimage import binary_fill_holes, binary_dilation
            _a = np.array(r_img.split()[3])
            _solid = _a > 0
            _hole = binary_fill_holes(_solid) & ~_solid
            _hole = binary_dilation(_hole, iterations=2)
            _arr = np.array(r_img)
            _arr[_hole] = BLUE
            r_img = Image.fromarray(_arr, "RGBA")
            sd = ImageDraw.Draw(r_img)
            sd.polygon(star_points(scx, scy, sr, sr * 0.42), fill=(255, 255, 255, 255))
            y_r = Y_TOP + (asc_s - asc_r)
            img.paste(r_img, (int(x), int(y_r)), r_img)
        else:
            d.text((x, Y_TOP + BOUNCE[idx] * U), ch, font=fb, fill=CYCLE[ci % 3])
            ci += 1
        x += cw
    return img

w100, _ = measure(100)
U = int(100 * TARGET_W / w100)
_, widths = measure(U)
img = render(U, widths)
img.save(OUT, dpi=(300, 300))
print(f"U={U} design_width={sum(widths)} saved {OUT} size={img.size}")

# verify: corners transparent, design opaque, bbox of ink
alpha = img.split()[3]
bbox = alpha.getbbox()
print("ink bbox:", bbox)
print("corner alpha (0,0):", alpha.getpixel((0, 0)), "| center alpha:", alpha.getpixel((1500, 600)))
