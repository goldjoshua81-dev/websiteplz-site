# Private mockups (/m/<slug>/)

One JSON file per prospect. `python3 build.py` builds `/m/<slug>/` for every JSON whose `created` date is
within `CONFIG["mockup_days"]` (14) days, and deletes `m/<slug>/` folders that are expired or have no JSON.
Pages are noindex/nofollow, `Referrer-Policy: no-referrer`, kept out of sitemap.xml and disallowed in robots.txt.

**Privacy:** real prospect JSON and images are git-ignored (the GitHub repo is public). Only `_sample-*.json`
and `img/sample-*` are committed. The `m/` output folder is git-ignored too; it exists only in deploys.

New mockup:
```bash
python3 -c "import build; print(build.mock_slug('Acme Plumbing'))"   # unguessable slug
```
```json
{"slug": "acme-plumbing-k7q2xm", "business": "Acme Plumbing", "trade": "plumbing", "city": "Tulsa, OK",
 "contact_name": "Sam", "images": {"desktop": "img/acme-desktop.webp", "mobile": "img/acme-mobile.webp"},
 "before": "", "video_url": "", "created": "2026-10-05"}
```
- `images` paths are relative to this folder (put files in `content/mockups/img/`). Desktop 1200x791, mobile 390x844 webp.
- `before`: optional real screenshot of their current site/listing (never a made-up one), e.g. `img/acme-before.webp`.
- `video_url`: optional Loom link (opens in a new tab; no iframes).
- `trade`: hvac, plumbing, electrical, pressure-washing or cleaning (cleaning and pressure washing get Booking-ready names).
- Then `tools/deploy.sh`. The link is `https://websiteplz.com/m/<slug>/`.
