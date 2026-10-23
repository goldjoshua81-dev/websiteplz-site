#!/usr/bin/env python3
"""WebsitePlz-owned Cloudflare Web Analytics daily snapshot.

Writes ONLY under /workspace/websiteplz-site/stats/ — does not edit Control Center.
Needs CLOUDFLARE_API_TOKEN with Account Analytics: Read.
"""
from __future__ import annotations
import datetime, json, os, sys, urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

HOST = "websiteplz.com"
CF = "https://api.cloudflare.com/client/v4"
PT = ZoneInfo("America/Los_Angeles")
OUT = Path(__file__).resolve().parents[1] / "stats"

def cf(path=None, gql=None):
    tok = os.environ.get("CLOUDFLARE_API_TOKEN")
    if not tok:
        raise SystemExit("CLOUDFLARE_API_TOKEN not set")
    h = {"Authorization": "Bearer " + tok, "Content-Type": "application/json"}
    req = urllib.request.Request(
        CF + (path or "/graphql"),
        data=json.dumps(gql).encode() if gql else None,
        headers=h,
    )
    return json.load(urllib.request.urlopen(req, timeout=30))

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    acc = cf("/accounts")["result"][0]["id"]
    sites = cf(f"/accounts/{acc}/rum/site_info/list").get("result") or []
    tag = None
    for s in sites:
        host = s.get("host") or (s.get("ruleset") or {}).get("zone_name")
        if host == HOST:
            tag = s["site_tag"]
            break
    if not tag:
        raise SystemExit(f"no Web Analytics site for {HOST}")

    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    start = now - datetime.timedelta(days=7)
    q = """query($a:String!,$t:String!,$s:Time!,$e:Time!){viewer{accounts(filter:{accountTag:$a}){
      rumPageloadEventsAdaptiveGroups(limit:1,filter:{siteTag:$t,datetime_geq:$s,datetime_lt:$e}){count sum{visits}}}}}"""
    r = cf(gql={"query": q, "variables": {
        "a": acc, "t": tag,
        "s": start.isoformat().replace("+00:00", "Z"),
        "e": now.isoformat().replace("+00:00", "Z"),
    }})
    if r.get("errors"):
        raise SystemExit(r["errors"][0].get("message"))
    g = r["data"]["viewer"]["accounts"][0]["rumPageloadEventsAdaptiveGroups"]
    views = g[0]["count"] if g else 0
    visits = g[0]["sum"]["visits"] if g else 0
    when_pt = now.astimezone(PT)
    payload = {
        "host": HOST,
        "window": "7d",
        "visits": visits,
        "views": views,
        "collected_at_pt": when_pt.isoformat(timespec="seconds"),
        "source": "Cloudflare Web Analytics (GraphQL rumPageloadEventsAdaptiveGroups)",
        "note": "Raw counts; may include bots. WebsitePlz lane snapshot only — not a Control Center write.",
    }
    day = when_pt.date().isoformat()
    path = OUT / f"cf-daily-{day}.json"
    path.write_text(json.dumps(payload, indent=2) + "\n")
    latest = OUT / "cf-latest.json"
    latest.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"ok: {visits} visits / {views} views (7d) @ {when_pt.isoformat(timespec='seconds')} -> {path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
