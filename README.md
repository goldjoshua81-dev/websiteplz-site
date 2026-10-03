# websiteplz.com

Static single-page promo site for WebsitePlz. No build tooling needed beyond Python 3.

- Edit prices / contact / checkout links in `CONFIG` at the top of `build.py`, then run `python3 build.py` (regenerates `index.html`).
- **Buy buttons:** `CONFIG["checkout_links"]` holds one URL per package (starter, emergency, emergency-care, care-monthly, care-quarterly, care-yearly). Empty = the button scrolls to the contact form with that package preselected, and a "checkout coming soon" note shows under Pricing.
- **Brand:** `img/logo.svg`, `img/logo-light.svg`, favicons and `img/og.png` (rendered from `tools/og.html`). `tools/brand.py` regenerates the logo/favicons. Fonts (Bricolage Grotesque + Inter, OFL) are self-hosted in `img/fonts/`.
- Portfolio screenshots `img/<slug>-desktop(-640).webp` / `-mobile.webp` come from `/workspace/emergency-site/shots/`.

## Contact form (`/api/contact`)
- `functions/api/contact.js` is a Cloudflare Pages Function. It validates input, has a honeypot (`company_fax`), a 3-second time trap and a rate limit (5 per 10 min per IP; per-isolate unless a `RATE_KV` KV binding is added).
- Delivery uses the first binding that exists: `MAILER` (Service binding to the `websiteplz-contact-mailer` Worker in `workers/contact-mailer/`, which emails `printplzeverything@gmail.com` from `form@websiteplz.com` via Email Routing `send_email`), else `SUBMISSIONS` (KV, stores JSON). With neither, the API returns 503 and the page tells visitors to email hello@websiteplz.com instead.
- Pages Functions can't use `send_email` directly, which is why a separate Worker is needed.
- **Not set up yet.** To turn it on: (1) a token with **Workers Scripts Edit** (and Email Routing enabled on websiteplz.com, already on); `cd workers/contact-mailer && npx -y wrangler@3 deploy`; (2) in Pages project `websiteplz` > Settings > Bindings, add Service binding `MAILER` -> `websiteplz-contact-mailer` (production), then redeploy. KV alternative: needs **Workers KV Storage Edit** to create a namespace, then bind it as `SUBMISSIONS`.
- `wrangler pages deploy` picks up `functions/` from the current directory, so run the deploy from this folder (as below).
- `_headers` / `_redirects` are for Cloudflare Pages (ignored by GitHub Pages).
- Preview: GitHub Pages. Production: Cloudflare Pages on websiteplz.com.

## Cloudflare Pages (production) - LIVE via Direct Upload
- Project: `websiteplz` (https://websiteplz.pages.dev), account 4003c9642a148a5b37a27b76397886ce.
- Custom domains: websiteplz.com, www.websiteplz.com (proxied CNAMEs -> websiteplz.pages.dev; apex is CNAME-flattened).
- Redirect rules (Single Redirects): www.websiteplz.com -> https://websiteplz.com{path} 301 (query kept; /.well-known/ excluded so Pages SSL validation works);
  sitesplz.com + www.sitesplz.com (proxied placeholder A @ 192.0.2.1, CNAME www -> sitesplz.com) -> https://websiteplz.com{path} 301 (query kept).

### Redeploy
Wrangler 4 needs Node >= 22; on this box (Node 20) use wrangler@3.
```bash
cd /workspace/websiteplz-site && python3 build.py
rm -rf /tmp/wplz-dist && mkdir /tmp/wplz-dist
cp -r 404.html _headers _redirects apple-touch-icon.png favicon.ico favicon.svg img index.html robots.txt site.webmanifest sitemap.xml styles.css /tmp/wplz-dist/
# needs CLOUDFLARE_API_TOKEN (Pages Edit) in env
CLOUDFLARE_ACCOUNT_ID=4003c9642a148a5b37a27b76397886ce npx -y wrangler@3 pages deploy /tmp/wplz-dist --project-name websiteplz --branch main --commit-dirty=true
git add -A && git commit -m "update" && git push   # keeps the GitHub repo in sync (GitHub Pages preview)
```
(build.py, README.md, tools/, workers/ and preview*.png are intentionally not uploaded; functions/ is compiled by wrangler from the cwd.)
