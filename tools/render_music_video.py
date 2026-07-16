#!/usr/bin/env python3
"""Neon Multiverse audio-reactive music video renderer for 'Show Me All The Signs'.

Follows the storyboard: neon portal intro build (0-25s), energy montage,
heart shockwave climax on the final chorus, glitter title card ending.
Palette: hot pink #FF1493, electric purple #BF00FF, neon cyan #00FFFF, gold #FFD700.
"""
import sys, math, subprocess
import numpy as np
from scipy.io import wavfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter

AUDIO = "Show Me All The Signs (Mastered).wav"

MODE = sys.argv[1] if len(sys.argv) > 1 else "wide"   # wide | vertical
if MODE == "wide":
    W, H, FPS = 1280, 720, 30
    T0, T1 = 0.0, None
    OUT = "Show Me All The Signs (Official Visualizer).mp4"
else:
    W, H, FPS = 720, 1280, 30
    T0, T1 = 28.0, 58.0
    OUT = "Show Me All The Signs (Hook Clip Vertical).mp4"

PINK   = (255, 20, 147)
PURPLE = (191, 0, 255)
CYAN   = (0, 255, 255)
GOLD   = (255, 215, 0)
BG     = (8, 4, 15)

# ---------- audio analysis ----------
sr, data = wavfile.read(AUDIO)
mono = data.astype(np.float32).mean(axis=1) / 32768.0
dur = len(mono) / sr
if T1 is None:
    T1 = dur
n_frames = int((T1 - T0) * FPS)

hop = sr // FPS
win = 2048
NB = 56  # spectrum bands
edges = np.geomspace(40, 12000, NB + 1)
hann = np.hanning(win)
freqs = np.fft.rfftfreq(win, 1 / sr)
band_idx = [(freqs >= edges[i]) & (freqs < edges[i + 1]) for i in range(NB)]

def frame_audio(t):
    c = int(t * sr)
    s = max(0, c - win // 2)
    seg = mono[s:s + win]
    if len(seg) < win:
        seg = np.pad(seg, (0, win - len(seg)))
    sp = np.abs(np.fft.rfft(seg * hann))
    bands = np.array([sp[m].mean() if m.any() else 0.0 for m in band_idx])
    rms = float(np.sqrt(np.mean(seg ** 2)))
    bass = float(bands[:8].mean())
    return bands, rms, bass

# pre-scan for normalization
print("scanning audio...", flush=True)
all_b, all_r, all_ba = [], [], []
for i in range(0, n_frames, 3):
    b, r, ba = frame_audio(T0 + i / FPS)
    all_b.append(b); all_r.append(r); all_ba.append(ba)
bmax = np.percentile(np.array(all_b), 98, axis=0) + 1e-9
rmax = np.percentile(all_r, 98) + 1e-9
bamax = np.percentile(all_ba, 98) + 1e-9

# ---------- helpers ----------
def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def spoke_color(frac):
    # angle-based gradient pink -> purple -> cyan -> gold -> pink
    stops = [PINK, PURPLE, CYAN, GOLD, PINK]
    x = frac * 4
    i = min(3, int(x))
    return lerp(stops[i], stops[i + 1], x - i)

def heart_pts(cx, cy, s, n=80):
    t = np.linspace(0, 2 * np.pi, n)
    x = 16 * np.sin(t) ** 3
    y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
    return list(zip(cx + x * s, cy - y * s))

try:
    FB = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(W * 0.055))
    FS = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(W * 0.020))
    FT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(W * 0.072))
except Exception:
    FB = FS = FT = ImageFont.load_default()

# vignette (precomputed multiply mask)
yy, xx = np.mgrid[0:H, 0:W]
d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
vig = np.clip(1.15 - 0.45 * d ** 2, 0, 1).astype(np.float32)[:, :, None]

# particles (deterministic star glitter field)
rng = np.random.default_rng(7)
NP = 170
px = rng.random(NP); py = rng.random(NP)
pspd = 0.004 + rng.random(NP) * 0.012
psz = 1 + rng.random(NP) * 2.4
pcol = [spoke_color(f) for f in rng.random(NP)]

CX, CY = W / 2, H * (0.44 if MODE == "wide" else 0.40)
RMAX = min(W, H) * 0.26

smooth_bands = np.zeros(NB)
smooth_rms = 0.0
hearts = []       # (birth_time,)
last_heart = -10.0
CLIMAX = (152.0, 181.0)   # final chorus window (song time)
title_txt = "SHOW ME ALL THE SIGNS"

ff = subprocess.Popen(
    ["ffmpeg", "-y", "-v", "error",
     "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
     "-ss", str(T0), "-t", str(T1 - T0), "-i", AUDIO,
     "-c:v", "libx264", "-preset", "medium", "-crf", "23",
     "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", OUT],
    stdin=subprocess.PIPE)

print(f"rendering {n_frames} frames {W}x{H}...", flush=True)
for fi in range(n_frames):
    t_song = T0 + fi / FPS
    bands, rms, bass = frame_audio(t_song)
    bands = np.clip(bands / bmax, 0, 1) ** 0.7
    smooth_bands = np.maximum(bands, smooth_bands * 0.82)
    rr = min(1.0, rms / rmax)
    smooth_rms = max(rr, smooth_rms * 0.9)
    bb = min(1.0, bass / bamax)

    img = Image.new("RGB", (W, H), BG)
    dr = ImageDraw.Draw(img, "RGBA")

    # global reveal during intro build
    reveal = min(1.0, t_song / 22.0) if MODE == "wide" else 1.0

    # --- synthwave floor grid ---
    horizon = H * 0.62
    ga = int(60 * reveal + 50 * smooth_rms)
    for k in range(10):  # horizontal scrolling lines
        ph = ((t_song * 0.35 + k / 10.0) % 1.0)
        y = horizon + (H - horizon) * ph ** 2.2
        dr.line([(0, y), (W, y)], fill=PINK + (max(10, int(ga * ph)),), width=2)
    for k in range(-8, 9):  # converging verticals
        x0 = CX + k * W * 0.09
        x1 = CX + k * W * 0.42
        dr.line([(x0, horizon), (x1, H)], fill=PURPLE + (ga,), width=2)
    dr.line([(0, horizon), (W, horizon)], fill=CYAN + (int(90 * reveal),), width=2)

    # --- particles / glitter ---
    inten = 0.35 + 0.65 * smooth_rms
    in_climax = CLIMAX[0] <= t_song <= CLIMAX[1]
    for i in range(NP):
        yy_p = (py[i] - t_song * pspd[i]) % 1.0
        x = px[i] * W
        y = yy_p * H
        tw = 0.5 + 0.5 * math.sin(t_song * 3 + i)
        a = int(200 * inten * tw * (1.6 if in_climax else 1.0) * reveal)
        s = psz[i] * (1.5 if in_climax else 1.0)
        dr.ellipse([x - s, y - s, x + s, y + s], fill=pcol[i] + (min(255, a),))

    # --- portal ring + swirl ---
    R = RMAX * (0.15 + 0.85 * reveal) * (1 + 0.10 * bb)
    for gw, gac in [(int(R * 0.30), 26), (int(R * 0.14), 60), (int(R * 0.05), 160)]:
        col = lerp(PINK, GOLD, 0.5 + 0.5 * math.sin(t_song * 0.7))
        dr.ellipse([CX - R - gw / 2, CY - R - gw / 2, CX + R + gw / 2, CY + R + gw / 2],
                   outline=col + (int(gac * (0.5 + 0.5 * smooth_rms)),), width=gw)
    dr.ellipse([CX - R, CY - R, CX + R, CY + R], outline=(255, 255, 255, 200), width=2)
    # inner swirl arcs
    for k in range(5):
        ang = math.degrees(t_song * (30 + k * 14)) % 360
        rr_in = R * (0.25 + 0.14 * k)
        col = [PINK, PURPLE, GOLD, CYAN, PINK][k]
        dr.arc([CX - rr_in, CY - rr_in, CX + rr_in, CY + rr_in],
               start=ang, end=ang + 120 + 100 * smooth_rms, fill=col + (150,), width=4)

    # --- radial spectrum spokes ---
    for i in range(NB):
        frac = i / NB
        ang = frac * 2 * math.pi - math.pi / 2
        v = smooth_bands[i]
        r0 = R * 1.06
        r1 = r0 + v * RMAX * 0.85 * (0.3 + 0.7 * reveal)
        c = spoke_color(frac)
        x0, y0 = CX + r0 * math.cos(ang), CY + r0 * math.sin(ang)
        x1, y1 = CX + r1 * math.cos(ang), CY + r1 * math.sin(ang)
        dr.line([(x0, y0), (x1, y1)], fill=c + (70,), width=7)
        dr.line([(x0, y0), (x1, y1)], fill=c + (230,), width=3)

    # --- heart shockwaves during climax ---
    if in_climax and bb > 0.75 and t_song - last_heart > 0.5:
        hearts.append(t_song); last_heart = t_song
    hearts = [h for h in hearts if t_song - h < 2.2]
    for h in hearts:
        age = t_song - h
        s = 0.6 + age * (min(W, H) / 45.0)
        a = int(230 * max(0, 1 - age / 2.2))
        col = lerp(PINK, GOLD, min(1, age))
        dr.line(heart_pts(CX, CY, s) + [heart_pts(CX, CY, s)[0]], fill=col + (a,), width=4)

    # --- text ---
    if MODE == "wide":
        if 4 <= t_song <= 18:  # intro title fade
            a = int(255 * min(1, (t_song - 4) / 2, (18 - t_song) / 2))
            tw_ = dr.textlength(title_txt, font=FB)
            dr.text((CX - tw_ / 2 + 2, H * 0.80 + 2), title_txt, font=FB, fill=PURPLE + (a // 2,))
            dr.text((CX - tw_ / 2, H * 0.80), title_txt, font=FB, fill=(255, 255, 255, a))
        if t_song >= dur - 12:  # end title card, spray on L->R
            prog = min(1.0, (t_song - (dur - 12)) / 2.5)
            fade = min(1.0, (t_song - (dur - 12)) / 1.0)
            # dim backdrop so the card reads clearly
            dr.rectangle([0, 0, W, H], fill=(4, 2, 8, int(150 * fade)))
            ft = FT
            sz = int(W * 0.072)
            while dr.textlength(title_txt, font=ft) > W * 0.92 and sz > 10:
                sz -= 2
                ft = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", sz)
            tw_ = dr.textlength(title_txt, font=ft)
            ty = H * 0.42
            card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            cd = ImageDraw.Draw(card)
            cd.text((CX - tw_ / 2 + 4, ty + 4), title_txt, font=ft, fill=PURPLE + (220,))
            cd.text((CX - tw_ / 2, ty), title_txt, font=ft, fill=PINK + (255,),
                    stroke_width=2, stroke_fill=GOLD + (255,))
            sub = "A NEON MULTIVERSE PRODUCTION"
            sw = cd.textlength(sub, font=FS)
            if prog >= 1.0:
                cd.text((CX - sw / 2, ty + sz * 1.35), sub, font=FS, fill=(255, 255, 255, 220))
            mask = Image.new("L", (W, H), 0)
            ImageDraw.Draw(mask).rectangle([0, 0, int(W * prog), H], fill=255)
            img.paste(card, (0, 0), Image.composite(card.split()[3], Image.new("L", (W, H), 0), mask))
    else:
        tw_ = dr.textlength(title_txt, font=FB)
        dr.text((CX - tw_ / 2, H * 0.86), title_txt, font=FB, fill=(255, 255, 255, 235))

    # --- post: chromatic aberration + vignette ---
    arr = np.asarray(img).astype(np.float32)
    sh = 1 + int(2 * smooth_rms)
    arr[:, sh:, 0] = arr[:, :-sh, 0]      # red shifted right
    arr[:, :-sh, 2] = arr[:, sh:, 2]      # blue shifted left
    arr *= vig
    frame = np.clip(arr, 0, 255).astype(np.uint8)
    ff.stdin.write(frame.tobytes())

    if fi % 300 == 0:
        print(f"frame {fi}/{n_frames} ({fi/n_frames*100:.0f}%)", flush=True)
    if MODE == "wide" and fi in (int(10 * FPS), int(45 * FPS), int(160 * FPS), int(186 * FPS)):
        Image.fromarray(frame).save(f"snap_{int(t_song)}s.png")

ff.stdin.close()
ff.wait()
print("DONE", OUT, flush=True)
