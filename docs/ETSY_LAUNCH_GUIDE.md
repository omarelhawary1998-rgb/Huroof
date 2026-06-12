# Huroof — Etsy + Printful Launch Guide

The website is the shop window; Etsy is the till. Follow this top to bottom and you can open in one sitting (~2–3 hours). Only you can do steps 1–3 — they need your identity and bank details.

## Milestone 1 — Open the shop (you, ~30 min)

1. Go to https://www.etsy.com/sell → **Get started**.
2. Shop preferences: language English, country your country, currency GBP.
3. Shop name: try **Huroof**, then **HuroofStore**, **HuroofArt**, **HuroofDesigns** if taken.
4. Complete identity verification and add your bank account + billing card.
5. Etsy requires at least one listing to open — use the first listing from the kit below.

## Milestone 2 — Connect Printful (you, ~20 min)

1. Create a free account at https://www.printful.com.
2. Dashboard → **Stores** → **Connect** → choose **Etsy** and authorise.
3. In Printful, create each product (canvas, poster, framed print, mug, tote, t-shirt, phone case), upload the design art, set retail prices, and **push to Etsy**. Printful then auto-fulfils every Etsy order.

> You will need print-ready artwork (300 DPI PNG, sized to the largest print). The current site renders placeholder canvas art — generate/export the final designs (e.g. Midjourney upscales) before pushing products.

## Milestone 3 — Paste listings (copy from LISTING_KIT.md)

`docs/LISTING_KIT.md` has ready-to-paste titles, descriptions, 13 tags, and pricing for all 8 launch designs.

## Milestone 4 — Wire the website to the shop

1. Edit `index.html`, find `STORE CONFIG`, set:
   `const ETSY_SHOP_URL = 'https://www.etsy.com/shop/YOURSHOPNAME';`
2. Optionally set `NEWSLETTER_URL` to a free MailerLite/Tally signup form.
3. Commit and push — the site redeploys automatically.

## Milestone 5 — First-week marketing

- Submit the sitemap in Google Search Console (`sitemap.xml`).
- Create Pinterest + Instagram accounts; post each design with EN+AR captions.
- Etsy ads: optional £1–2/day on the two bestseller listings for initial traction.
- Time launches to the calendar: Ramadan/Eid windows drive most gift traffic.

## Alternatives if you don't want Etsy

| Option | Fees | Notes |
|---|---|---|
| Etsy + Printful | ~6.5% + listing 20¢ | Built-in buyer traffic — recommended to start |
| Shopify + Printful | £25/mo + 2% | Own brand, no marketplace traffic |
| Gumroad / Payhip (digital downloads) | ~10% / 5% | Sell the art as printable files — zero fulfilment, can run alongside Etsy |
