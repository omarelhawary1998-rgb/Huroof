# Huroof — Growth Playbook (the production system, made compliant)

This adapts the "AI POD factory" model (Claude → image AI → Canva → POD partner → Etsy → social traffic) to what Etsy actually allows in 2026 and to our verified margins. The original model's core insight is right — **the asset is the system, not any single design** — but two of its tactics (mass template listing, apparel-led catalog) would get the shop suspended or keep it unprofitable. This version keeps the engine and fixes the fuel.

## 1. The production line (weekly batch cadence)

| Stage | Tool | Output | Compliance gate |
|---|---|---|---|
| Phrase & keyword research | Claude / eRank free tier | 10 candidate phrases + Etsy tags | No trademark phrases; no Quranic verses via AI |
| Visual generation | Midjourney/DALL·E from YOUR OWN prompts | Draft art | Own prompts only — bought prompt packs are banned by Etsy (June 2025) |
| Refinement | Canva / vector editor | 300 DPI, A2-size masters; Arabic re-typeset from proper fonts | **Native Arabic reader signs off every letterform** |
| Listing | Etsy (digital first) | Digital download + poster/mug variants | AI disclosure line in description; "Designed by" category |
| Traffic | Pinterest (priority), IG/TikTok reels, CapCut | 3–5 pins + 1 reel per design | Process clips double as authenticity proof |
| Feedback | Etsy stats → next batch | Double down on winners only | Kill listings with 0 favourites after 60 days |

**Batch rule:** produce in batches of 5–10, but make each listing *meaningfully distinct* (different phrase, composition, colourway story). Etsy's enforcement explicitly targets bulk near-duplicate uploads — 500 template clones is the 2023 playbook and it now ends in suspension, not sales.

## 2. Scaling stages (gated, not blind)

| Stage | Listings | Gate to advance |
|---|---|---|
| 1. Test | 10–20 (8 designs × digital + best physical) | 20 genuine sales/reviews |
| 2. Identify winners | 30–50 | 3+ designs with repeat sales; ≥4.8 rating held |
| 3. Exploit winners | 60–100 | Variations + **personalised versions** of winners only (custom name calligraphy — the highest-converting format on Etsy) |
| 4. Brand | own-site sales > 25% of revenue | Consider Shopify/wider catalog |

Income reality check (the ChatGPT conversation agrees with our data): most shops earn £0–100/month; the gates exist so we only spend effort past stage 1 if the market says yes.

## 3. Beating the fee stack (the "Etsy is expensive" answer)

Etsy's take on an organic UK sale is ~12% + £0.35 (incl. VAT on fees) — and ~27% if an Offsite Ad gets credit. You cannot negotiate it, but you can route around it:

| Channel | Approx. fees on a £10 digital sale | Net |
|---|---|---|
| Etsy (organic) | ~£1.55 | ~£8.45 |
| Etsy (Offsite-Ads attributed) | ~£3.35 | ~£6.65 |
| **Payhip free plan (direct)** | ~5% + card processing ≈ £0.80–£1.00 | **~£9.00+** |
| Gumroad (direct) | ~10% + processing | ~£8.60 |

*(Verify current rates at signup — fee schedules change.)*

The play:
1. **Opt out of Offsite Ads** on day one (Settings → Offsite Ads) while under $10k/yr.
2. **Open a free Payhip store** for the digital downloads and paste its URL into `DIRECT_STORE_URL` in `index.html` — the site then shows a "Buy direct" button on every product. Payhip acts as merchant of record and handles UK/EU VAT on digital sales for you.
3. **Routing rule:** Etsy listings serve *search traffic* (people who found you on Etsy — its fee buys that discovery). All traffic YOU generate (Pinterest, IG/TikTok, the website, email list) goes to the direct store — why pay Etsy 12% for a customer Etsy didn't bring?
4. **Raise average order value:** bundles (sets of 3 digital prints; gallery poster sets) amortise fixed fees; on Printful, a second poster in the same order ships for $0.30.
5. **List in GBP with a GBP bank account** (avoids Etsy's 2.5% currency conversion fee).

## 4. Direct-sales legal checklist (selling off-Etsy)

- Display business identity and a contact route on the site (UK Consumer Contracts Regulations / E-Commerce Regulations).
- Publish simple Terms, Privacy, and Refund pages (Payhip provides templates; digital downloads: state clearly that the right to cancel lapses once the download starts, with consumer consent at checkout).
- Personal-use licence statement on digital files (already in the listing kit).
- Same review rules as everywhere: no fabricated reviews or ratings, ever (UK DMCC Act / US FTC rule).
- Keep records of sales for income tax; UK trading allowance covers the first £1,000 of gross trading income, then self-assessment registration is required.

## 5. What we deliberately did NOT adopt from the source plan

- **200–500 listing target** → replaced with gated scaling (Section 2). Listing fees alone on 500 items = ~$100/cycle for mostly invisible listings, and bulk-similar uploads trigger Etsy's Creativity Standards enforcement.
- **"Template reuse" as a product strategy** → templates are fine as *internal* production scaffolding; listings built on purchased/shared templates are banned (June 2025 policy).
- **Apparel-led catalog** → digital-led (≈80% margin vs ≈17–28% on tees). Tees remain as upsells on proven phrases.
- **"Passive income" framing** → the source conversation itself concedes POD isn't passive early; budget 4–6 focused hours/week for the batch cadence.
