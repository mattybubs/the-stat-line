#!/usr/bin/env python3
"""Preview sheet for TSL apparel v2 — type only, all four designs."""
import os
from PIL import Image, ImageDraw, ImageFont

SHOP = os.path.expanduser("~/workspace/statline-blog/assets/shop")
FONTS = os.path.expanduser("~/workspace/tools/fonts")
ANTON = os.path.join(FONTS, "Anton-Regular.ttf")
DEJAVU = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DEJAVU_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

VOID = (11, 14, 23)
PANEL = (20, 22, 36)
BORDER = (58, 67, 88)
WHITE = (255, 255, 255)
VOLT = (200, 255, 46)
DIM = (139, 147, 167)

W, H = 2400, 2920
sheet = Image.new("RGB", (W, H), VOID)
d = ImageDraw.Draw(sheet)

anton = lambda s: ImageFont.truetype(ANTON, s)
sans = lambda s: ImageFont.truetype(DEJAVU, s)
sans_b = lambda s: ImageFont.truetype(DEJAVU_B, s)

t = "THE STAT LINE — NEW APPAREL · V2"
f = anton(96)
d.text((W // 2, 78), t, font=f, fill=VOLT, anchor="ma")
d.text((W // 2, 196), "Type only — no drawings, no scores, no numbers  ·  White + volt ink on dark  ·  For approval — nothing listed yet",
       font=sans(38), fill=DIM, anchor="ma")

DESIGNS = [
    ("HAT TRICK CLUB", "Hoodie · White ink", "hat-trick-club-back-v2.png", "hat-trick-club-front-v2.png"),
    ("TOP SHELF", "Dad hat · White ink", "top-shelf-hat-front-v2.png", None),
    ("ANY GIVEN SUNDAY", "Hoodie · White ink", "any-given-sunday-back-v2.png", "any-given-sunday-front-v2.png"),
    ("SCORIGAMI CLUB", "Hoodie · Volt ink", "scorigami-club-back-v2.png", "scorigami-club-front-v2.png"),
]

PW, PH, GAP = 1080, 1180, 40
X0, Y0 = 80, 300


def fit_into(img, bw, bh):
    s = min(bw / img.width, bh / img.height)
    return img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.LANCZOS), s


for i, (name, sub, hero, front) in enumerate(DESIGNS):
    px = X0 + (i % 2) * (PW + GAP)
    py = Y0 + (i // 2) * (PH + GAP)
    d.rounded_rectangle([px, py, px + PW, py + PH], radius=28, fill=PANEL,
                        outline=BORDER, width=2)
    him = Image.open(os.path.join(SHOP, hero)).convert("RGBA")
    him, _ = fit_into(him, 940, 760)
    sheet.paste(him, (px + (PW - him.width) // 2, py + 24), him)
    ly = py + 850
    if front:
        d.text((px + 36, ly - 6), "FRONT", font=sans_b(30), fill=VOLT)
        fim = Image.open(os.path.join(SHOP, front)).convert("RGBA")
        fim, _ = fit_into(fim, 280, 112)
        fx, fy = px + 36, py + PH - 150
        d.rounded_rectangle([fx - 6, fy - 6, fx + fim.width + 6, fy + fim.height + 6],
                            radius=10, outline=BORDER, width=2)
        sheet.paste(fim, (fx, fy), fim)
        tx = px + 360
        d.text((tx, ly), name, font=anton(56), fill=WHITE)
        d.text((tx, ly + 92), sub, font=sans(38), fill=DIM)
    else:
        d.text((px + PW // 2, ly), name, font=anton(56), fill=WHITE, anchor="ma")
        d.text((px + PW // 2, ly + 92), sub, font=sans(38), fill=DIM, anchor="ma")

d.text((W // 2, H - 90),
       "Print files: transparent PNG, 3000px, 300 DPI, one ink — ready for Printful once approved.",
       font=sans(32), fill=DIM, anchor="ma")

out = os.path.expanduser("~/workspace/your_files/tsl-new-apparel-preview-v2.png")
sheet.save(out, dpi=(300, 300))
print("saved", out, sheet.size)
