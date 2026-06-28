#!/usr/bin/env python3
"""Saudi Arabia poster — typeset tagline (verified Amiri pipeline) onto the
clean landscape source, then build every platform asset.

EN: GREATNESS HAS NO LIMITS   AR: العَظَمَةُ لا حُدودَ لها
Legally clean: silhouettes (no faces), generic trophy, fan-art disclaimer.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, features
import numpy as np

assert features.check("raqm"), "need Raqm for Arabic shaping"
AR = {"direction": "rtl", "language": "ar"}
SRC = os.environ.get("SAU_SRC", "/tmp/saudi.png")
FD = "/tmp/fonts"
ROOT = "/home/user/Huroof/products"
def P(*a): return os.path.join(ROOT, *a)
def f(n, s): return ImageFont.truetype(os.path.join(FD, n), s)

GOLD = (224, 188, 110)
GOLD_HI = (245, 224, 150)
AR_TXT = "العَظَمَةُ لا حُدودَ لها"
EN_TXT = "GREATNESS HAS NO LIMITS"
TRI = "TRIUMPH EDITION  |  إصدار النصر"

base = Image.open(SRC).convert("RGB")
W, H = base.size

def fit(text, fname, max_w, start, rtl=False):
    fn = f(fname, start); m = ImageDraw.Draw(Image.new("L", (8, 8)))
    w = m.textlength(text, font=fn, **(AR if rtl else {}))
    return f(fname, max(20, int(start*max_w/w))) if w > max_w else fn

def compose():
    img = base.copy().convert("RGBA")
    # top + bottom dark scrims for text legibility
    grad = np.zeros((H, 1, 4), np.uint8)
    ys = np.linspace(0, 1, H)
    top = np.clip((0.34-ys)/0.34, 0, 1)**1.4 * 200
    bot = np.clip((ys-0.62)/0.38, 0, 1)**1.4 * 215
    a = np.maximum(top, bot)
    scrim = np.zeros((H, W, 4), np.uint8); scrim[..., 3] = a[:, None]
    img.alpha_composite(Image.fromarray(scrim, "RGBA"))
    d = ImageDraw.Draw(img, "RGBA")
    # Arabic (top) — verified Amiri shaping
    fa = fit(AR_TXT, "Amiri-Bold.ttf", W*0.78, int(W*0.090), rtl=True)
    d.text((W//2, int(H*0.135)), AR_TXT, font=fa, fill=GOLD_HI, anchor="mm",
           stroke_width=max(1, W//900), stroke_fill=(40, 28, 6), **AR)
    # English (bottom)
    fe = fit(EN_TXT, "Inter[opsz,wght].ttf", W*0.82, int(W*0.085))
    d.text((W//2, int(H*0.855)), EN_TXT, font=fe, fill=GOLD,
           anchor="mm", stroke_width=max(2, W//520), stroke_fill=(30, 22, 6))
    # gold rule
    d.rectangle([int(W*0.40), int(H*0.915), int(W*0.60), int(H*0.918)], fill=GOLD)
    # Triumph line — English in Inter, Arabic in Amiri (Inter has no Arabic glyphs)
    col = (232, 224, 205)
    en_tri = "TRIUMPH EDITION"; sep = "  |  "; ar_tri = "إصدار النصر"
    ft = f("Inter[opsz,wght].ttf", int(W*0.020))
    far = f("Amiri-Bold.ttf", int(W*0.024))
    we = d.textlength(en_tri+sep, font=ft)
    wa = d.textlength(ar_tri, font=far, **AR)
    total = we + wa
    x0 = W//2 - int(total/2); y = int(H*0.95)
    d.text((x0, y), en_tri+sep, font=ft, fill=col, anchor="lm")
    d.text((x0+we, y), ar_tri, font=far, fill=col, anchor="lm", **AR)
    return img.convert("RGB")

master = compose()

# 1. CLEAN PRINT FILE (buyer download) — small © signature
pr = master.copy(); dp = ImageDraw.Draw(pr, "RGBA")
dp.text((int(W*0.012), H-int(W*0.012)), "© Huroof · huroofartdesign.com",
        font=f("Inter[opsz,wght].ttf", int(W*0.013)), fill=(255, 255, 255, 110), anchor="lb")
os.makedirs(P("print", "events"), exist_ok=True)
pr.save(P("print", "events", "saudi-greatness-print.jpg"), quality=95)

def sign_on(img):
    im = img.copy(); d = ImageDraw.Draw(im, "RGBA"); w, h = im.size
    d.text((int(w*0.02), h-int(w*0.02)), "© Huroof · huroofartdesign.com",
           font=f("Inter[opsz,wght].ttf", int(w*0.018)), fill=GOLD+(220,), anchor="lm")
    return im

def protected(img):
    im = img.copy().convert("RGBA"); w, h = im.size
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    wm = f("Inter[opsz,wght].ttf", int(w*0.030)); txt = "HUROOF · huroofartdesign.com"
    for yy in range(-h, h*2, int(h*0.22)):
        for xx in range(-w, w*2, int(w*0.42)):
            d.text((xx, yy), txt, font=wm, fill=(255, 255, 255, 36))
    ov = ov.rotate(22, expand=False); im.alpha_composite(ov)
    return sign_on(im.convert("RGB"))

def pad(img, tw, th, bg=(7, 12, 8)):
    c = Image.new("RGB", (tw, th), bg); im = img.copy()
    im.thumbnail((tw, th), Image.LANCZOS); c.paste(im, ((tw-im.width)//2, (th-im.height)//2)); return c

# 2. PREVIEW (watermarked)
prev = master.copy(); prev.thumbnail((1600, 1600), Image.LANCZOS)
protected(prev).save(P("previews", "events", "saudi-greatness.jpg"), quality=90)

# 3. PIN 1000x1500 (landscape padded on canvas, watermarked)
pin = master.copy(); pin.thumbnail((1000, 1000), Image.LANCZOS)
pad(protected(pin), 1000, 1500).save(P("pins", "events", "saudi-greatness-pin.jpg"), quality=90)

# 4. FRAMED MOCKUP (landscape)
def framed(poster, out, wall=(232, 226, 216)):
    cw, chh = 1400, 1050
    canvas = Image.new("RGB", (cw, chh), wall)
    fw = 980; fh = int(fw*poster.height/poster.width); fr_x = (cw-fw)//2; fr_y = (chh-fh)//2
    sh = Image.new("RGBA", (cw, chh), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    ds.rectangle([fr_x+14, fr_y+20, fr_x+fw+14, fr_y+fh+20], fill=(0, 0, 0, 70))
    canvas.paste(Image.new("RGB", (cw, chh), (0, 0, 0)), (0, 0), sh.filter(ImageFilter.GaussianBlur(18)))
    d = ImageDraw.Draw(canvas); d.rectangle([fr_x, fr_y, fr_x+fw, fr_y+fh], fill=(20, 20, 22))
    mat = 26; d.rectangle([fr_x+mat, fr_y+mat, fr_x+fw-mat, fr_y+fh-mat], fill=(250, 248, 244))
    p = poster.resize((fw-2*mat-20, fh-2*mat-20), Image.LANCZOS)
    canvas.paste(p, (fr_x+mat+10, fr_y+mat+10)); canvas.save(out, quality=92)
framed(protected(master.copy().resize((1000, int(1000*H/W)), Image.LANCZOS)),
       P("mockups", "events", "saudi-greatness-framed.jpg"))

# 5. SOCIAL
S = lambda *a: P("social", "events", *a)
master.resize((1200, 675), Image.LANCZOS).save(S("saudi-facebook-1200x675.jpg"), quality=90)
# square: center-crop
sq = master.crop(((W-H)//2, 0, (W-H)//2+H, H)).resize((1080, 1080), Image.LANCZOS)
sq.save(S("saudi-instagram-square-1080.jpg"), quality=90)
pad(master, 1080, 1350).save(S("saudi-instagram-portrait-1080x1350.jpg"), quality=90)
pad(master, 1080, 1920).save(S("saudi-story-1080x1920.jpg"), quality=90)

print("source", base.size)
for r, _, fs in os.walk(P()):
    for fn in fs:
        if "saudi" in fn:
            pth = os.path.join(r, fn); print(" ", os.path.relpath(pth, ROOT), Image.open(pth).size)
