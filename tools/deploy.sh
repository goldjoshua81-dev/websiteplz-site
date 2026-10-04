#!/usr/bin/env bash
# Build and deploy websiteplz.com to Cloudflare Pages (project "websiteplz").
# Needs CLOUDFLARE_API_TOKEN (Pages Edit) in env. Never echo it.
# Runs wrangler from /tmp/wplzproj (an empty node_modules/ there avoids the EACCES on /node_modules/.cache).
set -euo pipefail
SITE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SITE" && python3 build.py
KEY=$(python3 -c "import re;print(re.search(r'\"indexnow_key\": \"([0-9a-f]+)\"',open('build.py').read()).group(1))")
P=/tmp/wplzproj
rm -rf "$P" && mkdir -p "$P/node_modules" "$P/dist"
cp -r functions "$P/"
cp -r 404.html _headers _redirects apple-touch-icon.png favicon.ico favicon.svg img index.html robots.txt \
      site.webmanifest sitemap.xml styles.css "$KEY.txt" hvac plumbing electrical pressure-washing cleaning blog \
      js thanks terms privacy refunds guides "$P/dist/"
[ -d m ] && cp -r m "$P/dist/"   # private mockups (git-ignored, built locally)
cd "$P"
CLOUDFLARE_ACCOUNT_ID=4003c9642a148a5b37a27b76397886ce npx -y wrangler@3 pages deploy dist \
  --project-name websiteplz --branch main --commit-dirty=true
