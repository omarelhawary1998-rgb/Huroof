#!/usr/bin/env python3
"""Build every platform asset for the Morocco 'Where Dreams Become Legends'
poster. Source is square. Outputs clean print, watermarked preview, framed
mockup, Pinterest pin, and 4 social sizes. Re-run after dropping a higher-res
SRC to refresh the print file.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC = os.environ.get("MOR_SRC", "/tmp/morocco.jpg")
FD = "/tmp/fonts"
ROOT = "/home/user/Huroof/products"
def P(*a): return os.path.join(ROOT, *a)
def f(name, s): return ImageFont.truetype(os.path.join(FD, name), s)
GOLD = (224, 188, 110)

src = Image.open(SRC).convert("RGB")
W, H = src.size

def sign_on(img):
    im = img.copy(); d = ImageDraw.Draw(im, "RGBA"); w, h = im.size
    d.text((int(w*0.03), h-int(w*0.03)), "© Huroof · huroofartdesign.com",
           font=f("Inter[opsz,wght].ttf", int(w*0.020)), fill=GOLD+(220,), anchor="lm")
    return im

def protected(img):
    im = img.copy().convert("RGBA"); w, h = im.size
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    wm = f("Inter[opsz,wght].ttf", int(w*0.035))
    txt = "HUROOF · huroofartdesign.com"
    for yy in range(-h, h*2, int(h*0.20)):
        for xx in range(-w, w*2, int(w*0.55)):
            d.text((xx, yy), txt, font=wm, fill=(255, 255, 255, 38))
    ov = ov.rotate(30, expand=False); im.alpha_composite(ov)
    return sign_on(im.convert("RGB"))

def pad(img, tw, th, bg=(9, 11, 9)):
    canvas = Image.new("RGB", (tw, th), bg)
    im = img.copy(); im.thumbnail((tw, th), Image.LANCZOS)
    canvas.paste(im, ((tw-im.width)//2, (th-im.height)//2)); return canvas

# 1. CLEAN PRINT FILE (buyer download)
pr = src.copy(); d = ImageDraw.Draw(pr, "RGBA")
d.text((int(W*0.5), H-int(W*0.022)), "© Huroof · huroofartdesign.com",
       font=f("Inter[opsz,wght].ttf", int(W*0.018)), fill=(255,255,255,90), anchor="mm")
pr.save(P("print", "events", "morocco-legends-print.jpg"), quality=95)

# 2. WATERMARKED PREVIEW
prev = src.copy(); prev.thumbnail((1400, 1400), Image.LANCZOS)
protected(prev).save(P("previews", "events", "morocco-legends.jpg"), quality=90)

# 3. PINTEREST PIN 1000x1500
pin = src.copy(); pin.thumbnail((1000, 1000), Image.LANCZOS)
pad(protected(pin), 1000, 1500).save(P("pins", "events", "morocco-legends-pin.jpg"), quality=90)

# 4. FRAMED MOCKUP (square)
def framed(poster, out, wall=(232, 226, 216)):
    cw = chh = 1200
    canvas = Image.new("RGB", (cw, chh), wall)
    fw = fh = 820; fr_x = (cw-fw)//2; fr_y = (chh-fh)//2
    sh = Image.new("RGBA", (cw, chh), (0,0,0,0)); ds = ImageDraw.Draw(sh)
    ds.rectangle([fr_x+14, fr_y+20, fr_x+fw+14, fr_y+fh+20], fill=(0,0,0,70))
    canvas.paste(Image.new("RGB",(cw,chh),(0,0,0)),(0,0),sh.filter(ImageFilter.GaussianBlur(18)))
    d = ImageDraw.Draw(canvas)
    d.rectangle([fr_x, fr_y, fr_x+fw, fr_y+fh], fill=(20,20,22))
    mat = 30
    d.rectangle([fr_x+mat, fr_y+mat, fr_x+fw-mat, fr_y+fh-mat], fill=(250,248,244))
    p = poster.resize((fw-2*mat-20, fh-2*mat-20), Image.LANCZOS)
    canvas.paste(p, (fr_x+mat+10, fr_y+mat+10))
    canvas.save(out, quality=92)
framed(protected(src.copy().resize((700,700), Image.LANCZOS)),
       P("mockups", "events", "morocco-legends-framed.jpg"))

# 5. SOCIAL SET
S = lambda *a: P("social", "events", *a)
src.resize((1080,1080), Image.LANCZOS).save(S("morocco-instagram-square-1080.jpg"), quality=90)
pad(src, 1080, 1350).save(S("morocco-instagram-portrait-1080x1350.jpg"), quality=90)
pad(src, 1080, 1920).save(S("morocco-story-1080x1920.jpg"), quality=90)
pad(src, 1200, 675).save(S("morocco-facebook-1200x675.jpg"), quality=90)

print("source", src.size)
for r,_,fs in os.walk(P()):
    for fn in fs:
        if "morocco" in fn:
            pth=os.path.join(r,fn); print(" ", os.path.relpath(pth,ROOT), Image.open(pth).size)
