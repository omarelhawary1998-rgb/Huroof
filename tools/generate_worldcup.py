#!/usr/bin/env python3
"""Egypt football-pride poster — legally clean (no real players, no FIFA marks).

Generic gold trophy + football + confetti + Egyptian colours + original tagline
"DESTINY IS A CHOICE / المَصِيرُ اخْتِيَار". Huroof © watermark embedded.
"""
import math, os, sys, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, features

assert features.check("raqm"), "need Raqm for Arabic"
AR = {"direction": "rtl", "language": "ar"}
FD = "/tmp/fonts"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/wc"

RED, GOLD, GOLD_HI, CREAM = (206,17,38), (224,178,80), (245,224,150), (244,239,228)

def f(name, s): return ImageFont.truetype(os.path.join(FD, name), s)
def hx(h): h=h.lstrip("#"); return tuple(int(h[i:i+2],16) for i in (0,2,4))

def bg(w, h):
    top, mid, bot = (58,8,18), (28,6,12), (8,9,15)
    t = np.linspace(0,1,h)[:,None,None]
    col = np.where(t<.5,(1-t*2)*np.array(top)+t*2*np.array(mid),
                        (1-(t-.5)*2)*np.array(mid)+(t-.5)*2*np.array(bot))
    return Image.fromarray(np.repeat(col,w,axis=1).astype(np.uint8),"RGB").convert("RGBA")

def glow(img, cx, cy, r, color, a=120):
    ov=Image.new("RGBA",img.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=color+(a,))
    img.alpha_composite(ov.filter(ImageFilter.GaussianBlur(r/2.2)))

def rays(img, cx, cy, n=16):
    ov=Image.new("RGBA",img.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    W,H=img.size
    for i in range(n):
        a=(i/n)*2*math.pi
        x=cx+math.cos(a)*H; y=cy+math.sin(a)*H
        a2=a+0.06
        x2=cx+math.cos(a2)*H; y2=cy+math.sin(a2)*H
        d.polygon([(cx,cy),(x,y),(x2,y2)],fill=GOLD+(18,))
    img.alpha_composite(ov.filter(ImageFilter.GaussianBlur(6)))

def confetti(img, rng):
    ov=Image.new("RGBA",img.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    W,H=img.size
    cols=[RED+(220,),GOLD+(230,),(255,255,255,210),GOLD_HI+(220,)]
    for _ in range(140):
        x=rng.integers(0,W); y=rng.integers(0,int(H*0.62)); s=rng.integers(6,18)
        c=cols[rng.integers(0,len(cols))]
        if rng.random()<.5:
            d.rectangle([x,y,x+s,y+s*rng.uniform(.4,1)],fill=c)
        else:
            d.polygon([(x,y),(x+s,y),(x+s/2,y+s)],fill=c)
    img.alpha_composite(ov)

def trophy(img, cx, cy, sc):
    """Generic tall winners' cup — NOT the FIFA trophy. cy = top of rim."""
    d=ImageDraw.Draw(img,"RGBA")
    g=GOLD; gh=GOLD_HI; P=lambda v:int(v*sc)
    rimw=P(150); rimh=P(34)
    # tapering V bowl (rim -> narrow waist)
    waist_y=cy+P(190); waistw=P(46)
    d.polygon([(cx-rimw,cy+P(10)),(cx+rimw,cy+P(10)),
               (cx+waistw,waist_y),(cx-waistw,waist_y)],fill=g)
    # rim ellipse (cup opening)
    d.ellipse([cx-rimw,cy-rimh,cx+rimw,cy+rimh],fill=gh)
    d.ellipse([cx-rimw+P(12),cy-rimh+P(8),cx+rimw-P(12),cy+rimh-P(2)],fill=g)
    # highlight stripe on bowl
    d.polygon([(cx-rimw+P(30),cy+P(20)),(cx-rimw+P(60),cy+P(20)),
               (cx-waistw+P(8),waist_y),(cx-waistw-P(6),waist_y)],fill=gh)
    # handles
    for s in (-1,1):
        x0=cx+s*rimw
        d.arc([min(x0,x0+s*P(95)),cy-P(10), max(x0,x0+s*P(95)),cy+P(150)],
              -90,90 if s>0 else 0, fill=g, width=P(20))
        d.arc([x0-P(95),cy-P(10), x0+P(95),cy+P(150)],
              (-90 if s>0 else 90),(90 if s>0 else 270),fill=g,width=P(20))
    # stem
    d.polygon([(cx-waistw+P(6),waist_y),(cx+waistw-P(6),waist_y),
               (cx+P(26),waist_y+P(70)),(cx-P(26),waist_y+P(70))],fill=g)
    # base tiers
    d.rectangle([cx-P(70),waist_y+P(70),cx+P(70),waist_y+P(95)],fill=gh)
    d.rectangle([cx-P(100),waist_y+P(95),cx+P(100),waist_y+P(125)],fill=g)
    # star emblem on bowl
    d.text((cx,cy+P(70)),"★",font=f("Inter[opsz,wght].ttf",P(72)),fill=(58,8,18),anchor="mm")

def football(img, cx, cy, r):
    d=ImageDraw.Draw(img,"RGBA")
    d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(255,255,255,255),outline=(20,20,20),width=max(2,r//14))
    # central pentagon + spokes (simple)
    pts=[(cx+math.cos(math.radians(a-90))*r*0.42, cy+math.sin(math.radians(a-90))*r*0.42) for a in range(0,360,72)]
    d.polygon(pts,fill=(20,20,20))
    for a in range(0,360,72):
        x=cx+math.cos(math.radians(a-90))*r*0.9; y=cy+math.sin(math.radians(a-90))*r*0.9
        px=cx+math.cos(math.radians(a-90))*r*0.42; py=cy+math.sin(math.radians(a-90))*r*0.42
        d.line([(px,py),(x,y)],fill=(20,20,20),width=max(2,r//16))

def fit(text, fname, max_w, start, rtl=False):
    fn=f(fname,start); m=ImageDraw.Draw(Image.new("L",(8,8)))
    w=m.textlength(text,font=fn,**(AR if rtl else {}))
    return f(fname,max(40,int(start*max_w/w))) if w>max_w else fn

def poster(W=1000, H=1500):
    img=bg(W,H); rng=np.random.default_rng(2026)
    rays(img,W//2,int(H*0.30))
    glow(img,W//2,int(H*0.30),int(W*0.42),GOLD,90)
    confetti(img,rng)
    d=ImageDraw.Draw(img,"RGBA")
    # EGYPT banner + 2026
    d.text((W//2,int(H*0.095)),"E G Y P T",font=f("Inter[opsz,wght].ttf",int(W*0.105)),fill=CREAM,anchor="mm")
    d.text((W//2,int(H*0.155)),"·  2 0 2 6  ·",font=f("Inter[opsz,wght].ttf",int(W*0.052)),fill=GOLD,anchor="mm")
    football(img,int(W*0.5),int(H*0.205),int(W*0.030))
    # trophy (cy = rim top)
    trophy(img,W//2,int(H*0.255),W/620)
    glow(img,W//2,int(H*0.34),int(W*0.11),GOLD_HI,60)
    # tagline EN
    fe=fit("DESTINY IS A CHOICE","Inter[opsz,wght].ttf",W*0.86,int(W*0.085))
    d.text((W//2,int(H*0.60)),"DESTINY IS A CHOICE",font=fe,fill=CREAM,anchor="mm")
    # gold rule
    d.rectangle([int(W*0.30),int(H*0.645),int(W*0.70),int(H*0.648)],fill=GOLD)
    # tagline AR
    fa=fit("المَصِيرُ اخْتِيَار","Amiri-Bold.ttf",W*0.80,int(W*0.16),rtl=True)
    d.text((W//2,int(H*0.71)),"المَصِيرُ اخْتِيَار",font=fa,fill=GOLD_HI,anchor="mm",**AR)
    # sub line
    d.text((W//2,int(H*0.80)),"BELIEVE · PLAY · RISE",font=f("Inter[opsz,wght].ttf",int(W*0.034)),fill=RED if False else (230,180,180),anchor="mm")
    # watermark (embedded)
    d.text((W//2,int(H*0.88)),"© huroofartdesign.com",font=f("Inter[opsz,wght].ttf",int(W*0.024)),fill=(255,255,255,120),anchor="mm")
    # footer band
    d.rectangle([0,int(H*0.93),W,H],fill=(8,9,15,255))
    d.text((W//2,int(H*0.955)),"HUROOF — Bilingual Arabic Art",font=f("CormorantGaramond[wght].ttf",int(W*0.040)),fill=GOLD,anchor="mm")
    d.text((W//2,int(H*0.978)),"© Huroof · personal-use licence only · huroofartdesign.com",font=f("Inter[opsz,wght].ttf",int(W*0.020)),fill="#9aa",anchor="mm")
    return img.convert("RGB")

if __name__=="__main__":
    os.makedirs(OUT,exist_ok=True)
    poster(1000,1500).save(f"{OUT}/egypt-2026-pin.jpg",quality=92)
    poster(1000,1500).resize((900,1350)).save(f"{OUT}/egypt-2026-preview.jpg",quality=90)
    poster(2400,3600).save(f"{OUT}/egypt-2026-A-300dpi.jpg",quality=94)  # print file
    print("done", OUT)
