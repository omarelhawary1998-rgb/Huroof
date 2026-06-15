#!/usr/bin/env python3
"""Launch Batch 1 — 30 bilingual phrase posters (see docs/SKU_CATALOG.md).

Data-driven typography posters: Arabic (Amiri, HarfBuzz-shaped) + English,
one palette per collection. Usage:
    python3 tools/generate_batch1.py [OUT_DIR] [SKU-substring-filter]
"""
import os, sys
from PIL import Image, ImageDraw
from generate_artwork import (AR, GOLD, GOLD_LT, W, H, vgrad, glow, rings,
                              center_text, font, colophon)

OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/huroof_batch1"

# palette: bg1, bg2, arabic, english, ring/glow, colophon, light?
PAL = {
    "FAM": ("#2A1016", "#160A0D", GOLD_LT, "#E8927C", "#E8927C", GOLD, False),
    "UAE": ("#06281A", "#02140D", GOLD_LT, "#7ED9A7", "#2EB872", GOLD, False),
    "CHI": ("#F7EFE2", "#EADCC3", "#1C3050", "#B0653A", "#C8A664", "#8B6B3A", True),
    "DIA": ("#0D0F2A", "#101C38", "#9FE8E2", GOLD_LT, "#4ECDC4", "#4ECDC4", False),
}

BATCH1 = [
    ("RL-FAM-001", "أمي حبي الأول", "My First Love"),
    ("RL-FAM-002", "بابا بطلي", "Dad, My Hero"),
    ("RL-FAM-003", "جدتي كنز", "Grandma Is a Treasure"),
    ("RL-FAM-004", "جدي حكايتي", "Grandpa Is My Story"),
    ("RL-FAM-005", "العائلة أولاً", "Family First"),
    ("RL-FAM-006", "أمي عالمي", "Mum Is My World"),
    ("RL-FAM-007", "أبي فخري", "Dad, My Pride"),
    ("RL-FAM-008", "بيت مليء بالحب", "A Home Full of Love"),
    ("RL-FAM-009", "قلوبنا معاً", "Together at Heart"),
    ("RL-FAM-010", "حب لا ينتهي", "Love Without End"),
    ("RL-UAE-001", "أهل الإمارات ولاء وانتماء", "United by Loyalty & Belonging"),
    ("RL-UAE-002", "الإمارات في القلب", "UAE in My Heart"),
    ("RL-UAE-003", "الإمارات بيتنا", "UAE Is Our Home"),
    ("RL-UAE-004", "نفخر بالإمارات", "Proud of the UAE"),
    ("RL-UAE-005", "الإمارات تجمعنا", "The UAE Brings Us Together"),
    ("RL-UAE-006", "وطن الطموح", "Nation of Ambition"),
    ("RL-UAE-007", "هنا نبني المستقبل", "Building Tomorrow Together"),
    ("RL-UAE-008", "بيت الفرص", "Home of Opportunity"),
    ("RL-CHI-001", "أسد", "Lion · Asad"),
    ("RL-CHI-002", "فيل", "Elephant · Feel"),
    ("RL-CHI-003", "زرافة", "Giraffe · Zarafa"),
    ("RL-CHI-004", "شمس", "Sun · Shams"),
    ("RL-CHI-005", "قمر", "Moon · Qamar"),
    ("RL-CHI-006", "تفاحة", "Apple · Tuffaha"),
    ("RL-CHI-007", "كتاب", "Book · Kitab"),
    ("RL-DIA-001", "قلبي عربي", "Arab Heart, Global Journey"),
    ("RL-DIA-002", "بين ثقافتين", "Proud of Both Worlds"),
    ("RL-DIA-003", "أحمل جذوري معي", "I Carry My Roots With Me"),
    ("RL-DIA-004", "هويتي قوتي", "My Identity Is My Strength"),
    ("RL-DIA-005", "من وطن إلى وطن", "From One Home to Another"),
]

_meas = ImageDraw.Draw(Image.new("RGB", (8, 8)))

def fit_font(text, fname, max_w, start, rtl=False):
    f = font(fname, start)
    w = _meas.textlength(text, font=f, **(AR if rtl else {}))
    if w > max_w:
        f = font(fname, max(80, int(start * max_w / w)))
    return f

def phrase_poster(sku, ar_text, en_text):
    bg1, bg2, c_ar, c_en, c_ring, c_colo, light = PAL[sku.split("-")[1]]
    img = vgrad(W, H, bg1, bg2).convert("RGBA")
    rings(img, W / 2, H * 0.44, c_ring, alpha=(40 if light else 24))
    glow(img, W / 2, H * 0.44, W * 0.40, c_ring, 28 if light else 48)
    d = ImageDraw.Draw(img)
    big = 1150 if len(ar_text) <= 6 else 800
    fA = fit_font(ar_text, "Amiri-Bold.ttf", W * 0.84, big, rtl=True)
    center_text(d, (W / 2, H * 0.42), ar_text, fA, c_ar, rtl=True)
    fE = fit_font(en_text, "CormorantGaramond[wght].ttf", W * 0.78, 230)
    center_text(d, (W / 2, H * 0.585), en_text, fE, c_en)
    colophon(img, fg=c_colo)
    return img

def make_pin(art, sku):
    pin = Image.new("RGB", (1000, 1500), "#08090F")
    pin.paste(art.convert("RGB").resize((1000, 1414)), (0, 0))
    d = ImageDraw.Draw(pin)
    d.rectangle([0, 1414, 1000, 1500], fill="#08090F")
    d.text((500, 1442), "Huroof حروف — Arabic Art",
           font=font("CormorantGaramond[wght].ttf", 44), fill=GOLD, anchor="mm")
    d.text((500, 1483), "Digital download & prints · huroof on Etsy",
           font=font("Inter[opsz,wght].ttf", 26), fill="#9aa", anchor="mm")
    return pin

if __name__ == "__main__":
    only = sys.argv[2] if len(sys.argv) > 2 else None
    for sub in ("print-files", "previews", "pins"):
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    for sku, a, e in BATCH1:
        if only and only not in sku:
            continue
        art = phrase_poster(sku, a, e)
        art.convert("RGB").save(f"{OUT}/print-files/{sku}-A2-300dpi.png", optimize=True)
        art.convert("RGB").resize((900, 1273)).save(f"{OUT}/previews/{sku}.jpg", quality=86)
        make_pin(art, sku).save(f"{OUT}/pins/{sku}-pin.png", optimize=True)
        print("done", sku)
