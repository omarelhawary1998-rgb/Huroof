#!/usr/bin/env python3
"""Manuscript style — gold ink on parchment, classical Amiri calligraphy.

Renders fully-vocalized Arabic phrases as a traditional Islamic-manuscript
art piece: aged parchment ground, gold-gradient ink, ornamental gold border.
Letterforms come from the real Amiri typeface (HarfBuzz-shaped) so the script
is always correct — never AI-rendered.

    python3 tools/generate_manuscript.py [OUT_DIR] [SKU-substring-filter]
"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, features

assert features.check("raqm"), "Pillow needs Raqm for correct Arabic shaping"
AR = {"direction": "rtl", "language": "ar"}
FONT_DIR = "/tmp/fonts"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/huroof_manuscript"

def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

# (slug, arabic[diacritized], english) — 8 core + 30 batch-1
PHRASES = [
    ("01-bismillah", "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ", "In the Name of God, the Most Gracious, the Most Merciful"),
    ("03-sabr-patience", "الصَّبْرُ جَمِيلٌ", "Patience Is Beautiful"),
    ("04-ramadan-lantern", "رَمَضَانُ كَرِيمٌ", "Ramadan Kareem"),
    ("07-ya-allah", "يَا اللَّه", "Ya Allah"),
    ("08-this-too-shall-pass", "هَذَا أَيْضًا سَيَمْضِي", "This Too Shall Pass"),
    ("RL-FAM-001", "أُمِّي حُبِّي الأَوَّل", "My First Love"),
    ("RL-FAM-005", "العَائِلَةُ أَوَّلاً", "Family First"),
    ("RL-DIA-001", "قَلْبِي عَرَبِي", "Arab Heart, Global Journey"),
    ("RL-UAE-003", "الإِمَارَاتُ بَيْتُنَا", "UAE Is Our Home"),
    ("RL-CHI-005", "قَمَر", "Moon · Qamar"),
]

PARCH_TOP, PARCH_BOT = (242, 232, 206), (228, 212, 172)
GOLD_HI, GOLD_LO = (232, 201, 138), (150, 110, 44)
INK_SHADOW = (120, 92, 40)

def parchment(w, h):
    """Warm aged-paper ground: gradient + fibre noise + stains + vignette."""
    t = np.linspace(0, 1, h)[:, None, None]
    base = (1 - t) * np.array(PARCH_TOP) + t * np.array(PARCH_BOT)
    img = np.repeat(base, w, axis=1)
    # fine fibre noise
    rng = np.random.default_rng(7)
    noise = rng.normal(0, 6.0, (h, w, 1))
    img = img + noise
    # a few soft warm stains for age
    yy, xx = np.mgrid[0:h, 0:w]
    for cx, cy, r, a in [(0.18*w,0.22*h,0.22*w,-10),(0.82*w,0.7*h,0.28*w,-12),(0.5*w,0.5*h,0.5*w,6)]:
        d = np.sqrt((xx-cx)**2 + (yy-cy)**2) / r
        img += (a * np.clip(1-d, 0, 1)**2)[..., None]
    # vignette (darken edges)
    d = np.sqrt((xx-w/2)**2 + (yy-h/2)**2) / (0.72*math.hypot(w/2, h/2))
    img -= (np.clip(d-0.6, 0, 1)*38)[..., None]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")

def gold_text(size, text, fnt):
    """Return an RGBA layer of `text` filled with a vertical gold gradient."""
    w, h = size
    # measure
    tmp = ImageDraw.Draw(Image.new("L", (1, 1)))
    bbox = tmp.textbbox((0, 0), text, font=fnt, anchor="lt", **AR)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    mask = Image.new("L", (tw+40, th+60), 0)
    md = ImageDraw.Draw(mask)
    md.text((20-bbox[0], 30-bbox[1]), text, font=fnt, fill=255, anchor="lt", **AR)
    # gold gradient plate
    mh = mask.height
    tg = np.linspace(0, 1, mh)[:, None, None]
    grad = (1-tg)*np.array(GOLD_HI) + tg*np.array(GOLD_LO)
    grad = np.repeat(grad, mask.width, axis=1).astype(np.uint8)
    layer = Image.new("RGBA", mask.size, (0, 0, 0, 0))
    layer.paste(Image.fromarray(grad, "RGB"), (0, 0), mask)
    return layer, mask

def border(draw, w, h):
    g = (176, 132, 56)
    for inset, wd in [(int(w*0.045), 5), (int(w*0.060), 2)]:
        draw.rectangle([inset, inset, w-inset, h-inset], outline=g, width=wd)
    # corner 8-point diamonds
    m = int(w*0.045)
    for cx, cy in [(m, m), (w-m, m), (m, h-m), (w-m, h-m)]:
        r = int(w*0.014)
        draw.polygon([(cx, cy-r), (cx+r, cy), (cx, cy+r), (cx-r, cy)], fill=g)

def fit(text, fname, max_w, start):
    f = font(fname, start)
    d = ImageDraw.Draw(Image.new("L", (1, 1)))
    tw = d.textlength(text, font=f, **AR)
    if tw > max_w:
        f = font(fname, max(60, int(start*max_w/tw)))
    return f

def render(slug, arabic, english, W=1000, H=1414):
    img = parchment(W, H)
    d = ImageDraw.Draw(img)
    border(d, W, H)
    # main Arabic line(s)
    one_line = len(arabic) <= 20
    big = int(W*0.16) if one_line else int(W*0.115)
    fA = fit(arabic, "Amiri-Bold.ttf", W*0.74, big)
    layer, mask = gold_text((W, H), arabic, fA)
    lx = (W-layer.width)//2
    ly = int(H*0.40) - layer.height//2
    # soft ink shadow for depth
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.bitmap((lx+3, ly+4), mask, fill=INK_SHADOW+(90,))
    sh = sh.filter(ImageFilter.GaussianBlur(2))
    img.paste(sh, (0, 0), sh)
    img.paste(layer, (lx, ly), layer)
    # divider ornament
    cy = int(H*0.58)
    d.line([(W*0.34, cy), (W*0.46, cy)], fill=(176,132,56), width=2)
    d.line([(W*0.54, cy), (W*0.66, cy)], fill=(176,132,56), width=2)
    r = int(W*0.012)
    d.polygon([(W/2, cy-r), (W/2+r, cy), (W/2, cy+r), (W/2-r, cy)], fill=(176,132,56))
    # English caption
    fE = fit_latin(english, W*0.7, int(W*0.040))
    d.text((W/2, int(H*0.66)), english, font=fE, fill=(120, 92, 40), anchor="ma")
    # colophon
    d.text((W/2, H-int(H*0.055)), "Huroof · حروف", font=font("Amiri-Regular.ttf", int(W*0.028)),
           fill=(150, 110, 44), anchor="mm", **AR)
    return img

def fit_latin(text, max_w, start):
    f = font("CormorantGaramond[wght].ttf", start)
    d = ImageDraw.Draw(Image.new("L", (1, 1)))
    if d.textlength(text, font=f) > max_w:
        f = font("CormorantGaramond[wght].ttf", max(20, int(start*max_w/d.textlength(text, font=f))))
    return f

if __name__ == "__main__":
    only = sys.argv[2] if len(sys.argv) > 2 else None
    os.makedirs(os.path.join(OUT, "previews"), exist_ok=True)
    for slug, a, e in PHRASES:
        if only and only not in slug:
            continue
        img = render(slug, a, e)
        img.convert("RGB").resize((900, 1273)).save(f"{OUT}/previews/{slug}.jpg", quality=90)
        print("done", slug)
