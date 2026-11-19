#!/usr/bin/env python3
"""TSL Vibes line v1: composite cream designs onto blank charcoal tee bases.
Pocket tee: small sun mark + VIBES GUY / VIBES GIRL on the pocket.
Plain tee: THE VIBES ARE HIGH big center-chest with sun above.
Type is drawn programmatically (never AI text)."""
from PIL import Image, ImageDraw, ImageFont
import os

BASE = "/home/hatch/workspace/statline-blog/assets/shop/vibes"
POCKET = os.path.join(BASE, "media-generation-vibes-pocket-tee-base-v1-0-ee1c0d6d-3415-4dfe-97df-078ef03dbbf5.webp")
PLAIN = os.path.join(BASE, "media-generation-vibes-plain-tee-base-v1-0-45d7835c-b027-4913-9959-406e328a2811.webp")

CREAM = (245, 238, 222, 225)  # warm cream print ink, slightly softened

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]

def load_font(size):
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def draw_sun(d, cx, cy, r, color, ray_len=14, ray_w=5):
    """Minimal sun: filled disc + 8 short rays."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    import math
    for k in range(8):
        ang = math.radians(k * 45)
        x1 = cx + math.cos(ang) * (r + 6)
        y1 = cy + math.sin(ang) * (r + 6)
        x2 = cx + math.cos(ang) * (r + 6 + ray_len)
        y2 = cy + math.sin(ang) * (r + 6 + ray_len)
        d.line([x1, y1, x2, y2], fill=color, width=ray_w)

def text_width(d, s, font):
    b = d.textbbox((0, 0), s, font=font)
    return b[2] - b[0]

def composite(base_path, out_path, draw_fn):
    img = Image.open(base_path).convert("RGB")
    w, h = img.size
    print(f"{os.path.basename(base_path)}: {w}x{h}")
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    draw_fn(d, overlay, w, h)
    from PIL import ImageFilter
    overlay = overlay.filter(ImageFilter.GaussianBlur(0.6))  # soften so it reads printed, not stickered
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    img.save(out_path, "PNG")
    print(f"saved {out_path}")

# --- pocket tee: sun + VIBES GUY / VIBES GIRL centered on the pocket ---
# Pocket center from visual inspection: ~0.618w, ~0.40h; pocket ~0.13w wide.
def pocket_design(label):
    def fn(d, overlay, w, h):
        # print ABOVE the pocket on the chest — pocket stays blank,
        # nothing touches any seam
        cx = int(w * 0.618)
        font = load_font(int(w * 0.016))
        sun_r = int(w * 0.011)
        sun_cy = int(h * 0.255)
        draw_sun(d, cx, sun_cy, sun_r, CREAM, ray_len=int(w * 0.006), ray_w=4)
        tw = text_width(d, label, font)
        d.text((cx - tw / 2, int(h * 0.282)), label, font=font, fill=CREAM)
    return fn

composite(POCKET, os.path.join(BASE, "tsl-vibes-guy-pocket-tee-v4.png"), pocket_design("VIBES GUY"))
composite(POCKET, os.path.join(BASE, "tsl-vibes-girl-pocket-tee-v4.png"), pocket_design("VIBES GIRL"))

# --- plain tee: THE VIBES / ARE HIGH big center chest with sun above ---
def slogan_design(d, overlay, w, h):
    cx = int(w * 0.50)
    font_big = load_font(int(w * 0.047))
    sun_r = int(w * 0.022)
    sun_cy = int(h * 0.305)
    draw_sun(d, cx, sun_cy, sun_r, CREAM, ray_len=int(w * 0.011), ray_w=6)
    y = int(h * 0.345)
    for line in ("THE VIBES", "ARE HIGH"):
        tw = text_width(d, line, font_big)
        d.text((cx - tw / 2, y), line, font=font_big, fill=CREAM)
        y += int(w * 0.056)

FONTS_DIR = os.path.join(BASE, "fonts")

def load_named(name, size):
    p = os.path.join(FONTS_DIR, name)
    if os.path.exists(p):
        return ImageFont.truetype(p, size)
    return load_font(size)

def slogan_design_v3(d, overlay, w, h):
    """THE VIBES ARE HIGH in Anton, betting line VIBES -110 underneath."""
    cx = int(w * 0.50)
    font_big = load_named("Anton-Regular.ttf", int(w * 0.072))
    font_sub = load_named("BebasNeue-Regular.ttf", int(w * 0.030))
    y = int(h * 0.315)
    for line in ("THE VIBES", "ARE HIGH"):
        tw = text_width(d, line, font_big)
        d.text((cx - tw / 2, y), line, font=font_big, fill=CREAM)
        y += int(w * 0.082)
    sub = "VIBES -110"
    sw = text_width(d, sub, font_sub)
    rule_y = y + int(w * 0.012)
    d.line([cx - sw / 2, rule_y, cx + sw / 2, rule_y], fill=CREAM, width=3)
    d.text((cx - sw / 2, rule_y + int(w * 0.010)), sub, font=font_sub, fill=CREAM)

def slogan_design_v4(d, overlay, w, h):
    """THE VIBES ARE HIGH in Anton — headline only, no subline."""
    cx = int(w * 0.50)
    font_big = load_named("Anton-Regular.ttf", int(w * 0.072))
    y = int(h * 0.33)
    for line in ("THE VIBES", "ARE HIGH"):
        tw = text_width(d, line, font_big)
        d.text((cx - tw / 2, y), line, font=font_big, fill=CREAM)
        y += int(w * 0.082)

def bet_design(d, overlay, w, h):
    """Betting reference, small and clean: VIBES -110 only, no eyebrow."""
    cx = int(w * 0.50)
    font_small = load_named("Anton-Regular.ttf", int(w * 0.022))
    line = "VIBES -110"
    tw = text_width(d, line, font_small)
    d.text((cx - tw / 2, int(h * 0.33)), line, font=font_small, fill=CREAM)

def vibes_r_high_design(d, overlay, w, h):
    """VIBES R HIGH — the R mirrored backwards, Toys R Us style, in Anton."""
    from PIL import ImageOps
    cx = int(w * 0.50)
    font_big = load_named("Anton-Regular.ttf", int(w * 0.062))
    left = "VIBES "
    right = " HIGH"
    lw = text_width(d, left, font_big)
    rw = text_width(d, "R", font_big)
    rtw = text_width(d, right, font_big)
    total = lw + rw + rtw
    x0 = cx - total / 2
    y = int(h * 0.36)
    d.text((x0, y), left, font=font_big, fill=CREAM)
    # mirrored R glyph, same size and baseline as the rest of the line
    r_img = Image.new("RGBA", (rw + 10, int(w * 0.080)), (0, 0, 0, 0))
    rd = ImageDraw.Draw(r_img)
    rd.text((5, 0), "R", font=font_big, fill=CREAM)
    r_img = ImageOps.mirror(r_img)
    overlay.paste(r_img, (int(x0 + lw), y), r_img)
    d.text((x0 + lw + rw, y), right, font=font_big, fill=CREAM)

def vibes_r_high_toys(d, overlay, w, h):
    """VIBES R HIGH in Baloo 2 ExtraBold, Toys R Us colors, backwards R."""
    from PIL import ImageOps
    font_big = load_named("Baloo2-ExtraBold.ttf", int(w * 0.062))
    colors = [(30, 111, 217), (230, 51, 41), (245, 163, 0), (0, 166, 81), (255, 210, 0)]
    text = "VIBES R HIGH"
    space_w = int(w * 0.018)
    widths = [text_width(d, ch, font_big) if ch != " " else space_w for ch in text]
    total = sum(widths)
    x = int(w * 0.50) - total / 2
    y = int(h * 0.36)
    ci = 0
    for ch, cw in zip(text, widths):
        if ch == " ":
            x += cw
            continue
        color = colors[ci % len(colors)] + (235,)
        ci += 1
        if ch == "R":
            r_img = Image.new("RGBA", (cw + 10, int(w * 0.080)), (0, 0, 0, 0))
            rd = ImageDraw.Draw(r_img)
            rd.text((5, 0), "R", font=font_big, fill=color)
            r_img = ImageOps.mirror(r_img)
            overlay.paste(r_img, (int(x), y), r_img)
        else:
            d.text((x, y), ch, font=font_big, fill=color)
        x += cw

def star_points(cx, cy, r_out, r_in, rot=-90):
    import math
    pts = []
    for i in range(10):
        ang = math.radians(rot + i * 36)
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts

def vibes_r_high_toys_v3(d, overlay, w, h):
    """VIBES R HIGH matching the real Toys R Us logo: logo color order,
    big blue backwards R with a white star, bouncy baseline."""
    from PIL import ImageOps
    font_big = load_named("Baloo2-ExtraBold.ttf", int(w * 0.052))
    font_r = load_named("Baloo2-ExtraBold.ttf", int(w * 0.070))
    red = (238, 44, 36)
    orange = (247, 148, 29)
    green = (0, 166, 81)
    blue = (27, 79, 156)
    cycle = [red, orange, green]
    text = "VIBES R HIGH"
    space_w = int(w * 0.012)
    widths = []
    for ch in text:
        if ch == " ":
            widths.append(space_w)
        elif ch == "R":
            widths.append(int(text_width(d, "R", font_r) * 0.92))
        else:
            widths.append(int(text_width(d, ch, font_big) * 0.92))
    total = sum(widths)
    x = int(w * 0.50) - total / 2
    y = int(h * 0.36)
    asc_small = font_big.getmetrics()[0]
    asc_r = font_r.getmetrics()[0]
    bounce = [0, -5, 4, -3, 3, 0, -4, 3, -5, 4, -3, 2]
    ci = 0
    for idx, (ch, cw) in enumerate(zip(text, widths)):
        if ch == " ":
            x += cw
            continue
        if ch == "R":
            color = blue + (235,)
            rw = cw
            rh = int(w * 0.100)
            r_img = Image.new("RGBA", (rw + 12, rh), (0, 0, 0, 0))
            rd = ImageDraw.Draw(r_img)
            rd.text((6, 0), "R", font=font_r, fill=color)
            r_img = ImageOps.mirror(r_img)
            # fill the R's counter with blue so the star sits on solid blue (like the logo)
            import numpy as np
            from scipy.ndimage import binary_fill_holes, binary_dilation
            _a = np.array(r_img.split()[3])
            _solid = _a > 0
            _hole = binary_fill_holes(_solid) & ~_solid
            _hole = binary_dilation(_hole, iterations=1)
            _arr = np.array(r_img)
            _arr[_hole] = blue + (235,)
            r_img = Image.fromarray(_arr, "RGBA")
            # white star in the bowl (mirrored R: bowl on the left)
            sd = ImageDraw.Draw(r_img)
            scx, scy = int(rw * 0.36) + 13, int(rh * 0.36) + 22
            sr = int(w * 0.009)
            sd.polygon(star_points(scx, scy, sr, sr * 0.42), fill=(255, 255, 255, 235))
            y_r = y + (asc_small - asc_r)
            overlay.paste(r_img, (int(x), y_r), r_img)
        else:
            color = cycle[ci % 3] + (235,)
            ci += 1
            d.text((x, y + bounce[idx]), ch, font=font_big, fill=color)
        x += cw

composite(PLAIN, os.path.join(BASE, "tsl-vibes-r-high-toys-v3.png"), vibes_r_high_toys_v3)
composite(PLAIN, os.path.join(BASE, "tsl-vibes-minus-110-tee-v3.png"), bet_design)
print("done")
