# Huroof حروف — Arabic Art & Design Store

A bilingual (English/Arabic) storefront for original Arabic calligraphy, Islamic geometric prints, and seasonal gifts — print-on-demand via Printful, sold via Etsy.

**Live site:** https://omarelhawary1998-rgb.github.io/Huroof/

> 🆕 **New here? Read [`docs/START_HERE.md`](docs/START_HERE.md)** — the plain-language, click-by-click guide to getting products live and selling.
> Setting up the brand's accounts? Use [`docs/SOCIAL_PROFILES.md`](docs/SOCIAL_PROFILES.md) (paste-ready bios) + [`docs/SOCIAL_SETUP_GUIDE.md`](docs/SOCIAL_SETUP_GUIDE.md) (click-by-click).

## Stack

Single static page (`index.html`) — no build step, no dependencies. Product art is rendered client-side on `<canvas>`. Cart persists in `localStorage`.

## Deployment

Pushes to the deploy branches trigger `.github/workflows/deploy.yml`, which publishes the repo root to GitHub Pages. If the first run fails with a Pages error, enable **Settings → Pages → Source: GitHub Actions** once and re-run.

## Go-live checklist

- [ ] Follow `docs/ETSY_LAUNCH_GUIDE.md` — digital downloads first, then prints (Prodigi for wall art, Printful for mugs/tees).
- [ ] Price strictly per `docs/UNIT_ECONOMICS.md`; listing copy in `docs/LISTING_KIT.md`.
- [ ] Paste the shop URL into `ETSY_SHOP_URL` in `index.html` (search for `STORE CONFIG`).
- [ ] Optionally set `NEWSLETTER_URL` (MailerLite / Substack / Tally form).
- [ ] If you buy a custom domain (e.g. huroof.co), update the URLs in `index.html`, `sitemap.xml`, and `robots.txt`, and add a `CNAME` file.
- [ ] Submit `sitemap.xml` to Google Search Console.

Compliance rule baked into everything: no fabricated reviews, ratings, or stats anywhere (UK DMCC Act / US FTC rule), AI assistance always disclosed, and every Arabic design checked by a native reader before sale.
