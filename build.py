#!/usr/bin/env python3
"""Build index.html for websiteplz.com.

EDIT PRICES AND CONTACT HERE ONLY. Then run:  python3 build.py
Every price on the page (hero, pricing, care plans, FAQ, JSON-LD) is rendered
from CONFIG below, so nothing else needs touching.
"""
import html, json, pathlib

CONFIG = {
    "site_url": "https://websiteplz.com/",
    # --- PRICING: approved by Joshua Oct 3, 2026 -----------------------------
    "tiers": [
        {"id": "starter", "name": "Starter Page", "price": 249, "featured": False,
         "blurb": "Get online fast with a clean, phone-first page.",
         "items": ["One-page site on your domain", "Your logo, phone and cities",
                   "2 of your photos", "Click-to-call button", "Quote form",
                   "1 revision round", "Live 5 days after assets arrive"]},
        {"id": "emergency", "name": "Emergency-ready Site", "price": 1125, "featured": True,
         "blurb": "The full page built to turn visitors into calls.",
         "items": ["Everything in Starter", "Sticky call bar that stays on screen",
                   "4 of your photos", "Your 3 main services", "Reviews section",
                   "Financing line + license & insured line", "Quote / book form",
                   "2 revision rounds", "Live 5 days after assets arrive"]},
        {"id": "emergency-care", "name": "Emergency-ready + 3 Months Care", "price": 1495, "featured": False,
         "blurb": "The full site, plus we look after it for 3 months.",
         "items": ["Everything in Emergency-ready", "3 months of hosting included",
                   "2 small edits a month", "Monthly call-button and form test",
                   "Then Monthly Care at {care_monthly}/mo, optional"]},
    ],
    "care": {"monthly": 99, "quarterly": 249, "yearly": 990},
    # --- CONTACT (TODO: nothing confirmed yet) ------------------------------
    # TODO: replace with a real, working inbox before launch. Not set up yet.
    "contact_email": "hello@websiteplz.com",
    # TODO: paste profile URLs once Joshua's accounts exist; empty = hidden.
    "fiverr_url": "",
    "contra_url": "",
    # --- CHECKOUT (payment provider TBD) -------------------------------------
    # Paste a checkout URL (Stripe Payment Link, Square, PayPal...) per package.
    # Empty = the Buy button scrolls to the contact form with that package preselected.
    "checkout_links": {
        "starter": "",
        "emergency": "",
        "emergency-care": "",
        "care-monthly": "",
        "care-quarterly": "",
        "care-yearly": "",
    },
    # Contact form posts here (Cloudflare Pages Function: functions/api/contact.js).
    "form_endpoint": "/api/contact",
    "samples_base": "https://goldjoshua81-dev.github.io/contractor-samples/",
}

def money(n): return f"${n:,}"
C = CONFIG
care = C["care"]
care_m, care_q, care_y = care["monthly"], care["quarterly"], care["yearly"]
q_per_mo = round(care_q / 3)
y_save = care_m * 12 - care_y
y_pct = round(100 * y_save / (care_m * 12))
lowest = min(t["price"] for t in C["tiers"])
e = html.escape

SAMPLES = [
    ("ridgeline", "Ridge Line Heating &amp; Air", "HVAC"),
    ("stonecreek-plumbing", "Stone Creek Plumbing Co.", "Plumbing"),
    ("loneoak-pressure-washing", "Lone Oak Pressure Washing", "Pressure washing"),
    ("tidypine-cleaning", "Tidy Pine Home Cleaning", "House cleaning"),
]

FAQ = [
    ("How fast is it?", "Your site is live 5 days after you send your logo, phone number, cities and photos. The clock starts when your assets arrive."),
    ("Do I need a domain?", "Yes. The site goes on your own domain (about $15 a year), which you pay for and own. We walk you through connecting it."),
    ("Can you use my Facebook photos and reviews?", "Yes, as long as they're yours. Real reviews only."),
    ("Is it WordPress?", "No. It's a hand-built static page: faster, with no plugins to update and far less that can break or get hacked."),
    ("Are there monthly fees?", f"Only if you want Care. Monthly Care is {money(care_m)}/mo for hosting plus 2 small edits a month. Without Care, we hand the site off to your own host."),
    ("How many revisions do I get?", "Starter includes 1 round, the other packages include 2. A revision is a change to what's on the page, not a new design."),
    ("Do you do SEO or ads?", "No. This is a fast, honest page that turns visitors into calls. Your Google Business Profile and ads send the traffic."),
    ("What counts as a small edit?", "Anything that takes 15 minutes or less: text, hours, a price or a photo swap. Bigger changes are quoted separately, and unused edits don't roll over."),
    ("Who owns the site?", "You do. You own your domain, your content and the final page files once paid in full."),
]

ICONS = {
 "flame": '<path d="M12 3c.5 3.2 4.5 5.4 4.5 9.6A4.5 4.5 0 0 1 12 17a4.5 4.5 0 0 1-4.5-4.4c0-1.8.9-3.1 2-4 .1 1.6.9 2.6 1.9 2.9C11 9 11.2 5.6 12 3Z"/><path d="M5 21h14"/>',
 "drop": '<path d="M12 3.5s6 6.4 6 10.6a6 6 0 0 1-12 0C6 9.9 12 3.5 12 3.5Z"/><path d="M9.2 14.6a2.9 2.9 0 0 0 2.6 2.6"/>',
 "bolt": '<path d="M13 3 5 13.5h6L10 21l8-10.5h-6L13 3Z"/>',
 "spray": '<path d="M4 20 13.5 10.5"/><path d="M12 8.5l3.5 3.5 2.5-2.5-3.5-3.5Z"/><path d="M18 4.5h.01M20.5 7h.01M21 3.5h.01M17.2 2.3h.01"/>',
 "sparkle": '<path d="M12 3.5 13.8 9 19.5 10.8 13.8 12.6 12 18.3 10.2 12.6 4.5 10.8 10.2 9Z"/><path d="M19 16.5v4M17 18.5h4"/>',
 "phone": '<path d="M6.6 3.5h2.6l1.4 4-2 1.4a12 12 0 0 0 6.5 6.5l1.4-2 4 1.4v2.6a2 2 0 0 1-2.2 2A16.5 16.5 0 0 1 4.6 5.7a2 2 0 0 1 2-2.2Z"/>',
 "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "pin": '<path d="M12 21s7-6.2 7-11.5a7 7 0 0 0-14 0C5 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/>',
 "star": '<path d="m12 3.8 2.5 5.2 5.7.8-4.1 4 1 5.6L12 16.7l-5.1 2.7 1-5.6-4.1-4 5.7-.8Z"/>',
 "form": '<rect x="4.5" y="3.5" width="15" height="17" rx="2.5"/><path d="M8 8.5h8M8 12h8M8 15.5h4.5"/>',
 "shield": '<path d="M12 3.5 19 6v5.6c0 4.4-3 7.6-7 8.9-4-1.3-7-4.5-7-8.9V6Z"/><path d="m9 12 2.2 2.2L15.3 10"/>',
 "gauge": '<path d="M4.5 16.5a8 8 0 1 1 15 0"/><path d="m12 13 4-4"/><circle cx="12" cy="13.5" r="1.3"/>',
 "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.4 2.5 3.5 5.3 3.5 8.5s-1.1 6-3.5 8.5c-2.4-2.5-3.5-5.3-3.5-8.5S9.6 6 12 3.5Z"/>',
 "image": '<rect x="3.5" y="5" width="17" height="14" rx="2.5"/><circle cx="9" cy="10" r="1.7"/><path d="m20.5 16-4.5-4.5L7 19"/>',
 "list": '<path d="M9 7h11M9 12h11M9 17h11"/><path d="M4.5 7h.01M4.5 12h.01M4.5 17h.01"/>',
 "mail": '<rect x="3.5" y="5.5" width="17" height="13" rx="2.5"/><path d="m4 7 8 6 8-6"/>',
 "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
 "key": '<circle cx="8" cy="15" r="3.5"/><path d="m10.5 12.5 8-8M15.5 7.5l2.5 2.5"/>',
}
sprite = '<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">' + "".join(
    f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">{v}</symbol>'
    for k, v in ICONS.items()) + '</svg>'
def ic(name, cls="i"): return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#i-{name}"/></svg>'

def buy_btn(pid, name, cls, label="Buy now"):
    url = C["checkout_links"].get(pid, "")
    if url:
        return (f'<a class="btn {cls} btn-block" href="{e(url)}" rel="noopener">{label}'
                f'<span class="sr-only">: {e(name)}</span></a>')
    return (f'<a class="btn {cls} btn-block" href="#contact" data-package="{pid}">{label}'
            f'<span class="sr-only">: {e(name)}</span></a>')

PACKAGES = [(t["id"], f'{t["name"]} ({money(t["price"])})') for t in C["tiers"]] + [
    ("care-monthly", f"Monthly Care ({money(care_m)}/mo)"),
    ("care-quarterly", f"Quarterly Checkup ({money(care_q)}/quarter)"),
    ("care-yearly", f"Annual Refresh ({money(care_y)}/yr)"),
    ("not-sure", "Not sure yet"),
]
TRADE_OPTS = ["HVAC", "Plumbing", "Electrical", "Pressure washing", "House cleaning", "Other"]

def tier_html(t):
    items = "".join(f"<li>{ic('check')}<span>{x.format(care_monthly=money(care_m))}</span></li>" for x in t["items"])
    cls = "tier featured" if t["featured"] else "tier"
    badge = '<span class="badge">Most popular</span>' if t["featured"] else ""
    return (f'<article class="{cls}">{badge}<h3>{e(t["name"])}</h3>'
            f'<p class="price"><b>{money(t["price"])}</b><span>one-time</span></p>'
            f'<p class="tier-blurb">{e(t["blurb"])}</p><ul class="checks">{items}</ul>'
            f'{buy_btn(t["id"], t["name"], "btn-primary" if t["featured"] else "btn-outline")}</article>')

def browser(slug, name, eager=False, label=""):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<div class="browser"><div class="browser-bar" aria-hidden="true"><i></i><i></i><i></i><span>{label}</span></div>'
            f'<img src="img/{slug}-desktop.webp" srcset="img/{slug}-desktop-640.webp 640w, img/{slug}-desktop.webp 1200w" '
            f'sizes="(min-width:1024px) 560px, (min-width:768px) 46vw, 92vw" width="1200" height="791" {load} '
            f'alt="{name} demo site on a desktop browser"></div>')

def phone(slug, name, eager=False):
    load = '' if eager else 'loading="lazy" decoding="async"'
    return (f'<div class="phone"><img src="img/{slug}-mobile.webp" width="390" height="844" {load} '
            f'alt="{name} demo site on a phone, with the sticky call bar"></div>')

def sample_html(slug, name, niche, icon):
    url = C["samples_base"] + slug + "/"
    return (f'<article class="sample"><div class="sample-media">{browser(slug, name, label="Demo")}{phone(slug, name)}</div>'
            f'<div class="sample-body"><span class="tag">{ic(icon)}{niche}</span><h3>{name}</h3>'
            f'<p class="muted small">Fictional demo company</p>'
            f'<a class="text-link stretched" href="{url}" target="_blank" rel="noopener">View live demo<span class="sr-only"> of {name} (opens in a new tab)</span> {ic("arrow")}</a></div></article>')

SAMPLE_ICONS = {"ridgeline": "flame", "stonecreek-plumbing": "drop", "loneoak-pressure-washing": "spray", "tidypine-cleaning": "sparkle"}

platform_btns = ""
if C["fiverr_url"]:
    platform_btns += f'<a class="btn btn-outline-light" href="{e(C["fiverr_url"])}" rel="noopener">Order on Fiverr</a>'
if C["contra_url"]:
    platform_btns += f'<a class="btn btn-outline-light" href="{e(C["contra_url"])}" rel="noopener">Hire on Contra</a>'

mailto = f'mailto:{C["contact_email"]}?subject=' + "Website%20for%20my%20business"

faq_html = "".join(f'<details><summary>{e(q)}<span class="plus" aria-hidden="true"></span></summary><p>{e(a)}</p></details>' for q, a in FAQ)
jsonld = [
    {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "WebsitePlz",
     "url": C["site_url"], "image": C["site_url"] + "img/og.png", "logo": C["site_url"] + "img/icon-512.png",
     "description": "Phone-first one-page websites for local service businesses.",
     "makesOffer": [{"@type": "Offer", "name": t["name"], "price": t["price"], "priceCurrency": "USD"} for t in C["tiers"]]},
    {"@context": "https://schema.org", "@type": "FAQPage",
     "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
]

title = "WebsitePlz | Websites that make the phone ring for local service pros"
desc = (f"Phone-first websites for HVAC, plumbing, electrical, pressure washing and house cleaning businesses. "
        f"Click-to-call, your services and cities, live on your own domain in 5 days. From {money(lowest)}.")

INCLUDED = [
    ("phone", "Click-to-call everywhere", "A call button in the header and a bar that stays on screen while customers scroll."),
    ("image", "Your logo and photos", "Your brand, your trucks, your crew. Phone photos are fine."),
    ("list", "Your main services", "Clear cards for the jobs you want more of."),
    ("star", "Real reviews", "Reviews from your own customers, styled to build trust."),
    ("shield", "License, insured and financing lines", "The details homeowners check before they call."),
    ("form", "Quote or booking form", "For customers who would rather type than talk."),
    ("pin", "Cities you serve", "Your service area, spelled out so the right people call."),
    ("gauge", "Fast on phones", "A hand-built static page with no plugins slowing it down."),
    ("globe", "On your own domain", "You own the domain and, once paid in full, the files."),
]
included_html = "".join(f'<li>{ic(i, "i i-box")}<div><b>{t}</b><span>{d}</span></div></li>' for i, t, d in INCLUDED)

STEPS = [("Pick a package", "Choose the page you need below."),
         ("Send your assets", "Logo, phone, cities, services, photos and reviews. Phone photos are fine."),
         ("Review your preview", "Request changes in your included revision rounds."),
         ("Go live", "Your site goes live on your domain 5 days after your assets arrive.")]
steps_html = "".join(f'<li><span class="num" aria-hidden="true">{n}</span><b>{t}</b><span>{d}</span></li>' for n, (t, d) in enumerate(STEPS, 1))

TRADES = [("flame", "HVAC"), ("drop", "Plumbing"), ("bolt", "Electrical"), ("spray", "Pressure washing"), ("sparkle", "House cleaning")]
trades_html = "".join(f'<li>{ic(i)}{t}</li>' for i, t in TRADES)

checkout_note = "" if any(C["checkout_links"].get(t["id"]) for t in C["tiers"]) else (
    '<p class="checkout-note">Online checkout is coming soon. For now, tap Buy now, send your details and we\'ll reply with next steps.</p>')

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{C['site_url']}">
<meta name="theme-color" content="#0B1B2E">
<meta property="og:type" content="website">
<meta property="og:site_name" content="WebsitePlz">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{C['site_url']}">
<meta property="og:image" content="{C['site_url']}img/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="WebsitePlz: websites that make the phone ring">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{C['site_url']}img/og.png">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preload" href="img/fonts/bricolage.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="img/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="styles.css">
<script type="application/ld+json">{json.dumps(jsonld)}</script>
</head>
<body>
{sprite}
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap bar">
    <a class="logo" href="#top"><img src="img/logo.svg" width="168" height="40" alt="WebsitePlz home"></a>
    <nav aria-label="Main"><a href="#samples">Our work</a><a href="#included">What's included</a><a href="#pricing">Pricing</a><a href="#faq">FAQ</a></nav>
    <a class="btn btn-primary btn-sm" href="#contact">Get started</a>
  </div>
</header>

<main id="main">
<section class="hero" id="top">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="eyebrow"><span class="dot" aria-hidden="true"></span>For local service pros</p>
      <h1>Websites that make the <em>phone ring.</em></h1>
      <p class="lead">One-page, phone-first websites for HVAC, plumbing, electrical, pressure washing and cleaning businesses. A call button that stays on screen, your services and cities, and a quote form. Live on your own domain 5 days after you send your logo and photos.</p>
      <div class="cta-row"><a class="btn btn-primary btn-lg" href="#samples">See our work {ic("arrow")}</a><a class="btn btn-outline-light btn-lg" href="#pricing">See pricing</a></div>
      <ul class="trust"><li>{ic("check")}From {money(lowest)}</li><li>{ic("check")}Live in 5 days</li><li>{ic("check")}You own your domain</li><li>{ic("check")}No WordPress or plugins</li></ul>
    </div>
    <div class="hero-media">
      <div class="glow" aria-hidden="true"></div>
      {browser("ridgeline", "Ridge Line Heating &amp; Air", eager=True, label="Sample site")}
      {phone("tidypine-cleaning", "Tidy Pine Home Cleaning", eager=True)}
      <p class="media-note">Demo sites for fictional companies</p>
    </div>
  </div>
  <div class="wrap"><ul class="trades" aria-label="Trades we build for">{trades_html}</ul></div>
</section>

<section class="section" id="who">
  <div class="wrap">
    <div class="head"><p class="kicker">Who it's for</p><h2>Built for owners who live on the phone</h2>
    <p class="sub">Your phone is your sales team. Every page is built to get a call, not to be a blog.</p></div>
    <div class="grid3">
      <article class="card"><span class="ico">{ic("flame")}</span><h3>HVAC, plumbing &amp; electrical</h3><p>If you pay for LSA, Angi or Google Ads leads, this is the page those homeowners check before they call. Sticky call button, your license and insured line, financing and reviews.</p></article>
      <article class="card"><span class="ico">{ic("spray")}</span><h3>Pressure washing &amp; exterior cleaning</h3><p>Turn Facebook likes into booked jobs. A one-page site with a "Get a Free Quote" button, before-and-after photos, service areas and your flat prices.</p></article>
      <article class="card"><span class="ico">{ic("sparkle")}</span><h3>House cleaning &amp; maid service</h3><p>Flat prices by home size, a "Get My Price" form, your service area and guarantee, on one fast page clients can book from on their phone.</p></article>
    </div>
  </div>
</section>

<section class="section alt" id="samples">
  <div class="wrap">
    <div class="head"><p class="kicker">Our work</p><h2>See what we build</h2>
    <p class="sub">Four live demo sites, built the way we build yours. The companies are fictional, so open one on your phone and tap around.</p></div>
    <div class="grid2">{''.join(sample_html(s, n, ni, SAMPLE_ICONS[s]) for s, n, ni in SAMPLES)}</div>
    <p class="center more"><a class="text-link" href="{C['samples_base']}" target="_blank" rel="noopener">All samples<span class="sr-only"> (opens in a new tab)</span> {ic("arrow")}</a></p>
  </div>
</section>

<section class="section" id="included">
  <div class="wrap">
    <div class="head"><p class="kicker">What's included</p><h2>What's on the page</h2>
    <p class="sub">Everything a homeowner looks for before they call, and nothing that slows the page down.</p></div>
    <ul class="included">{included_html}</ul>
  </div>
</section>

<section class="section alt" id="how">
  <div class="wrap">
    <div class="head"><p class="kicker">How it works</p><h2>Four steps to live</h2></div>
    <ol class="steps">{steps_html}</ol>
  </div>
</section>

<section class="section" id="pricing">
  <!-- Prices come from CONFIG in build.py. Do not edit here; run build.py. -->
  <div class="wrap">
    <div class="head"><p class="kicker">Pricing</p><h2>Simple, one-time pricing</h2>
    <p class="sub">Pay once for the site. Care is optional.</p></div>{checkout_note}
    <div class="tiers">{''.join(tier_html(t) for t in C['tiers'])}</div>
  </div>
</section>

<section class="section alt" id="care">
  <div class="wrap">
    <div class="head"><p class="kicker">Care plans</p><h2>We look after it, you stay on the job</h2>
    <p class="sub">Optional. We host it, test it and make small edits for you.</p></div>
    <div class="tiers care">
      <article class="tier"><h3>Monthly Care</h3><p class="price"><b>{money(care_m)}</b><span>/mo</span></p><p class="tier-blurb">Billed monthly</p>
        <ul class="checks"><li>{ic("check")}<span>Hosting, SSL and form</span></li><li>{ic("check")}<span>2 small edits a month</span></li><li>{ic("check")}<span>Monthly test of the call button and form</span></li></ul>{buy_btn('care-monthly', 'Monthly Care', 'btn-outline', 'Choose plan')}</article>
      <article class="tier"><h3>Quarterly Checkup</h3><p class="price"><b>{money(care_q)}</b><span>/quarter</span></p><p class="tier-blurb">About {money(q_per_mo)}/mo</p>
        <ul class="checks"><li>{ic("check")}<span>Hosting</span></li><li>{ic("check")}<span>Quarterly speed, link, call and form test</span></li><li>{ic("check")}<span>New reviews and photos swapped in</span></li><li>{ic("check")}<span>Seasonal promo line</span></li><li>{ic("check")}<span>Up to 4 small edits a quarter</span></li></ul>{buy_btn('care-quarterly', 'Quarterly Checkup', 'btn-outline', 'Choose plan')}</article>
      <article class="tier"><h3>Annual Refresh</h3><p class="price"><b>{money(care_y)}</b><span>/yr</span></p><p class="tier-blurb">Prepaid. Saves {money(y_save)} (about {y_pct}%) vs. monthly</p>
        <ul class="checks"><li>{ic("check")}<span>Everything in Monthly Care</span></li><li>{ic("check")}<span>One yearly refresh: new hero photo, updated reviews, new offers</span></li><li>{ic("check")}<span>Speed test re-run</span></li></ul>{buy_btn('care-yearly', 'Annual Refresh', 'btn-outline', 'Choose plan')}</article>
    </div>
    <p class="small muted center fine">A small edit takes 15 minutes or less (text, hours, a price, a photo swap). Unused edits don't roll over. Cancel with 30 days' notice and we hand over your files.</p>
  </div>
</section>

<section class="section" id="faq">
  <div class="wrap narrow">
    <div class="head"><p class="kicker">FAQ</p><h2>Questions</h2></div>
    <div class="faq">{faq_html}</div>
  </div>
</section>

<section class="contact" id="contact">
  <div class="wrap contact-grid">
    <div class="contact-copy">
      <p class="kicker light">Get started</p>
      <h2>Ready for a site that gets calls?</h2>
      <p class="lead">Tell us about your business and which package you want. We'll reply by email with next steps.</p>
      <ul class="trust"><li>{ic("check")}Live 5 days after your assets arrive</li><li>{ic("check")}You own your domain</li><li>{ic("check")}No WordPress or plugins</li></ul>
      <!-- TODO: add Fiverr / Contra profile URLs in build.py once the accounts exist. -->
      <p class="contact-alt">Prefer email? <a href="{mailto}">{e(C["contact_email"])}</a></p>
      <div class="cta-row">{platform_btns}</div>
    </div>
    <form class="intake" id="intake" action="{C['form_endpoint']}" method="post" novalidate>
      <div class="f2">
        <label>Your name <span class="req" aria-hidden="true">*</span><input name="name" autocomplete="name" required maxlength="100"></label>
        <label>Business name <span class="req" aria-hidden="true">*</span><input name="business" autocomplete="organization" required maxlength="120"></label>
      </div>
      <div class="f2">
        <label>Email <span class="req" aria-hidden="true">*</span><input type="email" name="email" autocomplete="email" required maxlength="160"></label>
        <label>Phone <span class="opt">(optional)</span><input type="tel" name="phone" autocomplete="tel" maxlength="40"></label>
      </div>
      <div class="f2">
        <label>Trade <span class="req" aria-hidden="true">*</span><select name="trade" required><option value="">Choose your trade</option>{"".join(f'<option>{t}</option>' for t in TRADE_OPTS)}</select></label>
        <label>Package<select name="package" id="f-package">{"".join(f'<option value="{pid}"{" selected" if pid=="not-sure" else ""}>{lbl}</option>' for pid, lbl in PACKAGES)}</select></label>
      </div>
      <label>Current website <span class="opt">(optional)</span><input type="url" name="website" inputmode="url" placeholder="https://" maxlength="200"></label>
      <label>Message <span class="opt">(optional)</span><textarea name="message" rows="4" maxlength="3000" placeholder="Cities you serve, what you want more of, anything else."></textarea></label>
      <div class="hp" aria-hidden="true"><label>Leave this empty<input name="company_fax" tabindex="-1" autocomplete="off"></label></div>
      <input type="hidden" name="t" value="">
      <button class="btn btn-primary btn-lg btn-block" type="submit">Send my details</button>
      <p class="form-fine"><span class="req" aria-hidden="true">*</span> Required. We only use your details to reply to you.</p>
      <div class="form-status" role="status" aria-live="polite" tabindex="-1"></div>
    </form>
  </div>
</section>
</main>

<footer class="foot">
  <div class="wrap foot-grid">
    <div><img src="img/logo-light.svg" width="151" height="36" alt="WebsitePlz" loading="lazy"><p>Websites for local service businesses.</p></div>
    <nav aria-label="Footer"><a href="#samples">Our work</a><a href="#pricing">Pricing</a><a href="#care">Care plans</a><a href="#faq">FAQ</a><a href="#contact">Contact</a></nav>
  </div>
  <div class="wrap foot-fine">
    <p>Sample sites shown are fictional demo companies. Phone numbers, licenses, photos and reviews on them are placeholders.</p>
    <p>&copy; 2026 WebsitePlz</p>
  </div>
</footer>
<div class="mobile-bar mbar"><a class="btn btn-outline btn-block" href="#pricing">Pricing</a><a class="btn btn-primary btn-block" href="#contact">Get started</a></div>
<script>
(function(){{var f=document.getElementById('intake');if(!f)return;var sel=document.getElementById('f-package'),st=f.querySelector('.form-status'),btn=f.querySelector('button[type=submit]');
f.t.value=Date.now();
document.addEventListener('click',function(ev){{var a=ev.target.closest('[data-package]');if(a&&sel){{sel.value=a.getAttribute('data-package');}}}});
function show(msg,ok){{st.className='form-status '+(ok?'ok':'err');st.innerHTML=msg;st.focus();}}
var fallback='Sorry, the form could not be sent right now. Please email us at <a href="{mailto}">{e(C["contact_email"])}</a>.';
f.addEventListener('submit',function(ev){{ev.preventDefault();
  var bad=null;Array.prototype.forEach.call(f.querySelectorAll('[required]'),function(el){{el.removeAttribute('aria-invalid');if(!el.checkValidity()){{el.setAttribute('aria-invalid','true');bad=bad||el;}}}});
  ['email','website'].forEach(function(n){{var el=f[n];if(el.value&&!el.checkValidity()){{el.setAttribute('aria-invalid','true');bad=bad||el;}}}});
  if(bad){{show('Please check the highlighted fields.',false);bad.focus();return;}}
  btn.disabled=true;btn.textContent='Sending...';
  fetch(f.action,{{method:'POST',headers:{{'Accept':'application/json'}},body:new FormData(f)}}).then(function(r){{return r.json().catch(function(){{return {{ok:false}};}}).then(function(d){{return [r,d];}});}})
  .then(function(x){{var r=x[0],d=x[1];if(r.ok&&d.ok){{f.reset();f.t.value=Date.now();show('Thanks! Your details are in. We\u2019ll reply by email soon.',true);}}else{{show(r.status<500&&d.error?d.error:fallback,false);}}}})
  .catch(function(){{show(fallback,false);}}).then(function(){{btn.disabled=false;btn.textContent='Send my details';}});
}});}})();
</script>
</body>
</html>
"""
pathlib.Path(__file__).with_name("index.html").write_text(page)
print("wrote index.html")
