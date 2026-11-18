#!/usr/bin/env python3
"""TSL shop apparel v2 — TYPOGRAPHY ONLY.
Matt rejected v1: drawn pucks/footballs were corny, hated the score in the
design. V2: the slogan in big type IS the design. No sports-object drawings,
no scores, no numbers, no dates. Small chest hit + huge back print.
PIL + real fonts (Anton / Graduate), one ink on transparent, 300 DPI.
"""
import math, os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.expanduser("~/workspace/statline-blog/assets/shop")
FONTS = os.path.expanduser("~/workspace/tools/fonts")
ANTON = os.path.join(FONTS, "Anton-Regular.ttf")
GRADUATE = os.path.join(FONTS, "Graduate-Regular.ttf")

WHITE = (255, 255, 255, 255)
VOLT = (200, 255, 46, 255)
ERASE = (0, 0, 0, 0)


def font(path, size):
    return ImageFont.truetype(path, int(size))


def fit_font(path, text, max_w, start_size, tracking=0.0):
    size = start_size
    while size > 40:
        f = font(path, size)
        w = sum(f.getlength(ch) for ch in text) + tracking * size * max(len(text) - 1, 0)
        if w <= max_w:
            return f, size
        size -= 5
    return font(path, 40), 40


def text_w(f, text, tracking=0.0):
    return sum(f.getlength(ch) for ch in text) + tracking * f.size * max(len(text) - 1, 0)


def draw_tracked(d, cx, y, text, f, ink, tracking=0.0):
    total = text_w(f, text, tracking)
    x = cx - total / 2
    for ch in text:
        d.text((x, y), ch, font=f, fill=ink)
        x += f.getlength(ch) + tracking * f.size


def star(d, cx, cy, r_out, r_in, ink):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=ink)


def arch_text(img, text, f, cx, apex_y, radius, ink, tracking=0.0):
    """Upward-arched text; apex_y = top of the middle letter."""
    advances = []
    total = 0.0
    for ch in text:
        w = f.getlength(ch) + tracking * f.size
        advances.append(w)
        total += w
    total -= tracking * f.size
    span = total / radius
    a = -span / 2
    cy_center = apex_y + radius
    for ch, adv in zip(text, advances):
        mid = a + (adv / radius) / 2
        gw = int(f.getlength(ch)) + 8
        gh = int(f.size * 1.5) + 8
        tile = Image.new("RGBA", (gw, gh), (0, 0, 0, 0))
        td = ImageDraw.Draw(tile)
        td.text((gw / 2, gh / 2), ch, font=f, fill=ink, anchor="mm")
        tile = tile.rotate(-math.degrees(mid), resample=Image.BICUBIC, expand=True)
        px = cx + radius * math.sin(mid)
        py = cy_center - radius * math.cos(mid)
        img.paste(tile, (int(px - tile.width / 2), int(py - tile.height / 2)), tile)
        a += adv / radius


def save(img, name):
    path = os.path.join(OUT, name)
    img.save(path, dpi=(300, 300))
    print(f"saved {name}  {img.size}")
    return path


def new_canvas(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


def stacked_front(lines, max_w, ink, name, start_size=380):
    """Small two-line stacked chest hit, centered on 3000x1200."""
    img = new_canvas(3000, 1200)
    d = ImageDraw.Draw(img)
    f, size = fit_font(ANTON, max(lines, key=len), max_w, start_size)
    lh = int(size * 1.08)
    total_h = lh * len(lines)
    y = (1200 - total_h) // 2
    for line in lines:
        draw_tracked(d, 1500, y, line, f, ink, tracking=0.04)
        y += lh
    save(img, name)


# ---------------------------------------------------------------- 1. HAT TRICK CLUB (white)
stacked_front(["HAT TRICK", "CLUB"], 1500, WHITE, "hat-trick-club-front-v2.png")

img = new_canvas(2400, 3000)
f, _ = fit_font(ANTON, "HAT TRICK CLUB", 2200, 340)
arch_text(img, "HAT TRICK CLUB", f, 1200, 560, 1400, WHITE, tracking=0.03)
d = ImageDraw.Draw(img)
for sx in (1200 - 170, 1200, 1200 + 170):
    star(d, sx, 1560, 32, 13, WHITE)
save(img, "hat-trick-club-back-v2.png")

# ---------------------------------------------------------------- 2. TOP SHELF (hat, front only, white)
img = new_canvas(3000, 1200)
d = ImageDraw.Draw(img)
f, _ = fit_font(GRADUATE, "TOP SHELF", 2200, 340)
tw = text_w(f, "TOP SHELF", 0.02)
d.text((1500 - tw / 2, 430), "TOP SHELF", font=f, fill=WHITE)
# (Graduate has no per-letter tracking helper here; single centered draw)
save(img, "top-shelf-hat-front-v2.png")

# ---------------------------------------------------------------- 3. ANY GIVEN SUNDAY (white)
stacked_front(["ANY GIVEN", "SUNDAY"], 1500, WHITE, "any-given-sunday-front-v2.png")

img = new_canvas(2400, 3000)
f, _ = fit_font(ANTON, "ANY GIVEN SUNDAY", 2200, 310)
arch_text(img, "ANY GIVEN SUNDAY", f, 1200, 560, 1450, WHITE, tracking=0.03)
save(img, "any-given-sunday-back-v2.png")

# ---------------------------------------------------------------- 4. SCORIGAMI CLUB (volt)
img = new_canvas(3000, 1200)
d = ImageDraw.Draw(img)
f, _ = fit_font(ANTON, "SCORIGAMI CLUB", 1500, 380)
draw_tracked(d, 1500, 500, "SCORIGAMI CLUB", f, VOLT, tracking=0.04)
save(img, "scorigami-club-front-v2.png")

img = new_canvas(2400, 3000)
d = ImageDraw.Draw(img)
f, _ = fit_font(ANTON, "SCORIGAMI", 2100, 470)
draw_tracked(d, 1200, 900, "SCORIGAMI", f, VOLT, tracking=0.03)
f2, _ = fit_font(ANTON, "CLUB", 800, 170)
draw_tracked(d, 1200, 1560, "CLUB", f2, VOLT, tracking=0.18)
save(img, "scorigami-club-back-v2.png")

print("done")
