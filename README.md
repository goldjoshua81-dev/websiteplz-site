# websiteplz.com

Static single-page promo site for WebsitePlz. No build tooling needed beyond Python 3.

- Edit prices / contact in `CONFIG` at the top of `build.py`, then run `python3 build.py` (regenerates `index.html`).
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
(build.py, README.md and preview*.png are intentionally not uploaded.)
