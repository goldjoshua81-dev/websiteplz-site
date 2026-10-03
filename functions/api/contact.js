// Cloudflare Pages Function: POST /api/contact
// Validates the intake form, blocks bots (honeypot + time trap + rate limit),
// then delivers the submission via the first delivery option that is configured:
//   1. env.MAILER     - Service binding to the "websiteplz-contact-mailer" Worker
//                       (workers/contact-mailer), which emails it with send_email.
//   2. env.SUBMISSIONS - KV namespace binding; submission stored as JSON.
// If neither binding exists the API answers 503 and the page shows the email fallback.
// Optional env.RATE_KV (KV) makes the rate limit global instead of per-isolate.

const LIMITS = { name: 100, business: 120, email: 160, phone: 40, trade: 40, website: 200, package: 40, message: 3000 };
const TRADES = ["HVAC", "Plumbing", "Electrical", "Pressure washing", "House cleaning", "Other"];
const PACKAGES = ["starter", "emergency", "emergency-care", "care-monthly", "care-quarterly", "care-yearly", "not-sure"];
const RATE_MAX = 5;           // submissions
const RATE_WINDOW = 600;      // per 10 minutes per IP
const memHits = new Map();    // best-effort fallback limiter (per isolate)

const json = (body, status = 200, extra = {}) =>
  new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", ...extra } });

function htmlPage(title, msg, status) {
  return new Response(`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>${title} | WebsitePlz</title><link rel="stylesheet" href="/styles.css"></head><body style="padding:0"><main class="hero" style="min-height:100vh"><div class="wrap narrow center" style="position:relative"><h1>${title}</h1><p class="lead" style="margin-inline:auto">${msg}</p><p><a class="btn btn-primary" href="/">Back to WebsitePlz</a></p></div></main></body></html>`,
    { status, headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" } });
}

async function rateLimited(env, ip) {
  const now = Math.floor(Date.now() / 1000);
  if (env.RATE_KV) {
    const key = `rl:${ip}:${Math.floor(now / RATE_WINDOW)}`;
    const n = parseInt((await env.RATE_KV.get(key)) || "0", 10) + 1;
    await env.RATE_KV.put(key, String(n), { expirationTtl: RATE_WINDOW * 2 });
    return n > RATE_MAX;
  }
  const rec = memHits.get(ip) || [];
  const recent = rec.filter((t) => now - t < RATE_WINDOW);
  recent.push(now);
  memHits.set(ip, recent);
  if (memHits.size > 5000) memHits.clear();
  return recent.length > RATE_MAX;
}

function clean(v, max) {
  return String(v ?? "").replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, "").trim().slice(0, max);
}

export async function onRequestPost({ request, env }) {
  const wantsJson = (request.headers.get("accept") || "").includes("application/json");
  const fail = (error, status = 400) =>
    wantsJson ? json({ ok: false, error }, status) : htmlPage("Something went wrong", error, status);

  let raw;
  try {
    const ct = request.headers.get("content-type") || "";
    if (ct.includes("application/json")) raw = await request.json();
    else raw = Object.fromEntries(await request.formData());
  } catch {
    return fail("We couldn't read that form.");
  }

  // Bots: honeypot filled, or submitted faster than 3 seconds after page load.
  // Pretend success so bots don't learn anything.
  const started = parseInt(raw.t || "0", 10);
  if (clean(raw.company_fax, 200) || (started && Date.now() - started < 3000)) {
    return wantsJson ? json({ ok: true }) : htmlPage("Thanks!", "Your details are in. We'll reply by email soon.", 200);
  }

  const ip = request.headers.get("cf-connecting-ip") || "unknown";
  if (await rateLimited(env, ip)) return fail("Too many submissions. Please try again in a few minutes.", 429);

  const d = {};
  for (const [k, max] of Object.entries(LIMITS)) d[k] = clean(raw[k], max);
  d.email = d.email.replace(/[\r\n]/g, "");
  const errors = [];
  if (!d.name) errors.push("name");
  if (!d.business) errors.push("business name");
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(d.email)) errors.push("email");
  if (!TRADES.includes(d.trade)) errors.push("trade");
  if (d.package && !PACKAGES.includes(d.package)) d.package = "not-sure";
  if (!d.package) d.package = "not-sure";
  if (d.website && !/^(https?:\/\/)?[^\s]+\.[^\s]{2,}/i.test(d.website)) errors.push("current website");
  if (d.phone && !/^[0-9+().\-\s x]{7,40}$/i.test(d.phone)) errors.push("phone");
  if (errors.length) return fail(`Please check: ${errors.join(", ")}.`);

  const submission = {
    ...d,
    received_at: new Date().toISOString(),
    ip,
    country: request.cf?.country || "",
    user_agent: clean(request.headers.get("user-agent"), 300),
  };

  try {
    if (env.MAILER) {
      const r = await env.MAILER.fetch("https://mailer.internal/send", {
        method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(submission),
      });
      if (!r.ok) throw new Error(`mailer ${r.status}`);
    } else if (env.SUBMISSIONS) {
      const key = `sub:${submission.received_at}:${crypto.randomUUID()}`;
      await env.SUBMISSIONS.put(key, JSON.stringify(submission));
    } else {
      return fail("The form isn't connected yet.", 503);
    }
  } catch (err) {
    console.error("contact delivery failed", err);
    return fail("We couldn't send your details.", 502);
  }

  return wantsJson ? json({ ok: true }) : htmlPage("Thanks!", "Your details are in. We'll reply by email soon.", 200);
}

export async function onRequest({ request }) {
  if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: { allow: "POST" } });
  return json({ ok: false, error: "Use POST." }, 405, { allow: "POST" });
}
