# websiteplz.com

Static single-page promo site for WebsitePlz. No build tooling needed beyond Python 3.

- Edit prices / contact in `CONFIG` at the top of `build.py`, then run `python3 build.py` (regenerates `index.html`).
- `_headers` / `_redirects` are for Cloudflare Pages (ignored by GitHub Pages).
- Preview: GitHub Pages. Production: Cloudflare Pages on websiteplz.com.

## Cloudflare Pages (production)
1. Cloudflare dashboard > Workers & Pages > Create > Pages > Connect to Git > pick `goldjoshua81-dev/websiteplz-site`.
   Framework preset: None. Build command: (empty). Output directory: `/`.
2. Project > Custom domains > add `websiteplz.com` and `www.websiteplz.com` (zone is on the same account, so DNS records are created automatically).
3. www -> apex: Rules > Redirect Rules on the websiteplz.com zone: if hostname equals `www.websiteplz.com`, 301 to `https://websiteplz.com${uri}` (dynamic, preserve query string).

## sitesplz.com -> websiteplz.com
On the sitesplz.com zone: add proxied DNS records (A `@` 192.0.2.1 and CNAME `www` -> `sitesplz.com`, both orange-cloud; placeholder IP is never reached) then a Redirect Rule: "All incoming requests" -> dynamic 301 to `concat("https://websiteplz.com", http.request.uri.path)`, preserve query string. (Or use a Bulk Redirect list.)
