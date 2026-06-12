# Huroof حروف — Arabic Art & Design Store

A bilingual (English/Arabic) storefront for original Arabic calligraphy, Islamic geometric prints, and seasonal gifts — print-on-demand via Printful, sold via Etsy.

**Live site:** https://omarelhawary1998-rgb.github.io/Huroof/

## Stack

Single static page (`index.html`) — no build step, no dependencies. Product art is rendered client-side on `<canvas>`. Cart persists in `localStorage`.

## Deployment

Pushes to the deploy branches trigger `.github/workflows/deploy.yml`, which publishes the repo root to GitHub Pages. If the first run fails with a Pages error, enable **Settings → Pages → Source: GitHub Actions** once and re-run.

## Go-live checklist

- [ ] Create your Etsy shop and connect Printful.
- [ ] Paste the shop URL into `ETSY_SHOP_URL` in `index.html` (search for `STORE CONFIG`).
- [ ] Optionally set `NEWSLETTER_URL` (MailerLite / Substack / Tally form).
- [ ] If you buy a custom domain (e.g. huroof.co), update the URLs in `index.html`, `sitemap.xml`, and `robots.txt`, and add a `CNAME` file.
- [ ] Submit `sitemap.xml` to Google Search Console.
