#!/usr/bin/env python3
"""TSL shop apparel v1 — programmatic print files (PIL).
All type drawn with real fonts (Anton / Graduate); nothing AI-generated,
so no garbled text. One ink color per design on transparent, 300 DPI.
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
    """Largest size (<= start) whose rendered width fits max_w."""
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
    """Draw text centered at cx, top y, with per-letter tracking."""
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


def puck(img, cx, cy, w, h, ink):
    """Hockey puck cylinder silhouette with a gap line under the top disc."""
    d = ImageDraw.Draw(img)
    top_h = h * 0.42
    # body (near-sharp bottom corners, like a real puck)
    d.rounded_rectangle([cx - w / 2, cy - h / 2 + top_h * 0.45,
                         cx + w / 2, cy + h / 2], radius=h * 0.08, fill=ink)
    # top disc
    d.ellipse([cx - w / 2, cy - h / 2, cx + w / 2, cy - h / 2 + top_h], fill=ink)
    # clear gap between disc and body so the top face reads
    d.rectangle([cx - w / 2, cy - h / 2 + top_h - 1,
                 cx + w / 2, cy - h / 2 + top_h + h * 0.08], fill=ERASE)


def football(img, cx, cy, w, h, ink):
    """American football silhouette; laces cut out as transparent lines."""
    d = ImageDraw.Draw(img)
    n = 80
    top, bot = [], []
    for i in range(n + 1):
        t = -1 + 2 * i / n
        x = cx + t * w / 2
        dy = (h / 2) * (1 - t * t) ** 0.65
        top.append((x, cy - dy))
        bot.append((x, cy + dy))
    d.polygon(top + bot[::-1], fill=ink)
    # laces: one long line + 5 ticks, erased
    lw = max(6, int(w * 0.018))
    d.line([cx - w * 0.17, cy, cx + w * 0.17, cy], fill=ERASE, width=lw)
    for i in range(-2, 3):
        x = cx + i * w * 0.065
        d.line([x, cy - h * 0.15, x, cy + h * 0.15], fill=ERASE, width=lw)


def arch_text(img, text, f, cx, apex_y, radius, ink, tracking=0.0):
    """Upward-arched text; apex_y = top of the middle letter."""
    # total advance along the arc
    advances = []
    total = 0.0
    for ch in text:
        w = f.getlength(ch) + tracking * f.size
        advances.append(w)
        total += w
    total -= tracking * f.size  # no trailing tracking
    span = total / radius  # radians
    # walk letters from left (-span/2) to right (+span/2)
    a = -span / 2
    cy_center = apex_y + radius
    for ch, adv in zip(text, advances):
        mid = a + (adv / radius) / 2  # angle of this letter's center
        # glyph tile
        gw = int(f.getlength(ch)) + 8
        gh = int(f.size * 1.5) + 8
        tile = Image.new("RGBA", (gw, gh), (0, 0, 0, 0))
        td = ImageDraw.Draw(tile)
        td.text((gw / 2, gh / 2), ch, font=f, fill=ink, anchor="mm")
        tile = tile.rotate(-math.degrees(mid), resample=Image.BICUBIC, expand=True)
        # position: glyph center on the circle
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


# ---------------------------------------------------------------- 1. HAT TRICK CLUB
# front: small chest hit, text + three stars
img = new_canvas(3000, 1200)
d = ImageDraw.Draw(img)
f, _ = fit_font(ANTON, "HAT TRICK CLUB", 1900, 320)
draw_tracked(d, 1500, 330, "HAT TRICK CLUB", f, WHITE, tracking=0.04)
for i, sx in enumerate((1500 - 260, 1500, 1500 + 260)):
    star(d, sx, 830, 72, 30, WHITE)
save(img, "hat-trick-club-front.png")

# back: large arch + three pucks
img = new_canvas(2400, 3000)
f, _ = fit_font(ANTON, "HAT TRICK CLUB", 2200, 340)
arch_text(img, "HAT TRICK CLUB", f, 1200, 560, 1400, WHITE, tracking=0.03)
for px in (1200 - 430, 1200, 1200 + 430):
    puck(img, px, 1540, 320, 200, WHITE)
save(img, "hat-trick-club-back.png")

# ---------------------------------------------------------------- 2. TOP SHELF (hat, front only)
img = new_canvas(3000, 1200)
puck(img, 1500, 310, 300, 200, WHITE)
d = ImageDraw.Draw(img)
f, _ = fit_font(GRADUATE, "TOP SHELF", 2500, 360)
draw_tracked(d, 1500, 560, "TOP SHELF", f, WHITE, tracking=0.02)
save(img, "top-shelf-hat-front.png")

# ---------------------------------------------------------------- 3. ANY GIVEN SUNDAY
# front: small chest text + football
img = new_canvas(3000, 1200)
d = ImageDraw.Draw(img)
f, _ = fit_font(ANTON, "ANY GIVEN SUNDAY", 1900, 300)
draw_tracked(d, 1500, 330, "ANY GIVEN SUNDAY", f, WHITE, tracking=0.04)
football(img, 1500, 830, 420, 250, WHITE)
save(img, "any-given-sunday-front.png")

# back: large arch + football underneath
img = new_canvas(2400, 3000)
f, _ = fit_font(ANTON, "ANY GIVEN SUNDAY", 2200, 310)
arch_text(img, "ANY GIVEN SUNDAY", f, 1200, 560, 1450, WHITE, tracking=0.03)
football(img, 1200, 1560, 460, 275, WHITE)
save(img, "any-given-sunday-back.png")

# ---------------------------------------------------------------- 4. SCORIGAMI CLUB (volt)
# front: small chest text only
img = new_canvas(3000, 1200)
d = ImageDraw.Draw(img)
f, _ = fit_font(ANTON, "SCORIGAMI CLUB", 1900, 320)
draw_tracked(d, 1500, 420, "SCORIGAMI CLUB", f, VOLT, tracking=0.04)
save(img, "scorigami-club-front.png")

# back: big straight SCORIGAMI + rule + "46-40 · FIRST EVER"
img = new_canvas(2400, 3000)
d = ImageDraw.Draw(img)
f, _ = fit_font(ANTON, "SCORIGAMI", 2100, 470)
draw_tracked(d, 1200, 880, "SCORIGAMI", f, VOLT, tracking=0.03)
f2, _ = fit_font(ANTON, "46-40  FIRST EVER", 1500, 170)
# subline with a hand-drawn dot separator (Anton may lack U+00B7)
left, right = "46-40", "FIRST EVER"
lw, rw = f2.getlength(left), f2.getlength(right)
gap = 120
total = lw + gap + rw
x0 = 1200 - total / 2
d.text((x0, 1560), left, font=f2, fill=VOLT)
d.text((x0 + lw + gap, 1560), right, font=f2, fill=VOLT)
dot_cx = x0 + lw + gap / 2
d.ellipse([dot_cx - 16, 1560 + f2.size * 0.42, dot_cx + 16, 1560 + f2.size * 0.42 + 32], fill=VOLT)
save(img, "scorigami-club-back.png")

print("done")
