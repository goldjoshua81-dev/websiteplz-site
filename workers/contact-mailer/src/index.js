// websiteplz-contact-mailer: emails contact-form submissions to Joshua.
// Only reachable through the Pages project's service binding (workers_dev = false, no routes).
import { EmailMessage } from "cloudflare:email";

const FROM = "form@websiteplz.com";          // any address on the websiteplz.com Email Routing zone
const TO = "printplzeverything@gmail.com";   // must be a VERIFIED Email Routing destination

const b64 = (s) => btoa(unescape(encodeURIComponent(s)));
const noCrlf = (s) => String(s || "").replace(/[\r\n]+/g, " ").trim();
const encWord = (s) => `=?UTF-8?B?${b64(noCrlf(s))}?=`;

export default {
  async fetch(request, env) {
    if (request.method !== "POST") return new Response("POST only", { status: 405 });
    const d = await request.json();
    const PKG = { starter: "Starter Page ($249)", emergency: "Emergency-ready Site ($1,125)", "emergency-care": "Emergency-ready + 3 Months Care ($1,495)",
      "care-monthly": "Monthly Care ($99/mo)", "care-quarterly": "Quarterly Checkup ($249/quarter)", "care-yearly": "Annual Refresh ($990/yr)", "not-sure": "Not sure yet" };
    const mock = d.type === "mockup";
    const body = (mock ? [
      "New FREE MOCKUP request", "",
      `Name:      ${d.name}`, `Business:  ${d.business}`, `Trade:     ${d.trade}`, `City:      ${d.city}`,
      `Email:     ${d.email}`, `Phone:     ${d.phone || "-"}`, `Site/listing: ${d.listing || "-"}`,
    ] : [
      "New WebsitePlz message", "",
      `Name:      ${d.name}`, `Business:  ${d.business || "-"}`, `Trade:     ${d.trade || "-"}`,
      `Email:     ${d.email}`, `Phone:     ${d.phone || "-"}`, `Website:   ${d.website || "-"}`,
      `Package:   ${PKG[d.package] || d.package}`, "", "Message:", d.message || "-",
    ]).concat(["", `Received:  ${d.received_at}  (${d.country || "?"})`]).join("\r\n");
    const subject = mock ? `Free mockup request: ${d.business} (${d.trade}, ${d.city})`
      : `${d.package && d.package !== "not-sure" ? "Package inquiry" : "Question"}: ${d.business || d.name}`;
    const mime = [
      `From: WebsitePlz form <${FROM}>`, `To: <${TO}>`,
      ...(/^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]{2,}$/.test(d.email || "") ? [`Reply-To: <${d.email}>`] : []),
      `Subject: ${encWord(subject)}`, `Date: ${new Date().toUTCString()}`,
      `Message-ID: <${crypto.randomUUID()}@websiteplz.com>`, "MIME-Version: 1.0",
      "Content-Type: text/plain; charset=UTF-8", "Content-Transfer-Encoding: base64", "",
      b64(body).replace(/(.{76})/g, "$1\r\n"),
    ].join("\r\n");
    try {
      await env.SEB.send(new EmailMessage(FROM, TO, mime));
    } catch (e) {
      return new Response(`send failed: ${e.message}`, { status: 502 });
    }
    return new Response("ok");
  },
};
