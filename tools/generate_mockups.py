#!/usr/bin/env python3
"""Generate product mockups from preview art — framed wall scene + matted.

Self-contained (no external template images): composes a believable gallery
frame around each design so Etsy/Payhip listings have lifestyle imagery.

    python3 tools/generate_mockups.py SRC_DIR OUT_DIR
SRC_DIR holds NN-slug.jpg previews; OUT_DIR gets <slug>-framed.jpg (1200x1200).
"""
import os, sys, glob
from PIL import Image, ImageDraw, ImageFilter

SRC = sys.argv[1] if len(sys.argv) > 1 else "products/previews"
OUT = sys.argv[2] if len(sys.argv) > 2 else "products/mockups"

def hex2rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def wall(size, top="#EDE7DD", bot="#D9CFBF"):
    """Soft warm vertical gradient wall."""
    w, h = size
    img = Image.new("RGB", size)
    t, b = hex2rgb(top), hex2rgb(bot)
    px = img.load()
    for y in range(h):
        f = y / h
        row = tuple(int(t[i] * (1 - f) + b[i] * f) for i in range(3))
        for x in range(w):
            px[x, y] = row
    return img

def framed(prev, S=1200, frame="#2A2622", mat="#F7F3EC"):
    """Artwork in a mat + frame, drop-shadowed on a wall, portrait centred."""
    canvas = wall((S, S))
    # portrait art box ~62% of canvas height
    art_h = int(S * 0.62)
    art_w = int(art_h * prev.width / prev.height)
    mat_pad, frame_w = int(art_h * 0.06), int(art_h * 0.035)
    fw = art_w + 2 * (mat_pad + frame_w)
    fh = art_h + 2 * (mat_pad + frame_w)
    fx, fy = (S - fw) // 2, (S - fh) // 2 - int(S * 0.02)
    # drop shadow
    sh = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([fx + 14, fy + 20, fx + fw + 14, fy + fh + 20], fill=(0, 0, 0, 90))
    sh = sh.filter(ImageFilter.GaussianBlur(22))
    canvas.paste(Image.new("RGB", (S, S), "black"), (0, 0), sh.getchannel("A"))
    d = ImageDraw.Draw(canvas)
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=hex2rgb(frame))                      # frame
    d.rectangle([fx + frame_w, fy + frame_w, fx + fw - frame_w, fy + fh - frame_w], fill=hex2rgb(mat))  # mat
    art = prev.resize((art_w, art_h))
    canvas.paste(art, (fx + frame_w + mat_pad, fy + frame_w + mat_pad))
    # subtle inner bevel line
    d.rectangle([fx + frame_w + mat_pad - 3, fy + frame_w + mat_pad - 3,
                 fx + frame_w + mat_pad + art_w + 2, fy + frame_w + mat_pad + art_h + 2],
                outline=(190, 180, 165), width=2)
    return canvas

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for p in sorted(glob.glob(os.path.join(SRC, "*.jpg"))):
        slug = os.path.splitext(os.path.basename(p))[0]
        framed(Image.open(p).convert("RGB")).save(f"{OUT}/{slug}-framed.jpg", quality=88)
        print("mockup", slug)
