#!/usr/bin/env python3
"""Submit all site URLs to IndexNow after a deployment.

Run this script manually after deploying to Vercel:
    python3 tools/indexnow.py

IndexNow notifies Bing, Yandex, Seznam and (via Bing relay) other engines
within minutes of submission. Google has its own IndexNow endpoint which is
also included. Each URL is submitted at most once per run.

The IndexNow key and host are read from tools/site_config.py so there is a
single source of truth for both.
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
sys.path.insert(0, SCRIPT_DIR)
import site_config as cfg  # noqa: E402

KEY = cfg.INDEXNOW_KEY
HOST = "dmcturkeypartner.com"
KEY_URL = f"https://{HOST}/{KEY}.txt"

ENDPOINTS = [
    "https://www.bing.com/indexnow",
    "https://api.indexnow.org/indexnow",
]

NS = "http://www.sitemaps.org/schemas/sitemap/0.9"

# ---------------------------------------------------------------------------
# Collect URLs from all sitemaps
# ---------------------------------------------------------------------------

def collect_urls():
    urls = []
    for fname in sorted(os.listdir(ROOT)):
        if not (fname.startswith("sitemap-") and fname.endswith(".xml")):
            continue
        tree = ET.parse(os.path.join(ROOT, fname))
        for loc in tree.getroot().iter(f"{{{NS}}}loc"):
            url = loc.text.strip()
            if url not in urls:
                urls.append(url)
    return urls


# ---------------------------------------------------------------------------
# Submit to IndexNow endpoint
# ---------------------------------------------------------------------------

def submit(endpoint, urls):
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_URL,
        "urlList": urls,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status
    except urllib.error.HTTPError as exc:
        return exc.code


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not KEY:
        print("ERROR: INDEXNOW_KEY is not set in tools/site_config.py")
        sys.exit(1)

    urls = collect_urls()
    print(f"Collected {len(urls)} URLs from sitemaps")

    # IndexNow accepts up to 10,000 URLs per request; chunk just in case.
    chunk_size = 10_000
    chunks = [urls[i : i + chunk_size] for i in range(0, len(urls), chunk_size)]

    for endpoint in ENDPOINTS:
        for chunk in chunks:
            status = submit(endpoint, chunk)
            label = "OK" if status in (200, 202) else "WARN"
            print(f"  [{label}] {endpoint} → HTTP {status} ({len(chunk)} URLs)")

    print("Done.")


if __name__ == "__main__":
    main()
