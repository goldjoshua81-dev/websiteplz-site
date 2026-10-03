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
        {"name": "Starter Page", "price": 249, "featured": False,
         "blurb": "Get online fast with a clean, phone-first page.",
         "items": ["One-page site on your domain", "Your logo, phone and cities",
                   "2 of your photos", "Click-to-call button", "Quote form",
                   "1 revision round", "Live 5 days after assets arrive"]},
        {"name": "Emergency-ready Site", "price": 1125, "featured": True,
         "blurb": "The full page built to turn visitors into calls.",
         "items": ["Everything in Starter", "Sticky call bar that stays on screen",
                   "4 of your photos", "Your 3 main services", "Reviews section",
                   "Financing line + license & insured line", "Quote / book form",
                   "2 revision rounds", "Live 5 days after assets arrive"]},
        {"name": "Emergency-ready + 3 Months Care", "price": 1495, "featured": False,
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
    ("Is it WordPress?", "No. It's a hand-built static page: faster, no plugins to update, and nothing to hack."),
    ("Are there monthly fees?", f"Only if you want Care. Monthly Care is {money(care_m)}/mo for hosting plus 2 small edits a month. Without Care, we hand the site off to your own host."),
    ("How many revisions do I get?", "Starter includes 1 round, the other packages include 2. A revision is a change to what's on the page, not a new design."),
    ("Do you do SEO or ads?", "No. This is a fast, honest page that turns visitors into calls. Your Google Business Profile and ads send the traffic."),
    ("What counts as a small edit?", "Anything that takes 15 minutes or less: text, hours, a price or a photo swap. Bigger changes are quoted separately, and unused edits don't roll over."),
    ("Who owns the site?", "You do. You own your domain, your content and the final page files once paid in full."),
]

def tier_html(t):
    items = "".join(f"<li>{x.format(care_monthly=money(care_m))}</li>" for x in t["items"])
    cls = "tier featured" if t["featured"] else "tier"
    badge = '<span class="badge">Most popular</span>' if t["featured"] else ""
    return (f'<article class="{cls}">{badge}<h3>{e(t["name"])}</h3>'
            f'<p class="price">{money(t["price"])}<span> one-time</span></p>'
            f'<p class="muted">{e(t["blurb"])}</p><ul class="checks">{items}</ul>'
            f'<a class="btn {"btn-primary" if t["featured"] else "btn-ghost"}" href="#contact">Get started</a></article>')

def sample_html(slug, name, niche):
    url = C["samples_base"] + slug + "/"
    return (f'<article class="sample"><a href="{url}" target="_blank" rel="noopener">'
            f'<div class="shots"><img src="img/{slug}-desktop.webp" width="800" height="504" loading="lazy" alt="{name} demo site, desktop view">'
            f'<img class="phone" src="img/{slug}-mobile.webp" width="260" height="500" loading="lazy" alt="{name} demo site, phone view"></div>'
            f'<div class="sample-body"><span class="tag">{niche}</span><h3>{name}</h3>'
            f'<p class="muted small">Fictional demo company</p><span class="link">View live demo &rarr;</span></div></a></article>')

platform_btns = ""
if C["fiverr_url"]:
    platform_btns += f'<a class="btn btn-ghost-light" href="{e(C["fiverr_url"])}" rel="noopener">Order on Fiverr</a>'
if C["contra_url"]:
    platform_btns += f'<a class="btn btn-ghost-light" href="{e(C["contra_url"])}" rel="noopener">Hire on Contra</a>'

mailto = f'mailto:{C["contact_email"]}?subject=' + "Website%20for%20my%20business"

faq_html = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in FAQ)
jsonld = [
    {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "WebsitePlz",
     "url": C["site_url"], "image": C["site_url"] + "img/og.png",
     "description": "Phone-first one-page websites for local service businesses.",
     "makesOffer": [{"@type": "Offer", "name": t["name"], "price": t["price"], "priceCurrency": "USD"} for t in C["tiers"]]},
    {"@context": "https://schema.org", "@type": "FAQPage",
     "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
]

title = "WebsitePlz | Websites that make the phone ring for local service pros"
desc = (f"Phone-first websites for HVAC, plumbing, electrical, pressure washing and house cleaning businesses. "
        f"Click-to-call, your services and cities, live on your own domain in 5 days. From {money(lowest)}.")

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{C['site_url']}">
<meta name="theme-color" content="#0f2a44">
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
<link rel="stylesheet" href="styles.css">
<script type="application/ld+json">{json.dumps(jsonld)}</script>
</head>
<body>
<header class="top">
  <div class="wrap bar">
    <a class="logo" href="#top" aria-label="WebsitePlz home">Website<b>Plz</b><i></i></a>
    <nav aria-label="Main"><a href="#samples">Samples</a><a href="#how">How it works</a><a href="#pricing">Pricing</a><a href="#faq">FAQ</a></nav>
    <a class="btn btn-primary btn-sm" href="#contact">Get started</a>
  </div>
</header>

<main id="top">
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow">For HVAC, plumbing, electrical, pressure washing &amp; cleaning pros</p>
      <h1>Websites that make the phone ring.</h1>
      <p class="lead">One-page, phone-first websites for local service businesses. A call button that stays on screen, your services and cities, and a quote form. Live on your own domain 5 days after you send your logo and photos.</p>
      <div class="cta-row"><a class="btn btn-primary" href="#samples">See sample sites</a><a class="btn btn-ghost-light" href="#pricing">See pricing</a></div>
      <ul class="trust"><li>From {money(lowest)}</li><li>Live in 5 days</li><li>You own your domain</li><li>No WordPress, nothing to hack</li></ul>
    </div>
    <div class="hero-shot" aria-hidden="true">
      <img src="img/ridgeline-mobile.webp" width="260" height="500" alt="">
    </div>
  </div>
</section>

<section class="section" id="who">
  <div class="wrap">
    <h2>Built for owners who live on the phone</h2>
    <p class="sub">Your phone is your sales team. Every page is built to get a call, not to be a blog.</p>
    <div class="grid3">
      <article class="card"><div class="ico" aria-hidden="true">&#128295;</div><h3>HVAC, plumbing &amp; electrical</h3><p>If you pay for LSA, Angi or Google Ads leads, this is the page those homeowners check before they call. Sticky call button, your license and insured line, financing and reviews.</p></article>
      <article class="card"><div class="ico" aria-hidden="true">&#128166;</div><h3>Pressure washing &amp; exterior cleaning</h3><p>Turn Facebook likes into booked jobs. A one-page site with a "Get a Free Quote" button, before-and-after photos, service areas and your flat prices.</p></article>
      <article class="card"><div class="ico" aria-hidden="true">&#10024;</div><h3>House cleaning &amp; maid service</h3><p>Flat prices by home size, a "Get My Price" form, your service area and guarantee, on one fast page clients can book from on their phone.</p></article>
    </div>
  </div>
</section>

<section class="section alt" id="samples">
  <div class="wrap">
    <h2>See it before you buy</h2>
    <p class="sub">Four live demo sites built from the same template your site will use. The companies are fictional; tap one to try it on your phone.</p>
    <div class="grid2">{''.join(sample_html(*s) for s in SAMPLES)}</div>
    <p class="center"><a class="text-link" href="{C['samples_base']}" target="_blank" rel="noopener">All samples &rarr;</a></p>
  </div>
</section>

<section class="section" id="included">
  <div class="wrap two-col">
    <div>
      <h2>What's on the page</h2>
      <p class="sub">Everything a homeowner looks for before they call, and nothing that slows the page down.</p>
    </div>
    <ul class="checks big">
      <li>Your logo, phone number and cities served</li>
      <li>Click-to-call header that sticks while customers scroll</li>
      <li>Your 3 main services</li>
      <li>Real reviews from your customers</li>
      <li>Financing line, license and insured line</li>
      <li>Quote or booking form</li>
      <li>Fast on phones, hand-built static page</li>
      <li>On your own domain, which you own</li>
    </ul>
  </div>
</section>

<section class="section alt" id="how">
  <div class="wrap">
    <h2>How it works</h2>
    <ol class="steps">
      <li><b>Pick a package</b><span>Choose the page you need below.</span></li>
      <li><b>Send your assets</b><span>Logo, phone, cities, services, photos and reviews. Phone photos are fine.</span></li>
      <li><b>Review your preview</b><span>Request changes in your included revision rounds.</span></li>
      <li><b>Go live</b><span>Your site goes live on your domain 5 days after your assets arrive.</span></li>
    </ol>
  </div>
</section>

<section class="section" id="pricing">
  <!-- Prices come from CONFIG in build.py. Do not edit here; run build.py. -->
  <div class="wrap">
    <h2>Simple, one-time pricing</h2>
    <p class="sub">Pay once for the site. Care is optional.</p>
    <div class="tiers">{''.join(tier_html(t) for t in C['tiers'])}</div>
  </div>
</section>

<section class="section alt" id="care">
  <div class="wrap">
    <h2>Care plans</h2>
    <p class="sub">Optional. We host it, test it and make small edits so you can stay on the job.</p>
    <div class="tiers care">
      <article class="tier"><h3>Monthly Care</h3><p class="price">{money(care_m)}<span>/mo</span></p>
        <ul class="checks"><li>Hosting, SSL and form</li><li>2 small edits a month</li><li>Monthly test of the call button and form</li></ul></article>
      <article class="tier"><h3>Quarterly Checkup</h3><p class="price">{money(care_q)}<span>/quarter</span></p><p class="muted small">About {money(q_per_mo)}/mo</p>
        <ul class="checks"><li>Hosting</li><li>Quarterly speed, link, call and form test</li><li>New reviews and photos swapped in</li><li>Seasonal promo line</li><li>Up to 4 small edits a quarter</li></ul></article>
      <article class="tier"><h3>Annual Refresh</h3><p class="price">{money(care_y)}<span>/yr</span></p><p class="muted small">Prepaid. Saves {money(y_save)} (about {y_pct}%) vs. monthly</p>
        <ul class="checks"><li>Everything in Monthly Care</li><li>One yearly refresh: new hero photo, updated reviews, new offers</li><li>Speed test re-run</li></ul></article>
    </div>
    <p class="small muted center">A small edit takes 15 minutes or less (text, hours, a price, a photo swap). Unused edits don't roll over. Cancel with 30 days' notice and we hand over your files.</p>
  </div>
</section>

<section class="section" id="faq">
  <div class="wrap narrow">
    <h2>Questions</h2>
    <div class="faq">{faq_html}</div>
  </div>
</section>

<section class="section contact" id="contact">
  <div class="wrap narrow center">
    <h2>Ready for a site that gets calls?</h2>
    <p class="lead">Tell us your business name, trade and city. We'll reply with next steps.</p>
    <!-- TODO: contact_email in build.py is a placeholder; no inbox is set up yet. -->
    <!-- TODO: add Fiverr / Contra profile URLs in build.py once the accounts exist. -->
    <div class="cta-row center"><a class="btn btn-primary" href="{mailto}">Email us</a>{platform_btns}</div>
  </div>
</section>
</main>

<footer class="foot">
  <div class="wrap">
    <p><b>WebsitePlz</b> &middot; Websites for local service businesses</p>
    <p class="small">Sample sites shown are fictional demo companies. Phone numbers, licenses and reviews on them are placeholders.</p>
    <p class="small">&copy; 2026 WebsitePlz</p>
  </div>
</footer>
<div class="mobile-bar"><a href="#pricing">Pricing</a><a class="go" href="#contact">Get started</a></div>
</body>
</html>
"""
pathlib.Path(__file__).with_name("index.html").write_text(page)
print("wrote index.html")
