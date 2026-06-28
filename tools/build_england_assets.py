#!/usr/bin/env python3
"""Algeria 'Born to Win / ولدنا للفوز' poster — tagline already baked in.
Cut clean print, watermarked preview, framed mockup, pin, 4 social sizes.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRC = os.environ.get("ENG_SRC", "/tmp/england.jpg")
FD = "/tmp/fonts"; ROOT = "/home/user/Huroof/products"
def P(*a): return os.path.join(ROOT, *a)
def f(n, s): return ImageFont.truetype(os.path.join(FD, n), s)
GOLD = (224, 188, 110)
src = Image.open(SRC).convert("RGB"); W, H = src.size

def sign_on(img):
    im = img.copy(); d = ImageDraw.Draw(im, "RGBA"); w, h = im.size
    d.text((int(w*0.03), h-int(w*0.03)), "© Huroof · huroofartdesign.com",
           font=f("Inter[opsz,wght].ttf", int(w*0.020)), fill=GOLD+(220,), anchor="lm"); return im
def protected(img):
    im = img.copy().convert("RGBA"); w, h = im.size
    ov = Image.new("RGBA", (w, h), (0,0,0,0)); d = ImageDraw.Draw(ov)
    wm = f("Inter[opsz,wght].ttf", int(w*0.035))
    for yy in range(-h, h*2, int(h*0.20)):
        for xx in range(-w, w*2, int(w*0.55)):
            d.text((xx, yy), "HUROOF · huroofartdesign.com", font=wm, fill=(255,255,255,38))
    ov = ov.rotate(30, expand=False); im.alpha_composite(ov); return sign_on(im.convert("RGB"))
def pad(img, tw, th, bg=(8,10,8)):
    c = Image.new("RGB", (tw, th), bg); im = img.copy(); im.thumbnail((tw, th), Image.LANCZOS)
    c.paste(im, ((tw-im.width)//2, (th-im.height)//2)); return c

# 1. CLEAN PRINT
pr = src.copy(); d = ImageDraw.Draw(pr, "RGBA")
d.text((int(W*0.5), H-int(W*0.018)), "© Huroof · huroofartdesign.com",
       font=f("Inter[opsz,wght].ttf", int(W*0.014)), fill=(255,255,255,95), anchor="mm")
os.makedirs(P("print","events"), exist_ok=True)
pr.save(P("print","events","england-born-print.jpg"), quality=95)
# 2. PREVIEW
prev = src.copy(); prev.thumbnail((1400,2100), Image.LANCZOS)
protected(prev).save(P("previews","events","england-born.jpg"), quality=90)
# 3. PIN
pin = src.copy(); pin.thumbnail((1000,1500), Image.LANCZOS)
pad(protected(pin),1000,1500).save(P("pins","events","england-born-pin.jpg"), quality=90)
# 4. FRAMED MOCKUP (portrait)
def framed(poster,out,wall=(232,226,216)):
    cw,chh=1200,1500; canvas=Image.new("RGB",(cw,chh),wall)
    pw=760; ph=int(pw*poster.height/poster.width); fr_x=(cw-pw-92)//2; fr_y=(chh-ph-92)//2
    fw,fh=pw+92,ph+92
    sh=Image.new("RGBA",(cw,chh),(0,0,0,0)); ds=ImageDraw.Draw(sh)
    ds.rectangle([fr_x+14,fr_y+20,fr_x+fw+14,fr_y+fh+20],fill=(0,0,0,70))
    canvas.paste(Image.new("RGB",(cw,chh),(0,0,0)),(0,0),sh.filter(ImageFilter.GaussianBlur(18)))
    dd=ImageDraw.Draw(canvas); dd.rectangle([fr_x,fr_y,fr_x+fw,fr_y+fh],fill=(20,20,22))
    mat=30; dd.rectangle([fr_x+mat,fr_y+mat,fr_x+fw-mat,fr_y+fh-mat],fill=(250,248,244))
    p=poster.resize((fw-2*mat-20,fh-2*mat-20),Image.LANCZOS); canvas.paste(p,(fr_x+mat+10,fr_y+mat+10))
    canvas.save(out,quality=92)
framed(protected(src.copy().resize((600,int(600*H/W)),Image.LANCZOS)),
       P("mockups","events","england-born-framed.jpg"))
# 5. SOCIAL
S=lambda *a:P("social","events",*a)
pad(src,1080,1350).save(S("england-instagram-portrait-1080x1350.jpg"),quality=90)
cx=src.crop((0,(H-W)//2 if H>W else 0,W,(H-W)//2+W if H>W else H)).resize((1080,1080),Image.LANCZOS)
cx.save(S("england-instagram-square-1080.jpg"),quality=90)
pad(src,1080,1920).save(S("england-story-1080x1920.jpg"),quality=90)
pad(src,1200,675).save(S("england-facebook-1200x675.jpg"),quality=90)
print("source",src.size)
for r,_,fs in os.walk(P()):
    for fn in fs:
        if "england" in fn: pth=os.path.join(r,fn); print(" ",os.path.relpath(pth,ROOT),Image.open(pth).size)
