#!/usr/bin/env python3
"""TSL shop apparel v3 — REAL ILLUSTRATED ARTWORK.
Matt rejected v1 (PIL clip-art shapes = corny) and v2 (bare arched text =
basic). His steer (Nov 18, 00:34): the reference is the Spittin' Chiclets
HATS — so the TSL snapback is the LEAD piece, '47 HITCH style, bold
embroidered-style TSL mark. Mascot hoodie DROPPED from this batch.
V3 = image-model illustrated art (crest) + type composited in PIL.
No copied Barstool marks (no skull, no skull-and-wings, no gloves crest),
no team/league marks, no player names, no scores/numbers.
"""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.expanduser("~/workspace/statline-blog/assets/shop")
FONTS = os.path.expanduser("~/workspace/tools/fonts")
ANTON = os.path.join(FONTS, "Anton-Regular.ttf")
GRADUATE = os.path.join(FONTS, "Graduate-Regular.ttf")

CREST_ART = os.path.join(
    OUT, "media-generation-tsl-hockey-crest-art-v3-0-2f7fe393-090f-4f53-9f52-d6edbe687918.png")
# Wolverine mascot art generated for v3 but PARKED per Matt's steer
# (media-generation-tsl-wolverine-mascot-art-v3-0-8661778e-...png).

WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)
VOLT = (200, 255, 46, 255)


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


def ink_from_lum(img, ink_rgb):
    """White-on-black art -> ink-colored art on transparent (luminance = alpha)."""
    lum = np.array(img.convert("L")).astype(np.float32)
    alpha = np.clip((lum - 25.0) * 255.0 / 230.0, 0, 255).astype(np.uint8)
    out = np.zeros((img.height, img.width, 4), dtype=np.uint8)
    out[..., 0], out[..., 1], out[..., 2] = ink_rgb
    out[..., 3] = alpha
    return Image.fromarray(out, "RGBA")


def crop_content(img, margin=20, thresh=12):
    a = np.array(img)
    ys, xs = np.where(a[..., 3] > thresh)
    if len(xs) == 0:
        return img
    x0, x1 = max(0, xs.min() - margin), min(img.width, xs.max() + margin)
    y0, y1 = max(0, ys.min() - margin), min(img.height, ys.max() + margin)
    return img.crop((x0, y0, x1, y1))


def distress(img, amount=0.05, seed=7):
    """Speckle-erode alpha so PIL type gets the same worn vintage feel."""
    rng = np.random.default_rng(seed)
    a = np.array(img).copy()
    alpha = a[..., 3].astype(np.float32)
    mask = (rng.random(alpha.shape) < amount) & (alpha > 120)
    a[..., 3] = np.where(mask, (alpha * 0.3).astype(np.uint8), a[..., 3]).astype(np.uint8)
    return Image.fromarray(a, "RGBA")


def save(img, name):
    path = os.path.join(OUT, name)
    img.save(path, dpi=(300, 300))
    print(f"saved {name}  {img.size}")
    return path


def new_canvas(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


def bolt(d, cx, cy, w, h, ink):
    """Simple lightning bolt polygon (brand accent, not a sports object)."""
    pts = [
        (cx + 0.12 * w, cy - 0.5 * h),
        (cx - 0.42 * w, cy + 0.12 * h),
        (cx - 0.08 * w, cy + 0.12 * h),
        (cx - 0.15 * w, cy + 0.5 * h),
        (cx + 0.42 * w, cy - 0.12 * h),
        (cx + 0.08 * w, cy - 0.12 * h),
    ]
    d.polygon(pts, fill=ink)


# ---------------------------------------------------------------- load crest art
crest_rgb = Image.open(CREST_ART).convert("RGB")  # 1600x1600
crest = ink_from_lum(crest_rgb, (255, 255, 255))
crest = crop_content(crest, margin=10)
print("crest cropped:", crest.size)

# ---------------------------------------------------------------- 1. HAT PATCH (lead piece)
# Shield-ONLY art (no sticks, no banner) — hollow center, so "TSL" is drawn
# in the same NAVY ink inside the outline. Two-tone '47 HITCH format:
# CREAM crown + NAVY brim, patch in NAVY.
SHIELD_ART = os.path.join(
    OUT, "media-generation-tsl-shield-mark-art-v3-0-2bb538cb-5ef1-4625-8a18-8a892d4d60f0.png")
NAVY = (23, 36, 66)
CREAM = (242, 234, 216)
shield_rgb = Image.open(SHIELD_ART).convert("RGB")  # 1600x1600
shield = ink_from_lum(shield_rgb, NAVY)
shield = crop_content(shield, margin=10)
print("shield cropped:", shield.size)
# "TSL" in NAVY, centered in the shield's hollow panel (~0.50, 0.50).
patch = new_canvas(2400, 2400)
sw = 1900
sh = int(sw * shield.height / shield.width)
shield_big = shield.resize((sw, sh), Image.LANCZOS)
px, py = (2400 - sw) // 2, (2400 - sh) // 2
patch.alpha_composite(shield_big, (px, py))
d = ImageDraw.Draw(patch)
f, _ = fit_font(ANTON, "TSL", 820, 420, tracking=0.02)
tw = text_w(f, "TSL", 0.02)
d.text((1200 - tw / 2, 1200 - f.size / 2 - 10), "TSL", font=f, fill=NAVY + (255,))
save(patch, "tsl-hat-patch-v3.png")

# ---------------------------------------------------------------- 2. CREST HOODIE
# FRONT: small crest chest hit, 3000x1200 — with the TSL knockout in the
# shield, matching the back and the hat patch.
front = new_canvas(3000, 1200)
fw = 780
fh = int(fw * crest.height / crest.width)
front.alpha_composite(crest.resize((fw, fh), Image.LANCZOS),
                      ((3000 - fw) // 2, (1200 - fh) // 2))
d = ImageDraw.Draw(front)
tcx = 1500
tcy = (1200 - fh) // 2 + int(0.44 * fh)
f, _ = fit_font(ANTON, "TSL", 380, 200, tracking=0.02)
tw = text_w(f, "TSL", 0.02)
d.text((tcx - tw / 2, tcy - f.size / 2 - 4), "TSL", font=f, fill=(0, 0, 0, 255))
save(front, "tsl-hockey-club-front-v3.png")

# BACK: 2400x3000. "THE STAT LINE" arched above, huge crest, "TSL" knockout
# in the shield, "HOCKEY CLUB" knockout on the ribbon banner.
back = new_canvas(2400, 3000)
layer = new_canvas(2400, 3000)
f, _ = fit_font(ANTON, "THE STAT LINE", 2100, 300, tracking=0.03)
arch_text(layer, "THE STAT LINE", f, 1200, 330, 1500, WHITE, tracking=0.03)
back.alpha_composite(distress(layer, amount=0.045, seed=11))

cw = 1750
ch = int(cw * crest.height / crest.width)
cx0, cy0 = (2400 - cw) // 2, 620
crest_big = crest.resize((cw, ch), Image.LANCZOS)
back.alpha_composite(crest_big, (cx0, cy0))
# "TSL" black knockout in the shield center panel (~0.50, 0.44 of the art).
d = ImageDraw.Draw(back)
tcx = cx0 + int(0.50 * cw)
tcy = cy0 + int(0.44 * ch)
f, _ = fit_font(ANTON, "TSL", 700, 340, tracking=0.02)
tw = text_w(f, "TSL", 0.02)
d.text((tcx - tw / 2, tcy - f.size / 2 - 10), "TSL", font=f, fill=(0, 0, 0, 255))
# "HOCKEY CLUB" black knockout on the ribbon. Ribbon center is ~0.90 of
# the CROPPED crest height (fractions are of the cropped art, not the 1600px source).
rcx = cx0 + int(0.50 * cw)
rcy = cy0 + int(0.90 * ch)
f, _ = fit_font(ANTON, "HOCKEY CLUB", 580, 120, tracking=0.02)
tw = text_w(f, "HOCKEY CLUB", 0.02)
d.text((rcx - tw / 2, rcy - f.size / 2 - 4), "HOCKEY CLUB", font=f, fill=(0, 0, 0, 255))
save(back, "tsl-hockey-club-back-v3.png")

# ---------------------------------------------------------------- 3. CHANT HOODIE
# "FIRST. FAST. VERIFIED." — three arched lines, white, distressed.
# FRONT: small TSL badge chest hit, 3000x1200.
front = new_canvas(3000, 1200)
d = ImageDraw.Draw(front)
d.ellipse((1500 - 310, 600 - 310, 1500 + 310, 600 + 310), outline=WHITE, width=12)
f, _ = fit_font(ANTON, "TSL", 420, 300, tracking=0.02)
tw = text_w(f, "TSL", 0.02)
d.text((1500 - tw / 2, 600 - f.size / 2 - 8), "TSL", font=f, fill=WHITE)
save(front, "first-fast-verified-front-v3.png")

back = new_canvas(2400, 3000)
layer = new_canvas(2400, 3000)
lines = [("FIRST.", 700), ("FAST.", 1250), ("VERIFIED.", 1800)]
for text, apex in lines:
    f, _ = fit_font(ANTON, text, 2000, 420, tracking=0.03)
    arch_text(layer, text, f, 1200, apex, 2200, WHITE, tracking=0.03)
back.alpha_composite(distress(layer, amount=0.05, seed=23))
d = ImageDraw.Draw(back)
bolt(d, 1200, 2450, 200, 260, VOLT)
save(back, "first-fast-verified-back-v3.png")

print("done")
