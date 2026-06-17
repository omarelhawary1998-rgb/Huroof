#!/usr/bin/env python3
"""Generate Huroof print files, web previews, and Pinterest pins.

Arabic is typeset from real fonts (Amiri / Noto Naskh) via proper reshaping,
so letterforms and ligatures are correct by construction — never AI-rendered.

Outputs per design:
  print-files/NN-slug-A2-300dpi.png  (4961x7016, the sellable file — NOT committed)
  previews/NN-slug.jpg               (900px web preview)
  pins/NN-slug-pin.png               (1000x1500 Pinterest pin)
"""
import math, os, sys
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, features

assert features.check("raqm"), "Pillow must have Raqm for correct Arabic shaping"
AR = {"direction": "rtl", "language": "ar"}  # native HarfBuzz shaping

FONT_DIR = "/tmp/fonts"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/huroof_products"
W, H = 4961, 7016  # A2 @ 300dpi
GOLD, GOLD_LT, CREAM = "#C8A664", "#E2C98A", "#F2EDE4"

def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

def ar(text):
    return text  # raw Unicode; Raqm shapes it correctly at draw time

def hex2rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def vgrad(w, h, c1, c2, c3=None):
    """Vertical 2- or 3-stop gradient as an RGB image."""
    stops = [hex2rgb(c1)] + ([hex2rgb(c3)] if c3 else []) + [hex2rgb(c2)]
    t = np.linspace(0, 1, h)[:, None]
    if len(stops) == 2:
        col = (1 - t) * np.array(stops[0]) + t * np.array(stops[1])
    else:
        a, b, c = (np.array(s, float) for s in stops)
        col = np.where(t < .5, (1 - t * 2) * a + t * 2 * b, (1 - (t - .5) * 2) * b + (t - .5) * 2 * c)
    return Image.fromarray(np.repeat(col[:, None, :], w, axis=1).astype(np.uint8), "RGB")

def glow(img, cx, cy, r, color, alpha=90):
    """Soft radial glow (blurred disc — no banding, no hard edge)."""
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    rr = r * 0.55
    d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=hex2rgb(color) + (alpha,))
    ov = ov.filter(ImageFilter.GaussianBlur(r / 2.2))
    img.alpha_composite(ov)

def rings(img, cx, cy, color, alpha=26, n=9, step=None, width=3):
    """Faint concentric rings + 8 spokes — the Huroof background motif."""
    step = step or W * 0.055
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    c = hex2rgb(color) + (alpha,)
    for i in range(1, n + 1):
        r = step * i
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=width)
    R = step * n
    for k in range(8):
        a = k * math.pi / 4
        d.line([cx, cy, cx + R * math.cos(a), cy + R * math.sin(a)], fill=c, width=width)
    img.alpha_composite(ov)

def center_text(d, xy, text, fnt, fill, anchor="mm", rtl=False):
    d.text(xy, text, font=fnt, fill=fill, anchor=anchor, **(AR if rtl else {}))

def colophon(img, fg=GOLD):
    d = ImageDraw.Draw(img)
    f1 = font("CormorantGaramond[wght].ttf", 95)
    f2 = font("Amiri-Regular.ttf", 95)
    d.text((W / 2 - 110, H - 290), "Huroof", font=f1, fill=fg, anchor="mm")
    d.text((W / 2 + 160, H - 300), "حروف", font=f2, fill=fg, anchor="mm", **AR)

def star_outline(d, cx, cy, r, color, width, rot=0.0):
    pts = star8_path(cx, cy, r, rot)
    d.line(pts + [pts[0], pts[1]], fill=color, width=width, joint="curve")

def star8_path(cx, cy, r, rot=0.0):
    """Classic 8-point star (two rotated squares) as a polygon point list."""
    pts = []
    for k in range(16):
        rr = r if k % 2 == 0 else r * 0.55
        a = rot + k * math.pi / 8
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts

# ---------------------------------------------------------------- designs ---
def d_bismillah():
    img = vgrad(W, H, "#0D0F2A", "#1C1F40").convert("RGBA")
    rings(img, W / 2, H * 0.42, GOLD)
    glow(img, W / 2, H * 0.42, W * 0.42, GOLD, 70)
    d = ImageDraw.Draw(img)
    fA = font("Amiri-Bold.ttf", 620)
    center_text(d, (W / 2, H * 0.33), ar("بِسْمِ اللَّهِ"), fA, GOLD_LT, rtl=True)
    center_text(d, (W / 2, H * 0.50), ar("الرَّحْمَٰنِ الرَّحِيمِ"), fA, GOLD, rtl=True)
    fE = font("CormorantGaramond[wght].ttf", 150)
    center_text(d, (W / 2, H * 0.66), "In the name of God,", fE, CREAM)
    center_text(d, (W / 2, H * 0.695), "the Most Gracious, the Most Merciful", fE, CREAM)
    colophon(img)
    return img

def d_star8():
    img = vgrad(W, H, "#0A1628", "#1C3050").convert("RGBA")
    d = ImageDraw.Draw(img, "RGBA")
    teal, gold = hex2rgb("#4ECDC4"), hex2rgb(GOLD)
    cell = W / 4
    for row in range(-1, 8):
        for col in range(-1, 5):
            cx, cy = col * cell + cell / 2 + (cell / 2 if row % 2 else 0), row * cell + cell / 2 + H * 0.04
            main = (row + col) % 2 == 0
            c = (teal if main else gold)
            star_outline(d, cx, cy, cell * 0.46, c + (235,), 14)
            star_outline(d, cx, cy, cell * 0.30, c + (140,), 8, rot=math.pi / 8)
            d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=gold + (200,))
    # vignette band for title
    band = Image.new("RGBA", (W, int(H * 0.16)), (10, 22, 40, 215))
    img.alpha_composite(band, (0, int(H * 0.84)))
    center_text(d, (W / 2, H * 0.895), ar("نَجْمَةٌ ثَمَانِيَّةُ الرُّؤُوس"), font("Amiri-Bold.ttf", 230), GOLD_LT, rtl=True)
    center_text(d, (W / 2, H * 0.945), "THE EIGHT-POINT STAR", font("Inter[opsz,wght].ttf", 110), "#9FE8E2")
    return img

def d_sabr():
    img = vgrad(W, H, "#1A0A0A", "#3A1A1A").convert("RGBA")
    rings(img, W / 2, H * 0.44, "#E8927C")
    glow(img, W / 2, H * 0.44, W * 0.40, "#E8927C", 60)
    d = ImageDraw.Draw(img)
    center_text(d, (W / 2, H * 0.42), ar("الصَّبْرُ جَمِيلٌ"), font("Amiri-Bold.ttf", 800), GOLD_LT, rtl=True)
    center_text(d, (W / 2, H * 0.60), "Patience is beautiful", font("CormorantGaramond[wght].ttf", 190), "#E8927C")
    colophon(img)
    return img

def d_lantern():
    img = vgrad(W, H, "#1A1040", "#2A1870").convert("RGBA")
    d = ImageDraw.Draw(img, "RGBA")
    rng = np.random.default_rng(7)
    for _ in range(220):  # starfield
        x, y, r = rng.uniform(0, W), rng.uniform(0, H * .75), rng.uniform(2, 9)
        d.ellipse([x - r, y - r, x + r, y + r], fill=hex2rgb(GOLD_LT) + (rng.integers(60, 200),))
    # crescent — punched out on its own layer so the sky shows through
    cx, cy, R = W * 0.74, H * 0.16, W * 0.085
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.ellipse([cx - R, cy - R, cx + R, cy + R], fill=hex2rgb(GOLD) + (255,))
    hole = Image.new("L", img.size, 0)
    ImageDraw.Draw(hole).ellipse([cx - R * .55, cy - R * 1.05, cx + R * 1.25, cy + R * .75], fill=255)
    layer.putalpha(ImageChops.subtract(layer.getchannel("A"), hole))
    img.alpha_composite(layer)
    # lantern
    lx, ly = W / 2, H * 0.40
    bw, bh = W * 0.20, H * 0.26
    gold, teal = hex2rgb(GOLD), hex2rgb("#4ECDC4")
    d.line([lx, H * 0.06, lx, ly - bh * .62], fill=gold + (255,), width=22)
    d.ellipse([lx - 55, ly - bh * .68, lx + 55, ly - bh * .55], outline=gold + (255,), width=20)
    d.polygon([(lx - bw * .42, ly - bh * .42), (lx + bw * .42, ly - bh * .42), (lx + bw * .26, ly - bh * .56), (lx - bw * .26, ly - bh * .56)], fill=gold + (255,))
    d.rounded_rectangle([lx - bw * .5, ly - bh * .42, lx + bw * .5, ly + bh * .42], 60, outline=gold + (255,), width=26)
    for fx in (-.25, 0, .25):  # glass panes
        d.rounded_rectangle([lx + bw * fx - bw * .09, ly - bh * .34, lx + bw * fx + bw * .09, ly + bh * .34], 40,
                            fill=teal + (95,), outline=gold + (255,), width=12)
    d.polygon([(lx - bw * .34, ly + bh * .42), (lx + bw * .34, ly + bh * .42), (lx + bw * .2, ly + bh * .54), (lx - bw * .2, ly + bh * .54)], fill=gold + (255,))
    d.ellipse([lx - 40, ly + bh * .54, lx + 40, ly + bh * .64], fill=gold + (255,))
    glow(img, lx, ly, W * 0.30, "#4ECDC4", 55)
    d = ImageDraw.Draw(img)
    center_text(d, (W / 2, H * 0.80), ar("رَمَضَانُ كَرِيمٌ"), font("Amiri-Bold.ttf", 640), "#4ECDC4", rtl=True)
    center_text(d, (W / 2, H * 0.90), "RAMADAN KAREEM", font("Inter[opsz,wght].ttf", 130), GOLD_LT)
    return img

def d_arabesque():
    img = vgrad(W, H, "#2A1A0A", "#1A0A00").convert("RGBA")
    d = ImageDraw.Draw(img, "RGBA")
    gold = hex2rgb(GOLD)
    cell = W / 5
    for row in range(-1, 9):
        for col in range(-1, 6):
            cx, cy = col * cell + (cell / 2 if row % 2 else 0), row * cell * 0.9
            for rr, alpha, wd in ((0.50, 200, 12), (0.36, 130, 9), (0.22, 90, 7)):
                star_outline(d, cx, cy, cell * rr, gold + (alpha,), wd, rot=(math.pi / 8 if rr == 0.36 else 0))
            for k in range(8):
                a = k * math.pi / 4 + math.pi / 8
                x2, y2 = cx + cell * .62 * math.cos(a), cy + cell * .62 * math.sin(a)
                d.ellipse([x2 - 16, y2 - 16, x2 + 16, y2 + 16], fill=gold + (160,))
    band = Image.new("RGBA", (W, int(H * 0.15)), (26, 10, 0, 220))
    img.alpha_composite(band, (0, int(H * 0.85)))
    d = ImageDraw.Draw(img)
    center_text(d, (W / 2, H * 0.90), ar("أَرَابِيسْك الأَنْدَلُس"), font("Amiri-Bold.ttf", 230), GOLD_LT, rtl=True)
    center_text(d, (W / 2, H * 0.95), "AL-ANDALUS ARABESQUE", font("Inter[opsz,wght].ttf", 105), CREAM)
    return img

def d_dunes():
    img = vgrad(W, H, "#2A1505", "#E8C87A", "#C8943A").convert("RGBA")
    d = ImageDraw.Draw(img, "RGBA")
    sun_y = H * 0.40
    glow(img, W / 2, sun_y, W * 0.30, "#F5E8D0", 120)
    d.ellipse([W / 2 - 330, sun_y - 330, W / 2 + 330, sun_y + 330], fill=hex2rgb("#F5E8D0") + (255,))
    layers = [("#C8943A", 0.52, 240), ("#A06A28", 0.62, 255), ("#6B4318", 0.74, 255), ("#3A2010", 0.86, 255), ("#1A0E06", 0.97, 255)]
    for i, (c, base, alpha) in enumerate(layers):
        pts = [(0, H)]
        for x in range(0, W + 80, 80):
            y = H * base + math.sin(x / W * math.pi * (1.6 + i * .7) + i * 2.1) * H * 0.045
            pts.append((x, y))
        pts.append((W, H))
        d.polygon(pts, fill=hex2rgb(c) + (alpha,))
    center_text(d, (W / 2, H * 0.10), ar("كُثْبَانُ الصَّحْرَاء"), font("Amiri-Bold.ttf", 330), "#F5E8D0", rtl=True)
    center_text(d, (W / 2, H * 0.165), "DESERT DUNES AT DUSK", font("Inter[opsz,wght].ttf", 115), "#E8C87A")
    return img

def d_yaallah():
    img = vgrad(W, H, "#080810", "#1A1A2E").convert("RGBA")
    rings(img, W / 2, H * 0.45, GOLD, alpha=30, n=11)
    glow(img, W / 2, H * 0.45, W * 0.45, GOLD, 75)
    d = ImageDraw.Draw(img)
    center_text(d, (W / 2, H * 0.43), ar("يَا اللَّه"), font("Amiri-Bold.ttf", 1250), GOLD, rtl=True)
    center_text(d, (W / 2, H * 0.64), "Ya Allah — O God", font("CormorantGaramond[wght].ttf", 170), "#8A8AC0")
    colophon(img)
    return img

def d_pass():
    img = vgrad(W, H, "#0A1A2A", "#051018").convert("RGBA")
    rings(img, W / 2, H * 0.44, "#4ECDC4", alpha=24)
    glow(img, W / 2, H * 0.44, W * 0.38, "#4ECDC4", 50)
    d = ImageDraw.Draw(img)
    center_text(d, (W / 2, H * 0.41), ar("هَذَا أَيْضًا سَيَمْضِي"), font("Amiri-Bold.ttf", 560), "#9FE8E2", rtl=True)
    center_text(d, (W / 2, H * 0.58), "This too shall pass", font("CormorantGaramond[wght].ttf", 195), GOLD_LT)
    colophon(img, fg="#4ECDC4")
    return img

DESIGNS = [
    ("01-bismillah", d_bismillah), ("02-eight-point-star", d_star8),
    ("03-sabr-patience", d_sabr), ("04-ramadan-lantern", d_lantern),
    ("05-andalus-arabesque", d_arabesque), ("06-desert-dunes", d_dunes),
    ("07-ya-allah", d_yaallah), ("08-this-too-shall-pass", d_pass),
]

def make_pin(art, slug):
    pin = Image.new("RGB", (1000, 1500), "#08090F")
    a = art.convert("RGB").resize((1000, 1414))
    pin.paste(a, (0, 0))
    d = ImageDraw.Draw(pin)
    d.rectangle([0, 1414, 1000, 1500], fill="#08090F")
    d.text((500, 1442), "Huroof حروف — Arabic Art", font=font("CormorantGaramond[wght].ttf", 44), fill=GOLD, anchor="mm")
    d.text((500, 1483), "Digital download & prints · huroof on Etsy", font=font("Inter[opsz,wght].ttf", 26), fill="#9aa", anchor="mm")
    return pin

if __name__ == "__main__":
    for sub in ("print-files", "previews", "pins"):
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    only = sys.argv[2].split(",") if len(sys.argv) > 2 else None
    for slug, fn in DESIGNS:
        if only and not any(o in slug for o in only):
            continue
        art = fn()
        art.convert("RGB").save(f"{OUT}/print-files/{slug}-A2-300dpi.png", optimize=True)
        prev = art.convert("RGB").resize((900, 1273))
        prev.save(f"{OUT}/previews/{slug}.jpg", quality=88)
        make_pin(art, slug).save(f"{OUT}/pins/{slug}-pin.png", optimize=True)
        print("done", slug)
