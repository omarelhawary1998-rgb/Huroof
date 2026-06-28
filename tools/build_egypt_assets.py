#!/usr/bin/env python3
"""Build every platform asset for the Egypt 'Destiny Is a Choice' poster
from the upscaled clean source. Outputs: clean print file (buyer download),
watermarked preview, framed mockup, Pinterest pin, and 4 social sizes.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC = "/tmp/egypt_upscaled.png"
FD = "/tmp/fonts"
ROOT = "/home/user/Huroof/products"
def P(*a): return os.path.join(ROOT, *a)
def f(name, s): return ImageFont.truetype(os.path.join(FD, name), s)

GOLD = (224, 188, 110)
src = Image.open(SRC).convert("RGB")
W, H = src.size

# ---------- 1. CLEAN PRINT FILE (buyer download) — small © signature only ----------
print_img = src.copy()
d = ImageDraw.Draw(print_img, "RGBA")
sig = f("Inter[opsz,wght].ttf", int(W*0.018))
d.text((int(W*0.5), H-int(W*0.022)), "© Huroof · huroofartdesign.com",
       font=sig, fill=(255, 255, 255, 90), anchor="mm")
os.makedirs(P("print", "events"), exist_ok=True)
print_img.save(P("print", "events", "egypt-destiny-print.jpg"), quality=95)

# ---------- helpers ----------
def sign_on(img):
    """Gold © signature bottom-left."""
    im = img.copy(); d = ImageDraw.Draw(im, "RGBA")
    w, h = im.size
    d.text((int(w*0.03), h-int(w*0.03)), "© Huroof · huroofartdesign.com",
           font=f("Inter[opsz,wght].ttf", int(w*0.020)), fill=GOLD+(220,), anchor="lm")
    return im

def protected(img):
    """Diagonal repeating faint watermark across the image."""
    im = img.copy().convert("RGBA")
    w, h = im.size
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    wm = f("Inter[opsz,wght].ttf", int(w*0.035))
    txt = "HUROOF · huroofartdesign.com"
    step_x, step_y = int(w*0.55), int(h*0.20)
    for yy in range(-h, h*2, step_y):
        for xx in range(-w, w*2, step_x):
            d.text((xx, yy), txt, font=wm, fill=(255, 255, 255, 38))
    ov = ov.rotate(30, expand=False)
    im.alpha_composite(ov)
    return sign_on(im.convert("RGB"))

def pad(img, tw, th, bg=(8, 9, 15)):
    """Contain img on a dark canvas of tw x th (for social formats)."""
    canvas = Image.new("RGB", (tw, th), bg)
    im = img.copy()
    im.thumbnail((tw, th), Image.LANCZOS)
    canvas.paste(im, ((tw-im.width)//2, (th-im.height)//2))
    return canvas

# ---------- 2. WATERMARKED PREVIEW (listings + website main image) ----------
preview = src.copy()
preview.thumbnail((1200, 1800), Image.LANCZOS)
protected(preview).save(P("previews", "events", "egypt-destiny.jpg"), quality=90)

# ---------- 3. PINTEREST PIN 1000x1500 (watermarked) ----------
pin = src.copy(); pin.thumbnail((1000, 1500), Image.LANCZOS)
pin_canvas = pad(protected(pin), 1000, 1500)
pin_canvas.save(P("pins", "events", "egypt-destiny-pin.jpg"), quality=90)

# ---------- 4. FRAMED MOCKUP (sharp, from upscaled source) ----------
def framed(poster, out, wall=(232, 226, 216)):
    pw, ph = 760, int(760 * poster.height/poster.width)
    cw, chh = 1200, 1200
    canvas = Image.new("RGB", (cw, chh), wall)
    # soft shadow
    fr_x, fr_y = (cw-pw)//2 - 46, (chh-ph)//2 - 46
    fw, fh = pw + 92, ph + 92
    sh = Image.new("RGBA", (cw, chh), (0, 0, 0, 0))
    ds = ImageDraw.Draw(sh)
    ds.rectangle([fr_x+14, fr_y+20, fr_x+fw+14, fr_y+fh+20], fill=(0, 0, 0, 70))
    canvas.paste(Image.new("RGB", (cw, chh), (0, 0, 0)), (0, 0),
                 sh.filter(ImageFilter.GaussianBlur(18)))
    # black frame + white mat
    d = ImageDraw.Draw(canvas)
    d.rectangle([fr_x, fr_y, fr_x+fw, fr_y+fh], fill=(20, 20, 22))
    mat = 30
    d.rectangle([fr_x+mat, fr_y+mat, fr_x+fw-mat, fr_y+fh-mat], fill=(250, 248, 244))
    p = poster.resize((pw-2*mat+ (fw-2*mat - (pw-2*mat)), ph), Image.LANCZOS) if False else poster.resize((fw-2*mat-20, fh-2*mat-20), Image.LANCZOS)
    canvas.paste(p, (fr_x+mat+10, fr_y+mat+10))
    canvas.save(out, quality=92)
framed(protected(src.copy().resize((600, int(600*H/W)), Image.LANCZOS)),
       P("mockups", "events", "egypt-destiny-framed.jpg"))

# ---------- 5. SOCIAL SET ----------
S = lambda *a: P("social", "events", *a)
pad(src, 1080, 1350).save(S("egypt-instagram-portrait-1080x1350.jpg"), quality=90)
pad(src, 1080, 1080).save(S("egypt-instagram-square-1080.jpg"), quality=90)
pad(src, 1080, 1920).save(S("egypt-story-1080x1920.jpg"), quality=90)
pad(src, 1200, 675).save(S("egypt-facebook-1200x675.jpg"), quality=90)

print("done. source:", src.size)
for r, _, fs in os.walk(P()):
    for fn in fs:
        if "egypt" in fn:
            pth = os.path.join(r, fn)
            print(f"  {os.path.relpath(pth, ROOT)}  {Image.open(pth).size}")
