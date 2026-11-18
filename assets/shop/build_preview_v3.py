#!/usr/bin/env python3
"""Preview sheet v3 — hat leads, crest hoodie + chant hoodie below.
Hat mockup: two-tone '47 HITCH style — cream crown, navy brim, navy TSL
shield patch, small volt bolt side hit (the Chiclets side-hit format).
"""
import os
from PIL import Image, ImageDraw, ImageFont

SHOP = os.path.expanduser("~/workspace/statline-blog/assets/shop")
FONTS = os.path.expanduser("~/workspace/tools/fonts")
ANTON = os.path.join(FONTS, "Anton-Regular.ttf")
OUT = os.path.expanduser("~/workspace/your_files/tsl-new-apparel-preview-v3.png")

BG = (11, 14, 23)
PANEL = (23, 23, 31)
PANEL_LINE = (58, 58, 74)
WHITE = (255, 255, 255)
MUTED = (148, 152, 168)
VOLT = (200, 255, 46)
CREAM = (242, 234, 216)
NAVY = (23, 36, 66)

W, H = 2400, 3300
sheet = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(sheet)


def font(size):
    return ImageFont.truetype(ANTON, int(size))


def panel(x0, y0, x1, y1):
    d.rounded_rectangle((x0, y0, x1, y1), radius=28, fill=PANEL, outline=PANEL_LINE, width=3)


def fit_on_panel(img, max_w, max_h):
    w, h = img.size
    s = min(max_w / w, max_h / h)
    return img.resize((int(w * s), int(h * s)), Image.LANCZOS)


def bolt(dd, cx, cy, w, h, ink):
    pts = [
        (cx + 0.12 * w, cy - 0.5 * h),
        (cx - 0.42 * w, cy + 0.12 * h),
        (cx - 0.08 * w, cy + 0.12 * h),
        (cx - 0.15 * w, cy + 0.5 * h),
        (cx + 0.42 * w, cy - 0.12 * h),
        (cx + 0.08 * w, cy - 0.12 * h),
    ]
    dd.polygon(pts, fill=ink)


def load(name):
    return Image.open(os.path.join(SHOP, name)).convert("RGBA")


# ---------------------------------------------------------------- header
f = font(110)
t = "THE STAT LINE — NEW APPAREL · V3"
tw = d.textlength(t, font=f)
d.text(((W - tw) / 2, 55), t, font=f, fill=VOLT)
f2 = font(46)
t2 = "Hat leads · Real illustrated art · For approval — nothing listed yet"
tw2 = d.textlength(t2, font=f2)
d.text(((W - tw2) / 2, 185), t2, font=f2, fill=MUTED)

# ---------------------------------------------------------------- HAT panel (lead, full width)
panel(80, 260, 2320, 1240)
# Hat mockup: cream crown + navy brim, centered left.
hat = Image.new("RGBA", (1000, 820), (0, 0, 0, 0))
hd = ImageDraw.Draw(hat)
# crown: dome top + straight body so it meets the brim, cream
hd.ellipse((150, 40, 850, 420), fill=CREAM + (255,))
hd.rectangle((150, 220, 850, 640), fill=CREAM + (255,))
# crown panel seams
for sx in (330, 500, 670):
    hd.line((sx, 120, sx, 620), fill=(200, 190, 165, 255), width=5)
# brim: wide flat rounded bar, navy, overlapping the crown bottom
hd.rounded_rectangle((60, 620, 940, 710), radius=45, fill=NAVY + (255,))
# patch on the crown
patch = load("tsl-hat-patch-v3.png")
pw = 360
ph = int(pw * patch.height / patch.width)
patch_small = patch.resize((pw, ph), Image.LANCZOS)
hat.alpha_composite(patch_small, ((1000 - pw) // 2, 150))
# small volt bolt side hit on the crown
bolt(hd, 800, 480, 46, 64, VOLT)
sheet.paste(hat, (150, 330), hat)
# Hat labels, right side.
lx = 1300
f = font(84)
d.text((lx, 420), "TSL SNAPBACK", font=f, fill=WHITE)
f = font(52)
d.text((lx, 540), "'47 HITCH style · Two-tone", font=f, fill=MUTED)
d.text((lx, 610), "Cream crown / Navy brim", font=f, fill=MUTED)
d.text((lx, 680), "Embroidered TSL shield patch", font=f, fill=MUTED)
d.text((lx, 750), "Navy ink · Volt bolt side hit", font=f, fill=MUTED)
f = font(48)
d.text((lx + 46, 900), "LEAD PIECE", font=f, fill=VOLT)
# small volt star drawn (Anton has no ★ glyph)
_sx, _sy = lx + 20, 924
_star = []
import math as _math
for _i in range(10):
    _r = 22 if _i % 2 == 0 else 9
    _a = -_math.pi / 2 + _i * _math.pi / 5
    _star.append((_sx + _r * _math.cos(_a), _sy + _r * _math.sin(_a)))
d.polygon(_star, fill=VOLT)

# ---------------------------------------------------------------- hoodie panels
def hoodie_panel(x0, y0, x1, y1, back_name, front_name, title, sub):
    panel(x0, y0, x1, y1)
    back = load(back_name)
    # trim the back print's empty margins so it fills the panel
    bbox = back.getbbox()
    if bbox:
        m = 30
        back = back.crop((max(0, bbox[0] - m), max(0, bbox[1] - m),
                          min(back.width, bbox[2] + m), min(back.height, bbox[3] + m)))
    bw = (x1 - x0) - 160
    bh = 1500
    back_s = fit_on_panel(back, bw, bh)
    sheet.paste(back_s, (x0 + (x1 - x0 - back_s.width) // 2, y0 + 40), back_s)
    # front inset, bottom-left
    front = load(front_name)
    fw = 420
    fh = int(fw * front.height / front.width)
    front_s = front.resize((fw, fh), Image.LANCZOS)
    ix0, iy0 = x0 + 50, y1 - fh - 190
    d.rounded_rectangle((ix0 - 14, iy0 - 14, ix0 + fw + 14, iy0 + fh + 14),
                        radius=16, fill=(11, 14, 23), outline=PANEL_LINE, width=2)
    sheet.paste(front_s, (ix0, iy0), front_s)
    f = font(40)
    d.text((ix0 + 8, iy0 - 52), "FRONT", font=f, fill=VOLT)
    # label, bottom-right of panel
    f = font(64)
    d.text((x0 + 520, y1 - 210), title, font=f, fill=WHITE)
    f = font(44)
    d.text((x0 + 520, y1 - 130), sub, font=f, fill=MUTED)


hoodie_panel(80, 1290, 1180, 3150,
             "tsl-hockey-club-back-v3.png", "tsl-hockey-club-front-v3.png",
             "TSL HOCKEY CLUB", "Hoodie · White ink")
hoodie_panel(1220, 1290, 2320, 3150,
             "first-fast-verified-back-v3.png", "first-fast-verified-front-v3.png",
             "FIRST. FAST. VERIFIED.", "Hoodie · White + volt ink")

# ---------------------------------------------------------------- footer
f = font(40)
t = "Print files: transparent PNG, 3000px, 300 DPI — ready for Printful once approved."
tw = d.textlength(t, font=f)
d.text(((W - tw) / 2, 3200), t, font=f, fill=MUTED)

sheet.save(OUT, dpi=(300, 300))
print("saved", OUT, sheet.size)
