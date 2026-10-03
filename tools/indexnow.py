#!/usr/bin/env python3
"""Ping IndexNow (Bing, Yandex, Seznam, Naver...) with every URL in sitemap.xml. Run after each deploy."""
import json, re, pathlib, urllib.request
root = pathlib.Path(__file__).resolve().parent.parent
k = re.search(r'"indexnow_key": "([0-9a-f]+)"', (root / "build.py").read_text()).group(1)
urls = re.findall(r"<loc>([^<]+)</loc>", (root / "sitemap.xml").read_text())
body = json.dumps({"host": "websiteplz.com", "key": k, "keyLocation": f"https://websiteplz.com/{k}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, method="POST",
                             headers={"Content-Type": "application/json; charset=utf-8"})
print(urllib.request.urlopen(req, timeout=30).status, f"({len(urls)} URLs)")  # 200/202 = accepted
