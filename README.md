# websiteplz.com

Static promo site for WebsitePlz (home, 5 trade pages, blog). No build tooling needed beyond Python 3.

- Edit prices / contact / checkout links in `CONFIG` at the top of `build.py`, then run `python3 build.py` (regenerates every page, sitemap.xml, robots.txt and the IndexNow key file).
- **Buy buttons:** `CONFIG["checkout_links"]` holds one URL per package (starter, emergency, emergency-care, care-monthly, care-quarterly, care-yearly). Empty = the button scrolls to the contact form with that package preselected.
- **Brand:** `img/logo.svg`, `img/logo-light.svg`, favicons and `img/og.png` (rendered from `tools/og.html`). `tools/brand.py` regenerates the logo/favicons. Fonts (Bricolage Grotesque + Inter, OFL) are self-hosted in `img/fonts/`.
- Portfolio screenshots `img/<slug>-desktop(-640).webp` / `-mobile.webp` come from `/workspace/emergency-site/shots/`.

## Contact form (`/api/contact`)
- `functions/api/contact.js` is a Cloudflare Pages Function. It validates input, has a honeypot (`company_fax`), a 3-second time trap and a rate limit (5 per 10 min per IP; per-isolate unless a `RATE_KV` KV binding is added).
- Delivery uses the first binding that exists: `MAILER` (Service binding to the `websiteplz-contact-mailer` Worker in `workers/contact-mailer/`, which emails `printplzeverything@gmail.com` from `form@websiteplz.com` via Email Routing `send_email`), else `SUBMISSIONS` (KV, stores JSON). With neither, the API returns 503 and the page tells visitors to email hello@websiteplz.com instead.
- Pages Functions can't use `send_email` directly, which is why a separate Worker is needed.
- **Not set up yet.** To turn it on: (1) a token with **Workers Scripts Edit** (and Email Routing enabled on websiteplz.com, already on); `cd workers/contact-mailer && npx -y wrangler@3 deploy`; (2) in Pages project `websiteplz` > Settings > Bindings, add Service binding `MAILER` -> `websiteplz-contact-mailer` (production), then redeploy. KV alternative: needs **Workers KV Storage Edit** to create a namespace, then bind it as `SUBMISSIONS`.
- `wrangler pages deploy` picks up `functions/` from its working directory; `tools/deploy.sh` copies it into /tmp/wplzproj.
- `_headers` / `_redirects` are for Cloudflare Pages (ignored by GitHub Pages).
- Preview: GitHub Pages. Production: Cloudflare Pages on websiteplz.com.

## Cloudflare Pages (production) - LIVE via Direct Upload
- Project: `websiteplz` (https://websiteplz.pages.dev), account 4003c9642a148a5b37a27b76397886ce.
- Custom domains: websiteplz.com, www.websiteplz.com (proxied CNAMEs -> websiteplz.pages.dev; apex is CNAME-flattened).
- Redirect rules (Single Redirects): www.websiteplz.com -> https://websiteplz.com{path} 301 (query kept; /.well-known/ excluded so Pages SSL validation works);
  sitesplz.com + www.sitesplz.com (proxied placeholder A @ 192.0.2.1, CNAME www -> sitesplz.com) -> https://websiteplz.com{path} 301 (query kept).

### Redeploy
Wrangler 4 needs Node >= 22; on this box (Node 20) use wrangler@3. Running wrangler from this folder fails with
EACCES on /node_modules/.cache, so `tools/deploy.sh` builds, then deploys from a scratch project in /tmp/wplzproj
(empty node_modules/, a copy of functions/, public files in dist/):
```bash
cd /workspace/websiteplz-site && tools/deploy.sh      # needs CLOUDFLARE_API_TOKEN (Pages Edit) in env
python3 tools/indexnow.py                              # ping Bing/Yandex via IndexNow (key file /<key>.txt)
git add -A && git commit -m "update" && git push       # keeps GitHub in sync (GitHub Pages preview)
```
When adding a new top-level page folder, add it to the `cp` list in `tools/deploy.sh`.

### Caching
`/img/*` used to be cached for a year (`immutable`) and Cloudflare's edge kept old images. build.py now appends
`?v=<content hash>` to every local CSS/image/font URL (and to the font URLs inside styles.css), so a deploy always
serves fresh assets. The token can't purge cache (no Cache Purge permission).

## Pages and SEO
- `/` home (trade chooser + general sales), `/hvac/`, `/plumbing/`, `/electrical/` (uses the Ridge Line demo, labeled),
  `/pressure-washing/`, `/cleaning/`, `/blog/` + one article per trade. Trade copy: `content/trades.py`;
  articles: `content/blog.py` + `content/blog/<slug>.html`.
- Every page is indexable (only 404.html is noindex). robots.txt allows all and lists the sitemap; sitemap.xml
  lists every page with lastmod (`CONFIG["published"]`). Canonicals are absolute https://websiteplz.com/ URLs.
- JSON-LD: Organization, WebSite, ProfessionalService (no address/phone) and FAQPage on home; Service, FAQPage,
  BreadcrumbList on trade pages; Blog and BlogPosting on the blog.
- IndexNow key is `CONFIG["indexnow_key"]`; build.py writes `/<key>.txt`.
- Google Search Console: add a **Domain** property for websiteplz.com in Google's account, copy the TXT value,
  add it as a TXT record on the apex (`@`) of the websiteplz.com zone in Cloudflare DNS, verify, then submit
  `https://websiteplz.com/sitemap.xml` under Sitemaps.

## Three paths on every page
Buy now (CONFIG `checkout_links`; empty = contact form with the package preselected), Get a free mockup
(`#mockup` form, `type=mockup`), Ask a question (`#contact` form, `type=contact`). Both forms post to `/api/contact`.
