# Etsy Fix Sheet — copy-paste, minimal effort

Etsy can't be edited by CSV import, so these are paste-ready blocks for the
Etsy UI. Do the **CRITICAL** section first (5 min); the rest is optional polish.

To edit a listing: Shop Manager → Listings → click the listing → Edit.

---

## 🔴 CRITICAL (5 min) — add the 13 tags to the 3 UAE listings
These 3 have ZERO tags = invisible in Etsy search. Tags are the whole game.

**Same 13 tags for all three** (Etsy: type each into a tag box, ≤20 chars):
```
arabic word art, uae gift, emirati pride, national day gift, arabic wall art, bilingual print, printable art, digital download, arabic calligraphy, middle east decor, islamic wall art, muslim gift, eid gift idea
```
Apply to:
- "UAE , Bilingual Home Pride Print" (UAE Is Our Home)
- "UAE , Loyalty Belonging Print" (United by Loyalty)
- "UAE , Bilingual Wall Art" (The UAE Brings Us Together)

That alone makes those 3 findable. Everything below is optional improvement.

---

## ⚠️ OPTIONAL polish — better titles for those 3 UAE listings
Etsy ranks on title keywords. Replace the vague titles with these:

**UAE Is Our Home:**
```
UAE Is Our Home Printable Wall Art, Arabic UAE Pride Digital Download, الإِمَارَاتُ بَيْتُنَا, Bilingual Arabic English Print
```
**United by Loyalty & Belonging:**
```
United by Loyalty & Belonging Printable Wall Art, Arabic UAE Pride Digital Download, أهل الإمارات ولاء وانتماء, Bilingual Arabic
```
**The UAE Brings Us Together:**
```
The UAE Brings Us Together Printable Wall Art, Arabic UAE Pride Digital Download, الإمارات تجمعنا, Bilingual Arabic English Print
```

---

## ⚠️ OPTIONAL — add the © licence line to all 6 descriptions
Paste at the end of each listing's description:
```
© Huroof حروف — all rights reserved. This is an original artwork. Your purchase is a personal-use licence: print it for your own home or to give as a gift. Resale, redistribution, file-sharing, or any commercial use of the design is not permitted.
```
Also tick the **"Made with the help of AI tools"** attribute on each listing
(Etsy → Edit listing → "Details" → AI usage). Same disclosure rule as everywhere.

---

## ℹ️ Consistency note
- Prices already match across Etsy = Payhip = Website. ✅ No change needed.
- "The UAE Brings Us Together" is on Etsy but not yet on Payhip/website — list
  it on Payhip too (file RL-UAE-005) when you reach the UAE batch, for full parity.

---

## 14 designs not yet on Etsy
When you want full parity, list these from `docs/listings_master.csv`
(it already has the correct etsy_title, 13 tags, and description with the
licence line for every SKU): the 8 core except those listed, the 7 kids,
the remaining Family/UAE/Diaspora. Copy each row's `etsy_title`, `tags_13`,
and `description` straight in.
