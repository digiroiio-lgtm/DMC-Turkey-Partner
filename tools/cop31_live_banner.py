#!/usr/bin/env python3
"""COP31 live-period banner (9–20 November 2026).

A thin strip above the site header on the homepage and every COP31 page,
pointing urgent requests to the Antalya operations desk on WhatsApp and to
/cop31-last-minute-services/. Styles are inline in the marker block so the
strip needs no CSS deploy and disappears completely when removed.

Usage:
    python3 tools/cop31_live_banner.py           # add or refresh the banner
    python3 tools/cop31_live_banner.py --remove  # take it down after 20 November

Idempotent: re-running replaces the block instead of stacking copies.
"""

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cop31_common import whatsapp_url  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BEGIN = "<!-- cop31-live:begin -->"
END = "<!-- cop31-live:end -->"
BLOCK_RE = re.compile(r"[ \t]*" + re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n", re.S)
HEADER = '  <header class="site-header">'

# Confirmed by the business: replies within 30 minutes, 08:00–22:00 Antalya time.
RESPONSE = "WhatsApp replies within 30 minutes, 08:00–22:00 Antalya time."
WA_MESSAGE = "Hello, we need urgent local support at COP31 Antalya. Our requirement: "

STYLE = (
    ".cop31-live{background:#14171c;color:#fff;font-size:.875rem;line-height:1.45}"
    ".cop31-live__inner{max-width:1440px;margin:0 auto;padding:.55rem 20px;display:flex;"
    "flex-wrap:wrap;gap:.3rem 1.1rem;align-items:center;justify-content:center;text-align:center}"
    ".cop31-live a{color:#b7ff00;font-weight:600;text-decoration:underline;"
    "text-underline-offset:2px}"
    ".cop31-live a:focus-visible{outline:2px solid #b7ff00;outline-offset:2px}"
)


def block():
    return (
        "  " + BEGIN + "\n"
        "  <style>" + STYLE + "</style>\n"
        '  <div class="cop31-live" role="region" aria-label="COP31 urgent support">'
        '<div class="cop31-live__inner">'
        "<span><strong>COP31 Antalya, 9–20 November.</strong> Urgent local support? "
        + RESPONSE + "</span>"
        '<a href="' + whatsapp_url(WA_MESSAGE) + '" target="_blank" rel="noopener" '
        'data-track="cop31_whatsapp_click">WhatsApp the Antalya desk</a>'
        '<a href="/cop31-last-minute-services/">Last-minute services</a>'
        "</div></div>\n"
        "  " + END + "\n"
    )


def targets():
    paths = ["index.html"]
    paths += glob.glob(os.path.join(ROOT, "cop31-*", "index.html"))
    paths += glob.glob(os.path.join(ROOT, "cop31-news", "*", "index.html"))
    out = []
    for path in paths:
        rel = os.path.relpath(os.path.join(ROOT, path), ROOT)
        with open(os.path.join(ROOT, rel), encoding="utf-8") as handle:
            text = handle.read()
        if 'name="robots" content="noindex' in text:
            continue  # redirect stubs
        out.append(rel)
    return sorted(set(out))


def main():
    remove = "--remove" in sys.argv
    changed = 0
    for rel in targets():
        full = os.path.join(ROOT, rel)
        with open(full, encoding="utf-8") as handle:
            original = handle.read()
        text = BLOCK_RE.sub("", original)
        if not remove:
            if HEADER not in text:
                raise SystemExit("No site header in %s" % rel)
            text = text.replace(HEADER, block() + HEADER, 1)
        if text != original:
            with open(full, "w", encoding="utf-8") as handle:
                handle.write(text)
            changed += 1
    print("%s banner: %d files changed" % ("removed" if remove else "applied", changed))


if __name__ == "__main__":
    main()
