#!/usr/bin/env python3
"""Shrink the /events/ section from 25 pages to 5 (November 2026).

Why: NightWatch shows 97 of 98 tracked keywords out of the top 100 since
October, and the events section was the clearest off-topic, templated block on
the site: ~900-word guides to trade shows unrelated to a Turkey DMC (AIME
Melbourne, Money20/20, Web Summit...) plus three near-identical IMEX Frankfurt
pages and year/category/city listing pages.

Kept: /events/ (calendar hub), /events/imex-frankfurt/ (absorbs the 2026 and
2027 editions), /events/wtm-london-2026/, /events/ibtm-world-2026/,
/events/itb-berlin-2026/ — the major travel-trade shows where international
MICE buyers source DMCs.

Removed pages 301 to the closest kept page. Links to them are rewritten to that
page, or unwrapped to plain text when the only fallback is the hub.

Usage: python3 tools/events_consolidate.py   (no-op once applied)
"""

import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://dmcturkeypartner.com"
HUB = "/events/"

KEPT = ["imex-frankfurt", "wtm-london-2026", "ibtm-world-2026", "itb-berlin-2026"]

REMOVED = {
    "imex-frankfurt-2026": "/events/imex-frankfurt/",
    "imex-frankfurt-2027": "/events/imex-frankfurt/",
    "frankfurt": "/events/imex-frankfurt/",
    "berlin": "/events/itb-berlin-2026/",
    "london": "/events/wtm-london-2026/",
    "2026": HUB,
    "2027": HUB,
    "mice": HUB,
    "conferences": HUB,
    "incentive-travel": HUB,
    "business-travel": HUB,
    "aime-2026": HUB,
    "atm-dubai-2026": HUB,
    "business-travel-show-europe-2026": HUB,
    "international-confex-2026": HUB,
    "itb-asia-2026": HUB,
    "imex-america-2026": HUB,
    "money20-20-europe-2026": HUB,
    "the-meetings-show-2026": HUB,
    "web-summit-2026": HUB,
}

# /events/germany/ already redirected to /events/frankfurt/; point it straight
# at the final page so there is no redirect chain.
RETARGET = {"/events/germany": "/events/imex-frankfurt/", "/events/germany/:path*": "/events/imex-frankfurt/"}


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as handle:
        return handle.read()


def write(rel, text):
    with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as handle:
        handle.write(text)


def removed_path(href):
    path = href.replace(SITE, "")
    m = re.fullmatch(r"/events/([a-z0-9-]+)/(#.*)?", path)
    if m and m.group(1) in REMOVED:
        return m.group(1)
    return None


ANCHOR = re.compile(r'<a\b[^>]*\bhref="([^"]+)"[^>]*>(.*?)</a>', re.S)


def fix_links(text, own):
    # 1. Event cards in the hub grid for removed events. The IMEX 2026 card is
    #    repointed to the evergreen IMEX page; the rest are dropped.
    def card(m):
        block = m.group(0)
        first = re.search(r'href="([^"]+)"', block)
        slug = removed_path(first.group(1)) if first else None
        if not slug:
            return block
        if REMOVED[slug] == own and own != HUB:
            # An edition card on its own evergreen page: keep the facts, drop the links.
            block = re.sub(r'[ \t]*<a class="event-card__link"[^>]*>.*?</a>\n', "", block, flags=re.S)
            return ANCHOR.sub(lambda a: a.group(2), block)
        if slug == "imex-frankfurt-2026":
            return block.replace('href="/events/imex-frankfurt-2026/"', 'href="/events/imex-frankfurt/"')
        return ""

    text = re.sub(r'[ \t]*<li class="event-card"[^>]*>.*?</li>\n', card, text, flags=re.S)

    # 2. Browse-by sections that only list removed listing pages.
    def browse(m):
        hrefs = re.findall(r'href="([^"]+)"', m.group(0))
        if hrefs and all(removed_path(h) or h.rstrip("/").endswith("/events/germany") for h in hrefs):
            return ""
        return m.group(0)

    text = re.sub(
        r'[ \t]*<section class="page-section">\s*<h2>Browse by [^<]*</h2>.*?</section>\n\n?',
        browse, text, flags=re.S,
    )

    # 3. List items and link rows: drop removed links outright.
    text = re.sub(
        r'[ \t]*<li>\s*<a\b[^>]*href="(?:%s)?/events/(?:%s)/"[^>]*>[^<]*</a>[^<]*</li>\n'
        % (re.escape(SITE), "|".join(map(re.escape, REMOVED))),
        "", text,
    )

    def row(m):
        if not any(removed_path(a.group(1)) or a.group(1).rstrip("/").endswith("/events/germany")
                   for a in ANCHOR.finditer(m.group(2))):
            return m.group(0)
        kept = []
        for a in ANCHOR.finditer(m.group(2)):
            if removed_path(a.group(1)) or a.group(1).rstrip("/").endswith("/events/germany"):
                continue
            kept.append(a.group(0))
        sep = "\n          " if "\n" in m.group(2) else ""
        inner = (sep + sep.join(kept) + ("\n        " if sep else "")) if kept else ""
        return m.group(1) + inner + m.group(3)

    text = re.sub(r'(<(?:p|div) class="cluster-links">)(.*?)(</(?:p|div)>)', row, text, flags=re.S)
    text = re.sub(r'[ \t]*<(p|div) class="cluster-links">\s*</\1>\n', "", text)

    # 4. Everything else: repoint to the kept page, or unwrap to text.
    def inline(m):
        slug = removed_path(m.group(1))
        if not slug:
            if m.group(1).rstrip("/").endswith("/events/germany"):
                return m.group(0).replace(m.group(1), "/events/imex-frankfurt/")
            return m.group(0)
        target = REMOVED[slug]
        if target == HUB or target == own:
            return m.group(2)
        return m.group(0).replace(m.group(1), target)

    return ANCHOR.sub(inline, text)


def prune_filters(text):
    """Drop calendar filter options that no longer match any card."""
    cards = re.findall(r'<li class="event-card"[^>]*>', text)
    present = {"year": set(), "city": set(), "category": set()}
    for c in cards:
        for key in present:
            m = re.search(r'data-%s="([^"]*)"' % key, c)
            if m:
                present[key].update(m.group(1).split())
                present[key].add(m.group(1))

    def option(m):
        value = m.group(1)
        if not value:
            return m.group(0)
        for values in present.values():
            if value in values:
                return m.group(0)
        return ""

    return re.sub(r'[ \t]*<option value="([^"]*)">[^<]*</option>\n', option, text)


def html_files():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
        for name in files:
            if name.endswith(".html"):
                yield os.path.relpath(os.path.join(base, name), ROOT)


def redirects():
    data = json.loads(read("vercel.json"))
    for r in data["redirects"]:
        if r["source"] in RETARGET:
            r["destination"] = RETARGET[r["source"]]
    have = {r["source"] for r in data["redirects"]}
    for slug, target in REMOVED.items():
        for source in ("/events/%s" % slug, "/events/%s/:path*" % slug):
            if source not in have:
                data["redirects"].append({"source": source, "destination": target, "statusCode": 301})
    write("vercel.json", json.dumps(data, indent=2, ensure_ascii=False) + "\n")

    text = read("_redirects")
    text = text.replace("/events/germany/* /events/frankfurt/ 301!", "/events/germany/* /events/imex-frankfurt/ 301!")
    text = text.replace("/events/germany /events/frankfurt/ 301!", "/events/germany /events/imex-frankfurt/ 301!")
    if "Events section consolidation" not in text:
        lines = ["", "# Events section consolidation (Nov 2026): 25 pages reduced to 5."]
        for slug, target in REMOVED.items():
            lines += ["/events/%s/* %s 301!" % (slug, target), "/events/%s %s 301!" % (slug, target)]
        text = text.rstrip("\n") + "\n" + "\n".join(lines) + "\n"
    write("_redirects", text)


def sitemap():
    text = read("sitemap-events.xml")

    def drop(m):
        loc = re.search(r"<loc>([^<]+)</loc>", m.group(0)).group(1)
        return "" if removed_path(loc) else m.group(0)

    write("sitemap-events.xml", re.sub(r"[ \t]*<url>.*?</url>\n", drop, text, flags=re.S))


def main():
    for slug in REMOVED:
        path = os.path.join(ROOT, "events", slug)
        if os.path.isdir(path):
            shutil.rmtree(path)
    changed = 0
    for rel in html_files():
        own = "/" + os.path.dirname(rel) + "/"
        text = read(rel)
        new = fix_links(text, own)
        if rel == "events/index.html":
            new = prune_filters(new)
        if new != text:
            write(rel, new)
            changed += 1
    redirects()
    sitemap()
    print("removed %d event pages, rewrote links in %d files" % (len(REMOVED), changed))


if __name__ == "__main__":
    main()
