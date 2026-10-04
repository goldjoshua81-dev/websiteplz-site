# WebsitePlz playbook: mockups, emails and launch (manual steps)

From `upgrade_build_list.md` items MP-4, PP-1, PP-4, PP-5 and M-6. Nothing here is sent automatically.
All emails are sent by hand from Gmail. Never invent stats, reviews or results.

## MP-4 · Mockup delivery SOP
1. Within 1 business day (Mon–Fri) of a request, make the desktop (1200x791) and mobile (390x844) mockup images.
2. Add `content/mockups/<slug>.json` (see `content/mockups/README.md`; get a slug with `build.mock_slug()`), then `tools/deploy.sh`.
3. Optional: record a 2-minute (or shorter) Loom and put the link in `video_url` (needs a Loom account, BL-6).
4. Send the Day-0 email (below).
5. Track in a simple sheet: date requested, date sent, link, expires, outcome.
- Internal target: reply the same business day. **Not a public promise.**
- **Real expiry:** pages stop being built 14 days after `created`. Run `tools/deploy.sh` at least once a day while mockups
  are live (any deploy removes expired pages from the server); `js/mockup.js` also hides expired pages in the browser.

## PP-1 · Email templates
1. **Day 0, mockup delivery** (reply to their request). Subject: "Your {business} homepage mockup"
   > Hi {name or 'there'}, here's your homepage: {link}. It's private and stays up until {expires}. If you like it, the 'Make it live' buttons on that page start your site with a 50% deposit, and you only pay the rest at launch. If you'd change something, just reply. — Joshua Gold, WebsitePlz
2. **Order received** (after payment). Subject: "You're in. Here's what I need from you"
   > Logo · Phone (and after-hours or 24/7 line) · Cities served · Top services · 2 or 4 photos (per package) · Reviews you want shown (real ones) · License and insured lines · Domain registrar login, or a time to connect it together.
   > Your site goes live 5 days after the last item arrives. You'll see the full preview before launch, and the See-It-First Guarantee still applies.
3. **Day 3, no reply** (needs postal address in footer, BL-3). Subject: "Any changes to your mockup?"
   > Happy to swap photos, colors or services before you decide. Your link is up until {expires}.
4. **Day 7** (BL-3). Subject: "What a missed call costs a {noun} business"
   > Link to the calculator on the trade page (`/{trade}/#calc`) and the free checklist (`/guides/google-business-profile-checklist/`). No invented stats.
5. **Day 12** (BL-3). Subject: "Your mockup link comes down on {expires}"
   > Just a heads-up so it's not a surprise. Want it live, or want me to keep it a few more days? Either is fine.
- Emails 3–5 need a footer with the postal address and "Reply 'stop' and I won't email again." (CAN-SPAM). Don't send them until BL-3.
- Stop the sequence as soon as they reply or buy.

## PP-4 · Launch and after-launch
- Launch day: record a 60-second-or-shorter phone video tapping the call button and sending a test form on the live site; send it to the client.
- Deliver the free bonuses: Review Request Kit (3 texts + 1 email the client sends to *their* customers, asking every customer the same way, no rewards, no filtering) and the photo shot list.
- Starter / Emergency-ready launch email, one line: "Want me to look after it? Monthly Care is $99/mo, cancel any time."
- Month 5 email for $1,495 buyers: "Your 6 months of Care end on {date}. Want to keep it? Reply yes and I'll send the link. If not, I'll hand over your files." Do nothing without a yes.
- Day 30: "Would you leave an honest review of how it went? Good or bad, it helps me get better." Link WebsitePlz's Google profile once it exists (BL-9); until then ask permission to quote their words with first name and trade. Ask every client; no incentives, no filtering.
- Day 30 referral ask (direct clients only, never Fiverr): "Know another owner who needs a site? When someone you send buys any package, you get a free month of Care." Track via the `referred_by` form field.

## PP-5 · Optional credit link
Ask at launch: "Mind if I add a small 'Site by WebsitePlz' link in your footer? Totally fine to say no." Only with a yes; never a condition of the price.

## M-6 · Visitor auto-reply (blocked: Workers Paid + Cloudflare Email Service, BL-7)
Subject: "Got it: your free {trade} mockup"
> Thanks, {name or 'there'}. I'll send your private mockup link for {business} within 1 business day (Mon–Fri). The link stays up for 14 days. Questions? Just reply. — Joshua Gold, WebsitePlz
