#!/usr/bin/env python3
"""Site-wide CTA hygiene (November 2026 CTA audit).

Two marker-delimited, idempotent blocks:

1. Closing line — on every eligible page, a short line inside the page's
   closing CTA banner (or a small closing section when the page has none):
   "Prefer WhatsApp? Message our team · We reply within 1 business day."
   The reply promise is the one the site already makes elsewhere.
2. Hero CTA — on sales, cost, destination, event and insight pages whose hero
   has no conversion link: "Request a Proposal" + "Estimate Your Budget"
   directly under the H1 and its intro paragraphs.

Not touched: Czech/German pages (own WhatsApp routing and language), legal
pages, the proposal form itself, COP31 pages (they already carry WhatsApp
and a COP31-specific reply window), the group-hotel-offer and transfer-price pages, which
hotel_offers_build.py / transfer_prices_build.py regenerate in full (they have WhatsApp and a form),
and the Fam Trip 2027 pages, which deliberately promise no response time.

Usage: python3 tools/site_cta.py
"""

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cop31_common import whatsapp_url  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMISE = "We reply within 1 business day."
CLOSE_BEGIN, CLOSE_END = "<!-- site-cta-close:begin -->", "<!-- site-cta-close:end -->"
HERO_BEGIN, HERO_END = "<!-- site-cta-hero:begin -->", "<!-- site-cta-hero:end -->"

EXCLUDE = re.compile(r"^(cs|de|cop31-[^/]+|cookie-policy|privacy-policy|terms|request-proposal|group-hotel-offers-turkey|agency-fam-trip-2027|antalya-fam-trip-2027|antalya-transfer-prices)(/|$)")
HERO_PAGES = re.compile(
    r"^(mice-turkey|incentive-travel-turkey|corporate-events-turkey|group-travel-turkey|about|"
    r"event-costs(/[^/]+)?|destinations(/[^/]+)?|events(/[^/]+)?|insights/[^/]+)$"
)


def strip(text, begin, end):
    return re.sub(r"[ \t]*" + re.escape(begin) + r".*?" + re.escape(end) + r"\n?", "", text, flags=re.S)


def is_conversion(href):
    return (href.startswith("/request-proposal/") or "wa.me/" in href or href.startswith("/contact/")
            or href.startswith("/agency-fam-trip-2027/") or href.startswith("#"))


def wa_link(rel):
    message = "Hello, I'd like to discuss an event in Türkiye (from /%s)." % rel
    return ('<a href="%s" target="_blank" rel="noopener" data-track="site_whatsapp_click">'
            "Message our team on WhatsApp</a>" % whatsapp_url(message))


def closing(text, rel, main):
    has_wa = "wa.me/" in main
    line = ("Prefer WhatsApp? %s · %s" % (wa_link(rel), PROMISE)) if not has_wa else PROMISE
    note = '%s<p class="cta-banner__note">%s</p>%s\n' % (CLOSE_BEGIN, line, CLOSE_END)
    banner = re.search(r'class="cta-banner[^"]*"', text[text.find("<main"):])
    if banner:
        start = text.find("<main") + banner.start()
        actions = re.compile(r'<div class="cta-banner__actions[^"]*">.*?</div>\n?', re.S).search(text, start)
        if actions and actions.start() - start < 4000:
            return text[:actions.end()] + ("" if text[actions.end() - 1] == "\n" else "\n") + "        " + note + text[actions.end():]
    section = ('    %s\n    <section class="page-section" data-cta-location="closing">\n'
               '      <p class="cta-banner__note"><a href="/request-proposal/">Request a proposal</a> · %s</p>\n'
               "    </section>\n    %s\n") % (
        CLOSE_BEGIN, ("Prefer WhatsApp? %s · %s" % (wa_link(rel), PROMISE)) if not has_wa else PROMISE, CLOSE_END)
    # Sit above the hotel-offers strip, which hotel_offers_build.py always
    # re-appends just before </main>; otherwise the two tools would keep
    # swapping order.
    marker = "    <!-- hotel-offers:begin -->"
    if marker in text:
        return text.replace(marker, section + marker, 1)
    return text.replace("  </main>", section + "  </main>", 1)


def hero(text):
    m = re.search(r"</h1>((?:\s*<p\b[^>]*>.*?</p>)*)", text, re.S)
    if not m:
        return text
    block = ('\n      %s\n      <div class="hero-actions" data-cta-location="hero">'
             '<a class="btn btn--primary" href="/request-proposal/">Request a Proposal</a>'
             '<a class="btn btn--ghost" href="/event-cost-calculator/" data-track="hero_calculator_click">Estimate Your Budget</a>'
             "</div>\n      %s") % (HERO_BEGIN, HERO_END)
    return text[:m.end()] + block + text[m.end():]


def main():
    changed = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True)):
        rel = os.path.relpath(os.path.dirname(path), ROOT)
        rel = "" if rel == "." else rel
        if "node_modules" in path or EXCLUDE.match(rel):
            continue
        with open(path, encoding="utf-8") as handle:
            original = handle.read()
        if 'name="robots" content="noindex' in original:
            continue
        text = strip(strip(original, CLOSE_BEGIN, CLOSE_END), HERO_BEGIN, HERO_END)
        main_m = re.search(r"<main[^>]*>(.*?)</main>", text, re.S)
        if not main_m:
            continue
        main_html = main_m.group(1)
        # "Above the fold" = up to the second <h2>: many pages open with a
        # short intro section whose CTA sits right under its first heading.
        heads = [m.start() for m in re.finditer(r"<h2", main_html)]
        hero_html = main_html if len(heads) < 2 else main_html[:heads[1]]
        if HERO_PAGES.match(rel) and not any(is_conversion(h) for h in re.findall(r'href="([^"]+)"', hero_html)):
            text = hero(text)
        text = closing(text, rel, main_html)
        if text != original:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(text)
            changed += 1
    print("site CTA blocks updated on %d pages" % changed)


if __name__ == "__main__":
    main()
