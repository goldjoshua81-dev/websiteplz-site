# websiteplz.com

Static promo site for WebsitePlz (home, 5 trade pages, blog). No build tooling needed beyond Python 3.

- Edit prices / contact / checkout links in `CONFIG` at the top of `build.py`, then run `python3 build.py` (regenerates every page, sitemap.xml, robots.txt and the IndexNow key file).
- **Buy buttons:** `CONFIG["checkout_links"]` holds one URL per package (starter, emergency, emergency-care, care-monthly, care-quarterly, care-yearly). Empty = "Buy now" scrolls to the contact form with that package preselected; set = "Pay $X to start".
- **Brand:** `img/logo.svg`, `img/logo-light.svg`, favicons and `img/og.png` (rendered from `tools/og.html`). `tools/brand.py` regenerates the logo/favicons. Fonts (Bricolage Grotesque + Inter, OFL) are self-hosted in `img/fonts/`.
- Portfolio screenshots `img/<slug>-desktop(-640).webp` / `-mobile.webp` come from `/workspace/emergency-site/shots/`.

## Upgrade (Oct 4, 2026): offer, guarantee, mockups, legal pages
Built from `/workspace/emergency-site/upgrade_build_list.md`. Pricing is still in `CONFIG` only:
- 50% deposit (`deposit_pct`) shown on every card ("Pay $124.50 today, $124.50 at launch"); badge text `featured_label`;
  the $1,495 bundle has `care_months: 6` and its "Saves $224" line is computed (site + 6 x Monthly Care - bundle).
- New pages: `/terms/`, `/privacy/`, `/refunds/` (in sitemap), `/guides/google-business-profile-checklist/` (in sitemap),
  `/thanks/mockup/`, `/thanks/order/` and `/m/<slug>/` (noindex, nofollow, no-referrer, not in sitemap, disallowed in robots.txt).
- JavaScript beyond the inline form script lives in `/js/` (`calc.js`, `mockup.js`, `print.js`), allowed by CSP `script-src 'self'`.
  The inline form script's sha256 is recomputed into `_headers` on every build.
- Private mockups: see `content/mockups/README.md`. Prospect JSON/images and the `m/` output are git-ignored (public repo).
- Manual steps (mockup SOP, email templates, launch checklist): `docs/playbook.md`.

### ⚠️ Legal wording needs Joshua's review (BL-8)
`/terms/`, `/privacy/` and `/refunds/` are plain-English drafts written from the build list. **Joshua must review the wording
before Stripe goes live** (Stripe's terms checkbox will point at `/terms/`). Defaults used, pending confirmation (BL-10):
"5 days" = 5 calendar days from the last checklist item; Annual Refresh doesn't auto-renew. Also check: refund timing
("within 2 business days"), the Stripe customer-portal cancellation line, and the data-deletion line in Privacy.

### Switching on the blocked items
| Item | What Joshua provides | How to switch it on |
|---|---|---|
| Form delivery (BL-1, M-1) | Token with **Workers Scripts Edit** (+ Pages binding edit) | Deploy `workers/contact-mailer` (`cd workers/contact-mailer && npx -y wrangler@3 deploy`), add Service binding `MAILER` -> `websiteplz-contact-mailer` in Pages > Settings > Bindings, then set `CONFIG["form_delivery_live"] = True` and run `tools/deploy.sh`. Until then forms skip the network call and offer the prefilled email (no 503 errors). Successful mockup requests then redirect to `/thanks/mockup/`. |
| Stripe (BL-2, PP-3) | 3 deposit Payment Links ($124.50 / $562.50 / $747.50), 3 Care links (Annual as a one-time $990), customer portal, Terms URL `https://websiteplz.com/terms/`, success URL `https://websiteplz.com/thanks/order/` | Paste URLs into `CONFIG["checkout_links"]`. Site-package buttons become "Pay $X to start" (same tab), Care buttons open their links, and `/m/` "Make it live" buttons go to Stripe instead of a prefilled email. Don't go live before the legal pages are approved. |
| P.O. box (BL-3) | Mailing address | `CONFIG["postal_address"] = "..."` (shows in the footer). Then emails 3–5 in `docs/playbook.md` can be sent. |
| Founder photo (BL-4) | Real square photo, 600px+ | Save as `img/joshua.jpg`, set `CONFIG["founder_photo"] = "img/joshua.jpg"`. Until then the founder block is text-only (no stock or AI image). |
| Intro video (BL-5) | 60-second-or-shorter video link | `CONFIG["founder_video_url"] = "https://..."` (link opens in a new tab; no iframes, CSP has no frame-src). |
| Mockup walkthroughs (BL-6) | Loom account | Put the link in the mockup JSON `video_url`. |
| Fiverr/Contra (BL-11, GR-7) | Profile URLs | `CONFIG["fiverr_url"]`, `CONFIG["contra_url"]` (footer + forms show the links). |
| Visitor auto-reply (BL-7, M-6) | Workers Paid + Cloudflare Email Service | Copy is in `docs/playbook.md`; not built. |

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
- Every public page is indexable (404.html, /thanks/* and /m/* are noindex). robots.txt allows all and lists the sitemap; sitemap.xml
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
