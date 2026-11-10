#!/usr/bin/env python3
"""Show delivered projects from /selected-works/ on the commercial pages.

Selected Works is the site's most original content (29 documented projects
with event photos), but no service or destination page linked to it. This adds
a short "Recent projects" block with 3 relevant projects to each mapped page,
just before its FAQ. Titles, categories, venues and photos are read from the
project pages themselves, so nothing here is new copy.

Only Antalya-region projects exist today, so Istanbul, Bodrum and Cappadocia
pages get no block rather than unrelated examples.

Usage: python3 tools/project_cards.py   (idempotent; re-running refreshes the blocks)
"""

import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BEGIN = "<!-- project-cards:begin -->"
END = "<!-- project-cards:end -->"

PAGES = {
    "dmc-turkey": ["turk-telekom-business-partners-meeting", "23rd-national-surgery-congress", "anadolu-sigorta-100th-anniversary"],
    "mice-turkey": ["23rd-national-surgery-congress", "turkiye-is-bankasi-aktob-conference", "vakifbank-management-summit-titanic-belek"],
    "corporate-events-turkey": ["turk-telekom-business-partners-meeting", "mapfre-sigorta-corporate-event", "temsa-corporate-event-calista-belek"],
    "incentive-travel-turkey": ["bellona-dealer-meeting", "cw-enerji-dealer-sales-meeting", "eksim-holding-management-summit"],
    "services/event-production": ["anadolu-sigorta-100th-anniversary", "ets-holiday-concerts-rixos-sungate", "dosso-dossi-fashion-show"],
    "services/meetings-conferences": ["23rd-national-surgery-congress", "turkiye-is-bankasi-aktob-conference", "tusas-management-summit-fayrap-2026"],
    "services/incentive-programs": ["bellona-dealer-meeting", "cw-enerji-dealer-sales-meeting", "barikat-2-0-xanadu-belek"],
    "destinations/antalya": ["mapfre-sigorta-corporate-event", "turkiye-is-bankasi-aktob-conference", "tusas-management-summit-fayrap-2026"],
    "destinations/belek": ["23rd-national-surgery-congress", "vakifbank-management-summit-titanic-belek", "temsa-corporate-event-calista-belek"],
}

FAQ_HEADING = re.compile(r"<h2>[^<]*(?:FAQ|Frequently Asked Questions)[^<]*</h2>")
BLOCK_RE = re.compile(r"[ \t]*" + re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n", re.S)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as handle:
        return handle.read()


def project(slug):
    text = read("selected-works/%s/index.html" % slug)
    title = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.S).group(1)
    title = re.sub(r"<[^>]+>", "", title).strip()
    desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', text).group(1))
    # "Name delivered by ... — Category · Venue · Location." or "Name at Venue, City: ..."
    m = re.search(r"—\s*([^—]+?)\.?$", desc)
    if m and "·" in m.group(1):
        meta = m.group(1).strip()
    else:
        m = re.search(r" at ([^:]+):", desc)
        meta = m.group(1).strip() if m else ""
    img = None
    for tag in re.findall(r"<img\b[^>]*>", text):
        src = re.search(r'src="([^"]+)"', tag).group(1)
        if "/brand/" in src or not src.startswith("/assets/img/"):
            continue
        small = re.search(r'([^\s",]+-640\.webp) 640w', tag)
        alt = re.search(r'alt="([^"]*)"', tag)
        img = (small.group(1) if small else src, alt.group(1) if alt else title)
        break
    return {"slug": slug, "title": title, "meta": html.escape(meta, quote=False), "img": img}


def block(slugs):
    cards = []
    for p in map(project, slugs):
        pic = ""
        if p["img"]:
            pic = ('<img src="%s" alt="%s" width="640" height="438" loading="lazy" decoding="async" '
                   'style="width:100%%;height:auto;aspect-ratio:640/438;object-fit:cover;border-radius:4px;margin-bottom:.75rem">'
                   % p["img"])
        cards.append(
            '<article class="card">%s<h3><a href="/selected-works/%s/">%s</a></h3><p>%s</p></article>'
            % (pic, p["slug"], p["title"], p["meta"])
        )
    return (
        "    " + BEGIN + "\n"
        '    <section class="page-section" id="recent-projects">\n'
        "      <h2>Recent Projects We Delivered</h2>\n"
        '      <p class="page-section__lede">Documented with photos and scope in '
        '<a href="/selected-works/">Selected Works</a>.</p>\n'
        '      <div class="card-grid">' + "".join(cards) + "</div>\n"
        "    </section>\n"
        "    " + END + "\n"
    )


def main():
    changed = 0
    for page, slugs in PAGES.items():
        rel = page + "/index.html"
        original = read(rel)
        text = BLOCK_RE.sub("", original)
        m = FAQ_HEADING.search(text)
        if not m:
            raise SystemExit("No FAQ section on %s" % rel)
        at = text.rfind("<section", 0, m.start())
        line_start = text.rfind("\n", 0, at) + 1
        text = text[:line_start] + block(slugs) + text[line_start:]
        if text != original:
            with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as handle:
                handle.write(text)
            changed += 1
    print("project cards on %d pages (%d changed)" % (len(PAGES), changed))


if __name__ == "__main__":
    main()
