#!/usr/bin/env python3
"""Build a single master listing sheet for all SKUs (Payhip/Etsy paste source).

Generates docs/listings_master.csv with, per SKU: channel-ready Etsy title
(bilingual formula, <=140 chars), 13 tags, description, and the price ladder
from docs/UNIT_ECONOMICS.md. One source of truth for copy-paste or CSV import.
"""
import csv, os
from generate_batch1 import BATCH1  # 30 SKUs: (sku, arabic, english)

# 8 featured designs (sku, arabic, english, collection, base tag words)
FEATURED = [
    ("HRF-001", "بسم الله الرحمن الرحيم", "Bismillah Gold Navy", "Islamic", ["bismillah print", "islamic wall art", "thuluth", "quran wall art"]),
    ("HRF-002", "نجمة ثمانية الرؤوس", "Eight-Point Star", "Geometric", ["islamic geometric", "moroccan wall art", "sacred geometry", "arabesque print"]),
    ("HRF-003", "الصبر جميل", "Patience Is Beautiful — Sabr", "Quote", ["sabr print", "arabic quote", "patience quote", "islamic quote art"]),
    ("HRF-004", "رمضان كريم", "Ramadan Kareem Lantern", "Seasonal", ["ramadan decor", "ramadan kareem", "eid mubarak gift", "fanous lantern"]),
    ("HRF-005", "أرابيسك الأندلس", "Al-Andalus Arabesque", "Home", ["alhambra art", "arabesque panel", "moorish decor", "luxury wall art"]),
    ("HRF-006", "كثبان الصحراء", "Desert Dunes at Dusk", "Nature", ["desert wall art", "sahara print", "arabian landscape", "sunset print"]),
    ("HRF-007", "يا الله", "Ya Allah — Thuluth", "Islamic", ["ya allah print", "allah wall art", "thuluth calligraphy", "prayer room decor"]),
    ("HRF-008", "هذا أيضاً سيمضي", "This Too Shall Pass", "Quote", ["this too shall pass", "arabic quote print", "ruqaa calligraphy", "minimalist quote"]),
]

COLLECTION = {"FAM": "Family Gift", "UAE": "UAE Pride", "CHI": "Arabic Learning", "DIA": "Diaspora Identity"}
GENERIC_TAGS = ["arabic wall art", "islamic wall art", "printable art", "digital download",
                "arabic calligraphy", "muslim gift", "bilingual print", "eid gift idea",
                "islamic decor", "arabic art print", "ramadan gift", "muslim home decor"]
COMMON_TAGS = {
    "FAM": ["arabic gift", "muslim family gift", "bilingual print", "arabic wall art", "eid gift idea", "printable art", "digital download", "arabic calligraphy", "gift for parents"],
    "UAE": ["uae gift", "emirati pride", "national day gift", "arabic wall art", "bilingual print", "printable art", "digital download", "arabic calligraphy", "middle east decor"],
    "CHI": ["arabic for kids", "nursery wall art", "arabic learning", "bilingual print", "kids room decor", "printable art", "digital download", "educational print", "muslim kids gift"],
    "DIA": ["arab diaspora", "arabic identity", "bilingual print", "arabic wall art", "printable art", "digital download", "arabic calligraphy", "heritage gift", "arab pride"],
}

DESC = ("{en} — {ar}. An original bilingual Arabic–English design from Huroof. "
        "The Arabic is typeset from a classical Naskh typeface and checked for "
        "accuracy by a native reader. Available as an instant digital download "
        "(print at home up to A2, 300 DPI) or a premium print.\n\n"
        "This design was created by me using design tools from my own original "
        "concept. No physical item ships for the digital listing.\n\n"
        "© Huroof حروف — all rights reserved. This is an original artwork. Your "
        "purchase is a personal-use licence: print it for your own home or to "
        "give as a gift. Resale, redistribution, file-sharing, or any commercial "
        "use of the design is not permitted.\n\n"
        "Huroof حروف — Arabic art that speaks in two worlds.")

PRICES = {  # collection-default price ladder (GBP)
    "Islamic": (10, 25, 16, 22), "Geometric": (8, 25, 16, 22), "Quote": (7, 25, 16, 22),
    "Seasonal": (9, 25, 16, 22), "Home": (12, 28, 16, 22), "Nature": (8, 25, 16, 22),
    "Family Gift": (8, 25, 16, 22), "UAE Pride": (8, 25, 16, 22),
    "Arabic Learning": (7, 25, 16, 22), "Diaspora Identity": (8, 25, 16, 22),
}

def etsy_title(en, ar, coll):
    t = f"{en} Printable Wall Art, Arabic {coll} Digital Download, {ar}, Bilingual Arabic English Print"
    return t[:140]

def tags13(base, coll_key):
    out = []
    for t in list(base) + COMMON_TAGS.get(coll_key, []) + GENERIC_TAGS:
        if len(out) >= 13: break
        t = t.strip()
        if t and len(t) <= 20 and t not in out:  # Etsy: tags <= 20 chars
            out.append(t)
    return out

def rows():
    for sku, ar, en, coll, base in FEATURED:
        d, p, m, t = PRICES[coll]
        yield [sku, coll, en, ar, etsy_title(en, ar, coll),
               ", ".join(tags13(base, coll[:3].upper())), DESC.format(en=en, ar=ar),
               d, p, m, t]
    for sku, ar, en in BATCH1:
        key = sku.split("-")[1]
        coll = COLLECTION[key]
        d, p, m, t = PRICES[coll]
        base = [en.split(" · ")[0].lower() + " arabic", "arabic word art"]
        yield [sku, coll, en, ar, etsy_title(en, ar, coll),
               ", ".join(tags13(base, key)), DESC.format(en=en, ar=ar),
               d, p, m, t]

if __name__ == "__main__":
    os.makedirs("docs", exist_ok=True)
    path = "docs/listings_master.csv"
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["sku", "collection", "title_en", "title_ar", "etsy_title",
                    "tags_13", "description", "price_digital", "price_poster",
                    "price_mug", "price_tee"])
        n = 0
        for r in rows():
            w.writerow(r); n += 1
    print(f"wrote {n} listings -> {path}")
